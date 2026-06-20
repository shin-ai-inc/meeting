#!/usr/bin/env python3
"""Generate ShinAI LP PDF from the 1206x2622 PNG with a clickable CTA link."""

import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
IMG_PATH = os.path.join(PROJECT_DIR, 'public', 'assets', 'shinai-lp-1206x2622.png')
OUTPUT_PATH = os.path.join(PROJECT_DIR, 'public', 'assets', 'shinai-lp.pdf')

IMG_W = 1206
IMG_H = 2622

CONSULT_URL = 'https://meeting-taupe.vercel.app/consult'

# CTA button position (matching the HTML overlay percentages)
CTA_LEFT_PCT = 0.164
CTA_TOP_PCT = 0.9555
CTA_WIDTH_PCT = 0.672
CTA_HEIGHT_PCT = 0.0355

# Add slight padding around button for easier tapping
PAD_X_PCT = 0.01
PAD_Y_PCT = 0.005


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Page size matches the image exactly (in points, 72 dpi)
    page_w = IMG_W
    page_h = IMG_H

    c = canvas.Canvas(OUTPUT_PATH, pagesize=(page_w, page_h))
    c.setTitle('ShinAI｜AIが働ける土台を。')
    c.setAuthor('ShinAI')
    c.setSubject('AIネイティブ基盤づくりと伴走支援のご案内')

    img = ImageReader(IMG_PATH)
    c.drawImage(img, 0, 0, width=page_w, height=page_h, preserveAspectRatio=False)

    # CTA link area (ReportLab uses bottom-left origin)
    link_x = (CTA_LEFT_PCT - PAD_X_PCT) * page_w
    link_w = (CTA_WIDTH_PCT + PAD_X_PCT * 2) * page_w

    # Convert top-origin percentage to bottom-origin
    cta_bottom_pct = 1.0 - CTA_TOP_PCT - CTA_HEIGHT_PCT
    link_y = (cta_bottom_pct - PAD_Y_PCT) * page_h
    link_h = (CTA_HEIGHT_PCT + PAD_Y_PCT * 2) * page_h

    # Transparent clickable rect (no visible border)
    rect = (link_x, link_y, link_x + link_w, link_y + link_h)
    c.linkURL(CONSULT_URL, rect, relative=0, thickness=0)

    c.save()
    print(f'PDF generated: {OUTPUT_PATH}')
    print(f'  Image: {IMG_W}x{IMG_H}px')
    print(f'  CTA link area: ({rect[0]:.0f}, {rect[1]:.0f}) - ({rect[2]:.0f}, {rect[3]:.0f})')
    print(f'  Link URL: {CONSULT_URL}')


if __name__ == '__main__':
    generate()
