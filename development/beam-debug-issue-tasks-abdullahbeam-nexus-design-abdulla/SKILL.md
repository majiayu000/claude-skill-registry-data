---
name: beam-debug-issue-tasks
description: Debug failed/issue tasks from Beam.ai using Langfuse traces. Load when user says "debug issue tasks", "check failed tasks", "why did task fail", "task errors", "debug agent", or needs to investigate task failures.
---

# Beam Debug Issue Tasks

**Debug failed Beam.ai tasks using Langfuse traces.**

## When to Use

- Diagnose why a task failed, stopped, or needs input
- Find root cause from Langfuse trace reasoning
- Generate debug reports for documentation or handoff

---

## Prerequisites

`.env` file at project root:

```
# Beam.ai - BID instance
BEAM_API_KEY=your_bid_api_key
BEAM_WORKSPACE_ID=your_bid_workspace_id

# Beam.ai - Prod instance
BEAM_API_KEY_PROD=your_prod_api_key
BEAM_WORKSPACE_ID_PROD=your_prod_workspace_id

# Langfuse (self-hosted)
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://tracing.beamstudio.ai
```

**Dependencies**: `pip install requests python-dotenv`

---

## Quick Start

```bash
# List issue tasks (default: last 1 day, BID workspace)
python 03-skills/beam-debug-issue-tasks/scripts/debug_issue_tasks.py <agent_id>

# Debug specific task with full trace analysis
python 03-skills/beam-debug-issue-tasks/scripts/debug_issue_tasks.py <agent_id> --task-id <task_id>

# Use prod workspace
python 03-skills/beam-debug-issue-tasks/scripts/debug_issue_tasks.py <agent_id> --workspace prod
```

---

## Workspaces

| Workspace | API Endpoint | Langfuse Project |
|-----------|--------------|------------------|
| `bid` (default) | api.bid.beamstudio.ai | cmauxbgww000582ry4644c2qr |
| `prod` | api.beamstudio.ai | clw5gbhuy0003u3rv4jzzoesh |

---

## Issue Statuses

Tasks are flagged as "issue" if status is:
- `FAILED` - Execution failed
- `ERROR` - Processing error
- `STOPPED` - Condition failed
- `CANCELLED` - User cancelled
- `TIMEOUT` - Execution timeout
- `USER_INPUT_REQUIRED` - Missing input data

---

## Debug Reports

Reports saved to: `04-workspace/agents/{agent_name}/debug/`

**Format**: Smart Brevity (headline, takeaway, why it matters, details, fix)

**Key spans analyzed**:
- `ParameterSelection/v2` - How parameters were matched
- `ExecuteGPT_Tool/v1` - Tool execution reasoning
- `NodeSelection:EdgeEvaluation/v1` - Routing decisions
- `TaskSuccessCriteriaCheck/v1` - Why task stopped

---

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `agent_id` | Beam agent ID (required) | - |
| `--workspace`, `-w` | Workspace: bid or prod | bid |
| `--days`, `-d` | Look back period (1, 3, 7, 14, 30) | 1 |
| `--task-id`, `-t` | Debug specific task ID | - |
| `--summary`, `-s` | Show grouped summary | false |
| `--limit`, `-l` | Max tasks to show | 10 |
| `--output`, `-o` | Save to JSON file | - |
| `--no-trace` | Skip Langfuse lookup | false |

---

## Example Output

### Debug Report (Smart Brevity)

```markdown
# Task stopped: condition failed

Checklist evaluation: subfolder must equal 'Schreiben Schuldner' but was null.

**Why it matters**: This task did not complete successfully and may need attention.

**The details**:
- **Status**: `STOPPED`
- **Task**: `ab3cbbb8-28da-41aa-b726-25931d14d7d4`
- **Latency**: 159.6s
- **Cost**: $0.1043

**Key spans**:
- NodeSelection:EdgeEvaluation/v1 (23.4s)
- TaskSuccessCriteriaCheck/v1 (7.2s)

**Root cause**:
> The criterion is not met because subfolder is not set to required value.

**Fix**: Review the condition that stopped execution. Check if input data meets requirements.
```

---

## Langfuse Links

Each report includes direct links:
- **Session URL**: All traces for the task
- **Trace URL**: Specific execution with full details

---

## Error Handling

| Error | Solution |
|-------|----------|
| `BEAM_API_KEY not found` | Add to .env |
| `Invalid workspace` | Check workspace parameter (bid/prod) |
| `No traces found` | Verify agent has Langfuse integration |
| `401 Unauthorized` | Verify API keys |

---

## Related Skills

- `beam-get-agent-analytics` - Performance metrics
- `beam-create-agent-task` - Create test tasks
- `beam-list-agents` - List available agents
