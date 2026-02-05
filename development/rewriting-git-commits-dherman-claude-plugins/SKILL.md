---
name: Rewriting Git Commits
description: Rewrites a git commit sequence for a changeset to create a clean branch with commits optimized for readability and review
allowed-tools: Task, Bash, Read
---

# Rewriting Git Commits Skill

You coordinate three parallel agents (analyst, narrator, and scribe) to rewrite git commit sequences into clean, logical commits.

## Input

The changeset description: **$PROMPT**

## Your Task

### Step 1: Establish Session ID

Create a unique session ID for the agents to communicate via sidechat:

```bash
# Generate timestamp-based session ID
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SESSION_ID="historian-$TIMESTAMP"

# Create work directory for storing state and logs
WORK_DIR="/tmp/$SESSION_ID"
mkdir -p "$WORK_DIR"

# Initialize state file
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
cat > "$WORK_DIR/state.json" <<EOF
{
  "session_id": "$SESSION_ID",
  "timestamp": "$TIMESTAMP",
  "original_branch": "$CURRENT_BRANCH",
  "work_dir": "$WORK_DIR"
}
EOF

echo "Created session: $SESSION_ID"
echo "Work directory: $WORK_DIR"
```

Save both `$SESSION_ID` and `$WORK_DIR` for later use.

### Step 2: Launch All Three Agents in Parallel

**CRITICAL: Make THREE Task calls in a SINGLE message** to launch all agents in parallel:

```
Task(
  subagent_type: "historian:analyst",
  description: "Analyze changeset and create commit plan",
  prompt: "Session ID: $SESSION_ID
Work directory: $WORK_DIR
Changeset: $PROMPT"
)

Task(
  subagent_type: "historian:narrator",
  description: "Execute commit plan",
  prompt: "Session ID: $SESSION_ID
Work directory: $WORK_DIR"
)

Task(
  subagent_type: "historian:scribe",
  description: "Create commits with build validation",
  prompt: "Session ID: $SESSION_ID
Work directory: $WORK_DIR"
)
```

The agents coordinate via sidechat MCP. You will **block here** until all complete.

### Step 3: Report Results

Read `$WORK_DIR/state.json` to extract `original_branch`, `clean_branch`, and `commits_created`. Report success with the branch names and commit count.
