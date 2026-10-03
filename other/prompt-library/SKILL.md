---
name: prompt-library
description: Save a prompt that worked well for this repo, or look one up before re-deriving it from scratch. Use when a prompt (for one of ReVision's four tools, or for a Claude Code task in this repo) produced a notably good result and is worth reusing, or when starting a task that might already have a saved prompt.
---

# Prompt library

One job: read from and append to `docs/prompt-library.md`, a checked-in file
of prompts that worked well in this repo. Not a general prompt-engineering
guide — just a save/retrieve mechanism so a good prompt doesn't get
re-derived from memory every time.

## Before writing a new prompt from scratch

Check `docs/prompt-library.md` for an existing entry covering the same task
(same tool, same kind of request). If one's close, adapt it instead of
starting over.

## When to save one

Only add an entry when a prompt clearly outperformed a first attempt —
noticeably better structure, fewer follow-up corrections, or a result the
user explicitly praised. Routine prompts that worked as expected don't need
an entry; this is a library of *wins*, not a transcript log.

## Entry format

Append to `docs/prompt-library.md` under the right category heading:

```markdown
### <short title>

**Use for:** <the situation this applies to>
**Prompt:**
> <the exact prompt text, with [placeholders] for the variable parts>
**Why it works:** <one line — the specific thing that made it effective>
```

Keep entries short. If the file doesn't have a fitting category heading yet,
add one (`## <Category>`) rather than forcing the entry under an unrelated
one.
