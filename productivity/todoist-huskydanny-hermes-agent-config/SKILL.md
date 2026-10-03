---
name: todoist
description: Manage Todoist tasks and projects via @doist/todoist-cli. Full task lifecycle — quick add, structured create, subtask decomposition, conflict detection, conversational escalation, and section/topic management. Built-in authentication via system credential manager.
version: 2.0.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [node]
metadata:
  hermes:
    tags: [Todoist, Tasks, Productivity, CLI, Task Management, Planning]
---

# Todoist — Task & Project Management

Complete task management for Hermes. Handles natural-language input (English + Chinese), structured task creation, subtask decomposition, scheduling conflict detection, and conversational escalation.

## CLI Binary

```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js <command>
```

Always use the full `node /path/to/index.js` invocation — the `td` symlink may not be in PATH.

---

## Preflight Check

The `npm install -g @doist/todoist-cli` sometimes leaves the package's own `node_modules` incomplete (missing `commander`), causing every command to fail with `ERR_MODULE_NOT_FOUND`.

```bash
TD_CLI="/opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js"
TD_PKG="/opt/homebrew/lib/node_modules/@doist/todoist-cli"

# Fix if needed
ls "$TD_PKG/node_modules/commander" >/dev/null 2>&1 \
  || (cd "$TD_PKG" && npm install)

# Verify
node "$TD_CLI" --version
```

---

## Data Model

```
Project (5 fixed): 生活, 工作, 学习, Inbox, Welcome
  └─ Section (= Topic): 韩国游, 服务器部署, 搬家, …
      └─ Task: 订机票
          ├─ due: 2026-04-20 (or datetime)
          ├─ priority: p1..p4
          ├─ description: context / why
          └─ Subtask: 比较航司
          └─ Subtask: 确认行李限制
```

**Rules:**
- Projects are **fixed** — never create or delete them. Valid projects: `生活`, `工作`, `学习`, `Inbox`, `Welcome`.
- Sections are Topics — created on demand via `section create --project X --name Y`.
- Tasks belong to a Section within a Project. A task without a section is "loose" under the project.
- Subtasks use `--parent id:xxx`. Nesting is capped at **4 levels from root** — deeper nesting silently re-parents to the grandparent.

---

## Intent Parsing

When a user sends a task-like message, extract these fields:

| Field | Source | Default |
|-------|--------|---------|
| `project` | Explicit mention (`#生活`, `工作里`, "life:", "work:") | `Inbox` |
| `section` | Topic name (`/韩国游`, "韩国游 topic") | none |
| `task` | Task title (imperative verb phrase) | required |
| `due` | Natural-language date/time (`下周`, `明天下午三点`, "tomorrow 3pm") | none |
| `priority` | Urgency words or explicit `p1..p4` | `p4` |
| `subtasks` | Auto-decompose if user asks for a plan or task is complex | none |
| `context` | Why this task exists — stored in `--description` | none |

### Priority word mapping

| Words (EN / 中文) | CLI flag | JSON `priority` (inverted) |
|------------------|----------|----------------------------|
| urgent, critical, ASAP / 紧急, 火烧眉毛 | `p1` | 4 |
| important, high / 比较重要, 重要 | `p2` | 3 |
| medium, soon / 一般, 稍后 | `p3` | 2 |
| (none) / default | `p4` | 1 |

> JSON priority is inverted: CLI `p1` = JSON `priority: 4`. Normalize when reading JSON back.

### Intent examples

1. **"给生活/韩国游加个任务，下周订机票，比较重要"**
   → `project=生活`, `section=韩国游`, `task=订机票`, `due="next week"`, `priority=p2`, `description="用户原话：..."`

2. **"工作里加个新topic叫服务器部署，明天下午三点检查CPU"**
   → `project=工作`, `section=服务器部署` (create if missing), `task=检查CPU`, `due="tomorrow 3pm"`, `priority=p4`

3. **"完成了订机票"**
   → `action=complete`, `task=订机票`

4. **"add a task to review PR #42 tomorrow morning, urgent"**
   → `project=工作`, `task="Review PR #42"`, `due="tomorrow 9am"`, `priority=p1`

5. **"plan the Korea trip — need flights, hotels, itinerary"**
   → `action=decompose`, `task=Plan Korea trip`, proposed subtasks: `订机票`, `订酒店`, `写行程`
   **Conversational** — confirm the subtask list before creating.

