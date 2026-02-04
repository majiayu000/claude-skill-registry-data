---
name: beam-connect
description: "Connect to Beam AI workspace for agent management. Load when user mentions 'beam', 'beam agent', 'beam task', 'beam analytics', 'list agents', 'create task', or any Beam AI operations. Meta-skill that validates config, discovers agents, and routes to appropriate operations."
---

# Beam Connect

**User-facing meta-skill** for Beam AI workspace integration.

## Purpose

Single entry point for all Beam AI operations:
- **Discover** workspace agents
- **Create** and manage tasks
- **Monitor** analytics and performance
- **Debug** failed executions
- **Optimize** tool configurations

Follows the master/connect pattern - references `beam-master` for shared scripts and references.

---

## Trigger Phrases

Load this skill when user says:
- "beam" / "beam ai"
- "list agents" / "show beam agents"
- "create beam task" / "run agent task"
- "beam analytics" / "agent performance"
- "beam task status"
- Any agent name from cached context

---

## Pre-Flight Check (ALWAYS RUN FIRST)

Before ANY Beam operation, validate configuration:

```bash
python 00-system/skills/beam/beam-master/scripts/check_beam_config.py --json
```

### Handle Config Status

| `ai_action` | What to Do |
|-------------|------------|
| `proceed_with_operation` | Config OK → Continue |
| `prompt_for_api_key` | Ask user for API key, save to .env |
| `prompt_for_workspace_id` | Ask user for workspace ID, save to .env |
| `run_setup_wizard` | Run interactive setup |

### If Setup Needed

```
I need to set up Beam AI integration first.

To get your credentials:
1. Log into Beam AI (app.beam.ai)
2. Go to Settings → API Keys
3. Create a new API key
4. Also get your Workspace ID from Settings → Workspace

Please provide:
1. Your Beam API key:
```

After user provides key:
```bash
# Write to .env
BEAM_API_KEY=xxx
BEAM_WORKSPACE_ID=workspace-id

# Re-run config check to verify
python 00-system/skills/beam/beam-master/scripts/check_beam_config.py --json
```

---

## Workflows

### Workflow 0: Config Check (Auto)
**Trigger**: Before any operation
**Script**: `check_beam_config.py --json`
**Output**: Config status, required actions

---

### Workflow 1: List Agents
**Trigger**: "list agents", "show beam agents", "my agents"

```bash
python 00-system/skills/beam/beam-master/scripts/list_agents.py --json
```

**Display Format**:
```
Found 5 agents in your workspace:

1. Customer Support Agent
   ID: abc-123-def
   Type: beam-os
   Created: 2024-01-15

2. Email Processor
   ID: ghi-456-jkl
   ...
```

**Cache agents** for future reference:
- Store agent list in context
- User can reference by name: "run task for Customer Support"

---

### Workflow 2: Get Agent Graph
**Trigger**: "get agent graph", "show agent workflow", "agent config for X"

```bash
python 00-system/skills/beam/beam-master/scripts/get_agent_graph.py --agent-id AGENT_ID --json
```

**Display**: Show nodes, connections, entry/exit points

---

### Workflow 3: Create Task
**Trigger**: "create task", "run agent", "execute agent X"

**Required**: Agent ID, task query
**Optional**: URLs to parse, context files

```bash
python 00-system/skills/beam/beam-master/scripts/create_task.py \
  --agent-id AGENT_ID \
  --query "Task description" \
  --json
```

**Follow-up**: Offer to monitor task progress

```bash
python 00-system/skills/beam/beam-master/scripts/get_task_updates.py --task-id TASK_ID
```

---

### Workflow 4: Get Analytics
**Trigger**: "analytics", "agent performance", "how is X performing"

```bash
python 00-system/skills/beam/beam-master/scripts/get_analytics.py \
  --agent-id AGENT_ID \
  --json
```

