# -*- coding: utf-8 -*-
"""
《Excel数据可视化——从图表到数据大屏》Python 迁移实现
基于 matplotlib，按照 PPT 中的图表设计原则进行美化
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

# ========== 全局设置：字体、配色 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

colors_primary = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47']
colors_gradient = ['#1f4e79', '#2e75b6', '#5b9bd5', '#9dc3e6', '#bdd7ee', '#deebf7']
colors_pie = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000']


def add_title_and_note(ax, title, subtitle=None, note=None, fontsize_title=14, fontsize_sub=10):
    # 主标题在上，副标题在其下，统一用 text 放置避免重叠
    if subtitle:
        ax.text(0, 1.16, title, transform=ax.transAxes, fontsize=fontsize_title, fontweight='bold')
        ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=fontsize_sub, color='#555555')
    else:
        ax.text(0, 1.04, title, transform=ax.transAxes, fontsize=fontsize_title, fontweight='bold')
    if note:
        ax.text(0, -0.14, note, transform=ax.transAxes, fontsize=8, color='#888888')


# ========== 图1：区域销售量 —— 簇状柱形图 ==========
def plot_sales_column():
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
    print('[完成] 图1：区域销售量柱形图 -> chart_1_sales_column.png')


# ========== 图2：季度销售额 —— 饼图（构成关系） ==========
def plot_quarterly_pie():
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
    print('[完成] 图2：季度销售额饼图 -> chart_2_quarterly_pie.png')


# ========== 图3：多系列柱形图（比较关系） ==========
def plot_multi_series_column():
    categories = ['类别 1', '类别 2', '类别 3', '类别 4']
    series1 = [4.3, 2.5, 3.5, 4.5]
    series2 = [2.4, 4.4, 1.8, 2.8]
    series3 = [2.0, 2.0, 3.0, 5.0]

    x = np.arange(len(categories))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar(x - width, series1, width, label='系列 1', color=colors_primary[0])
    bars2 = ax.bar(x, series2, width, label='系列 2', color=colors_primary[1])
    bars3 = ax.bar(x + width, series3, width, label='系列 3', color=colors_primary[2])

    ax.legend(loc='upper right', frameon=False)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('数值')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='多系列数据比较',
        subtitle='系列 3 在类别 4 表现突出，系列 2 在类别 2 达到峰值',
        note='数据来源：实验测试数据'
    )

    plt.tight_layout()
    plt.savefig('chart_3_multi_column.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] 图3：多系列柱形图 -> chart_3_multi_column.png')


# ========== 图4：多系列折线图（趋势关系） ==========
def plot_multi_series_line():
    categories = ['类别 1', '类别 2', '类别 3', '类别 4']
    series1 = [4.3, 2.5, 3.5, 4.5]
    series2 = [2.4, 4.4, 1.8, 2.8]
    series3 = [2.0, 2.0, 3.0, 5.0]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(categories, series1, marker='o', linewidth=2.5, label='系列 1', color=colors_primary[0])
    ax.plot(categories, series2, marker='s', linewidth=2.5, label='系列 2', color=colors_primary[1])
    ax.plot(categories, series3, marker='D', linewidth=2.5, label='系列 3', color=colors_primary[2])

    for i, s in enumerate([series1, series2, series3]):
        for j, v in enumerate(s):
            ax.text(j, v + 0.15, f'{v}', ha='center', fontsize=9, color=colors_primary[i])

    ax.legend(loc='upper left', frameon=False)
    ax.set_ylabel('数值')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='多系列数据趋势变化',
        subtitle='系列 3 呈上升趋势，系列 2 波动较大',
        note='数据来源：实验测试数据'
    )

    plt.tight_layout()
    plt.savefig('chart_4_multi_line.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] 图4：多系列折线图 -> chart_4_multi_line.png')


# ========== 图5：组合图（柱形图 + 折线图） ==========
def plot_combo_chart():
    categories = ['1月', '2月', '3月', '4月', '5月', '6月']
    sales = [120, 132, 101, 134, 90, 230]
    growth_rate = [5.2, 10.0, -23.5, 32.7, -32.8, 155.6]

    fig, ax1 = plt.subplots(figsize=(9, 5))

    bars = ax1.bar(categories, sales, color='#4472C4', alpha=0.8, label='销售额（万元）')
    ax1.set_ylabel('销售额（万元）', color='#4472C4', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#4472C4')
    ax1.set_ylim(0, max(sales) * 1.3)

    ax2 = ax1.twinx()
    ax2.plot(categories, growth_rate, color='#ED7D31', marker='o', linewidth=2.5, label='增长率（%）')
    ax2.set_ylabel('增长率（%）', color='#ED7D31', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#ED7D31')

    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 5,
                 f'{int(height)}', ha='center', va='bottom', fontsize=9, color='#4472C4')

    for i, v in enumerate(growth_rate):
        ax2.text(i, v + 5, f'{v}%', ha='center', fontsize=9, color='#ED7D31')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=False)

    ax1.spines['top'].set_visible(False)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)

    add_title_and_note(
        ax1,
        title='销售额与增长率组合分析',
        subtitle='6月销售额与增长率同步达到峰值，5月出现双降',
        note='数据来源：2024年上半年经营数据'
    )

    plt.tight_layout()
    plt.savefig('chart_5_combo.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] 图5：组合图 -> chart_5_combo.png')


# ========== 图6：水平条形图（带渐变色效果） ==========
def plot_horizontal_bar():
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
    print('[完成] 图6：水平条形图 -> chart_6_horizontal_bar.png')


# ========== 图7：数据大屏风格 —— 综合仪表板 ==========
def plot_dashboard():
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('#0f172a')

    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

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
    print('[完成] 图7：数据大屏综合仪表板 -> chart_7_dashboard.png')


# ========== 图8：散点图 —— 分布与联系（PPT 第9页内嵌图表真实数据） ==========
def plot_scatter():
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
    print('[完成] 图8：散点图 -> chart_8_scatter.png')


# ========== 图9：帕累托图 —— 分布（二八法则，PPT 第9页） ==========
def plot_pareto():
    reasons = ['外观划痕', '功能异常', '包装破损', '配件缺失', '其他问题']
    counts = [42, 31, 17, 6, 4]
    total = sum(counts)
    cumulative = np.cumsum(counts) / total * 100

    fig, ax1 = plt.subplots(figsize=(9, 5.5))

    bars = ax1.bar(reasons, counts, color='#4472C4', width=0.6,
                   edgecolor='white', label='缺陷数量')
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.8,
                 f'{int(height)}', ha='center', va='bottom',
                 fontsize=10, fontweight='bold', color='#4472C4')

    ax1.set_ylabel('缺陷数量（个）', fontsize=11, color='#4472C4')
    ax1.tick_params(axis='y', labelcolor='#4472C4')
    ax1.set_ylim(0, max(counts) * 1.2)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax1.set_axisbelow(True)

    ax2 = ax1.twinx()
    ax2.plot(reasons, cumulative, color='#ED7D31', marker='o',
             linewidth=2.5, label='累计占比')
    for i, v in enumerate(cumulative):
        ax2.text(i, v + 5, f'{v:.0f}%', ha='center', fontsize=9,
                 color='#ED7D31', fontweight='bold')
    ax2.set_ylabel('累计占比（%）', fontsize=11, color='#ED7D31')
    ax2.tick_params(axis='y', labelcolor='#ED7D31')
    ax2.set_ylim(0, 110)
    ax2.spines['top'].set_visible(False)

    ax2.axhline(80, color='#C00000', linestyle='--', linewidth=1.2, alpha=0.8)
    ax2.text(len(reasons) - 0.5, 82, '80% 关键分界线',
             ha='right', fontsize=9, color='#C00000')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', frameon=False)

    add_title_and_note(
        ax1,
        title='产品质量缺陷原因帕累托分析',
        subtitle='前两项原因累计占比 73%，是质量改善的关键少数',
        note='数据来源：月度质量检验统计 | 帕累托图遵循"关键的少数，次要的多数"原则'
    )

    plt.tight_layout()
    plt.savefig('chart_9_pareto.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] 图9：帕累托图 -> chart_9_pareto.png')


# ========== 图10：堆积柱形图 —— 1 个度量值 + 2 个维度（PPT 第7页） ==========
def plot_stacked_column():
    products = ['产品 A', '产品 B', '产品 C', '产品 D']
    quarters = ['第一季度', '第二季度', '第三季度', '第四季度']
    data = np.array([
        [120, 90, 70, 60],
        [140, 110, 80, 70],
        [100, 130, 90, 50],
        [170, 120, 110, 90],
    ])

    x = np.arange(len(products))
    fig, ax = plt.subplots(figsize=(9, 5.5))

    bottom = np.zeros(len(products))
    for qi, (q, row) in enumerate(zip(quarters, data)):
        ax.bar(x, row, width=0.55, bottom=bottom, label=q,
               color=colors_primary[qi], edgecolor='white')
        for xi, val, b in zip(x, row, bottom):
            if val > 0:
                ax.text(xi, b + val / 2, f'{val}', ha='center', va='center',
                        fontsize=9, color='white', fontweight='bold')
        bottom += row

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
    print('[完成] 图10：堆积柱形图 -> chart_10_stacked_column.png')


# ========== 图11：圆环图 —— 构成关系（PPT 第20-21页） ==========
def plot_doughnut():
    items = ['人力成本', '采购成本', '运营费用', '营销费用', '其他支出']
    values = [38, 30, 14, 12, 6]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(8.5, 6))

    wedges, _ = ax.pie(
        values, colors=colors_pie[:len(values)], startangle=90,
        wedgeprops=dict(width=0.38, edgecolor='white', linewidth=2)
    )

    ax.text(0, 0.12, f'{total}', ha='center', va='center',
            fontsize=30, fontweight='bold', color='#1f4e79')
    ax.text(0, -0.18, '总成本（万元）', ha='center', va='center',
            fontsize=11, color='#666666')

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
    print('[完成] 图11：圆环图 -> chart_11_doughnut.png')


# ========== 图12：面积图 —— 折线面积图（PPT 第22-23页） ==========
def plot_area():
    months = [f'{i}月' for i in range(1, 13)]
    online = [42, 48, 55, 60, 72, 85, 95, 110, 125, 140, 158, 180]
    offline = [80, 75, 78, 70, 72, 68, 70, 65, 68, 62, 60, 58]

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.stackplot(x, online, offline,
                 labels=['线上渠道', '线下渠道'],
                 colors=['#4472C4', '#ED7D31'], alpha=0.75,
                 edgecolor='white')

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
    print('[完成] 图12：面积图 -> chart_12_area.png')


# ========== 图13：误差线与趋势线 —— 统计类图表元素（PPT 第16页） ==========
def plot_error_trend():
    months = [f'{i}月' for i in range(1, 9)]
    sales = [118, 132, 125, 142, 138, 156, 168, 185]
    errors = [8, 10, 7, 12, 9, 11, 10, 13]

    x = np.arange(len(months))
    fig, ax = plt.subplots(figsize=(9.5, 5.5))

    bars = ax.bar(x, sales, width=0.55, color='#5B9BD5',
                  edgecolor='white', label='月销售额',
                  yerr=errors, capsize=5,
                  error_kw=dict(ecolor='#C00000', elinewidth=1.4, capthick=1.4))

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=9, color='#2f5597')

    coef = np.polyfit(x, sales, 1)
    fitted = np.polyval(coef, x)
    ax.plot(x, fitted, color='#ED7D31', linewidth=2.5, linestyle='--',
            marker='D', markersize=5,
            label=f'线性趋势线 y={coef[0]:.1f}x+{coef[1]:.1f}')

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
    print('[完成] 图13：误差线与趋势线 -> chart_13_error_trend.png')


# ========== 图14：涨/跌柱线 —— 股票行情（PPT 第16页） ==========
def plot_stock():
    days = ['周一', '周二', '周三', '周四', '周五']
    opens = [10.2, 10.6, 10.9, 10.5, 10.8]
    highs = [10.8, 11.0, 11.1, 10.9, 11.3]
    lows = [10.0, 10.5, 10.4, 10.3, 10.7]
    closes = [10.6, 10.9, 10.5, 10.8, 11.2]

    x = np.arange(len(days))
    fig, ax = plt.subplots(figsize=(9, 5.5))

    for i in range(len(days)):
        up = closes[i] >= opens[i]
        color = '#C00000' if up else '#00B050'
        ax.vlines(x[i], lows[i], highs[i], color=color, linewidth=1.6)
        ax.vlines(x[i], opens[i], closes[i], color=color, linewidth=8, alpha=0.85)
        ax.hlines([lows[i], highs[i]], x[i] - 0.08, x[i] + 0.08,
                  color=color, linewidth=1.6)
        ax.text(x[i], highs[i] + 0.07, f'{closes[i]:.1f}',
                ha='center', fontsize=9, color=color, fontweight='bold')

    legend_handles = [
        Line2D([0], [0], color='#C00000', linewidth=8, alpha=0.85, label='上涨（收≥开）'),
        Line2D([0], [0], color='#00B050', linewidth=8, alpha=0.85, label='下跌（收<开）'),
    ]
    ax.legend(handles=legend_handles, loc='upper left', frameon=False)

    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.set_ylabel('股价（元）', fontsize=11)
    ax.set_ylim(min(lows) - 0.35, max(highs) + 0.55)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    add_title_and_note(
        ax,
        title='某股票五个交易日行情（涨/跌柱线图）',
        subtitle='周三收阴回调，其余四个交易日均收涨，周五收于周内最高价',
        note='数据来源：行情模拟数据 | 竖线=最高/最低价，柱体=开盘/收盘价（PPT 第16页涨跌柱线）'
    )

    plt.tight_layout()
    plt.savefig('chart_14_stock.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('[完成] 图14：涨/跌柱线图 -> chart_14_stock.png')


# ========== 图15：KPI 单值卡片图 —— 1 个度量值、0 个轴标签（PPT 第7页） ==========
def plot_kpi_cards():
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
        card = FancyBboxPatch(
            (x0, 0.16), 0.84, 0.56,
            boxstyle='round,pad=0.02,rounding_size=0.05',
            linewidth=1.6, edgecolor=color, facecolor=color, alpha=0.10,
            transform=ax.transData
        )
        ax.add_patch(card)
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
    print('[完成] 图15：KPI 单值卡片图 -> chart_15_kpi_cards.png')


# ========== 主入口 ==========
if __name__ == '__main__':
    print('=' * 50)
    print('开始生成图表...')
    print('=' * 50)

    plot_sales_column()
    plot_quarterly_pie()
    plot_multi_series_column()
    plot_multi_series_line()
    plot_combo_chart()
    plot_horizontal_bar()
    plot_dashboard()
    plot_scatter()
    plot_pareto()
    plot_stacked_column()
    plot_doughnut()
    plot_area()
    plot_error_trend()
    plot_stock()
    plot_kpi_cards()

    print('=' * 50)
    print('所有图表生成完毕！')
    print('=' * 50)
