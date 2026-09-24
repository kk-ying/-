# -*- coding: utf-8 -*-
"""
图表 09：对比柱形图
复现《Excel数据可视化-从图表到数据大屏》第二章
运行: python 09_对比柱形图.py  ->  生成 09_对比柱形图.png
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

if __name__ == '__main__':
    fig09()
