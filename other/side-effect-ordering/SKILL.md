---
name: side-effect-ordering
description: "Side-effect ordering analyzer: map operation chains in request handlers, LLM judges if ordering is safe or an incident waiting to happen. Read-only. Trigger: /sideorder"
trigger: /sideorder
---
# /sideorder

Systems fail not because individual operations fail but because they happen in the wrong order. This skill finds ordering risks.

## What this is for

- Email sent before DB write confirms (user sees "confirmed" but order failed)
- Cache updated before DB write (stale cache after rollback)
- Irreversible operation before reversible one (charged credit card but order failed)
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/sideorder -help` or `/sideorder -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/sidechain-trace.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

Read each handler's operation chain:

- **Safe**: transactional or order doesn't matter
- **Risky**: later failure leaves inconsistency
- **Dangerous**: data loss on crash mid-chain
- **Inverted**: non-atomic operation order could cause inconsistency

### Step 5 - Write report

File `side-effect-ordering-report.md` in current working directory:

1. **Summary** - handlers by risk level.
2. **Handler table** - most dangerous first. Per handler: file, handler name, operation chain, ordering risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight handlers that would leave inconsistent state on failure.

## Usage

```
/sideorder               # interactive
/sideorder <dir>         # scan project
/sideorder -help
```


