---
name: learn-from-failure
description: "Convert failures into reusable artifacts and check repetition. Use when analyzing a failure mode or a recurring failure."
---

# /learn-from-failure — Convert failure to reusable artifact

When a failure occurs, classify it, check for repetition, and produce a durable artifact that prevents recurrence.

## Trigger

`/learn-from-failure` or `/learn-from-failure <failure description>`

Use on: "same issue", "happened again", "recurring", "third time", "keeps happening"

## Flow

### 1. Identify failure
- If argument provided: use it
- If no argument: ask "What failed?"

### 2. Classify failure mode

| Mode | Description | Example |
|------|-------------|---------|
| `routing` | Task sent to wrong agent/model/tool | Opus used for a read-only task |
| `verification` | Output accepted without checking data flow | Video "looked fine" but spec was wrong |
| `tool` | Tool unavailable, broken API, wrong usage | Gmail MCP auth expired |
| `knowledge` | Agent lacked domain knowledge | Didn't know SDK v6 changed type strings |
| `authority` | Agent acted outside delegation zone | the AIgent made a Level 3 decision |

### 3. Check for repetition
Read `$AIGENT_VAULT/memory/FAILURE_MODES.md`. Search for Pattern lines matching the current failure's root cause.

- **0-1 prior occurrences:** Phase 1 — log and monitor
- **2+ occurrences:** Phase 2 — mandatory artifact. A log entry is not enough.
- **3+ occurrences:** The prior artifact failed. Diagnose why and fix or replace it.

### 4. Log to FAILURE_MODES.md
Append a new entry following the existing format:

```markdown
## {YYYY-MM-DD} — {short symptom name}

**Symptom:** {what went wrong, user-visible}
**Verified cause:** {exact mechanism}
**Fix:** {what was done}
**Layer:** {which system layer}
**Pattern:** {one-line category — this is the load-bearing piece for repetition detection}
```

### 5. Determine artifact type

| Failure mode | Artifact | Target |
|---|---|---|
| `routing` | Skill description or hook | the skill's `SKILL.md` description, or `.claude/hooks/` |
| `verification` | Checklist item in doctrine | Relevant doctrine note |
| `tool` | SKILL_GAPS entry + skill spec | `memory/SKILL_GAPS.md` |
| `knowledge` | Vault note or memory candidate | `concepts/` or `memory/` |
| `authority` | Flag to the operator | `aigent_authority_matrix.md` |

### 6. Create artifact
- For routing: add 3+ trigger phrases to the skill's `description` ("Use when ...")
- For verification: append a concrete, runnable check to the relevant doctrine
- For tool: log to SKILL_GAPS.md, suggest /skill-hunt if external capability needed
- For knowledge: write a memory candidate or vault note
- For authority: surface to the operator with recommendation

### 7. Output
```
Failure logged: {classification}
Pattern: {pattern line}
Repeated: {yes/no, count}
Artifact: {type} at {path}
```

## Boundary

Per [[Self-Learning Doctrine]]: a failure logged without an artifact is a false resolution. The ledger grows, the failure recurs, the system learns nothing.

## Bounded procedure experiment (fixture only)

A Finding is an observation, not a verified cause or authority to edit a procedure.
The [fixture mechanics](../../evals/procedure-experiment/README.md) use a declarative grammar and a pinned historical corpus.
Freeze the candidate, evidence, corpus, size budgets and rollback before evaluating.
Require a passing verdict and a caller-supplied approval bound to the candidate and base.
Distinct identity strings are not authenticated review.
This proves mechanics on a fixture, not natural-language procedure compliance or live behavior.

## Related

- [[concepts/Self-Learning Doctrine]] — the doctrine this skill implements
- [[memory/FAILURE_MODES.md]] — the ledger
- [[concepts/Capability Expansion Doctrine]] — tool failures feed the expansion loop
- [[Self-Improving CLAUDE.md]] — the broader self-improvement cycle