---

## Quick Add vs Structured Add

### Quick add (one-liner)
```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js add "订机票 #生活 /韩国游 p1 next Friday 2pm"
```

- `#ProjectName` → project (Chinese OK)
- `/SectionName` → section (Chinese OK)
- `p1..p4` → priority
- Natural-language dates → due
- **`@label` is NOT parsed by quick add** — use `task update --labels a,b,c` after creation

### Structured add (programmatic)
```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task add "订机票" \
  --project "生活" \
  --section "韩国游" \
  --due "next week" \
  --priority p2 \
  --description "Telegram 2026-04-17: 下周去首尔，需要先订机票比价" \
  --json
```

**Do NOT use `--deadline`** — returns `403 AUTH_ERROR` (likely paid-plan only).

---

## Task Operations

### Create a task
```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task add "Task name" \
  --project "生活" \
  --section "section_name_or_id" \
  --due "2026-04-17" \
  --priority p1 \
  --labels "@搬家,@出行" \
  --description "Context or why this exists" \
  --json
```

### List tasks
```bash
# By due date
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --due 2026-04-17 --json

# By project
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --project "工作" --json

# By project + section (Todoist filter syntax — no --section flag on list)
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --filter "##生活 & /韩国游" --json

# By project + today
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --filter "##生活 & today" --json

# By parent (direct children only)
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --parent "id:$PARENT_ID" --json

# Filter by priority
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --priority p1 --json

# Limit
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task list --project "工作" --limit 10 --json
```

### View a task
```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task view "task name or id:xxx" --json
```

### Complete a task
```bash
# By id (preferred — avoids AMBIGUOUS_TASK)
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task complete "id:$TASK_ID"

# By name (only if unique)
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task complete "订机票"
```

> `task complete` does NOT support `--json`. It prints `Completed: <name> (id:xxx)`. Parse that string or check exit code.

**Cascade warning:** Completing a parent auto-completes ALL descendants. Always confirm before completing a parent with subtasks.

### Update a task
```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task update "id:$TASK_ID" \
  --due "next Monday" \
  --priority p2 \
  --labels "@新标签"
```

### Reschedule
```bash
# CORRECT — task update --due accepts natural language
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task update "id:$TASK_ID" --due "tomorrow 3pm"

# WRONG — task reschedule only accepts YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
# (and requires an existing due date)
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task reschedule "id:$TASK_ID" "2026-04-18T15:00:00"
```

### Delete a task
```bash
node /opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js task delete "id:$TASK_ID" --yes
```

> Delete cascades to ALL descendants. Always confirm the full descendant list before deleting a parent.

---

## Section (Topic) Management

### Create-if-missing workflow
```bash
TD_CLI="/opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js"
PROJECT="生活"
TOPIC="韩国游"

# 1. List existing sections
EXISTING=$(node "$TD_CLI" section list --project "$PROJECT" --json)

# 2. Check if topic exists
HAS=$(echo "$EXISTING" | python3 -c "
import sys, json
data = json.load(sys.stdin)
sections = data.get('results', data) if isinstance(data, dict) else data
print('yes' if '$TOPIC' in [s['name'] for s in sections] else 'no')
")

# 3. Create if missing
if [ "$HAS" = "no" ]; then
  SECTION_JSON=$(node "$TD_CLI" section create --project "$PROJECT" --name "$TOPIC" --json)
  SECTION_ID=$(echo "$SECTION_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
  echo "Created topic '$TOPIC' under $PROJECT (id:$SECTION_ID)"
fi
```

> **Never use `project view --detailed`** — it has a zod validation error on the `collaborators` field. Always use `section list --project X --json`.

### Other section operations
```bash
# List all sections in a project
node "$TD_CLI" section list --project "生活" --json

# Search sections
node "$TD_CLI" section list --project "生活" --search "韩国" --json

# Rename
node "$TD_CLI" section update <section_id> --name "韩国自由行" --json

# Delete (fails if tasks remain — move or delete them first)
node "$TD_CLI" section delete <section_id> --yes
```

---

## Subtask Decomposition

