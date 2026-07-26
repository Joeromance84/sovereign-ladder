import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://joeromance84.github.io/sovereign-ladder/"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

html = urllib.request.urlopen(BASE, timeout=30).read().decode("utf-8")

print("=== DOWNLOAD LINKS ON THE LIVE PAGE ===")
links = re.findall(r'href="(assets/[^"]+)"\s+download', html)
for i, l in enumerate(links, 1):
    where = "PRIMARY card" if html.find(l) < html.find('class="deeper"') else "grid below"
    print("  %d. %-52s [%s]" % (i, l, where))
print("  total download links:", len(links))

print("")
print("=== EACH FILE, FETCHED LIVE ===")
for l in links:
    try:
        r = urllib.request.urlopen(BASE + l, timeout=30)
        print("  [%d] %-52s %6d bytes" % (r.status, l, len(r.read())))
    except Exception as e:
        print("  [FAIL] %s -> %s" % (l, e))

print("")
print("=== DOCUMENTS IN THE REPO ===")
adir = os.path.join(REPO, "assets")
docs = [f for f in sorted(os.listdir(adir)) if f.endswith((".md", ".pdf"))]
for f in docs:
    print("  %-52s %6d bytes" % (f, os.path.getsize(os.path.join(adir, f))))
print("  total documents:", len(docs))
