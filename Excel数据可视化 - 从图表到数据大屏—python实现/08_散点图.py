# -*- coding: utf-8 -*-
"""
08 散点图 —— 分布与联系
对应 PPT 第9页"图表类型的选择：分布 / 联系"，使用 PPT 内嵌散点图真实数据
散点图一般需要添加坐标轴标题（PPT 第16页）
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.18, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    # PPT 第9页内嵌散点图数据
    x_values = [0.7, 1.8, 2.6]
    y_values = [2.7, 3.2, 0.8]
    labels = ['样本 A', '样本 B', '样本 C']

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.scatter(x_values, y_values, s=160, color='#4472C4',
               edgecolor='white', linewidth=1.5, zorder=3)

    for x, y, lab in zip(x_values, y_values, labels):
        ax.annotate(f'{lab}\n({x}, {y})', xy=(x, y), xytext=(8, 10),
                    textcoords='offset points', fontsize=9, color='#333333')

    ax.set_xlabel('X 变量', fontsize=11)
    ax.set_ylabel('Y 变量', fontsize=11)
    ax.set_xlim(0, 3.4)
    ax.set_ylim(0, 4.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='变量 X 与变量 Y 的相关性分析',
        subtitle='三个样本分布较为分散，未呈现明显的线性相关模式',
        note='数据来源：PPT 第9页散点图示例 | 散点图用于展示数据分布及变量间联系'
    )

    plt.tight_layout()
    plt.savefig('chart_8_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_8_scatter.png')


if __name__ == '__main__':
    main()
