---
name: pipeline-feature
version: 1.0.0
description: "Full feature development pipeline — plan, execute, critique, review, QA, ship, deploy. Chains autoplan, executing-plans, critique skills, review, qa, ship, and deploy into a single multi-stage workflow with quality gates between stages."
---

# Pipeline: Feature Development

You are orchestrating a full feature development pipeline. Execute each stage sequentially. Do NOT skip stages. If a gate fails, STOP and report which stage failed and why.

## Pipeline State

Create a pipeline tracker at `.gstack/pipeline-feature-{date}.md` at the start. Update it after each stage completes.

```markdown
## Pipeline: Feature Development
Started: {timestamp}
Feature: {description}

| # | Stage | Status | Gate | Duration | Notes |
|---|-------|--------|------|----------|-------|
| 1 | PLAN | pending | — | — | — |
| 2 | EXECUTE | pending | — | — | — |
| 3 | CRITIQUE | pending | — | — | — |
| 4 | REVIEW | pending | — | — | — |
| 5 | QA | pending | — | — | — |
| 6 | SHIP | pending | — | — | — |
| 7 | DEPLOY | pending | — | — | — |
```

---

## Stage 1: PLAN

Invoke `/autoplan` on the feature description.

This runs CEO review, design review (if UI scope), and eng review internally.

**Gate:** User must approve the plan before proceeding. The autoplan skill handles this with its Final Approval Gate. Do NOT proceed to Stage 2 until the user explicitly approves.

**On pass:** Update tracker row 1 → PASS, proceed to Stage 2.
**On fail:** Update tracker row 1 → BLOCKED, report the blocking reason.

---

## Stage 2: EXECUTE

Read the approved plan file. Determine execution method:

- **If the plan has 3+ independent waves:** invoke `/superpowers-subagent-driven-development` (parallel subagent execution)
- **Otherwise:** invoke `/superpowers-executing-plans` (sequential in-session execution)

Both skills handle their own verification checkpoints internally.

**Gate:** All plan tasks must be marked completed. Run the project's test suite (`npm test`, `pytest`, `mix test`, etc.) — all tests must pass.

**On pass:** Update tracker row 2 → PASS, proceed to Stage 3.
**On fail:** If tests fail, fix failures before proceeding. If blocked, update tracker row 2 → BLOCKED.

---

## Stage 3: CRITIQUE (parallel)

Detect which critique skills apply based on changed files:

```bash
git diff main...HEAD --name-only
```

Dispatch applicable critiques as parallel subagents (Agent tool):

| Changed files match | Critique skill | Condition |
|---|---|---|
| `*.py`, `*.js`, `*.ts` (server/API dirs) | `/backend-critique` | Backend/API files changed |
| `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.css` | `/design-critique` | UI/frontend files changed |
| Auth, tokens, secrets, encryption, `.env` | `/security-critique` | Security-sensitive files changed |

If no files match any condition, skip this stage (update tracker → SKIPPED).

**Gate:** ALL critiques must grade **B or above**. If any critique grades C or below:
1. Report the findings to the user
2. Ask: "Fix the issues flagged by {critique-name} before proceeding?"
3. If user says yes → fix the issues, re-run that critique
4. If user says skip → note the override in the tracker and proceed

**On pass:** Update tracker row 3 → PASS (include grades), proceed to Stage 4.

---

## Stage 4: REVIEW

Invoke `/review` on the current branch.

This runs structural analysis, scope drift detection, plan completion audit, test coverage diagram, and adversarial review (Codex + subagent).

**Gate:** No P1 (critical) issues. All AUTO-FIX items applied. ASK items presented to user for decision.

**On pass:** Update tracker row 4 → PASS, proceed to Stage 5.
**On fail:** Fix P1 issues, re-run review. If still failing after 2 attempts → BLOCKED.

---

## Stage 5: QA

Invoke `/qa` with the project's dev server URL.

If no dev server is running, start it first (`npm run dev`, `python manage.py runserver`, etc.) and wait for it to be ready.

The QA skill runs browser testing, finds bugs, fixes them atomically with regression tests, and produces a health score.

**Gate:** Health score >= 70. If score < 70:
1. Report the QA findings
2. The `/qa` skill's internal fix loop should have addressed fixable issues
3. If score is still < 70 after fixes → report to user, ask whether to proceed

**On pass:** Update tracker row 5 → PASS (include health score), proceed to Stage 6.

---

## Stage 6: SHIP

Invoke `/ship`.

This merges base branch, runs tests, generates coverage, bumps version, updates CHANGELOG, creates bisectable commits, pushes, and creates a PR.

**Gate:** PR created successfully. All CI checks pass (or no CI configured).

**On pass:** Update tracker row 6 → PASS (include PR URL), proceed to Stage 7.
**On fail:** Report the failure. Usually a test or merge conflict — fix and retry.

---

## Stage 7: DEPLOY (optional)

Ask the user: "Deploy to production? (railway / vercel / skip)"

If user says skip → update tracker row 7 → SKIPPED, go to Final Report.

If deploying:

### 7a: Baseline capture
```
/canary --baseline {production-url}
/benchmark --baseline {production-url}
```

### 7b: Deploy
Invoke `/railway-deploy` or `/vercel-deploy` based on user's choice.

### 7c: Post-deploy verification (parallel subagents)
```
/canary {production-url} --duration 5m
/benchmark {production-url} --diff
```

**Gate:** Canary verdict is HEALTHY. No benchmark REGRESSION.

**On pass:** Update tracker row 7 → PASS.
**On fail:** Report findings. Canary DEGRADED or benchmark REGRESSION may warrant a rollback — ask the user.

---

## Final Report

After all stages complete (or a stage is BLOCKED), produce the final pipeline report:

```markdown
## Pipeline Report: Feature Development
Feature: {description}
Run: {timestamp}
Duration: {total elapsed}

| # | Stage | Skill(s) | Result | Gate | Duration |
|---|-------|----------|--------|------|----------|
| 1 | PLAN | autoplan | {PASS/BLOCKED/SKIPPED} | {gate result} | {time} |
| 2 | EXECUTE | executing-plans | {result} | {gate result} | {time} |
| 3 | CRITIQUE | {skills used} | {result} ({grades}) | {gate result} | {time} |
| 4 | REVIEW | review | {result} | {gate result} | {time} |
| 5 | QA | qa | {result} | Score: {N}/100 | {time} |
| 6 | SHIP | ship | {result} | {PR URL} | {time} |
| 7 | DEPLOY | {deploy skill} | {result} | {gate result} | {time} |

Overall: {PASS / PASS_WITH_OVERRIDES / BLOCKED}
Artifacts: {list of PR URLs, report paths, deploy URLs}
```

Append the report to the pipeline tracker file. Print it to the user.
