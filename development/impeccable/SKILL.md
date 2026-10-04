---
name: impeccable
license: MIT
description: 'Final quality pass before shipping: verify it works, remove loose ends, confirm it matches the ask. Use for "make it impeccable", "polish this", "final pass", "ship-ready".'
---

# Impeccable

A disciplined last-mile review that turns "it works on my machine" into "this is ready to ship." Run it as the final step on a change, after the code is written but before you commit or open a PR.

**Not a substitute for `/code-review` (bug hunting) or `/verify` (behavioral checks).** This skill is the closeout: it assumes the logic is roughly right and focuses on completeness, correctness of scope, and polish.

## When To Use

- The user says "make it impeccable", "polish this", "final pass", "clean it up", "ship-ready".
- You're about to commit or open a PR on more than a trivial edit.
- A change touched several files and you want to be sure nothing was left half-done.

Skip it for one-line fixes, doc-only edits, or config tweaks — the overhead isn't worth it.

## The Checklist

Work through these in order. Do not report "impeccable" until every box is genuinely true — if one fails, fix it and re-run the affected check.

### 1. It does exactly what was asked

- Re-read the original request. List each thing it asked for. Confirm each is done — no more, no less.
- No scope creep: no speculative features, no unrequested refactors, no "while I was here" changes.
- No scope gaps: every acceptance criterion the user stated is met.

### 2. It actually works

- Exercise the changed path end-to-end, not just the tests. Drive the real flow and observe the result.
- Run the build and the test suite. Both pass. If either fails, it is not impeccable.
- Check the edge and boundary cases relevant to the change (empty input, error paths, limits).

### 3. No loose ends

- No leftover debugging: stray `console.log` / `print`, commented-out code, `TODO`/`FIXME` you introduced.
- No dead code: unused imports, variables, functions, or files you added and no longer need.
- No placeholder values, mock data, or hardcoded test credentials left in real code paths.
- Temporary/scratch files are removed, not committed.

### 4. It reads like the surrounding code

- Naming, formatting, and idioms match the neighboring code — not your personal style.
- Comment density matches the file. Explain *why*, not *what*; delete comments that restate the code.
- Files stay within the project's size norms (this repo: keep files under 500 lines).

### 5. It's safe

- No secrets, credentials, tokens, or `.env` contents in the diff.
- Input is validated at system boundaries.
- No new logging of sensitive data (PII, keys, full request bodies).

### 6. The commit tells the truth

- Commit message describes what changed and why, in the repo's existing style.
- The diff contains only the intended change — no unrelated files, no accidental reverts.
- Follow this repo's attribution rules: do **not** add a `Co-Authored-By` trailer unless `.claude/settings.json` sets `attribution.commit`.

## Report Honestly

State plainly what you verified and how. If a check was skipped or a test failed, say so with the evidence — never claim "impeccable" over a red build or an unrun path. When every item genuinely passes, say so without hedging.
