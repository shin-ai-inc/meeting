#!/usr/bin/env python3
"""Generate a premium hero image for ShinAI LP.

Concept: Elegant golden geometric composition on deep navy,
representing structured information rising into clarity.
Rendered at 2x and downscaled for anti-aliased quality.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT = os.path.join(PROJECT_DIR, 'public', 'assets', 'hero-visual.webp')

SCALE = 2
W, H = 1600 * SCALE, 900 * SCALE
OUT_W, OUT_H = 1600, 900

NAVY_DEEP = (4, 14, 36)
NAVY = (6, 31, 68)
NAVY_MID = (12, 42, 88)
NAVY_LIGHT = (18, 55, 110)
GOLD = (197, 165, 90)
GOLD_LIGHT = (220, 192, 130)
GOLD_PALE = (235, 215, 170)
GOLD_DARK = (160, 130, 65)
GOLD_GLOW = (240, 215, 160)
GOLD_BRIGHT = (255, 235, 180)

random.seed(42)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))


def draw_radial_gradient(img, cx, cy, radius, color, max_alpha, power=1.5):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    step = max(1, radius // 200)
    for r in range(radius, 0, -step):
        t = 1.0 - r / radius
        a = int(max_alpha * (t ** power))
        if a > 0:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    return Image.alpha_composite(img, overlay)


def draw_block(img, cx, cy, bw, bh, bd, colors, alpha=240):
    """Draw a polished isometric block with gradient faces."""
    base, light, dark, highlight = colors
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    dx = bd * 0.55
    dy = bd * 0.32

    # Shadow beneath block
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    shadow_pts = [
        (cx - bw/2 + 8, cy + 4),
        (cx + bw/2 + 8, cy + 4),
        (cx + bw/2 + dx + 8, cy - dy + 8),
        (cx - bw/2 + dx + 8, cy - dy + 8),
    ]
    sd.polygon(shadow_pts, fill=(0, 0, 0, 30))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12 * SCALE))
    img = Image.alpha_composite(img, shadow)

    # Front face with vertical gradient
    front = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(front)
    for row in range(int(bh)):
        t = row / max(bh, 1)
        c = lerp_color(light, dark, t * 0.7)
        y = int(cy - bh + row)
        fd.line([(int(cx - bw/2), y), (int(cx + bw/2), y)], fill=c + (alpha,))
    overlay = Image.alpha_composite(overlay, front)
    d = ImageDraw.Draw(overlay)

    # Top face with gradient
    top_pts = [
        (cx - bw/2, cy - bh),
        (cx - bw/2 + dx, cy - bh - dy),
        (cx + bw/2 + dx, cy - bh - dy),
        (cx + bw/2, cy - bh),
    ]
    top_face = Image.new('RGBA', img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top_face)
    td.polygon(top_pts, fill=highlight + (alpha,))
    # Add subtle gradient to top
    top_grad = Image.new('RGBA', img.size, (0, 0, 0, 0))
    tgd = ImageDraw.Draw(top_grad)
    for i in range(int(dy)):
        t = i / max(dy, 1)
        a = int(40 * t)
        y = int(cy - bh - dy + i)
        tgd.line([(int(cx - bw/2 + dx * (1 - t)), y),
                   (int(cx + bw/2 + dx * (1 - t)), y)],
                  fill=(0, 0, 0, a))
    top_face = Image.alpha_composite(top_face, top_grad)
    overlay = Image.alpha_composite(overlay, top_face)
    d = ImageDraw.Draw(overlay)

    # Right face
    right_pts = [
        (cx + bw/2, cy - bh),
        (cx + bw/2 + dx, cy - bh - dy),
        (cx + bw/2 + dx, cy - dy),
        (cx + bw/2, cy),
    ]
    d.polygon(right_pts, fill=dark + (alpha,))

    # Edge highlights
    edge_alpha = min(alpha + 30, 255)
    d.line([top_pts[0], top_pts[1]], fill=GOLD_BRIGHT + (edge_alpha,), width=max(1, SCALE))
    d.line([top_pts[1], top_pts[2]], fill=GOLD_PALE + (edge_alpha,), width=max(1, SCALE))
    d.line([top_pts[2], top_pts[3]], fill=GOLD_LIGHT + (edge_alpha // 2,), width=max(1, SCALE))

    # Front top edge
    d.line([top_pts[0], top_pts[3]], fill=light + (edge_alpha,), width=max(1, SCALE))

    # Front-right vertical edge
    d.line([(cx + bw/2, cy - bh), (cx + bw/2, cy)],
           fill=lerp_color(light, dark, 0.4) + (edge_alpha // 2,), width=max(1, SCALE))

    return Image.alpha_composite(img, overlay)


def draw_golden_curve(img, points, color, width=2, alpha=60):
    """Draw a smooth golden bezier-like curve."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Interpolate smooth curve through points
    curve_pts = []
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        steps = 40
        for s in range(steps):
            t = s / steps
            # Smooth interpolation
            t2 = t * t * (3 - 2 * t)
            x = lerp(x0, x1, t2)
            y = lerp(y0, y1, t2)
            curve_pts.append((int(x), int(y)))

    # Draw the curve with varying alpha
    for i in range(len(curve_pts) - 1):
        t = i / max(len(curve_pts) - 1, 1)
        # Fade at ends
        fade = min(t * 4, 1.0) * min((1 - t) * 4, 1.0)
        a = int(alpha * fade)
        if a > 0:
            d.line([curve_pts[i], curve_pts[i + 1]],
                   fill=color + (a,), width=width)

    return Image.alpha_composite(img, overlay)


