# -*- coding: utf-8 -*-
"""
01 各区域销售量对比 —— 簇状柱形图
对应 PPT 第6页"三步建立专业图表"示例数据
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
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    sales = [2354, 1902, 3524, 2698, 2896, 2563]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(regions, sales, color=colors_primary[:len(regions)], width=0.6, edgecolor='white')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 50,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    add_title_and_note(
        ax,
        title='各区域销售量对比',
        subtitle='东北区域销量最高，华南区域相对较低',
        note='数据来源：2024年销售统计 | 单位：件'
    )

    ax.set_ylabel('销售量（件）', fontsize=11)
    ax.set_ylim(0, max(sales) * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig('chart_1_sales_column.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_1_sales_column.png')


if __name__ == '__main__':
    main()
