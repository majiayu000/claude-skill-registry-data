---
name: project-help
description: '[Utilities] Use when asking what the .claude framework does for THIS project: configuration, skills/agents/workflows, reference docs, key tech/architecture/structure facts. Command keyword search: framework-config --mode=help.'
disable-model-invocation: true
---

## Quick Summary

**Goal:** Answer anything about (a) the portable `.claude` framework **as configured for this project** and (b) this project's own key technical, architecture, and structural knowledge — from generated output, never from memory.

**Workflow:**

1. **Classify** the question against the routing table below.
2. **Run** the matching generator command. Never answer from recall.
3. **Present** the output verbatim, then add only the interpretation the user asked for.
4. **Route onward** when the question belongs to a narrower help surface (`/project-config --help`, `/project-init --help`).

**Key Rules:**

- MUST ATTENTION this skill is **read-only and terminal**. It creates no tasks, runs no scan, edits no file, and never proposes a change. If the user wants a change afterwards, hand off to `/project-config` or `/project-init`.
- MUST ATTENTION every number, path, and name in the answer comes from a command run **in this session**. The framework and the config both drift; a memorised count is a hallucination with a plausible shape.
- Show the generator output verbatim before commenting on it. Do not summarise it away.
- Config **option** questions ("what can I set", "who reads `docsRoots`") belong to `/project-config --help` — delegate rather than duplicating.
- Never print secrets. The config holds references only; if a value looks like a credential, report the key and stop.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Scope

**In scope:** what the framework is, what each of its layers does, which skills/agents/workflows/hooks exist here, which reference docs exist and what each is for, how the mirrors are generated, this project's stack, structure, module map, and verification commands.

**Out of scope:** changing configuration (`/project-config`), initialising or re-initialising a project (`/project-init`), generic ClaudeKit command usage unrelated to this project (`/framework-config --mode=help`), and any implementation work.

## Routing table

| The user asks… | Run |
|---|---|
| "what is this `.claude` thing / how is it wired / what are the layers" | `node .claude/skills/project-help/scripts/project-overview.cjs --framework` |
| "what skills do I have / is there a skill for X" | `node .claude/skills/project-help/scripts/project-overview.cjs --skills` (or `--skills=<term>`) |
| "what is the structure of this project / where does code live" | `node .claude/skills/project-help/scripts/project-overview.cjs --structure` |
| "what stack / architecture / database / deployment" | `node .claude/skills/project-help/scripts/project-overview.cjs --stack` |
| "how do I test / verify / what command do I run" | `node .claude/skills/project-help/scripts/project-overview.cjs --commands` |
| "what docs exist / which doc do I read for X" | `node .claude/skills/project-help/scripts/project-overview.cjs --docs` |
| "tell me everything" / no clear target | `node .claude/skills/project-help/scripts/project-overview.cjs --all` |
| "what can I configure / who reads option X" | `node .claude/skills/project-config/scripts/project-config-help.cjs --overview` — then delegate to `/project-config --help` |
| "every project-config option" / "what is inside option X, including nested and array-item fields" | `node .claude/skills/project-config/scripts/project-config-help.cjs --sections`, then `--section=<name>` (or `--search=<term>`) |
| "what can I set in `.ck.json` / `.ck.local.json`", "which environment variables", "how do I turn X off" | `node .claude/scripts/ck-config-help.cjs` — then delegate to `/framework-config --mode=help config` |
| "which skills consume which option" | `node .claude/skills/project-config/scripts/project-config-help.cjs --consumers` |
| "where do specs, plans, and ADRs live" (roots and tokens) | `node .claude/skills/project-config/scripts/project-config-help.cjs --roots` |
| "what does init decide" | `/project-init --help` |

A bare `--skills=<term>` argument filters the catalog; use it instead of guessing whether a skill exists.

## The two generators

Both are plain `node` entrypoints using only `node:` built-ins (PORT-001). Neither takes a host `package.json` script, and both resolve the repository root by walking up for a marker, so they also run from the `.agents/` mirror.

- **`.claude/skills/project-help/scripts/project-overview.cjs`** — framework inventory and project knowledge. Reads `.claude/.ck.json`, the project-config file it points at, and the live contents of `.claude/{skills,agents,workflows,hooks}`. Modes: `--framework`, `--skills[=<term>]`, `--structure`, `--stack`, `--commands`, `--docs`, `--all` (default).
- **`.claude/skills/project-config/scripts/project-config-help.cjs`** — the configuration option surface. Reads the config SCHEMA, the portability tokens, and the reference-doc registry, then counts consumers by scanning the framework tree. Modes: `--overview` (default), `--sections`, `--section=<name>`, `--consumers[=<key>]`, `--docs`, `--roots`, `--skills`, `--current`, `--search=<term>`, `--json`, `--help`.

## Presentation rules

- Print the command you ran, then its output verbatim, then your interpretation — in that order, so the user can re-run it.
- Consumer counts are **name-reference counts**, not a call graph: a skill that mentions an option in prose counts. Say so whenever you quote one.
- `--current` in the config helper reports declared-vs-defaulted only; validity is `/project-config --validate`, not this skill.
- When a doc is listed as configured but missing on disk, report the gap and name the owning `/scan --target=…`; do not offer to create it here.
- If the user's real question is "change this", stop answering and route: `/project-config` for an existing project, `/project-init` for an uninitialised one.

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

## Closing Reminders

**IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting

**IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
**IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
