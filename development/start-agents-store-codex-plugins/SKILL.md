---
name: start
description: 'Create or repair a project''s macstack/ folder and macstack.json — from nothing (a six-question interview), from an existing macstack.json, from an existing codebase, or by migrating an older layout Arguments: project path | business request | (empty = design from scratch) | --migrate.'
---

One entry point for everything that brings a project into the standard. Work out which
case it is, **say which and why, and wait for confirmation** before writing anything.
Guessing is expensive here: three of these modes move or overwrite files.

Read `macstack-dev:setup` first — it resolves paths, checks the tooling and tells you
what already exists.

**Three ways a project starts.** They differ only in where the facts come from:

| You have | Facts come from | Mode |
|---|---|---|
| **Nothing** | the owner — six questions in result-first order | **design** — `spec-authoring` B0, then B1–B5 |
| **A `macstack.json`** | the spec | **derive** — `documents`, write the six documents from it |
| **A codebase** | the code | **audit** — `code-audit` enumerates, then `spec-authoring` A1–A3 |

Never mix them. A spec half-derived from a business request and half-guessed from a
half-read codebase is a spec nobody can defend a single line of.

**Three ways a project is already partly here.** The folder exists and something is off:

| What you find | Mode |
|---|---|
| `macstack.json` at the repo root, or a flat/`docs/`-era layout, or v1 table-shaped documents | **migrate** — `documents`, migration mode |
| A valid spec, an incomplete `macstack/` | **repair** — `documents`, create only what is missing |
| A valid spec and folder, no project files | **scaffold** — `scaffold-project` |
| A valid spec and folder, and code that has moved on | not this command — `/macstack-dev:check --new` |

Then, in order and without skipping:

0. **`code-audit`** — in **audit** mode only: enumerate what the code contains before
   writing a line of spec. Reading a codebase into a spec by browsing it is how a
   subsystem goes unmentioned — the enumerator lists every candidate the declared stack's
   conventions produce, and says out loud when a convention matched nothing.
1. **`spec-authoring`** — produce or complete `macstack.json`. In **design** mode start
   at B0, the interview: six questions asked through AskUserQuestion, in result-first
   order, recommendation first. The order is the method — the chain reads Goal ← Result
   ← Process ← Task ← Workflow ← Software, so software is decided last or it is decided
   for the wrong reason. For a hard case, delegate to the `macstack-architect` agent.
2. **`documents`** — create or repair `macstack/`, seeding the authored client
   documents once and rendering the generated ones. Read `documents/references/format-rules.md`
   before writing any document.
3. **`infisical-env`** — wire the environment if the spec declares accesses.
4. **`best-practices`** — install the project rules and slash-command skills.
5. **`scaffold-project`** — only in scaffold mode, and only in the mandatory source
   order: prototype → stack plugins → dev plugins → generation. That order is the
   product; every violation in testing produced files that contradicted the
   architecture.
6. **`lint`** — a spec that fails lint is not scaffolded from.

Finally write the `## Stack Specification` block into **both** `CLAUDE.md` and
`AGENTS.md`, pointing at `macstack/macstack.json` and naming the six client documents.
Both, not one: the documents are meant to be read by whichever coding agent the team
runs, and a spec only Claude Code can find is a spec half the team cannot use.

Report what was created, what was left alone, and the single next command.