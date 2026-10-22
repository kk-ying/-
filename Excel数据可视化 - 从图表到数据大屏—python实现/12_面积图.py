# -*- coding: utf-8 -*-
"""
12 面积图 —— 折线面积图
对应 PPT 第22-23页"折线面积图12例"：面积填充展示渠道构成与趋势变化
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
    months = [f'{i}月' for i in range(1, 13)]
    online = [42, 48, 55, 60, 72, 85, 95, 110, 125, 140, 158, 180]
    offline = [80, 75, 78, 70, 72, 68, 70, 65, 68, 62, 60, 58]

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.stackplot(x, online, offline,
                 labels=['线上渠道', '线下渠道'],
                 colors=['#4472C4', '#ED7D31'], alpha=0.75,
                 edgecolor='white')

    # 各渠道轮廓线
    ax.plot(x, online, color='#2f5597', linewidth=2)
    ax.plot(x, np.array(online) + np.array(offline),
            color='#C00000', linewidth=2, marker='o', markersize=4,
            label='全渠道合计')

    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.set_ylabel('销售额（万元）', fontsize=11)
    ax.set_xlim(0, len(months) - 1)
    ax.legend(loc='upper left', frameon=False, ncol=3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='线上与线下渠道月度销售趋势（面积图）',
        subtitle='线上渠道下半年增长强劲，全渠道销售规模稳步扩大',
        note='数据来源：2024年度渠道销售数据 | 面积图同时表达构成关系与时间趋势'
    )

    plt.tight_layout()
    plt.savefig('chart_12_area.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_12_area.png')


if __name__ == '__main__':
    main()
