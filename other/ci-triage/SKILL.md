---
name: ci-triage
description: "Diagnoses failing GitHub Actions checks on a PR or branch: lists the failures, ranks falsifiable hypotheses, confirms the root cause with log evidence, then applies and verifies the smallest authorized fix. Use when CI is red, a check or workflow run fails, or the user asks why a build, lint or test job failed."
allowed-tools: Bash(gh pr *), Bash(gh run *), Bash(git branch *), Bash(git log *)
---

## CI Triage

**Step 1 — List failures**
Run `gh pr checks` on the current PR and list every failing check by name. For a push-triggered run with no PR, use `gh run list --branch <branch> --limit 5` instead.

**Step 2 — Hypotheses first, before any investigation**
For each failing check, enumerate your top 3 hypotheses with the single fastest command to falsify each (usually starting with `gh run view <id> --log-failed`). Present this list to the user. Do not start running commands or reading files yet.

**Step 3 — Investigate**
Test each hypothesis from cheapest to most expensive; read-only investigation needs no additional confirmation. Stop and report findings after each hypothesis before moving to the next.

**Step 4 — Confirm root cause**
State the confirmed root cause clearly. Do not guess or propose a fix until you have evidence.

**Step 5 — Apply the authorized fix**
For a fix request, make the smallest supported change within the task. For a review-only request, report the proposed fix without editing. Ask only at the root AGENTS.md boundaries; existing authorization counts.

**Step 6 — Verification command**
After the fix is applied, run and report the exact command that confirms it resolves the failure before pushing — the same command CI runs (from the workflow YAML), not an approximation.

---

Current PR info (Claude Code fills these in; in Codex, run the commands):
- Branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
