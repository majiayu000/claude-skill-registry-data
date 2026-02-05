---
name: get-history
description: Access raw conversation history from Claude Code session storage for audit and analysis
---

# Get History Skill

**Purpose**: Provide direct access to raw, unfiltered conversation history stored by Claude Code for audit trails, compliance verification, and conversation analysis.

**When to Use**:
- During `/audit-session` to provide raw conversation data to parse-conversation-timeline skill
- When investigating protocol violations or agent behavior
- To verify user approval checkpoints in conversation
- To analyze tool call sequences and working directory context
- When main agent's filtered summaries are insufficient

## Skill Capabilities

### 1. Access Current Session Conversation

**Location**: `/home/node/.config/projects/-workspace/{session-id}.jsonl`

**Session ID Detection**:

**REQUIRED**: The session ID is automatically provided via the `get-session-id` skill (SessionStart hook).

Look for the system reminder in context:
```
✅ Session ID: 88194cb6-734b-498c-ab5d-ac7c773d8b34
```

Then use it directly:
```bash
# Use the session ID from system reminder
SESSION_ID="88194cb6-734b-498c-ab5d-ac7c773d8b34"

# Access conversation file
cat /home/node/.config/projects/-workspace/${SESSION_ID}.jsonl
```

**If session ID not found in context**:
```bash
echo "ERROR: Session ID not available in context. Cannot access conversation logs." >&2
echo "The session ID should be provided by get-session-id skill at SessionStart." >&2
exit 1
```

### 2. Parse Conversation Structure

**Entry Types**:
- `type: "summary"` - High-level conversation summary
- `type: "message"` - User or assistant messages
- `type: "tool_use"` - Tool invocations
- `type: "tool_result"` - Tool outputs

**Extract Messages**:
```bash
# Get all user messages
jq 'select(.type == "message" and .role == "user") | .content' conversation.jsonl

# Get all assistant messages
jq 'select(.type == "message" and .role == "assistant") | .content' conversation.jsonl

# Get all tool uses with names
jq 'select(.type == "tool_use") | {name: .name, input: .input}' conversation.jsonl
```

### 3. Verify User Approval Checkpoints

**Search Patterns**:
```bash
# Look for approval-related user messages
jq -r 'select(.type == "message" and .role == "user") | .content' conversation.jsonl | \
  grep -iE "(approve|proceed|continue|go ahead|yes|looks good|lgtm)"

# Look for agent waiting for approval
jq -r 'select(.type == "message" and .role == "assistant") | .content' conversation.jsonl | \
  grep -iE "(waiting for approval|user approval required|proceed\?|continue\?)"
```

### 4. Extract Tool Call Context

**Get Working Directory for Each Tool Call**:
```bash
# For each Edit/Write operation, check if pwd or cd preceded it
jq -r 'select(.type == "tool_use" and (.name == "Edit" or .name == "Write")) |
  {tool: .name, file: .input.file_path, timestamp: .timestamp}' conversation.jsonl

# Look for Bash calls that changed directory before Edit/Write
jq -r 'select(.type == "tool_use" and .name == "Bash" and
  (.input.command | contains("cd "))) | .input.command' conversation.jsonl
```

### 5. Agent Invocation Analysis

**Extract All Task Tool Calls**:
```bash
# Get all agent invocations with prompts
jq 'select(.type == "tool_use" and .name == "Task") |
  {agent: .input.subagent_type, description: .input.description,
   prompt: .input.prompt[0:200]}' conversation.jsonl
```

## Usage in /audit-session

### Phase 1: Process-Recorder Integration

**Replace filtered data with raw conversation access**:

```markdown
**CRITICAL**: Main agent MUST NOT provide filtered summaries. parse-conversation-timeline skill uses
get-history skill to access raw conversation independently.

**Mandatory Actions**:
1. Use get-history skill to get current session conversation file
2. Parse conversation for:
   - User messages (approval checkpoints)
   - Tool uses (Edit/Write with working directory context)
   - Task invocations (agent delegation sequence)
   - Bash commands (directory changes, git operations)
3. Extract objective facts WITHOUT main agent interpretation
4. Output raw data to audit-protocol-compliance skill
```

### Phase 2: Compliance Review Integration

**Use raw conversation data for verification**:

