import hashlib
import os
from datetime import date

REPO = r"C:\Users\logan\sovereign-ladder"
FILES = [
    "index.html",
    "terms.html",
    "assets/three-pillars-ai-primer.md",
    "assets/psp-1-protocol-spec.md",
    "assets/sovereign-ladder-protocol-v4.pdf",
    "assets/master-geometry-of-addiction-sovereignty.pdf",
    "assets/qr-code.png",
    "assets/qr-code.svg",
]

lines = [
    "# Checksum manifest",
    "",
    "SHA-256 for every published file. Use this to confirm a copy you were",
    "given is unaltered.",
    "",
    "Canonical source: https://joeromance84.github.io/sovereign-ladder/",
    "Generated: " + date.today().isoformat(),
    "",
    "Verify on Windows:    certutil -hashfile <file> SHA256",
    "Verify on macOS:      shasum -a 256 <file>",
    "Verify on Linux:      sha256sum <file>",
    "",
    "```",
]

for rel in FILES:
    path = os.path.join(REPO, rel.replace("/", os.sep))
    if not os.path.exists(path):
        print("MISSING:", rel)
        continue
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    digest = h.hexdigest()
    lines.append("%s  %s" % (digest, rel))
    print("%s  %s" % (digest[:16] + "...", rel))

lines.append("```")
lines.append("")

out = os.path.join(REPO, "CHECKSUMS.md")
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines))

print("")
print("WROTE:", out)
