---
name: parse-conversation-timeline
description: Transform raw session logs into structured timeline JSON for protocol audit analysis
allowed-tools: Read, Bash, Grep, LS, Skill
---

# Parse Conversation Timeline Skill

**Purpose**: Transform 6MB raw conversation logs into 100-300KB structured timelines that auditors can query for compliance and efficiency analysis.

**When to Use**:
- Before running protocol compliance audits
- Before running protocol efficiency audits
- When investigating specific task execution patterns
- To analyze conversation structure and event sequencing

## Skill Workflow

**Overview**: Parse conversation.jsonl → structured timeline JSON with events, file classifications, state transitions, git status, and statistics.

### Phase 1: Access Conversation Data

**Get Session ID** from SessionStart system reminder:
```
✅ Session ID: 88194cb6-734b-498c-ab5d-ac7c773d8b34
```

**Access conversation logs**:
```bash
# REQUIRED: Use session ID from system reminder
SESSION_ID="88194cb6-734b-498c-ab5d-ac7c773d8b34"

# Verify session ID is provided
if [ -z "$SESSION_ID" ]; then
  echo "ERROR: Session ID not available in context." >&2
  exit 1
fi

# Main session conversation
CONV_FILE="/home/node/.config/projects/-workspace/${SESSION_ID}.jsonl"

# Verify conversation file exists
if [ ! -f "$CONV_FILE" ]; then
  echo "ERROR: Conversation file not found: $CONV_FILE" >&2
  exit 1
fi
```

### Phase 2: Parse Timeline Events

Extract chronological events from conversation:

```bash
# Parse all events into structured timeline
jq -c 'select(.type == "user" or .type == "assistant") | {
  timestamp,
  type: (if .type == "user" then "user_message"
         elif (.message.content[]? | select(.type == "tool_use")) then "tool_use"
         elif (.message.content[]? | select(.type == "tool_result")) then "tool_result"
         else "assistant_message" end),
  actor: (if .type == "user" then "user" else "main" end),
  context: {cwd, branch: .gitBranch},
  content: .message.content
}' "$CONV_FILE"
```

**Event Types**:
1. **user_message**: User input to main agent
2. **assistant_message**: Main agent text output (non-tool)
3. **tool_use**: Any tool invocation (Edit, Write, Bash, Task, Read)
4. **tool_result**: Output from tool execution
5. **state_transition**: Detected task state change (inferred from TodoWrite or task.json)

### Phase 3: Classify File Operations

For each Edit/Write tool use, classify the target file and worktree:

```bash
# File type classification
classify_file_type() {
  local file_path="$1"
  case "$file_path" in
    */src/main/java/*.java) echo "source_file" ;;
    */src/test/java/*.java) echo "test_file" ;;
    */module-info.java|*/pom.xml|*.gradle) echo "infrastructure" ;;
    *.md|*.txt) echo "documentation" ;;
    *) echo "other" ;;
  esac
}

# Worktree type classification
classify_worktree() {
  local cwd="$1"
  case "$cwd" in
    /workspace/main*) echo "main_worktree" ;;
    /workspace/tasks/*/code) echo "task_worktree" ;;
    /workspace/tasks/*/agents/*/code) echo "agent_worktree" ;;
    *) echo "unknown" ;;
  esac
}
```

### Phase 4: Detect State Transitions

Infer state transitions from conversation:

```bash
# Method 1: TodoWrite tool calls mentioning states
jq -r 'select(.type == "assistant") |
  .message.content[]? |
  select(.type == "tool_use" and .name == "TodoWrite") |
  .input.todos[]? |
  select(.content | contains("SYNTHESIS") or contains("IMPLEMENTATION") or contains("VALIDATION"))' \
  "$CONV_FILE"

# Method 2: Infer from working directory changes and Task tool patterns
# INIT → CLASSIFIED: First Task tool invocation
# CLASSIFIED → REQUIREMENTS: Multiple parallel Task tools (review mode)
# REQUIREMENTS → SYNTHESIS: After all agents in review mode complete
# SYNTHESIS → IMPLEMENTATION: CD to task worktree + Task tools (implementation mode)
```

### Phase 5: Extract User Approval Checkpoints

Search for user approvals after critical state transitions:

```bash
# Extract user messages and check for approval patterns
jq -c 'select(.type == "user") | {
  timestamp,
  content: .message.content,
  is_approval: (.message.content | test("(?i)(yes|approve|proceed|continue|go ahead|lgtm|looks good)"))
}' "$CONV_FILE"
```

### Phase 6: Collect Current Git and Task State

Gather filesystem state to complement timeline:

```bash
# Task state
if [ -f "/workspace/tasks/${TASK_NAME}/task.json" ]; then
  cat "/workspace/tasks/${TASK_NAME}/task.json"
fi

# Git worktrees
git worktree list

# Git branches and merge status
cd /workspace/main
git branch --contains ${TASK_BRANCH_HEAD} 2>/dev/null | grep -q "main" && echo "MERGED" || echo "NOT_MERGED"

# Agent outputs (if applicable)
ls -la "/workspace/tasks/${TASK_NAME}/"*-requirements.md 2>/dev/null || true
```

