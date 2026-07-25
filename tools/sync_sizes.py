import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Keep the download-size labels on index.html honest after document edits.
pairs = [
    ("assets/three-pillars-ai-primer.md", "MD"),
    ("assets/sovereign-ladder-protocol-v4.pdf", "PDF"),
    ("assets/master-geometry-of-addiction-sovereignty.pdf", "PDF"),
    ("assets/psp-1-protocol-spec.md", "MD"),
]

index_path = os.path.join(REPO, "index.html")
html = open(index_path, encoding="utf-8").read()

for rel, kind in pairs:
    path = os.path.join(REPO, rel.replace("/", os.sep))
    kb = max(1, round(os.path.getsize(path) / 1024))
    total = 0
    # secondary cards: <span class="meta">MD · 8 KB</span>
    pattern = (
        r'(href="' + re.escape(rel) + r'" download>Download &darr; '
        r'<span class="meta">' + kind + r' · )\d+( KB</span>)'
    )
    html, n = re.subn(pattern, r"\g<1>" + str(kb) + r"\g<2>", html)
    total += n
    # primary card: <span style="opacity:.7">MD · 14 KB</span>
    pattern2 = (
        r'(href="' + re.escape(rel) + r'" download>Download &darr; '
        r'<span style="opacity:\.7">' + kind + r' · )\d+( KB</span>)'
    )
    html, n2 = re.subn(pattern2, r"\g<1>" + str(kb) + r"\g<2>", html)
    total += n2
    status = "OK" if total else "NO LABEL FOUND"
    print("%-52s -> %3d KB  (%d updated, %s)" % (rel, kb, total, status))

open(index_path, "w", encoding="utf-8", newline="\n").write(html)
print("")
print("index.html rewritten")
