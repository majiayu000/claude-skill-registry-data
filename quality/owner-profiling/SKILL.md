---
name: owner-profiling
description: |
  Build and maintain a structured personal-context portfolio for the project owner — identity, working style, goals, team, decision patterns. Includes both an interview protocol for bootstrapping and observable-signal patterns for incremental refinement. Use to bootstrap an owner profile (interview), to refine an existing profile (target one file), or to incrementally update the profile based on observed patterns from a normal session (the agent watches for signals and proposes additions when evidence accrues).
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-owner-profiling
    version: "1.0.0"
    created: 2026-04-07T00:00:00Z
    category: processkit
    layer: 4
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: actor-profile
        purpose: Resolve and validate Actor IDs referenced by this skill's entities.
    provides:
      primitives: []
      templates: [identity, working-style, goals-and-context, team-and-relationships]
    commands:
      - name: pk-owner-bootstrap
        args: "owner-name"
        description: "Run the initial profiling interview for a new project owner"
      - name: pk-observe
        args: "owner-name observation"
        description: "Record a behavioural observation about a project owner"
---

# Owner Profiling

## Intro

`owner-profiling` builds and maintains a four-file personal context portfolio
for the project owner: who they are, how they want to be communicated with,
what they're optimizing for, and who they work with. The profile is the
single most-loaded set of files per session — it's how the agent learns to
sound like the owner and act in their interest. This skill operates in three
modes: **bootstrap** (interview when no profile exists), **refine** (walk
through one file to update it), and **observe** (incrementally enrich the
profile from signals seen during normal work).

## Overview

### The four files

```
context/owner/                  ← public + project-private files (git-tracked)
  identity.md                   privacy: public
  working-style.md              privacy: project-private (default)
  goals-and-context.md          privacy: project-private (default)

context/owner/private/          ← user-private files (gitignored)
  team-and-relationships.md     privacy: user-private
```

| File | What it contains | Privacy |
|---|---|---|
| `identity.md` | Name, role, organization, what you do, what you're known for. The "if the agent can only read one file, this is it" file. | public |
| `working-style.md` | Communication style + preferences-and-constraints + role-and-responsibilities merged. The hard rules, the always-do/never-do list, the tone preferences, the actual weekly cadence. The single highest-leverage file per session. | project-private |
| `goals-and-context.md` | Goals & priorities + domain knowledge merged. What you're optimizing for, what you know that the agent doesn't, where you're a beginner. | project-private |
| `team-and-relationships.md` | Per-person notes about collaborators — communication style, sensitivities, mutual dependencies. **Never checked into git.** Lives in `private/` so the gitignore rule `context/**/private/` excludes it. | user-private |

### The three modes

#### Mode 1 — Bootstrap (first-time interview)

Triggered when `context/owner/identity.md` is missing or is a stub. The
agent runs the interview protocol from `references/interview-protocol.md`,
which walks through each of the four files in order. Each file's interview
is a small set of questions (3-6 per file). Drafts are reviewed by the
user before being saved. The whole bootstrap takes 20-40 minutes and
should NOT be done in a single sitting unless the user is fresh — break
across sessions if needed.

The recommended order is:
1. `identity.md` first (10 minutes) — quick wins, useful immediately
2. `working-style.md` second (15 minutes) — biggest payoff per minute
3. `goals-and-context.md` third (10 minutes)
4. `team-and-relationships.md` last (5 minutes per person, optional — many users skip this initially)

#### Mode 2 — Refine (target one file)

Triggered by an explicit user request: "Let's update my working style file."
Or by the agent noticing a section is empty/stale and asking. The agent
loads the file, walks the relevant interview questions for the empty
sections only, drafts updates, gets approval, writes back.

#### Mode 3 — Observe (incremental enrichment)

Triggered by signals seen during normal work, NOT by an explicit request.
The agent has the table from `references/observable-signals.md` in mind
and watches for evidence: terse vs. verbose messages, formality, jargon
usage, decision speed, dependency attitudes, etc. When the agent has
observed something **3+ times** in the same session OR **across 3+
sessions**, it surfaces it to the user:

> "I've noticed you consistently prefer X over Y. Want me to add this to
> your working-style.md as a preference?"

The agent NEVER edits the profile silently. The user always approves.

### Always-loaded vs. on-demand

The agent loads `identity.md` and `working-style.md` at session start. These
are short and high-leverage. `goals-and-context.md` is loaded when the
session involves planning or scoping decisions. `team-and-relationships.md`
is loaded selectively when the agent is preparing communication for a
specific person (PR review, email draft, meeting prep).

