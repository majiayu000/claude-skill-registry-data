---
name: create
description: Scaffolds a new plugin, skill or agent in this repo, following its authoring guidelines. Use when the user wants to "create a skill", "add a new agent", start a "new plugin" or "scaffold" a component. Not for changing an existing one.
argument-hint: <plugin|skill|agent> <name> [description]
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Bash(mkdir *), Bash(make vendor-shared), Bash(pre-commit run *), Bash(make test *), Bash(make validate *)
---

# Component Creator

## Overview

Scaffolds a new plugin, skill or agent under `plugins/`. It reads the guideline for the component type and a few current examples, shows a plan for approval, writes the files along with every registry entry they need, and runs the repo's checks. It never commits.

## When to Use

Creates a component that doesn't exist yet.

### When NOT to use

- Changing an existing skill or agent: edit it, then walk the guideline's pre-publish checklist.
- One fix across many files: use `batch-fix`.
- Drafting a plugin skill through pressure scenarios and a RED/GREEN/REFACTOR loop: use `/mz-base:construct-skill`.

## Input

`$ARGUMENTS` — what to create:

- `skill <name> <description>` — a new skill in an existing plugin
- `agent <name> <description>` — a new agent in an existing plugin
- `plugin <name> <description>` — a new plugin with its manifest and registry entries

If the type, the target plugin or the purpose is unclear, ask with AskUserQuestion. Never guess.

## Core Process

### Phase Overview

| #   | Step                   | Gate             |
| --- | ---------------------- | ---------------- |
| 1   | Read the guideline     | —                |
| 2   | Study current examples | —                |
| 3   | Plan                   | Approve / Reject |
| 4   | Write the files        | —                |
| 5   | Verify                 | —                |

State lives at `.mz/task/<task_name>/state.md` under the repo root, where `task_name` is `<YYYY_MM_DD>_create_<name>` (`_v2`, `_v3` on a same-day collision). Use schema v2 from `guidelines/STATE_SCHEMA.md`, plus `Component: <type> <plugin>/<name>` and `FilesWritten`. Write it after each step and before the gate.

### 1. Read the guideline

Read the guideline for the component type in full. It is the authority, and its closing pre-publish checklist is what step 5 walks.

- **Skill**: `guidelines/SKILL_GUIDELINES.md`, plus `guidelines/STATE_SCHEMA.md` if the skill writes state and `guidelines/JOURNAL_GUIDELINES.md` if it has a gate.
- **Agent**: `guidelines/AGENTS_GUIDELINES.md`.
- **Plugin**: "Adding a New Plugin" in `CLAUDE.md`, the guideline for each skill and agent it will ship, and `guidelines/HOOKS_GUIDELINES.md` if it ships hooks.

### 2. Study current examples

Read the reference implementations the guideline names, then two or three components of the same type in the target plugin: SKILL.md plus one phase file, an agent's frontmatter and body, or a `.claude-plugin/plugin.json` and its directory layout. An example that contradicts the guideline predates it, so follow the guideline.

### 3. Plan

The plan covers:

- **Skill**: the file tree (SKILL.md, phase and reference files, eval cases); the description draft with its character count; the phase table with each gate; the agents it dispatches, the tier each one pins, and any plugin this adds to `dependencies`; each Bash command `allowed-tools` grants; the routing-table row, or the `user-invocable: false` or `disable-model-invocation: true` flag that exempts it.
- **Agent**: the full frontmatter (`name`, `description`, `tools`, `model`, `effort`, `maxTurns`, `color`); the archetype; standalone or pipeline-only, and who dispatches it; the body outline.
- **Plugin**: the directory tree; `.claude-plugin/plugin.json`; the marketplace entry; the `data/codex_migration.toml` package; whether it needs the `shared` link; its planned skills and agents.

Write the plan to `.mz/task/<task_name>/plan.md`, then present the gate.

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

1. Write `state.md` with the plan path and `awaiting approval: plan` in `what_remains`.
1. Read `plan.md` and emit it verbatim as a chat message under `## Plan for review: create`, ending with `**Approve** → write the files · **Reject** → stop, nothing written · reply with feedback to revise`. Never replace the body with a path or a summary.
1. Call AskUserQuestion with the question `The plan above is ready for review.`, the header `Plan`, and the options **Approve** and **Reject**.

