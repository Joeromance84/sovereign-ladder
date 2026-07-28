import io
import re

h = io.open(r"C:\Users\logan\sovereign-ladder\index.html", encoding="utf-8").read()

# order of major landmarks
marks = [
    ("hero", r'<header class="hero">'),
    ("safety block", r'<section class="safety">'),
    ("state selector", r'id="start"'),
    ("documents", r'id="documents"'),
    ("how to use", r'id="how"'),
    ("ladder", r'id="ladder"'),
]
print("=== ORDER ON PAGE ===")
for name, pat in marks:
    m = re.search(pat, h)
    print("  %-16s char %6d" % (name, m.start() if m else -1))

body = h[h.find("<body>"):]
print("")
print("=== HERO AS WRITTEN ===")
hero = re.search(r'<header class="hero">(.*?)</header>', h, re.S)
print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", hero.group(1))).strip()[:600] if hero else "n/a")

print("")
print("=== SAFETY BLOCK AS WRITTEN ===")
saf = re.search(r'<section class="safety">(.*?)</section>', h, re.S)
print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", saf.group(1))).strip() if saf else "n/a")

print("")
print("=== VISUAL WEIGHT ===")
print("  safety heading style :", "font-size:11px" in h[h.find(".safety h2"):h.find(".safety h2")+200])
print("  safety is <h2>       :", "<h2>Read this first</h2>" in h)
print("  hero eyebrow text    :", re.search(r'<p class="eyebrow">([^<]+)', h).group(1))
