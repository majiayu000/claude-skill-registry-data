---
name: project-kickoff
description: "Interview-style skill for starting a new project. It clarifies the goal and scope, then creates three tracking files (PROJECT.md, DECISIONS.md, PROGRESS.md) that act as persistent memory across all future Claude sessions. Use this skill EVERY time the user starts a new project of any kind — an app, a website, a plugin, a design, a prototype, a documentation or knowledge system, anything. Typical trigger phrases: I'm starting a new project, let's build something new, I want to make a website/app/plugin/tool, let's kick off, new project. At the end of the interview the skill doesn't just ask questions — it creates the three tracking files, writes the tracking convention into the project's CLAUDE.md, and from then on every conversation automatically records important decisions and completed units of work."
---

# Project Kickoff

Guides the user through clarifying goals, scope, and key decisions at the start of a new project, then creates three tracking files that serve as the project's memory for its entire lifetime — across every future Claude session.

**Language**: Conduct the entire interview and write all generated files in the language the user is speaking. If the user writes in Spanish, ask in Spanish and write Spanish PROJECT.md/DECISIONS.md/PROGRESS.md files. The headings shown in the templates below should be translated accordingly.

---

## When to use

When the user is starting a new project — any kind: an app, a website, a plugin, a design or prototype, a tool, a knowledge base or documentation system.

Do NOT use it for a new component or feature inside an ongoing project — this is for kickoff only.

---

## The three files

The output of this skill is three markdown files that live alongside the project:

### 1. PROJECT.md — What we're building
A snapshot of the project that records the initial state, but **gets updated** when scope or direction changes substantially. Contents:

```
# [Project name]

## What
One or two sentences describing what we're building.

## For whom / why
Target user or use case + motivation.

## V1 scope
- Concrete things that are definitely in
- As a list

## Out of scope
- Concrete things that are not
- As a list (marked as V2 if planned for later)

## Look & feel
One or two sentences about the visual / tonal direction (skip if not applicable).

## Stack / tools
What we're using to build it.

## Where it lives
The path of the three tracking files (folder).
```

### 2. DECISIONS.md — What changed and why
A chronological log, **newest on top**. Each entry: date + title + 1–3 sentence rationale. **Auto-recorded** — whenever an explicit decision comes up in conversation (scope change, change of technical direction, aesthetic change, discarded idea), Claude writes it in.

```
# Decision log

## 2026-06-09 — [Short descriptive title]
Brief rationale.

## 2026-06-08 — [Short descriptive title]
Brief rationale.
```

### 3. PROGRESS.md — What's been built
A chronological log, **newest on top**. Entries are added when a substantial unit is completed (a component, a feature, a screen) — **not** small tweaks and bug fixes. **Auto-recorded** — whenever a substantial unit is finished, Claude writes it in.

```
# Completed work

## 2026-06-09 — [Unit name]
- What it does
- What variants it has
- Anything a future session needs to know

## 2026-06-08 — [Unit name]
...
```

---

## Process

### 1. Opening question

Start with a single question, no clarifying questions yet:

> **What would you like to build? Give me 1–2 sentences.**

### 2. Clarifying questions

Only ask about what the opening answer did **not** already cover. Don't ask questions whose answers you already have. Adapt the wording and depth of these questions to the kind of project the user described.

- Who is it for / what's the use case
- What's in V1, what's left out (or pushed to V2)
- Look & feel direction in one sentence (skip if irrelevant for this project)
- Stack / tools, if applicable (and whether there's an existing system or library to build on, or it's from scratch)
- Where the three tracking files will live (project folder path)

### 3. PROJECT.md proposal

Based on the answers, write a `PROJECT.md` proposal following the template above and ask for approval. **Do not create any files until the user approves.**

If the user requests changes, revise and show it again.

### 4. Creating the three files

After approval:

1. **Create `PROJECT.md`** at the agreed path.
2. **Create `DECISIONS.md`** empty except for the header and a first entry:

   ```
   # Decision log

   ## [date] — Project started
   Initial scope and direction recorded in PROJECT.md.
   ```

3. **Create `PROGRESS.md`** empty except for the header:

   ```
   # Completed work

   _No entries yet._
   ```

