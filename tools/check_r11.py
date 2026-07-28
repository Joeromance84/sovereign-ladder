import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Users\logan\sovereign-ladder"


def rd(*p):
    return io.open(os.path.join(R, *p), encoding="utf-8").read()


psp = rd("assets", "psp-1-protocol-spec.md")
pri = rd("assets", "three-pillars-ai-primer.md")
idx = rd("index.html")

print("=== R11 SHIPPED ===")
print("  psp: R11 present      :", "R11. STORY vs EVENT" in psp)
print("  psp: story in step 2  :", "STORY (what they made it mean)" in psp)
print("  psp: conformance R1-R11:", "R1–R11" in psp)
print("  primer: story section :", "THE STORY IS ITS OWN DATA" in pri)
print("  primer: log has story :", "and **the story**" in pri)
print("  primer: evidence added:", "cognitive restructuring" in pri)
print("  site: state 01 updated:", "what you told yourself it meant" in idx)

print("")
print("=== NO DIAGNOSIS ===")
print("  psp bans clinical name:", "NEVER name or imply a clinical condition" in psp)
print("  psp bans arguing belief:", "NEVER argue the belief is false" in psp)
print("  psp: reflect as question:", "AS AN OPEN QUESTION" in psp)
print("  psp: escalate not label:", "ESCALATE, DO NOT DIAGNOSE" in psp)
print("  primer: not a diagnosis:", "it is not the same as a clinical assessment" in pri)
print("  primer: escalation note:", "past what a self-help framework should be handling" in pri)

print("")
print("=== NOT REGRESSED ===")
rules = [i for i in range(1, 13) if re.search(r"^R%d\. " % i, psp, re.M)]
print("  hard rules R1-R11     :", rules == list(range(1, 12)))
print("  R1 safety gate intact :", "R1. SAFETY GATE — If the user indicates" in psp)
print("  R10 intact            :", "R10. NO AUTHENTICITY ASSESSMENT" in psp)
print("  micro-action list = 4 :", pri.count("- **The ") == 4)
print("  sections balanced     :", idx.count("<section") == idx.count("</section>"))
print("  divs balanced         :", idx.count("<div") == idx.count("</div>"))
