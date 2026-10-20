---
name: agent-workspace
description: >-
  Use when entering, bootstrapping, migrating, or working inside a shared repo
  organized as an "agent-workspace" — a workspace designed for humans and AI
  agents to collaborate, with conventions for story or project tracking,
  session logs, skills, and CLAUDE.md routing. Triggers: agent workspace,
  bootstrap workspace, set up CLAUDE.md for a shared workspace, workspace
  audit, "where does this go in the workspace", where does this sessionlog go,
  copy notes from another repo.
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: 0.1.0-alpha.1
---

# Agent Workspace

An **agent-workspace** is a git repo structured so humans and AI agents can work in it together without friction. It's a pattern, not a product — a handful of directory conventions and files that let an agent land cold, orient itself, and contribute without breaking the grain of ongoing work.

> **Alpha, and a living document.** Working workspaces disagree on several conventions, on purpose. Where they do, this skill names the options instead of pretending there is one rule — see "Where workspaces differ" below. Expect it to change.

Full concept & rationale: `${CLAUDE_SKILL_DIR}/references/concept.md`.
Bootstrapping or migrating a workspace: `${CLAUDE_SKILL_DIR}/references/bootstrapping.md`.

## When to invoke this skill

- You landed in a repo with `CLAUDE.md` plus `sessionlogs/`, `stories/`, `projects/` or `.claude/skills/` (at the root or under `docs/`) — orient before acting.
- The user says "bootstrap a workspace," "set up CLAUDE.md for this," "audit this workspace," or "where should this file go."
- Converting an existing ad-hoc shared repo into the pattern.

## Workflow: ORIENT → LOCATE → CONTRIBUTE

### 1. ORIENT

Read in this order:

1. `CLAUDE.md` (or `AGENTS.md`) at the repo root — the routing guide. If neither exists, this is not (yet) an agent-workspace; flag it. Some sections may be parsed by tools — keep their headings and keys literal.
2. `README.md` — human overview; may carry context CLAUDE.md assumes.
3. The work index — a stories index, `projects/`, or a central `TODO.md`, whichever the workspace uses.
4. The last 2-3 sessionlogs — what happened recently and what's unresolved.
5. `.claude/skills/` and `.claude/agents/` — workspace-local conventions that override generic behavior.

### 2. LOCATE

**The workspace's `CLAUDE.md` is authoritative for paths.** The table below gives the *default* homes; use one only when `CLAUDE.md` and the existing files are both silent.

**If the path you are about to write does not exist yet and `CLAUDE.md` doesn't name it** — a new top-level directory, or a kind of file the workspace has no place for — ask the user where it goes before writing, and offer to record the answer in `CLAUDE.md`. Every unasked guess becomes precedent.

| Kind of content | Default home |
|---|---|
| Multi-session work tracking | `docs/stories/{slug}/STORY-{slug}.md` (or `projects/{name}/`) |
| Per-session notes | `docs/sessionlogs/YYYY-MM-DD-topic-slug.md` |
| Project rules for agents | `docs/rules/` (imported from `CLAUDE.md`) |
| Reusable templates | `docs/templates/` |
| Plans (actionable) | `docs/plans/` — one plan directory per repo; narrative plans stay in the story |
| Research reports | inside the story/project they serve; no such home → ask |
| Workspace-local skills | `.claude/skills/{name}/` (incubate here before promoting) |
| Workspace-local agents | `.claude/agents/{name}.md` |
| Content from another scope | **Its own repo — not here** (see below) |

Full lookup table and frontmatter conventions: `${CLAUDE_SKILL_DIR}/references/structure.md`.

### The access boundary: data scope, not agent scope

You may *read* across workspaces to help the user. You may not *move content* across them.

**Before writing, compare where the content came from with who can read where it is going.** If any of it came from a place with a different or narrower audience — another repo or workspace, a mounted submodule, a client or sub-unit folder in this repo with its own readers — do not copy, summarize or paraphrase it into the destination, even when the user asks for it "to have it handy". Instead:

- answer in the conversation, or
- write the note at the source (its own repo's or unit's sessionlog), or
- record only a pointer at the destination ("see the deploy runbook in the work workspace"), with no confidential detail.

Say which you did and why. A shared workspace must be safe for every one of its readers; a personal workspace must not absorb work or customer data. Details: `${CLAUDE_SKILL_DIR}/references/concept.md`.

### 3. CONTRIBUTE

