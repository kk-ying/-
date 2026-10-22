# -*- coding: utf-8 -*-
"""
05 销售额与增长率组合分析 —— 组合图（柱形 + 折线，双坐标轴）
对应 PPT 第24页组合图章节
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.14, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    categories = ['1月', '2月', '3月', '4月', '5月', '6月']
    sales = [120, 132, 101, 134, 90, 230]
    growth_rate = [5.2, 10.0, -23.5, 32.7, -32.8, 155.6]

    fig, ax1 = plt.subplots(figsize=(9, 5))

    bars = ax1.bar(categories, sales, color='#4472C4', alpha=0.8, label='销售额（万元）')
    ax1.set_ylabel('销售额（万元）', color='#4472C4', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#4472C4')
    ax1.set_ylim(0, max(sales) * 1.3)

    ax2 = ax1.twinx()
    ax2.plot(categories, growth_rate, color='#ED7D31', marker='o', linewidth=2.5, label='增长率（%）')
    ax2.set_ylabel('增长率（%）', color='#ED7D31', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#ED7D31')

    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 5,
                 f'{int(height)}', ha='center', va='bottom', fontsize=9, color='#4472C4')

    for i, v in enumerate(growth_rate):
        ax2.text(i, v + 5, f'{v}%', ha='center', fontsize=9, color='#ED7D31')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False)

    ax1.spines['top'].set_visible(False)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)

    add_title_and_note(
        ax1,
        title='销售额与增长率组合分析',
        subtitle='6月销售额与增长率同步达到峰值，5月出现双降',
        note='数据来源：2024年上半年经营数据'
    )

    plt.tight_layout()
    plt.savefig('chart_5_combo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_5_combo.png')


if __name__ == '__main__':
    main()
