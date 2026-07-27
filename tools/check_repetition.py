import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*p):
    return open(os.path.join(REPO, *p), encoding="utf-8").read()


psp = read("assets", "psp-1-protocol-spec.md")
primer = read("assets", "three-pillars-ai-primer.md")

print("=== REPETITION SHIPPED ===")
print("  primer section          :", "WHY ONCE IS NOT ENOUGH" in primer)
print("  automaticity is the goal:", "stop having to remember it" in primer)
print("  effortful != failure    :", "not a sign that it isn't working" in primer)
print("  evidence paragraph      :", "Repetition and automaticity." in primer)
print("  instruction 4 updated   :", "the mechanism is automaticity, not insight" in primer)
print("  PSP-1 R4 repetition     :", "REPETITION: prefer an action" in psp)

print("")
print("=== HARMS EXCLUDED ===")
print("  no prescribed count     :", "NEVER PRESCRIBE A COUNT" in psp)
print("  no streaks/resets       :", "No streaks, no resets" in psp)
print("  missing a day is fine   :", "Missing a day does not reset anything" in primer)
print("  no rung gating          :", "NEVER GATE A RUNG ON REPETITION" in psp)
print("  range stated, not point :", "18 days to over 250" in primer)

print("")
print("=== NOT REGRESSED ===")
rules = [i for i in range(1, 12) if re.search(r"^R%d\. " % i, psp, re.M)]
print("  hard rules R1-R10       :", rules == list(range(1, 11)))
print("  R1 safety gate intact   :", "R1. SAFETY GATE — If the user indicates" in psp)
print("  R9 seam intact          :", "R9. SEAM PERMISSION" in psp)
print("  R10 authenticity intact :", "R10. NO AUTHENTICITY ASSESSMENT" in psp)
print("  R4 still has 10-min floor:", "within ~10 minutes" in psp)
