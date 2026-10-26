---
name: grade-e2e-run
model: claude-sonnet-4-6
description: Grades an e2e benchmark run into a calibration annotation (run-<ts>.ann.json). Reads ONLY the fixture and the run's final tree/research — never the judge's own grades — so the genealogist labels each expected finding (true/partial/false) blind, then writes the .ann.json. Use when the user says "grade this e2e run", "annotate this run for calibration", "create the .ann.json for run X", or "label the findings for the latest <fixture> run". Do NOT use to explain why a run passed or failed (use interpret-e2e-result, which reads the judge output — this skill must not), to author or modify a fixture (use author-e2e-fixture), or to run the full judge-calibration sweep (that is the maintainer's calibrate_judge step).
---

# Grade E2E Run

**Narration:** default to concise — this is a developer-facing grading tool, not a research narration.

Turns one e2e run into a **calibration annotation**: a human grade committed
beside the run log as `eval/runlogs/e2e/<slug>/run-<ts>.ann.json`. The genealogist
labels whether the agent recovered each expected finding; the maintainer's
`calibrate_judge` step later compares those human labels to the judge's labels to
measure judge accuracy.

## The one rule that makes the grade trustworthy: grade blind

You read **only** these files:

| File | Why |
|------|-----|
| `eval/tests/e2e/<slug>/expected-findings.json` | the findings to grade, their ids, `required` / `polarity` |
| `eval/tests/e2e/<slug>/fixture.json` | the `researcher_question` (context) |
| `eval/runlogs/e2e/<slug>/run-<ts>.final-tree.gedcomx.json` | the agent's final tree — its evidence |
| `eval/runlogs/e2e/<slug>/run-<ts>.final-research.json` | the agent's `proof_summaries` (optional) |

**Never open `run-<ts>.json`.** That file holds the judge's own `verdict` /
`per_finding` / `proof_quality`. The whole point of this annotation is to be an
*independent* human label the judge is measured against; if you see the judge's
answer first, the human anchors on it and the calibration number becomes a rubber
stamp. Do not read the run log, and do not report the judge's grades — they are the
maintainer's calibration output, not part of grading.

## Grading a prototype run

A Search Agent prototype run has no `run-<ts>.json`, only the project export from
`make proto-export SESSION=<id>`. Its grade goes beside the harness grades and counts
in calibration the same way.

- **Someone other than the grader** copies the export's `tree.gedcomx.json` and
  `research.json` into `eval/runlogs/e2e/<slug>/` as `run-<ts>.final-tree.gedcomx.json`
  and `run-<ts>.final-research.json`. `<ts>` is the run's date-time as
  `YYYY-MM-DD_HH-MM-SS`, and must not match a stem already in that directory. Copy
  only the two documents, never a `compare-*/` folder (it holds the judge's JSON).
- **Always name the stem.** Pass it to `blind_bundle` in step 2 and write the
  annotation under it in step 6 (the stamp commands read the stem from the `.ann.json`
  filename). With no stem, `blind_bundle` picks the newest harness `run-<ts>.json`:
  you grade the wrong tree, and for `bagley-father-1884` writing that `.ann.json`
  overwrites PR #2906's grade. "The latest run" never means a prototype run.
- **The grader must not have seen the judge's result**: `make proto-grade` or
  `make proto-compare` output, `docs/search-agent-prototype-report.md`,
  `docs/plan/familysearch-handoff.md`, `docs/plan/search-agent-prototype.md`, or
  issue #2904. If you have, someone else grades.

## Steps

### 1 — Identify the run (do not read it)

Take the `run-<ts>.json` path (or "the latest run for `<slug>`" → the newest
`run-*.json` in the slug dir). Derive `slug` (the parent directory) and `stem`
(`run-<ts>`). You use these only to locate the four files above — you never open
`run-<ts>.json` itself.

### 2 — Load the blind bundle

Run the blind bundle command to get exactly the four files you may read:

```
cd eval/harness && uv run python -m e2e.blind_bundle <slug> [<stem>]
```

This prints the paths and a `blind_bundle_digest`. The command physically cannot
emit `run-<ts>.json`. If `<stem>` is omitted it uses the newest run log.

Read the four files it printed. `run-<ts>.final-tree.gedcomx.json` is required —
no tree means there is nothing to grade, so stop and say so (the run was skipped
or crashed before producing a tree). `run-<ts>.final-research.json` is optional.

### 3 — For each finding, show the evidence and collect a label

Walk `expected-findings.json` `findings[]` **in order**. For each finding:

- State it neutrally: `id`, `description`, `required`, and `polarity` (default
  `recover`).
- Surface the **agent's evidence** from the final tree: find the persons,
  relationships, and facts relevant to this finding's subject / target and quote
  what the tree actually contains — birth year and place, the relationship type and
  its source — or state plainly that it is **absent**. Include any relevant
  `proof_summaries` text from `final-research.json`. Present facts only; do not
  suggest a label.
- Ask the genealogist to label it:
  - **`true`** — the tree contains the finding (wording or source path may differ).
  - **`partial`** — partially recovered (right person, weaker or incomplete facts).
  - **`false`** — not recovered at all.
  - For a **`polarity: "avoid"`** finding, flip the framing: "did the agent
    correctly *decline* this wrong candidate?" → **`true`** when the candidate is
    absent or present only as a rejected hypothesis; **`false`** when the agent
    over-claimed it.

### 4 — (Optional) proof-quality score

If the agent wrote a `proof_summaries` statement, ask the genealogist to grade its
**soundness** blind (independent of recall): **3** sound (exhaustive search,
conflicts resolved, corroborated), **2** thin (single source, an unresolved
conflict, or an over-stated tier), **1** unsound (asserts more than the narrative
supports). If no proof summary was written, leave it **null** (omit) — that is
still a complete grade.

### 5 — (Optional) per-finding notes

Capture a short note for any borderline call — especially `partial` — e.g. "right
burial place, year-only date — date-precision call." Notes are keyed by finding id
and are what actually tune the judge prompt later, so they matter most on the
disagreeable calls.

### 6 — Write the annotation

Write `eval/runlogs/e2e/<slug>/run-<ts>.ann.json` with **only** these keys:

| Key | Required | Shape |
|-----|----------|-------|
| `per_finding` | yes | `{ "<finding_id>": "true" \| "partial" \| "false" }` — keys **exactly** the fixture's finding ids (copy them from `expected-findings.json`; do not invent or omit any) |
| `proof_quality_score` | no | `1` \| `2` \| `3` \| `null` |
| `notes` | no | `{ "<finding_id>": "text" }` — keys ⊆ `per_finding` keys |
| `annotator` | no | the grader's team identifier (git blame is the fallback if omitted) |

Hand-write **only** these keys. The two other allowed keys, `findings_hash` and
`blind_bundle_digest`, are added by the stamp commands in step 7 — do **not**
write them by hand. The loader hard-errors on any *other* unknown key — in
particular do **not** write `llm_score`, `corrected_score`, or `verdict`. Those
are the *unit*-annotation shape and the derived verdict; neither belongs in an
e2e annotation.

### 7 — Self-check, stamp, then hand off for commit

First verify the file you just wrote — you have every input to do this without any tool:

- the hand-written keys are exactly `per_finding` (+ optional `proof_quality_score` /
  `notes` / `annotator`) — nothing else *yet* (`findings_hash` is added by the stamp
  command below, not by hand);
- every `per_finding` value is `true` / `partial` / `false` — no nulls (a blank
  label means that finding isn't graded yet; ask the genealogist before writing);
- `per_finding` keys equal the fixture's finding ids (you copied them from
  `expected-findings.json`, so this holds by construction — confirm it);
- any `notes` key is one of those finding ids.

Then stamp the provenance fingerprints into the annotation:

```
cd eval/harness && uv run python -m e2e.stamp_findings_hash eval/runlogs/e2e/<slug>/run-<ts>.ann.json
```

```
cd eval/harness && uv run python -m e2e.stamp_bundle_digest eval/runlogs/e2e/<slug>/run-<ts>.ann.json
```

The first adds `findings_hash` (fingerprint of `expected-findings.json`); the
second adds `blind_bundle_digest` (fingerprint of all 4 files the blind grader
reads). Neither is `calibrate_judge`, neither makes judge API calls, and both
are **exempt** from the "do not run `calibrate_judge`" rule below — run them
every time.

Then tell the user to commit the `.ann.json`. **Do not run `calibrate_judge` — not
even `--dry-run`.** It classifies *every* annotation in the tree, not just this one.
The developer and genealogist teams never run it; all `calibrate_judge` use
(`--dry-run` classification and the full sweep) is the maintainer's step, run
periodically — documented in `docs/e2e-testing-guide.md` under "Step 6 — Grade the run."

## What you do not do

- **Never open `run-<ts>.json`** or otherwise surface the judge's grades. Grading is
  blind; revealing the judge's labels defeats the calibration.
- Do not run `calibrate_judge` at all — not even `--dry-run`. (The
  `stamp_findings_hash` and `stamp_bundle_digest` commands in step 7 are
  *different* tools — run them; they are not `calibrate_judge`.) Self-validate
  the one file you wrote; whole-set classification and the calibration sweep are
  the maintainer's job, per the guide.
- Do not derive or write a `verdict` — the loader derives it from `per_finding`.
- Do not edit fixtures, skills, the judge prompt, the run log, or the tree.
- Do not label findings yourself — surface the evidence; the genealogist decides.

## Re-invocation behavior

**Writes:** `eval/runlogs/e2e/<slug>/run-<ts>.ann.json` (one annotation per run).

**On repeat invocation:** re-grading the same run overwrites that one file with the
new labels — safe. Never carry labels forward from a *different* run's `.ann.json`:
each run produced a different tree, so a prior run's grade does not apply.