This is the entry point for the broader context-efficiency story (see the
`agent-management` skill's "Context budget and lazy loading" section).

### Commands

- `/pk-owner-bootstrap owner-name` — run the initial profiling interview
  for a new project owner
- `/pk-observe owner-name observation` — record a behavioural observation
  about a project owner

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Updating the owner profile when the relationship is what
  changed.** If Alice's role on the project shifted, that's a
  Binding update, not an owner-profile rewrite. The owner profile
  describes who the owner IS, not what they're currently DOING.
- **Putting sensitive information in public profile files.**
  Personal context (home situation, salary, relationship dynamics
  with specific colleagues) belongs in the user-private files
  under `context/owner/private/`. Never write sensitive content
  to `assets/identity.md` or any other public-tier file.
- **Treating the profile as a static one-shot document.** Owner
  profiles are living artifacts. Re-run the interview protocol
  when major life or work changes happen, and update incrementally
  whenever observable signals warrant it (per the
  observable-signals reference).
- **Skipping the interview protocol because "it'll be faster to
  guess".** Don't infer the owner's preferences from one
  conversation. The interview exists because preferences are
  surprising — even self-aware owners frequently say "I didn't
  realize I cared about that" mid-interview.
- **Profile fields out of sync with each other.** If
  `working-style.md` says timezone CET but `goals-and-context.md`
  says working hours 6am-10am ET, one of them is wrong. Run a
  consistency check across the four files when updating any of
  them.
- **Inferring strong preferences from one interaction.** A
  one-time annoyance is not a preference. Wait for at least two
  independent observations of the same pattern before adding it
  to the profile.
- **Forgetting privacy tier on new fields.** Every field added to
  the profile must declare its privacy tier (`public`,
  `project-private`, or `user-private`). Defaulting to public for
  convenience leaks information. Default to `user-private` and
  upgrade visibility deliberately.

## Full reference

### The four templates

The templates live in `assets/` and are scaffolded into a project's
`context/owner/` and `context/owner/private/` directories during `aibox
init` (or when the owner-profiling skill is first activated).

- **`assets/identity.md`** — frontmatter (`privacy: public`) + sections:
  Name/Role/Organization, What I Do (one paragraph), What I'm Known For
  (1-3 sentences). The entire file should be under one screen.

- **`assets/working-style.md`** — frontmatter (`privacy: project-private`) +
  sections: Communication style (tone, length, formality), Hard
  constraints (timezone, availability, non-negotiables), Strong preferences
  (formatting, vocabulary, dislikes), Role and responsibilities (weekly
  cadence, decision authority, deliverables), Things I hate (visceral pet
  peeves the agent should avoid).

- **`assets/goals-and-context.md`** — frontmatter (`privacy: project-private`) +
  sections: Current goals (this quarter), Longer-term goals (year+),
  How I think about tradeoffs (default positions), What I'm NOT
  prioritizing, Areas of expertise, Key terminology (jargon I use without
  needing definitions), Where I'm a beginner (topics where I want more
  explanation).

- **`assets/team-and-relationships.md`** — frontmatter (`privacy:
  user-private`) + per-person blocks: Name, Role, Relationship type, How
  we interact, What they need from me, What I need from them, Context for
  agents (sensitivities, communication style, preferences). **Lives in
  `context/owner/private/` by convention.**

### The interview protocol

See `references/interview-protocol.md`. It contains the per-file question
list, the order, and the discipline rules (sequential not batched, draft
after 3-4 questions, validate before saving, never edit silently).

### Observable signals

See `references/observable-signals.md`. A table of patterns the agent
should watch for during normal work, organized by category (communication,
technical preferences, decision patterns, workflow patterns). Each row
describes the signal, how to observe it, and an example recorded preference.

### The privacy convention

Privacy tiers are enforced by directory layout:

| Tier | Path under `context/` | Git status |
|---|---|---|
| public | `owner/identity.md` (and other `privacy: public` files) | tracked |
| project-private | `owner/working-style.md`, `owner/goals-and-context.md` | tracked |
| user-private | `owner/private/team-and-relationships.md` | gitignored |

The aibox `.gitignore` includes `context/**/private/` which matches
`private/` directories at any depth under `context/`. `aibox lint` (Phase 4.4)
verifies that any entity with `privacy: user-private` lives under a
`private/` directory.

### Why these four and not the original ten

The portfolio source ([nlwhittemore/personal-context-portfolio](https://github.com/nlwhittemore/personal-context-portfolio))
proposes ten files. We merged for context efficiency:

| Original portfolio file | Where it goes here |
|---|---|
| identity.md | `identity.md` |
| role-and-responsibilities.md | merged into `working-style.md` |
| communication-style.md | merged into `working-style.md` |
| preferences-and-constraints.md | merged into `working-style.md` |
| current-projects.md | dropped — overlaps with `context/PROJECTS.md` (process tier) |
| goals-and-priorities.md | merged into `goals-and-context.md` |
| domain-knowledge.md | merged into `goals-and-context.md` |
| team-and-relationships.md | `team-and-relationships.md` (kept standalone, in `private/`) |
| tools-and-systems.md | dropped — already captured by `aibox.toml` and the devcontainer |
| decision-log.md | dropped — overlaps with `context/decisions/` (DecisionRecord primitive) |

Net: 10 portfolio files → 4 owner-profiling files. Roughly half the loaded
context for a typical session, with no information loss for the workflows
we care about.

### Relationship to the Actor primitive

`owner-profiling` does NOT replace the `Actor` primitive. They serve
different purposes:

- **`Actor` entities** (under `context/actors/`) — structured records of
  every person/agent/service that participates in the project. Used for
  assignments, bindings, role-binding lookups. Machine-readable.
- **`owner-profiling` files** (under `context/owner/`) — the project owner's
  rich personal context, in prose, optimized for the agent reading them at
  session start. Human-authored.

The owner is also an Actor entity (`ACTOR-owner` typically), but their
Actor file is a thin pointer to the rich `owner/` files. The `Actor` file
might say `bio_files: ["context/owner/identity.md", "context/owner/working-style.md"]`
so any tool that wants the owner's profile knows where to look.

### Multi-actor profiles (future)

The current design assumes a single owner per project. A future extension
could put each actor's profile under `context/actors/<actor-id>/` with the
same four-file structure. The `actor-profile` skill would learn about
this layout. v0.4.0 ships only the owner case.

### MCP server

None in v0.4.0. The skill is markdown-only. The agent reads/writes the
files via the standard file-edit tool. If patterns of use justify a server
in a future release (e.g. "validate the privacy tier matches the
directory" as a tool call), it can be added; until then, the simplicity
of "just files" wins.
