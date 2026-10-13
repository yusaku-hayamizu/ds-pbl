#!/usr/bin/env python3
""" 移動中央値とMADを使って、ping RTTの外れ値を検出・可視化

処理の流れ:
1. pingログからicmp_seqとRTTを読み込み
2. 各測定点の周辺にあるデータから移動中央値とMADを計算
3. 中央値から大きく離れたRTTを異常として判定
4. RTT、判定範囲、異常スコアをMatplotlibで可視化
"""

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_ping_log(log_path: Path) -> pd.DataFrame:
    """pingログからsequence番号とRTT [ms]を抽出
    ``icmp_seq=10`` と ``icmp_seq 10``、および
    ``time=12.3 ms`` と ``time<1 ms`` のような表記に対応
    """
    # 1番目のグループでicmp_seq、2番目のグループでRTTを取得
    pattern = re.compile(
        r"icmp_seq[= ](\d+).*?time[=<]([\d.]+)\s*ms"
    )

    records = []

    # 解釈できない文字がログ中にあっても処理を継続
    with log_path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = pattern.search(line)

            # ping応答行だけを測定データとして追加
            if match:
                records.append(
                    {
                        "seq": int(match.group(1)),
                        "rtt": float(match.group(2)),
                    }
                )

    # 空のDataFrameを後続処理へ渡さず、原因が分かるエラーを出力
    if not records:
        raise ValueError("pingログからRTTを抽出できませんでした。")

    # sequence番号順に並べ、行番号を0から採番
    return pd.DataFrame(records).sort_values("seq").reset_index(drop=True)


def calculate_mad(values: np.ndarray) -> float:
    """Median Absolute Deviation（中央絶対偏差）を計算

    MADは 各値と中央値との差の絶対値について、さらに中央値を取った値で、
    平均値と標準偏差よりも大きな外れ値の影響を受けにくい
    """
    median = np.median(values)
    return np.median(np.abs(values - median))


def detect_anomalies(
    df: pd.DataFrame,
    window_size: int = 31,
    threshold: float = 3.5,
) -> pd.DataFrame:
    """移動中央値とMADを使ってRTTの異常を判定

    Parameters
    ----------
    df:
        ``seq``列と``rtt``列を持つ測定データ
    window_size:
        各測定点の前後を評価する移動窓（ウィンドウ）の大きさで、中央窓なので奇数に設定
    threshold:
        Robust Z-score がこの値を超えた測定点を異常と検知
    """
    # 中央点と周辺データを含めるため、最低3点が必要
    if window_size < 3:
        raise ValueError("window_sizeは3以上にしてください。")

    # 偶数では窓の中央が1点に決まらないため、奇数だけを許可
    if window_size % 2 == 0:
        raise ValueError("中央移動窓を使うため、window_sizeは奇数にしてください。")

    # 入力DataFrameを変更しないよう、分析用のコピーを作成
    result = df.copy()

    # 各点を中心としたwindow_size件のRTTについて中央値を計算
    # 端では窓のデータ数が不足するため、結果は対象外 (NaN: Not a Number)
    result["rolling_median"] = (
        result["rtt"]
        .rolling(
            window=window_size,
            center=True,
            min_periods=window_size,
        )
        .median()
    )

    # 同じ移動窓についてMADを計算
    # raw=Trueにより、calculate_madにはNumPy配列を譲渡
    result["rolling_mad"] = (
        result["rtt"]
        .rolling(
            window=window_size,
            center=True,
            min_periods=window_size,
        )
        .apply(calculate_mad, raw=True)
    )

    # 正規分布を仮定した標準偏差に近い尺度へMADを変換
    # 1.4826は正規分布におけるMADの補正係数
    result["robust_sigma"] = 1.4826 * result["rolling_mad"]

    # MADが0の窓では除算できないため、一時的にNaNへ置き換え
    safe_sigma = result["robust_sigma"].replace(0, np.nan)

    # RTTが移動中央値から何sigma離れているかを表すRobust Z-score
    result["anomaly_score"] = (
        (result["rtt"] - result["rolling_median"]).abs()
        / safe_sigma
    )

    # グラフ表示用に、正常とみなすRTTの下限と上限を計算
    result["lower_limit"] = (
        result["rolling_median"]
        - threshold * result["robust_sigma"]
    )
    result["upper_limit"] = (
        result["rolling_median"]
        + threshold * result["robust_sigma"]
    )

    # スコアが指定した閾値を超えた測定点を異常と判断
    result["is_anomaly"] = result["anomaly_score"] > threshold

    return result


