import re
import subprocess

REPO = r"C:\Users\logan\sovereign-ladder"
r = subprocess.run(["git", "-C", REPO, "show", "adb8350", "--", "index.html"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
added = [l[1:] for l in r.stdout.splitlines()
         if l.startswith("+") and not l.startswith("+++")]
print("=== LINES ADDED BY adb8350 ===")
for l in added:
    print(l)

print()
print("=== PLAIN TEXT ===")
txt = re.sub(r"<[^>]+>", " ", "\n".join(added))
print(re.sub(r"\s+", " ", txt).strip())

print()
print("=== IS IT IN THE OTHER DOCUMENTS? ===")
for f in ("assets/three-pillars-ai-primer.md", "assets/psp-1-protocol-spec.md"):
    body = open(REPO + "\\" + f.replace("/", "\\"), encoding="utf-8").read()
    print("  %-40s 'Pattern Direction': %s" % (f, "Pattern Direction" in body))
