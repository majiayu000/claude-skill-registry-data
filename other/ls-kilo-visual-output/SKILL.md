---
name: ls-kilo-visual-output
description: "Kilo CLI visual output organization guide. Defines structured, readable response patterns for questions, options, preferred choices, rationale blocks, and execution summaries without relying on unsupported inline color control."
metadata:
  version: "1.0"
compatibility: "Kilo CLI-oriented guidance. Uses plain Markdown/text only; no required binaries, scripts, or ANSI color support. Patterns can be adapted to other agent CLIs."
---

# ls-kilo-visual-output

## When to use

Use this skill when the user asks for:

- clearer or more visual Kilo CLI output,
- better readability for decision trees,
- distinction between question/options/preferred/rationale,
- response templates for planning or execution reports.

## Important constraints

1. Do **not** assume per-message or inline text color control is available in Kilo CLI.
2. Do **not** rely on ANSI escape sequences for critical meaning.
3. Use semantic structure (labels, headings, spacing) as the primary readability method.
4. Mention `/themes` only as a global user-side appearance control.

## Default formatting profile

- Mode: `markdown-basic`
- Structure: short headings + explicit labels
- Labels to use:
  - `Question:`
  - `Options:`
  - `Preferred:`
  - `Rationale:`
  - `Your reply:`

## Decision tree response template

Use exactly one question per turn.

```md
### Decision X/N - <topic>

**Question:** <single question>

A. <option A>
B. <option B>
C. <option C>
D. <option D>

**Preferred:** <A|B|C|D>

**Rationale:** <one concise paragraph>

**Your reply:** Choose A/B/C/D (or provide a custom answer).
```

## Execution summary template

```md
### Execution summary
- Status: <Success|Partial|Failed>
- Scope: <what was processed>
- Updated: <count or list>
- Skipped: <count or list>
- Errors: <none or short list>

### Next actions
1. <action 1>
2. <action 2>
```

## Plain-text fallback template

```text
[Decision X/N] <topic>
----------------------
Question: <single question>
A) <option A>
B) <option B>
C) <option C>
D) <option D>
Preferred: <A|B|C|D>
Rationale: <one concise paragraph>
Your reply: Choose A/B/C/D or provide custom input.
```

## Practical guidance for agents

1. Keep lines compact; avoid large dense paragraphs.
2. Use one block per decision/question.
3. Keep rationale to one concise paragraph unless user asks for detail.
4. Use tables only if known renderer support is good.
5. Never encode important meaning with color alone.

## Embedded templates

This skill is self-contained. Use the templates above as the source examples for Kilo CLI output; if future `references/` or `templates/` files are added, link them here with paths relative to this skill directory.
