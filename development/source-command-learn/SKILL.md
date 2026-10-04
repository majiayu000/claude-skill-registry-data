---
name: "source-command-learn"
description: "Extract reusable patterns from the current session and save them as skill files. Run after solving a non-trivial problem."
---

# source-command-learn

Use this skill when the user asks to run the migrated source command `learn`.

## Command Template

# /learn — Extract Reusable Patterns

Analyze the current session and save any patterns worth reusing as skill files.

## What qualifies

Extract only if the pattern is:
- **Non-obvious** — not just fixing a typo or standard syntax
- **Reusable** — applicable beyond this specific session
- **Generalizable** — worth activating in a future session

Good candidates:
- Error resolution patterns (root cause + fix + when it recurs)
- Non-obvious debugging techniques or tool combinations
- Library/API quirks or version-specific workarounds
- Project-specific conventions discovered during investigation

Do **not** extract:
- One-time issues (API outages, transient failures)
- Trivial fixes (missing semicolons, import order)
- Patterns already covered by existing skills

## Process

1. Review the session for extractable patterns
2. Pick the single most valuable insight (one skill per run)
3. Draft the skill file using the format below
4. Show the draft and ask for confirmation before saving
5. Save to `.Codex/skills/learned/{pattern-name}.md`

## Skill file format

Use SKILL.md format so the skill is discoverable by the skills system:

```markdown
---
name: {pattern-name}
description: >
  {One-line trigger description — when should this activate?
  Be specific enough that Codex will recognize the situation.}
type: learned
extracted: {YYYY-MM-DD}
---

## Problem
{What goes wrong — be specific about symptoms}

## Root Cause
{Why it happens}

## Solution
{The fix or technique}

## Example
{Code or command example if applicable}

## When to apply
{Trigger conditions — what situation activates this pattern}
```

Save to `.Codex/skills/learned/{pattern-name}/SKILL.md` so the skills index picks it up.
