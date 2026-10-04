---
name: bmad-ml-startup-meeting
description: 'Run an AI Startup division meeting with the seven AI Startup agents (no AI Lab agents). Use when the user requests to "start a startup meeting", "convene the startup team", or "run a sprint review for the product".'
---

Follow the instructions in ./workflow.md.

## Optional: Agent Teams (Claude Code)

**When to use.** If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set at session start, assemble a team instead of dispatching serially. Nosh is team lead; the 7 AI Startup specialists are teammates (`bmad-dumbledore`, `bmad-hermione`, `bmad-snape`, `bmad-luna`, `bmad-mcgonagall`, `bmad-moody`, `bmad-hagrid`). Team coordination happens via the shared task list and inter-agent mailbox, with phase-gate approvals still enforced by the workflow.

**Fallback contract.** If the env var is unset, this workflow runs as serial Task-tool invocations per `./workflow.md`. Users who don't opt in see no behavior change. The installer never writes `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; users export it from their shell.
