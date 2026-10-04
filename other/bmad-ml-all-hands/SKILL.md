---
name: bmad-ml-all-hands
description: 'Run a cross-division all-hands meeting that includes both AI Lab and AI Startup agents. Use when the user requests to "start an all-hands", "convene both divisions", or "run a cross-division meeting".'
---

Follow the instructions in ./workflow.md.

## Optional: Agent Teams (Claude Code)

**When to use.** If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set at session start, assemble a team instead of dispatching serially. Nosh is team lead; all 20 specialists are teammates across both divisions — AI Lab (8 Research: `bmad-sova`, `bmad-sage`, `bmad-cypher`, `bmad-viper`, `bmad-breach`, `bmad-fade`, `bmad-astra`, `bmad-killjoy`; 5 Build: `bmad-chamber`, `bmad-jett`, `bmad-gekko`, `bmad-omen`, `bmad-kayo`) plus AI Startup (`bmad-dumbledore`, `bmad-hermione`, `bmad-snape`, `bmad-luna`, `bmad-mcgonagall`, `bmad-moody`, `bmad-hagrid`). Team coordination happens via the shared task list and inter-agent mailbox.

**Fallback contract.** If the env var is unset, this workflow runs as serial Task-tool invocations per `./workflow.md`. Users who don't opt in see no behavior change. The installer never writes `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; users export it from their shell.