Follow the conventions the workspace already demonstrates:

- **Language:** follow the workspace's choice for directory names and headings (default: English structure, content in the team's language). Keys and headings that tools parse stay literal in any language.
- **Story / project updates:** append, update status markers, never silently rewrite history. Sessionlogs are append-only. Default: one file per topic; a later session on the same topic appends a dated section to it. Some workspaces start a new dated file beside the predecessor instead — follow `CLAUDE.md`.
- **Commits:** match the repo's prefixes and its git workflow — some workspaces want every unit of work committed and pushed, others want PRs, others want the human to commit.
- **Shared memory:** project knowledge goes in the workspace, not in an agent's per-machine memory.
- **Skill incubation:** new skills live in the workspace until battle-tested AND generally useful. Only then promote to a shared skills repo.
- **Dual-tool compatibility:** prefer plain Markdown + frontmatter in `.claude/` so other tools (e.g. Cursor) can read it.

## Where workspaces differ

Real workspaces answer these differently, and each answer works somewhere. Find the workspace's answer in `CLAUDE.md`; don't import another workspace's.

1. Work dirs under `docs/` or at the root
2. Stories with frontmatter status, or projects with `_paused/` / `_done/` folders
3. Action items per story, or in a central `TODO.md`
4. Session narrative in `sessionlogs/` only, inside stories, or per sub-unit
5. Rules inline in `CLAUDE.md`, or split into `docs/rules/`
6. A compiled knowledge layer (`context/`, `wiki/`) or none
7. One plan directory, or one per tool
8. Nested code repos: does the agent commit there, or only the human?
9. Agent git workflow: push to `main` after each unit, PRs, or never commit
10. Agent memory vs workspace as the shared memory
11. Raw command-output logs kept or not
12. Secrets: manager only, or encrypted in the repo
13. How the scope boundary is drawn (per-customer repos, `clients/` submodules, documented exceptions)
14. Where research reports go
15. Entry file: `CLAUDE.md`, `AGENTS.md`, or one importing the other
16. Sub-units: a folder in an umbrella workspace, or their own workspace repo
17. Conventions stated locally, or inherited from an umbrella workspace by link
18. Rollups, reports and generated files: which, and how they are checked
19. Language of directory names and headings: English, the team's language, or mixed
20. Top-level taxonomy: functional dirs, numbered area folders, or topical root files
21. What workspace agents are (tools, personas, domain workers) and their autonomy levels

Options and when each fits: `${CLAUDE_SKILL_DIR}/references/variations.md`.

## Bootstrapping a new workspace

Run the interview in `${CLAUDE_SKILL_DIR}/references/bootstrapping.md`. It covers greenfield repos and migrating an existing one, and has the user answer the "where workspaces differ" questions up front. Templates live in `${CLAUDE_SKILL_DIR}/templates/`.

## Related skills

- `dossier` — research reports; decide with the user where in the workspace they land.
- `ballot` — decisions reviewed asynchronously; the ballot file lives in the story/project it decides.
- `lab-notes` — experiments with a hypothesis and a verdict, for workspaces that keep `experiments/`.
- `story-tracking` and Plot ([plot-pm/plot](https://github.com/plot-pm/plot)) — story folders and the plan → implement → deliver workflow.
- A session wrap-up skill (e.g. `bye`) — writes the sessionlog at the end of a session.
- An MCP server for the workspace can expose its status and sections to chat clients that cannot open the repo.

## Red flags

Stop and surface these to the user rather than patching over:

- No `CLAUDE.md` or `AGENTS.md` at root → don't silently create one; ask whether this workspace should adopt the pattern.
- About to write content whose source has a different or narrower audience than its destination (another repo, a client folder, customer data in a group-shared workspace) → access-boundary check above.
- Research or notes about to be committed into a repo whose audience doesn't match (private research into a public repo, personal into work) → stop; find the right repo.
- A session doing real work with no sessionlog yet → write one before ending; if an earlier session ended without one, recover what you can from git history.
- A story or project marked active whose last update is weeks old → ask whether it is really active, paused, or done.
- Skills scattered outside `.claude/skills/` → flag; don't "helpfully" reorganize without approval.
- A `CLAUDE.md` rule that automation depends on, with no hook or script enforcing it → suggest a gate (`concept.md`, "Composing with the system prompt").
- Conflict between workspace `CLAUDE.md` and this skill → **workspace wins**. This skill describes the pattern; individual workspaces refine it.
