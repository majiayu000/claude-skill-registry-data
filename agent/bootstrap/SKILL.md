---
name: bootstrap
description: Scaffold a new learning sub-project under the agentic-study-environment harness — create the directory, generate per-project AGENTS.md, CLAUDE.md, and PROGRESS.md from templates, and register the new project in the .studyenv/PROGRESS.md cross-project tracker. Use this skill whenever the user wants to start studying a new topic, paper, book, language, or domain with the tutor harness — phrases like "bootstrap a new project to learn X", "start a new sub-project for Y", "set up a learning project on Z", or "create a sub-project to study W" should all trigger this skill. Do not use for general project scaffolding outside the agentic-study-environment harness.
---

# Bootstrap a learning sub-project

This skill mints a new sub-project under the agentic-study-environment harness. A sub-project is a self-contained folder where a learner works through a single topic with the agent as tutor, scaffolded by the harness's conventions.

## When to use

The user wants to start studying something new. They might say "bootstrap a project to learn TASEP", "create a sub-project for Spanish vocabulary", "set up a learning project for the seam carving paper", or similar. The signal is: a topic they want to learn, an intent to study it under the harness.

This skill does NOT run a teaching session — that's `start-session`. It only sets up the scaffolding.

## What you need from the user

**Required (ask if missing — do not invent):**

- a **sub-project name** (becomes the directory name, e.g. `seam-carver`, `spanish-b2`, `tasep`)
- a **one-line learning goal** that captures what the user wants to learn

