---
name: collaborating-with-coco
description: Delegates coding tasks to Coco CLI (Codebase Copilot) for prototyping, debugging, and code review. Use when needing algorithm implementation, bug analysis, or code quality feedback. Supports multi-turn sessions via SESSION_ID.
---

## Quick Start

```bash
python scripts/coco_bridge.py --cd "/path/to/project" --PROMPT "Your task"
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

## Parameters

```
usage: coco_bridge.py [-h] --PROMPT PROMPT --cd CD [--SESSION_ID SESSION_ID] [--return-all-messages] [--model MODEL] [--yolo]
                      [--allowed-tool ALLOWED_TOOL] [--disallowed-tool DISALLOWED_TOOL] [--bash-tool-timeout BASH_TOOL_TIMEOUT]
                      [--query-timeout QUERY_TIMEOUT]

Coco Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to coco.
  --cd CD               Set the workspace root for coco before executing the task.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the coco. Defaults to empty string, start a new session.
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the coco session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --model MODEL         The model to use for the coco session. This parameter is strictly prohibited unless explicitly specified by the user.
  --yolo                Enable YOLO mode - bypass tool permission checks.
  --allowed-tool ALLOWED_TOOL
                        Auto approve on this tool (e.g. 'Bash', 'Edit', 'Write'), can specify multiple times.
  --disallowed-tool DISALLOWED_TOOL
                        Auto reject this tool, can specify multiple times.
  --bash-tool-timeout BASH_TOOL_TIMEOUT
                        Timeout for bash tool, e.g. '30s' (30 seconds), '5m' (5 minutes), '1h' (1 hour).
  --query-timeout QUERY_TIMEOUT
                        Timeout for a single query, e.g. '30s' (30 seconds), '5m' (5 minutes), '1h' (1 hour).
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python scripts/coco_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python scripts/coco_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

## Common Patterns

**Prototyping (request diffs):**
```bash
python scripts/coco_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging"
```

**Debug with full trace:**
```bash
python scripts/coco_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```

**CI/CD integration with allowed tools:**
```bash
python scripts/coco_bridge.py --cd "/project" --allowed-tool Bash --allowed-tool Edit --PROMPT "Fix the failing tests"
```

**YOLO mode for trusted environments:**
```bash
python scripts/coco_bridge.py --cd "/project" --yolo --PROMPT "Refactor the authentication module"
```
