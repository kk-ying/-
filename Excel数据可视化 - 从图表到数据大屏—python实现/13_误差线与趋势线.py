# -*- coding: utf-8 -*-
"""
13 误差线与趋势线 —— 统计类图表元素
对应 PPT 第16页：
误差线反映每个数据标记的可能误差量；趋势线按回归分析方法对数据进行拟合预测
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
    months = [f'{i}月' for i in range(1, 9)]
    sales = [118, 132, 125, 142, 138, 156, 168, 185]
    errors = [8, 10, 7, 12, 9, 11, 10, 13]

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(9.5, 5.5))

    # 柱形图 + 误差线
    bars = ax.bar(x, sales, width=0.55, color='#5B9BD5',
                  edgecolor='white', label='月销售额',
                  yerr=errors, capsize=5,
                  error_kw=dict(ecolor='#C00000', elinewidth=1.4, capthick=1.4))

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=9, color='#2f5597')

    # 线性趋势线（一元线性回归拟合）
    coef = np.polyfit(x, sales, 1)
    fitted = np.polyval(coef, x)
    ax.plot(x, fitted, color='#ED7D31', linewidth=2.5, linestyle='--',
            marker='D', markersize=5,
            label=f'线性趋势线 y={coef[0]:.1f}x+{coef[1]:.1f}')

    # 预测未来两个月（虚线延伸）
    future_x = np.array([len(months), len(months) + 1])
    future_y = np.polyval(coef, future_x)
    ax.plot(np.concatenate([[x[-1]], future_x]),
            np.concatenate([[fitted[-1]], future_y]),
            color='#ED7D31', linewidth=2.5, linestyle=':', alpha=0.7)
    for fx, fy in zip(future_x, future_y):
        ax.text(fx, fy + 3, f'预测 {fy:.0f}', ha='center',
                fontsize=9, color='#ED7D31')

    ax.set_xticks(np.concatenate([x, future_x]))
    ax.set_xticklabels(months + ['9月(预)', '10月(预)'])
    ax.set_ylabel('销售额（万元）', fontsize=11)
    ax.set_ylim(0, max(np.array(sales) + np.array(errors)) * 1.25)
    ax.legend(loc='upper left', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='月度销售额：误差线与线性趋势线',
        subtitle='红色误差线表示波动范围，剔除波动后销售额呈稳定上升趋势',
        note='数据来源：2024年1-8月经营数据 | 误差线反映波动，趋势线用于回归预测（PPT 第16页）'
    )

    plt.tight_layout()
    plt.savefig('chart_13_error_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] chart_13_error_trend.png')


if __name__ == '__main__':
    main()