**Response handling**:

- **Approve** → record the plan path under `## Decisions` in `state.md`, clear the `awaiting approval` entry, go to step 4.
- **Reject** → set `Status: aborted_by_user` and stop.
- **Any other answer** is feedback: revise `plan.md`, re-emit the whole plan message and ask again. Loop until Approve.
- **No answer** (AskUserQuestion denied or unavailable) → set `Status: blocked` and stop. A missing answer is never approval.

### 4. Write the files

Write what the plan lists. The guideline's checklist holds every rule; these are the ones most often missed here.

**Skill**

- The description opens with a capability clause, then "Use when the user wants …", keeps phrases users type, and names the nearest sibling as a counter-trigger. It is one line of at most 250 characters with any `when_to_use`, has no `<` or `>` and no all caps, and is quoted if it contains `: `.
- SKILL.md sets no `model:`; the agents it dispatches pin their tiers. `allowed-tools` grants Bash one command at a time, as `Bash(<command> *)`.
- SKILL.md aims for about 150 lines and stays under about 20,000 characters. Phase files stay under about 400 lines and are read at the start of their phase. Sections follow "Skill Anatomy".
- Gates copy the canonical skeleton from "Approval Gates". State Management copies the compact contract block from `guidelines/STATE_SCHEMA.md` verbatim.
- Add its row to the routing table in `plugins/mz-base/skills/using-mozg-pipelines/SKILL.md`, with its plugin in the last column, unless it is exempt.
- A skill Claude can invoke gets at least three `claude plugin eval` cases under `evals/<plugin>/`, two that should fire and one near miss, shaped like the plugin's existing cases.

**Agent**

- `name` is kebab-case, two to four words, unique across the marketplace, and matches the filename.
- The description opens with a capability clause, then "Use when …". A standalone agent gives two to four prose trigger scenarios and no `<example>` blocks. A pipeline-only agent states its purpose, who dispatches it and when not to use it.
- `tools` follows the table in "Archetype Templates" with least privilege: an analysis agent omits `Edit` and holds `Write` only for its named output file, and only orchestrators list `Agent`.
- `model` is an explicit tier, never `inherit`. `effort` stays `medium` unless a higher level measurably helps, and then the agent gets a `HIGH_EFFORT_AGENTS` entry in `tests/plugin_lint/test_agents.py`. `maxTurns` is set.
- The body has Role, Core Principles, Process, Output Format and Red Flags, in the second person, and ends with one `STATUS:` line when an orchestrator consumes its output.
- When a skill in another plugin dispatches it, that plugin's manifest lists this one in `dependencies`.

**Plugin**: follow "Adding a New Plugin" in `CLAUDE.md`. Easy to miss:

- `version` in `plugin.json` is the marketplace's current `metadata.version`. Read it; never invent one.
- When its skills or agents read shared rule files, create an empty `plugins/<name>/shared/` folder and run `make vendor-shared` to fill it with a copy of mz-base's. Never symlink it: Anthropic's directory blocks symlinks.
- A plugin with `dependencies` also goes into `_EXPECTED_DEPENDENCIES` in `tests/codex_migration/test_inventory.py`, next to the pinned plugin list.
- Give it a `README.md`, and add it to the install list and the plugin sections of the root `README.md`.

**Every new skill or agent** in a marketplace plugin changes the skill or agent count that `tests/codex_migration/test_inventory.py` pins. Update the count in the same change.

### 5. Verify

1. Run `pre-commit run --files <every file written or edited>` and fix what it reports.
1. Run `make test`. Its `tests/plugin_lint/` suite covers frontmatter, the description budget, Bash grants, sizes, paths, dispatched agents and `dependencies`, the routing-table row and all-caps emphasis.
1. Run `make validate`, which runs `claude plugin validate --strict` on the repo and every plugin.
1. Walk the guideline's "Review checks" list by hand.
1. For a skill or a standalone agent, offer `make eval PLUGIN=<plugin>`. It spends money, so run it only on a yes.

Set `Status: complete` and report the files written, each command with its result, and every checklist item left unchecked. Don't commit.

## Red Flags

- You wrote a file before the plan was approved.
- You copied frontmatter or a description from an older component without checking it against the guideline.
- A new skill has no routing-table row, or the inventory count wasn't updated.
- You reported success without the output of `make test` and `make validate`.
