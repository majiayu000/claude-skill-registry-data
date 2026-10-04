---
name: fleet-report
description: >
  Post a structured report to Mission Control board memory or as a task comment.
  Use when you need to report findings, results, or status updates to the fleet.
  Triggers on: "report", "post report", "fleet report", "post findings".
user-invocable: true
---

# Fleet Report

Post a structured report to Mission Control.

## When to Use

After completing analysis, investigation, or a phase of work, use this skill
to report findings in a consistent, structured format.

## Report Formats

### Task Comment (progress/completion)

```bash
TASK_ID="<from task assignment>"
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks/$TASK_ID/comments" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d "$(cat <<BODY
{"message": "## <Report Title>\n\n**Status:** <completed|in-progress|blocked>\n\n### Findings\n- Finding 1\n- Finding 2\n\n### Changes\n- `file/path.py`: description\n\n### Next Steps\n- Step 1\n- Step 2\n\nBranch: fleet/<agent>/<task-short>\nCommits: <count>\nFiles: <list>"}
BODY
)"
```

### Board Memory (persistent knowledge)

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/memory" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d "$(cat <<BODY
{"content": "<report content>", "tags": ["report", "<topic>"], "source": "<agent-name>"}
BODY
)"
```

## Report Structure

Every report should include:

1. **Title** — clear, specific
2. **Status** — completed, in-progress, blocked
3. **Findings** — what was discovered or done
4. **Changes** — files modified with brief descriptions
5. **References** — branch name, commit SHAs, task ID
6. **Next Steps** — what should happen next (if any)

## Rules

- Read TOOLS.md first for credentials
- Use task comments for task-specific updates
- Use board memory for cross-task knowledge (decisions, standards, architecture)
- Tag board memory entries appropriately: `report`, `decision`, `architecture`, `blocker`
- Keep reports concise — bullet points over paragraphs
- Include file paths and commit references for traceability