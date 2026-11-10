---
name: stress-next
description: Build the first open step of a listed stressor app's PLAN.md in a worktree of the app's repo, filing every framework gap it meets with `fli file --area <app>` and ticking the box — one step per session. Use when asked to run the next stressor step.
disable-model-invocation: true
---

# Stress next

The loop from *an open box in a stressor's plan* to *that box ticked, with every framework gap it met filed*. Arguments: an app name and a step id (`scripts/stress-loop.mjs` passes both, with a `## Pre-brief` naming the worktree, the branch and the framework root).

**A stressor exists to find what the framework cannot do yet.** So the session's job is two things at once: build the step as the plan says, and file each gap — a defect, a missing feature, a choice the framework has not made — in the framework's registers rather than working around it in the app (`docs/STRESSOR-UPGRADE.md`). A step built around a gap hides the gap, which is the one failure this skill exists to prevent.

## 1. Pick

The pre-brief names the app, its worktree and the step. Without one, the step is `fli plan <app dir>/PLAN.md`'s first open box, and the worktree is yours to make: `git -C <app repo> worktree add -b stress/<step> ~/.fli/stress/<app> HEAD`. **Say the app and the step id before doing anything else**, so a person watching can redirect.

**Work only in the worktree.** The app's own checkout is the owner's working tree and holds their uncommitted work; a file written there is a collision. If the worktree's branch carries commits from an earlier attempt and the arguments say so, they are yours: read `git log` and `git diff` there and build on them.

## 2. Brief

Read the plan's phase around the step (`fli outline PLAN.md "Phase N"`), the app's `CLAUDE.md` or `AGENTS.md` and the files the step names, in the worktree. The step's own words are the whole specification; a step that says "file what broke" is filed, not built. A search across the framework goes to one `Explore` subagent asked for `file:line` answers only — a framework package's `CLAUDE.md` is tens of KB and a step needs a paragraph of it.

## 3. Build

Build the step in the worktree, the way the plan says. Prove it with the app's own `check` and `test` scripts from the pre-brief, run with `cd <worktree> &&`. A dev server the step needs runs on the app's own ports and is stopped before the session ends.

**When the framework stops you, stop building and file (step 4).** The signs: a `.lite` attribute the schema does not take, a service hook with no seam for the step, a `fli` command that refuses something the plan assumes, a Mesa form that cannot express the field, a check rule that fires on correct code. Do not patch the framework (`node_modules/@frontierjs/*` is linked into this tree; a change there is a change to the framework the fix loop owns), and do not write the app around it.

## 4. File

`fli file` runs from the framework root, your cwd. First `fli find <terms>`: a gap already filed takes `fli amend <id> --detail "<also met by <app> step N.N>"` and no new row.

```
fli file --sev S3 --area <app> --title "<the gap, one sentence, as the step met it>" --detail "Met building <app> PLAN.md step N.N · <what was tried, the error verbatim> · [file](<app>/path)"
```

A **choice** the framework has not made is a question, not a defect: `fli file --sev decision --area <app> --title "<the question?>" --detail "Found building <app> step N.N"`, then write lettered options and a recommendation under the step's bullet in the worktree's PLAN.md, in `frame-next`'s shape (`**A** — … / **Recommend A** — why`). Run `decision-rules` before writing options. **Never rule**: `DECISIONS.md` is not written and `fli decide` is not run, except `fli decide <Q> --file PLAN.md` for a question the app's own plan asks and the owner has already framed.

**The pre-brief says how many rows this run may file.** Past that count, a gap goes as a line under the step's bullet (`- gap: …`) and the step ends `blocked`; the next run files it.

## 5. Tick

When the step is built and proved, tick its box in the worktree's `PLAN.md`: `- [ ] N.N …` becomes `- [x] N.N …`, and one indented line under it says what was built and what proves it, in the plan's own voice. When a filed gap stops the step, the box stays open and the line under it names the ids: `  - blocked by FJS-####: <what the step cannot do until it is fixed>`.

Then `fli done` from the framework root and clear what it lists for the registers you wrote; the app's own check is step 3's. Do not commit: the loop commits the branch when the session ends, whatever the outcome, and the owner merges it.

## 6. Report

Say what was built, what was filed and why, and what the step still needs. **The last line of the report is exactly `stress-next: <app> <step> <status>`**, status one of `ticked`, `blocked` (followed by ` — ` and the ids), `busy` or `failed`. The loop reads the worktree's plan and the registers first and this line only for what they cannot show.

Then end the session. **One step per session**: the next box builds on this one, and the owner has not merged it yet.