def draw_diamond(img, cx, cy, size, color, alpha=120):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    pts = [
        (cx, cy - size),
        (cx + size * 0.6, cy),
        (cx, cy + size),
        (cx - size * 0.6, cy),
    ]
    d.polygon(pts, fill=color + (alpha,))
    # Bright center
    inner = size // 3
    inner_pts = [
        (cx, cy - inner),
        (cx + inner * 0.6, cy),
        (cx, cy + inner),
        (cx - inner * 0.6, cy),
    ]
    d.polygon(inner_pts, fill=GOLD_BRIGHT + (min(alpha + 40, 255),))
    return Image.alpha_composite(img, overlay)


def generate():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # === Background ===
    img = Image.new('RGBA', (W, H), NAVY_DEEP + (255,))

    # Multi-stop background gradient
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        if t < 0.4:
            c = lerp_color(NAVY_DEEP, NAVY, t / 0.4)
        elif t < 0.7:
            c = lerp_color(NAVY, NAVY_MID, (t - 0.4) / 0.3)
        else:
            c = lerp_color(NAVY_MID, (3, 10, 28), (t - 0.7) / 0.3)
        bd.line([(0, y), (W, y)], fill=c + (255,))
    img = Image.alpha_composite(img, bg)

    # Atmospheric glows
    img = draw_radial_gradient(img, int(W * 0.48), int(H * 0.55), int(600 * SCALE),
                                GOLD_DARK, 22, 2.0)
    img = draw_radial_gradient(img, int(W * 0.52), int(H * 0.48), int(400 * SCALE),
                                GOLD, 12, 2.0)
    img = draw_radial_gradient(img, int(W * 0.70), int(H * 0.20), int(450 * SCALE),
                                NAVY_LIGHT, 20, 1.8)
    img = draw_radial_gradient(img, int(W * 0.25), int(H * 0.75), int(350 * SCALE),
                                (8, 25, 55), 18, 1.8)

    # === Subtle grid lines (information structure) ===
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)

    # Horizontal lines
    for ly in range(int(H * 0.25), int(H * 0.80), int(50 * SCALE)):
        dist_from_center = abs(ly - H * 0.52) / H
        a = max(3, int(12 * (1 - dist_from_center * 1.5)))
        gd.line([(int(W * 0.15), ly), (int(W * 0.85), ly)],
                fill=GOLD_DARK + (a,), width=1)

    # Vertical lines (sparser)
    for lx in range(int(W * 0.25), int(W * 0.78), int(80 * SCALE)):
        dist_from_center = abs(lx - W * 0.50) / W
        a = max(2, int(8 * (1 - dist_from_center * 2)))
        gd.line([(lx, int(H * 0.30)), (lx, int(H * 0.75))],
                fill=GOLD_DARK + (a,), width=1)

    img = Image.alpha_composite(img, grid)

    # === Block composition ===
    gold_colors = (GOLD, GOLD_LIGHT, GOLD_DARK, GOLD_PALE)
    mid_colors = (
        lerp_color(GOLD_DARK, GOLD, 0.5),
        lerp_color(GOLD, GOLD_LIGHT, 0.5),
        lerp_color(GOLD_DARK, NAVY, 0.25),
        lerp_color(GOLD_LIGHT, GOLD_PALE, 0.5),
    )
    back_colors = (
        lerp_color(NAVY_MID, GOLD_DARK, 0.35),
        lerp_color(NAVY_MID, GOLD, 0.4),
        lerp_color(NAVY_DEEP, GOLD_DARK, 0.15),
        lerp_color(NAVY_MID, GOLD_LIGHT, 0.3),
    )

    s = SCALE

    # Back row
    back_blocks = [
        (W*0.28, H*0.48, 85*s, 60*s, 28*s, 140),
        (W*0.42, H*0.44, 95*s, 72*s, 32*s, 155),
        (W*0.58, H*0.46, 80*s, 58*s, 26*s, 135),
        (W*0.71, H*0.49, 70*s, 50*s, 22*s, 125),
    ]
    for bx, by, bw, bh, bd, alpha in back_blocks:
        img = draw_block(img, bx, by, bw, bh, bd, back_colors, alpha)

    # Middle row
    mid_blocks = [
        (W*0.33, H*0.60, 115*s, 90*s, 38*s, 200),
        (W*0.50, H*0.56, 135*s, 105*s, 45*s, 210),
        (W*0.66, H*0.61, 105*s, 82*s, 36*s, 195),
    ]
    for bx, by, bw, bh, bd, alpha in mid_blocks:
        img = draw_block(img, bx, by, bw, bh, bd, mid_colors, alpha)

    # Front row (most prominent)
    front_blocks = [
        (W*0.36, H*0.76, 155*s, 125*s, 52*s, 240),
        (W*0.56, H*0.72, 175*s, 145*s, 60*s, 248),
        (W*0.74, H*0.78, 135*s, 110*s, 45*s, 235),
    ]
    for bx, by, bw, bh, bd, alpha in front_blocks:
        img = draw_block(img, bx, by, bw, bh, bd, gold_colors, alpha)

    # Keystone block (tallest, central)
    keystone_colors = (GOLD, GOLD_GLOW, GOLD_DARK, GOLD_BRIGHT)
    img = draw_block(img, W*0.48, H*0.66, 125*s, 175*s, 48*s,
                     keystone_colors, 252)

    # Glow above keystone
    img = draw_radial_gradient(img, int(W*0.48), int(H*0.66 - 175*s),
                                int(120*SCALE), GOLD_LIGHT, 28, 1.8)
    img = draw_radial_gradient(img, int(W*0.48), int(H*0.66 - 175*s - 20*s),
                                int(60*SCALE), GOLD_GLOW, 18, 1.5)

    # === Flowing golden curves (data flow / connection) ===
    curves = [
        # Left flowing curve
        [(W*0.12, H*0.65), (W*0.25, H*0.50), (W*0.35, H*0.42),
         (W*0.48, H*0.38)],
        # Right flowing curve
        [(W*0.88, H*0.60), (W*0.75, H*0.48), (W*0.65, H*0.40),
         (W*0.52, H*0.36)],
        # Bottom left to center
        [(W*0.15, H*0.85), (W*0.30, H*0.72), (W*0.42, H*0.62)],
        # Bottom right to center
        [(W*0.85, H*0.82), (W*0.72, H*0.70), (W*0.60, H*0.60)],
        # Upper arc
        [(W*0.30, H*0.22), (W*0.40, H*0.18), (W*0.55, H*0.16),
         (W*0.68, H*0.20)],
    ]

    for pts in curves:
        c = lerp_color(GOLD, GOLD_LIGHT, random.uniform(0.2, 0.6))
        img = draw_golden_curve(img, pts, c, width=max(2, 2*SCALE),
                                alpha=random.randint(30, 55))

    # === Diamond accent markers at curve intersections ===
    diamonds = [
        (W*0.48, H*0.37, 8*s),
        (W*0.30, H*0.22, 5*s),
        (W*0.68, H*0.20, 5*s),
        (W*0.15, H*0.85, 4*s),
        (W*0.85, H*0.82, 4*s),
        (W*0.12, H*0.65, 4*s),
        (W*0.88, H*0.60, 4*s),
    ]
    for dx, dy, sz in diamonds:
        img = draw_diamond(img, int(dx), int(dy), int(sz),
                           GOLD_LIGHT, random.randint(60, 110))

    # === Floating particles ===
    particle = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particle)

    # Small particles
    for _ in range(100):
        px = random.randint(int(W*0.08), int(W*0.92))
        py = random.randint(int(W*0.05), int(H*0.92))
        size = random.randint(1*SCALE, 3*SCALE)
        a = random.randint(15, 70)
        c = lerp_color(GOLD, GOLD_LIGHT, random.random())
        pd.ellipse([px, py, px + size, py + size], fill=c + (a,))

    # Medium particles with glow
    for _ in range(20):
        px = random.randint(int(W*0.15), int(W*0.85))
        py = random.randint(int(H*0.10), int(H*0.80))
        size = random.randint(3*SCALE, 5*SCALE)
        a = random.randint(50, 120)
        # Outer glow
        glow_size = size * 3
        pd.ellipse([px - glow_size, py - glow_size,
                     px + size + glow_size, py + size + glow_size],
                    fill=GOLD_GLOW + (a // 6,))
        pd.ellipse([px, py, px + size, py + size],
                    fill=GOLD_BRIGHT + (a,))

    img = Image.alpha_composite(img, particle)

    # === Vignette ===
    vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    vig_depth = int(120 * SCALE)
    for edge in range(vig_depth):
        t = 1 - edge / vig_depth
        a = int(65 * (t ** 2))
        vd.rectangle([edge, edge, W - edge, H - edge],
                     outline=(0, 0, 0, a))
    img = Image.alpha_composite(img, vignette)

    # === Final processing ===
    rgb = img.convert('RGB')

    # Slight blur for anti-aliasing smoothness
    rgb = rgb.filter(ImageFilter.GaussianBlur(0.8 * SCALE))

    # Downscale with high-quality resampling
    rgb = rgb.resize((OUT_W, OUT_H), Image.LANCZOS)

    rgb.save(OUTPUT, 'WEBP', quality=92)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f'Hero image saved: {OUT_W}x{OUT_H}, {size_kb:.0f}KB')
    print(f'Output: {OUTPUT}')


if __name__ == '__main__':
    generate()
