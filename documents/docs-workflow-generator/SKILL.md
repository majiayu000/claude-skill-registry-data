---
name: docs-workflow-generator
description: >-
  Generate a documentation package for new feature work: PRD, task breakdown with skill assignments, roadmap and execution prompt under docs/<initiative>/. Use when asked to create or update the PRD, tasks, roadmap or a planning/docs workflow.
---

# Docs Workflow Generator

Create a consistent documentation package for a feature initiative by scanning the codebase, choosing an initiative folder name, and generating PRD, task files, roadmap and execution prompt. Detailed requirements for each artifact: [references/requirements.md](references/requirements.md).

## Workflow

1. Confirm scope and constraints.
2. Scan the codebase and existing docs.
3. Select the initiative folder name.
4. Create the docs structure.
5. Generate PRD content.
6. Discover available skills and create task files with skill assignments.
7. Generate the roadmap.
8. Validate cross-links and consistency.
9. Generate and display the LLM execution prompt.

## 1. Confirm scope

Ask up to 3 clarifying questions if unclear: feature set and user outcomes, target areas of the codebase, timeline or sequencing constraints, net-new initiative or update of an existing package.

## 2. Scan the codebase

Always do a quick scan before writing docs:
- Read the instructions file (`CLAUDE.md` for Claude Code, `AGENTS.md` for codex, antigravity, gemini and other LLMs) for doc conventions and architecture.
- Check `docs/` for existing initiatives and patterns.
- Use `rg` to locate relevant features, services or Convex files.
- Open a small set of key files that define current behavior.

Goal: identify existing patterns, dependencies and where changes will land, so the PRD and tasks are concrete.

## 3. Select the initiative folder name

Rules for `docs/<initiative>/`:
- Lowercase hyphen-case, 2-4 meaningful keywords, no generic terms like `feature` or `update`.
- Under ~40 characters when possible.
- Reuse a matching existing initiative instead of creating a new folder.
- If scope is meaningfully different, add a short suffix (e.g., `-v2`).

## 4. Create the docs structure

Ensure these exist:
- `docs/<initiative>/PRD.md`
- `docs/<initiative>/roadmap.md`
- `docs/<initiative>/tasks/` and `tasks/_template.md` ([references/templates.md](references/templates.md#task-template))
- `docs/<initiative>/PROMPT.md`

`walkthrough.md` is created by the implementing LLM at the end of work, not by this skill. If `docs/` is missing, create it. Never create a parallel `DOC/` folder.

## 5. PRD content

Model the PRD after existing `docs/*/PRD.md` files. Sections: Summary, Goals, Non-goals, Decisions (Locked), Architecture Overview, Data Model Changes, Backend Design, Frontend and UX Changes, Acceptance Criteria, Risks, and `Execution PRD (Codex-run)`.

**REQUIRED**: the PRD must include a Task and Roadmap Tracking section stating that task files in `docs/<initiative>/tasks/` and the roadmap are updated during implementation (status, decisions, touched files, tests, blockers, next step), and that a `walkthrough.md` is created at the end. Exact wording requirements: `references/requirements.md`.

## 6. Task breakdown with skill assignment

Discover available skills first, following [references/skill-discovery.md](references/skill-discovery.md) (per-LLM instructions file and skills directory, `find . -name SKILL.md`).

Create 6-15 tasks (unless scope requires otherwise), one `TXX-<slug>.md` per task in `docs/<initiative>/tasks/`. Each task file uses the task template, has a goal and checklist, a `Required Skills` section, likely touched files, a minimal TDD/Test Plan, `Status: not-started` and `Last updated` set to today.

## 7. Roadmap

`docs/<initiative>/roadmap.md` with title and last-updated date, the PRD path, a status table listing every task (T01, T02, ...), and a notes section. Statuses start as `not-started` unless the user says otherwise.

## 8. Validation

Before responding:
- Every roadmap task has a matching task file, with matching titles and IDs.
- Dates use `YYYY-MM-DD`.
- No file was overwritten unintentionally.
- The PRD includes the Task and Roadmap Tracking section.
- Every skill referenced in task files exists in the codebase.

## 9. LLM execution prompt

Save a ready-to-use prompt to `docs/<initiative>/PROMPT.md` and display it in full for copy-paste. Template: [references/templates.md](references/templates.md#llm-execution-prompt-template). It must include goal (PRD path and task range), workflow, task update rules, roadmap sync, walkthrough creation, and constraints. Fill placeholders with real task numbers, feature areas and test scenarios.

## Output expectations

Close with a concise summary: initiative name and path, files created or updated, task count, skills discovered and assigned, the full execution prompt, open questions or assumptions.

Stop after docs are generated. Do not implement the feature unless explicitly asked.
