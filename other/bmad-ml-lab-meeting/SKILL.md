---
name: bmad-ml-lab-meeting
description: 'Run an AI Lab division meeting with research and build agents (no AI Startup agents). Use when the user requests to "start a lab meeting", "convene the lab", or "run a sprint retrospective for the lab".'
---

Follow the instructions in ./workflow.md.

## Optional: Agent Teams (Claude Code)

**When to use.** If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set at session start, assemble a team instead of dispatching serially. Nosh is team lead; the 13 AI Lab specialists are teammates (8 Research: `bmad-sova`, `bmad-sage`, `bmad-cypher`, `bmad-viper`, `bmad-breach`, `bmad-fade`, `bmad-astra`, `bmad-killjoy`; 5 Build: `bmad-chamber`, `bmad-jett`, `bmad-gekko`, `bmad-omen`, `bmad-kayo`). Team coordination happens via the shared task list and inter-agent mailbox.

**Fallback contract.** If the env var is unset, this workflow runs as serial Task-tool invocations per `./workflow.md`. Users who don't opt in see no behavior change. The installer never writes `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; users export it from their shell.
