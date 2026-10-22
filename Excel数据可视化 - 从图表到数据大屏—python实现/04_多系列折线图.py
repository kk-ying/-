# -*- coding: utf-8 -*-
"""
04 多系列数据趋势变化 —— 折线图（趋势关系）
对应 PPT 第8页"趋势"关系示例数据
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

colors_primary = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47']


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.14, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    categories = ['类别 1', '类别 2', '类别 3', '类别 4']
    series1 = [4.3, 2.5, 3.5, 4.5]
    series2 = [2.4, 4.4, 1.8, 2.8]
    series3 = [2.0, 2.0, 3.0, 5.0]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(categories, series1, marker='o', linewidth=2.5, label='系列 1', color=colors_primary[0])
    ax.plot(categories, series2, marker='s', linewidth=2.5, label='系列 2', color=colors_primary[1])
    ax.plot(categories, series3, marker='D', linewidth=2.5, label='系列 3', color=colors_primary[2])

    for i, s in enumerate([series1, series2, series3]):
        for j, v in enumerate(s):
            ax.text(j, v + 0.15, f'{v}', ha='center', fontsize=9, color=colors_primary[i])

    ax.legend(loc='upper left', frameon=False)
    ax.set_ylabel('数值')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='多系列数据趋势变化',
        subtitle='系列 3 呈上升趋势，系列 2 波动较大',
        note='数据来源：实验测试数据'
    )

    plt.tight_layout()
    plt.savefig('chart_4_multi_line.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_4_multi_line.png')


if __name__ == '__main__':
    main()