```markdown
**Check 1.0: User Approval Checkpoints**
- Input: Raw user messages from conversation
- Search: Messages containing approval after SYNTHESIS/REVIEW states
- Verdict: PASS if approval found, FAIL if proceeded without approval

**Check 1.3: Working Directory Violations**
- Input: Bash cd commands + Edit/Write file paths
- Correlate: Did main agent cd to agent worktree before Edit/Write?
- Verdict: FAIL if any Edit/Write in /workspace/tasks/{task}/agents/{agent}/code
```

## Conversation File Structure

### Main Session File
**Path**: `/home/node/.config/projects/-workspace/{session-id}.jsonl`

**Format**: JSON Lines (one JSON object per line)

**Example Entry Structure**:
```json
{"type":"message","role":"user","content":"Work on implement-formatter-api","timestamp":1730331600000}
{"type":"message","role":"assistant","content":"I'll help with that task...","timestamp":1730331610000}
{"type":"tool_use","name":"Task","input":{"subagent_type":"architect","prompt":"..."}}
{"type":"tool_result","tool_use_id":"xyz","content":"Agent output..."}
```

### Agent Sidechain Conversations
**Path Pattern**: `/home/node/.config/projects/-workspace/agent-{agent-id}.jsonl`

**Format**: JSON Lines (same format as main session)

**Discovery**:
```bash
# Find all agent sidechain logs
ls -lht ~/.config/projects/-workspace/agent-*.jsonl | head -10

# Find agent logs for specific session
grep -l "sessionId.*88194cb6-734b-498c-ab5d-ac7c773d8b34" \
  ~/.config/projects/-workspace/agent-*.jsonl

# Get most recent agent execution
ls -t ~/.config/projects/-workspace/agent-*.jsonl | head -1
```

**Agent Log Structure**:
```json
{"isSidechain":true,"agentId":"a74f3744","type":"user","message":{"role":"user","content":"..."}}
{"isSidechain":true,"agentId":"a74f3744","type":"assistant","message":{"role":"assistant","content":[...]}}
{"isSidechain":true,"agentId":"a74f3744","type":"user","message":{"role":"user","content":[{"type":"tool_result","content":"..."}]}}
```

**Key Fields**:
- `isSidechain: true` - Identifies agent execution vs main conversation
- `agentId` - Unique identifier for this agent invocation
- `sessionId` - Links back to parent session
- `cwd` - Working directory for agent execution
- `agentName` - Optional agent type name

**Analyzing Agent Tool Errors**:
```bash
# Find tool errors in agent execution
grep -i "no such tool\|error" ~/.config/projects/-workspace/agent-{agent-id}.jsonl

# Extract failed tool calls
jq 'select(.type == "user" and .message.content[].is_error == true) |
    .message.content[]' agent-{agent-id}.jsonl

# Count tool usage by type
jq -r 'select(.type == "assistant") |
    .message.content[] |
    select(.type == "tool_use") |
    .name' agent-{agent-id}.jsonl | sort | uniq -c
```

**Linking Agent Invocation to Sidechain Log**:
```bash
# From main session, find Task invocation
jq 'select(.type == "tool_result" and .toolUseResult.agentId != null) |
    {timestamp: .timestamp, agentId: .toolUseResult.agentId, status: .toolUseResult.status}' \
    {session-id}.jsonl

# Then open corresponding agent log
cat ~/.config/projects/-workspace/agent-{agentId}.jsonl
```

### Historical Data
**Path**: `/home/node/.config/history.jsonl`

**Format**: High-level history entries with display summaries

## Error Handling

**If session ID not in context**:

The session ID is REQUIRED and automatically provided at SessionStart. Look for:
```
✅ Session ID: {uuid}
```

**If not found**:
```bash
echo "ERROR: Session ID not available in context." >&2
echo "Expected system reminder: '✅ Session ID: {uuid}'" >&2
echo "Provided by get-session-id skill at SessionStart." >&2
exit 1
```

Do NOT attempt to guess or calculate the session ID. Report the error to the user.

**If file not readable**:
- Check permissions: `ls -la /home/node/.config/projects/-workspace/`
- Verify path: `realpath ~/.claude/projects/`
- Verify session ID is correct (check system reminder for actual session ID)

## Security Considerations

