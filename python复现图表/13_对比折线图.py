# -*- coding: utf-8 -*-
"""
图表 13：对比折线图
复现《Excel数据可视化-从图表到数据大屏》第二章
运行: python 13_对比折线图.py  ->  生成 13_对比折线图.png
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

if __name__ == '__main__':
    fig13()
