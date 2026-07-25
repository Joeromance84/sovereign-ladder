#!/usr/bin/env python3
"""
make_qr.py - generate the QR code for the live landing page.

Usage:
    python make_qr.py                          # uses DEFAULT_URL below
    python make_qr.py https://your.url/here    # or pass any URL

Writes:
    assets/qr-code.png   high-resolution raster, for print and for the page
    assets/qr-code.svg   vector, scales to any size without softening

Requires:
    pip install "qrcode[pil]"

Error correction is set to H (~30% recoverable), so the code still scans
after photocopying, folding, or a coffee ring.
"""

import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.svg import SvgPathImage

DEFAULT_URL = "https://joeromance84.github.io/sovereign-ladder/"

FILL = "black"
BACK = "white"

BOX_SIZE = 30
BORDER = 4  # quiet zone, in modules. 4 is the spec minimum. Do not reduce it.


def build(url: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=BOX_SIZE,
        border=BORDER,
    )
    qr.add_data(url)
    qr.make(fit=True)

    png_path = out_dir / "qr-code.png"
    qr.make_image(fill_color=FILL, back_color=BACK).save(png_path)

    svg_qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=BOX_SIZE, border=BORDER)
    svg_qr.add_data(url)
    svg_qr.make(fit=True)
    svg_path = out_dir / "qr-code.svg"
    svg_qr.make_image(image_factory=SvgPathImage).save(svg_path)

    size_px = (qr.modules_count + BORDER * 2) * BOX_SIZE
    print("URL     " + url)
    print("PNG     " + str(png_path) + "  (" + str(size_px) + "x" + str(size_px) + "px)")
    print("SVG     " + str(svg_path))
    print("")
    print("Scan it with a phone before you print it. Always.")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    build(target, Path(__file__).resolve().parent.parent / "assets")
