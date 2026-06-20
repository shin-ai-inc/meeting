#!/usr/bin/env python3
"""Generate OGP image for ShinAI LP (1200x630)."""

import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT = os.path.join(PROJECT_DIR, 'public', 'assets', 'ogp.png')

W, H = 1200, 630

NAVY = (6, 31, 68)
NAVY_DEEP = (4, 14, 36)
GOLD = (197, 165, 90)
GOLD_LIGHT = (220, 192, 130)
WHITE = (255, 255, 255)

FONT_JP = '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'
FONT_LATIN = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def generate():
    img = Image.new('RGB', (W, H), NAVY_DEEP)
    d = ImageDraw.Draw(img)

    # Background gradient
    for y in range(H):
        t = y / H
        c = lerp_color(NAVY_DEEP, NAVY, t * 0.6)
        d.line([(0, y), (W, y)], fill=c)

    # Subtle radial glow
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    cx, cy = W // 2, H // 2 + 40
    for r in range(400, 0, -3):
        a = int(12 * (1 - r / 400) ** 2)
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD + (a,))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    d = ImageDraw.Draw(img)

    # Gold accent lines
    line_y_top = 80
    line_y_bottom = H - 80
    d.line([(100, line_y_top), (W - 100, line_y_top)], fill=GOLD + (40,), width=1)
    d.line([(100, line_y_bottom), (W - 100, line_y_bottom)], fill=GOLD + (40,), width=1)

    # Short gold bar center-top
    bar_w = 40
    d.line([(W // 2 - bar_w // 2, line_y_top + 40),
            (W // 2 + bar_w // 2, line_y_top + 40)], fill=GOLD, width=2)

    # Brand: "ShinAI"
    try:
        font_brand = ImageFont.truetype(FONT_LATIN, 52)
    except Exception:
        font_brand = ImageFont.load_default()

    brand_text = "ShinAI"
    bbox = d.textbbox((0, 0), brand_text, font=font_brand)
    bw = bbox[2] - bbox[0]
    d.text(((W - bw) // 2, 150), brand_text, fill=WHITE, font=font_brand)

    # Subtitle
    try:
        font_sub = ImageFont.truetype(FONT_JP, 16)
    except Exception:
        font_sub = ImageFont.load_default()

    sub_text = "AI・業務最適化の伴走支援"
    bbox_s = d.textbbox((0, 0), sub_text, font=font_sub)
    sw = bbox_s[2] - bbox_s[0]
    d.text(((W - sw) // 2, 130), sub_text, fill=GOLD_LIGHT, font=font_sub)

    # Main copy
    try:
        font_main = ImageFont.truetype(FONT_JP, 42)
    except Exception:
        font_main = ImageFont.load_default()

    lines = ["まずは、", "AIが働ける土台を。"]
    y_start = 260
    for i, line in enumerate(lines):
        bbox_m = d.textbbox((0, 0), line, font=font_main)
        mw = bbox_m[2] - bbox_m[0]
        d.text(((W - mw) // 2, y_start + i * 64), line, fill=WHITE, font=font_main)

    # Description
    try:
        font_desc = ImageFont.truetype(FONT_JP, 18)
    except Exception:
        font_desc = ImageFont.load_default()

    desc_lines = [
        "社内に散在する文書・資料を整え、",
        "AIが読める・つながる・答えられる状態へ。",
    ]
    y_desc = 430
    for i, line in enumerate(desc_lines):
        bbox_d = d.textbbox((0, 0), line, font=font_desc)
        dw = bbox_d[2] - bbox_d[0]
        alpha_color = lerp_color(WHITE, NAVY, 0.3)
        d.text(((W - dw) // 2, y_desc + i * 32), line, fill=alpha_color, font=font_desc)

    # Gold bar bottom
    d.line([(W // 2 - bar_w // 2, line_y_bottom - 40),
            (W // 2 + bar_w // 2, line_y_bottom - 40)], fill=GOLD, width=2)

    img.save(OUTPUT, 'PNG', optimize=True)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f'OGP image saved: {W}x{H}, {size_kb:.0f}KB → {OUTPUT}')


if __name__ == '__main__':
    generate()
