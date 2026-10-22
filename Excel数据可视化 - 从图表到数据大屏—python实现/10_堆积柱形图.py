# -*- coding: utf-8 -*-
"""
10 堆积柱形图 —— 1 个度量值 + 2 个维度
对应 PPT 第7页"图表数据的基本结构"：各商品四个季度销量，使用轴坐标和颜色区分类别
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
        ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    products = ['产品 A', '产品 B', '产品 C', '产品 D']
    quarters = ['第一季度', '第二季度', '第三季度', '第四季度']
    data = np.array([
        [120, 90, 70, 60],    # 第一季度
        [140, 110, 80, 70],   # 第二季度
        [100, 130, 90, 50],   # 第三季度
        [170, 120, 110, 90],  # 第四季度
    ])

    x = np.arange(len(products))
    fig, ax = plt.subplots(figsize=(9, 5.5))

    bottom = np.zeros(len(products))
    for q, row in zip(quarters, data):
        ax.bar(x, row, width=0.55, bottom=bottom, label=q,
               color=colors_primary[quarters.index(q)], edgecolor='white')
        # 段内数据标签
        for xi, val, b in zip(x, row, bottom):
            if val > 0:
                ax.text(xi, b + val / 2, f'{val}', ha='center', va='center',
                        fontsize=9, color='white', fontweight='bold')
        bottom += row

    # 顶部总量标签
    totals = data.sum(axis=0)
    for xi, t in zip(x, totals):
        ax.text(xi, t + 8, f'合计 {t}', ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='#333333')

    ax.set_xticks(x)
    ax.set_xticklabels(products)
    ax.set_ylabel('销售量（件）', fontsize=11)
    ax.set_ylim(0, totals.max() * 1.15)
    ax.legend(loc='upper right', frameon=False, ncol=4, bbox_to_anchor=(1, 1.02))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='各产品分季度销售量（堆积柱形图）',
        subtitle='产品 A 全年销量最高；各产品第四季度均有明显增长',
        note='数据来源：2024年度销售统计 | 一个度量值（销售量）+ 两个维度（产品、季度）'
    )

    plt.tight_layout()
    plt.savefig('chart_10_stacked_column.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_10_stacked_column.png')


if __name__ == '__main__':
    main()
