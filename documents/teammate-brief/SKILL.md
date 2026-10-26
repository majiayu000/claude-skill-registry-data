---
name: teammate-brief
description: Write an onboarding document for a person joining or picking up a project — what it is, setup steps verified by running them, env var names and where to get them, tasks with "done when", owners, don't-touch list. Use for "brief my teammate", "onboarding doc for X", "hand this project to someone".
argument-hint: "[teammate name or role]"
---

One Markdown file for a human reader, in plain language: "run this command", not "invoke"; no skill or session jargon. **Gate**: commit only if the `handoff-auto` skill's `TRACKING.md` allows it, only on `<default>` (defined there; protected → its docs branch `docs/brief-<name-slug>`, "Protected `<default>`" there), and on the user's yes; push needs its own yes; sharing the file is the user's call.

## 1. Ask (one batch, each with its default)

1. **Who** (default: the person just named, else "the next person on this"; file-name slug `teammate` when no name).
2. **Role**: what they'll own (default: inferred from context, confirmed).
3. **Familiarity** with the stack (default: new, so spell steps out).

"go" → defaults.

## 2. Sections

1. **What it is**: 2–3 sentences: purpose, users, state (shipping / prototype / paused), from the README and recent `git log`.
2. **Setup**: gather steps from README, package scripts, Makefile, compose, CI. Run each here and note the observed result (tests 41/41, server on :3000). Skip destructive, credentialed and slow steps (deploys, migrations on real data, anything needing a secret, long builds); mark them and any step you couldn't run **unverified — <reason>**.
3. **Env vars**: table Variable · purpose · where to get it, from `.env.example`, config loaders, env lookups, CI secrets. **Names only**: read no real `.env` or secret file, write no value. Unknown source → "ask <owner>".
4. **Tasks**: numbered, each with a "done when" checkable without asking you. From open issues (skip `wayfinder:*` planning tickets and issues In Progress or In Review per the `next` skill's `BOARD.md`); ask the user for the rest. Issues via `gh issue list -R <o>/<r>`, `<o>/<r>` per the `next` skill's `BOARD.md`, Target repo section. `gh` unavailable → ask the user for the task list.
5. **Owners**: area/path → who to ask. Unknown → "unclear — ask <user>".
6. **Don't touch**: path — reason. Empty is fine: "nothing off-limits".

## 3. Draft, then write

Show the full draft. On yes: `skilleddocs/briefs/<name-slug>-<local-date>.md`. Untracked → exclude `skilleddocs/` per [TRACKING.md](../handoff-auto/TRACKING.md) (it also covers the `pip install .` hazard).
