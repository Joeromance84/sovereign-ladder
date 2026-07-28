# SESSION CONTEXT — read this first

Point Claude at this file at the start of a new thread:

> Read C:\Users\logan\sovereign-ladder\CONTEXT.md before we start.

---

## What this is

**The Sovereign Ladder** — a free, open framework for understanding and changing
recurring compulsive patterns. Live at https://joeromance84.github.io/sovereign-ladder/
Author: Logan Royce Lorentz. CC BY 4.0. No signup, no tracking, no account.

Four documents: the primer (entry point, built to be pasted into any AI), Protocol v4
(full system), Master Geometry (theory), PSP-1 (machine-readable spec).

## Access already configured — do not re-do setup

- `gh` CLI authenticated as Joeromance84, token in Windows keyring
  (`C:\Program Files\GitHub CLI\gh.exe`)
- Repo: `C:\Users\logan\sovereign-ladder` -> github.com/Joeromance84/sovereign-ladder
- Sister repo: `C:\Users\logan\nourishology` -> github.com/Joeromance84/nourishology
- Desktop Commander is the file/process tool throughout

## Run before any change ships

```
python tools\release_check.py      # 48 checks, both projects, live + local
python tools\corpus_audit.py       # cross-document integrity
python tools\psp1_audit.py <file>  # transcript conformance
python tools\make_checksums.py     # regenerate manifest after edits
python tools\sync_sizes.py         # fix download size labels after edits
```

All return honest exit codes and name what they do **not** check. A green run is
not a certificate.

## Design decisions that must not be reversed

These were each reached deliberately. Reopening them is almost always a regression.

1. **No gating.** No rung is locked behind completing another. Stopping at rung 3 is a
   complete intervention (R9, "the seam"). Rungs 0–3 are acute work, 4–6 are cold work.
2. **No authenticity assessment.** Never judge whether a user's reported experience is
   genuine, performed, or earned. Never treat disagreement, calm, fluency, or difficulty
   describing feelings as evidence about their inner state (R10). Unfalsifiable tests are
   the primary control vector against this framework.
3. **No diagnosis.** Interpretation is trackable pattern data, never a clinical label
   (R11). Reflect a user's own absolute words back as an open question; never correct,
   never name a condition, escalate to professionals without labeling.
4. **No reluctance-as-evidence.** Withholding is a boundary, treated as rung 4 work, not
   resistance to overcome (R5).
5. **Never a substitute for human connection** (R8).
6. **Weights are provisional.** The USS weighting was reasoned, not measured. Never
   present composite scores as validated; never prescribe day counts or streaks.
7. **Mathematics is metaphor.** Notation in Master Geometry computes nothing and is
   labeled as such. Do not re-import formalism as if it were operational.
8. **No commercial content.** Nourishology is a separate project with a separate site.
   Nothing links the free resource to a product. `corpus_audit.py` enforces this.
9. **Safety leads.** The landing page opens with crisis resources BEFORE any scope
   disclaimer. Person first, liability second. Do not reorder.

## Known pattern to watch for

Multiple AI-generated proposals during development arrived as flattering "upgrades" that
would have introduced: performance detection, fragility mapping, repetition gates, and a
product funnel aimed at people who had just identified themselves as vulnerable. Each was
rejected. Expect more of the same shape — real insight wrapped around something that
quietly damages the work. Check proposals against the list above before building.

## Open items (as of last session)

- Revoke the GitHub PAT still sitting in plaintext in
  `%APPDATA%\Claude\claude_desktop_config.json` (github MCP server). `gh` makes it
  redundant.
- System clock: timezone is set to "Central America Standard Time"; should be
  "Central Standard Time" for Oklahoma. W32Time service is stopped.
- Scan a physically printed QR card with a phone. Never verified outside software.
- Decide on a domain (e.g. namethepattern.org) BEFORE any print run — changing the
  domain is the one thing that breaks printed codes.
- Optional: move the repo into a GitHub organization so `joeromance84` isn't the public
  face. Do NOT rename the personal account; it would break 21 repos.

## Nourishology — separate project, unresolved

Small-batch moisturizer by Stacia King and Andrea King. Site live, claims cleaned.
**No qualified formulator has reviewed the formula.** Seven revisions produced six
arithmetic errors; label and formula still disagree on four ingredients. A cosmetic
formulation consultant is needed before samples go to anyone. Do not offer formulation
advice as a substitute for that.
