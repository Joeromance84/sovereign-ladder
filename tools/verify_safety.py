import re
import time
import urllib.request

U = "https://joeromance84.github.io/sovereign-ladder/"

for i in range(20):
    try:
        c = urllib.request.urlopen(U, timeout=20).read().decode("utf-8", "replace")
        if "Rung 0 — safety comes first" in c:
            break
    except Exception:
        pass
    time.sleep(15)

c = urllib.request.urlopen(U, timeout=25).read().decode("utf-8", "replace")

print("=== SAFETY BLOCK, LIVE ===")
m = re.search(r'<section class="safety">(.*?)</section>', c, re.S)
txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()
print(txt)

print("")
print("=== CHECKS ===")
print("  heading is Rung 0     :", "Rung 0 — safety comes first" in c)
print("  person before scope   :", txt.index("988") < txt.index("not treatment"))
print("  crisis 988            :", "988" in c)
print("  SAMHSA                :", "1-800-662-4357" in c)
print("  findahelpline         :", "findahelpline.com" in c)
print("  withdrawal warning    :", "benzodiazepines" in c)
print("  no-urgency line       :", "still be here when you are steady" in c)
print("  safety before selector:", c.index('class="safety"') < c.index('id="start"'))
print("  heading uses serif    :", ".safety h2{\n  font-family:var(--serif)" in c)
