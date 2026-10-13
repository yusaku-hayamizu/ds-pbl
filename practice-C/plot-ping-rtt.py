#!/usr/bin/env python3
""" ping ログから RTT を抽出し、時間変化を折れ線グラフとして描画するプログラム

処理の流れ:
1. 各行から ``icmp_seq`` と ``time`` を正規表現で抽出
2. ``icmp_seq × 測定間隔`` により、sequence番号を経過時間へ変換
3. 経過時間を横軸、RTT [ms]を縦軸としてMatplotlibで描画
4. グラフをPNGファイルとして保存
"""

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt


# ログ1行から必要な数値を取り出すための正規表現。
# ``?P<seq>`` と ``?P<rtt>`` は、後から名前で値を取得するためのグループ名
PING_PATTERN = re.compile(
    # 通常形式（time=12.3 ms）と簡略形式（time=12.3）の両方に対応
    r"icmp_seq=(?P<seq>\d+).*?time=(?P<rtt>[0-9.]+)(?:\s*ms)?"
)


def load_ping_log(log_path: Path) -> tuple[list[int], list[float]]:
    """pingログからicmp_seqとRTTを読み込み

    Parameters
    ----------
    log_path:
        読み込むpingログのパス

    Returns
    -------
    sequences:
        抽出したicmp_seqの一覧
    rtts:
        抽出したRTT [ms]の一覧
    """
    # 同じ位置の要素が対応する2つのリストとして保持
    # 例: sequences[0]のRTTはrtts[0]に格納
    sequences: list[int] = []
    rtts: list[float] = []

    # errors="ignore"により、ログに不正な文字が含まれても読み込みを継続
    with log_path.open("r", encoding="utf-8", errors="ignore") as log_file:
        for line in log_file:
            # 現在の行がping測定結果なら、seqとRTTを取得
            match = PING_PATTERN.search(line)
            if match:
                sequences.append(int(match.group("seq")))
                rtts.append(float(match.group("rtt")))

    # 対象行が1件もなければ、空のグラフを作らずエラーとして通知
    if not sequences:
        raise ValueError(f"RTTデータを抽出できませんでした: {log_path}")

    return sequences, rtts


def plot_rtt(
    sequences: list[int],
    rtts: list[float],
    interval_seconds: float,
    output_path: Path,
    show: bool,
) -> None:
    """RTTの時間変化を描画し、画像ファイルへ保存する。"""

    # sequence番号を経過時間[秒]へ変換
    # interval_seconds=0.1としているので、seq=10は1.0秒に変換
    # sequence番号を直接利用するため、途中のseqが欠けても時間位置はずれない
    elapsed_seconds = [seq * interval_seconds for seq in sequences]

    # 12×5インチの描画領域を作成する。
    fig, ax = plt.subplots(figsize=(12, 5))

    # 経過時間とRTTを折れ線で結ぶ
    ax.plot(
        elapsed_seconds,
        rtts,
        color="tab:blue",
        linewidth=1.0,
    )

    # タイトル、軸ラベル、補助線を設定
    ax.set_title("Ping RTT over Time")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("RTT (time) [ms]")
    ax.grid(True, alpha=0.3)

    # 横軸の表示範囲を最初から最後の測定時刻までに限定
    ax.set_xlim(elapsed_seconds[0], elapsed_seconds[-1])

    # ラベルが画像外にはみ出さないよう調整してからPNGとして保存
    fig.tight_layout()
    fig.savefig(output_path, dpi=160, bbox_inches="tight")

    # 処理結果を端末に表示
    print(f"samples={len(rtts)}")
    print(f"time_range={elapsed_seconds[0]:.1f}-{elapsed_seconds[-1]:.1f} s")
    print(f"output={output_path.resolve()}")

    # --showが指定された場合だけウィンドウを表示
    # 指定されていない場合は、使用した描画領域を明示的に解放
    if show:
        plt.show()
    else:
        plt.close(fig)


def main() -> None:
    """コマンドライン引数を処理し、ログの読み込みと描画を実行 """

    # argparseを使うことで、入力ファイルや出力先を実行時に変更可
    parser = argparse.ArgumentParser(
        description="Plot ping RTT with icmp_seq converted to elapsed time."
    )
    parser.add_argument("log_file", type=Path, help="pingログファイル")
    parser.add_argument(
        "--interval",
        type=float,
        default=0.1,
        help="1 icmp_seqあたりの秒数（今回は既定値: 0.1）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ping-rtt-01s.png"),
        help="出力画像のパス",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="保存後にグラフを画面表示",
    )
    args = parser.parse_args()

    # 0秒以下の測定間隔では時間軸を作れないため、事前に検査
    if args.interval <= 0:
        raise ValueError("--intervalには0より大きい値を指定してください。")

    # ログを読み込み
    sequences, rtts = load_ping_log(args.log_file)

    # 出力先のディレクトリが存在しない場合は自動的に作成
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # 読み込んだデータをグラフ化
    plot_rtt(sequences, rtts, args.interval, args.output, args.show)


# このファイルが直接実行されたときだけmain()を呼び出す（他のPythonコードからimportされた時は自動実行されない）
if __name__ == "__main__":
    main()
