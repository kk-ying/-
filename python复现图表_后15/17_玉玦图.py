# -*- coding: utf-8 -*-
"""
图表 17 玉玦图
复现《Excel数据可视化 - 从图表到数据大屏》第二章后15个图表
运行: python 17_玉玦图.py  ->  生成 17_玉玦图.png
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


# ============ 17 玉玦图 ============
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


if __name__ == '__main__':
    fig17()