def plot_results(
    df: pd.DataFrame,
    threshold: float,
    output_path: Path,
) -> None:
    """RTTの判定結果と異常スコアを2段のグラフにする"""
    # 異常点だけを抽出し、赤い点として重ねて表示する
    anomalies = df[df["is_anomaly"]]

    # Matplotlibへ渡しやすいよう各列をNumPy配列に変換
    x = df["seq"].to_numpy()
    rtt = df["rtt"].to_numpy()
    rolling_median = df["rolling_median"].to_numpy()
    lower_limit = df["lower_limit"].to_numpy()
    upper_limit = df["upper_limit"].to_numpy()
    anomaly_score = df["anomaly_score"].to_numpy()

    # 上段をRTT、下段を異常スコアとして、横軸を共有
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(14, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    # --- 上段: RTT、移動中央値、正常範囲、異常点 ---
    axes[0].plot(x, rtt, color="steelblue", linewidth=1, label="RTT")
    axes[0].plot(
        x,
        rolling_median,
        color="darkorange",
        linewidth=2,
        label="Moving median",
    )
    axes[0].fill_between(
        x,
        lower_limit,
        upper_limit,
        color="orange",
        alpha=0.2,
        label="MAD threshold range",
    )
    axes[0].scatter(
        anomalies["seq"],
        anomalies["rtt"],
        color="red",
        marker="o",
        s=35,
        zorder=5,
        label="Anomaly",
    )
    axes[0].set_title("Ping RTT anomaly detection using moving median and MAD")
    axes[0].set_ylabel("RTT (ms)")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # --- 下段: Robust Z-scoreと異常判定の閾値 ---
    axes[1].plot(
        x,
        anomaly_score,
        color="purple",
        linewidth=1,
        label="MAD anomaly score",
    )
    axes[1].axhline(
        threshold,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Threshold = {threshold}",
    )
    axes[1].scatter(
        anomalies["seq"],
        anomalies["anomaly_score"],
        color="red",
        s=30,
        zorder=5,
    )

    # 通常の対数軸と異なり、0付近も表示できるsymlogを使用
    # 大きな異常スコアがあっても、通常範囲の変化を読み取りやすくする
    axes[1].set_yscale("symlog", linthresh=1)
    axes[1].set_xlabel(
        "Elapsed time (seconds, assuming one ping per second)"
    )
    axes[1].set_ylabel("Anomaly score")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # グラフ全体のタイトルに異常数と全測定数を表示
    fig.suptitle(
        f"Detected anomalies: {len(anomalies)} / {len(df)}",
        fontsize=12,
    )

    # レイアウトを整え、指定された画像ファイルへ保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def main() -> None:
    """引数を読み込み、ログ解析・異常検出・可視化を順に実行"""
    parser = argparse.ArgumentParser(
        description="Detect ping RTT anomalies using moving median and MAD."
    )

    # 入力ログは必須の位置引数として受け取る
    parser.add_argument(
        "log_file",
        type=Path,
        help="Path to the ping log file",
    )

    # 移動窓と判定閾値は必要に応じてコマンドラインから変更可能
    parser.add_argument(
        "--window",
        type=int,
        default=31,
        help="Moving-window size; must be odd (default: 31)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=3.5,
        help="Anomaly-score threshold (default: 3.5)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ping_rtt_mad.png"),
        help="Output image path",
    )
    args = parser.parse_args()

    # 1. pingログをDataFrameへ読み込み
    df = load_ping_log(args.log_file)

    # 2. 移動中央値とMADを計算して異常を判定
    result = detect_anomalies(
        df,
        window_size=args.window,
        threshold=args.threshold,
    )

    # 3. 検出結果を端末へ表示
    anomalies = result[result["is_anomaly"]]
    print(f"測定数: {len(result)}")
    print(f"異常検出数: {len(anomalies)}")

    if not anomalies.empty:
        print("\n検出された異常:")
        print(
            anomalies[
                ["seq", "rtt", "rolling_median", "anomaly_score"]
            ].to_string(index=False)
        )

    # 4. 分析結果をグラフ化して保存
    plot_results(
        result,
        threshold=args.threshold,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
