---
name: scaffold
description: Bootstrap a greenfield project — git init, the full convention folder skeleton, and a CLAUDE.md contract. Lays structure only and makes no design decisions; the stack and commands are left as pending fields for architect to fill. Run once at the start.
version: 1.0
---

## Contract terms — read first

Before anything else, read your slice of the Plumbline contract at **`${CLAUDE_PLUGIN_ROOT}/terms/scaffold.md`** — generated from the root `TERMS.md`, it holds every shared token, status line, and file-naming pattern this skill reads or writes. Reproduce them **verbatim**. **If you cannot load it, stop and report; do not guess the contract.**

---

## When to use this skill
- Starting a **greenfield** project — one you're committing to from the start, with no `Planning/` structure yet.

**Not for adopting an existing project.**  scaffold assumes a clean start.
Run once. If a partial structure already exists, scaffold fills only what's missing — it never overwrites your files.

---

## What it creates

`scaffold` lays the **full convention skeleton** up front (empty folders are guide-rails) and
writes the contract. The split: **`Planning/` = human intent (specs, reference) · `Plumbline/` = everything the workflow generates** (blueprints, decisions, reports). Code lives wherever the stack puts it, outside both.

**Folders:**
- `Planning/specs/` — specs (the single source of truth)
- `Planning/reference/` — shared definitions specs cite (data models, constants); fills as specs need it
- `Plumbline/` — everything the workflow generates. Its subfolders are laid up front as guide-rails, each filled by the skill that owns it:
  `Plumbline/blueprints/` (foreman), `Plumbline/decisions/` (architect; append-only, see **Change rules** in CLAUDE.md, Full Path), `Plumbline/inspect/` (inspector), `Plumbline/deviations/` (builder), `Plumbline/surveys/` (surveyor), `Plumbline/walkthrough/` (walkthrough), `Plumbline/homeowner/` (homeowner run logs).

**History mode — git by default.** In **git** mode (the default) every project starts in git:
`git init` plus a sensible `.gitignore` and a first commit of the skeleton; the git log *is* the
history, no separate changelog. In **none** mode (only when the caller asks for a no-git project)
scaffold skips every git step and history is the dated artifact trail instead (see the contract's
`## History`). Default to **git** unless told otherwise.

Do **not** create: `specs/archive/` (git or in-place edits handle spec history), a `tools/`
folder (walkthrough makes it lazily), `Plumbline/architecture.md` (written only once modules need a
map), or a spec template (the spec format lives in `architect`).

**Files:**
- `CLAUDE.md` — the project contract, from `${CLAUDE_PLUGIN_ROOT}/skills/scaffold/contract-template.md` (created only if missing).

---

## Step 1 — Check what exists

List the project root. If there's already substantial code, a `CLAUDE.md`, or a legacy doc pile,
**stop and ask the user if they really want to scaffold** — it's meant for greenfield projects.

Otherwise note each folder/file below as present vs. missing. Never overwrite an existing file.
If everything already exists, report that and stop.

---

## Step 2 — Create folders (and init git in git mode)

Create any missing folders from the **What it creates** list above.

**Empty folders and git.** Git does not track empty directories, so in **git** mode drop a `.gitkeep` file in each folder that is still empty — that keeps the guide-rail skeleton in the first commit and on a fresh clone. Write each `.gitkeep` as a **single purpose line** rather than an empty file, so the folder documents itself to anyone who opens it cold:

```
Planning/specs/ — specs, the single source of truth for behavior. Written by architect.
Planning/reference/ — shared definitions specs cite. Filled as specs need it.
Plumbline/blueprints/ — per-feature build plans. Written by foreman.
Plumbline/decisions/ — why a non-obvious choice was made. Append-only. Written by architect.
Plumbline/inspect/ — proof reports. Written by inspector.
Plumbline/deviations/ — deviation logs. Written by builder.
Plumbline/surveys/ — drift reports. Written by surveyor.
Plumbline/walkthrough/ — walkthrough logs + recommendations. Written by walkthrough.
Plumbline/homeowner/ — run logs. Written by homeowner.
```

The `.gitkeep` stays when real output arrives — it is the folder's label, not just a placeholder. In **none** mode the folders simply exist on disk with no `.gitkeep`; the contract's "Where things live" table is the routing there.

**git mode (default):** if the project isn't already a git repository, `git init`, write a
**generic** `.gitignore` (OS/editor cruft and common ignores — the stack isn't decided yet, so
don't tailor it; architect or a later change appends stack-specific lines), and make the first
commit once `CLAUDE.md` is written (Step 3). Git is the project's history from day one — decisions
still go to `Plumbline/decisions/`, but "what changed when" lives in the log.

**none mode:** skip git entirely — no `git init`, no `.gitignore`, no commit. The folder skeleton
and the dated artifacts are the project; history is the trail under `Plumbline/`.

---

## Step 3 — Write CLAUDE.md

Create `CLAUDE.md` from **`${CLAUDE_PLUGIN_ROOT}/skills/scaffold/contract-template.md`** (the canonical contract — do not
re-invent it inline). Fill **only the fields that need no design decision:**
- **Project name** and the **one-line identity** — from the brief / folder name (architect refines if thin).
- **Shell/OS** — the environment you're running in (e.g. PowerShell on Windows).

**Leave Stack and Commands as their `[pending — architect]` placeholders, and do not add the
UI evidence line.** Scaffold makes no stack or command decisions: those are consequences of *what*
gets built, which architect settles when it writes the first spec. Don't guess them — a placeholder
that architect fills is correct; a guessed command that inspector later can't run is not.

If `CLAUDE.md` already exists, append only missing sections — never touch existing content.

Set the contract's `## History` **Mode:** line to the chosen mode — `git` by default, `none` if the
caller asked for a no-git project.

**git mode only —** finish with the first commit: the skeleton plus `CLAUDE.md`, message like
`Scaffold: project skeleton + contract (Plumbline v1.0)`. In `none` mode there is nothing to
commit; the files on disk are the record.

---

## Step 4 — Report

List what was created vs. already present, and note that the contract's Stack/Commands are pending. Then tell the user:

1. Run **architect** to write the first spec — it also **fills the pending Stack and Commands** in CLAUDE.md (and owns the `**Done when:**` format).
2. Run **foreman** to generate the blueprint from the spec.
3. Run **builder** slice by slice.
4. Run **inspector** to prove the "Done when" items are met.

