# -*- coding: utf-8 -*-
"""
07 销售数据可视化大屏 —— 综合仪表板（深色主题）
对应 PPT 中"数据大屏"进阶实战概念（卡片图 + 柱形图 + 饼图 + 折线图）
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def main():
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('#0f172a')

    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

    # 顶部 KPI 卡片
    kpi_data = [
        ('总销售额', '1,245万元', '#3b82f6'),
        ('订单总量', '8,932单', '#10b981'),
        ('客单价', '139.4元', '#f59e0b'),
    ]

    for i, (label, value, color) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor('#1e293b')
        ax.text(0.5, 0.6, value, transform=ax.transAxes, fontsize=28,
                ha='center', va='center', color=color, fontweight='bold')
        ax.text(0.5, 0.25, label, transform=ax.transAxes, fontsize=14,
                ha='center', va='center', color='#94a3b8')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        for spine in ax.spines.values():
            spine.set_color('#334155')
            spine.set_linewidth(1.5)

    # 左上：区域销售量柱形图
    ax1 = fig.add_subplot(gs[1, :2])
    ax1.set_facecolor('#1e293b')
    regions = ['华北', '华南', '东北', '西北', '西南', '华东']
    sales = [2354, 1902, 3524, 2698, 2896, 2563]
    bars = ax1.bar(regions, sales, color='#3b82f6', edgecolor='white', width=0.6)
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 50,
                 f'{int(height)}', ha='center', va='bottom', fontsize=10, color='white')
    ax1.set_title('各区域销售量', color='white', fontsize=14, fontweight='bold', pad=10, loc='left')
    ax1.tick_params(colors='white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#475569')
    ax1.spines['bottom'].set_color('#475569')
    ax1.yaxis.grid(True, linestyle='--', alpha=0.3, color='#475569')
    ax1.set_axisbelow(True)

    # 右上：季度占比饼图
    ax2 = fig.add_subplot(gs[1, 2])
    ax2.set_facecolor('#1e293b')
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    values = [8.2, 3.2, 1.4, 1.2]
    wedges, texts, autotexts = ax2.pie(
        values, labels=quarters, autopct='%1.1f%%',
        colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.7, edgecolor='#1e293b')
    )
    for text in texts:
        text.set_color('white')
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    ax2.set_title('季度占比', color='white', fontsize=14, fontweight='bold', pad=10, loc='left')

    # 底部：月度销售趋势对比折线图
    ax3 = fig.add_subplot(gs[2, :])
    ax3.set_facecolor('#1e293b')
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    trend1 = [120, 132, 101, 134, 90, 230]
    trend2 = [100, 115, 130, 125, 140, 180]
    ax3.plot(months, trend1, marker='o', linewidth=2.5, color='#3b82f6', label='2024年')
    ax3.plot(months, trend2, marker='s', linewidth=2.5, color='#10b981', label='2023年')
    ax3.fill_between(months, trend1, trend2, alpha=0.15, color='#3b82f6')
    ax3.set_title('月度销售趋势对比', color='white', fontsize=14, fontweight='bold', pad=10, loc='left')
    ax3.legend(loc='upper left', frameon=False, labelcolor='white')
    ax3.tick_params(colors='white')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_color('#475569')
    ax3.spines['bottom'].set_color('#475569')
    ax3.yaxis.grid(True, linestyle='--', alpha=0.3, color='#475569')
    ax3.set_axisbelow(True)

    fig.suptitle('销售数据可视化大屏', color='white', fontsize=20, fontweight='bold', y=0.98)

    plt.savefig('chart_7_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print('[完成] chart_7_dashboard.png')


if __name__ == '__main__':
    main()
