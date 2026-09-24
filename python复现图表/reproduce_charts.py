# -*- coding: utf-8 -*-
"""
复现《Excel数据可视化 - 从图表到数据大屏》第二章前15个图表
用 Python (matplotlib) 逐个复现，输出 PNG 到 python复现图表/ 目录
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, PathPatch
from matplotlib.path import Path
import matplotlib.colors as mcolors

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120

BASE = r"c:\Users\DENG_影\Desktop\作业\数据可视化\《Excel数据可视化 - 从图表到数据大屏》-清华-郭宏远"
OUT = os.path.join(BASE, "python复现图表")
os.makedirs(OUT, exist_ok=True)

# 配色
C_BLUE   = '#0070C0'
C_BLUE_L = '#00B0F0'
C_BLUE_M = '#82ADD7'
C_DARK   = '#1A1E43'
C_ORANGE = '#FFC000'
C_RED    = '#E74E69'
C_OR     = '#E66B4C'
C_PURPLE = '#7030A0'
C_GREEN  = '#49A098'
C_TEAL   = '#4A5BD1'
C_INDIGO = '#464CAC'
C_CYAN   = '#7BBDD5'
C_SKY    = '#0097E0'

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("saved:", name)

def gradient_bars(ax, x, h, w, c_top, c_bot):
    """垂直渐变填充柱形"""
    cmap = mcolors.LinearSegmentedColormap.from_list('g', [c_bot, c_top])
    for xi, hi in zip(x, h):
        if hi <= 0:
            continue
        grad = np.linspace(0, 1, 256).reshape(-1, 1)
        ax.imshow(grad, extent=[xi - w/2, xi + w/2, 0, hi],
                  aspect='auto', cmap=cmap, zorder=2)
    ax.set_ylim(bottom=0)

def style_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BFBFBF')
    ax.spines['bottom'].set_color('#BFBFBF')
    ax.tick_params(colors='#595959')

def catmull(x, y, n=30):
    """Catmull-Rom 平滑曲线"""
    pts = list(zip(x, y))
    pts = [pts[0]] + pts + [pts[-1]]
    xs, ys = [], []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i], pts[i+1], pts[i+2], pts[i+3]
        for t in np.linspace(0, 1, n):
            t2, t3 = t*t, t*t*t
            X = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t +
                     (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 +
                     (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            Y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t +
                     (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 +
                     (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            xs.append(X); ys.append(Y)
    return xs, ys

# ============ 1 渐变柱形图 ============
def fig01():
    area = ['华北','华南','东北','西北','西南','华东']
    val  = [2354,1902,3524,2698,2896,2563]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(area))
    gradient_bars(ax, x, val, 0.6, C_BLUE_L, C_BLUE)
    for xi, v in zip(x, val):
        ax.text(xi, v+60, str(v), ha='center', va='bottom', fontsize=10, color=C_DARK)
    ax.set_xticks(x); ax.set_xticklabels(area)
    ax.set_title('1 渐变柱形图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销售量'); style_ax(ax)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '01_渐变柱形图.png')

# ============ 2 带均值柱形图 ============
def fig02():
    area = ['华北','华南','东北','西北','西南','华东']
    val  = [2354,1902,3524,2698,2896,2563]
    mean = np.mean(val)
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(area))
    bars = ax.bar(x, val, width=0.55, color=C_BLUE, zorder=3)
    ax.axhline(mean, color=C_ORANGE, lw=2, zorder=4)
    ax.text(len(area)-0.5, mean+40, '均值 %.0f' % mean, color=C_ORANGE, fontsize=10, ha='right')
    for xi, v in zip(x, val):
        ax.text(xi, v+60, str(v), ha='center', fontsize=9, color=C_DARK)
    ax.set_xticks(x); ax.set_xticklabels(area)
    ax.set_title('2 带均值柱形图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销售量'); style_ax(ax)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '02_带均值柱形图.png')

# ============ 3 渐变圆角柱形图 ============
def fig03():
    item = ['口红','面膜','隔离','防晒','精华','面霜']
    val  = [653,523,648,856,714,785]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(item)); w = 0.55
    cmap = mcolors.LinearSegmentedColormap.from_list('g', [C_DARK, '#3A3F6E'])
    for xi, v in zip(x, val):
        grad = np.linspace(0, 1, 256).reshape(-1, 1)
        im = ax.imshow(grad, extent=[xi-w/2, xi+w/2, 0, v], aspect='auto', cmap=cmap, zorder=2)
        # 圆角遮罩：用 FancyBboxPatch clip
        patch = FancyBboxPatch((xi-w/2, 0), w, v,
                               boxstyle="round,pad=0,rounding_size=0.12",
                               mutation_aspect=1, fc='none', ec='none', zorder=3)
        ax.add_patch(patch)
        im.set_clip_path(patch)
        ax.text(xi, v+12, str(v), ha='center', fontsize=10, color=C_DARK)
    ax.set_xticks(x); ax.set_xticklabels(item)
    ax.set_title('3 渐变圆角柱形图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销量'); style_ax(ax)
    ax.set_ylim(0, max(val)*1.15)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '03_渐变圆角柱形图.png')

# ============ 4 标注柱形图 ============
def fig04():
    item = ['口红','面膜','隔离','防晒','精华','面霜','眼影','气垫']
    val  = [9221,5102,6571,5760,6321,8612,2645,5321]
    cols = [C_CYAN,C_GREEN,C_OR,C_ORANGE,C_SKY,C_BLUE,C_TEAL,C_INDIGO]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(item))
    ax.bar(x, val, width=0.6, color=cols, zorder=3)
    imax = int(np.argmax(val)); imin = int(np.argmin(val))
    ax.annotate('最大值 %d' % val[imax], xy=(imax, val[imax]),
                xytext=(imax, val[imax]+900), ha='center',
                arrowprops=dict(arrowstyle='->', color=C_RED), color=C_RED, fontsize=10)
    ax.annotate('最小值 %d' % val[imin], xy=(imin, val[imin]),
                xytext=(imin, val[imin]-1400), ha='center',
                arrowprops=dict(arrowstyle='->', color=C_BLUE), color=C_BLUE, fontsize=10)
    for xi, v in zip(x, val):
        ax.text(xi, v+60, str(v), ha='center', fontsize=8, color=C_DARK)
    ax.set_xticks(x); ax.set_xticklabels(item)
    ax.set_title('4 标注柱形图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销量'); style_ax(ax)
    ax.set_ylim(0, max(val)*1.18)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '04_标注柱形图.png')

# ============ 5 层叠柱形图 ============
def fig05():
    q = ['2021Q1','Q2','Q3','Q4','2022Q1','Q2']
    sales  = [3121,4086,4321,4601,4936,4231]
    profit = [1020,1421,1502,1623,1781,1432]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(q))
    ax.bar(x, sales, width=0.55, label='销售额', color=C_BLUE, zorder=3)
    ax.bar(x, profit, width=0.55, bottom=sales, label='利润额', color=C_RED, zorder=3)
    for xi, s, p in zip(x, sales, profit):
        ax.text(xi, s/2, str(s), ha='center', va='center', color='white', fontsize=9)
        ax.text(xi, s+p/2, str(p), ha='center', va='center', color='white', fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(q)
    ax.set_title('5 层叠柱形图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('金额'); style_ax(ax)
    ax.legend(frameon=False, loc='upper left')
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '05_层叠柱形图.png')

# ============ 6 蝴蝶图 ============
def fig06():
    area = ['华东','西北','东北','华北','华南']
    y2022 = [1215,1321,1426,1531,2238]
    y2021 = [1003,1265,1531,1436,2066]
    fig, ax = plt.subplots(figsize=(8,5))
    y = np.arange(len(area))
    ax.barh(y, y2022, color=C_BLUE, label='2022年销量', zorder=3)
    ax.barh(y, [-v for v in y2021], color=C_RED, label='2021年销量', zorder=3)
    for yi, v in zip(y, y2022):
        ax.text(v+30, yi, str(v), va='center', fontsize=9, color=C_DARK)
    for yi, v in zip(y, y2021):
        ax.text(-v-30, yi, str(v), va='center', ha='right', fontsize=9, color=C_DARK)
    ax.set_yticks(y); ax.set_yticklabels(area)
    ax.set_xlim(-2500, 2500)
    ax.set_xticks([-2000,-1000,0,1000,2000])
    ax.set_xticklabels(['2000','1000','0','1000','2000'])
    ax.set_title('6 蝴蝶图', fontsize=14, color=C_DARK, pad=12)
    style_ax(ax)
    ax.legend(frameon=False, loc='lower right')
    ax.xaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '06_蝴蝶图.png')

# ============ 7 蝴蝶图(百分比) ============
def fig07():
    area = ['华东','西北','东北','华北','华南']
    y2022 = [0.36,0.31,0.18,0.13,0.09]
    y2021 = [0.42,0.26,0.19,0.12,0.05]
    fig, ax = plt.subplots(figsize=(8,5))
    y = np.arange(len(area))
    ax.barh(y, y2022, color=C_BLUE, label='2022年', zorder=3)
    ax.barh(y, [-v for v in y2021], color=C_RED, label='2021年', zorder=3)
    for yi, v in zip(y, y2022):
        ax.text(v+0.01, yi, '%.0f%%' % (v*100), va='center', fontsize=9, color=C_DARK)
    for yi, v in zip(y, y2021):
        ax.text(-v-0.01, yi, '%.0f%%' % (v*100), va='center', ha='right', fontsize=9, color=C_DARK)
    ax.set_yticks(y); ax.set_yticklabels(area)
    ax.set_xlim(-0.5, 0.5)
    ax.set_xticks([-0.4,-0.2,0,0.2,0.4])
    ax.set_xticklabels(['40%','20%','0','20%','40%'])
    ax.set_title('7 蝴蝶图(百分比)', fontsize=14, color=C_DARK, pad=12)
    style_ax(ax)
    ax.legend(frameon=False, loc='lower right')
    ax.xaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '07_蝴蝶图_百分比.png')

# ============ 8 数值百分比 ============
def fig08():
    area = ['华北','华南','东北','西北','西南','华东']
    val  = [4321,1946,1536,1872,1369,2109]
    pct  = [-0.136,-0.208,-0.093,-0.159,-0.179,-0.058]
    mx = max(val)
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(area))
    # 吊顶式：柱子顶部对齐到 mx，柱长=val
    ax.bar(x, val, width=0.55, bottom=[mx-v for v in val], color=C_BLUE, zorder=3)
    for xi, v, p in zip(x, val, pct):
        ax.text(xi, mx+120, '%.1f%%' % (p*100), ha='center', fontsize=10,
                color=C_RED if p < 0 else C_GREEN)
        ax.text(xi, mx-v+v/2, str(v), ha='center', va='center', color='white', fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(area)
    ax.set_title('8 数值百分比', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销量'); style_ax(ax)
    ax.set_ylim(0, mx*1.18)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '08_数值百分比.png')

# ============ 9 对比柱形图 ============
def fig09():
    item = ['口红','面膜','隔离','防晒','精华']
    y2021 = [3568,4135,4436,4106,4936]
    y2022 = [2569,3241,2965,3209,3541]
    diff  = [999,894,1471,897,1395]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(item))
    ax.bar(x-0.2, y2021, width=0.38, label='2021销量', color=C_BLUE, zorder=3)
    ax.bar(x+0.2, y2022, width=0.38, label='2022销量', color=C_BLUE_M, zorder=3)
    ax2 = ax.twinx()
    ax2.plot(x, diff, color=C_OR, lw=2, marker='o', label='差值', zorder=5)
    for xi, d in zip(x, diff):
        ax2.text(xi, d+30, str(d), ha='center', fontsize=9, color=C_OR)
    ax.set_xticks(x); ax.set_xticklabels(item)
    ax.set_title('9 对比柱形图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销量'); ax2.set_ylabel('差值', color=C_OR)
    style_ax(ax); ax2.spines['top'].set_visible(False)
    ax2.tick_params(colors=C_OR)
    h1,l1 = ax.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, frameon=False, loc='upper right')
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '09_对比柱形图.png')

# ============ 10 甘特图 ============
def fig10():
    import datetime
    proj = ['制定计划','方案设计','资源调配','第一阶段','第二阶段','第三阶段','项目总结']
    start = [datetime.date(2022,3,1),datetime.date(2022,3,13),datetime.date(2022,3,22),
             datetime.date(2022,4,2),datetime.date(2022,4,16),datetime.date(2022,5,11),
             datetime.date(2022,5,26)]
    days  = [11,8,10,13,24,14,7]
    prog  = [0.51,0.32,0.21,0.85,0.36,0.68,0.68]
    fig, ax = plt.subplots(figsize=(10,5))
    y = np.arange(len(proj))[::-1]
    for yi, s, d, p in zip(y, start, days, prog):
        done = d*p
        ax.barh(yi, done, left=s, color=C_BLUE, height=0.55, zorder=3)
        ax.barh(yi, d-done, left=s+datetime.timedelta(days=done),
                color=C_BLUE_L, height=0.55, zorder=3, alpha=0.5)
        ax.text(s+datetime.timedelta(days=d+0.5), yi, '%.0f%%' % (p*100),
                va='center', fontsize=9, color=C_DARK)
    ax.set_yticks(y); ax.set_yticklabels(proj)
    ax.set_title('10 甘特图', fontsize=14, color=C_DARK, pad=12)
    ax.xaxis_date()
    fig.autofmt_xdate()
    style_ax(ax)
    ax.xaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '10_甘特图.png')

# ============ 11 平滑折线图 ============
def fig11():
    mon = ['5月','6月','7月','8月','9月','10月','11月','12月','1月','2月','3月']
    val = [146,198,296,412,506,615,789,1021,3782,3215,2936]
    fig, ax = plt.subplots(figsize=(9,5))
    x = np.arange(len(mon))
    xs, ys = catmull(x, val, 25)
    ax.plot(xs, ys, color=C_OR, lw=2.5, zorder=3)
    ax.scatter(x, val, color=C_OR, s=40, zorder=4)
    for xi, v in zip(x, val):
        ax.text(xi, v+80, str(v), ha='center', fontsize=8, color=C_DARK)
    ax.set_xticks(x); ax.set_xticklabels(mon)
    ax.set_title('11 平滑折线图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销量'); style_ax(ax)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '11_平滑折线图.png')

# ============ 12 菱形走势图 ============
def fig12():
    mon = ['1月','2月','3月','4月','5月','6月','7月','8月']
    val = [0.536,0.498,0.527,0.708,0.609,0.496,0.586,0.704]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(mon))
    ax.plot(x, val, color=C_RED, lw=2, marker='D', markersize=9,
            markerfacecolor=C_RED, markeredgecolor='white', zorder=3)
    for xi, v in zip(x, val):
        ax.text(xi, v+0.02, '%.1f%%' % (v*100), ha='center', fontsize=9, color=C_DARK)
    ax.set_xticks(x); ax.set_xticklabels(mon)
    ax.set_title('12 菱形走势图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('完成率'); ax.set_ylim(0.4, 0.8)
    ax.set_yticks([0.4,0.5,0.6,0.7,0.8])
    ax.set_yticklabels(['40%','50%','60%','70%','80%'])
    style_ax(ax)
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '12_菱形走势图.png')

# ============ 13 对比折线图 ============
def fig13():
    mon = ['1月','2月','3月','4月','5月','6月']
    y2021 = [1686,1345,1934,1658,1865,1936]
    y2022 = [1385,1846,1654,1936,2564,2236]
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(mon))
    ax.plot(x, y2021, color=C_RED, lw=2.5, marker='o', label='2021年', zorder=3)
    ax.plot(x, y2022, color=C_BLUE, lw=2.5, marker='o', label='2022年', zorder=3)
    for xi, v in zip(x, y2021):
        ax.text(xi, v+40, str(v), ha='center', fontsize=8, color=C_RED)
    for xi, v in zip(x, y2022):
        ax.text(xi, v-80, str(v), ha='center', fontsize=8, color=C_BLUE)
    ax.set_xticks(x); ax.set_xticklabels(mon)
    ax.set_title('13 对比折线图', fontsize=14, color=C_DARK, pad=12)
    ax.set_ylabel('销量'); style_ax(ax)
    ax.legend(frameon=False, loc='upper left')
    ax.yaxis.grid(True, color='#E8E8E8', zorder=0)
    save(fig, '13_对比折线图.png')

# ============ 14 单值圆环图 ============
def fig14():
    rate = 0.85
    fig, ax = plt.subplots(figsize=(6,6))
    ax.add_patch(Wedge((0,0), 1, 0, 360, width=0.28, facecolor='#E0E0E0', zorder=1))
    ax.add_patch(Wedge((0,0), 1, 90, 90-360*rate, width=0.28, facecolor=C_PURPLE, zorder=2))
    ax.text(0, 0, '%.0f%%' % (rate*100), ha='center', va='center',
            fontsize=34, color=C_PURPLE, fontweight='bold')
    ax.text(0, -0.25, '完成率', ha='center', va='center', fontsize=12, color='#7F7F7F')
    ax.set_title('14 单值圆环图', fontsize=14, color=C_DARK, pad=12)
    ax.set_aspect('equal'); ax.axis('off')
    save(fig, '14_单值圆环图.png')

# ============ 15 水球图 ============
def fig15():
    rate = 0.65
    fig, ax = plt.subplots(figsize=(6,6))
    # 容器圆
    ax.add_patch(Circle((0,0), 1, fc='none', ec=C_DARK, lw=2, zorder=5))
    # 水填充 (clip 到圆内)
    theta = np.linspace(0, 2*np.pi, 200)
    circ_x = np.cos(theta); circ_y = np.sin(theta)
    # 水面波浪
    wx = np.linspace(-1.2, 1.2, 400)
    level = -1 + 2*rate
    wave = level + 0.03*np.sin(wx*12)
    fill_x = np.concatenate([wx, wx[::-1]])
    fill_y = np.concatenate([wave, np.full_like(wx, -1.2)])
    ax.fill(fill_x, fill_y, color=C_BLUE, zorder=2, alpha=0.85)
    ax.plot(wx, wave, color=C_BLUE_L, lw=1.5, zorder=3)
    # clip 到圆
    circle_path = Path(np.column_stack([circ_x, circ_y]))
    for coll in ax.collections:
        coll.set_clip_path(PathPatch(circle_path, transform=ax.transData))
    ax.text(0, 0, '%.0f%%' % (rate*100), ha='center', va='center',
            fontsize=34, color='white', fontweight='bold', zorder=6)
    ax.set_title('15 水球图', fontsize=14, color=C_DARK, pad=12)
    ax.set_aspect('equal'); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.axis('off')
    save(fig, '15_水球图.png')

if __name__ == '__main__':
    for f in [fig01,fig02,fig03,fig04,fig05,fig06,fig07,fig08,fig09,
              fig10,fig11,fig12,fig13,fig14,fig15]:
        try:
            f()
        except Exception as e:
            import traceback
            print("ERROR in %s: %s" % (f.__name__, e))
            traceback.print_exc()
    print("ALL DONE ->", OUT)