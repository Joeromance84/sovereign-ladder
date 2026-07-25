import re

PATH = r"C:\Users\logan\sovereign-ladder\print-cards.html"

with open(PATH, encoding="utf-8") as fh:
    html = fh.read()

before_svg_imgs = len(re.findall(r'<img src="assets/qr-code\.svg"', html))

# FIX 1: SVG-in-<img> does not survive many print pipelines. PNG does.
# The PNG is 1470x1470; at 1.35in that is ~1089 DPI - far above print needs.
html = html.replace(
    '<img src="assets/qr-code.svg" alt="QR code">',
    '<img src="assets/qr-code.png" alt="QR code">',
)

# FIX 2: the URL was breaking mid-word. Never break a URL someone may type.
html = html.replace(
    "  font-family:var(--mono);font-size:6.4pt;letter-spacing:.02em;\n"
    "  color:var(--pine);margin:0;word-break:break-all;",
    "  font-family:var(--mono);font-size:6pt;letter-spacing:0;\n"
    "  color:var(--pine);margin:0;white-space:nowrap;",
)

with open(PATH, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(html)

print("svg <img> tags before :", before_svg_imgs)
print("svg <img> tags after  :", len(re.findall(r'<img src="assets/qr-code\.svg"', html)))
print("png <img> tags after  :", len(re.findall(r'<img src="assets/qr-code\.png"', html)))
print("word-break remaining  :", "word-break:break-all" in html)
print("nowrap applied        :", "white-space:nowrap" in html)
print("prose SVG advice kept :", "<b>assets/qr-code.svg</b>" in html)
