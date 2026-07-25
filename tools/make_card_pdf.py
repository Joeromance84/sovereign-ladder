"""
make_card_pdf.py - build a print-ready PDF of business cards.

Why this exists: browser printing dropped the QR image silently. A PDF
generated here has the code embedded in the file itself, so what you see
is what prints. This is also the file a print shop wants.

Output: sovereign-ladder-cards.pdf  (US Letter, 8 cards, 3.5in x 2in)

Requires: pip install reportlab
"""

import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR = os.path.join(REPO, "assets", "qr-code.png")
OUT = os.path.join(REPO, "sovereign-ladder-cards.pdf")

CARD_W, CARD_H = 3.5 * inch, 2.0 * inch
MARGIN_X, MARGIN_Y = 0.5 * inch, 0.5 * inch
GAP_X, GAP_Y = 0.5 * inch, 0.16 * inch
COLS, ROWS = 2, 4

INK = (0.086, 0.126, 0.169)
STEEL = (0.353, 0.420, 0.463)
PINE = (0.184, 0.365, 0.314)
GUIDE = (0.85, 0.87, 0.85)

HEAD = ["You are not fighting", "willpower. You are", "running a pattern."]
SUB = [
    "Patterns can be understood.",
    "What can be understood can",
    "be changed. Free - no signup,",
    "no tracking.",
]
URL = "joeromance84.github.io/sovereign-ladder"


def draw_card(c, x, y):
    c.setStrokeColorRGB(*GUIDE)
    c.setDash(3, 3)
    c.setLineWidth(0.5)
    c.rect(x, y, CARD_W, CARD_H)
    c.setDash()

    pad = 0.17 * inch
    qr_size = 1.32 * inch
    qr_x = x + pad
    qr_y = y + (CARD_H - qr_size) / 2.0
    c.drawImage(ImageReader(QR), qr_x, qr_y, qr_size, qr_size,
                preserveAspectRatio=True, mask="auto")

    tx = qr_x + qr_size + 0.15 * inch
    top = y + CARD_H - pad - 0.10 * inch

    c.setFillColorRGB(*INK)
    c.setFont("Times-Roman", 12.5)
    for i, line in enumerate(HEAD):
        c.drawString(tx, top - i * 14.5, line)

    c.setFillColorRGB(*STEEL)
    c.setFont("Helvetica", 6.6)
    sub_top = top - len(HEAD) * 14.5 - 6
    for i, line in enumerate(SUB):
        c.drawString(tx, sub_top - i * 8.4, line)

    c.setFillColorRGB(*PINE)
    c.setFont("Courier", 5.7)
    c.drawString(tx, y + pad - 0.02 * inch, URL)


def main():
    if not os.path.exists(QR):
        print("MISSING QR:", QR)
        sys.exit(1)

    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Sovereign Ladder - cards")

    page_w, page_h = letter
    for r in range(ROWS):
        for col in range(COLS):
            x = MARGIN_X + col * (CARD_W + GAP_X)
            y = page_h - MARGIN_Y - (r + 1) * CARD_H - r * GAP_Y
            draw_card(c, x, y)

    c.showPage()
    c.save()
    print("WROTE:", OUT)
    print("Cards:", COLS * ROWS, "| size: 3.5in x 2.0in | page: US Letter")


if __name__ == "__main__":
    main()
