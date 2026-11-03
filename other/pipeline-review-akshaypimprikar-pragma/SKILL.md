---
name: pipeline-review
description: Audit the agent pipeline itself for drift, staleness, gaps, and inefficiencies, producing a severity-rated report. Runs automatically after every release and on a weekly schedule; can also be invoked manually.
disable-model-invocation: true
---

# Pipeline Review Agent

You are the **Pipeline Review Agent** for an iOS app project. Your job is to audit the agent pipeline for drift, staleness, gaps, and inefficiencies — and produce a severity-rated, actionable report.

## Trigger
Runs automatically after every `/release` and on a weekly schedule. Can also be invoked manually: `/pipeline-review`.

## Process

Run this entire audit in the background. Save findings and send a push notification when done.

## What to audit

### 1. Stale skill references
Check every file in `.claude/skills/` for references to skills that are not in the current registry.

Current valid skills:
`plan`, `spec`, `design`, `review`, `feature`, `test`, `bugfix`, `release`, `gates`, `pipeline-review`, `sync-workflow`, `trim-context`, `simplify`, `security-review`, `code-review:code-review`, `ios-build-verify`, `ios-coverage`, `ios-swiftdata-test-fixture`, `update-config`, `keybindings-help`, `fewer-permission-prompts`, `schedule`, `loop`, `claude-api`, `init`, `claude-code-setup:claude-automation-recommender`, `run`, `verify`, `status`, `benchmark`, `parallel-review`, `pr-followup`, `pragma-review`, `deterministic-pr-gates`

Flag any skill name used in a skill or command file that does not appear on this list. Severity: **Critical**.

### 2. Template drift
If this project was derived from a workflow template (e.g. pragma), compare `.claude/skills/` against the template. Flag:
- App-specific content in the template that should use placeholders — **High**
- Skill files that exist in this project but have no template equivalent — **Medium**
- Logic improvements in this project's skills not yet back-ported to the template — **Low**
- Logic improvements present in the template but not yet pulled into this project's skills — **Medium** (higher than its counterpart above: this direction means the live pipeline is running stale/buggy logic already fixed elsewhere, not just a future scaffold missing an enhancement; `/sync-workflow` only pushes project → template, so this comparison is the only thing that catches it)

### 3. AGENTS.md token budget
Count lines in `AGENTS.md` (or `CLAUDE.md`, for a project still on the pre-AGENTS.md convention). Target: ≤50 lines.
If over budget, list the specific sections that could be trimmed. Severity: **Medium** if 51–60 lines, **High** if >60 lines.

### 4. Memory staleness
Read every file in `~/.claude/projects/<project>/memory/`.
Flag any memory that:
- References a branch, PR, or task that no longer exists in `git log` or `gh pr list`
- Describes a failure mode that has since been fixed in the skill files (the fix is the source of truth)
- Has not been confirmed valid in >60 days and makes a specific factual claim
Severity: **Medium** per stale entry.

### 5. Pipeline gate coverage
Check whether the following gates exist as skill files or documented steps in the pipeline:

| Gate | Required location | Severity if missing |
|---|---|---|
| Pre-PR gate (`/gates`) | `.claude/skills/gates/SKILL.md` | Critical |
| Build verification (separate from tests) | Gate 1 of `/gates` | High |
| CHANGELOG incremental update | Step in `/feature` | High |
| `/test` before `/gates`; `code-review:code-review` before `/review` | `feature/SKILL.md` Done-when + `pr-followup/SKILL.md` + `AGENTS.md`/`CLAUDE.md` | High |
| Lane config and required checks (`gates`, `review-evidence`) | `scripts/pipeline_lanes.json`, `.github/workflows/gates.yml`, `.github/workflows/review-evidence.yml` | Critical |
| Coverage check (`ios-coverage` skill) | `/gates` or post-`/test` step | Medium |
| Security check for sensitive PRs | `security-review` skill reference | Medium |
| Session recovery command (`/status`) | `.claude/skills/status/SKILL.md` | Low |

### 6. Skill file completeness
Each skill or command file must have: **Trigger**, **Process**, **Done when** sections.
Flag any file missing a section. Severity: **Medium**.

### 7. Settings hygiene
Read `.claude/settings.json`. Flag:
- Hooks referencing non-existent files or scripts — **High**
- Missing `UserPromptSubmit` hook for unaddressed pipeline-review alert — **Medium**
- Permissions that are overly broad where tighter patterns would suffice — **Low**

## Output format

Save to `docs/pipeline-review/YYYY-MM-DD.md` with this exact structure:

```markdown
---
date: YYYY-MM-DD
addressed: false
---

# Pipeline Review — YYYY-MM-DD

## Critical
- [ ] <finding> — `<file>:<line>` — **Fix:** <one-line recommended action>

## High
- [ ] <finding> — **Fix:** <recommended action>

## Medium
- [ ] <finding> — **Fix:** <recommended action>

## Low
- [ ] <finding> — **Fix:** <recommended action>

## All clear
- <area>: no issues found
```

Mark items `[x]` as they are resolved. An item deliberately left open — not a live bug, a judgment call to defer — still counts as resolved for this purpose: check it `[x]` and append a `**Deferred <date>** — <reason>` note instead of leaving it `[ ]` forever, which would permanently block `/status`'s next-action check with no way to represent "won't-fix" separately from "not yet done." When every item is either fixed or explicitly deferred this way, update the frontmatter to `addressed: true`.

## Notify when done

After saving the report, use the `PushNotification` tool:
- Title: `Pipeline Review Complete`
- Body: `<N> findings (<X> critical, <Y> high). Open docs/pipeline-review/YYYY-MM-DD.md to review.`

If there are zero findings, body: `Pipeline is healthy — no issues found.`

## Done when
Report saved to `docs/pipeline-review/YYYY-MM-DD.md` and push notification sent.
