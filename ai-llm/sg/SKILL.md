---
name: sg
description: Metacognitive oversight. "$sg review" for on-demand evaluation, "$sg init" to set up, "$sg audit" to review decisions.
---

# superego - Metacognitive Oversight

Superego provides metacognitive review for AI sessions, catching premature commitment, scope creep, and misalignment.

All commands invoke the `sg` CLI. If sg is not installed, show:
```
sg not installed. Install with:
  brew tap open-horizon-labs/homebrew-tap && brew install superego
  # or: cargo install superego
```

## $sg review

Review staged changes or current work. On-demand metacognitive evaluation.

```bash
sg review
```

## $sg init

Initialize superego for this project.

```bash
sg init
```

## $sg audit

Review decision history with LLM analysis.

```bash
sg audit
```

## $sg history

Query decision history.

```bash
sg history
```

## $sg prompt list

List available superego prompts.

```bash
sg prompt list
```

## $sg prompt switch <name>

Switch to a different superego prompt.

```bash
sg prompt switch <name>
```

## $sg prompt show

Show current prompt content.

```bash
sg prompt show
```

## $sg mode

Show current evaluation mode (always or pull).

```bash
sg mode
```

## $sg reset

Reset superego state (recovery from corruption).

```bash
sg reset
```

## $sg check

Check hooks and auto-update if outdated.

```bash
sg check
```

---

## Protocol

**Mode:** Pull mode - evaluates only when explicitly requested.

**When to use $sg review:**
- Before committing to a plan or approach
- When choosing between alternatives
- Before non-trivial implementations
- When the task feels complex or uncertain
- Before claiming work is "done"

**Results:**
- `has_concerns: true` = STOP and show feedback to user
- `has_concerns: false` = continue with confidence
- `skipped: true` = proceed normally (this is fine)

Superego is opt-in. Use it for high-stakes decisions, architectural choices, or when you want a second opinion.
