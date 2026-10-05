---
name: start-session
description: "Start a new working session on animath. Reads the latest handoff, creates a progress report, and presents context. Invoke at the beginning of a conversation when the user or an agent asks to start/kick off a session (e.g. /start-session) — do not auto-invoke spontaneously."
argument-hint: "[session focus, one sentence]"
---

# Start Session

Initialize a new working session on **animath**. Read the latest handoff, create a
progress report, and present context. Do NOT start any implementation work.

## Path Convention (read first)

Session logs are **committed to the repo** and partitioned **per branch** so
parallel branches never collide. Each report is **Markdown + YAML frontmatter**
(see `docs/sessions/REPORT_STYLE.md`): it reads natively on GitHub, and the
build (`npm run sessions`) renders it into the rich HTML view. Everything this
session writes goes under a branch-slug folder:

```
docs/sessions/progress/<branch-slug>/YYYY-MM-DD-SNN-description.md
docs/sessions/handoff/<branch-slug>/YYYY-MM-DD-SNN-description.md
```

`<branch-slug>` = the current branch (`git branch --show-current`) with the
`claude/` prefix stripped and any `/` turned into `-` — e.g. `claude/menu-bar`
→ `menu-bar`. The folder name is a pure function of the branch (no shared index
to merge), so two branches can never write the same path. **Keep branch names
short and topical** so the folders stay tidy.

## Steps

1. **Resolve the branch slug** — run `git branch --show-current`, strip a leading
   `claude/`, replace `/` with `-`. Use it for every path below; create the
   `docs/sessions/{progress,handoff}/<branch-slug>/` folders if they don't exist.
2. **Find the latest handoff for this branch** — list
   `docs/sessions/handoff/<branch-slug>/`, sort by filename, read the last one. If
   that folder is empty (new branch), fall back to the single most-recent handoff
   across all branch folders for continuity, and note that this is the first
   tracked session on this branch.
3. **Read the backlog** — `docs/sessions/TODO.md` (the project to-do list, rendered
   as the control center's "To-do" panel). Note any open items touching this
   session's focus; they carry the notes meant to inform this round.
4. **Determine the session number** — check
   `docs/sessions/progress/<branch-slug>/` for today's date. If files exist for
   today (e.g., `2026-06-05-S03-...`), the next session is S04. If none exist for
   today, start at S01.
5. **Get the session focus** — use `$ARGUMENTS` if provided, otherwise ask the user
   (one sentence).
6. **Orient in the repo** — note which **app** (`src/animations/<Name>/`) the focus
   names, if any. Skim `CLAUDE.md` / `AGENTS.md` for any conventions relevant to the
   focus, and read **`docs/sessions/RECIPES.md`** — the if-this-then-that cookbook of
   habits worth making reflexive (verify visual changes, pin scope before building,
   real checks, test pure logic); keep its **WHEN** triggers in mind as you work.
   Remember the parallel-branch rule: shared files (`src/index.tsx`,
   `src/apps.ts`, `CLAUDE.md`, `README.md`) are **append-only** — never reorder
   existing entries. **Do not `git pull` / `merge origin/main` to start** — the
   fresh clone is already current, and this branch may be stacked on another
   feature branch (see CLAUDE.md → *Branch sync*). Main-sync happens only at PR
   finalization.
7. **Create the progress report** at
   `docs/sessions/progress/<branch-slug>/YYYY-MM-DD-SNN-description.md` by copying
   `docs/sessions/_template-progress.md` and filling the `[bracketed]` frontmatter
   and sections (see structure below).
8. **Present a summary** of the last handoff: status, what was done, what's pending.
   Include the **live-preview links** (see below). Then wait for the user to direct
   what to work on.

## Continuity

The latest handoff may or may not be directly relevant to this session. When
presenting the summary:

- If the session focus clearly continues from the handoff, highlight the pending
  items and recommended next steps.
- If the session focus is a **new topic** unrelated to the latest handoff, say so.
  Briefly note the handoff status (so nothing is lost), then focus the summary on
  orienting for the new topic instead.
- If the user's message provides additional context beyond the focus (e.g., "I'm
  not picking up from the handoff" or "this is about something different"), respect
  that framing.

## Progress Report Structure

Copy `docs/sessions/_template-progress.md` and fill it in. The full spec is
`docs/sessions/REPORT_STYLE.md`; the essentials:

- **Frontmatter** (YAML) carries the metadata the cross-branch control center
  indexes — keep `status`/`build`/`pr` accurate as the session progresses. `slug`
  must match the folder name (it is the report's provenance).
- **Working notes = the timeline.** Each state transition is one `###` entry,
  **newest first**, with the heading formatted exactly:
  `### <emoji> <type> · HH:MM — <what>` where `type ∈ decision | code | finding |
  blocker | milestone` and the emoji is 🟣 decision · 🟢 code · 🔵 finding ·
  🔴 blocker · 🟡 milestone. Follow it with a `**Why:** …` line, then body.
  The renderer turns this section into the rich timeline rail.
- **Callouts** use GitHub alerts: `> [!NOTE]` / `[!TIP]` / `[!IMPORTANT]` (decision)
  / `[!WARNING]` (warn) / `[!CAUTION]` (gotcha).
- **Sections** are `##` headings; the TOC builds itself in the rendered view.

Write plain, readable Markdown — it renders on GitHub as-is, and `npm run sessions`
generates the rich HTML (timeline rail, scroll-spy TOC, styled callouts).

## Live preview (while on a branch)

GitHub Pages only deploys from `main`, so a branch's reports aren't on the deployed
site. Two ways to view this session's report:

- **GitHub native** (quick read): `https://github.com/piyarsquare/animath/blob/<branch>/docs/sessions/progress/<branch-slug>/<file>.md`
  (commit + push first). Use the full branch name.
- **Rich render + cross-branch control center**: run `npm run sessions` (after
  `git fetch --all`) to (re)generate `docs/sessions/converted/**` and
  `docs/sessions/control-center.html`, then open the control center — it aggregates
  every active branch's reports (Cards · Timeline · **Reflections** views, a `#cat=`
  category filter, and a link out to the embed demo). The **Reflections** view is an
  exit-interview digest built from each report's `## Self-reflection` section — a fast
  way to scan prior sessions' follow-up flags. Surface these in the step-7 summary.

## Progress Report Rule

**After every state transition: write. After every write: state why.** A state
transition is any change in what the agent is doing — responding to the user,
switching subtasks, finishing a read and starting a write, dispatching a sub-agent,
receiving results. Not just user-facing exchanges; internal transitions count. Both
the write and the why are unconditional. The progress report is the audit trail. If
it wasn't written, it didn't happen.

## Rules

- **The progress report is the memory of the session.** When this context is
  discarded, the progress report is all that remains. Future agents — and the user —
  will rely on it to understand what happened, what was decided, and why. Without
  the Why, the record is incomplete and decisions become unauditable.
- Do NOT begin any implementation, investigation, or code changes.
- Do NOT `git pull` or merge `origin/main` during startup — begin from the branch
  as checked out. Syncing `main` happens only when finalizing a PR, and only for
  branches that target `main` (stacked branches sync their own base). See
  CLAUDE.md → *Branch sync*.
- Do NOT run scripts or explore the codebase beyond resolving the branch slug,
  reading the handoff, and the orientation skim in step 5.
- After presenting the summary, STOP and wait for the user to direct next steps.
- The description in the filename should be lowercase-hyphenated, 2–5 words, derived
  from the session focus.
