---
name: sr-validate
description: >
  Phase 7 of the SRS workflow. Runs srs_validator.py --dir on the generated
  SRS files, reports errors and warnings, auto-fixes ERRORs, and outputs
  a COMPLIANT / PARTIALLY COMPLIANT / NON-COMPLIANT verdict.
---

# sr-validate

Goal: validate the generated SRS against IEEE 830-1998.
Fix all ERRORs before reporting. WARNings are captured for the improvement report.

---

## Step 0 — Identify Project

Ask the user: "Which project to validate? (slug)"

Check that `projects/{slug}/srs/` exists and contains .md files.
If missing: tell user to run `$sr-generate` first.

---

## Step 1 — Run Validator

Execute:
```bash
python .codex/scripts/srs_validator.py --dir projects/{slug}/srs/
```

Capture stdout. Display the full validation table.

---

## Step 2 — Fix ERRORs Immediately

For each ERROR finding:
1. Identify the affected SRS section file
2. Fix the issue following IEEE 830 rules:
   - `missing-section`: add the section with correct heading format
   - `fr-no-shall`: rewrite the Requirement line with explicit "shall" clause
   - `fr-numbering-gap`: renumber FRs to fill gaps (update all references)
3. State what was fixed: `FIXED [ERROR] fr-no-shall in FR-07 → added "shall" clause`

After fixing all ERRORs: re-run validator and confirm no new ERRORs.

---

## Step 3 — Collect WARNings

List all WARN findings but do NOT fix them here — they go into the improvement report.

Format:
```
WARN: unresolved-tag — 3 [TBD] tags remain (NFR-03, NFR-07, §1.3)
WARN: fr-incomplete-gwt — FR-12: missing "Then:" field
WARN: nfr-no-numeric — NFR-05 Response Measure has no numeric threshold
```

---

## Step 4 — Verdict

Output:
```
## Validation Result

Verdict: COMPLIANT | PARTIALLY COMPLIANT | NON-COMPLIANT
File:    projects/{slug}/srs/ ({N} files)

ERRORs fixed:  {count}
WARNings open: {count} → captured in $sr-improve report

Next: $sr-improve → improvement report + warning resolution guide
```
