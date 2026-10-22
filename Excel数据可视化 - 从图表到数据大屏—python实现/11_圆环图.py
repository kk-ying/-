# -*- coding: utf-8 -*-
"""
11 圆环图 —— 构成关系
对应 PPT 第20-21页"圆环图/圆饼图一般修饰"：环形填充 + 中心总量 + 数据标签引线
"""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

colors_pie = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5']


def main():
    items = ['人力成本', '采购成本', '运营费用', '营销费用', '其他支出']
    values = [38, 30, 14, 12, 6]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(8.5, 6))

    wedges, _ = ax.pie(
        values, colors=colors_pie[:len(values)], startangle=90,
        wedgeprops=dict(width=0.38, edgecolor='white', linewidth=2)
    )

    # 中心总量文本
    ax.text(0, 0.12, f'{total}', ha='center', va='center',
            fontsize=30, fontweight='bold', color='#1f4e79')
    ax.text(0, -0.18, '总成本（万元）', ha='center', va='center',
            fontsize=11, color='#666666')

    # 外部标签 + 引线（PPT：通过形状添加数据标签引线，更加灵活美观）
    for wedge, name, v in zip(wedges, items, values):
        ang = (wedge.theta2 + wedge.theta1) / 2
        rad = np.deg2rad(ang)
        x, y = np.cos(rad), np.sin(rad)
        ha = 'left' if x >= 0 else 'right'
        ax.annotate(f'{name}  {v / total * 100:.0f}%',
                    xy=(0.82 * x, 0.82 * y),
                    xytext=(1.22 * x, 1.12 * y),
                    ha=ha, va='center', fontsize=10,
                    arrowprops=dict(arrowstyle='-', color='#999999',
                                    connectionstyle='arc3,rad=0'))

    ax.text(0, 1.28, '企业成本费用构成', ha='left',
            fontsize=14, fontweight='bold', transform=ax.transAxes)
    ax.text(0, 1.14, '人力与采购成本合计占比 68%，是成本管控的核心',
            ha='left', fontsize=10, color='#555555', transform=ax.transAxes)
    ax.text(0, -0.12, '数据来源：2024年度财务预算 | 圆环图中心可放置汇总指标',
            ha='left', fontsize=8, color='#888888', transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig('chart_11_doughnut.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_11_doughnut.png')


if __name__ == '__main__':
    main()
