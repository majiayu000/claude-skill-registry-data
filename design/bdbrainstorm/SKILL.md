---
name: bdbrainstorm
description: Combines multi-agent brainstorming, the /grill-me slash command, and the 3 Core Godmodes (godmode-engineering, godmode-ui-ux, godmode-shipping) to force a comprehensive, multi-agent ideation and technical design workflow, ending in a hand-off to /startcycle-graph.
category: bdb-core
---

# BDBrainstorm: The Ultimate Multi-Agent Design & Ideation Workflow

When this skill is invoked or requested, you MUST orchestrate a comprehensive ideation and development workflow using a combination of multi-agent brainstorming, interactive user grilling, and strict adherence to the 3 Core Godmodes (`godmode-engineering`, `godmode-ui-ux`, `godmode-shipping`).

## Core Requirements & Workflow

You are strictly required to enforce the following 6 pillars in your process:

### 1. Multi-Agent Brainstorming
- Instead of brainstorming alone, you MUST spawn specialized subagents (using `invoke_subagent`) to discuss ideas, architecture, and features.
- Assign clear, distinct roles to subagents (e.g., "UI/UX Visionary", "Technical Architect", "Devil's Advocate") and have them debate and refine the concept before any code is written.

### 2. The Grilling Interview
- **Invoke the `grill-with-docs` skill and follow it** — or `grill-me` when there is no working directory to leave a paper trail in. Do not paraphrase an interview here; those skills hold the protocol (design tree, frontier rounds, numbered questions each with a recommended answer), and a second description of it in this file would drift from the first.
- Actively challenge the user's initial ideas. Do not accept vague requirements.
- `grill-with-docs` additionally runs `domain-modeling`, so terminology and decisions settled during the debate land in `CONTEXT.md` and ADRs as they crystallise rather than evaporating with the session — which is usually what you want before a multi-agent build.

### 3. Target Folder Selection & Project Scaffolding
- After the brainstorming and grilling phase produces a solid conceptual plan, you MUST explicitly ask the user: *"In which folder, workspace, or project directory should the output artifacts (e.g., plan, README.md, AGENTS.md) be stored?"*
- Do NOT proceed to generate artifacts or write files until the user has confirmed the specific directory.
- **Crucial:** Once the directory is confirmed, and BEFORE starting the development phase, you MUST utilize the `openwiki-skill` and `github-repo` skills to initialize the directory, set up `AGENTS.md`, and generate the foundational project files.

### 4. Engineering Godmode (Clean Architecture)
- Once the conceptual plan is solid, you must strictly enforce `godmode-engineering` principles.
- Delegate specific implementation tasks to independent subagents using Domain-Driven Design (DDD). You act as the Master Orchestrator, reviewing their work to ensure it passes the 5-step debugging triage.

### 5. UI/UX Godmode (Anti-Slop Standards)
- Every user interface decision, wireframe, or component generated during this process MUST adhere to the `godmode-ui-ux` guidelines.
- Enforce high-agency frontend interfaces, strict design taste, calibrated color palettes, and modern typography. Do not settle for "MVP" aesthetics.

### 6. Shipping Godmode & Pipeline Hand-off
- Before the brainstorm concludes, verify that the plan satisfies the `godmode-shipping` rules (Spec-Driven Development, feature flags, rollback strategies).
- **Mandatory — Plan Canvas review.** Write the aligned plan to a file. Choose the planning mode by running `aos-plan-canvas modes` and presenting available modes to the user (see the "Planning mode choice" section in the `plan-canvas` skill). Then run `aos-plan-canvas open <file> --mode <choice>` followed by `aos-plan-canvas await <file>` and leave it running. The user reviews and annotates in the browser (Mermaid diagrams render live, click-to-annotate, chat rail); do not write `state.goal` or hand off to `/startcycle-graph` before an `approve` verdict comes back. A `request_changes` verdict means revise the plan file and reopen the session — it live-reloads. This runs identically regardless of which agent harness is executing this skill; it is a plain CLI, not a Claude-Code-specific mechanism. See the `plan-canvas` skill.
- Write the plan in the agenttrail component convention (`## Name {#id}` components with `needs:` / `files:` lines, tasks as `- [ ] ... {#id}`) and render the architecture with `aos-archify` so the canvas review includes the diagram; after the `approve` verdict, Trigger A starts the live map. See the `agenttrail` and `archify` skills.
- Present the aligned plan and hand off to `/startcycle-graph` for execution — write `state.goal` from this session's output and let `/startcycle-graph`'s dispatcher take it from there (see `.agents/graph.md`). This skill does not invoke `/startcycle-graph`'s agents itself; it produces the goal they read.
- For a recurring quality goal, run `/design-control-loop` after shipping (manual, opt-in; not part of the graph).

## Competing Plans

If the brainstorm yields two viable directions, have two different agents each
write a plan file and compare them with the `plan-arbiter` skill before
handing off to `/startcycle-graph`. Review the arbiter's memo in `plan-canvas`.

## Execution Rules
1. **Never skip the debate:** Ideas must be contested by subagents and the user before finalization.
2. **Never build alone:** Always use subagents for implementation.
3. **Never accept ugly UI:** Always apply `godmode-ui-ux` rules.
4. **Never skip architecture & shipping checks:** Always enforce `godmode-engineering` and `godmode-shipping` constraints.
5. **Never dump artifacts blindly:** Always ask the user for the target project directory before creating the plan, README, or `AGENTS.md` files.

To begin the BDBrainstorm process, start by invoking the "grill-me" interview style to question the user's premise, while simultaneously spinning up 2-3 subagents to analyze the initial request from different angles. Once aligned, ask the user for the target directory before writing the project artifacts and spawning development subagents.
