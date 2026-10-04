---
name: brain-sync
description: Keeps a living knowledge base in /brain synchronized with the real state of the codebase. Use this skill whenever code is created, edited, moved, renamed, or deleted — after finishing a feature, fix, or refactor, or whenever the user asks to "sync the brain," "update the docs," "atualizar o brain," or similar. Also trigger it proactively at the end of any coding task before considering it done, even if the user didn't explicitly ask for documentation. Do not trigger it for purely cosmetic changes (whitespace, formatting) with no semantic impact.
---

# brain-sync

## Why this exists

Codebases drift from their documentation almost immediately — someone renames a function, adds a dependency, or changes a contract, and the docs quietly go stale. `/brain` is meant to be the opposite of that: a second brain for the project that a human or an AI agent can read *instead of* re-reading the whole codebase to understand what something does, why it exists, and what depends on it. That's only useful if it's actually kept current, so this skill treats "update /brain" as part of finishing a change, not an optional extra step.

The goal isn't to produce more documentation — it's to keep a small, trustworthy set of documents that never lie about the current state of the code.

## When to use this

Use this skill:
- Right after code has been created, modified, moved, renamed, or deleted
- At the end of any development task (feature, bugfix, refactor), before calling it done
- When explicitly asked to "sync the brain" / "atualizar o brain" / "update the docs"

Skip it for:
- Pure formatting/whitespace changes with no semantic effect
- Exploratory edits that were reverted before the task ended
- Changes inside `/brain` itself (don't recursively document the documentation)

## The `/brain` structure

Always use this layout. Don't invent a new convention per run — consistency is what makes `/brain` navigable over time.

```
/brain
  INDEX.md                        <- entry point, links to everything below
  modulos/
    <modulo>.md                   <- one file per module/service/major component
  componentes/
    <componente>.md                <- classes/functions worth documenting individually
  dependencias/
    mapa.md                        <- current dependency graph between modules
  decisoes/
    <YYYY-MM-DD>-<slug>.md         <- ADR-style record of a technical decision
  mudancas/
    CHANGELOG.md                   <- append-only log of each sync
```

If the project already has a `/brain` with a different structure, follow the existing one instead of imposing this — the point is consistency, not this exact layout.

## Process

Work through these steps in order. Steps 1–2 are about understanding what changed; steps 3–7 are about reflecting that change in `/brain` with minimal disruption to what's already there.

### 1. Detect what changed

Prefer `git diff` / `git status` against the last synced commit when git is available — it's the most reliable source of truth. If there's no git history to compare against, compare the current file tree and contents to what's already documented in `/brain/modulos/*.md` and infer the delta from there.

Collect: files added, files modified, files removed, files moved/renamed.

### 2. Classify the impact of each change

For each changed file, decide what kind of change it is — this determines what needs updating:

- **New module/component** → needs a new doc
- **Behavior change** (logic changed, same interface) → update the module doc's description, leave dependency map alone unless imports changed
- **Interface/contract change** (function signature, API shape, exported members) → update the module doc AND check if anything documented as a dependent is now stale
- **Pure refactor** (moved code, same behavior and interface) → update file paths/references only
- **Removal** → don't just delete the doc; see step 7

Don't treat every diff as equally significant. A one-line change to a log message doesn't need the same documentation effort as a new exported function.

### 3. Find or create the matching document

Before creating a new file, search `/brain` for an existing document about that module or component — grep by filename, by module name, and by any obviously related terms. Reusing and updating an existing doc is always preferable to creating a near-duplicate.

- **Exists** → update only the sections affected by the change. Don't regenerate the whole file from scratch; that erodes any hand-written context a human previously added (rationale, gotchas, links).
- **Doesn't exist** → create it in the right subfolder using `assets/module_template.md` as the starting structure.

Each module/component doc should answer, briefly:
- What is this responsible for?
- What does it depend on, and what depends on it?
- Any non-obvious decisions or gotchas a newcomer would otherwise have to rediscover the hard way?

Prefer capturing *why* a change was made over restating *what* changed line-by-line — the diff already shows the "what."

### 4. Update the dependency map

If the change added, removed, or altered a relationship between modules (a new import, a new call into another service, an integration point going away), reflect that in `/brain/dependencias/mapa.md`. Keep this as a simple, scannable list or table of `A depends on B` relationships rather than prose — it's meant to be skimmed, not read top to bottom.

### 5. Record a decision, if this was one

If the change reflects a real architectural choice (new library adopted, pattern changed project-wide, a trade-off deliberately accepted), add an entry under `/brain/decisoes/`. Not every change warrants this — only ones where someone six months from now would reasonably ask "wait, why did we do it this way?"

### 6. Log the sync

Append one entry to `/brain/mudancas/CHANGELOG.md`: date, one-line summary of what changed in the code, and links to whichever `/brain` files were touched. This file is append-only — never rewrite past entries.

### 7. Handle removals and check for orphans

If code was deleted, don't leave its doc silently describing something that no longer exists. Either:
- Delete the doc and remove its links from `INDEX.md` and `mapa.md`, or
- If the removal is itself noteworthy (a module was deprecated on purpose), move a short note to `/brain/decisoes/` explaining what replaced it, then remove the module doc.

Before finishing, scan `/brain` for links or mentions pointing at files/modules that no longer exist and fix or flag them — a `/brain` full of broken links is worse than no `/brain` at all, since it actively misleads whoever reads it next.

### 8. Update the index

Make sure `INDEX.md` links to every file that currently exists under `/brain` and to nothing that doesn't. This is the map of the map — it should always be trustworthy even if someone only has 30 seconds to look something up.

## Principles for what you write

- **Explain the why, not just the what.** "Uses Redis for session storage" is less useful than "Uses Redis for session storage because sessions need to survive across the horizontally-scaled API instances — see decisoes/2026-03-uses-redis.md."
- **Don't duplicate.** If something is already documented elsewhere in `/brain`, link to it instead of restating it. Duplication is how documentation quietly diverges from itself.
- **Update incrementally.** Never regenerate a whole document from scratch when only part of it is affected — you'll likely discard useful hand-written context that a human added.
- **Be concise.** A module doc that takes 3 minutes to read will get skipped next time. Say what matters, link for depth.
- **When in doubt about scope, under-document rather than pad.** A short accurate doc beats a long generic one that restates the obvious ("this file contains functions").

## Definition of done

Before considering a sync complete, check:
- [ ] Every changed file has a corresponding up-to-date entry somewhere in `/brain` (or a deliberate decision not to document it, e.g. trivial internal helper)
- [ ] `dependencias/mapa.md` reflects any new/removed relationships from this change
- [ ] `mudancas/CHANGELOG.md` has a new entry for this sync
- [ ] No document in `/brain` references code, files, or modules that no longer exist
- [ ] `INDEX.md` links to everything current and nothing stale

## Example

**Change detected:** new file `src/services/authService.js` implementing OAuth login; `src/services/userService.js` modified to call it.

**Resulting sync:**
- New file `/brain/modulos/auth-service.md` — describes responsibility (handles OAuth login flow), the provider/library used, and any config it expects
- `/brain/dependencias/mapa.md` — new row: `authService -> userService`
- `/brain/modulos/user-service.md` — updated: note that it now receives authenticated user data from `authService` instead of handling credentials itself
- `/brain/mudancas/CHANGELOG.md` — new entry: `2026-07-19 — Added OAuth login via authService, refactored userService to consume it — see modulos/auth-service.md, modulos/user-service.md`
- `/brain/INDEX.md` — updated with the new link to `auth-service.md`

Use `assets/module_template.md` as the starting point whenever creating a new module doc.
