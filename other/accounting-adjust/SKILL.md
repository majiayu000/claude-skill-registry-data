---
name: accounting-adjust
description: Record period-end adjusting entries — accruals, deferrals, depreciation, bad-debt and other estimates — with the calculation and rationale for each and the impact on net income. Use when the user has an unadjusted trial balance and needs revenue and expenses moved into the right period before statements. Not for booking the period's regular transactions; see /accounting-journal.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: accounting
  phase: 5
  artifact: 05-adjust.md
---

# Adjust

Record adjusting entries for "$ARGUMENTS". Ensure revenue and expenses are recognized in the correct period by recording accruals, deferrals, depreciation, and estimates.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"accounting-adjust","workflow":"accounting","phase":5,"project":"<project>","event":"skipped","artifact":"05-adjust.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 5 (Adjust) of the Accounting Cycle workflow (`accounting`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `accounting` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"accounting-adjust","workflow":"accounting","phase":5,"project":"<project>","event":"refused","artifact":"05-adjust.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"accounting-adjust","workflow":"accounting","phase":5,"project":"<project>","event":"started","artifact":"05-adjust.md","note":""}`.

Read `.singularskills/accounting/<project>/04-trial-balance.md` for the unadjusted trial balance.

## Process

1. **Identify required adjustments:**
   - **Accrued revenues** — revenue earned but not yet billed or received
   - **Accrued expenses** — expenses incurred but not yet paid (wages, interest, taxes)
   - **Prepaid expenses** — payments made in advance that need to be expensed over time
   - **Unearned revenue** — cash received in advance that needs to be recognized as earned
   - **Depreciation** — allocate the cost of long-lived assets over their useful lives
   - **Allowances & estimates** — bad debt allowance, warranty reserves, inventory write-downs

2. **Create adjusting journal entries:**
   - For each adjustment, record:
     - **Type** — accrual, deferral, depreciation, or estimate
     - **Accounts** — debit and credit accounts
     - **Amount** — calculated adjustment amount with supporting calculation
     - **Rationale** — why this adjustment is necessary
   - Number entries sequentially (AJE-001, AJE-002, etc.)

3. **Validate adjustments:**
   - Each adjusting entry must have equal debits and credits
   - Verify that no operating transactions are included (those belong in Phase 2)
   - Confirm depreciation methods and useful lives are consistent with policy

4. **Write the artifact** to `.singularskills/accounting/<project>/05-adjust.md` with sections:
   - **Adjusting Journal Entries** — all entries with type, accounts, amounts, and rationale
   - **Adjustment Summary** — total adjustments by type
   - **Impact Analysis** — how adjustments affect net income and key account balances

## Output

The adjustments written to `.singularskills/accounting/<project>/05-adjust.md`. Present a summary highlighting:
- Number of adjusting entries by type
- Net impact on net income
- Largest adjustments by dollar amount

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"accounting-adjust","workflow":"accounting","phase":5,"project":"<project>","event":"finished","artifact":"05-adjust.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: accounting-adjust
workflow: accounting
phase: 5
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```

End the artifact with this paragraph, verbatim:

> **Not financial or tax advice.** This artifact is generated analysis for review by a qualified accountant or financial professional before any filing, reporting or decision relies on it.
