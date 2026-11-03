---
name: accounting-close
description: Close revenue, expense and dividend accounts to retained earnings and prepare the post-closing trial balance that opens the next period. Use when the user has the period's financial statements done and wants the temporary accounts zeroed and balances rolled forward. Not for starting a period's close from source documents; see /accounting-analyze.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: accounting
  phase: 8
  artifact: 08-close.md
---

# Close

Close temporary accounts for "$ARGUMENTS". Zero out revenue, expense, and dividend accounts by transferring their balances to retained earnings.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"accounting-close","workflow":"accounting","phase":8,"project":"<project>","event":"skipped","artifact":"08-close.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 8 (Close) of the Accounting Cycle workflow (`accounting`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `accounting` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"accounting-close","workflow":"accounting","phase":8,"project":"<project>","event":"refused","artifact":"08-close.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"accounting-close","workflow":"accounting","phase":8,"project":"<project>","event":"started","artifact":"08-close.md","note":""}`.

Read `.singularskills/accounting/<project>/07-statements.md` for the financial statements and `.singularskills/accounting/<project>/06-adjusted-balance.md` for the adjusted trial balance.

## Process

1. **Close revenue accounts:**
   - Debit each revenue account for its full balance
   - Credit Income Summary for the total revenue
   - All revenue accounts should now have zero balances

2. **Close expense accounts:**
   - Credit each expense account for its full balance
   - Debit Income Summary for the total expenses
   - All expense accounts should now have zero balances

3. **Close Income Summary:**
   - If Income Summary has a credit balance (net income): debit Income Summary, credit Retained Earnings
   - If Income Summary has a debit balance (net loss): credit Income Summary, debit Retained Earnings
   - Income Summary should now have a zero balance

4. **Close dividends/draws:**
   - Credit Dividends (or Owner's Draws) for its full balance
   - Debit Retained Earnings
   - Dividends account should now have a zero balance

5. **Prepare post-closing trial balance:**
   - List only permanent accounts (assets, liabilities, equity)
   - Verify debits equal credits
   - These balances become the opening balances for the next period

6. **Write the artifact** to `.singularskills/accounting/<project>/08-close.md` with sections:
   - **Closing Journal Entries** — all closing entries with accounts and amounts
   - **Post-Closing Trial Balance** — permanent accounts only
   - **Period Summary** — net income transferred, dividends closed, ending retained earnings

## Output

The closing entries written to `.singularskills/accounting/<project>/08-close.md`. Present a summary highlighting:
- Net income transferred to retained earnings
- Ending retained earnings balance
- Confirmation that all temporary accounts are zeroed

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"accounting-close","workflow":"accounting","phase":8,"project":"<project>","event":"finished","artifact":"08-close.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: accounting-close
workflow: accounting
phase: 8
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
