---
name: note
description: Ultra-fast thought capture to the Cognitive Ledger. One command, no ceremony. Tags route the entry to the right bucket.
version: 1.0.0
execution-mode: side_effecting
argument-hint: "<tag> <content>  — tags: idea | blocker | insight | quote | reminder | decision"
category: fleet-ops
status: candidate
---
# [note]

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=note] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

> Capture before the thought escapes. Think of it as texting yourself — but it lands in the ledger where agents and future sessions can find it.

Faster than `[ledger]` for quick captures. No template, no schema ceremony. One line → one entry.

## Usage

```
[note] idea "BKI onboarding flow could mirror Duolingo streak mechanics"
[note] blocker "Prabhath email still pattern-only — need Hunter verify before send"
[note] insight "When I frame HUMMBL as belonging infrastructure, legal buyers get it faster than IT buyers"
[note] quote "Governance without belonging is compliance theater — R. Paul"
[note] reminder "GA annual registration — $75, overdue — do before Wave 1 closes"
[note] decision "Going with Resend over Postmark — better DX + pricing at our volume"
```

## Tag Definitions

| Tag | Ledger type | When to use |
|-----|------------|-------------|
| `idea` | `insight` | Product ideas, feature concepts, wild thoughts |
| `blocker` | `finding` | Something blocking work — capture now, resolve later |
| `insight` | `insight` | Pattern you just recognized, lesson from the work |
| `quote` | `reference` | Worth-keeping phrases — yours or others' |
| `reminder` | `task` | Time-sensitive to-do that doesn't belong in a PR |
| `decision` | `decision` | Small decisions that don't warrant a full ADR |

## Execution

```bash
# Post to ledger via CLP
python3 -m hummbl_governance.cognition post \
  --type "<mapped_type>" \
  --scope "general" \
  --tags "note,<tag>" \
  --content "<content>"
# The skill invocation runtime injects the caller's canonical identity as agent.

# Confirm landed
~/.venv/bin/python -m hummbl_governance.cognition query \
  --tags "note" --limit 1
```

## Output Format

```
✓ Note captured | <tag> | <timestamp>
Content: <first 80 chars>
Ledger ID: <id>

(retrieve later: [ledger] search "note" or [ledger] query --tags note)
```

## When to Use Instead of `[ledger]`
- `[note]` — one thought, right now, no context needed
- `[ledger]` — structured entry with full metadata, links, scope
- `[decision-log]` — architectural decisions with rationale and ADR format

## Chain
- After capturing a batch of ideas → `[rice-prioritize]`
- Blocker note → escalate to bus with `[bus]`
- Decision note that needs full ADR → `[decision-log]`

## Skill Chains

### Mandatory

None — ledger append is low-risk, content-scanned, and reversible.

### Advisory

- After capturing a batch of ideas → `[rice-prioritize]`
- Blocker note → escalate to bus with `[bus]`
- Decision note that needs full ADR → `[decision-log]`

## Authority

- **T1 (TRUSTED)**: May run
- **T2 (Active/High)**: May run
- **T3 (Medium)**: May run
- **T4 (Probationary)**: May run (ledger append is low-risk)
- **Operator**: Override any restriction
