import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for name in ("index.html", "terms.html", "print-cards.html"):
    path = os.path.join(REPO, name)
    if not os.path.exists(path):
        continue
    h = open(path, encoding="utf-8").read()

    refs = sorted(set(re.findall(r'(?:href|src)="((?!http|#|mailto)[^"]+)"', h)))
    missing = [r for r in refs if not os.path.exists(os.path.join(REPO, r.replace("/", os.sep)))]

    print(name)
    print("  sections balanced :", h.count("<section") == h.count("</section>"))
    print("  divs balanced     :", h.count("<div") == h.count("</div>"))
    print("  terminated        :", h.rstrip().endswith("</html>"))
    print("  broken refs       :", missing if missing else "none")
    print("  size              :", len(h), "bytes")
    print("")
