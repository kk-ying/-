# -*- coding: utf-8 -*-
"""
图表 15：水球图
复现《Excel数据可视化-从图表到数据大屏》第二章
运行: python 15_水球图.py  ->  生成 15_水球图.png
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
    fig15()
