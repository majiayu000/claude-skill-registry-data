---
name: bot
description: >
  The Universal Autonomous Entity Standard. A local-first framework for
  observable, composable agents with policy-guarded execution on ClawHub.
---
# BOT: Standardized Agent Framework

bot is a local-first agent framework for observable execution, composable tool use, and multi-agent orchestration.

## Safety Model
- Network: Core demos do not initiate outbound network requests by default.
- Execution: This release provides policy-guarded local execution, not OS-level sandbox isolation.
- File System: Local memory is stored in `./.bot_memory/` by default, configurable via `BOT_MEMORY_DIR`.
- Viewer: Optional local monitor binds to `127.0.0.1` only when explicitly started.
- Credentials: No external API keys required for core demos.

## Included Capabilities
- Single-agent reasoning core
- Botfile static declaration
- TUI thought visualization
- Crypto identity and signing
- Multi-agent coordination
- Local Web thought-tree viewer
- Unified local run entrypoint
- Capability-aware tool registration
- Policy-guarded execution layer

## Quick Start
```bash
PYTHONPATH=. python3 examples/run_bot.py --mode multi --prompt "Design a safe local-first agent workflow"
```

## Custom Roles
```bash
PYTHONPATH=. python3 examples/run_bot.py --mode multi --roles "planner_bot,critic_bot,executor_bot,auditor_bot"
```

## Single-Agent Mode
```bash
PYTHONPATH=. python3 examples/run_bot.py --mode single --prompt "Summarize this task safely"
```

Then open:
- http://127.0.0.1:8765
