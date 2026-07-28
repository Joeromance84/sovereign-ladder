#!/usr/bin/env python3
"""
corpus_audit.py - integrity harness for the Sovereign Ladder corpus.

Finds inconsistencies BETWEEN documents. Reports two classes:

  MECHANICAL  - objectively wrong, safe to fix without judgment
                (broken cross-reference, stale size label, numbering gap)
  JUDGMENT    - possible contradiction, needs a human decision
                (two documents saying different things about the same rule)

It does NOT fix anything. It proposes; you dispose.

Exit: 0 clean, 1 findings, 2 bad input.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(*p):
    return open(os.path.join(ROOT, *p), encoding="utf-8").read()


findings = []


def add(kind, where, what, detail=""):
    findings.append({"kind": kind, "where": where, "what": what, "detail": detail})


psp = rd("assets", "psp-1-protocol-spec.md")
primer = rd("assets", "three-pillars-ai-primer.md")
index = rd("index.html")
terms = rd("terms.html")

# ---- 1. rule numbering is contiguous ------------------------------------
rules = sorted(int(m) for m in re.findall(r"^R(\d+)\. ", psp, re.M))
if rules != list(range(1, len(rules) + 1)):
    add("MECHANICAL", "psp-1", "rule numbering not contiguous", str(rules))

styles = sorted(int(m) for m in re.findall(r"^S(\d+)\. ", psp, re.M))
if styles != list(range(1, len(styles) + 1)):
    add("MECHANICAL", "psp-1", "style directive numbering not contiguous", str(styles))

# ---- 2. every cross-referenced rule exists ------------------------------
refs = set(int(m) for m in re.findall(r"\bR(\d+)\b", psp))
missing = sorted(r for r in refs if r not in rules)
if missing:
    add("MECHANICAL", "psp-1", "cross-reference to non-existent rule",
        "R" + ", R".join(str(m) for m in missing))

# ---- 3. CONFORMANCE range matches actual max ----------------------------
m = re.search(r"hard rules R1[–-]R(\d+)", psp)
if m and int(m.group(1)) != max(rules):
    add("MECHANICAL", "psp-1",
        "CONFORMANCE cites R1-R%s but spec defines R1-R%d" % (m.group(1), max(rules)))

# ---- 4. audit harness claims match reality ------------------------------
claimed = set(re.findall(r"mechanically for ((?:R\d+, |S\d+, |and )+[RS]\d+)", psp))
if claimed:
    listed = set(re.findall(r"[RS]\d+", list(claimed)[0]))
    try:
        harness = rd("tools", "psp1_audit.py")
        implemented = set(re.findall(r'\("(R\d+|S\d+)"', harness))
        implemented |= set(re.findall(r'"rule": "(R\d+|S\d+)"', harness))
        overclaim = listed - implemented
        if overclaim:
            add("MECHANICAL", "psp-1",
                "CONFORMANCE claims harness checks rules it does not implement",
                ", ".join(sorted(overclaim)))
    except FileNotFoundError:
        add("MECHANICAL", "psp-1", "CONFORMANCE references a harness that is missing")

# ---- 5. seven rungs present everywhere ----------------------------------
site_states = len(re.findall(r'<div class="state">', index))
site_steps = len(re.findall(r'data-step="\d"', index))
if site_steps != 7:
    add("MECHANICAL", "index.html", "expected 7 ladder rungs, found %d" % site_steps)
if site_states != 6:
    add("MECHANICAL", "index.html", "expected 6 state-selector entries, found %d" % site_states)

# ---- 6. crisis info in every reader-facing surface -----------------------
for name, doc in (("index.html", index), ("terms.html", terms),
                  ("primer", primer)):
    if "988" not in doc:
        add("MECHANICAL", name, "crisis line 988 absent from reader-facing document")

# ---- 7. download size labels match real files ---------------------------
for rel, kind in (("assets/three-pillars-ai-primer.md", "MD"),
                  ("assets/psp-1-protocol-spec.md", "MD"),
                  ("assets/sovereign-ladder-protocol-v4.pdf", "PDF"),
                  ("assets/master-geometry-of-addiction-sovereignty.pdf", "PDF")):
    real = max(1, round(os.path.getsize(os.path.join(ROOT, rel.replace("/", os.sep))) / 1024))
    lab = re.search(re.escape(rel) + r'"[^>]*>[^<]*<span[^>]*>' + kind + r' · (\d+) KB', index)
    if not lab:
        add("MECHANICAL", "index.html", "no size label found for %s" % rel)
    elif int(lab.group(1)) != real:
        add("MECHANICAL", "index.html",
            "stale size label for %s" % rel,
            "shows %s KB, file is %d KB" % (lab.group(1), real))

# ---- 8. checksum manifest current ---------------------------------------
try:
    import hashlib
    manifest = rd("CHECKSUMS.md")
    for line in manifest.splitlines():
        mm = re.match(r"^([0-9a-f]{64})  (.+)$", line.strip())
        if not mm:
            continue
        digest, rel = mm.groups()
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(path):
            add("MECHANICAL", "CHECKSUMS.md", "manifest lists missing file", rel)
            continue
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        if h.hexdigest() != digest:
            add("MECHANICAL", "CHECKSUMS.md", "stale checksum", rel)
except FileNotFoundError:
    add("MECHANICAL", "CHECKSUMS.md", "manifest missing")

# ---- 9. seam consistency across documents -------------------------------
seam_psp = "SEAM" in psp
seam_primer = "THE SEAM" in primer
seam_site = 'class="seam"' in index
if not (seam_psp and seam_primer and seam_site):
    add("JUDGMENT", "corpus", "seam documented inconsistently",
        "psp=%s primer=%s site=%s" % (seam_psp, seam_primer, seam_site))

# ---- 10. R11 story field consistency ------------------------------------
story_psp = "STORY (what they made it mean)" in psp
story_primer = "and **the story**" in primer
story_site = "what you told yourself it meant" in index
if not (story_psp and story_primer and story_site):
    add("JUDGMENT", "corpus", "story field documented inconsistently",
        "psp=%s primer=%s site=%s" % (story_psp, story_primer, story_site))

# ---- 10b. concept drift: anything on the site must exist in the documents --
CONCEPTS = [
    ("seam / acute vs cold", 'class="seam"', "SEAM", "THE SEAM"),
    ("pattern direction", "id=\"pattern-direction\"", "CHECK DIRECTION FIRST",
     "PATTERN DIRECTION"),
    ("story vs event", "what you told yourself it meant",
     "STORY (what they made it mean)", "THE STORY IS ITS OWN DATA"),
]
for label, site_key, psp_key, primer_key in CONCEPTS:
    on_site = site_key in index
    in_psp = psp_key in psp
    in_primer = primer_key in primer
    if on_site and not (in_psp and in_primer):
        add("MECHANICAL", "corpus",
            "concept drift: '%s' is on the site but missing from documents" % label,
            "site=%s psp-1=%s primer=%s" % (on_site, in_psp, in_primer))

# ---- 11. no commercial content in the free resource ---------------------
for term in ("nourish", "derma", "moistur", "buy now", "purchase"):
    if term in index.lower():
        add("JUDGMENT", "index.html", "commercial term in free resource", term)

# ---- report --------------------------------------------------------------
mech = [f for f in findings if f["kind"] == "MECHANICAL"]
judg = [f for f in findings if f["kind"] == "JUDGMENT"]

print("SOVEREIGN LADDER — CORPUS INTEGRITY AUDIT")
print("=" * 64)
if not findings:
    print("  no findings")
for f in findings:
    print("  [%-10s] %-14s %s" % (f["kind"], f["where"], f["what"]))
    if f["detail"]:
        print("               %s" % f["detail"])
print("-" * 64)
print("MECHANICAL (safe to fix): %d      JUDGMENT (your call): %d" % (len(mech), len(judg)))
print()
print("This harness proposes. It does not apply. Rule content, safety")
print("clauses and wording are never auto-edited.")

sys.exit(1 if findings else 0)
