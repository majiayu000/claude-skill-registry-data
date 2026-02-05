---
name: task-debugger
description: Debug and fix Taskcluster task failures
---

## Setup

**Taskcluster CLI:**
```bash
taskcluster version  # check if installed
export TASKCLUSTER_ROOT_URL=https://firefox-ci-tc.services.mozilla.com
```
If not installed: https://github.com/taskcluster/taskcluster/releases/latest/

**Commands:**
- `taskcluster task log <task-id>` - Get logs
- `taskcluster task def <task-id>` - Get definition (optional)

## Debug Process

1. Extract task ID from message or URL
2. Fetch logs: `taskcluster task log <task-id>`
3. Analyze errors (tracebacks, test failures, build errors)
4. If fix is obvious → apply it. Otherwise → reproduce locally:
   - Docker-worker tasks: `taskgraph load-task --develop <task-id>` (Firefox: `./mach taskgraph`, others: check virtualenv or `uv run taskgraph`)
   - Flags: `--interactive`, `--volume`, `--root`, `--image`, `--keep`
   - Non-docker: extract command from task def and run locally
5. For non-obvious issues: add debug statements → iterate → fix
6. Verify fix using same reproduction method
7. **Clean up** debug artifacts (don't re-verify after cleanup)
8. Report: root cause, fix, verification, files changed
