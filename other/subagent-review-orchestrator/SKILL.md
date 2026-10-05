---
name: subagent-review-orchestrator
description: Generate and validate project-scoped Codex subagents for explicit read-heavy exploration, review, security, docs research, browser QA, and trajectory auditing. Use when a repo should expose .codex/agents specialists without bundling global agent config or spawning agents automatically.
---

# Subagent Review Orchestrator

## Purpose

Create narrow project-scoped subagent definitions that can be explicitly spawned for review, research, QA, and trajectory auditing.

## Inspect First

- existing `.codex/agents`
- review docs, security docs, browser QA docs, trajectory risk artifacts, package manifests, architecture docs, and validation scripts
- whether each proposed agent has real repo artifacts to inspect

## Procedure

1. Suggest useful subagents.
   - Run `scripts/suggest_project_subagents.py <repo> --json`.
   - Recommend only agents backed by project artifacts.
   - Do not generate personal `~/.codex/agents` entries or mutate global Codex config.

2. Generate project agents.
   - Run `scripts/generate_project_subagents.py <repo>`.
   - Write standalone TOML files under `.codex/agents/`.
   - Default generated agents are read-only unless a repo explicitly chooses a broader execution agent.

3. Keep agents narrow.
   - `repo-explorer` maps affected code paths and avoids fixes.
   - `reviewer` leads with correctness, security, tests, and regressions.
   - `security-reviewer` focuses on auth, secrets, data, dependencies, and migrations.
   - `docs-researcher` verifies APIs and version-specific behavior.
   - `browser-qa-reviewer` inspects UI paths, accessibility, console/network, and Playwright gaps.
   - `trajectory-auditor` audits task traces, skipped evidence, and risky transitions.

4. Validate agent files.
   - Run `scripts/check_project_subagents.py <repo>`.
   - Confirm required TOML fields exist and that read-heavy agents use read-only sandbox mode.

5. Explain explicit usage.
   - Subagents only run when the user or parent agent explicitly asks Codex to spawn them.
   - Do not treat generated subagents as hooks or daemons.

## Validation

- Run `scripts/suggest_project_subagents.py <repo> --json`.
- Run `scripts/check_project_subagents.py <repo>`.
- Confirm generated agents preserve existing user-edited files unless overwrite is explicitly requested.

## Completion Criteria

- The repo has only useful project-scoped subagents backed by real artifacts.
- Generated subagents are narrow, mostly read-only, and documented as explicit-use specialists.
