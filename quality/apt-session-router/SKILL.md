---
name: apt-session-router
description: Start-of-session router for APT work in Cursor. Identify the child repo, load local instructions, classify the task, then pick the cheapest sufficient Task model.
title: "APT Session Router"
kind: "platform-adapter"
domain: "platforms"
status: "active"
owner: "APT"
last_updated: "2026-09-06"
source_paths: ["apt-principles-agents/platforms/cursor/source/skills/apt-session-router/SKILL.md"]
---

# APT Session Router

Use at the start of a Cursor session in the Applied Practical Thinking workspace or any installed target repo.

## Process

1. Run the clarify-before-acting skill. Stop if the owning repo, outcome, or plan-versus-implement choice is missing.
2. Identify the child repository. Do not treat the workspace root as an app.
3. Read that repo's `README.md`, `AGENTS.md`, `.apt/installation.json` when present, and `docs/project-context.md` when present.
4. Build a compact task packet: goal, scope, risk, Working Backwards status, validation command, approval gates.
5. Classify the next step as read, design, implement, test, or review.
6. Choose capability from the dated map in `.cursor/routing/cursor-model-map.md` (or `platforms/cursor/source/routing/cursor-model-map.md` in the doctrine repo). Use Task subagents with those slugs. Do not put slugs into doctrine files.
7. For product work without an approved Working Backwards package, stay in intake. Do not implement from an unapproved package.

## Quality bar

The session names the repo, task class, and tier before expensive work. Reads stay on a cheap explore model. Humans approve protected changes.