**Optional (use if supplied; do not prompt for them — they can be filled later via the sub-project's `AGENTS.md`):**

- a **Domain** — controls which overlay applies during sessions. Known values: `coding`, `speech-therapy` (synonym: `logopedics`), `legal-documents` (synonyms: `official-documents`, `public-documents`), `academic-research` (synonyms: `research`, `scholarship`), `study` (the neutral default), or any user-supplied custom value. If unset, the sub-project falls back to the neutral default.
- a **Language** — BCP 47 tag (e.g. `de`, `es`, `fr`) overriding the conversational language for chat replies inside this sub-project. Default is English unless an optional `.studyenv/AGENTS.md` (or `.studyenv/CLAUDE.md`) sets otherwise. Structural tokens (status legends, field names, trigger words) stay in English regardless — see `../../reference/conventions.md` for the exact rules.
- **Tools & Materials** — anything the user already knows they'll work with (a language + version for coding, a textbook, a notation convention, …).
- **Tracking** — `global` (default) or `local-only`. `global` registers the sub-project in the cross-project `.studyenv/PROGRESS.md` tracker (the umbrella mode). `local-only` keeps just the sub-project's own `PROGRESS.md` and skips the cross-project tracker entirely — for a lone learning project where no global index is wanted. Default to `global` when unstated; do not prompt. See `../../reference/conventions.md` → *Tracking scope*.
- A note that **source materials are already in place** — controls the starting status of the sub-project.

## Refuse to overwrite

If `.studyenv/<sub-project-name>/` already exists, **stop and ask the user**. Never overwrite an existing sub-project. If the user wants to wipe and start over, they can delete the directory themselves and re-invoke. A sub-project may carry weeks of work in its `PROGRESS.md` and `work/` — silent overwrite would be destructive.

## What to create

Everything the harness generates lives under `.studyenv/` at the current working directory (the host project root). Create `.studyenv/` if it does not yet exist, then create:

1. **`.studyenv/<name>/`** — the sub-project directory.
2. **`.studyenv/<name>/source-materials/`** — empty placeholder for the user to drop PDFs, notes, links, prepared code projects.
3. **`.studyenv/<name>/AGENTS.md`** — render from `../../templates/sub-project-agents.md` (relative to this SKILL.md). Substitute `<name>`, the learning goal(s), and any supplied `Domain:` / `Language:` / Tools & Materials. If `Domain:` was not supplied, **omit the line entirely** (do not leave a blank or a placeholder string). Same for `Language:`. If `Tracking: local-only` was requested, write that line; otherwise (the `global` default) **omit the `Tracking:` line**. If Tools & Materials were not supplied, keep the placeholder text `TBD when setting curriculum`.
4. **`.studyenv/<name>/CLAUDE.md`** — render from `../../templates/sub-project-claude.md`. It is a compatibility pointer to `.studyenv/<name>/AGENTS.md`.
5. **`.studyenv/<name>/PROGRESS.md`** — render from `../../templates/sub-project-progress.md`. Status opens at `created`, or at `ready` if the user mentioned source materials are already in place.

**Do NOT create** `.studyenv/<name>/ai-agent-materials/` or `.studyenv/<name>/work/`. The `set-curriculum` skill creates `ai-agent-materials/`; sessions create `work/` on demand per the active domain overlay.

## Update the cross-project tracker (`.studyenv/PROGRESS.md`)

**If `Tracking: local-only` was requested, skip this entire section** — do not create or register `.studyenv/PROGRESS.md`. The sub-project's own `PROGRESS.md` is its only tracker (see `../../reference/conventions.md` → *Tracking scope*).

Otherwise (the `global` default), after creating the sub-project, register it in the cross-project tracker at `.studyenv/PROGRESS.md`. Because `.studyenv/` is harness-owned, this file is always either the harness tracker or absent — there is no foreign file to collide with and no shape to detect.

The tracker structure (a `# PROGRESS.md — studyenv` heading, a `## Projects` table, `## Grand Topics Covered`, and `## Journal`) is documented in `../../reference/conventions.md` → *`.studyenv/PROGRESS.md` structure*.

- **If `.studyenv/PROGRESS.md` does not exist** (first bootstrap in this host), create it from the canonical structure, then add this sub-project's row and Journal entry.
- **If it exists**, append the row and dated Journal entry **without touching prior rows or entries**.

The Projects row uses the matching status (`created` or `ready`) and a one-line note (typically the learning goal, abbreviated); the Journal gets an entry under today's date describing the bootstrap.

Whatever the outcome, the sub-project directory (`.studyenv/<name>/`) is already created and self-contained — its own `PROGRESS.md` is the source of truth; the tracker is only an index.

## Confirm and prompt for materials

After scaffolding is in place:

- Tell the user concisely what was created (paths, opening status). For `local-only`, note that the sub-project is self-tracked and was **not** registered in a cross-project tracker.
- **Prompt the user to drop source materials into `.studyenv/<name>/source-materials/`** — PDFs, papers, links, prepared code projects, exercise sheets, anything.
- If the user supplies materials in the same turn (or confirms they've already added some), flip the sub-project's `PROGRESS.md` Status line from `created` to `ready` — and the `.studyenv/PROGRESS.md` Projects row too, unless this is a `local-only` sub-project (which has no Projects row).

## Why these rules

- The harness is structural — every sub-project follows the same layout so the agent can navigate any of them without re-learning the conventions. The templates enforce that.
- Everything generated goes under `.studyenv/` so the harness footprint is fully contained and portable — the host project stays clean, and the whole study environment can be gitignored, deleted, zipped, or synced as one folder. The harness never touches the host's own root files.
- Domain and Language stay **optional and omitted-when-unset** rather than written as placeholders, because the agent uses presence/absence of those fields at session time to decide whether to load an overlay or switch conversational language. A placeholder string would falsely trigger.
- `ai-agent-materials/` and `work/` are deliberately not created here. Bootstrap should be cheap and reversible; the heavier folders appear when their work actually begins.
- `Tracking: local-only` exists so the harness can be dropped onto a single existing project as a lone learning unit without spinning up (or polluting) a cross-project index. It's the opt-out from the umbrella; `global` stays the default so the common multi-sub-project case needs no flag.

## Related skills

- After bootstrap, the user typically runs `set-curriculum` once source materials are in place, then `start-session` (or `onboard-session`, for getting up to speed on an existing artifact) to actually study.
- `stop-session` updates the per-project `PROGRESS.md` and `.studyenv/PROGRESS.md`.
