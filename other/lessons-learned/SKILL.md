---
name: lessons-learned
disable-model-invocation: true
description: >-
  Extract lessons learned from the current conversation — reviewing the session for moments that
  went wrong or required rework — and append them to LESSONS_LEARNED.md.
context: fork
background: false
---

# Lessons Learned Extractor

Review the full conversation, identify moments where something went wrong or required correction,
and append structured lessons to `.agents_workspace/LESSONS_LEARNED.md`.

## What counts as a lesson

- **Corrections** — user had to ask you to redo, move, rename, or restructure something
- **Failed commands** — a tool call errored and required a follow-up fix
- **Misunderstood requirements** — you built in the wrong place, format, or scope
- **Wrong assumptions** — you assumed something that turned out to be false
- **Sequencing mistakes** — steps done out of order or a prerequisite skipped

Do NOT capture: things that worked correctly first time, routine tool use, or preference changes
that weren't errors. Write for a future LLM reading cold — so the next session avoids repeating.

## Output format

```markdown
## YYYY-MM-DD — <short title describing the mistake>

**What happened:** One or two sentences — the concrete mistake or misunderstanding.

**Lesson:** One or two sentences — the actionable rule to apply next time.
```

- Use today's actual date
- Title names the mistake, not the fix (e.g. `mv requires parent directory to exist`)
- Keep each entry under 6 sentences — dense and specific beats thorough and vague
- Prefer file paths, command names, and exact decisions over abstract descriptions

## File handling

1. Check whether `.agents_workspace/LESSONS_LEARNED.md` exists.
2. If missing, create it (including parent directories) with this header:
   ```markdown
   # Lessons Learned

   ---
   ```
3. Append new lessons at the very end — after the last existing entry, never between entries.
4. Use the Edit tool with the final line(s) as the `old_string` anchor so insertion lands at the true end.
5. Separate each new lesson from the previous content with a blank line.

## After writing

Report: how many lessons were added and the title of each (one line each).
If no lessons were found, say so explicitly rather than writing a placeholder entry.
