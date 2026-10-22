# -*- coding: utf-8 -*-
"""
15 KPI 单值卡片图 —— 1 个度量值、0 个轴标签
对应 PPT 第7页"图表数据的基本结构"：卡片图，度量某一个指标，常用于数据大屏
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def main():
    # (指标名, 数值, 单位, 主题色, 同比文字, 是否向好)
    kpis = [
        ('总销售量', '12,537', '件', '#4472C4', '▲ 12.4%', True),
        ('总销售额', '1,245', '万元', '#70AD47', '▲ 8.6%', True),
        ('平均客单价', '139.4', '元', '#FFC000', '▲ 3.2%', True),
        ('销售退货率', '2.1', '%', '#ED7D31', '▼ 0.5%', True),
    ]

    fig, ax = plt.subplots(figsize=(13, 4.2))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.axis('off')

    fig.text(0.065, 0.9, '核心经营指标卡片（单值卡片图）',
             fontsize=16, fontweight='bold')
    fig.text(0.065, 0.82, '卡片图只展示一个聚合度量值，是数据大屏最常用的组件',
             fontsize=10, color='#555555')

    for i, (label, value, unit, color, delta, good) in enumerate(kpis):
        x0 = i + 0.08
        # 卡片背景（圆角矩形 + 浅色主题填充）
        card = FancyBboxPatch(
            (x0, 0.16), 0.84, 0.56,
            boxstyle='round,pad=0.02,rounding_size=0.05',
            linewidth=1.6, edgecolor=color, facecolor=color, alpha=0.10,
            transform=ax.transData
        )
        ax.add_patch(card)
        # 左侧主题色竖条
        bar = FancyBboxPatch(
            (x0 + 0.02, 0.22), 0.025, 0.44,
            boxstyle='round,pad=0.005,rounding_size=0.01',
            linewidth=0, facecolor=color
        )
        ax.add_patch(bar)

        ax.text(x0 + 0.12, 0.58, label, fontsize=12, color='#555555')
        ax.text(x0 + 0.12, 0.38, value, fontsize=26, fontweight='bold', color=color)
        ax.text(x0 + 0.12 + len(value) * 0.072, 0.35, unit,
                fontsize=11, color='#888888')
        delta_color = '#00B050' if good else '#C00000'
        ax.text(x0 + 0.12, 0.24, f'同比 {delta}', fontsize=10,
                color=delta_color, fontweight='bold')

    fig.text(0.065, 0.06,
             '数据来源：2024年度经营汇总 | 数据结构：1 个度量值 + 0 个轴标签（PPT 第7页）',
             fontsize=8, color='#888888')

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.savefig('chart_15_kpi_cards.png', dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close()
    print('[完成] chart_15_kpi_cards.png')


if __name__ == '__main__':
    main()
