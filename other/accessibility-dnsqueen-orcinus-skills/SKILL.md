---
name: accessibility
description: Audit a web UI for accessibility with the ultra11y engine (RGAA 4.1.2 on a WCAG 2.2 AA core, 102 static checks), fix what it finds, and re-audit. Use before shipping any web UI change and in CI on every UI change. A page that was never audited is not accessible. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires Node.js; the bundled ultra11y engine is self-contained and install-free, with no dependencies beyond Node.
---

# ACCESSIBILITY — can everyone use this page?

An automated check sees only part of accessibility. This skill owns that part with a deterministic engine, and says plainly what the engine cannot see. A page that was never audited is not accessible, and a page whose audit was never read is not fixed.

## Rules

- Audit before shipping any web UI change. A blocking or major finding is a FAIL.
- Every finding names its criterion, its location, and its remediation. A finding without a criterion is an opinion, not a result.
- Never declare conforming what was not verified. The engine's `check` and `verify` gates exist to reject invented non-conformities — and invented conformities.
- Fix, then re-audit. A fix that was not re-audited is a claim, not a fix.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Audit

```bash
python3 skills/accessibility/scripts/check_accessibility.py <page-or-glob> --out <dir>
```

The audit runs through the ORCINUS gate wrapper (`scripts/check_accessibility.py`), which calls the engine (`node skills/accessibility/scripts/ultra11y.mjs audit`, `--fail-on major` by default) after pre-checking every input. A missing input, a glob that matches nothing, or an audit of zero files is INCOMPLETE (exit 2) — the engine on its own warns and exits 0 with zero files audited and 100% conformance, which is never a pass. The engine is self-contained and install-free (Node only, no dependencies). It audits the page against RGAA 4.1.2, the French State's accessibility standard, on a WCAG 2.2 AA core; other country standards are pluggable packs. Read the JSON report it writes: each criterion carries a status (conforming, non-conforming, not applicable, manual), and each finding carries its rule, criterion, file, line, severity, message, and remediation.

### 2. Classify

- **Blocking / major:** must be fixed before shipping. A missing main landmark, an image without an alternative, a form field without a label.
- **Minor:** fix in the same change if it is cheap; otherwise record it in the report with a reason, not silently.
- **Manual:** the engine cannot decide these (for example, whether an image alternative actually describes the image). A human must judge them — the engine saying "manual" is not a pass.

### 3. Fix

Fix one finding at a time, starting with the blocking and major ones. Prefer native HTML first: a real `<button>`, a real `<label>`, a real `<main>`. Do not fix an accessibility finding by adding ARIA where a native element would do — ARIA is a patch, not a design.

### 4. Re-audit and gate

Re-run the audit on the fixed page. In CI, gate on it:

```bash
python3 skills/accessibility/scripts/check_accessibility.py <page-or-glob> --fail-on major
```

The wrapper defaults to `--fail-on major`: it exits 1 when a blocking or major finding exists, and exits 2 (INCOMPLETE) when an input is missing or no file was audited — a missing page is never reported as passed. (The bare engine without `--fail-on` reports findings and still exits 0 — a gate that cannot fail is not a gate — which is why the audit always goes through the wrapper.)

### 5. Verdict

- PASS: no blocking or major findings, and every manual criterion has a recorded human judgment.
- FAIL: any blocking or major finding, or any manual criterion left undecided.

## Report

Return the report in this form:

- The exact engine command, its version, and its exit code.
- Each finding, with criterion, file, line, severity, and remediation.
- Each manual criterion and the human judgment recorded for it.
- The fix applied per finding, and the re-audit result.
- Verdict: PASS or FAIL, and what remains.

## Scope

Static checks only. The engine checks the markup it can see; it does not see rendered behaviour — keyboard traps, focus order in a dynamic flow, or a live region that never announces. Those need a real browser (use `webapp-testing`) and a human with a keyboard and a screen reader. This skill does not claim a page is accessible; it claims the engine's checks passed and the manual criteria were judged.

## Sources

Method, in our own words, using the ultra11y engine (maxgfr/ultra11y, MIT, licence verified from the primary LICENSE file) as-is. No code was copied from ultra11y except the engine script itself, which is bundled verbatim (see `ATTRIBUTION.md` for why the upstream `SKILL.md` was not copied verbatim).
