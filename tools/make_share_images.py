"""
make_share_images.py - shareable QR cards for messaging and social media.

Design note: every image carries the URL in readable text alongside the code.
A bare QR cannot be scanned on the phone that is displaying it, is invisible
to screen readers, and reads as phishing. The visible URL fixes all three.

Output (in share/):
    share-square.png   1080x1080  - Instagram, Facebook, chat, general
    share-story.png    1080x1920  - Stories, TikTok, Snapchat
    share-wide.png     1200x630   - link previews, X, LinkedIn

Requires: pip install "qrcode[pil]"
"""

import os
import sys

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "share")

URL = "https://joeromance84.github.io/sovereign-ladder/"
URL_DISPLAY = "joeromance84.github.io/sovereign-ladder"

PAPER = (237, 239, 234)
INK = (22, 32, 43)
STEEL = (90, 107, 118)
PINE = (47, 93, 80)
WHITE = (255, 255, 255)

HEAD = ["You are not fighting", "willpower. You are", "running a pattern."]
TAIL = "Free  ·  No signup  ·  No tracking"

FONTS = {
    "serif": ["georgia.ttf", "Georgia.ttf", "times.ttf", "DejaVuSerif.ttf"],
    "serif_i": ["georgiai.ttf", "timesi.ttf", "DejaVuSerif-Italic.ttf"],
    "mono": ["consola.ttf", "Consolas.ttf", "cour.ttf", "DejaVuSansMono.ttf"],
    "sans": ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"],
}
FONT_DIRS = [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu", "/Library/Fonts"]


def load(kind, size):
    for name in FONTS[kind]:
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()


def qr_image(px):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=2)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((px, px), Image.NEAREST)


def centered(d, y, text, font, fill, W):
    w = d.textbbox((0, 0), text, font=font)[2]
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def build(W, H, qr_px, head_pt, url_pt, tail_pt, gap, path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_head = load("serif", head_pt)
    f_url = load("mono", url_pt)
    f_tail = load("sans", tail_pt)

    line_h = int(head_pt * 1.14)
    block_h = line_h * len(HEAD) + gap + (qr_px + 48) + gap + int(url_pt * 2.6)
    y = (H - block_h) // 2

    for line in HEAD:
        centered(d, y, line, f_head, INK, W)
        y += line_h

    y += gap

    pad = 24
    qx = (W - qr_px) // 2
    d.rectangle([qx - pad, y - pad, qx + qr_px + pad, y + qr_px + pad], fill=WHITE)
    img.paste(qr_image(qr_px), (qx, y))
    y += qr_px + pad + gap

    centered(d, y, URL_DISPLAY, f_url, PINE, W)
    y += int(url_pt * 1.9)
    centered(d, y, TAIL, f_tail, STEEL, W)

    img.save(path, "PNG", optimize=True)
    return path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    made = [
        build(1080, 1080, 470, 62, 30, 26, 46, os.path.join(OUT_DIR, "share-square.png")),
        build(1080, 1920, 560, 72, 34, 30, 78, os.path.join(OUT_DIR, "share-story.png")),
        build(1200, 630, 300, 48, 24, 20, 30, os.path.join(OUT_DIR, "share-wide.png")),
    ]
    for p in made:
        im = Image.open(p)
        print("WROTE  %-42s %s" % (os.path.basename(p), "x".join(map(str, im.size))))
    print("")
    print("Target URL:", URL)


if __name__ == "__main__":
    main()
