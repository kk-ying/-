# -*- coding: utf-8 -*-
"""
图表 22 仪表盘图
复现《Excel数据可视化 - 从图表到数据大屏》第二章后15个图表
运行: python 22_仪表盘图.py  ->  生成 22_仪表盘图.png
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


# ============ 22 仪表盘图 ============
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


if __name__ == '__main__':
    fig22()
