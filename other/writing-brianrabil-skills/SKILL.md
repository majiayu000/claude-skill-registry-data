---
name: writing
description: "Router for the writing toolkit: pick the right writing stage for any form — capture, outline, world bible, draft, critique, revise, line edit, fact-check. Use when a writing task doesn't name a specific skill, when a piece is not working and the stage is unclear, when starting a new piece, or when unsure whether to critique, revise, edit, outline, or fact-check. For fiction, essays, articles, scripts, newsletters, books, and series."
---

# Writing

A piece of writing has one **spine** — the single claim it argues (nonfiction)
or the story engine that drives it (fiction): protagonist want against
obstacle, promising an ending. Every stage below serves that spine; when a
change doesn't, either the spine is wrong or the change is.

Pick the stage you are actually in; you may loop.

| Skill              | Reach for it when                               | It returns                                         |
| ------------------ | ----------------------------------------------- | -------------------------------------------------- |
| `writing-capture`  | A topic, seed, notes, transcript — no piece yet | Fragments: noticings, lines, scenes, half-thoughts |
| `writing-outline`  | Material exists; order or engine unsettled      | Spine or story engine + beat sheet + scene list    |
| `writing-bible`    | A world or series must stay consistent          | Canon: entries, ledgers, retcon log                |
| `writing-draft`    | Structure settled; prose is needed              | The piece, grown block by block or scene by scene  |
| `writing-critique` | A draft exists; something is off                | Read-only findings, ranked, no edits               |
| `writing-revise`   | Findings or a brief; substance must change      | Revised piece + change log                         |
| `writing-edit`     | Substance right, sentences wrong                | Line-level changes, meaning fixed                  |
| `writing-verify`   | Claims will go out in the world                 | Claim-by-claim source audit                        |

Forms ride the stages: fiction branches (story engine, scene list, scene
craft), essays and arguments (spine, blocks, evidence), scripts (acts, scene
beats), poetry and technical writing where the stages fit. Each stage skill
carries its own reference files for the form you're in — you never need more
than the stage you're in.

## The two rules that keep the loop honest

**Diagnose before you fix.** Run `writing-critique` before `writing-revise`
unless the problem is already known and named. Fixing the wrong thing is the
most expensive move in writing.

**Keep the spine visible.** If a change doesn't serve the spine, either the
spine is wrong or the change is. When a user request fights the spine, surface
the fight instead of smoothing it over.

## The pipeline in practice

Real work loops: capture → outline → (bible alongside) → draft → critique →
revise → edit → verify. Read-only stages (`writing-critique`, `writing-verify`)
report; everything else writes to files. When a user hands you a draft with no
stage named, run `writing-critique` first unless they asked for a specific
operation — the diagnosis sets the order of everything after it.
