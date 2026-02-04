---
name: github-swarm-issue
description: GitHub issue-based swarm coordination for intelligent task decomposition and progress tracking. Use for transforming issues into multi-agent tasks, automated triage, task breakdown, and issue lifecycle management.
---

# GitHub Swarm Issue Skill

## Overview

This skill transforms GitHub Issues into intelligent swarm tasks, enabling automatic task decomposition, agent coordination, and comprehensive progress tracking. It provides issue-to-swarm conversion, automated triage, and lifecycle management.

**Key Capabilities:**
- Issue-to-swarm conversion with automatic decomposition
- Issue comment commands for swarm control
- Automated triage and labeling
- Task breakdown with subtask creation
- Progress tracking with visual updates
- Duplicate detection and linking

## Quick Start

```bash
# Get issue details for swarm initialization
gh issue view 456 --json title,body,labels,assignees,comments

# List issues ready for swarm processing
gh issue list --label "swarm-ready"

# Add swarm label to trigger processing
gh issue edit 456 --add-label "swarm-ready"

# Post swarm status comment
gh issue comment 456 --body "Swarm initialized for this issue"
```

## When to Use

- **Complex Issues**: Multi-step tasks requiring decomposition
- **Bug Investigation**: Issues needing systematic debugging
- **Feature Requests**: New features requiring architecture and implementation
- **Technical Debt**: Refactoring tasks with multiple components
- **Epic Management**: Coordinating child issues under parent

## Usage Examples

### 1. Issue-to-Swarm Conversion

```bash
# Get complete issue context
ISSUE=$(gh issue view 456 --json title,body,labels,assignees,comments,projectItems)

# Analyze issue complexity
BODY=$(echo "$ISSUE" | jq -r '.body')
LABEL_COUNT=$(echo "$ISSUE" | jq '.labels | length')
COMMENT_COUNT=$(echo "$ISSUE" | jq '.comments | length')

# Determine swarm topology based on complexity
if [ $LABEL_COUNT -gt 3 ] || [ ${#BODY} -gt 1000 ]; then
  TOPOLOGY="hierarchical"
  MAX_AGENTS=8
elif echo "$BODY" | grep -qE "(\[ \]|1\.|step)" ; then
  TOPOLOGY="mesh"
  MAX_AGENTS=5
else
  TOPOLOGY="ring"
  MAX_AGENTS=3
fi

echo "Issue #456: Using $TOPOLOGY topology with $MAX_AGENTS agents"

# Initialize swarm comment
gh issue comment 456 --body "## Swarm Initialized

**Topology**: $TOPOLOGY
**Agents**: $MAX_AGENTS

Processing issue for task decomposition..."
```

### 2. Task Decomposition

```bash
# Get issue body
ISSUE_BODY=$(gh issue view 456 --json body --jq '.body')

# Extract tasks from issue body (markdown checklist items)
TASKS=$(echo "$ISSUE_BODY" | grep -E '^\s*-\s*\[ \]' | sed 's/.*\[ \]//')

# Create subtask checklist
SUBTASK_LIST=""
TASK_NUM=1
echo "$TASKS" | while read -r task; do
  SUBTASK_LIST+="- [ ] $TASK_NUM. $task\n"
  TASK_NUM=$((TASK_NUM + 1))
done

# Update issue with structured subtasks
UPDATED_BODY="$ISSUE_BODY

## Swarm Task Breakdown
$SUBTASK_LIST

---
Decomposed by Swarm Agent"

gh issue edit 456 --body "$UPDATED_BODY"

# Create linked issues for major subtasks
gh issue create \
  --title "Subtask: Implement authentication" \
  --body "Part of #456

## Task
Implement the authentication module.

## Acceptance Criteria
- [ ] User login works
- [ ] Token refresh works
- [ ] Logout clears session" \
  --label "subtask"
```

### 3. Progress Tracking

```bash
# Track issue progress
track_progress() {
  local ISSUE_NUM=$1

  # Get current issue state
  ISSUE=$(gh issue view $ISSUE_NUM --json body,labels)
  BODY=$(echo "$ISSUE" | jq -r '.body')

  # Count completed vs total tasks
  TOTAL=$(echo "$BODY" | grep -cE '^\s*-\s*\[[ x]\]' || echo 0)
  COMPLETED=$(echo "$BODY" | grep -cE '^\s*-\s*\[x\]' || echo 0)
  PERCENT=$((COMPLETED * 100 / TOTAL))

  # Generate progress bar
  FILLED=$((PERCENT / 5))
  EMPTY=$((20 - FILLED))
  PROGRESS_BAR=$(printf '█%.0s' $(seq 1 $FILLED))$(printf '░%.0s' $(seq 1 $EMPTY))

  # Post progress update
  gh issue comment $ISSUE_NUM --body "## Progress Update

**Completion**: $PERCENT% [$PROGRESS_BAR]
**Tasks**: $COMPLETED / $TOTAL completed

$([ $PERCENT -eq 100 ] && echo '✅ All tasks complete!' || echo '🔄 Work in progress...')

---
Updated: $(date '+%Y-%m-%d %H:%M')"
}

track_progress 456
```

