#!/usr/bin/env python3
"""Generate professional LP images for ShinAI using Pillow."""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(PROJECT_DIR, 'public', 'assets')

NAVY = (6, 31, 68)
NAVY_LIGHT = (15, 50, 100)
GOLD = (197, 165, 90)
GOLD_SOFT = (212, 183, 106)
WHITE = (255, 255, 255)
BG_WARM = (246, 244, 238)
GRAY_LIGHT = (235, 233, 228)

def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    if fill:
        draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
        draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
        draw.pieslice([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=fill)
        draw.pieslice([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=fill)
        draw.pieslice([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=fill)
        draw.pieslice([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0 + r, y0, x1 - r, y0], fill=outline, width=width)
        draw.line([x0 + r, y1, x1 - r, y1], fill=outline, width=width)
        draw.line([x0, y0 + r, x0, y1 - r], fill=outline, width=width)
        draw.line([x1, y0 + r, x1, y1 - r], fill=outline, width=width)


def get_font(size):
    paths = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()


def generate_hero_image():
    """Professional dashboard mockup showing organized information management."""
    W, H = 1200, 640
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # === Main dashboard card ===
    card_w, card_h = 720, 520
    card_x, card_y = (W - card_w) // 2, (H - card_h) // 2

    # Shadow layer
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    rounded_rect(sd, (card_x + 4, card_y + 6, card_x + card_w + 4, card_y + card_h + 6), 20,
                 fill=(0, 0, 0, 35))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    # Card body
    rounded_rect(draw, (card_x, card_y, card_x + card_w, card_y + card_h), 20,
                 fill=WHITE + (250,))

    # Navy sidebar
    sidebar_w = 72
    rounded_rect(draw, (card_x, card_y, card_x + sidebar_w, card_y + card_h), 20,
                 fill=NAVY + (255,))
    draw.rectangle([card_x + sidebar_w - 20, card_y, card_x + sidebar_w, card_y + card_h],
                   fill=NAVY + (255,))

    # Sidebar brand mark
    bx = card_x + sidebar_w // 2
    draw.rectangle([bx - 12, card_y + 28, bx + 12, card_y + 30], fill=GOLD + (180,))

    # Sidebar menu items
    for i, sy in enumerate(range(card_y + 70, card_y + 380, 50)):
        is_active = (i == 2)
        if is_active:
            draw.rectangle([card_x + 4, sy - 6, card_x + sidebar_w, sy + 24],
                          fill=(255, 255, 255, 15))
            draw.rectangle([card_x, sy - 6, card_x + 3, sy + 24], fill=GOLD + (220,))
        dot_color = GOLD + (200,) if is_active else (255, 255, 255, 50)
        draw.ellipse([bx - 8, sy, bx + 8, sy + 16], fill=dot_color)
        # Mini line next to dot
        if is_active:
            draw.rectangle([bx - 16, sy + 22, bx + 16, sy + 23], fill=(255, 255, 255, 30))

    # === Content area ===
    cx = card_x + sidebar_w + 28
    cy = card_y + 24

    # Header bar
    draw.rectangle([cx, cy, cx + 180, cy + 14], fill=NAVY + (50,))
    draw.rectangle([card_x + card_w - 100, cy, card_x + card_w - 28, cy + 14],
                   fill=(230, 228, 222, 200))
    draw.rectangle([card_x + card_w - 60, cy + 22, card_x + card_w - 28, cy + 32],
                   fill=GOLD + (60,))

    # Separator line
    cy += 48
    draw.rectangle([cx, cy, card_x + card_w - 28, cy + 1], fill=(230, 228, 222, 200))

    # Content rows
    cy += 20
    row_h = 56
    for i in range(7):
        ry = cy + i * (row_h + 8)
        is_highlight = (i == 2)

        # Row background
        row_fill = (250, 246, 235, 255) if is_highlight else (252, 251, 249, 255)
        rounded_rect(draw, (cx, ry, card_x + card_w - 28, ry + row_h), 10, fill=row_fill)

        # Left accent
        if is_highlight:
            draw.rectangle([cx, ry + 8, cx + 3, ry + row_h - 8], fill=GOLD + (200,))

        # Status circle
        sx = cx + 20
        status_fill = GOLD if is_highlight else (200, 198, 192)
        draw.ellipse([sx, ry + 18, sx + 18, ry + 36], fill=status_fill + (180,))
        # Checkmark in circle
        draw.ellipse([sx + 4, ry + 22, sx + 14, ry + 32], fill=WHITE + (180,))

        # Title bar
        tx = sx + 30
        title_w = random.randint(130, 240)
        title_fill = NAVY + (160,) if is_highlight else (180, 178, 172, 160)
        draw.rectangle([tx, ry + 16, tx + title_w, ry + 28], fill=title_fill)

        # Subtitle bar
        sub_w = random.randint(80, 140)
        draw.rectangle([tx, ry + 34, tx + sub_w, ry + 42], fill=(215, 213, 208, 130))

        # Right side tag
        if i % 2 == 0 or is_highlight:
            tag_x = card_x + card_w - 110
            tag_fill = GOLD + (40,) if is_highlight else NAVY + (20,)
            rounded_rect(draw, (tag_x, ry + 18, tag_x + 60, ry + 34), 4, fill=tag_fill)
            draw.rectangle([tag_x + 8, ry + 24, tag_x + 48, ry + 28],
                          fill=GOLD + (60,) if is_highlight else NAVY + (30,))

    # === Floating notification card (top-right, overlapping) ===
    notif_w, notif_h = 200, 100
    nx = card_x + card_w - 60
    ny = card_y - 20

    # Notification shadow
    nshadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    nsd = ImageDraw.Draw(nshadow)
    rounded_rect(nsd, (nx + 3, ny + 4, nx + notif_w + 3, ny + notif_h + 4), 12,
                 fill=(0, 0, 0, 30))
    nshadow = nshadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, nshadow)
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, (nx, ny, nx + notif_w, ny + notif_h), 12,
                 fill=WHITE + (245,), outline=(230, 228, 222), width=1)
    # Gold top accent
    draw.rectangle([nx + 20, ny + 12, nx + 50, ny + 14], fill=GOLD + (160,))
    # Content lines
    draw.rectangle([nx + 20, ny + 26, nx + 160, ny + 36], fill=NAVY + (60,))
    draw.rectangle([nx + 20, ny + 44, nx + 130, ny + 52], fill=(220, 218, 212, 160))
    draw.rectangle([nx + 20, ny + 60, nx + 100, ny + 68], fill=(220, 218, 212, 120))
    # Gold indicator
    draw.ellipse([nx + notif_w - 30, ny + 12, nx + notif_w - 18, ny + 24],
                fill=GOLD + (200,))

    # === Floating mini card (bottom-left, overlapping) ===
    mini_w, mini_h = 180, 120
    mx = card_x - 50
    my = card_y + card_h - 100

    mshadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    msd = ImageDraw.Draw(mshadow)
    rounded_rect(msd, (mx + 3, my + 4, mx + mini_w + 3, my + mini_h + 4), 12,
                 fill=(0, 0, 0, 25))
    mshadow = mshadow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, mshadow)
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, (mx, my, mx + mini_w, my + mini_h), 12,
                 fill=NAVY + (240,))
    # Connected nodes mini visualization
    nodes = [(mx + 40, my + 35), (mx + 100, my + 30), (mx + 140, my + 50),
             (mx + 60, my + 70), (mx + 120, my + 80)]
    for i, (nx1, ny1) in enumerate(nodes):
        for j, (nx2, ny2) in enumerate(nodes):
            if j > i and abs(i - j) <= 2:
                draw.line([(nx1, ny1), (nx2, ny2)], fill=(255, 255, 255, 40), width=1)
    for nx1, ny1 in nodes:
        draw.ellipse([nx1 - 5, ny1 - 5, nx1 + 5, ny1 + 5], fill=(255, 255, 255, 70))
        draw.ellipse([nx1 - 3, ny1 - 3, nx1 + 3, ny1 + 3], fill=GOLD + (160,))

    # Label
    draw.rectangle([mx + 30, my + mini_h - 28, mx + 120, my + mini_h - 18],
                  fill=(255, 255, 255, 40))

    # Save with tight crop
    bbox = img.getbbox()
    if bbox:
        final = img.crop(bbox)
        out = Image.new('RGBA', (final.width + 60, final.height + 60), (0, 0, 0, 0))
        out.paste(final, (30, 30), final)
    else:
        out = img
    out.save(os.path.join(ASSETS_DIR, 'hero-visual.webp'), 'WEBP', quality=92)
    print(f'Hero image saved: {out.size[0]}x{out.size[1]}')


