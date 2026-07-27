import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()

print("=== STATE SELECTOR ===")
states = re.findall(r'<div class="state">', html)
print("  state rows           :", len(states), "(expect 6)")
print("  panels               :", len(re.findall(r'<div class="panel">', html)))
print("  action blocks        :", len(re.findall(r'<div class="do">', html)))
print("  aria-expanded set    :", len(re.findall(r'aria-expanded="false"', html)))
print("  seam row present     :", 'class="seamrow"' in html)

print("")
print("=== PLACEMENT ===")
i_safety = html.find('class="safety"')
i_start = html.find('id="start"')
i_docs = html.find('id="documents"')
i_ladder = html.find('id="ladder"')
print("  safety before start  :", 0 < i_safety < i_start)
print("  start before docs    :", 0 < i_start < i_docs)
print("  docs before ladder   :", 0 < i_docs < i_ladder)
print("  hero links to #start :", 'href="#start"' in html)

print("")
print("=== SAFETY CONTENT REACHABLE ===")
print("  988 above selector   :", 0 < html.find("988") < i_start)
print("  withdrawal warning   :", "benzodiazepines" in html)
print("  state 00 = grounding :", "Breathe out longer than you breathe in" in html)

print("")
print("=== SEAM CONSISTENCY ===")
print("  stopping at 3 ok     :", "you did the whole job for today" in html)
print("  4-5 marked cold      :", "for a calm day, not a hard moment" in html)
print("  no product content   :", not re.search(r"nourish|skin|derma", html, re.I))

print("")
print("=== STRUCTURE ===")
print("  sections balanced    :", html.count("<section") == html.count("</section>"))
print("  divs balanced        :", html.count("<div") == html.count("</div>"))
print("  buttons balanced     :", html.count("<button") == html.count("</button>"))
print("  terminated           :", html.rstrip().endswith("</html>"))
print("  size                 :", len(html), "bytes")