### Phase 7: Generate Statistics

Compute aggregate statistics:

```bash
# Count events by type
# Count tool uses by tool name
# Count state transitions
# Identify agents invoked (Task tool calls)
# Detect approval checkpoints vs required checkpoints
```

## Output Format

**Structured Timeline JSON** - Comprehensive, queryable data:

```json
{
  "session_metadata": {
    "session_id": "88194cb6-734b-498c-ab5d-ac7c773d8b34",
    "task_name": "implement-formatter-api",
    "start_timestamp": "2025-10-30T14:58:00Z",
    "end_timestamp": "2025-10-30T20:24:59Z",
    "conversation_file": "~/.config/projects/-workspace/88194cb6-....jsonl",
    "conversation_size_bytes": 6046009
  },

  "timeline": [
    {
      "timestamp": "2025-10-30T14:58:00Z",
      "seq": 1,
      "type": "user_message",
      "content": "Work on implement-formatter-api task",
      "context": {
        "cwd": "/workspace/main",
        "branch": "main"
      }
    },
    {
      "timestamp": "2025-10-30T14:58:20Z",
      "seq": 3,
      "type": "tool_use",
      "actor": "main",
      "tool": {
        "name": "Edit",
        "input": {
          "file_path": "/workspace/tasks/.../FormattingRule.java"
        }
      },
      "context": {
        "cwd": "/workspace/tasks/implement-formatter-api/agents/architect/code",
        "branch": "implement-formatter-api-architect"
      },
      "file_classification": {
        "type": "source_file",
        "worktree_type": "agent_worktree",
        "agent": "architect"
      }
    },
    {
      "timestamp": "2025-10-30T15:02:00Z",
      "seq": 5,
      "type": "state_transition",
      "from_state": "SYNTHESIS",
      "to_state": "IMPLEMENTATION",
      "trigger": "main_agent",
      "user_approval_found": false,
      "context": {
        "cwd": "/workspace/tasks/implement-formatter-api/code",
        "branch": "implement-formatter-api"
      }
    }
  ],

  "git_status": {
    "current_branch": "main",
    "branches": [
      {
        "name": "implement-formatter-api",
        "head": "def456",
        "merged_to_main": false,
        "task_complete_but_not_merged": true
      }
    ],
    "worktrees": [
      {
        "path": "/workspace/tasks/implement-formatter-api/code",
        "branch": "implement-formatter-api",
        "head": "def456",
        "pruned": false
      }
    ]
  },

  "task_state": {
    "task_json": {
      "exists": true,
      "path": "/workspace/tasks/implement-formatter-api/task.json",
      "state": "COMPLETE"
    },
    "module_in_main": {
      "exists": false,
      "expected_path": "/workspace/main/formatter"
    },
    "agent_outputs": {
      "architect": {
        "file": "implement-formatter-api-architect-requirements.md",
        "exists": true
      }
    }
  },

  "statistics": {
    "total_events": 150,
    "user_messages": 5,
    "tool_uses": {
      "Edit": 26,
      "Write": 15,
      "Bash": 50,
      "Task": 4,
      "Read": 30
    },
    "state_transitions": 6,
    "agents_invoked": ["architect", "engineer", "formatter"],
    "approval_checkpoints": {
      "after_synthesis": {
        "required": true,
        "found": false,
        "transition_timestamp": "2025-10-30T15:02:00Z"
      }
    }
  }
}
```

## Critical Rules

**DO**:
- ✅ Parse entire conversation into chronological timeline
- ✅ Include ALL event types (user messages, tool uses, results, state transitions)
- ✅ Preserve working directory and git branch context for every event
- ✅ Classify file operations (source/test/infrastructure/documentation)
- ✅ Classify worktree types (main/task/agent worktrees)
- ✅ Extract user approval patterns
- ✅ Compute aggregate statistics
- ✅ Verify current git and task state
- ✅ Keep timeline comprehensive (any auditor can query it)

**DON'T**:
- ❌ Filter timeline based on what you think auditors need
- ❌ Pre-compute specific compliance checks (auditors will query timeline)
- ❌ Make judgments about violations (just provide data)
- ❌ Make recommendations (that's auditors' job)
- ❌ Skip events to save tokens (timeline must be complete)
- ❌ Interpret intent or make assumptions

## Verification Checklist

Before outputting structured timeline JSON:
- [ ] session_metadata section complete with session ID, task name, timestamps
- [ ] timeline array contains ALL events in chronological order
- [ ] Each timeline event has timestamp, seq, type, context fields
- [ ] Tool uses include working directory and git branch context
- [ ] File operations classified by type and worktree
- [ ] State transitions detected and recorded
- [ ] git_status section includes branches, worktrees, merge status
- [ ] task_state section includes task.json, module existence, agent outputs
- [ ] statistics section includes event counts, tool usage, approval checkpoints
- [ ] JSON is valid and parseable
- [ ] No compliance judgments included (data only)

## Related Skills

- **get-history**: Access raw conversation logs
- **audit-protocol-compliance**: Use timeline to check protocol violations
- **audit-protocol-efficiency**: Use timeline to find efficiency improvements
