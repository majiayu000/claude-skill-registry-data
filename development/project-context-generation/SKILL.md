---
name: project-context-generation
description: Guidance for analyzing a repository and creating concise, high-value AGENTS.md and related instruction context for future agent sessions.
compatibility: opencode
metadata:
  audience: context-builders
  purpose: project-guidance
---
## Core approach

- Build a mental model of the repository first.
- Capture only the instructions future sessions are likely to need repeatedly.
- Prefer concise, actionable guidance over long prose.
- Focus on facts visible from the repo unless a key ambiguity requires a clearly labeled assumption.

## What to capture

- build, test, lint, and verification commands
- command ordering when it matters
- project structure and module boundaries that are not obvious from names alone
- important stack conventions, coding patterns, and workflow expectations
- setup quirks, operational gotchas, and environment assumptions
- references to other existing rules or standards files when they should be pulled in through config
- code intelligence output (from `hero scan`) — package structure, key symbols, dependency graph, and hot files that help orient future sessions

## Guardrails

- Do not restate the whole codebase.
- Do not add generic advice that is not specific to the project.
- Improve existing `AGENTS.md` in place when present.
- Keep the file useful for future agent execution, not as a general project README.
