# -*- coding: utf-8 -*-
"""
图表 05：层叠柱形图
复现《Excel数据可视化-从图表到数据大屏》第二章
运行: python 05_层叠柱形图.py  ->  生成 05_层叠柱形图.png
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

if __name__ == '__main__':
    fig05()
