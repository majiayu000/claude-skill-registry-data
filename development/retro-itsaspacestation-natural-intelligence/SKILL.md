---
name: retro
description: "Use when the user asks what would have prevented a mistake, asks for a retro, a post-mortem, or lessons, or asks how to stop something happening again. Also use when a session ended with a wrong fix, a missed convention, a slow search, or a repeated question, and at the end of a plan workspace before integration."
---
# Retro

## When to use
- User asks what would have prevented a mistake
- User asks for a retro, a post-mortem, or lessons
- User asks how to stop something happening again
- A session ended with a wrong fix, a missed convention, a slow search, or a repeated question
- A plan workspace ends, before integration

## Overview

A retro turns one session's friction into a change to the agent's environment.
The product is out of scope: the output is a check, a convention, or a pointer.
Every finding cites evidence under the [`evidence-based-analysis`](../evidence-based-analysis/SKILL.md) rules.
A finding without a line to point at is an opinion, not a finding.

## Workflow

1. Gather the friction. Read the transcript, the diff, the test runs, and the user's corrections.
2. Write one finding per friction. Cite a file:line or quote the line that shows it.
3. Classify each finding: mechanical, judgement, or navigation.
4. Propose one check per finding. Name the file it lands in.
5. Present the table, severity first. Stop and wait for the user.
6. Apply after approval only. One commit per check, with the [`git-conventions`](../git-conventions/SKILL.md) skill.

## Classification

Three classes. Each has one outcome.

| Class | The friction | Becomes |
|---|---|---|
| Mechanical | A mistake a machine can catch | A deterministic check: a lint rule, a test, a hook, a CI job |
| Judgement | A call a human made differently | A written convention: the project CLAUDE.md, a coding standard, a glossary entry when GLOSSARY.md exists |
| Navigation | Time lost finding something | A pointer: a line in the docs or the README |

When two classes fit, pick mechanical. A check runs on its own; a convention needs a reader.

Not: "be more careful with imports"
Yes: "lint rule forbidding relative imports, added to the CI job"

## Output

One table, severity first. One row per finding. No praise rows.
A session with nothing to fix gets one line, not a table.

| Column | Holds |
|---|---|
| Severity | Wrong result, lost time, or repeated question; the sort key |
| Finding | What went wrong, in one clause |
| Evidence | A file:line, or a quoted line from the transcript |
| Class | Mechanical, judgement, or navigation |
| Proposed check | The change and the file it lands in |

Severity: a wrong result outranks lost time; lost time outranks a repeated question.

## Boundaries

Never edit product code or tests of product behaviour.
A code fix belongs to the [`debug`](../debug/SKILL.md) or [`software-engineer`](../software-engineer/SKILL.md) skills.
A check this skill adds must pass the project's own CI before the commit.
Never remove an existing check. Tighten a noisy one instead.
