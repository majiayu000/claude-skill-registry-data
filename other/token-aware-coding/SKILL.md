---
name: token-aware-coding
description: General token-efficiency habits for this kit's agents — prefer targeted search over full reads, precise @-mentions, periodic summarization, avoid re-reading known context. Read once at session start or when a task looks like it'll involve many files/tool calls.
---

# Working token-efficiently

These are habits, not a checklist to run every time — apply them by default.

- **Prefer Grep/Glob over a full Read** when you only need to find or confirm something (a
  symbol, a device name, whether a pattern already exists). Read the whole file only once you
  actually need to edit it or read surrounding context matters.
- **Use precise `@file` mentions** instead of describing "the file that handles X" and having the
  agent search for it, when you already know the path.
- **Summarize internally after 3-4 tool calls** in a research/search sequence rather than
  carrying every intermediate result forward verbatim — keep the conclusion, drop the scratch
  work.
- **Don't re-read a file you already have the relevant content from earlier in the same task** —
  reuse what's already in context instead of re-fetching it "to be safe."
- **Grep ROADMAP.md's `Tasks` table for the one task ID/row you need instead of reading the whole
  file** once it has grown to dozens of tasks across several releases — the plan-first workflow
  (`~/.claude/CLAUDE.md` rule 13) means this table only grows, and most operations (flipping a
  Status, checking one acceptance criterion) only ever need one row.
- **Don't restate the whole conversation or task back to the user** before acting — a one-line
  "doing X" (or nothing, straight into the tool call) beats a paragraph of preamble.
- **Delegate verbose or exploratory work to a subagent** (when available) rather than doing wide
  exploration inline — the subagent's intermediate output doesn't consume the main session's
  context.
- **Use `/clear` or `/compact`** between unrelated tasks in the same session instead of letting
  context accumulate across work that has nothing to do with each other.
- Periodically, `/context` shows what's actually consuming the window — useful when a session
  feels slow or a task keeps needing trimming.

None of this trades off correctness — when a task genuinely needs a full read or a broad
search, do it. This skill is about not doing the expensive thing by default when a cheaper one
answers the same question.