### Create parent + subtasks
```bash
TD_CLI="/opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js"

# 1. Create parent, capture its id
PARENT_JSON=$(node "$TD_CLI" task add "Plan Korea trip" \
  --project "生活" \
  --section "韩国游" \
  --due "next week" \
  --description "Decomposed from user message" \
  --json)

PARENT_ID=$(echo "$PARENT_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Create subtasks under it
for sub in "订机票" "订酒店" "写行程" "换韩元" "买旅游保险"; do
  node "$TD_CLI" task add "$sub" --parent "id:$PARENT_ID" --json
done
```

### Decomposition is conversational

Auto-decomposition (3–5 subtasks) requires **user confirmation first**:

```
Hermes: "帮你拆成 5 步可以吗？
  1. 订机票
  2. 订酒店
  3. 写行程
  4. 换韩元
  5. 买旅游保险
需要增减或调整顺序吗？"
```

Only after the user confirms do you create the subtasks.

---

## Conflict Detection

Before creating or rescheduling, run two checks.

### Step 1 — Time overlap (1-hour granularity)
```bash
TD_CLI="/opt/homebrew/lib/node_modules/@doist/todoist-cli/dist/index.js"
TARGET_DATE="2026-04-20"
TARGET_TIME="15:00"   # 24h, omit if day-level check

EXISTING=$(node "$TD_CLI" task list --due "$TARGET_DATE" --json)

TD_JSON="$EXISTING" TARGET_DATE="$TARGET_DATE" TARGET_TIME="$TARGET_TIME" python3 <<'PY'
import os, sys, json
from datetime import datetime, timedelta

data = json.loads(os.environ['TD_JSON'])
tasks = data.get('results', data if isinstance(data, list) else [])
target_date = os.environ['TARGET_DATE']
target_time = os.environ.get('TARGET_TIME', '').strip()

def parse_due(task):
    due = task.get('due') or {}
    raw = due.get('datetime') or due.get('date')
    if not raw:
        return None
    raw = raw.rstrip('Z')  # normalize UTC-Z
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None

if not target_time:
    print(f"{len(tasks)} existing task(s) on {target_date}:")
    for t in tasks:
        print(f"  - {t['content']}  due={t.get('due',{}).get('datetime') or t.get('due',{}).get('date')}")
    sys.exit(0)

target_dt = datetime.fromisoformat(f"{target_date}T{target_time}:00")
window_start = target_dt - timedelta(hours=1)
window_end   = target_dt + timedelta(hours=1)

overlaps = []
for t in tasks:
    dt = parse_due(t)
    if dt and window_start <= dt <= window_end:
        overlaps.append((t['content'], dt.isoformat()))

if overlaps:
    print(f"TIME OVERLAP on {target_date} near {target_time}:")
    for name, when in overlaps:
        print(f"  - {name} @ {when}")
else:
    print("No time overlap.")
PY
```

### Step 2 — Daily capacity (default: 5 tasks/day)
```bash
DAILY_CAPACITY=5
COUNT=$(node "$TD_CLI" task list --due "$TARGET_DATE" --json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results', d if isinstance(d,list) else [])))")

if [ "$COUNT" -ge "$DAILY_CAPACITY" ]; then
  echo "DAILY CAPACITY EXCEEDED: $COUNT/$DAILY_CAPACITY tasks on $TARGET_DATE"
else
  echo "Capacity OK: $COUNT/$DAILY_CAPACITY on $TARGET_DATE"
fi
```

### Decision table

| | No conflict | Conflict |
|---|---|---|
| **Add simple task** | One-shot create | Conversational: name conflict, suggest alternative |
| **Add subtasks** | One-shot | One-shot (under confirmed parent) |
| **Complete (no children)** | One-shot | One-shot |
| **Complete (has children)** | Confirm cascade first | Confirm cascade first |
| **Delete** | Confirm + list descendants | Always confirm |
| **Reschedule** | One-shot update | Conversational: name conflict, suggest alternative |

---

## Conversational Escalation Rules

**Always escalate (confirm first):**
- Destructive actions: delete, complete-with-cascade on parent
- Complex decomposition: confirm subtask list before creating
- Ambiguous task name: disambiguate by listing candidates with their sections/dates

**Escalate on conflict:**
- Time overlap on target slot → name the overlapping task, suggest adjacent slot
- Day >= 5 existing tasks → suggest previous/next day

**One-shot when clear:**
- Add task with no conflict
- Add subtasks under a confirmed parent
- Complete a simple task (no children, unambiguous)

---

## Project & Label Operations

