---
name: fp-drift
description: >-
  Phase 5 of the feature-pipeline suite. Use this after /fp-iterate prints the
  M4 stop hook confirming CI is green. Fetches origin/main, runs gaia dev diff
  to surface any skill-registry changes the PR introduced that are unrelated to
  its stated purpose (accidental drift), then prints the final pipeline summary
  including a CI churn report (via /ci-churn). Also invoke standalone whenever
  you want to audit whether a branch has unexpected registry drift — e.g. before
  merging any review/meta or cli/ branch, or when a reviewer asks "did this PR
  touch anything it shouldn't?". Triggers: "check for drift", "drift check",
  "final summary", "pipeline done", "wrap up the pipeline", "fp-drift", "Phase 5".
version: 3.1.0
---

# fp-drift  (Phase 5 — Drift Check & Final Summary)

Verify no unintended registry changes leaked into the branch, then close the
pipeline with a human-readable summary that includes a CI churn report.
Runs in the main turn — no sub-agent.

## Setup

Read pipeline state:

```bash
STATE=".agents/skills/feature-pipeline/scripts/state.sh"
feature=$($STATE get feature)
branch=$($STATE get branch)
pr=$($STATE get prNumber)
prUrl=$($STATE get prUrl)
issues=$($STATE get issueNumbers)
ciStatus=$($STATE get ciStatus)
```

If `ciStatus` is not `"green"`, stop here — the drift check is only meaningful
once CI has passed, because a failing run may have left the branch in a
partially applied state:

```
⚠ CI is not confirmed green. Run /fp-iterate first, then re-run /fp-drift.
```

## Drift check

Fetch the latest main so the diff is against the true merge base, not a stale
local ref:

```bash
git fetch origin main
gaia dev diff 2>/dev/null || gaia dev validate
```

`gaia dev diff` compares registry nodes on this branch against `origin/main`.
Any field change, added node, or removed node will appear here. The question
to answer: are ALL changes attributable to the stated purpose of this PR?

**If unexpected drift is detected** (skills or fields changed that have no
connection to `{{feature}}`):

Print a warning table so the user can make an informed call — do not silently
discard or auto-revert the drift:

```
⚠ Skill drift detected — please confirm these changes are intentional:

| Skill ID | Field | Value on main | Value on branch |
|----------|-------|---------------|-----------------|
| …        | …     | …             | …               |
```

End your turn and wait. The user may say "intentional", may ask you to revert,
or may open a follow-up PR. Never decide for them.

**If no unexpected drift (or all drift is confirmed intentional):**

Collect the commit list for the summary:

```bash
git log origin/main..HEAD --oneline
```

## CI Churn Report

Before printing the final summary, run the `/ci-churn` script to measure how
many commits and CI-compute seconds were burned on avoidable push rounds.
See `.claude/skills/ci-churn/SKILL.md` for full documentation.

```bash
python3 scripts/ci_churn.py "$pr" 2>/dev/null
```

If `$pr` is unavailable from state, pass the PR number directly.  
If the script is unavailable (not yet in repo), skip gracefully with a note.

Capture the output and embed it verbatim in the final summary under a
`CI Churn` section. Do **not** interpret or editorialize the numbers —
just include the raw report so the human can read it directly.

Print the final summary and close the pipeline state:

```
✅ Feature Pipeline Complete
════════════════════════════════════════════════════════

Feature explored : {{feature}}
Issues filed     : <count>  (links: <#N> <#M> …)
PR               : <prUrl>
CI               : All checks green ✅
Skill drift      : None detected ✅

Commits
───────
<sha7> <message>
…

What was fixed
──────────────
• <issue title>
…

CI Churn
────────
<output of python3 scripts/ci_churn.py $pr>
```

```bash
$STATE set phase 7
$STATE set ciStatus "done"
```

```
── Pipeline complete ──────────────────────────────────────────────────────────
```
