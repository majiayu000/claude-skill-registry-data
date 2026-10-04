---
name: start-session
description: Begin a bracketed learning session inside a agentic-study-environment sub-project — pick a topic, propose theory vs. practice (or an overlay-specific type such as simulation or defense), and conduct it per the sub-project's domain overlay. Use whenever the user signals they want to actively study, work an exercise, role-play a clinical case, rehearse a research defense, or review theory inside a sub-project — phrases like "start session", "let's work on X", "begin a practice session", "ok let's study Y", or "I want to do an exercise on Z" should trigger this skill. A session is the harness's unit of work and ends with the stop-session skill.
---

# Start a learning session

This skill begins a bracketed session inside a learning sub-project. A session is the unit of work in the harness: it has a start (this skill), a focus (one topic, one session type), and an end (`stop-session`). Progress is recorded at session end.

## When to use

The user wants to actively study something. They might say "start session", "let's work on TASEP", "begin a practice session on derivatives", or just "I want to do an exercise on Y". Anything that signals "tutor me through a topic now" should match.

If the user has not bootstrapped a sub-project yet, redirect them to the `bootstrap` skill first.

## What to read before doing anything else

Before proposing or conducting anything, load context:

1. The harness's optional `.studyenv/AGENTS.md` if present, otherwise `.studyenv/CLAUDE.md` if present (for cross-project conventions and any global `Language:`), and `.studyenv/PROGRESS.md` (created by `bootstrap` on first use). Both are optional context; if either is missing, continue without it. Everything the harness generates lives under `.studyenv/` — the host project's own files are not read or modified.
2. The sub-project's `.studyenv/<name>/AGENTS.md`, falling back to `.studyenv/<name>/CLAUDE.md` for older projects (for `Domain:`, `Language:`, goals, Tools & Materials), and `.studyenv/<name>/PROGRESS.md` (for what's been covered and at what status).
3. The sub-project's `.studyenv/<name>/ai-agent-materials/` — especially `curriculum.md` and any concept maps / excerpts. If there are unanalyzed items in `.studyenv/<name>/source-materials/`, analyze them now and write the intermediate representations into `ai-agent-materials/` before proposing a route.
4. If the sub-project declares `Domain:`, load the matching overlay at `../../domains/<domain>.md` (relative to this SKILL.md). The overlay refines the generic rules in this skill — it does **not** replace them. If no `Domain:` is set, or `Domain: study`, no overlay applies and the neutral defaults stand.

This up-front read is what makes the agent feel like a continuing tutor instead of a stateless responder. Without it, every session restarts from zero.

## Decide session type

Sessions focus on **one** of four core **types**, though a theory session may include some grounding practice and a practice session may include some motivating theory. Overlays don't add types — they supply domain-specific *flavors* of these (see `../../reference/conventions.md` → *Session types vs. flavors*):

- **`theory`** — concept discussion, definitions, intuitions, proofs/derivations on request.
- **`practice`** — work an exercise grounded in the current theory topic; the agent prepares scaffolding (the active overlay specifies the form), the user implements, the agent reviews and pushes deeper.
- **`role-play`** — an in-character session: setup out of character, role-play in character, debrief out of character. Available when the active overlay flavors it — `simulation` (`speech-therapy`: agent = patient), `defense` (`academic-research`: agent = examiner), `review` / `interview` (`coding`: agent = reviewer / interviewer). Generic protocol in `../../reference/conventions.md` → *Role-play session protocol (generic)*; the overlay fixes the role, whose work is scrutinized, and the debrief rubric.

A fourth core type, **`onboarding`** — a guided walkthrough of an existing artifact you didn't author (a codebase, a document corpus, a body of papers) — has its own dedicated skill, `onboard-session`, rather than being proposed here. If the user wants to get up to speed on something they didn't write, redirect to `onboard-session`.

## Propose a route

Look at `PROGRESS.md` and `curriculum.md`. Propose:

- which **topic** to work on (cite topic id from the curriculum where it exists)
- which **session type** to run
- a one-sentence **why now** — does it advance the next prerequisite? Reinforce a topic that's `introduced` but not yet `exercised`? Stress-test something fragile from last session?

The user may override. Do not start the session until they accept (explicitly or implicitly by engaging with the proposed topic).

## Conduct the session

Once route is set, run the session per type. The active domain overlay (if any) refines the shape:

- **Scaffolding form** — what materials/files the agent prepares for the user to work on. Without an overlay, default is a `work/<exercise-name>.md` file with prompt, success criteria, and any reference excerpts inline.
- **Review focus** — what the agent attends to when reviewing the user's output. Without an overlay, defaults are concept correctness and clarity.
- **`/work/` layout** — where artifacts go. Without an overlay, default is a flat folder of markdown files. Code-shaped layouts (CMake, pyproject) come from `../../domains/coding.md`; case-folder layouts come from `../../domains/speech-therapy.md`; flavored research layouts (per-manuscript and per-defense folders) come from `../../domains/academic-research.md`.

Teaching style across all types: **theory-first with explicit examples, definitions and intuitions before proofs, proofs on request**. Concise. Push deeper after the user's first pass — alternative implementations, edge cases, idiomatic alternatives, missed dimensions, the kind of thing a sharp tutor would flag.

**Honor external-source labels.** The curriculum's source entries distinguish in-source material from `[ext]`-labeled external material (see `../../reference/conventions.md` *External-source labeling*). When teaching a topic whose primary source is external, **say so up front** — *"this part comes from Krapivsky et al., ch. 7, not from your paper"* or *"this is general probability background, not from your source"*. The user always gets to know whether they're studying their own material or something the agent brought in.

## Language

Reply in the conversational language declared by the active `Language:` field (BCP 47 tag). Sub-project `Language:` overrides the global `.studyenv/AGENTS.md` setting. If unset, default to English. Code identifiers, file names, scaffolding stub files and their instructional comments, status legends, field names, trigger words, and verbatim source excerpts stay in their original language regardless of the setting — see `../../reference/conventions.md` for the exact rules.

## Why these rules

- Loading PROGRESS.md and curriculum.md up front is what makes the agent feel like a continuing tutor instead of a stateless responder.
- Domain overlays are additive (not replacement) so the generic core remains predictable across domains, with only the truly domain-specific bits (scaffolding form, review focus, work layout) varying.
- Proposing a route and letting the user override is the right power balance: the agent does the planning load, the user keeps editorial control.

## Ending the session

When the user signals they're done — "stop session", "wrap up", "end session", or similar — invoke the `stop-session` skill. It handles `PROGRESS.md` updates and the summary.

## Related skills

- `bootstrap` — mint a new sub-project.
- `set-curriculum` — build or update the teaching plan.
- `onboard-session` — the dedicated skill for `onboarding` sessions (getting up to speed on an artifact you didn't author).
- `stop-session` — record progress and summarize at session end.
