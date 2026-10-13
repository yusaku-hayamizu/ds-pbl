#!/usr/bin/env python3
"""1秒区間ごとのiperf3スループットを折れ線グラフ化"""

import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt


# 実行形式: python plot_iperf_throughput.py 入力ファイル [出力PNG]
if len(sys.argv) not in (2, 3):
    raise SystemExit(f"Usage: python {Path(sys.argv[0]).name} INPUT [OUTPUT.png]")

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("iperf-throughput.png")

# 例「0.00-1.00 2.09」から開始時刻、終了時刻、Mbpsを抽出
pattern = re.compile(r"^\s*([0-9.]+)-([0-9.]+)\s+([0-9.]+)\s*$")
times, throughputs = [], []

with input_path.open(encoding="utf-8", errors="ignore") as log_file:
    for line in log_file:
        match = pattern.match(line)
        if not match:
            continue

        start, end, mbps = map(float, match.groups())

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
