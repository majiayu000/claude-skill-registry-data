---
name: init-advanced
description: >
  Create, rewrite, audit, or refresh repo-wide AI instruction files such as
  AGENTS.md, CLAUDE.md, .cursorrules, or Copilot-style guidance. Use this when
  the user wants to set up a repo, monorepo, package, or subproject for Codex
  or Claude, fix stale or generic agent docs, compare instruction files against
  the real codebase, or generate grounded AI coding guidance from repo
  evidence. Triggers on requests like "make an AGENTS.md", "review my
  CLAUDE.md", "set up this repo for Codex", "prepare this codebase for AI
  agents", "fix my agent docs", or "analyze this project so we can write
  strong instructions". This is the canonical keeper for this workflow and
  supersedes `project-context-seeder`. Do not use for tiny one-rule edits; use
  it for whole-file creation, rewrite, audit, or substantial refresh work.
---

# Init Advanced

Create grounded instruction files from repo evidence, not framework stereotypes.
Produce distinct outputs for Codex/GPT (`AGENTS.md`) and Claude (`CLAUDE.md`).
This skill is the canonical merged entrypoint for repo instruction-file setup,
refresh, and audit work.

<!-- Merged from: context-control (2026-04-05). Legacy material preserved under merged/. -->

## Routing Table

Load only what you need.

| Need | Read |
|---|---|
| Intake questions and missing-context rules | `references/intake-template.md` |
| Repo inspection checklist | `references/repo-analysis-checklist.md` |
| Codex/GPT file calibration | `references/agents-md-playbook.md` |
| Claude file calibration | `references/claude-md-playbook.md` |
| Delivery format and confidence labels | `references/output-template.md` |
| End-to-end workflow, file strategy, and anti-patterns | `references/execution-guide.md` |
| Example final shape | `references/example-output.md` |

## Core Rules

1. Ground commands, paths, and architecture in repo evidence first.
2. Ask only for policy or workflow choices the repo cannot reveal.
3. Keep `AGENTS.md` and `CLAUDE.md` fact-aligned but differently calibrated.
4. Use progressive disclosure: keep this file lean and pull details from `references/`.

## Default Flow

1. Read intake + repo checklist.
2. Inspect manifests, docs, CI, existing instruction files, and a few representative source files.
3. Choose create, rewrite, layered update, or audit.
4. Load the relevant playbook(s), draft the file(s), then verify commands and paths.
5. Deliver using `references/output-template.md`.
