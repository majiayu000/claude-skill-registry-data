---
name: repo-health
description: Periodic AI-readiness report — 9-asset action checklist, audit drift, and suggest-only reviewer-feedback phrases mined from the last N merged PRs.
type: skill
license: MIT
compatibility:
  - claude-code
user-invocable: false
---

# Repo health

## Overview

One report from three scripts — `repo-health-score.sh` (nine assets, `pass`/`partial`/`fail`/`na` plus `action_needed`; no medal or aggregate; assets 5–6 read `na` outside the MTK checkout; rubric in `.claude/references/repo-health-assets.md`), `audit-drift-check.sh`, and `pr-review-mine.sh` (imperative reviewer phrases recurring across ≥2 merged PRs, tagged `[MINED:feedback]`, suggest-only; heuristics and denylist in `.claude/references/pr-mining-patterns.md`).
Writes `.claude/repo-health-latest.md` (always) and `.claude/repo-health-latest.json` (with `--json`); both are gitignored.

## When To Use

- "Is this repo AI-ready?", "repo health", "what should we improve?", "mine our PRs", "what do reviewers keep asking for?"
- Periodically, before a major release, or after `/mtk-setup --audit`.

### When NOT To Use

- MTK usage numbers → `mtk-doctor --usage`.
- Inside the build loop, or on a repo with fewer than 3 merged PRs (mining has no signal; run with `--no-mining`).

## Workflow

1. **Flags.** `--prs N` (1..50, default 10), `--json`, `--no-mining`.

2. **Checklist.** `bash scripts/repo-health-score.sh` (add `--json` for the JSON file). The nine assets are canonical; never add, drop or re-grade one at runtime — a change goes through the reference and the script.

3. **Audit drift** (best-effort, never blocks):

   ```bash
   CONST_DOC=AGENTS.md; [ -f "$CONST_DOC" ] || CONST_DOC=CLAUDE.md
   for doc in "$CONST_DOC" .claude/references/architecture-principles.md .claude/references/conventions.md; do
     [ -f "$doc" ] || continue
     bash scripts/audit-drift-check.sh "$doc" || true   # exit 1 = drift
   done
   ```

   Drift annotates asset 2 as `🟨 audit drift: N citations`; it never changes the status. Unstamped docs are skipped silently.

4. **Mining** (unless `--no-mining`): `bash scripts/pr-review-mine.sh --prs <N>`. Fail-soft: without an authenticated `gh` it prints `Skipped: <reason>` and exits 0 — report that line, never phrases from memory. A phrase needs ≥2 distinct PRs; one reviewer repeating it in one PR is not a team norm. Boilerplate that slips through ("great work") goes on the `## Denylist` of `pr-mining-patterns.md`, then re-run; the denylist is never bypassed for one run.

5. **Top 3 actions.** Candidates: every `action_needed` asset and every mined phrase cited by ≥3 PRs. Rank AI Context > Onboarding > Toolkit > mined phrase. One sentence each, naming the file or command.

6. **Write the report** to `.claude/repo-health-latest.md`: checklist, drift table, mining section, `## Top 3 actionable changes`. With `--json`, also `.claude/repo-health-latest.json` as `{ "scorecard": {...}, "mining": {...}, "top3": [...] }`. Write the file even when the engineer asks for chat only; echo the path, the `Needs action` line and the top 3.

7. **Publish** per `.claude/references/artifact-publishing.md` after the file is on disk (silent no-op when the tool is unavailable or `MTK_ARTIFACT_PUBLISH=0`).

**Never edit `architecture-principles.md` from this skill.** A mined phrase becomes a principle only when the engineer promotes it, one phrase at a time, with the `[MINED:feedback]` tag and its PR numbers, after seeing the diff.

## Verification

- `.claude/repo-health-latest.md` exists with a `Needs action:` line, the nine-asset table and a "Top 3 actionable changes" section.
- `bash scripts/repo-health-score.sh --json | jq '.action_needed'` is an array; the output carries no medal or score.
- The mining section cites PR numbers (`#<n>`) for every phrase, or reads `Skipped: <reason>`.
- `architecture-principles.md` is unchanged.