### 4. Issue Comment Commands

Use these commands in issue comments:

```markdown
<!-- Analyze issue and suggest approach -->
/swarm analyze

<!-- Decompose into subtasks -->
/swarm decompose 5

<!-- Assign specific agent type -->
/swarm assign @coder

<!-- Estimate effort -->
/swarm estimate

<!-- Start swarm processing -->
/swarm start

<!-- Check progress -->
/swarm progress

<!-- Complete and summarize -->
/swarm complete
```

### 5. Automated Triage

```bash
# Triage unlabeled issues
triage_issues() {
  # Get unlabeled issues
  gh issue list --label "" --json number,title,body | \
    jq -r '.[] | @base64' | while read -r encoded; do
      ISSUE=$(echo "$encoded" | base64 -d)
      NUM=$(echo "$ISSUE" | jq -r '.number')
      TITLE=$(echo "$ISSUE" | jq -r '.title')
      BODY=$(echo "$ISSUE" | jq -r '.body')

      # Analyze content for auto-labeling
      LABELS=""

      # Bug detection
      if echo "$TITLE $BODY" | grep -qiE "bug|error|broken|crash|fail"; then
        LABELS="bug"
      fi

      # Feature detection
      if echo "$TITLE $BODY" | grep -qiE "feature|add|implement|new"; then
        LABELS="${LABELS:+$LABELS,}enhancement"
      fi

      # Performance detection
      if echo "$TITLE $BODY" | grep -qiE "slow|performance|optimize|speed"; then
        LABELS="${LABELS:+$LABELS,}performance"
      fi

      # Security detection
      if echo "$TITLE $BODY" | grep -qiE "security|vulnerability|auth|permission"; then
        LABELS="${LABELS:+$LABELS,}security"
      fi

      # Apply labels
      if [ -n "$LABELS" ]; then
        gh issue edit $NUM --add-label "$LABELS"
        echo "Issue #$NUM: Added labels $LABELS"
      fi
    done
}

triage_issues
```

### 6. Stale Issue Management

```bash
# Process stale issues
manage_stale_issues() {
  # Get issues not updated in 30 days
  STALE_DATE=$(date -d '30 days ago' '+%Y-%m-%d')

  gh issue list --state open --json number,title,updatedAt | \
    jq -r ".[] | select(.updatedAt < \"$STALE_DATE\") | .number" | \
    while read -r num; do
      # Check if already marked stale
      LABELS=$(gh issue view $num --json labels --jq '.labels[].name')

      if echo "$LABELS" | grep -q "stale"; then
        # Already stale for 7+ days - close
        STALE_CHECK=$(date -d '7 days ago' '+%Y-%m-%d')
        UPDATED=$(gh issue view $num --json updatedAt --jq '.updatedAt[:10]')

        if [ "$UPDATED" \< "$STALE_CHECK" ]; then
          gh issue close $num --comment "Closing due to inactivity. Feel free to reopen if still relevant."
        fi
      else
        # Mark as stale
        gh issue edit $num --add-label "stale"
        gh issue comment $num --body "This issue has been inactive for 30 days. It will be closed in 7 days if there's no activity."
      fi
    done
}

manage_stale_issues
```

## Issue Templates for Swarms

```yaml
# .github/ISSUE_TEMPLATE/swarm-task.yml
name: Swarm Task
description: Create a task for AI swarm processing
body:
  - type: dropdown
    id: topology
    attributes:
      label: Swarm Topology
      options:
        - mesh (collaborative)
        - hierarchical (structured)
        - ring (sequential)
        - star (centralized)
    validations:
      required: true

  - type: input
    id: agents
    attributes:
      label: Required Agents
      placeholder: "coder, tester, analyst"

  - type: textarea
    id: description
    attributes:
      label: Task Description
      placeholder: "Describe what needs to be done..."
    validations:
      required: true

  - type: textarea
    id: subtasks
    attributes:
      label: Subtasks (Optional)
      placeholder: |
        - [ ] Subtask 1
        - [ ] Subtask 2
        - [ ] Subtask 3
```

## MCP Tool Integration

### Multi-Agent Issue Processing

```javascript
// Initialize issue-specific swarm
mcp__claude-flow__swarm_init { topology: "hierarchical", maxAgents: 8 }
mcp__claude-flow__agent_spawn { type: "coordinator", name: "Issue Coordinator" }
mcp__claude-flow__agent_spawn { type: "analyst", name: "Issue Analyzer" }
mcp__claude-flow__agent_spawn { type: "coder", name: "Solution Developer" }
mcp__claude-flow__agent_spawn { type: "tester", name: "Validation Engineer" }

// Store issue context in swarm memory
mcp__claude-flow__memory_usage {
  action: "store",
  key: "issue/456/context",
  value: {
    issue_number: 456,
    title: "Implement authentication",
    labels: ["feature", "priority:high"],
    complexity: "high",
    agents_assigned: ["coordinator", "analyst", "coder", "tester"]
  }
}

// Orchestrate issue resolution
mcp__claude-flow__task_orchestrate {
  task: "Coordinate multi-agent issue resolution with progress tracking",
  strategy: "adaptive",
  priority: "high"
}
```

