# -*- coding: utf-8 -*-
"""
图表 29 滑珠图
复现《Excel数据可视化 - 从图表到数据大屏》第二章后15个图表
运行: python 29_滑珠图.py  ->  生成 29_滑珠图.png
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


# ============ 29 滑珠图 ============
def fig29():
    data = [('华南', 0.86), ('华北', 0.74), ('东北', 0.62),
            ('西北', 0.51), ('华东', 0.35)]
    fig = dashboard('2022年上半年产品销量目标达成率情况',
                    '华南完成率最高达到86%，华东最低35%',
                    '*注：数据来源于公司销售系统，统计日期截至2022.06.30')
    _draw_bead_chart(fig, [d[0] for d in data], [d[1] for d in data])
    save(fig, '29_滑珠图.png')


if __name__ == '__main__':
    fig29()
