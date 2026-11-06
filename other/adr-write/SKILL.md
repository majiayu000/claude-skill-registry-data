---
name: adr-write
description: >-
  User-invoked as /adr-write <title>. Scaffolds a new Architecture Decision
  Record in docs/adr/ using the MADR template, pre-filling context from recent
  git log and open GitHub issues. Use when a design decision needs to be
  recorded before implementation.
allowed-tools: Read, Grep, Glob, Bash, Write
invocation: /adr-write <title>
---

# ADR Write (MADR)

Scaffold a new ADR for the decision titled `$ARGUMENTS`.

## Steps

1. Determine the next ADR number: list `docs/adr/`, find the highest
   `NNNN-` prefix, increment (zero-padded to 4 digits). If none exist, start at
   `0001`. Filename: `docs/adr/NNNN-<kebab-title>.md`.
2. Seed **Context** from the repo: run `git log --oneline -10` and, if `gh` is
   authenticated, `gh issue list --state open --limit 10`. Summarise what is
   prompting this decision.
3. Write the file using the MADR template below. Status starts as `Proposed`.
   Use today's date from session context.
4. Add an index line to `docs/README.md`.

## MADR template

```markdown
# NNNN. <Title>

- Status: Proposed
- Date: <YYYY-MM-DD>
- Deciders: <names>

## Context and Problem Statement
<what forces this decision; seeded from git log / issues>

## Decision Drivers
- <driver>

## Considered Options
1. <option A>
2. <option B>

## Decision Outcome
Chosen option: "<option>", because <justification>.

### Consequences
- Good: <…>
- Bad / risk: <…>
- Follow-up (coder/qa/docs): <…>

## Pros and Cons of the Options
### <option A>
- Good: …
- Bad: …
```

## Output

Print the path of the created ADR and a one-line summary. Note that the
`app-architect` agent owns the decision content - this skill only scaffolds and
seeds it. Leave it `Proposed` for human/architect sign-off.
