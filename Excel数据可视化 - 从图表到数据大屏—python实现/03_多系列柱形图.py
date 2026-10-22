# -*- coding: utf-8 -*-
"""
03 多系列数据比较 —— 分组柱形图（比较关系）
对应 PPT 第8页"比较"关系示例数据
"""

import matplotlib.pyplot as plt
import numpy as np

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

    x = np.arange(len(categories))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width, series1, width, label='系列 1', color=colors_primary[0])
    ax.bar(x, series2, width, label='系列 2', color=colors_primary[1])
    ax.bar(x + width, series3, width, label='系列 3', color=colors_primary[2])

    ax.legend(loc='upper right', frameon=False)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('数值')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='多系列数据比较',
        subtitle='系列 3 在类别 4 表现突出，系列 2 在类别 2 达到峰值',
        note='数据来源：实验测试数据'
    )

    plt.tight_layout()
    plt.savefig('chart_3_multi_column.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_3_multi_column.png')


if __name__ == '__main__':
    main()
