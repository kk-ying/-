# -*- coding: utf-8 -*-
"""
02 季度销售额构成 —— 饼图（构成关系）
对应 PPT 第8页"构成"关系示例数据
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

colors_pie = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']


def add_title_and_note(ax, title, subtitle=None, note=None):
    ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=14, fontweight='bold')
    if subtitle:
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=10, color='#555555')
    if note:
        ax.text(0, -0.14, note, transform=ax.transAxes, fontsize=8, color='#888888')


def main():
    quarters = ['第一季度', '第二季度', '第三季度', '第四季度']
    values = [8.2, 3.2, 1.4, 1.2]

    fig, ax = plt.subplots(figsize=(7, 6))
    explode = (0.05, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(
        values, labels=quarters, autopct='%1.1f%%',
        colors=colors_pie, explode=explode,
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.8, edgecolor='white')
    )

    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
        autotext.set_color('white')

    add_title_and_note(
        ax,
        title='季度销售额构成',
        subtitle='第一季度占比超过一半，第四季度占比最低',
        note='数据来源：2024年度财务报表 | 单位：百万元'
    )

    plt.tight_layout()
    plt.savefig('chart_2_quarterly_pie.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_2_quarterly_pie.png')


if __name__ == '__main__':
    main()