4. **Write the convention into the project's `CLAUDE.md`** (create it if it doesn't exist). This step is critical: without it, a future fresh session won't know about the tracking files and auto-recording will silently stop. The block to add:

   ```
   ## Project tracking files (project-kickoff convention)

   Three tracking files live alongside this project: `PROJECT.md`, `DECISIONS.md`, `PROGRESS.md`.
   Maintain them automatically in every conversation:

   - `DECISIONS.md` — on every explicit decision, add a new entry ON TOP
     (date + short title + 1–3 sentence rationale). A decision = scope change,
     change of direction, aesthetic change, discarded idea. No minor technical details.
     If a decision overturns a previously recorded direction or assumption,
     use the richer narrative format (What we thought / Why we turned / What changed).
   - `PROGRESS.md` — when a substantial unit (component, feature, screen) is
     completed, add a new entry ON TOP. No small tweaks or bug fixes.
   - `PROJECT.md` — update it when scope or direction changes substantially
     (and record that change in DECISIONS.md as well).

   After recording, mention it in one sentence ("Recorded in DECISIONS.md: ...").
   Only ask when uncertain (thinking out loud ≠ a decision).
   ```

### 5. Wrap-up

Tell the user:
- The three files have been created, and where to find them.
- The convention is now in `CLAUDE.md`, so **every future conversation** will automatically write to `DECISIONS.md` on important decisions and to `PROGRESS.md` when larger units are completed.
- If the scope or direction changes substantially, `PROJECT.md` gets updated too (and the change also shows up in `DECISIONS.md`).

---

## Auto-recording rules

After this skill completes, in all further conversations on the project:

### When to write to DECISIONS.md

Whenever an **explicit decision** is made in conversation that departs from the previous state or sets a meaningful new direction:

- Scope change (something dropped from V1, something pulled forward from V2, a new requirement)
- Change of technical direction (e.g. "let's drop Tailwind, vanilla CSS instead")
- Aesthetic change (e.g. "dark background after all")
- Naming / branding change
- A discarded idea worth writing down so it doesn't have to be re-debated later
- Anything else that would help a future session answer "why is it like this?"

Do **not** record minor technical details (class names, padding values) — those live in the code.

Entry format: date + short title + 1–3 sentence rationale. Newest on top.

**Direction reversals get the richer format.** When a decision overturns a previously recorded direction or assumption — not just adjusts it, but reverses it — use the narrative entry format, because the reasoning behind a turn is worth more than a bare statement:

```
## [date] — [Title of the turn]
**What we thought**: ...
**Why we turned**: ...
**What changed**: ...
```

For ordinary decisions, stick to the short format — don't pad small decisions into the narrative structure.

When a decision also affects the contents of `PROJECT.md` (e.g. something drops out of V1), **update `PROJECT.md` too**, don't just log it in `DECISIONS.md`.

### When to write to PROGRESS.md

When a **substantial unit** is completed:
- A component
- A feature (e.g. a command, a page)
- A screen (for design projects)
- Anything a future session will need to know "this already exists"

Do **not** record small tweaks, bug fixes, or styling refinements.

Entry format: date + unit name + 2–5 lines about what it does, what variants it has, and anything a future Claude instance should know about it.

### How to record

Don't ask every time ("Should I add this to DECISIONS?"). If the decision is clear and the user has confirmed it, just write it in and mention it in one sentence:

> "Recorded in `DECISIONS.md`: [date] — [title]."

Or:

> "Added to `PROGRESS.md`: [unit name]."

Only ask when uncertain ("Should I record this?"). The typical uncertain case: the user is thinking out loud and it's not clear whether the option they voiced is a decision yet.

---

## Process overview

```
Trigger (starting a new project)
  ↓
Opening question: "What would you like to build?"
  ↓
Ask only about what isn't known yet
  (adapt questions to the kind of project)
  ↓
PROJECT.md proposal → approval
  ↓
Create the three files in the agreed folder:
  - PROJECT.md (filled in)
  - DECISIONS.md (empty + opening entry)
  - PROGRESS.md (empty)
  + convention block in the project's CLAUDE.md
  ↓
Wrap-up: explain auto-recording
  ↓
[in all further conversations on the project, Claude
 keeps the three files up to date based on the
 CLAUDE.md convention — even in fresh sessions]
```
