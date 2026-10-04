---
name: goal-achievement-review
description: Goal achievement verification methodology. Truths, artifacts, and key links verification for reviewer agent.
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Goal Achievement Review

## Truths Verification

For each truth from must_haves:
- **TRUE**: confirmed by code (file exists, logic is correct)
- **FALSE**: truth not achieved → P0 blocker
- **PARTIAL**: partially implemented → P1 warning

## Artifacts Verification

For each artifact, 3 levels:
- **Level 1**: File exists?
- **Level 2**: File is not a stub (real code, not placeholder)?
- **Level 3**: File exports/contains what was declared?

## Key Links Verification

For each key_link:
- Is there a real connection from → to?
- Is the `via` method used?

```bash
# Example key_link check
grep -l "fetch.*api/chat" src/components/Chat.tsx  # from → to via fetch
```

## Output Format

```
## Goal Achievement
| Truth | Status | Evidence |
|-------|--------|----------|
| "Shortcodes are replaced" | TRUE | parser.ts:45 parseShortcodes() |
| "Non-existent don't break" | PARTIAL | no fallback for unknown |
```
