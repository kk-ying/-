# -*- coding: utf-8 -*-
"""
复现《Excel数据可视化 - 从图表到数据大屏》第二章后15个图表（编号16-30）
用 Python (matplotlib) 逐个复现，输出 PNG 到本脚本所在目录
运行: python reproduce_charts_hou15.py
数据来源: 第二章 图表(后15).xlsx 各工作表
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Wedge, Rectangle, FancyBboxPatch,
                                PathPatch)
from matplotlib.path import Path
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.colors as mcolors

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------- 配色（取自原图表像素） ----------------
BG       = '#1A1E43'   # 深蓝底
BLUE     = '#0070C0'
BLUE_L   = '#00B0F0'
BLUE_M   = '#82ADD7'
BLUE_BR  = '#0E5DFF'   # 子弹图-实际
RED      = '#E74E69'
YELLOW   = '#FFC000'
AMBER    = '#FFC54D'
TEAL     = '#087E8B'
ROSE_R   = '#F94C66'
CYAN     = '#37A2DA'
GREEN_T  = '#11A7AD'
PURPLE   = '#7030A0'
DARKLINE = '#1A1E43'
TXT      = '#FFFFFF'
TXT2     = '#E9EAF2'
TXT3     = '#AEB1C2'
GREY_TR  = '#767889'   # 滑珠轨道灰
GREY_BEAD= '#A6A6A6'
OUTLINE  = '#9BA0BC'   # 目标柱描边
# 南丁格尔圆环
R_PURPLE = '#512DCB'
R_BLUE   = '#6073F3'
R_CYAN   = '#66CBDD'
# 复合柱形图季度色
Q_COLORS = ['#4A5BD1', '#FC6C0F', '#F6A50B', '#A2417B']

TITLE_FS  = 23
SUB_FS    = 14.5
NOTE_FS   = 10.5


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, facecolor=BG, bbox_inches='tight', pad_inches=0.12)
    plt.close(fig)
    print('saved:', name)


def dashboard(title=None, subtitle=None, footnote=None, figsize=(8.4, 6.0)):
    """统一的深色大屏画布，返回 fig，标题/副标题/脚注用 figure 坐标"""
    fig = plt.figure(figsize=figsize, facecolor=BG)
    if title:
        fig.text(0.055, 0.955, title, fontsize=TITLE_FS, fontweight='bold',
                 color=TXT, va='top', ha='left')
    if subtitle:
        fig.text(0.055, 0.885, subtitle, fontsize=SUB_FS, color=TXT2,
                 va='top', ha='left')
    if footnote:
        fig.text(0.055, 0.045, footnote, fontsize=NOTE_FS, color=TXT3,
                 va='bottom', ha='left')
    return fig


def polar_xy(r, deg_cw_from_top):
    """顺时针(从正上方)角度 -> 直角坐标"""
    a = np.radians(90 - deg_cw_from_top)
    return r * np.cos(a), r * np.sin(a)


def ring(ax, r_in, r_out, vals, colors, start=90, edge=DARKLINE, lw=1.2):
    """画一个(甜甜圈)环：vals 为各项占比(自动归一)，从 start 度起顺时针着色"""
    vals = np.asarray(vals, dtype=float)
    total = vals.sum()
    cur = start
    out = []
    for v, c in zip(vals, colors):
        sweep = 360.0 * v / total
        if c is not None:
            w = Wedge((0, 0), r_out, cur - sweep, cur,
                      width=r_out - r_in, facecolor=c, edgecolor=edge,
                      linewidth=lw, zorder=2)
            ax.add_patch(w)
            out.append(w)
        cur -= sweep
    return out


def capsule(ax, x0, x1, y, thick_pt, color, z=2):
    """以粗圆头线画胶囊条(thick_pt 为线宽/点)，不受坐标比例影响"""
    ax.plot([x0, x1], [y, y], color=color, lw=thick_pt,
            solid_capstyle='round', solid_joinstyle='round',
            zorder=z, clip_on=False)


# ============================================================
# 16 波浪水球图
# ============================================================
def fig16():
    rate = 0.65
    fig = plt.figure(figsize=(5.6, 5.6), facecolor=BG)
    ax = fig.add_axes([0.06, 0.06, 0.88, 0.88])
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)
    ax.set_aspect('equal'); ax.axis('off')

    # 外圈描边
    ax.add_patch(Circle((0, 0), 1.02, fill=False, ec='#0097E0', lw=2.2, zorder=5))
    ax.add_patch(Circle((0, 0), 0.99, fill=False, ec='#0E86D4', lw=0.8,
                        alpha=.6, zorder=5))

    # 波浪水体（clip 到圆内，波形与原图一致：左缘波峰→波谷→波峰→右缘下降）
    level = 0.16
    wx = np.linspace(-1.02, 1.02, 600)
    t = (wx + 1.0) / 2.0
    wave = level + 0.07 * np.cos(2 * np.pi * 1.35 * t)
    fill_x = np.concatenate([wx, wx[::-1]])
    fill_y = np.concatenate([wave, np.full_like(wx, -1.12)])
    poly = ax.fill(fill_x, fill_y, color=BLUE, zorder=2)[0]
    wline, = ax.plot(wx, wave, color='#0F8FE0', lw=1.1, alpha=.85, zorder=3)
    clip = Circle((0, 0), 0.975, transform=ax.transData)
    poly.set_clip_path(clip)
    wline.set_clip_path(clip)

    ax.text(0, 0.02, '%.0f%%' % (rate * 100), ha='center', va='center',
            fontsize=40, color='white', fontweight='bold', zorder=6)
    save(fig, '16_波浪水球图.png')


# ============================================================
# 17 玉玦图
# ============================================================
def fig17():
    labels = ['[20,30)', '[30,40)', '[40,50)', '>=50']
    vals   = [0.375, 0.2916667, 0.2083333, 0.125]
    colors = [RED, AMBER, GREEN_T, CYAN]

    fig = dashboard('2022年上半年龄分布',
                    '公司平均年龄32.5，23-30员工比例最高',
                    '*注：数据来源于公司人力系统，统计日期截至2022.06.30',
                    figsize=(8.4, 6.0))
    ax = fig.add_axes([0.30, 0.06, 0.62, 0.74])
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.30, 1.25)
    ax.set_aspect('equal'); ax.axis('off')

    n = 4
    r_in0, r_out = 0.35, 1.0
    step = (r_out - r_in0) / n
    # 由外向内：[20,30) 37.5% ... >=50 12.5%
    for i in range(n):
        r_out_i = r_out - i * step
        r_in_i = r_out_i - step * 0.82
        p = vals[i]
        ring(ax, r_in_i, r_out_i, [p, 0.5 - p], [colors[i], None],
             edge=DARKLINE, lw=1.4)
        # 起始端标签（顶部）
        rm = (r_in_i + r_out_i) / 2
        ax.text(-0.04, rm, labels[i], ha='right', va='center',
                fontsize=12.5, color=TXT)
        # 末端百分比
        sweep = p / 0.5 * 360
        ex, ey = polar_xy(rm, sweep + 4)
        ha = 'left' if ex > 0 else 'right'
        ax.text(ex, ey, '%.1f%%' % (p * 100), ha=ha, va='center',
                fontsize=11.5, color=TXT)
    save(fig, '17_玉玦图.png')


# ============================================================
# 18 跑道图
# ============================================================
def fig18():
    labels = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    vals   = [451, 326, 293, 238, 226, 130]
    colors = [RED, AMBER, GREEN_T, CYAN, BLUE, PURPLE]
    half = sum(vals) * 0.5  # 832

    fig = dashboard('2022年上半年各部门人数',
                    '公司总人数1664，销售部人数最多451，占比27%',
                    '*注：数据来源于公司人力资源系统，统计日期截止2022.06.30')
    ax = fig.add_axes([0.30, 0.05, 0.62, 0.76])
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.30, 1.25)
    ax.set_aspect('equal'); ax.axis('off')

    n = 6
    r_in0, r_out = 0.45, 1.0
    step = (r_out - r_in0) / n
    for i in range(n):
        r_out_i = r_out - i * step
        r_in_i = r_out_i - step * 0.82
        v = vals[i]
        ring(ax, r_in_i, r_out_i, [v, half - v], [colors[i], None],
             edge=DARKLINE, lw=1.4)
        rm = (r_in_i + r_out_i) / 2
        ax.text(-0.04, rm, '%s %d' % (labels[i], v), ha='right', va='center',
                fontsize=11.5, color=TXT)
    save(fig, '18_跑道图.png')


# ============================================================
# 19 南丁格尔圆饼图（Excel 渲染为普通饼图 + 彩色引导线）
# ============================================================
def fig19():
    cats   = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    vals   = [0.292, 0.227, 0.175, 0.136, 0.103, 0.067]
    palette = [RED, AMBER, GREEN_T, BLUE, CYAN, PURPLE]

    fig = dashboard('2021年各部门人数分布',
                    '公司总人数1664，销售部人数最多451，占比29.2%',
                    '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01')
    ax = fig.add_axes([0.20, 0.09, 0.62, 0.74])
    ax.set_xlim(-1.30, 1.45); ax.set_ylim(-1.12, 1.18)
    ax.set_aspect('equal'); ax.axis('off')

    # 六扇区实心饼（从正上方起顺时针），细深色分隔线
    ring(ax, 0.0, 1.0, vals, palette, start=90, edge=DARKLINE, lw=1.2)

    # 引导线（原图无标签文字）：右侧两条带圆点，左侧三条折线
    # (锚点, 拐点, 水平末端, 颜色, 是否带圆点)
    leaders = [
        ((0.75, 0.29), (0.88, 0.45), (1.30, 0.45), RED, True),    # 销售
        ((0.60, -0.37), (0.67, -0.45), (1.22, -0.45), AMBER, True),  # 采购
        ((-0.40, -0.70), (-0.52, -0.78), (-1.15, -0.78), GREEN_T, False),  # 工程
        ((-0.55, -0.05), (-0.56, -0.30), (-1.15, -0.30), BLUE, False),    # 财务
        ((-0.40, 0.33), (-0.49, 0.18), (-1.15, 0.18), CYAN, False),      # 行政
    ]
    for anchor, elbow, end, c, dot in leaders:
        ax.plot([anchor[0], elbow[0], end[0]],
                [anchor[1], elbow[1], end[1]],
                color=c, lw=1.3, zorder=4)
        if dot:
            ax.scatter([anchor[0]], [anchor[1]], s=60, color=c, zorder=5)
    save(fig, '19_南丁格尔圆饼图.png')


# ============================================================
# 20 南丁格尔圆环图
# ============================================================
def fig20():
    cats   = ['[20,30)', '[30,40)', '[40,50)', '>=50']
    vals   = [0.375, 0.2916667, 0.2083333, 0.125]
    colors = [R_PURPLE, R_BLUE, R_CYAN, AMBER]

    fig = dashboard('2022年上半各年龄段人数分布',
                    '公司平均年龄32.5，20-30员工比例最高占比37.5%',
                    '*注：数据来源于公司人力资源系统，统计日期截至2022.06.30')
    ax = fig.add_axes([0.16, 0.07, 0.72, 0.74])
    ax.set_xlim(-1.30, 1.35); ax.set_ylim(-1.12, 1.00)
    ax.set_aspect('equal'); ax.axis('off')

    # 5 层同心弧：内半径 .37 外半径 .72；小占比段层数减少
    R_IN, R_OUT, N_LAYER = 0.37, 0.72, 5
    step = (R_OUT - R_IN) / N_LAYER
    bounds = [R_IN + step * k for k in range(N_LAYER + 1)]
    n_layers = [5, 5, 5, 3]          # 紫 / 蓝 / 青 / 琥珀
    gap_deg = 3.0                    # 段间角度间隙
    explode = [0.05, 0.03, 0.0, 0.0]  # 外拉
    cur = 90.0
    mids = []
    for i, v in enumerate(vals):
        sweep = 360.0 * v
        t1, t2 = cur - sweep + gap_deg / 2, cur - gap_deg / 2
        mid = math.radians((t1 + t2) / 2)
        mids.append(mid)
        ox, oy = explode[i] * math.cos(mid), explode[i] * math.sin(mid)
        for k in range(n_layers[i]):
            w = Wedge((ox, oy), bounds[k + 1] - 0.004, t1, t2,
                      width=step - 0.008, facecolor=colors[i],
                      edgecolor=DARKLINE, linewidth=0.8, zorder=2)
            ax.add_patch(w)
        cur -= sweep

    # 外部标注：圆点在扇区上 -> 拐点 -> 水平延长线，文字堆叠在水平线上方
    # (圆点, 拐点, 水平末端, 标签x, 标签对齐, 类别y, 百分比y, 类别, 百分比, 颜色)
    callouts = [
        ((0.72, 0.30), (0.86, 0.45), (1.28, 0.45), 1.07, 'center', 0.56, 0.45,
         cats[0], '37.5%', R_PURPLE),
        ((0.33, -0.70), (0.40, -1.00), (1.18, -1.00), 0.78, 'left', -0.82, -0.92,
         cats[1], '29.2%', R_BLUE),
        ((-0.47, -0.03), (-0.62, -0.20), (-1.20, -0.20), -0.95, 'center', 0.04, -0.06,
         cats[2], '20.8%', R_CYAN),
        ((-0.19, 0.46), (-0.28, 0.58), (-0.62, 0.58), -0.47, 'center', 0.70, 0.59,
         cats[3], '12.5%', AMBER),
    ]
    for dot, elbow, end, lx, ha, y_cat, y_pct, cat, pct, c in callouts:
        ax.plot([dot[0], elbow[0], end[0]], [dot[1], elbow[1], end[1]],
                color=c, lw=1.3, zorder=4)
        ax.scatter([dot[0]], [dot[1]], s=55, color=c, zorder=5)
        ax.text(lx, y_cat, cat, ha=ha, va='bottom', fontsize=12, color=TXT)
        ax.text(lx, y_pct, pct, ha=ha, va='bottom', fontsize=12,
                color=c, fontweight='bold')
    save(fig, '20_南丁格尔圆环图.png')


# ============================================================
# 21 南丁格尔玫瑰图（PPT 版，等角 / 半径编码占比）
# ============================================================
def fig21():
    cats   = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
    vals   = [0.292, 0.227, 0.175, 0.136, 0.103, 0.067]
    palette = [RED, AMBER, GREEN_T, BLUE, CYAN, PURPLE]

    fig = dashboard('2021年各部门人数分布',
                    '公司总人数1664，销售部人数最多451，占比29.2%（PPT版南丁格尔玫瑰图）',
                    '*注：数据来源于公司人力资源系统，统计日期截至2022.01.01')
    ax = fig.add_axes([0.18, 0.14, 0.64, 0.62], projection='polar')
    ax.set_facecolor(BG)
    n = len(vals)
    width = 2 * np.pi / n
    angles = np.pi / 2 - (np.arange(n) + 0.5) * width  # 自正上方起顺时针
    radii = 0.22 + np.array(vals) / 0.292 * 0.72       # 半径编码占比
    ax.bar(angles, radii, width=width * 0.88, bottom=0.0,
           color=palette, edgecolor=DARKLINE, linewidth=1.2, zorder=2)
    # 外侧类别 + 百分比标签
    for a, c, v in zip(angles, cats, vals):
        ha = 'left' if np.cos(a) > 0.15 else 'right' if np.cos(a) < -0.15 else 'center'
        ax.text(a, 1.12, '%s\n%.1f%%' % (c, v * 100), ha=ha, va='center',
                linespacing=1.35, fontsize=12, color=TXT)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_ylim(0, 1.28)
    ax.spines['polar'].set_visible(False)
    ax.grid(False)
    ax.tick_params(length=0)
    save(fig, '21_南丁格尔玫瑰图_PPT版.png')


# ============================================================
# 22 仪表盘图
# ============================================================
def fig22():
    value = 76
    vmin, vmax = 50, 150

    def tc(v):  # 数值 -> 从正上方顺时针的角度
        return 225 + (v - vmin) / (vmax - vmin) * 270

    fig = dashboard(figsize=(8.0, 6.4))
    fig.text(0.5, 0.955, '2022年6月29公司整体运营指数良好',
             fontsize=TITLE_FS, fontweight='bold', color=TXT,
             va='top', ha='center')
    ax = fig.add_axes([0.20, 0.02, 0.60, 0.78])
    ax.set_xlim(-1.30, 1.30); ax.set_ylim(-1.20, 1.20)
    ax.set_aspect('equal'); ax.axis('off')

    # 外环：12 段蓝色刻度弧（50/150 两端各向下多延伸约 25°）
    bounds_cw = ([200] + [tc(v) for v in range(50, 151, 10)] + [520])
    for c1, c2 in zip(bounds_cw[:-1], bounds_cw[1:]):
        a1, a2 = 90 - c2 + 0.6, 90 - c1 - 0.6
        ax.add_patch(Wedge((0, 0), 1.0, a1, a2, width=0.13,
                           facecolor=BLUE, edgecolor=BG, lw=.8, zorder=2))

    # 内圈色带：50-80 青 / 80-120 黄 / 120-150 红
    zones = [(50, 80, TEAL), (80, 120, AMBER), (120, 150, ROSE_R)]
    for v1, v2, c in zones:
        a1, a2 = 90 - tc(v2) + 1.0, 90 - tc(v1) - 1.0
        ax.add_patch(Wedge((0, 0), 0.84, a1, a2, width=0.10,
                           facecolor=c, edgecolor=BG, lw=.8, zorder=3))

    # 刻度标签
    for v in range(50, 151, 10):
        x, y = polar_xy(0.66, tc(v))
        ax.text(x, y, str(v), ha='center', va='center',
                fontsize=12.5, color=TXT)

    # 指针（原图无中心圆点）
    ang = np.radians(90 - tc(value))
    ax.plot([0, 0.48 * np.cos(ang)], [0, 0.48 * np.sin(ang)],
            color='white', lw=2.0, zorder=6, solid_capstyle='round')
    ax.text(0, -0.42, str(value), ha='center', va='center',
            fontsize=30, color='white', fontweight='bold')
    save(fig, '22_仪表盘图.png')


# ============================================================
# 23 柱形折线图
# ============================================================
def fig23():
    years = ['2017', '2018', '2019', '2020', '2021', '2022']
    sales = [1603, 2106, 2406, 3265, 3721, 3921]
    yoy   = [0.27, 0.3138, 0.1425, 0.3570, 0.1397, 0.0537]

    fig = dashboard('近六年销售量及增长率',
                    '平台销量近6年持续增长，但近两年增长率有所放缓',
                    '*注：数据来源于公司销售系统')
    ax = fig.add_axes([0.075, 0.13, 0.88, 0.62])
    ax.set_facecolor(BG)
    x = np.arange(len(years))
    ax.bar(x, sales, width=0.22, color=BLUE, zorder=3)
    for xi, v in zip(x, sales):
        ax.text(xi, v + 80, str(v), ha='center', va='bottom',
                fontsize=11.5, color=TXT)
    ax.set_xticks(x); ax.set_xticklabels(years, fontsize=12.5, color=TXT)
    ax.set_ylim(0, 5800)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#6E7079')
    ax.tick_params(length=0)

    ax2 = ax.twinx()
    ax2.plot(x, yoy, color=RED, lw=2.4, marker='o', ms=7, zorder=5)
    for xi, v in zip(x, yoy):
        ax2.text(xi, v + 0.014, '%.0f%%' % (v * 100), ha='center',
                 va='bottom', fontsize=11.5, color=TXT)
    ax2.set_ylim(-0.18, 0.40)
    ax2.axis('off')

    legend = [Patch(facecolor=BLUE, label='销售量'),
              Line2D([0], [0], color=RED, lw=2.4, marker='o', ms=6, label='同比')]
    ax.legend(handles=legend, loc='upper right', bbox_to_anchor=(0.95, 1.12),
              ncol=2, frameon=False, fontsize=12, labelcolor=TXT,
              columnspacing=1.6)
    save(fig, '23_柱形折线图.png')


# ============================================================
# 24 目标柱形图
# ============================================================
def fig24():
    cats   = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    actual = [653, 523, 648, 856, 714, 785]
    target = [700, 500, 600, 900, 600, 600]

    fig = dashboard('2022年上半年各商品销量完成情况',
                    '防晒整体销量最好，达到856，面霜远超目标，超额完成30%',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06.30')
    ax = fig.add_axes([0.075, 0.13, 0.88, 0.62])
    ax.set_facecolor(BG)
    x = np.arange(len(cats))
    # 目标：空心描边框（更宽）
    for xi, t in zip(x, target):
        ax.add_patch(Rectangle((xi - 0.155, 0), 0.31, t, fill=False,
                               edgecolor=OUTLINE, lw=1.3, zorder=3))
    # 实际：窄实心柱
    ax.bar(x, actual, width=0.15, color=BLUE, zorder=4)
    for xi, v in zip(x, actual):
        ax.text(xi, v + 55, str(v), ha='center', va='bottom',
                fontsize=11.5, color=TXT)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=13, color=TXT)
    ax.set_ylim(0, 1050)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#6E7079')
    ax.tick_params(length=0)

    legend = [Patch(facecolor='none', edgecolor=OUTLINE, lw=1.3, label='目标销量'),
              Patch(facecolor=BLUE, label='实际销量')]
    ax.legend(handles=legend, loc='upper left', bbox_to_anchor=(0.02, 1.08),
              ncol=2, frameon=False, fontsize=12, labelcolor=TXT,
              handlelength=1.2, columnspacing=1.4)
    save(fig, '24_目标柱形图.png')


# ============================================================
# 25 子弹图
# ============================================================
def fig25():
    cats   = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
    actual = [653, 523, 648, 856, 714, 785]
    target = [700, 500, 600, 900, 600, 600]
    bands = [(600, BLUE_M, 0.85), (200, BLUE_L, 0.55), (200, BLUE, 0.90)]

    fig = dashboard('2022年上半年各商品销量完成情况',
                    '防晒整体销量最好，达到856，面霜远超目标，超额完成30%',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06.30')
    ax = fig.add_axes([0.09, 0.13, 0.86, 0.62])
    ax.set_facecolor(BG)
    x = np.arange(len(cats))
    bottom = np.zeros(len(cats))
    for w, c, al in bands:
        ax.bar(x, np.full(len(cats), w), width=0.26, bottom=bottom,
               color=c, alpha=al, edgecolor='none', zorder=2)
        bottom += w
    # 实际值
    ax.bar(x, actual, width=0.10, color=BLUE_BR, zorder=4)
    # 目标刻度线
    for xi, t in zip(x, target):
        ax.plot([xi - 0.10, xi + 0.10], [t, t], color=YELLOW, lw=3.0,
                solid_capstyle='butt', zorder=5)

    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=13, color=TXT)
    ax.set_ylim(0, 1200)
    ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
    ax.set_yticklabels(['0', '200', '400', '600', '800', '1000', '1200'],
                       fontsize=11.5, color=TXT)
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#6E7079')
    ax.tick_params(length=0)

    legend = [
        Patch(facecolor=BLUE_M, alpha=.85, label='及格'),
        Patch(facecolor=BLUE_L, alpha=.55, label='良好'),
        Patch(facecolor=BLUE, alpha=.90, label='优秀'),
        Patch(facecolor=BLUE_BR, label='实际'),
        Line2D([0], [0], color=YELLOW, lw=3.0, label='目标'),
    ]
    ax.legend(handles=legend, loc='upper left', bbox_to_anchor=(0.08, 1.08),
              ncol=5, frameon=False, fontsize=11.5, labelcolor=TXT,
              handlelength=1.1, columnspacing=1.1)
    save(fig, '25_子弹图.png')


# ============================================================
# 26 柱形圆
# ============================================================
def fig26():
    cats = ['华北', '华南', '东北', '西北', '西南', '华东']
    vals = [2354, 1902, 3524, 2698, 2896, 2563]
    yoy  = [0.12, 0.25, 0.16, 0.21, 0.18, 0.25]

    fig = dashboard('各区域上半年销量以同比',
                    '东北区域销量持续保持第一，华东和华南同比去年增长最多',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06,30')
    ax = fig.add_axes([0.075, 0.13, 0.88, 0.62])
    ax.set_facecolor(BG)
    x = np.arange(len(cats))
    ax.bar(x, vals, width=0.34, color=RED, zorder=3)
    for xi, v in zip(x, vals):
        ax.text(xi, v + 70, str(v), ha='center', va='bottom',
                fontsize=11.5, color=TXT)
    # 圆点：置于柱顶上方空白带，直径与同比成正比
    cy = 4550
    for xi, p in zip(x, yoy):
        ax.scatter(xi, cy, s=(p * 130) ** 2, color=BLUE, zorder=4,
                   edgecolor='none')
        ax.text(xi, cy, '%.0f%%' % (p * 100), ha='center', va='center',
                fontsize=10.5, color='white', zorder=5)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=13, color=TXT)
    ax.set_ylim(0, 4850)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#6E7079')
    ax.tick_params(length=0)
    save(fig, '26_柱形圆.png')


# ============================================================
# 27 簇状柱形折线图
# ============================================================
def fig27():
    cats   = ['华北', '华南', '东北', '西北', '西南', '华东']
    v2022  = [2354, 1902, 3524, 2698, 2896, 2563]
    v2021  = [2021, 1563, 3213, 2531, 2631, 2361]  # 华北原表为文本"2021"
    labels21 = ['2021', '1563', '3213', '2531', '2631', '2361']
    yoy    = [0.16, 0.22, 0.10, 0.07, 0.10, 0.09]

    fig = dashboard('上半年各月商品销量同比去年情况',
                    '2022年相比于2021年销量都有提升，半年整体提升17%',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06,30')
    ax = fig.add_axes([0.075, 0.13, 0.88, 0.62])
    ax.set_facecolor(BG)
    x = np.arange(len(cats))
    ax.bar(x - 0.15, v2022, width=0.26, color=BLUE, zorder=3, label='2022')
    ax.bar(x + 0.15, v2021, width=0.26, color=RED, zorder=3, label='2021')
    for xi, v in zip(x, v2022):
        ax.text(xi - 0.15, v + 70, str(v), ha='center', va='bottom',
                fontsize=11, color=TXT)
    for xi, v, lab in zip(x, v2021, labels21):
        ax.text(xi + 0.15, v + 70, lab, ha='center', va='bottom',
                fontsize=11, color=TXT)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=13, color=TXT)
    ax.set_ylim(0, 5200)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#6E7079')
    ax.tick_params(length=0)

    ax2 = ax.twinx()
    ax2.plot(x, yoy, color=YELLOW, lw=2.4, marker='o', ms=7, zorder=5)
    for xi, v in zip(x, yoy):
        ax2.text(xi, v + 0.012, '%.0f%%' % (v * 100), ha='center',
                 va='bottom', fontsize=11.5, color=TXT)
    ax2.set_ylim(-0.30, 0.24)
    ax2.axis('off')

    # 右下角自定义图例（深色底+彩色描边）
    for i, (c, t) in enumerate([(BLUE, '2022'), (RED, '2021')]):
        bx, by = 0.855, 0.20 - i * 0.11
        ax.add_patch(Rectangle((bx, by), 0.11, 0.07, transform=ax.transAxes,
                               facecolor='#232A55', edgecolor=c, lw=1.4,
                               zorder=6))
        ax.text(bx + 0.055, by + 0.035, t, transform=ax.transAxes,
                ha='center', va='center', fontsize=11.5, color=TXT, zorder=7)
    save(fig, '27_簇状柱形折线图.png')


# ============================================================
# 28 复合柱形图
# ============================================================
def fig28():
    months = ['1月', '2月', '3月', '4月', '5月', '6月',
              '7月', '8月', '9月', '10月', '11月', '12月']
    monthly = [2354, 1902, 3524, 2698, 2896, 2563,
               3156, 2896, 3621, 2635, 2963, 2789]
    quarter = [7780, 8157, 9673, 8387]
    # 每组3个月，组间空一个位置
    pos = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14]
    group_centers = [1, 5, 9, 13]

    fig = dashboard('2021年各月化妆品销量走势',
                    '2021年第三季度销量最多9673，9月单月销量最大3621',
                    '*注：数据来源于公司销售系统，统计日期截至2021.12.31')
    ax = fig.add_axes([0.06, 0.13, 0.90, 0.63])
    ax.set_facecolor(BG)
    # 季度总量背景块
    for gc, q, c in zip(group_centers, quarter, Q_COLORS):
        ax.add_patch(Rectangle((gc - 1.42, 0), 2.84, q, facecolor=c,
                               alpha=0.20, edgecolor='none', zorder=1))
        ax.text(gc, q + 130, str(q), ha='center', va='bottom',
                fontsize=11.5, color=TXT, zorder=3)
    # 月度窄柱（颜色同季度）
    for p, v, m in zip(pos, monthly, months):
        q = p // 4   # 位置 0-2/4-6/8-10/12-14 对应四个季度
        ax.bar(p, v, width=0.62, color=Q_COLORS[q], zorder=2)
        ax.text(p, v + 90, str(v), ha='center', va='bottom',
                fontsize=10.5, color=TXT)
    ax.set_xticks(pos); ax.set_xticklabels(months, fontsize=12.5, color=TXT)
    ax.set_xlim(-1.2, 15.2)
    ax.set_ylim(0, 10800)
    ax.set_yticks([])
    for s in ['top', 'right', 'left']:
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color('#6E7079')
    ax.tick_params(length=0)
    save(fig, '28_复合柱形图.png')


# ============================================================
# 29 滑珠图
# ============================================================
def _draw_bead_chart(fig, rows, p2022, p2021=None, title2021=False):
    ax = fig.add_axes([0.16, 0.13, 0.74, 0.66])
    ax.set_facecolor(BG)
    n = len(rows)
    ys = list(range(n - 1, -1, -1))   # 第一行在最上
    SCALE = 0.74                      # 轨道 100% 对应的 x 长度
    ax.set_xlim(-0.20, 0.92)
    ax.set_ylim(-0.6, n - 0.4)
    ax.axis('off')
    track_pt, bead_s = 15, 530
    for y, row, a in zip(ys, rows, p2022):
        px = a * SCALE
        # 区域名
        ax.text(-0.14, y, row, ha='right', va='center',
                fontsize=13.5, color=TXT)
        # 完整灰轨道 + 蓝色达成段
        capsule(ax, 0, SCALE, y, track_pt, GREY_TR, z=1)
        capsule(ax, 0, px, y, track_pt, BLUE, z=2)
        if p2021 is None:
            # 2022 珠子（蓝底白边）
            ax.scatter([px], [y], s=bead_s, facecolor=BLUE,
                       edgecolor='white', linewidths=1.3, zorder=5)
            ax.text(px - 0.03, y, '%.0f%%' % (a * 100), ha='right',
                    va='center', fontsize=12, color='white', zorder=6)
        else:
            b = p2021[rows.index(row)] * SCALE
            ax.scatter([px], [y], s=bead_s, facecolor=BLUE,
                       edgecolor='white', linewidths=1.3, zorder=5)
            ax.scatter([b], [y], s=bead_s, facecolor=GREY_BEAD,
                       edgecolor='white', linewidths=1.3, zorder=4)
            ax.text(px, y + 0.30, '%.0f%%' % (a * 100), ha='center',
                    va='bottom', fontsize=12, color=TXT, zorder=6)
    if p2021 is not None:
        leg_x, leg_y = -0.16, n - 0.65
        ax.scatter([leg_x], [leg_y], s=240, facecolor=BLUE,
                   edgecolor='white', linewidths=1.1, zorder=5)
        ax.text(leg_x + 0.04, leg_y, '2022完成率', va='center',
                fontsize=11.5, color=TXT)
        ax.scatter([leg_x + 0.22], [leg_y], s=240, facecolor=GREY_BEAD,
                   edgecolor='white', linewidths=1.1, zorder=5)
        ax.text(leg_x + 0.26, leg_y, '2021完率', va='center',
                fontsize=11.5, color=TXT)
    return ax


def fig29():
    data = [('华南', 0.86), ('华北', 0.74), ('东北', 0.62),
            ('西北', 0.51), ('华东', 0.35)]
    fig = dashboard('2022年上半年产品销量目标达成率情况',
                    '华南完成率最高达到86%，华东最低35%',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06.30')
    _draw_bead_chart(fig, [d[0] for d in data], [d[1] for d in data])
    save(fig, '29_滑珠图.png')


# ============================================================
# 30 对比滑珠图
# ============================================================
def fig30():
    data = [('华南', 0.86, 0.92), ('华北', 0.74, 0.69), ('东北', 0.62, 0.53),
            ('西北', 0.51, 0.39), ('华东', 0.35, 0.45)]
    fig = dashboard('2022年上半年销量目标达成率同比去年情况',
                    '华南完成率最高达到86%，华东最低35%，其中华南和华东不及2021年',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06.30')
    _draw_bead_chart(fig, [d[0] for d in data], [d[1] for d in data],
                     p2021=[d[2] for d in data])
    save(fig, '30_对比滑珠图.png')


ALL_FIGS = [fig16, fig17, fig18, fig19, fig20, fig21, fig22, fig23, fig24,
            fig25, fig26, fig27, fig28, fig29, fig30]

if __name__ == '__main__':
    for f in ALL_FIGS:
        try:
            f()
        except Exception as e:
            import traceback
            print('ERROR in %s: %s' % (f.__name__, e))
            traceback.print_exc()
    print('ALL DONE ->', OUT)
