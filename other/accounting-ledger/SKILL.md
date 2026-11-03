---
name: accounting-ledger
description: Post journal entries to the general ledger by account, with running balances, closing balances and a journal-to-ledger cross-reference. Use when the user has a period's journal entries and wants them posted to ledger accounts or needs each account's balance. Not for writing the journal entries themselves; see /accounting-journal.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: accounting
  phase: 3
  artifact: 03-ledger.md
---

# Ledger

Post journal entries to the general ledger for "$ARGUMENTS". Organize all debits and credits by account and calculate running balances.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"accounting-ledger","workflow":"accounting","phase":3,"project":"<project>","event":"skipped","artifact":"03-ledger.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Ledger) of the Accounting Cycle workflow (`accounting`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `accounting` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"accounting-ledger","workflow":"accounting","phase":3,"project":"<project>","event":"refused","artifact":"03-ledger.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"accounting-ledger","workflow":"accounting","phase":3,"project":"<project>","event":"started","artifact":"03-ledger.md","note":""}`.

Read `.singularskills/accounting/<project>/02-journal.md` for the journal entries.

## Process

1. **Set up ledger accounts:**
   - Create a T-account or tabular format for each account in the chart of accounts
   - Include the account number, name, and normal balance side (debit or credit)
   - Carry forward any opening balances from the prior period

2. **Post journal entries:**
   - Transfer each journal entry to the appropriate ledger accounts
   - Record the date, journal entry reference (JE-001, etc.), and amount
   - Post debits to the debit side and credits to the credit side
   - Calculate the running balance after each posting

3. **Verify completeness:**
   - Cross-reference every journal entry to confirm it has been posted
   - Check that no entries were double-posted or missed
   - Ensure running balances are mathematically correct

4. **Write the artifact** to `.singularskills/accounting/<project>/03-ledger.md` with sections:
   - **General Ledger** — each account with all postings and running balance
   - **Account Summary** — closing balance for each account
   - **Cross-Reference** — journal entry to ledger posting map

## Output

The ledger written to `.singularskills/accounting/<project>/03-ledger.md`. Present a summary highlighting:
- Number of active accounts
- Top accounts by transaction volume
- Closing balances for key accounts

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"accounting-ledger","workflow":"accounting","phase":3,"project":"<project>","event":"finished","artifact":"03-ledger.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: accounting-ledger
workflow: accounting
phase: 3
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
