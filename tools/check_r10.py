import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*parts):
    return open(os.path.join(REPO, *parts), encoding="utf-8").read()


psp = read("assets", "psp-1-protocol-spec.md")
primer = read("assets", "three-pillars-ai-primer.md")
terms = read("terms.html")

print("=== PSP-1 INTEGRITY ===")
rules = [i for i in range(1, 12) if re.search(r"^R%d\. " % i, psp, re.M)]
print("  hard rules present     :", rules)
print("  R1 SAFETY GATE intact  :", "R1. SAFETY GATE — If the user indicates" in psp)
print("  R10 present            :", "R10. NO AUTHENTICITY ASSESSMENT" in psp)
print("  sole authority clause  :", "SOLE AUTHORITY ON THEIR OWN EXPERIENCE" in psp)
print("  conformance says R1-R10:", "R1–R10" in psp)

print("")
print("=== PRIMER ===")
print("  instruction 8 present  :", "Never assess whether the person is being authentic" in primer)
print("  names who it excludes  :", "autistic" in primer and "dissociated" in primer)
print("  action floor as check  :", "behaviour is observable, interiority is not" in primer)
print("  instruction count      :", len(re.findall(r"^\d+\. ", primer, re.M)))

print("")
print("=== TERMS (reader-facing) ===")
print("  misuse item added      :", "just performance" in terms)
items = terms.count("<li>", terms.find("being <strong>misused</strong>"), terms.find("None of that is this framework"))
print("  misuse list items      :", items)

print("")
print("=== CROSS-DOCUMENT CONSISTENCY ===")
print("  R2/R5 inversions cited :", "banned by R2 and R5" in psp)
print("  no felt-sense probing  :", "Do not probe for felt-sense proof" in psp)