- Conversation files may contain sensitive data (code, credentials mentions, paths)
- Only parse-conversation-timeline skill and audit agents should access raw conversation
- Do not log or store conversation content outside audit workflow
- Verify conversation file belongs to current project before parsing

## Output Format for Audits

**Structured JSON Output**:
```json
{
  "session_id": "fa3f1ca8-903e-4253-baf8-30416279a7e0",
  "conversation_file": "/home/node/.config/projects/-workspace/fa3f1ca8-903e-4253-baf8-30416279a7e0.jsonl",
  "entry_count": 1543,
  "user_messages": 27,
  "assistant_messages": 26,
  "tool_uses": {
    "Task": 11,
    "Edit": 26,
    "Write": 62,
    "Bash": 221,
    "Read": 52
  },
  "user_approvals": [
    {
      "timestamp": 1730331800000,
      "content": "yes, proceed",
      "context": "after SYNTHESIS state"
    }
  ],
  "working_directory_violations": [
    {
      "timestamp": 1730335200000,
      "tool": "Edit",
      "file": "FormattingViolationTest.java",
      "pwd": "/workspace/tasks/implement-formatter-api/agents/architect/code",
      "violation": "Main agent editing in agent worktree"
    }
  ],
  "agent_invocations": [
    {
      "timestamp": 1730331900000,
      "agent": "architect",
      "state": "CLASSIFIED",
      "output_verified": true
    }
  ]
}
```

## Integration with Existing Skills

**Complements learn-from-mistakes**:
- get-history: Provides raw conversation data
- learn-from-mistakes: Analyzes mistakes and recommends fixes
- Used together: Complete audit and improvement cycle

**Enables Independent Verification**:
- Main agent cannot filter/sanitize conversation
- Audit agents get unbiased, complete conversation history
- Prevents false negatives in compliance audits

## Practical Example: Investigating Agent Tool Errors

**Scenario**: User reports architect agent encountered "No such tool available: Bash" and Read errors.

**Investigation Steps**:

```bash
# Step 1: Get session ID from SessionStart system reminder
# Look for: ✅ Session ID: 88194cb6-734b-498c-ab5d-ac7c773d8b34
SESSION_ID="88194cb6-734b-498c-ab5d-ac7c773d8b34"
echo "Session ID: $SESSION_ID"

# Step 2: Find architect agent invocations in main session
jq 'select(.type == "tool_result" and .toolUseResult.agentId != null) |
    {time: .timestamp, agent: .toolUseResult.agentId}' \
    ~/.config/projects/-workspace/${SESSION_ID}.jsonl

# Step 3: Get agent ID (e.g., a74f3744)
AGENT_ID="a74f3744"

# Step 4: Check agent sidechain log for errors
grep -i "no such tool\|error" ~/.config/projects/-workspace/agent-${AGENT_ID}.jsonl | \
    jq -r 'select(.type == "user") | .message.content[]'

# Output:
# {"type":"tool_result","content":"<tool_use_error>Error: No such tool available: Bash</tool_use_error>","is_error":true}
# {"type":"tool_result","content":"<tool_use_error>Error: No such tool available: Read</tool_use_error>","is_error":true}

# Step 5: Count which tools actually worked
jq -r 'select(.type == "assistant") | .message.content[] | select(.type == "tool_use") | .name' \
    ~/.config/projects/-workspace/agent-${AGENT_ID}.jsonl | sort | uniq -c

# Output:
#   7 Glob
#  15 Grep
#   2 Write

# Step 6: Identify attempted vs successful tools
echo "Attempted but failed: Bash, Read"
echo "Successfully used: Grep, Glob, Write"

# Step 7: Verify agent completed despite errors
jq 'select(.type == "tool_result" and .toolUseResult.agentId == "a74f3744") |
    {status: .toolUseResult.status, duration: .toolUseResult.totalDurationMs, tools: .toolUseResult.totalToolUseCount}' \
    ~/.config/projects/-workspace/${SESSION_ID}.jsonl

# Output:
# {"status":"completed","duration":41617,"tools":13}
```

**Findings**:
1. Agent attempted to use Bash and Read (declared in frontmatter)
2. Both tools failed with "No such tool available" errors
3. Agent successfully adapted to use Grep and Glob instead
4. Agent completed successfully despite 4 tool failures
5. This is a systematic restriction affecting all agents, not a bug in architect
