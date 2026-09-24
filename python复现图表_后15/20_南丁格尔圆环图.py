# -*- coding: utf-8 -*-
"""
图表 20 南丁格尔圆环图
复现《Excel数据可视化 - 从图表到数据大屏》第二章后15个图表
运行: python 20_南丁格尔圆环图.py  ->  生成 20_南丁格尔圆环图.png
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


# ============ 20 南丁格尔圆环图 ============
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


if __name__ == '__main__':
    fig20()
