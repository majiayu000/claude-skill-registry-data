---
name: fleet-pause
description: >
  Pause work and escalate when requirements are unclear, changes are
  high-risk, you're stuck, or you need human/agent input. Properly
  notifies via task comment, IRC, and board memory. Prevents agents
  from continuing when they should stop.
  Triggers on: "pause", "blocked", "need help", "escalate", "stuck",
  "fleet pause", "unclear requirements".
user-invocable: true
---

# Fleet Pause / Escalate

Know when to STOP working and ASK for help. **Continuing to guess when you
should stop wastes time and produces bad output.**

## When to Pause

### 1. Requirements are unclear
You can't determine what to do from the task description.
Don't guess — ask.

### 2. High-risk change
The change affects security, data integrity, infrastructure, or auth.
Don't proceed without human approval.

### 3. Multiple valid approaches
There are 2+ reasonable ways to do this and the choice matters.
Let the human or architect decide.

### 4. Blocked by another agent
You need output from another agent's task and it's not done.
Create a follow-up or wait.

### 5. Stuck
You've been working for a while without progress.
Something is wrong — escalate.

### 6. Found something unexpected
The codebase is different from what was described.
Requirements contradict what you see.
A dependency is broken or missing.

## How to Pause

### Step 1: Stop working

Do not make any more changes. If you have uncommitted work, commit what's safe
with a `chore: WIP — paused for escalation [task:XXXXXXXX]` commit.

### Step 2: Post blocker comment on task

Use `agents/_template/markdown/comment-blocker.md`:

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/tasks/$TASK_ID/comments" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{"message": "## 🚫 Blocked\n\n**Reason:** {specific reason}\n**Impact:** {what cannot proceed}\n**Needed:** {exactly what would unblock}\n**Suggested action:** {who should do what}\n\n---\n<sub>{agent_name} · [{task_short}]({task_url})</sub>"}'
```

### Step 3: Post to IRC

```bash
bash scripts/notify-irc.sh --agent "{agent_name}" --event "BLOCKED" --title "{reason}" --url "{task_url}"
```

### Step 4: Post to board memory (if it affects other agents)

Only if other agents need to know about this blocker:

```bash
curl -s -X POST "$BASE_URL/api/v1/agent/boards/$BOARD_ID/memory" \
  -H "X-Agent-Token: $AUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{"content": "## 🚫 Blocker: {title}\n\n**Agent:** {name}\n**Task:** [{title}]({task_url})\n**Impact:** {what this blocks}\n**Needed:** {resolution}\n\n---", "tags": ["blocked", "project:{project}"], "source": "{agent_name}"}'
```

### Step 5: WAIT

Do not continue working on this task. Wait for human input via:
- IRC response
- Board memory response
- Task comment
- New instructions via chat.send

## Decision Tree

```
Am I stuck?
  ├─ Yes → Post blocker, notify IRC, WAIT
  └─ No
      ├─ Is this high-risk? → Post for review, notify IRC, WAIT
      ├─ Are requirements unclear? → Post question, notify IRC, WAIT
      ├─ Do I need another agent? → Create proposed task (fleet-task-create), notify
      └─ Multiple approaches? → Post options to board memory, tag @human, WAIT
```

## Rules

- **NEVER** continue guessing when you should stop
- **ALWAYS** explain WHY you're pausing (not just "I'm stuck")
- **ALWAYS** say what would UNBLOCK you (specific action needed)
- **ALWAYS** notify IRC so the human sees it immediately
- Pausing is NOT failure — it's intelligence. Bad output from guessing IS failure.