# -*- coding: utf-8 -*-
"""
06 产品销量排名 —— 水平条形图（渐变色）
对应 PPT 第19页条形图修饰方式（渐变填充、间隙宽度）
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

colors_gradient = ['#1f4e79', '#2e75b6', '#5b9bd5', '#9dc3e6', '#bdd7ee', '#deebf7']


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.14, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    products = ['产品 A', '产品 B', '产品 C', '产品 D', '产品 E', '产品 F']
    values = [4200, 3800, 3200, 2800, 2100, 1500]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(products, values, color=colors_gradient[:len(products)], edgecolor='white', height=0.6)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 80, bar.get_y() + bar.get_height() / 2.,
                f'{int(width)}', ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_xlim(0, max(values) * 1.2)
    ax.set_xlabel('销售量（件）', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    ax.invert_yaxis()

    add_title_and_note(
        ax,
        title='产品销量排名',
        subtitle='产品 A 销量领先，产品 F 有待提升',
        note='数据来源：2024年Q3销售数据'
    )

    plt.tight_layout()
    plt.savefig('chart_6_horizontal_bar.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_6_horizontal_bar.png')


if __name__ == '__main__':
    main()
