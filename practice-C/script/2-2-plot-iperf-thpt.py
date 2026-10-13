#!/usr/bin/env python3
""" 1秒区間ごとのiperf3スループットを折れ線グラフに描画 """

import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt


# 実行形式: python plot_iperf_throughput.py 入力ファイル [出力PNG]
if len(sys.argv) not in (2, 3):
    raise SystemExit(f"Usage: python {Path(sys.argv[0]).name} INPUT [OUTPUT.png]")

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("iperf-throughput.png")

# awk 整形済み形式: 0.00-1.00 2.09
simple_pattern = re.compile(
    r"^\s*([0-9.]+)-([0-9.]+)\s+([0-9.]+)\s*$"
)

# iperf3標準形式:
# [  7] 0.00-1.00 sec 256 KBytes 2.09 Mbits/sec
standard_pattern = re.compile(
    r"\[\s*\d+\]\s+([0-9.]+)-([0-9.]+)\s+sec\s+"
    r"[0-9.]+\s+[KMGT]?Bytes\s+([0-9.]+)\s+([KMGT]?)bits/sec"
)

# bitrateを Mbps へ変換する倍率
to_mbps = {"": 1e-6, "K": 1e-3, "M": 1.0, "G": 1e3, "T": 1e6}
times, throughputs = [], []

with input_path.open(encoding="utf-8", errors="ignore") as log_file:
    for line in log_file:
        simple_match = simple_pattern.match(line)
        standard_match = standard_pattern.search(line)

        if simple_match:
            start, end, mbps = map(float, simple_match.groups())
        elif standard_match:
            start, end, bitrate = map(float, standard_match.groups()[:3])
            unit = standard_match.group(4)
            mbps = bitrate * to_mbps[unit]
        else:
            # 接続情報やヘッダーなど、測定値以外の行は無視
            continue

        # 0.00-120.00などのsender/receiver集計行を除外
        if not 0.5 <= end - start <= 1.5:
            continue

        # 各1秒区間の中央時刻を、その区間の代表時刻として利用
        times.append((start + end) / 2)
        throughputs.append(mbps)

if not throughputs:
    raise SystemExit("スループットデータを読み込めませんでした。")

# 横軸を時間、縦軸をスループットとして描画
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(times, throughputs, linewidth=1.4, color="tab:blue")
ax.set(
    title="iperf3 Throughput over Time",
    xlabel="Time [s]",
    ylabel="Bitrate (Throughput) [Mbps]",
)
ax.grid(alpha=0.3)
ax.set_xlim(times[0], times[-1])

# レイアウトを調整し、PNGとして保存
fig.tight_layout()
fig.savefig(output_path, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"samples={len(throughputs)}")
print(f"output={output_path.resolve()}")