---
name: draw-mermaid-diagrams
description: >-
  Draw and edit Mermaid diagrams in Markdown. Use when the user wants to
  visualize processes, flows or sequences, or asks for a diagram. Load it before
  writing any Mermaid block, even when you know the syntax — that is why it gets
  skipped.
---

# Draw Mermaid Diagrams

## Overview

Writing Mermaid is not the hard part; producing Mermaid that renders is.
Measured on 2026-08-30/31 over twelve agent-written diagrams: without the
check below, three of three broke on a task whose labels carried parentheses
and whose sequence messages carried semicolons — and every draft written
_with_ the skill broke the same way at first. The diagrams that shipped
correct were the ones where the check ran and the agent fixed what it
reported. That is what this skill is for.

## Rules & Constraints

<rules>
1. **The check is not optional.** Every diagram you write or edit is checked
   before you present it, however simple it looks and however confident you
   are. This is a precondition on showing the diagram, not a step you may skip
   when the diagram seems easy — the drafts that broke were all easy-looking.
2. **Fix and re-check.** A reported problem is repaired and the check is run
   again, until it reports nothing. Reporting the problem to the user instead
   of fixing it is not a substitute.
3. **Do not escape what does not need escaping.** `#`, `&`, `%`, `<`, `>`,
   emoji and line breaks are harmless — see `references/SPEC.md`. Defensive
   escaping makes the source unreadable and fixes nothing.
4. **Keep the user's wording.** Quote the label; do not paraphrase the text to
   avoid quoting it.
</rules>

## Instructions

<step_by_step>

1. **Pick the diagram type.** Flowchart for processes and decision trees,
   sequence for interactions between parties, state for lifecycles, ER for
   schemas, Gantt for timelines, class for structure. `references/SPEC.md`
   lists them with what each is for.

2. **Read `references/SPEC.md` before writing.** It is a hazard list, not a
   syntax dump: which characters end a label early, which reserved words
   cannot be node identifiers, and which characters are safe. Reading it first
   is cheaper than fixing the draft afterwards.

3. **Write the diagram** inside a ` ```mermaid ` block in a Markdown file.

4. **Run the check.** Required, on the file you just wrote:

   ```bash
   python3 scripts/validate.py path/to/diagram.md
   ```

   It needs Python 3 and nothing else — no network, no Node, no install — and
   finishes in milliseconds. Exit 0 means clean; exit 1 prints one line per
   problem with the line number and the fix.

5. **Repair anything it reports and run it again.** Repeat until it is clean.
   Only then present the diagram.

</step_by_step>

## What the check covers

It is a hazard list, not a full parser. It catches the constructs measured to
stop a diagram rendering — unquoted brackets in node labels, edge labels and
subgraph titles; a literal quote inside a label; reserved words used as node
identifiers; a semicolon in a sequence message; a stray pipe in an edge label.
Across 43 synthetic probes and 12 agent-written diagrams it agreed with the
official Mermaid parser on all 55, with no misses and no false alarms.

It will not catch a novel syntax error outside that list. When a diagram uses
a shape or directive you are not sure of, check Mermaid's own reference —
linked at the end of `references/SPEC.md`.

## Resources

- [Rendering hazards, and the syntax reference](references/SPEC.md)
- [`scripts/validate.py`](scripts/validate.py) — the check from step 4
