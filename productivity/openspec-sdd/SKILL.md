---
name: openspec-sdd
description: Use OpenSpec for formal spec-driven development. Use when a feature, refactor, or product change should be proposed, designed, task-planned, validated, synced, or archived through openspec/ artifacts before or during implementation.
---

# OpenSpec SDD

## Purpose

Run a formal OpenSpec workflow so feature work has proposal, requirements, design, tasks, validation, and archive history instead of living only in chat or ad hoc docs.

## Inspect First

- `openspec/`, existing specs, active changes, archived changes, and OpenSpec config
- product docs, architecture docs, tests, routes, schemas, and previous feature specs
- package manager, Node version, and whether `openspec` is installed

## Procedure

1. Detect OpenSpec state.
   - If `openspec/` is missing, recommend `npm install -g @fission-ai/openspec@latest` or project-native equivalent, then `openspec init`.
   - If OpenSpec exists, preserve active changes and current specs.
   - Set `OPENSPEC_TELEMETRY=0` when CI or privacy-sensitive automation needs telemetry disabled.

2. Start or continue the change.
   - Use `/opsx:propose "<idea>"` for the default workflow.
   - Use expanded commands such as `/opsx:new`, `/opsx:continue`, `/opsx:ff`, and `/opsx:verify` only when the repo has that profile enabled.
   - Each change should have `proposal.md`, `design.md`, `tasks.md`, and delta specs under `openspec/changes/<change-name>/`.

3. Keep artifacts executable.
   - Requirements use ADDED, MODIFIED, or REMOVED sections and scenario examples.
   - Tasks are checkboxes tied to validation evidence.
   - Design names affected modules, APIs, schemas, tests, rollout risk, and docs.
   - Use `assets/templates/openspec-change-notes.md.tmpl` for local notes when needed.
   - Use `$research-first-change` when the change depends on current external APIs, framework behavior, security guidance, or dependency choices.

4. Validate and sync.
   - Add or update target repo `scripts/check-openspec` when OpenSpec is part of the workflow.
   - Use `scripts/check_openspec.py` for lightweight local inventory, including active changes and per-change delta spec files.
   - Run `openspec validate <change-name>` when the CLI is available.
   - After implementation, use `/opsx:sync` or `/opsx:archive` according to the active workflow.

5. Route follow-on skills.
   - Use `task-planning-and-pr-protocol` for implementation planning.
   - Use `feature-state-machine` to map OpenSpec tasks to feature IDs, WIP state, verification commands, and passing evidence.
   - Use `tdd-playwright-workflow` for red-green-refactor tasks.
   - Use `agent-reviewer` to confirm implementation matches OpenSpec tasks and requirements.

## Validation

- Run `./scripts/check-openspec` when present.
- Run `openspec list`, `openspec show <change-name>`, and `openspec validate <change-name>` when the CLI is available.
- Confirm proposal, design, tasks, and delta specs agree with the implemented behavior.

## Completion Criteria

- The feature has an OpenSpec change or a documented reason OpenSpec is unnecessary.
- Requirements are scenario-based and implementation tasks are checkable.
- Active changes are validated before implementation and archived or synced after completion.