def generate_flow_image():
    """3-step flow visualization: Read → Connect → Answer."""
    W, H = 1000, 340
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    card_w, card_h = 250, 250
    gap = 55
    total = card_w * 3 + gap * 2
    sx = (W - total) // 2
    font = get_font(17)

    labels = ["読める", "つながる", "答えられる"]

    for idx in range(3):
        cx = sx + idx * (card_w + gap)
        cy = 20

        # Card shadow
        shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        rounded_rect(sd, (cx + 3, cy + 4, cx + card_w + 3, cy + card_h + 4), 14,
                     fill=(0, 0, 0, 25))
        shadow = shadow.filter(ImageFilter.GaussianBlur(8))
        img = Image.alpha_composite(img, shadow)
        draw = ImageDraw.Draw(img)

        # Card
        rounded_rect(draw, (cx, cy, cx + card_w, cy + card_h), 14,
                     fill=WHITE + (245,))

        # Top accent
        accent = GOLD if idx == 2 else NAVY
        draw.rectangle([cx + card_w // 2 - 24, cy + 10, cx + card_w // 2 + 24, cy + 13],
                       fill=accent + (140,))

        if idx == 0:
            # Scattered document lines
            positions = [
                (25, 40, 110), (80, 58, 90), (35, 78, 130), (90, 98, 70),
                (30, 120, 100), (100, 138, 80), (40, 158, 120), (70, 178, 90)
            ]
            for px, py, pw in positions:
                draw.rectangle([cx + px, cy + py, cx + px + pw, cy + py + 8],
                              fill=(210, 208, 200, 180))
                draw.rectangle([cx + px, cy + py + 12, cx + px + pw - 20, cy + py + 17],
                              fill=(225, 223, 218, 140))

        elif idx == 1:
            # Connected network
            nodes = [
                (card_w // 2, 60), (80, 100), (card_w - 80, 100),
                (60, 160), (card_w // 2, 150), (card_w - 60, 160)
            ]
            # Draw connections
            connections = [(0,1), (0,2), (1,3), (1,4), (2,4), (2,5), (3,4), (4,5)]
            for a, b in connections:
                x1, y1 = nodes[a]
                x2, y2 = nodes[b]
                draw.line([(cx + x1, cy + y1), (cx + x2, cy + y2)],
                         fill=NAVY + (50,), width=2)
            for nx, ny in nodes:
                draw.ellipse([cx + nx - 10, cy + ny - 10, cx + nx + 10, cy + ny + 10],
                            fill=NAVY + (80,))
                draw.ellipse([cx + nx - 5, cy + ny - 5, cx + nx + 5, cy + ny + 5],
                            fill=WHITE + (220,))
            # Center node gold
            cnx, cny = nodes[4]
            draw.ellipse([cx + cnx - 10, cy + cny - 10, cx + cnx + 10, cy + cny + 10],
                        fill=GOLD + (120,))
            draw.ellipse([cx + cnx - 5, cy + cny - 5, cx + cnx + 5, cy + cny + 5],
                        fill=WHITE + (220,))

        else:
            # Clean organized result
            # Search bar
            rounded_rect(draw, (cx + 24, cy + 40, cx + card_w - 24, cy + 68), 6,
                        fill=(245, 243, 238, 255), outline=(220, 218, 212), width=1)
            draw.rectangle([cx + 36, cy + 50, cx + 100, cy + 58], fill=NAVY + (40,))
            # Search icon
            draw.ellipse([cx + card_w - 58, cy + 46, cx + card_w - 44, cy + 60],
                        outline=NAVY + (80,), width=2)

            # Results
            for ri, ry in enumerate([(84, 130), (144, 186)]):
                y0, y1 = ry
                is_main = (ri == 0)
                bg = (250, 246, 235, 255) if is_main else (250, 249, 247, 255)
                rounded_rect(draw, (cx + 24, cy + y0, cx + card_w - 24, cy + y1), 8, fill=bg)
                if is_main:
                    draw.rectangle([cx + 24, cy + y0 + 4, cx + 27, cy + y1 - 4],
                                  fill=GOLD + (180,))
                draw.rectangle([cx + 38, cy + y0 + 12, cx + 38 + (140 if is_main else 120), cy + y0 + 22],
                              fill=NAVY + (100,) if is_main else (190, 188, 182, 140))
                draw.rectangle([cx + 38, cy + y0 + 28, cx + 38 + (110 if is_main else 90), cy + y0 + 35],
                              fill=(210, 208, 202, 130))

        # Label
        bbox_t = draw.textbbox((0, 0), labels[idx], font=font)
        tw = bbox_t[2] - bbox_t[0]
        draw.text((cx + (card_w - tw) // 2, cy + card_h - 32), labels[idx],
                 fill=NAVY + (200,), font=font)

        # Arrow between cards
        if idx < 2:
            ax = cx + card_w + 8
            ay = cy + card_h // 2
            for i in range(0, gap - 20, 8):
                draw.ellipse([ax + i, ay - 2, ax + i + 4, ay + 2], fill=GOLD + (140,))
            draw.polygon([(ax + gap - 16, ay), (ax + gap - 26, ay - 8), (ax + gap - 26, ay + 8)],
                        fill=GOLD + (180,))

    img.save(os.path.join(ASSETS_DIR, 'flow-visual.webp'), 'WEBP', quality=92)
    print(f'Flow image saved: {W}x{H}')


if __name__ == '__main__':
    os.makedirs(ASSETS_DIR, exist_ok=True)
    generate_hero_image()
    generate_flow_image()
    print('\nLP images generated successfully.')
