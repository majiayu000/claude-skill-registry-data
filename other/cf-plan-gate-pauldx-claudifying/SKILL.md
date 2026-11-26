---
name: cf-plan-gate
description: When the user asks to enforce spec-driven development, add planning gates, require specs before coding, or prevent scope creep — activate this SDD enforcement skill
---

# Plan Gate — Spec-Driven Development Enforcement

## Concept

Plan Gate enforces **Spec-Driven Development (SDD)** through two complementary hooks that keep
Claude aligned with your written specifications. Instead of letting implementation drift from the
plan, these hooks provide continuous feedback:

1. **plan-gate.sh** (PreToolUse) -- reminds you when no recent `.spec.md` file exists before
   editing source code. Non-blocking, just a nudge.
2. **scope-guard.sh** (Stop) -- compares files actually modified against files declared in the
   active spec. Warns about out-of-scope changes. Non-blocking.

Together they create a lightweight planning discipline: write a spec, declare what files you will
touch, then implement. Any deviation gets flagged.

## The `.spec.md` File Format

Create a `.spec.md` file before starting work. The critical section is **Files to Create/Modify**:

```markdown
# Feature: User Authentication
## Goal
Add JWT-based authentication to the API gateway.
## Files to Create/Modify
- src/auth/jwt.service.ts
- src/auth/auth.guard.ts
- src/config/jwt.config.ts
## Acceptance Criteria
- Tokens expire after 1 hour
- Invalid tokens return 401
```

Filenames are matched as substrings against git-modified paths. Use relative paths.

## How plan-gate.sh Works

1. Claude attempts to edit a source file via Edit or Write
2. The PreToolUse hook runs `plan-gate.sh`, which searches for `.spec.md` modified in last 14 days
3. **Spec found** -- edit proceeds silently (exit 0)
4. **No spec found** -- prints a reminder, still allows the edit (exit 0, non-blocking)

## How scope-guard.sh Works

1. Claude finishes a task and the Stop event fires
2. Script collects modified files via `git diff --name-only` (staged + unstaged)
3. Finds the most recently modified `.spec.md` (within 60 minutes)
4. Extracts declared files from "Files to Create/Modify" section, compares against actual changes
5. **All in scope** -- silent exit. **Out-of-scope** -- prints warning listing unexpected files

Excluded from scope checking: test files, config, infrastructure, docs, lockfiles.

## Installation

Add both hooks to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/skills/skills/plan-gate/scripts/plan-gate.sh",
            "statusMessage": "Plan Gate: checking for active spec..."
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/skills/skills/plan-gate/scripts/scope-guard.sh",
            "statusMessage": "Scope Guard: checking for out-of-scope changes..."
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/` with the actual absolute path to this repo on your machine.

## Customizing

- **Spec freshness**: `plan-gate.sh` uses `-mtime -14` (14 days). Use `-mtime -7` for weekly sprints.
- **Scope-guard recency**: Uses 60-minute window for active spec. Increase if you write specs early.
- **Exclusions**: Both scripts skip test/config/infra files. Add project-specific patterns as needed.

## Gotchas

- **Spec location**: Both scripts search from `git rev-parse --show-toplevel`. Keep specs in the repo.
- **Multiple specs**: `scope-guard.sh` picks the most recently modified `.spec.md`. Archive old specs
  when starting new work to avoid ambiguity.
- **Partial path matching**: Declared file `auth.service.ts` matches `src/auth/auth.service.ts` but
  also `old/auth.service.ts`. Use specific paths in your spec.
- **Non-blocking by design**: Neither hook blocks Claude. They are reminders. For hard enforcement,
  change exit codes to `2` in `plan-gate.sh`.
- **Git dependency**: `scope-guard.sh` relies on `git diff`. Fresh repos with no commits produce no
  output, so the guard stays silent.
- **CLAUDE_TOOL_INPUT_FILE**: Set by Claude Code automatically. For manual testing, export it yourself.

## Pairing With Other Skills

- Use `/cf-tdd-gate` alongside Plan Gate for spec + test-first enforcement
- Use `/cf-workflow-auto` to auto-generate `.spec.md` templates from issue descriptions
- Use `/cf-scqa` to structure the spec's goal and context sections