### GitHub Integration Tools

```javascript
// Track issues
mcp__claude-flow__github_issue_track {
  repo: "owner/repo",
  action: "triage"
}

// Analyze repository
mcp__claude-flow__github_repo_analyze {
  repo: "owner/repo",
  analysis_type: "code_quality"
}

// Get metrics
mcp__claude-flow__github_metrics {
  repo: "owner/repo"
}
```

## GitHub Actions Integration

```yaml
# .github/workflows/issue-swarm.yml
name: Issue Swarm Handler
on:
  issues:
    types: [opened, labeled]
  issue_comment:
    types: [created]

jobs:
  process-new-issue:
    if: github.event.action == 'opened'
    runs-on: ubuntu-latest
    steps:
      - name: Auto-Triage Issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          TITLE="${{ github.event.issue.title }}"
          BODY="${{ github.event.issue.body }}"

          # Determine labels based on content
          LABELS=""
          if echo "$TITLE $BODY" | grep -qiE "bug|error"; then
            LABELS="bug"
          elif echo "$TITLE $BODY" | grep -qiE "feature|add"; then
            LABELS="enhancement"
          fi

          if [ -n "$LABELS" ]; then
            gh issue edit ${{ github.event.issue.number }} --add-label "$LABELS"
          fi

  handle-swarm-label:
    if: github.event.action == 'labeled' && github.event.label.name == 'swarm-ready'
    runs-on: ubuntu-latest
    steps:
      - name: Initialize Swarm
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh issue comment ${{ github.event.issue.number }} \
            --body "## Swarm Processing Started

          This issue has been queued for swarm processing.

          **Status**: Analyzing...
          **ETA**: ~15 minutes"

  handle-commands:
    if: github.event_name == 'issue_comment' && startsWith(github.event.comment.body, '/swarm')
    runs-on: ubuntu-latest
    steps:
      - name: Process Command
        run: |
          COMMAND="${{ github.event.comment.body }}"
          echo "Processing swarm command: $COMMAND"
```

## Issue Types and Strategies

### Bug Reports

```bash
# Specialized bug handling
handle_bug() {
  local ISSUE_NUM=$1

  gh issue comment $ISSUE_NUM --body "## Bug Investigation Swarm

**Agents Assigned:**
- Debugger: Reproduce and isolate
- Analyst: Root cause analysis
- Tester: Regression tests
- Coder: Fix implementation

**Process:**
1. Reproduce the bug
2. Isolate to minimal case
3. Identify root cause
4. Implement fix
5. Add regression tests
6. Verify fix"
}
```

### Feature Requests

```bash
# Feature implementation workflow
handle_feature() {
  local ISSUE_NUM=$1

  gh issue comment $ISSUE_NUM --body "## Feature Implementation Swarm

**Agents Assigned:**
- Architect: Design approach
- Coder: Implementation
- Tester: Test coverage
- Reviewer: Code quality

**Phases:**
1. Design review
2. Implementation
3. Testing
4. Documentation
5. Demo/Review"
}
```

## Best Practices

### 1. Issue Templates
- Include swarm configuration options
- Provide structured task breakdown
- Set clear acceptance criteria
- Include complexity estimates

### 2. Label Strategy
- Use consistent swarm-related labels (swarm-ready, swarm-processing)
- Map labels to agent types
- Include priority indicators
- Track status with labels

### 3. Comment Etiquette
- Clear command syntax (/swarm command)
- Progress updates in threads
- Summary comments for decisions
- Link to relevant PRs

### 4. Progress Tracking
- Regular status updates
- Visual progress indicators
- ETA estimates
- Blocker identification

## Metrics and Analytics

```bash
# Issue resolution metrics
generate_metrics() {
  # Get closed issues from last 30 days
  gh issue list --state closed --json number,title,createdAt,closedAt,labels | \
    jq '{
      total_closed: length,
      avg_resolution_days: ([.[].createdAt, .[].closedAt] | map(fromdateiso8601) | . as $dates | (($dates[1] - $dates[0]) / 86400)) | add / length,
      by_label: group_by(.labels[].name) | map({label: .[0].labels[0].name, count: length})
    }'
}

generate_metrics
```

## Related Skills

- [github-swarm-pr](../github-swarm-pr/SKILL.md) - PR-based swarm coordination
- [github-project-board](../github-project-board/SKILL.md) - Project board integration
- [github-workflow](../github-workflow/SKILL.md) - CI/CD automation
- [github-modes](../github-modes/SKILL.md) - GitHub integration modes

---

## Version History

- **1.0.0** (2026-01-02): Initial skill conversion from swarm-issue agent
