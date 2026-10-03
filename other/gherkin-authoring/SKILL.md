---
name: gherkin-authoring
description: Use when drafting, reviewing, or improving Gherkin, Cucumber scenarios, BDD acceptance criteria, feature examples, Scenario Outlines, Backgrounds, Rules, Doc Strings, Data Tables, tags, or Gherkin embedded in Markdown.
license: MIT
compatibility: Codex lazy-loaded skill for OpenSpec projects.
---

# Gherkin Authoring

Use this optional skill only after recommendation and user consent.

Write Gherkin as executable examples of business behavior. Optimize for domain
language, concrete examples, and observable outcomes.

## Workflow

1. Identify the Gherkin region or acceptance-criteria section.
2. Preserve surrounding Markdown unless explicitly asked to rewrite it.
3. Clarify initial state, event, and observable outcome.
4. Choose the smallest useful structure: `Feature`, optional `Rule`,
   `Background`, `Scenario`, `Scenario Outline`, or `Examples`.
5. Keep scenarios short, usually 3-5 steps.
6. Review syntax, duplicate steps, outcome observability, tables, and doc
   strings before returning.

## Rules

- `Given` is state, not user interaction.
- `When` is one meaningful event.
- `Then` is externally observable outcome.
- Avoid UI clicks, HTTP calls, database rows, queues, and mocks unless they are
  the actual domain contract.
- Use two-space indentation unless preserving existing style.
- Escape `|` as `\|`, newline as `\n`, and backslash as `\\` in tables.
