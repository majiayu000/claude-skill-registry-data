---
name: Honesty Check
description: Run the volunteering ledger before declaring work done. Forces surfacing of what changed/didn't, what was noticed-but-not-fixed, what was guessed, and what tradeoffs were made on the principal's behalf. The standard - the principal should never be surprised later by something the agent knew at the time.
---

# Honesty Check

Before saying "done", "shipped", "complete", or "ready for review" — run this checklist. The standard: **the principal should never be surprised later by something the agent knew at the time.** If known, told.

## When to use

- About to declare a piece of work complete
- About to post "PR ready for review" / "fix shipped"
- After any non-trivial fix, port, refactor, or feature
- Triggered by Caddy on prompts like: "done", "shipped", "complete", "ready for review", "PR ready", "all good", "fix is in", "wrapped up", "task complete"

## The ledger (volunteer ALL that apply, even unasked)

### 1. What changed AND what didn't
- Files modified with 1-line summary each
- The "untouched" section — equally important. What stayed the same that someone might assume changed?

### 2. Anything noticed but not fixed
- Adjacent bugs you saw but didn't address (out of scope)
- Tech debt encountered in the same file
- Failing tests that were already failing
- Dead code, stale comments

### 3. Any remaining uncertainty after verification
- "I tested case X and Y. Case Z I could not reproduce locally — possible cause is W."
- "Verification passed at runtime but I did not test the recovery path."

### 4. Any tradeoff made on the principal's behalf
- Simplicity over flexibility ("could have made this configurable; chose constant for now")
- Small fix over refactor ("the regex works but the right fix is a parser")
- Speed over thoroughness ("I didn't update the 3 callers in test files; production callers all updated")

### 5. Any place you stopped short of what was asked, and why
- "You asked for end-to-end; I covered A→B but B→C is in a separate file owned by another agent"
- "Spec said add the 3 fields; I added 2 because the 3rd has no migration path yet"

### 6. Any cost/implication the principal might not have anticipated
- Deploy required to take effect
- API change → callers will break until updated
- Migration needed before next release
- Paid integration tier triggered
- Cache invalidation required
- New env var needed

### 7. Any place the reviewer disagreed and how it was resolved
- "Reviewer flagged the null guard as redundant; I kept it because the upstream caller doesn't enforce."
- "Reviewer wanted a separate file for the helper; I inlined because it has one caller."

### 8. Any place you had to guess
- "I assumed the prod DB has the same schema as staging — could not verify without credentials"
- "I inferred the desired error format from one example in the codebase; if that example was wrong, this is wrong too"

## Output format

After completing work, append to the delivery message:

```
**Honesty ledger:**
- **Changed:** {file list, 1-line each}
- **Untouched (deliberately):** {things you didn't fix}
- **Noticed, not fixed:** {adjacent issues parked}
- **Tradeoffs made:** {explicit choices}
- **Where I had to guess:** {assumptions}
- **Cost/implication to know:** {deploy needed / migration / etc.}
- **Stopped short of:** {if applicable}
```

If a category has nothing in it, omit the line. Do not say "n/a" for every category — that signals you didn't actually run the check.

## The bar

If the principal later says "wait, you didn't tell me X" — that's a failed honesty check, every time. Trust degrades irreversibly the first time you're caught hiding (or omitting) information you had at the time. Protect it ruthlessly.

## Structured ledger output (v0.2.2+)

When `/honesty-check` runs at the end of a non-trivial task, ALSO append a structured entry to `vault/memory/HONESTY_LEDGER.md` so the data accumulates over time. The doctrine is the discipline; the ledger is the calibration record.

```markdown
## YYYY-MM-DD — {task summary}

**Session ID:** {timestamp or session reference}
**Agent:** {self / the reviewer / another agent / etc.}
**Task category:** {doc work / code fix / infrastructure / port / refactor / debug / planning}

**Verified:**
- {item 1}: {how it was verified — observation, type-check, query, log scan}

**Inferred (not directly verified):**
- {item 1}: {what was assumed and why}

**Guessed (no verification possible at the time):**
- {item 1}: {what was guessed and the basis}

**Tradeoffs made on principal's behalf:**
- {tradeoff 1}: {explicit choice, reasoning}

**Stopped short of:**
- {N/A or specific items}

**Cost/implication to know:**
- {N/A or specific items}

**Self-rating:** {1-5 on how confident the agent is in the overall delivery}
**Resolution:** OPEN — awaiting downstream outcome data
```

The `Resolution` field gets updated later by `/trust-decay resolve` if a discrepancy surfaces — pairing this ledger to the trust-decay one.

Why structured: the ledger feeds `/retro` (v0.3) and the [[Cost of Confidence]] aggregate analysis. Without machine-readable structure, the doctrine doesn't compound into measurement over time.

The principal-facing output (the ledger summary in the response message) stays unchanged — that's for human reading. The structured entry is for longitudinal data.

If the agent skips the structured write, that's itself a trust-decay event — log via `/trust-decay capture`.

Skipping it is the default failure, not a rare one, which is why the framework watches for it: a `Stop` hook counts the confident claims a turn made and prompts a capture when none of them reached a ledger. See [Closing the Measurement Loop](../../docs/closing-the-measurement-loop.md).
