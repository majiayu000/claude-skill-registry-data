---
name: set-curriculum
description: Build or update the teaching curriculum for a learning sub-project from its source materials. Use whenever the user wants to plan, structure, or refresh the learning path for a sub-project — phrases like "set curriculum for X", "update the curriculum", "plan the teaching path", "build a curriculum from these materials", or general intent to organize source material into an ordered teaching plan. This skill reads the sub-project's source materials and writes ai-agent-materials/curriculum.md. It does not start a session and does not update PROGRESS.md.
---

# Set or update a sub-project's curriculum

This skill builds the teaching plan for a learning sub-project. The curriculum is a **reference document** the agent consults when proposing what to study next — it does not force the order, but it makes the route through the material explicit and reviewable.

## When to use

The user has bootstrapped a sub-project (via the `bootstrap` skill) and dropped source materials into `.studyenv/<name>/source-materials/`. They want to organize that material into an ordered teaching plan. Phrases: "set curriculum for tasep", "update the curriculum for spanish-b2", "plan how we should work through these papers".

This skill is **not a session** — it does **not** update `PROGRESS.md`. It only writes the curriculum file.

## What you need from the user

**Required:**

- The **sub-project name** to act on. If the user did not name one, **ask** — never default to "all sub-projects" or guess.

If multiple sub-projects exist in the harness, prefer asking over assuming.

## What to read

Before writing or updating the curriculum, load context:

1. The sub-project's `.studyenv/<name>/AGENTS.md`, falling back to `.studyenv/<name>/CLAUDE.md` for older projects — for `Domain:`, `Language:`, learning goals, and Tools & Materials.
2. The harness conventions at `../../reference/conventions.md` — for the curriculum format and status legends.
3. The sub-project's `.studyenv/<name>/ai-agent-materials/` — especially any existing `curriculum.md` and source extractions (concept maps, copied excerpts).
4. The sub-project's `.studyenv/<name>/source-materials/` — the canonical source content.

If `.studyenv/<name>/ai-agent-materials/` does not exist, create it. Concept maps and excerpts are added here over time; this skill primarily writes `curriculum.md`.

## What to write

Render or update `.studyenv/<name>/ai-agent-materials/curriculum.md` with the structure documented in `../../reference/conventions.md` (Curriculum format section):

- An **overview** paragraph — what this sub-project teaches and the intended end state.
- A **topics** section: an ordered list of topic entries, each with
  - a stable **id** (`T1`, `T2.a`, …) so `PROGRESS.md` can cross-reference
  - a one-line **description**
  - **prerequisites** (other topic ids; `none` if root)
  - suggested **session type** — one of the four core types `theory`, `practice`, `role-play`, `onboarding` (or `both` for theory + practice). `theory`/`practice`/`role-play` are run via `start-session`; `onboarding` via the dedicated `onboard-session` skill. Where the active overlay flavors `role-play`, the curriculum may name the flavor — `simulation` (`Domain: speech-therapy`), `defense` (`Domain: academic-research`), `review` / `interview` (`Domain: coding`). See `../../reference/conventions.md` → *Session types vs. flavors*.
  - **source references** — page numbers, section anchors, URLs
  - **exercise hooks** — short outlines of proposed practice/theory exercises; the actual exercise artifacts live in `work/`, created at session time per the active domain overlay.

If `curriculum.md` already exists, **update** rather than overwrite:

- Integrate any newly added source materials.
- Fold in user-provided corrections or additions.
- Re-check dependencies and ordering.

The curriculum is **reference-only**. It does not constrain `start-session` or `onboard-session` — the agent may consult it when proposing a route, but is free to deviate.

## Stay source-faithful; label any departures

This skill produces a **source-faithful** curriculum by default — every topic should be traceable to the user's `source-materials/`. If the source assumes a prerequisite it doesn't itself cover, you have two options: (a) name the prereq as a gap to fill at session time and don't add a curriculum topic for it, or (b) add a short bridging topic and label it `[ext]` per the *External-source labeling* rules in `../../reference/conventions.md`. **Do not silently weave training knowledge into a curriculum that's supposed to track the user's source.** If the user wants a curriculum that genuinely shifts level (simpler / more advanced), they should use `adjust-level` instead, which is explicitly built for that.

## Source-material handling

When extracting material from sources, build intermediate fixed representations under `.studyenv/<name>/ai-agent-materials/` alongside `curriculum.md`:

- **Terse concept maps** — with references back to the source (page numbers for PDFs, section/heading anchors or URLs for other formats).
- **Copied verbatim excerpts** — sections, examples, definitions for explicit use during sessions. Keep these in the source's original language regardless of the sub-project's `Language:` setting.

Do **not** duplicate exercise content here; the curriculum's exercise hooks point at `work/`, but `work/` is populated at session time by `start-session`.

## Why these rules

- The curriculum is the explicit teaching plan, separate from `PROGRESS.md` (which tracks what's been done). Splitting plan from progress lets the user revise the plan without rewriting history.
- Topic ids are stable identifiers so `PROGRESS.md` can record `T1: exercised` without restating the topic description — and so reordering the curriculum doesn't break those references.
- Updating rather than overwriting matters when the user has been corresponding about plan revisions; the existing curriculum may carry their edits.

## Related skills

- `bootstrap` mints the sub-project.
- `start-session`, `onboard-session` consult the curriculum (among other inputs) when proposing what to study next.
