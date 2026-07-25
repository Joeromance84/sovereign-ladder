import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

psp = open(os.path.join(REPO, "assets", "psp-1-protocol-spec.md"), encoding="utf-8").read()
primer = open(os.path.join(REPO, "assets", "three-pillars-ai-primer.md"), encoding="utf-8").read()
index = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()

print("=== PSP-1 INTEGRITY ===")
print("  R1 SAFETY GATE intact :", "R1. SAFETY GATE — If the user indicates" in psp)
rules = [i for i in range(1, 10) if ("R%d. " % i) in psp]
print("  hard rules present    :", rules)
print("  all R1-R9             :", rules == list(range(1, 10)))
print("  R9 seam permission    :", "R9. SEAM PERMISSION" in psp)
print("  loop seam marker      :", "--- SEAM:" in psp)
print("  conformance = 4 checks:", "these four checks" in psp)

print("")
print("=== PRIMER ===")
print("  seam section          :", "THE SEAM — READ THIS BEFORE" in primer)
print("  stopping at 3 complete:", "complete intervention, not an abandoned climb" in primer)
print("  no-plan-while-flooded :", "asking yourself to plan while flooded" in primer)
print("  'you did not fail'    :", "the tool changed modes — you did not fail" in primer)
print("  intro no longer 'must':", "You are not obliged to reach the top" in primer)

print("")
print("=== SITE ===")
print("  seam block            :", 'class="seam"' in index)
print("  placed after rung 3   :",
      index.find('class="seam"') > index.find('data-step="3"')
      and index.find('class="seam"') < index.find('data-step="4"'))
