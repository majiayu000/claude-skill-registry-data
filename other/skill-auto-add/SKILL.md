---
description: Update a skill or prompt using lessons learned from a file's Git history
argument-hint: <FILE> <PROMPT>
model: sonnet
---

# Goal

- The user gives two arguments:
  - `<FILE>`: a path to a file edited across one or more Git commits
  - `<PROMPT>`: a path to a skill (`SKILL.md`) or prompt file to improve
- The edits to `<FILE>` encode a lesson: someone fixed by hand what `<PROMPT>`
  should have gotten right the first time
- Update `<PROMPT>` so that, given the original `<FILE>`, it would produce the
  final `<FILE>`
- Generalize: infer the underlying *rule*. Do not hard-code the strings from this
  one diff

# Inputs

- If `<FILE>` or `<PROMPT>` is missing or ambiguous, stop and ask the user. Do not
  guess
- If `<FILE>` has no committed changes, report that and stop

# Workflow

## Determine the Changes

- Find the commits that touched `<FILE>`:
  ```bash
  > git log --oneline --follow -- <FILE>
  ```
- Identify the *first* and *last* relevant revisions. Default to the full history.
  If the user named a range, use that instead
- Extract `<CHANGES>` as a unified diff:
  ```bash
  > git diff <FIRST_SHA> <LAST_SHA> -- <FILE>
  ```
  - If the diff is large, also read the final version to see the intended end
    state, not just the deltas:
    ```bash
    > git show <LAST_SHA>:<FILE>
    ```
- Do not use interactive commands (e.g., `git difftool`). They block

## Read the Prompt and the Conventions

- Read `<PROMPT>` in full
- Read `.claude/skills/skill.rules.md` for the rules that govern how skills and
  prompts are written
- Read any files `<PROMPT>` references, so you do not duplicate a rule that
  already lives elsewhere

## Infer the Rules

- For each meaningful hunk in `<CHANGES>`, note:
  - What changed (before -> after)
  - The general rule it implies
  - Whether `<PROMPT>` already covers it (fully, partially, not at all)
- Drop hunks that are one-off content edits, not repeatable rules (e.g., a typo
  fix, a date update). Say which hunks you dropped and why
- Merge restated rules. Prefer one sharp rule over three overlapping ones

## Improve the Prompt

- Draft the minimal edit to `<PROMPT>` that encodes the inferred rules:
  - Amend an existing rule when one is close but imprecise
  - Add a new rule only when no existing rule covers the case
  - Keep the structure, heading style, and voice of `<PROMPT>`
  - State rules as imperatives, with a short before/after example when a rule is
    easy to misread
- Do not grow the prompt unnecessarily. If the new rule makes an old one
  redundant, remove the old one

## Apply via rules.add

- Follow `.claude/skills/rules.add/SKILL.md`: propose the change to the user
  first, then apply it once approved

# Output

Report, in this order:

1. The commit range and files inspected
2. A table of inferred rules: change observed -> rule -> covered / new
3. The proposed diff to `<PROMPT>`
4. Anything you deliberately did not encode, and why

# Verification
- [ ] The proposed diff was shown to the user before `<PROMPT>` was changed
- [ ] Each inferred rule is a general rule, not a hard-coded string from the one
      diff inspected
- [ ] No rule made redundant by the new edit was left in `<PROMPT>`
