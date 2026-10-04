---
name: parallel
description: "Run multi-agent parallel workflow through Trellis plan/start/status pipeline."
---
# Multi-Agent Parallel Workflow

Use this skill when work should be parallelized through Trellis multi-agent pipeline.

## Goal

- Keep orchestrator work in the main repo.
- Run code implementation inside linked worktrees.
- Track each task with task metadata and registry records.

## Quick Start

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/multi_agent/plan.py --name "<feature>" --type "<backend|frontend|fullstack>" --requirement "<requirement>"
python3 ./.trellis/scripts/multi_agent/start.py "<task-dir>" --platform <claude|opencode|codex>
python3 ./.trellis/scripts/multi_agent/status.py
```

## Platform Notes

- `claude` and `opencode`: background CLI agent is started automatically.
- `codex`: manual mode. The script prepares worktree and context, then continue inside Codex in that worktree.

## Completion

- Monitor progress with `status.py`.
- Cleanup worktrees with `cleanup.py` after tasks are merged or archived.