**Display**:
```
Analytics for Customer Support Agent (Last 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tasks: 150 total (+15.5%)
├─ Completed: 135 (+12.3%)
└─ Failed: 15 (-5.2%)

Performance:
├─ Avg Eval Score: 87.5 (+4.5%)
├─ Avg Runtime: 45.7s (-8.7%)
└─ Positive Feedback: 120

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Workflow 5: Task Management
**Trigger**: "task status", "retry task", "approve task"

**Get Task Details**:
```bash
python 00-system/skills/beam/beam-master/scripts/get_task.py --task-id TASK_ID --json
```

**Retry Failed Task**:
```bash
python 00-system/skills/beam/beam-master/scripts/retry_task.py --task-id TASK_ID
```

**Approve HITL Task**:
```bash
python 00-system/skills/beam/beam-master/scripts/approve_task.py --task-id TASK_ID
```

**Provide User Input**:
```bash
python 00-system/skills/beam/beam-master/scripts/provide_user_input.py \
  --task-id TASK_ID \
  --input "User response"
```

**Rate Task Output**:
```bash
python 00-system/skills/beam/beam-master/scripts/rate_task_output.py \
  --task-id TASK_ID \
  --node-id NODE_ID \
  --rating positive \
  --feedback "Worked well"
```

---

### Workflow 6: Test & Update Nodes
**Trigger**: "test node", "update node config"

**Test Node**:
```bash
python 00-system/skills/beam/beam-master/scripts/test_graph_node.py \
  --agent-id AGENT \
  --node-id NODE \
  --graph-id GRAPH \
  --input '{"key": "value"}'
```

**Update Node**:
```bash
python 00-system/skills/beam/beam-master/scripts/update_graph_node.py \
  --node-id NODE \
  --objective "New objective"
```

---

### Workflow 7: Tool Optimization
**Trigger**: "optimize tool", "improve tool performance"

**Start Optimization**:
```bash
python 00-system/skills/beam/beam-master/scripts/optimize_tool.py --tool TOOL_NAME
```

**Check Status**:
```bash
python 00-system/skills/beam/beam-master/scripts/get_optimization_status.py --thread-id THREAD
```

---

## Smart Routing

When user mentions:

| Phrase | Route To |
|--------|----------|
| "list agents", "show agents" | Workflow 1 |
| "agent graph", "agent workflow" | Workflow 2 |
| "create task", "run task", "execute" | Workflow 3 |
| "analytics", "performance", "metrics" | Workflow 4 |
| "task status", "retry", "approve" | Workflow 5 |
| "test node", "update node" | Workflow 6 |
| "optimize tool" | Workflow 7 |
| Agent name (from cache) | Show agent details, offer actions |

---

## Error Handling

**Common Errors**:

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Token expired - re-authenticate |
| 403 Forbidden | Check workspace permissions |
| 404 Not Found | Verify agent/task ID |
| Rate Limited | Wait and retry |

**On Error**:
1. Load: `beam-master/references/error-handling.md`
2. Display user-friendly message
3. Offer fix if possible

---

## Context Caching

After listing agents, cache for session:
```python
# Store in conversation context
agents_cache = [
    {"name": "Customer Support", "id": "abc-123"},
    {"name": "Email Processor", "id": "def-456"}
]
```

When user says "run Customer Support", match to cached agent ID.

---

## Integration with Other Beam Skills

This skill can hand off to specialized skills:

| Skill | When to Use |
|-------|-------------|
| `beam-list-agents` | Detailed agent listing |
| `beam-get-agent-graph` | Deep graph analysis |
| `beam-get-agent-analytics` | Extended analytics |
| `beam-create-agent-task` | Task creation with monitoring |
| `beam-debug-issue-tasks` | Debug via Langfuse |

---

## Example Interactions

**User**: "list my beam agents"

**AI**:
```
Let me check your Beam configuration first...
✅ Configuration valid

Found 3 agents in your workspace:

1. Customer Support Agent
   ID: abc-123-def
   Description: Handles customer inquiries

2. Email Processor
   ID: ghi-456-jkl
   Description: Processes incoming emails

3. Report Generator
   ID: mno-789-pqr
   Description: Creates weekly reports

What would you like to do? Options:
- "get analytics for Customer Support"
- "create task for Email Processor"
- "show graph for Report Generator"
```

---

**User**: "create task for Customer Support: Process the latest support ticket"

**AI**:
```
Creating task for Customer Support Agent...

✅ Task Created!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task ID: AGE-785
Status: QUEUED
Query: Process the latest support ticket

Would you like me to monitor this task for updates?
```

---

## Version

**Version**: 1.0
**Created**: 2025-12-11
**Status**: Production Ready
