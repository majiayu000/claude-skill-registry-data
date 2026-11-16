---
name: yt-research
description: >-
  Research a video from its primary source before anything is written: a cited
  brief of what the source actually says, then an independent fact check of the
  finished script. Use for history, mythology, scripture, science or any video
  that retells a text or a record - "research this", "what does the original
  say", "fact check my script", "is this accurate", "find the source".
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/sourcekit.py *)
---

# yt-research

A retelling channel lives or dies on one promise: what you say happened is what the source says
happened. This skill keeps it. It works in two passes, and the second is done by someone who did
not do the first.

```bash
python3 ${CLAUDE_SKILL_DIR}/sourcekit.py index source.txt          # sections with line ranges
python3 ${CLAUDE_SKILL_DIR}/sourcekit.py find  source.txt "phrase"   # where the source says it
python3 ${CLAUDE_SKILL_DIR}/sourcekit.py show  source.txt "Canto XLV"
```

The tools live in this skill's folder. `${CLAUDE_SKILL_DIR}` is that folder in Claude Code; anywhere
it does not expand (claude.ai, Codex), use the folder this SKILL.md was loaded from.

## 1. Get the primary source

The text itself, not a summary of it and not a video about it. Prefer a public-domain translation
or the original record: Project Gutenberg, sacred-texts.com, archive.org, official transcripts.
Save it as plain text in the project and write down what it is: translator, year, edition, what it
leaves out. If the edition numbers its chapters differently from other editions, say so now, and
cite in this edition's numbering every time.

If the user cannot share or name a source, stop and say the video cannot be checked. Do not fall
back on memory and present it as the text.

## 2. The brief (`brief.md`)

Index the source, read the sections the video covers - in full, footnotes included - and write:

- **Events in order**, each with its section and line range: "Book III, Canto XLV, lines 32700-32790".
- **Words worth quoting**, short, with line numbers.
- **The careful list:** what is ambiguous, what the translator flags as a later insertion, what the
  source omits, and every famous detail that comes from a later retelling rather than this text.
  The script may mention those, but only as what they are ("later retellings add...").

The brief is what the script is written from. If it is not in the brief, it is not in the script.

## 3. The independent fact check (after the script is written)

Whoever wrote the script does not check it. Start a fresh agent that never saw the writing and give
it this, filled in:

> You are fact-checking a narration script against its source. You did not write it.
> Script: `<path>`. Source: `<path>`, lines `<a>-<b>` (`<edition>, <sections>`). Read those lines
> in full, footnotes included.
> For every factual claim (who did what, numbers, names, order of events, speech), return one row:
> `| Para | Claim | Verdict | Evidence (line numbers, short quote) |`
> Verdicts: SUPPORTED (the source says it) · NOT IN SOURCE (invention or later tradition; say which
> if you know) · CONTRADICTED (the source says otherwise) · OVERSTATED (true in spirit, stronger or
> more specific than the text) · FLAGGED (the source has it, but the editor calls the passage
> spurious).
> No line number, no SUPPORTED. Paraphrase is fine; changed meaning is not. Also list anything the
> script leaves out that would mislead a viewer. End with the count of each verdict.
> Write the table to `factcheck.md`. Do not edit the script.

**Gate:** nothing is recorded until `factcheck.md` has no CONTRADICTED, and every NOT IN SOURCE,
OVERSTATED and FLAGGED claim is fixed or said plainly in the narration.

## What to hand back

The brief, the source's line ranges, and the careful list. After the check: the verdict counts and
each claim that needs fixing, with the line that settles it.

## Before you hand it over

This skill drafts; you publish. End with the copy-ready block and one question: **post it as is,
or another pass?**