### Projects (fixed — never create or delete)
```bash
node "$TD_CLI" project list --json
node "$TD_CLI" project progress "工作"
```

Valid projects: `Inbox`, `Welcome`, `生活`, `工作`, `学习`

### Labels
```bash
# List all labels
node "$TD_CLI" label list --json

# Create label
node "$TD_CLI" label create --name "搬家" --color red

# Labels on tasks: use comma-sep, no spaces
--labels "@搬家,@出行"
```

### Completed tasks
```bash
node "$TD_CLI" completed --json
```

---

## Error Handling

### Project not one of the 5 fixed projects
Never create a new project silently. Either:
1. Fall back to `Inbox` with a note in description, OR
2. Ask the user which of the 5 to use

### Section not found
Create it via `section create --project X --name Y --json`. Report back: "Created new topic 'X' under Y."

### Ambiguous task name (AMBIGUOUS_TASK)
CLI returns candidate ids. Disambiguate conversationally:
```
『订机票』匹配 2 个任务：
  1. 订机票 — 生活/韩国游, 2026-04-24
  2. 订机票 — 生活/日本游, 2026-05-02
要操作哪一个？
```

### CLI error propagation
Surface stderr or JSON `error.message` verbatim to the user. Do not swallow or retry blindly.

---

## Organizing Complex Projects

**3-level hierarchy:** Section (Topic) → Parent Task → Subtask

For multi-topic projects (e.g., a 20-day relocation):

1. **Create sections** (topics), capture their IDs
2. **Create parent tasks** (assigned to section, with labels), capture their IDs
3. **Create subtasks** under parents (omit `--section`, it inherits from parent)

Cross-cutting concerns use **labels** (e.g., `@搬家`, `@出差`, `@入职`) not sections.

```bash
# Step 1: Create sections
S1=$(node "$CLI" section create --project "生活" --name "🚚 搬家" --json \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Step 2: Create parent task
P1=$(node "$CLI" task add "打包整理" \
  --project "生活" \
  --section "$S1" \
  --due "2026-04-17" \
  --priority p1 \
  --labels "@搬家" \
  --json \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Step 3: Create subtasks
node "$CLI" task add "Label 9 boxes" --parent "id:$P1" --priority p1
node "$CLI" task add "预约货拉拉" --parent "id:$P1" --priority p1
```

---

## Typical Workflow (Message → Todoist)

```
User message → Parse intent → Ensure topic exists → Conflict check →
  → Create task → (optional: propose subtask decomposition) → Confirm
```

**Example:** User sends "给生活/韩国游加个任务，下周订机票，比较重要"

1. **Parse:** `project=生活`, `section=韩国游`, `task=订机票`, `due="next week"`, `priority=p2`
2. **Ensure topic:** `section list --project 生活` → create if missing
3. **Conflict check:** `task list --due "2026-04-24"` → run overlap + capacity
4. **Create:** `task add` with all fields, capture `id`
5. **Confirm:** "已加到 生活/韩国游：『订机票』 (p2, 2026-04-24)。需要拆成子任务吗？"

---

## Known Caveats

1. **`project view --detailed` is broken** — zod validation error on `collaborators`. Use `section list --project X --json`.
2. **`--deadline` returns `403 AUTH_ERROR`** — do NOT use.
3. **`task reschedule` rejects natural language** — use `task update --due "tomorrow 3pm"` instead.
4. **`@label` NOT parsed in quick add** — use `task update --labels` after creation.
5. **Priority inversion** — CLI `p1` = JSON `priority: 4`. Normalize when reading JSON.
6. **Parent complete/delete cascades** — auto-completes/deletes all descendants. Always warn.
7. **Subtask nesting cap = 4 levels** — deeper nesting silently re-parents to grandparent.
8. **`task complete` has no `--json`** — only human-readable output.
9. **Always use `id:xxx` after creation** — name-based writes risk `AMBIGUOUS_TASK`.
10. **Two `due.date` shapes** — structured add returns naive local ISO; quick add returns UTC with trailing `Z`. Conflict-detection parser handles both.
11. **Section delete fails if tasks remain** — move or delete tasks first.
12. **JSON `{"results": [...]}` wrapper** — access `data['results']` not `data` directly on `task list --json`.
13. **Emoji in `--json` fails to parse** — task IS created; omit `--json` and capture ID from stdout.
