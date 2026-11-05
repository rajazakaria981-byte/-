"""Animated Red Spider Lily — Matplotlib edition.

Install:
    python -m pip install numpy matplotlib

Run:
    python red_spider_lily.py
Press Q or close the window to stop.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------- Scene ----------
FIG_SIZE = (8, 9)
FPS = 30
DURATION = 8
FRAMES = FPS * DURATION

fig, ax = plt.subplots(figsize=FIG_SIZE)
fig.patch.set_facecolor("#050509")
ax.set_facecolor("#050509")
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.8, 3.0)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("RED SPIDER LILY", color="#f5d7df", fontsize=17,
             fontweight="bold", pad=18)

# Soft background stars
rng = np.random.default_rng(12)
for _ in range(90):
    x, y = rng.uniform(-2.4, 2.4), rng.uniform(-2.6, 2.8)
    ax.scatter(x, y, s=rng.uniform(1, 5), color="#9b718b",
               alpha=rng.uniform(.12, .45), linewidths=0)

# Stem and leaves
t = np.linspace(0, 1, 160)
stem_x = -0.08 + 0.10 * np.sin(t * 2.1)
stem_y = -2.35 + 2.45 * t
ax.plot(stem_x, stem_y, color="#477b48", lw=4, solid_capstyle="round")
ax.plot(stem_x + .025, stem_y, color="#8eb56c", lw=1, alpha=.55)

leaf_t = np.linspace(0, 1, 100)
for side in (-1, 1):
    x0, y0 = -.05, -1.95
    lx = x0 + side * (1.25 * leaf_t) + .08 * np.sin(leaf_t * np.pi)
    ly = y0 - .35 * leaf_t + .52 * np.sin(leaf_t * np.pi)
    ax.plot(lx, ly, color="#315f3b", lw=9, solid_capstyle="round", alpha=.9)
    ax.plot(lx, ly + .015, color="#83a85c", lw=1.4, alpha=.7)

# Curled petals: long flowing curves radiating from the flower center.
center = np.array([0.0, 0.18])
petal_lines = []
petal_glows = []
petal_count = 6
for i in range(petal_count):
    angle = 2 * np.pi * i / petal_count - np.pi / 2
    u = np.linspace(0, 1, 180)
    length = 1.75 + .18 * np.sin(i * 2.3)
    # A sweeping, curling path with a delicate hooked tip.
    radial = length * u
    bend = .40 * np.sin(np.pi * u) + .42 * u**3
    x = center[0] + radial * np.cos(angle) - bend * np.sin(angle)
    y = center[1] + radial * np.sin(angle) + bend * np.cos(angle)
    glow, = ax.plot(x, y, color="#8f1638", lw=10, alpha=.14,
                    solid_capstyle="round")
    line, = ax.plot(x, y, color="#e52b54", lw=3.2,
                    solid_capstyle="round")
    ax.plot(x, y, color="#ff8a9e", lw=.8, alpha=.75)
    petal_glows.append(glow)
    petal_lines.append(line)

# Central filaments and golden pollen tips
filaments = []
tips = []
for i in range(18):
    a = 2 * np.pi * i / 18
    length = .9 + .28 * np.sin(i * 4.7)
    u = np.linspace(0, 1, 70)
    bend = .12 * np.sin(u * np.pi)
    x = center[0] + .08 * np.cos(a) + length * u * np.cos(a) - bend * np.sin(a)
    y = center[1] + .08 * np.sin(a) + length * u * np.sin(a) + bend * np.cos(a)
    filament, = ax.plot(x, y, color="#f6a3b0", lw=1.2, alpha=.9)
    tip = ax.scatter([x[-1]], [y[-1]], s=18, color="#ffd36b",
                     edgecolors="#fff0b0", linewidths=.35, zorder=8)
    filaments.append(filament)
    tips.append(tip)

# Floating glowing particles
particle_count = 38
px = rng.uniform(-2.1, 2.1, particle_count)
py = rng.uniform(-2.4, 2.5, particle_count)
phase = rng.uniform(0, 2 * np.pi, particle_count)
sizes = rng.uniform(4, 20, particle_count)
particles = ax.scatter(px, py, s=sizes, color="#ffb6c8",
                       alpha=.45, edgecolors="none", zorder=10)

# Small glow behind the flower
ax.scatter([center[0]], [center[1]], s=850, color="#c91f4a",
           alpha=.08, edgecolors="none", zorder=0)

def animate(frame):
    time = frame / FPS
    pulse = .88 + .12 * np.sin(time * 2 * np.pi / 3)
    for glow, line in zip(petal_glows, petal_lines):
        glow.set_linewidth(8 + 2 * pulse)
        line.set_linewidth(2.7 + .6 * pulse)

    # Filaments gently sway together.
    sway = .025 * np.sin(time * 2.2)
    for i, (filament, tip) in enumerate(zip(filaments, tips)):
        a = 2 * np.pi * i / len(filaments)
        # Keep the original shape, adding a tiny moving offset.
        xdata, ydata = filament.get_data()
        filament.set_data(xdata + sway * np.cos(a),
                          ydata + sway * np.sin(a))
        tip.set_offsets([[xdata[-1] + sway * np.cos(a),
                          ydata[-1] + sway * np.sin(a)]])

    particles.set_offsets(np.c_[px + .035 * np.sin(time + phase),
                                py + .07 * np.sin(time * 1.4 + phase)])
    particles.set_alpha(.25 + .3 * (0.5 + 0.5 * np.sin(time * 2 + phase)))
    return petal_glows + petal_lines + filaments + tips + [particles]

ani = FuncAnimation(fig, animate, frames=FRAMES, interval=1000 / FPS,
                    blit=False, repeat=True)
plt.tight_layout()
plt.show()
