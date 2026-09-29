---
name: context-audit
description: >-
  Audit an agent's context layout against the four places: system prompt,
  tools, history, tail. Use when the user asks to audit, review or fix their
  agent's context, prompt caching, token spend per turn, or CLAUDE.md /
  AGENTS.md layout. Read-only: reports findings and a fix list, changes
  nothing. Do NOT use for writing evals (evals-bootstrap) or for loop
  design (goal-test).
---

# Audit the context window

Theory: [How models read context](https://undefined-ui.github.io/second-brain-os/#course-1-context/how-models-read)
and [The four places](https://undefined-ui.github.io/second-brain-os/#course-1-context/the-four-places).
Every piece of context belongs in exactly one of four places — a byte-stable
system prompt, a frozen tool set, a compacting history, and a short live tail —
and most agent problems trace back to something sitting in the wrong one.

## Core rule

Report and rank; never edit. The output is an audit, and the user decides
what to apply. If they ask you to apply fixes afterwards, that is a normal
edit session, not this skill.

## Workflow

1. **Find the context sources.** Locate what actually reaches the model:
   system prompt (or CLAUDE.md / AGENTS.md for a Claude Code setup), tool
   definitions, and — if the project logs requests — one full mid-conversation
   payload. If nothing is logged, say so and audit the static files; ask for
   one captured request only if the user can produce it cheaply.
2. **Measure the five numbers.** Approximate token counts for: system prompt,
   tool definitions, message history, retrieved content, current query.
   A rough count (chars / 4) is fine; write all five down.
3. **Hunt cache killers.** Flag every dynamic value in the system prompt —
   timestamps, user names, injected memories, "current task" lines. Each one
   is a guaranteed cache miss on every call. Check whether the tool list can
   change mid-run; a changing list invalidates the whole prefix.
4. **Hunt window bloat.** Find the largest single item in the history. A
   verbatim tool result over ~2,000 tokens should have been a file path plus
   a one-line receipt. Count tools: past twenty (or ~10K tokens of
   definitions), recommend deferred tools + tool search.
5. **Check the tail.** Locate the current goal. If it appears only in the
   opening message, it lives in the weak middle of the window — recommend
   restating it in the tail every three to five steps.
6. **Check guides.** If CLAUDE.md / AGENTS.md exists: it should be a few
   lines of constraints the code cannot show, not four pages of narrative.
   Flag anything the repo already records (structure, history).

## Output format

```
Context audit — <project>
system prompt   <n> tok   <clean | N dynamic values: ...>
tools           <n> tok   <n> tools  <frozen | mutates mid-run>
history         <n> tok   largest item: <what, n tok>
tail            <present | goal only in opening message>

Top fixes, in order of saved tokens per turn:
1. ...
2. ...
```

Each fix names the file and line where possible, states what moves to which
of the four places, and estimates the saving. Close with the one-line rule:
stable prefix, frozen tools, compact history, live tail.
