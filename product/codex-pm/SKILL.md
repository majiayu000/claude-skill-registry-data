---
name: codex-pm
description: Use when the user needs product-management help for Codex or a Codex-like AI coding product, including product analysis, PRD drafting, roadmap planning, UX review, safety workflow design, skill strategy, or competitive teardown.
---

# Codex PM

This skill has two parts:

1. `SKILL.md`
   This file only defines when to use the skill and how to use it.
2. Knowledge description file
   All detailed Codex product facts, PM interpretations, and reusable analysis material live in [references/knowledge.md](references/knowledge.md).

## Required Usage Rule

Every time this skill is triggered, first inspect the knowledge description file before producing the answer.

Recommended sequence:

1. Search [references/knowledge.md](references/knowledge.md) for the relevant topic.
2. Read only the matching section(s).
3. Separate confirmed facts from inference.
4. Produce the PM output the user asked for.

## Suggested Search Topics

Search the knowledge file for one or more of:

- `cloud agent`
- `desktop app`
- `CLI`
- `approval modes`
- `sandbox`
- `skills`
- `automations`
- `PM implications`
- `PM questions`

## Typical Outputs

- product summary
- feature brief
- PRD
- competitive teardown
- roadmap
- UX flow
- PM operating skill

## Output Rule

Do not treat guessed internal OpenAI decisions as fact. Use the knowledge file as the source of truth for this skill.

