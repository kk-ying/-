# -*- coding: utf-8 -*-
"""
09 帕累托图 —— 分布（二八法则）
对应 PPT 第9页提到的"帕累托图"：降序柱形图 + 累计百分比折线 + 80% 参考线
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    reasons = ['外观划痕', '功能异常', '包装破损', '配件缺失', '其他问题']
    counts = [42, 31, 17, 6, 4]
    total = sum(counts)
    cumulative = np.cumsum(counts) / total * 100

    fig, ax1 = plt.subplots(figsize=(9, 5.5))

    bars = ax1.bar(reasons, counts, color='#4472C4', width=0.6,
                   edgecolor='white', label='缺陷数量')
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.8,
                 f'{int(height)}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold', color='#4472C4')

    ax1.set_ylabel('缺陷数量（个）', fontsize=11, color='#4472C4')
    ax1.tick_params(axis='y', labelcolor='#4472C4')
    ax1.set_ylim(0, max(counts) * 1.2)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax1.set_axisbelow(True)

    # 次坐标轴：累计百分比折线
    ax2 = ax1.twinx()
    ax2.plot(reasons, cumulative, color='#ED7D31', marker='o',
             linewidth=2.5, label='累计占比')
    for i, v in enumerate(cumulative):
        ax2.text(i, v + 5, f'{v:.0f}%', ha='center', fontsize=9,
                 color='#ED7D31', fontweight='bold')
    ax2.set_ylabel('累计占比（%）', fontsize=11, color='#ED7D31')
    ax2.tick_params(axis='y', labelcolor='#ED7D31')
    ax2.set_ylim(0, 110)
    ax2.spines['top'].set_visible(False)

    # 80% 关键参考线（二八法则）
    ax2.axhline(80, color='#C00000', linestyle='--', linewidth=1.2, alpha=0.8)
    ax2.text(len(reasons) - 0.5, 82, '80% 关键分界线',
             ha='right', fontsize=9, color='#C00000')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', frameon=False)

    add_title_and_note(
        ax1,
        title='产品质量缺陷原因帕累托分析',
        subtitle='前两项原因累计占比 73%，是质量改善的关键少数',
        note='数据来源：月度质量检验统计 | 帕累托图遵循"关键的少数，次要的多数"原则'
    )

    plt.tight_layout()
    plt.savefig('chart_9_pareto.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_9_pareto.png')


if __name__ == '__main__':
    main()
