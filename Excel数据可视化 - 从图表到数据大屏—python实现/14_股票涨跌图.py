# -*- coding: utf-8 -*-
"""
14 股票行情图 —— 涨/跌柱线
对应 PPT 第16页："涨/跌柱线，在折线图中连接两个系列同一轴标签下数据点的柱形，
常用于展示股票信息"。竖线表示最高-最低价，柱体表示开盘-收盘价（红涨绿跌）
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    days = ['周一', '周二', '周三', '周四', '周五']
    opens = [10.2, 10.6, 10.9, 10.5, 10.8]
    highs = [10.8, 11.0, 11.1, 10.9, 11.3]
    lows = [10.0, 10.5, 10.4, 10.3, 10.7]
    closes = [10.6, 10.9, 10.5, 10.8, 11.2]

    x = np.arange(len(days))
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for i in range(len(days)):
        up = closes[i] >= opens[i]
        color = '#C00000' if up else '#00B050'
        # 最高价-最低价竖线
        ax.vlines(x[i], lows[i], highs[i], color=color, linewidth=1.6)
        # 开盘-收盘价柱体（粗横线，模拟涨/跌柱）
        ax.vlines(x[i], opens[i], closes[i], color=color, linewidth=8, alpha=0.85)
        # 端点小横线
        ax.hlines([lows[i], highs[i]], x[i] - 0.08, x[i] + 0.08,
                  color=color, linewidth=1.6)
        ax.text(x[i], highs[i] + 0.07, f'{closes[i]:.1f}',
                ha='center', fontsize=9, color=color, fontweight='bold')

    legend_handles = [
        Line2D([0], [0], color='#C00000', linewidth=8, alpha=0.85, label='上涨（收≥开）'),
        Line2D([0], [0], color='#00B050', linewidth=8, alpha=0.85, label='下跌（收<开）'),
    ]
    ax.legend(handles=legend_handles, loc='upper left', frameon=False)

    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.set_ylabel('股价（元）', fontsize=11)
    ax.set_ylim(min(lows) - 0.35, max(highs) + 0.55)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='某股票五个交易日行情（涨/跌柱线图）',
        subtitle='周三收阴回调，其余四个交易日均收涨，周五收于周内最高价',
        note='数据来源：行情模拟数据 | 竖线=最高/最低价，柱体=开盘/收盘价（PPT 第16页涨跌柱线）'
    )

    plt.tight_layout()
    plt.savefig('chart_14_stock.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_14_stock.png')


if __name__ == '__main__':
    main()
