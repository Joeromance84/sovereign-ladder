#!/usr/bin/env python3
"""
release_check.py - full pre-release verification across both projects.

Runs every harness, checks both live sites, verifies QR codes decode,
and reports an honest verdict. Names what it does NOT check.

Exit: 0 all clear, 1 findings.
"""

import hashlib
import os
import re
import subprocess
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

LADDER = r"C:\Users\logan\sovereign-ladder"
NOURISH = r"C:\Users\logan\nourishology"
LADDER_URL = "https://joeromance84.github.io/sovereign-ladder/"
NOURISH_URL = "https://joeromance84.github.io/nourishology/"

fails = []


def head(t):
    print("")
    print("=" * 66)
    print(t)
    print("=" * 66)


def ck(label, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  — " + detail) if detail else ""))
    if not ok:
        fails.append(label)
    return ok


def fetch(url, timeout=30):
    return urllib.request.urlopen(url, timeout=timeout).read()


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# ------------------------------------------------------------------ ladder
head("SOVEREIGN LADDER — LOCAL HARNESSES")

rc, out = run([sys.executable, "-X", "utf8", r"tools\corpus_audit.py"], LADDER)
ck("corpus integrity audit", rc == 0,
   "clean" if rc == 0 else out.strip().splitlines()[-6] if out else "see output")

rc, out = run([sys.executable, "-X", "utf8", r"tools\psp1_audit.py",
               r"tools\samples\transcript_urge.txt"], LADDER)
ck("conformance harness self-test — urge transcript", rc == 1 and "VIOLATIONS: 5" in out,
   "detects known R8/S4/R1a violations")

rc, out = run([sys.executable, "-X", "utf8", r"tools\psp1_audit.py",
               r"tools\samples\transcript_vague_opener.txt"], LADDER)
ck("conformance harness self-test — vague opener", rc == 1 and "VIOLATIONS: 3" in out,
   "detects safety question substituted for safety information")

# R1(a) must be unconditional in BOTH AI-facing documents
spec_local = open(os.path.join(LADDER, "assets", "psp-1-protocol-spec.md"),
                  encoding="utf-8").read()
prim_local = open(os.path.join(LADDER, "assets", "three-pillars-ai-primer.md"),
                  encoding="utf-8").read()
ck("PSP-1 standing notice is unconditional", "UNCONDITIONAL, NO TRIGGER" in spec_local)
ck("PSP-1 forbids question-for-information", "NEVER SUBSTITUTE A QUESTION" in spec_local)
ck("PSP-1 defines first reply order", "FIRST REPLY ORDER" in spec_local)
ck("primer carries unconditional disclosure",
   "Every time. No exceptions." in prim_local)
ck("primer forbids question-for-information",
   "Do not substitute a question for it" in prim_local)

head("SOVEREIGN LADDER — CHECKSUM MANIFEST")
manifest = open(os.path.join(LADDER, "CHECKSUMS.md"), encoding="utf-8").read()
stale = []
for line in manifest.splitlines():
    m = re.match(r"^([0-9a-f]{64})  (.+)$", line.strip())
    if not m:
        continue
    digest, rel = m.groups()
    p = os.path.join(LADDER, rel.replace("/", os.sep))
    if not os.path.exists(p):
        stale.append(rel + " (missing)")
        continue
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    if h.hexdigest() != digest:
        stale.append(rel)
ck("all checksums current", not stale, ", ".join(stale) if stale else "verified")

head("SOVEREIGN LADDER — LIVE")
paths = ["", "terms.html", "print-cards.html", "CHECKSUMS.md",
         "assets/three-pillars-ai-primer.md", "assets/psp-1-protocol-spec.md",
         "assets/sovereign-ladder-protocol-v4.pdf",
         "assets/master-geometry-of-addiction-sovereignty.pdf",
         "assets/qr-code.png", "assets/qr-code.svg",
         "sovereign-ladder-cards.pdf", "share/share-square.png"]
for p in paths:
    try:
        b = fetch(LADDER_URL + p)
        ck("200 %s" % (p or "(landing page)"), True, "%d bytes" % len(b))
    except Exception as e:
        ck("200 %s" % (p or "(landing page)"), False, str(e))

live = fetch(LADDER_URL).decode("utf-8", "replace")
lp = fetch(LADDER_URL + "assets/three-pillars-ai-primer.md").decode("utf-8", "replace")
lspec = fetch(LADDER_URL + "assets/psp-1-protocol-spec.md").decode("utf-8", "replace")

head("SOVEREIGN LADDER — SAFETY CONTENT (LIVE)")
ck("crisis line on landing page", "988" in live)
ck("crisis line in primer", "988" in lp)
ck("withdrawal warning on site", "benzodiazepines" in live)
ck("state selector present", live.count('<div class="state">') == 6)
ck("seven rungs present", len(re.findall(r'data-step="\d"', live)) == 7)
ck("seam marked", "calm day, not a hard moment" in live)
ck("terms link present", "terms.html" in live)
ck("no commercial content", not re.search(r"nourish|derma|moistur", live, re.I))

head("SOVEREIGN LADDER — SPEC INTEGRITY (LIVE)")
rules = sorted(int(m) for m in re.findall(r"^R(\d+)\. ", lspec, re.M))
ck("hard rules contiguous R1-R%d" % (max(rules) if rules else 0),
   rules == list(range(1, len(rules) + 1)), str(rules))
ck("R1 safety gate intact", "R1. SAFETY GATE — If the user indicates" in lspec)
ck("R8 human connection intact", "R8. HUMAN CONNECTION" in lspec)
ck("R10 no authenticity assessment", "R10. NO AUTHENTICITY ASSESSMENT" in lspec)
ck("R11 story vs event", "R11. STORY vs EVENT" in lspec)
ck("conformance not overclaiming", "A CLEAN RUN IS NOT A CERTIFICATE" in lspec)
ck("evidentiary status stated", "is UNTESTED" in lspec)

head("QR CODES DECODE")
try:
    import cv2
    import numpy as np
    from PIL import Image
    import io as _io

    for name, url, target in (
        ("ladder PNG", LADDER_URL + "assets/qr-code.png", LADDER_URL),
        ("nourishology PNG", NOURISH_URL + "assets/qr-code.png", NOURISH_URL),
    ):
        raw = fetch(url)
        img = np.array(Image.open(_io.BytesIO(raw)).convert("RGB"))[:, :, ::-1]
        d, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
        ck("%s decodes to correct URL" % name, d == target, d or "no decode")
except ImportError:
    print("  [SKIP] opencv not installed — scan with a phone instead")

head("NOURISHOLOGY — LIVE")
for p in ["", "assets/qr-code.png", "assets/qr-code.svg"]:
    try:
        b = fetch(NOURISH_URL + p)
        ck("200 %s" % (p or "(page)"), True, "%d bytes" % len(b))
    except Exception as e:
        ck("200 %s" % (p or "(page)"), False, str(e))

nl = fetch(NOURISH_URL).decode("utf-8", "replace")
head("NOURISHOLOGY — CLAIM SAFETY (LIVE)")
ck("no fabricated founder", "Claire" not in nl)
ck("no chemist claim", "chemist" not in nl.lower())
ck("no nurse claim", "nurse" not in nl.lower())
ck("no price listed", "$48" not in nl)
ck("states not for sale", "isn't a business yet" in nl)
ck("FDA disclaimer present", "Not evaluated by the Food and Drug Administration" in nl)
ck("patch test guidance", "Patch test first" in nl)
ck("contamination warning", "grow bacteria" in nl)
ck("adverse-event contact", "report a reaction" in nl)
ck("no drug claims", not re.search(
    r"anti-inflammatory|stabilizes the derma|treats|cures|heals", nl, re.I))

# ------------------------------------------------------------------ verdict
head("VERDICT")
if fails:
    print("  %d CHECK(S) FAILED:" % len(fails))
    for f in fails:
        print("    - %s" % f)
else:
    print("  ALL MECHANICAL CHECKS PASS")

print("")
print("NOT CHECKED BY THIS HARNESS — these need a person:")
print("  - Whether a printed QR card scans in real light with a real phone")
print("  - Whether the Nourishology formula is safe (no formulator has reviewed it)")
print("  - Whether the physical labels match the formula in the jar")
print("  - Whether PSP-1's R1/R5/R6/R7/S1/S6 hold in any real conversation")
print("  - Whether the framework helps anyone (untested; no outcome data)")
print("")
print("A green run means nothing mechanical tripped. It is not a certificate.")

sys.exit(1 if fails else 0)
