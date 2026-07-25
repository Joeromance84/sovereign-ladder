# The Sovereign Ladder

A free, open framework for understanding and changing recurring compulsive patterns —
substances, behaviours, relationships, digital consumption.

**Live page:** https://joeromance84.github.io/sovereign-ladder/

Four documents, no signup, no tracking, no account. Copy it, print it, translate it,
hand it to someone.

---

## What's in here

| File | What it is |
|---|---|
| `assets/three-pillars-ai-primer.md` | The whole framework in plain language. Built to be pasted into any AI assistant. **Start here.** |
| `assets/sovereign-ladder-protocol-v4.pdf` | The full adaptive system: intake, gap analysis, five pathway types, USS scoring, safety overrides, client worksheet. |
| `assets/master-geometry-of-addiction-sovereignty.pdf` | The theory — the missing-mechanism principle and the three diagnostic dimensions. |
| `assets/psp-1-protocol-spec.md` | Machine-readable spec. Eight hard rules, six-step loop, conformance test. |
| `index.html` | The landing page. Single file, no build step, no dependencies. |
| `tools/make_qr.py` | Regenerates the QR code for any URL. |

---

## Updating a document

Replace the file in `assets/` under the same filename, commit, push. The live page
serves the new version within a minute. **Printed QR codes keep working** — they point
at the page, not at any individual file.

If you change a *filename*, update the matching `href` in `index.html` in the same
commit, or that download button will 404.

## Regenerating the QR code

```
pip install "qrcode[pil]"
python tools/make_qr.py https://joeromance84.github.io/sovereign-ladder/
```

A custom domain is the one change that breaks printed codes. Decide on the domain
before the first print run.

---

## Note on scope

This is a self-understanding tool, not treatment. It does not diagnose and does not
replace therapy, medical care, or detox. Rung 0 is safety, and it always comes first.
The landing page carries this notice above the fold; please keep it there in any fork
or translation.

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Logan Royce Lorentz.
Copy, print, translate, remix, build on it. Keep the attribution.
