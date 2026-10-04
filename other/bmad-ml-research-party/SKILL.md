---
name: bmad-ml-research-party
description: 'Run multi-agent research discourse session. Use when the user requests to "start a research party" or "run a journal club".'
---

Follow the instructions in ./workflow.md.

## Optional: Agent Teams (Claude Code)

**When to use.** If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set at session start, assemble a team instead of dispatching serially. Nosh is team lead; the default roster is `bmad-sova` (lit survey), `bmad-cypher` (mechanistic interp), `bmad-viper` (empirical), `bmad-killjoy` (eval), `bmad-fade` (theory). The roster is user-configurable per session — swap in other Research or Build specialists as needed.

**Fallback contract.** If the env var is unset, this workflow runs as serial Task-tool invocations per `./workflow.md`. Users who don't opt in see no behavior change. The installer never writes `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; users export it from their shell.
