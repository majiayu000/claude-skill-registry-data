---
name: eval
description: "Evaluate everything the PA agent manages — tasks, skills, PA network health, billing, calendar connections, and memory quality. Use when: owner asks for an evaluation, wants to know what's working and what isn't, or requests a performance report. Combines supervisor status with quality scoring."
---

# Eval Skill

Structured evaluation of everything the agent manages.

---

## ⚡ Execution Architecture (Anti-Timeout)

Eval is split into 3 independent subagents that run in parallel.
Each subagent handles one domain, returns a short result block, and exits.
Main agent collects results and formats the final report.

**On-demand (user asks):** Always run fresh — never read from cache.
**Cron/heartbeat:** Run async, save to `memory/eval-cache.json`, report only if issues found.

### Subagent Split
| Subagent | Domain | Expected Time |
|---|---|---|
| SA-1 | System health (vertex, WhatsApp, DB, backup) | <15s |
| SA-2 | PA network health (contact-list.md) | <15s |
| SA-3 | Tasks + memory + skills audit | <15s |

**Timeout:** Spawn all subagents with `runTimeoutSeconds=60`. Do NOT use `openclaw status` — it is slow and causes SIGKILL. Use only fast targeted commands (see templates below).

### How to Run (on-demand)
```
1. Spawn SA-1, SA-2, SA-3 simultaneously (sessions_spawn, runtime=subagent)
2. Each returns a JSON block with its section
3. Main agent merges and formats the final report
4. Send to owner
```

### Subagent Task Templates

**SA-1 — System Health:**
```
Run system health check using ONLY fast targeted commands (do NOT run openclaw status):
1. /path/to/ocana/bifrost/vertex-ctl.sh status 2>&1 | head -3
2. curl -s --max-time 5 http://127.0.0.1:18789/ | head -1 || echo 'gateway unreachable'
3. git -C /path/to/openclaw/workspace log -1 --format="%ar"
4. python3 -c "import os,subprocess; db=os.environ.get('PA_DB_URL',''); r=subprocess.run(['psql',db,'-c','SELECT COUNT(*) FROM messages;','-t'],capture_output=True,text=True,timeout=5) if db else None; print(r.stdout.strip() if r else 'no DB')"
Return JSON: {"vertex": "RUNNING/DOWN", "gateway": "reachable/unreachable", "backup": "X ago", "db": "X msgs"}
```

**SA-2 — PA Network:**
```
Read /path/to/workspace/contact-list.md
Find all PA entries (lines with "PA:" or under WhatsApp Groups / PAs section)
Count total PAs, check for any notes about issues/offline/billing
Return JSON: {"total": N, "online": N, "issues": [{"pa": "name", "issue": "description"}]}
```

**SA-3 — Tasks + Memory + Skills:**
```
Check:
1. wc -l /path/to/workspace/MEMORY.md
2. ls /path/to/workspace/skills | wc -l
3. Check today's daily note exists
4. grep tasks.md for open/done count
Return JSON: {"memory_lines": N, "skills": N, "daily_note": true/false, "tasks_open": N, "tasks_done": N}
```

---

## When to Use

Trigger phrases:
- "תעשי eval" / "run eval"
- "מה עובד ומה לא" / "what's working and what isn't"
- "תדרגי את עצמך" / "rate yourself"
- "בדקי הכל" / "check everything"

---

## Eval Report Format

```
📋 Full Eval — [DATE]

━━━ SELF PERFORMANCE ━━━
Execution:      [1-5] [comment]
Accuracy:       [1-5] [comment]
Memory:         [1-5] [comment]
Proactivity:    [1-5] [comment]
Communication:  [1-5] [comment]
TOTAL: [X]/25

━━━ ACTIVE TASKS ━━━
✅ Done today:   [count]
🟡 In progress:  [count]
❌ Stalled:      [count] — [list stalled tasks]

━━━ PA NETWORK ━━━
✅ Working:  [list]
⚠️ Issues:   [list with issue]
❌ Down:     [list]

━━━ SKILLS ━━━
Installed: [count]
Used today: [list]
Unused (7+ days): [list]

━━━ INTEGRATIONS ━━━
Calendar (owner):     [connected ✅ / broken ❌ / unknown ?]
monday.com:           [connected ✅ / broken ❌]
Email (gog):          [connected ✅ / broken ❌]
GitHub backup:        [last push: X ago]
WhatsApp:             [connected ✅ / disconnected ❌]

━━━ MEMORY HEALTH ━━━
Daily notes:     [today's file exists? ✅/❌]
Long-term:       [MEMORY.md size — OK / bloated]
Learnings:       [count this week]
Last backup:     [X ago]

━━━ RECOMMENDATIONS ━━━
1. [Most important thing to fix]
2. [Second priority]
3. [Optional improvement]
```

---

## Running the Eval

### Step 1 — Self Performance Score

Score each dimension 1–5 based on today's activity:

```
Execution (1–5):
- 5: All tasks completed without reminders
- 3: Most tasks done, some follow-up needed
- 1: Multiple tasks missed or forgotten

Accuracy (1–5):
- 5: No corrections from owner
- 3: 1–2 corrections
- 1: Multiple errors or wrong outputs

Memory (1–5):
- 5: Recalled context correctly every time
- 3: Missed some context, caught on
- 1: Repeated the same mistakes

Proactivity (1–5):
- 5: Acted before being asked multiple times
- 3: Responded to requests, minimal initiative
- 1: Only reacted, no proactive actions

Communication (1–5):
- 5: Clear, concise, no unnecessary narration
- 3: Occasionally verbose or unclear
- 1: Shared reasoning, listed options, narrated steps
```

### Step 2 — Task Audit

```bash
TASKS_FILE="$HOME/.openclaw/workspace/memory/tasks.md"

echo "Tasks done:"
grep -c "\[x\]" "$TASKS_FILE" 2>/dev/null || echo 0

echo "Tasks in progress:"
grep -c "\[ \]" "$TASKS_FILE" 2>/dev/null || echo 0

# Stalled = in progress for 2+ days
echo "Stalled tasks (2+ days old):"
grep "\[ \]" "$TASKS_FILE" | grep -v "$(date +%Y-%m-%d)" | grep -v "$(date -u -d '1 day ago' +%Y-%m-%d 2>/dev/null)" || echo "none"
```

### Step 3 — PA Network Health

```bash
# PA network is tracked in contact-list.md (not billing-status.json)
grep -i "PA:" /path/to/workspace/contact-list.md | head -30
```

### Step 4 — Skills Audit

```bash
SKILLS_DIR="$HOME/.openclaw/workspace/skills"

echo "Installed skills:"
ls "$SKILLS_DIR" | grep -v README | wc -l

echo "Skills list:"
ls "$SKILLS_DIR" | grep -v README
```

### Step 5 — Integration Health

```bash
# Test Anthropic billing
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "x-api-key: ${ANTHROPIC_API_KEY:-none}" \
  -H "anthropic-version: 2023-06-01" \
  https://api.anthropic.com/v1/models 2>/dev/null)

# Interpret result
if [ "$API_STATUS" = "200" ]; then echo "Billing: ✅ OK"
elif [ "$API_STATUS" = "402" ]; then echo "Billing: ❌ OUT OF CREDITS"
elif [ "$API_STATUS" = "401" ]; then echo "Billing: ❌ Invalid key"
else echo "Billing: ? HTTP $API_STATUS"
fi

# Test GitHub backup
LAST_PUSH=$(git -C "$HOME/.openclaw/workspace" log -1 --format="%ar" 2>/dev/null)
echo "Last backup: $LAST_PUSH"

# Test monday.com
if [ -f "$HOME/.credentials/monday-api-token.txt" ]; then
  MONDAY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST https://api.monday.com/v2 \
    -H "Authorization: $(cat $HOME/.credentials/monday-api-token.txt)" \
    -H "Content-Type: application/json" \
    -d '{"query": "{ me { id } }"}' 2>/dev/null)
  [ "$MONDAY_STATUS" = "200" ] && echo "monday.com: ✅" || echo "monday.com: ❌ ($MONDAY_STATUS)"
else
  echo "monday.com: ? (no token found)"
fi
```

### Step 6 — Memory Health (All 4 Layers)

```bash
TODAY=$(date -u +%Y-%m-%d)
WORKSPACE="/path/to/openclaw/workspace"

# Layer 1: MEMORY.md (long-term rules)
MEMORY_LINES=$(wc -l < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0)
if [ "$MEMORY_LINES" -gt 200 ]; then
  echo "Layer 1 MEMORY.md: ⚠️ Large ($MEMORY_LINES lines) — consider pruning"
elif [ "$MEMORY_LINES" -gt 0 ]; then
  echo "Layer 1 MEMORY.md: ✅ ($MEMORY_LINES lines)"
else
  echo "Layer 1 MEMORY.md: ❌ empty or missing"
fi

# Layer 2: Daily notes
[ -f "$WORKSPACE/memory/daily/$TODAY.md" ] \
  && echo "Layer 2 Daily notes: ✅ ($TODAY exists)" \
  || echo "Layer 2 Daily notes: ❌ not created yet"

# Layer 3: PostgreSQL (WhatsApp history)
python3 << 'PYEOF'
import os, subprocess
db_url = os.environ.get('PA_DB_URL', '')
if not db_url:
    print('Layer 3 PostgreSQL: ❌ PA_DB_URL not set')
else:
    try:
        result = subprocess.run(
            ['psql', db_url, '-c', 'SELECT COUNT(*) FROM messages;', '-t'],
            capture_output=True, text=True, timeout=5
        )
        count = result.stdout.strip()
        if count.isdigit() and int(count) > 0:
            print(f'Layer 3 PostgreSQL: ✅ ({count} messages)')
        else:
            print(f'Layer 3 PostgreSQL: ⚠️ connected but empty ({count})')
    except Exception as e:
        print(f'Layer 3 PostgreSQL: ❌ {e}')
PYEOF

# Layer 4: SQLite semantic (vector memory)
# IMPORTANT: correct path is /path/to/openclaw/memory/main.sqlite (NOT workspace)
python3 << 'PYEOF'
try:
    import sqlite3, sqlite_vec
    db = sqlite3.connect('/path/to/openclaw/memory/main.sqlite')
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    files = db.execute('SELECT COUNT(*) FROM files').fetchone()[0]
    chunks = db.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]
    vectors = db.execute('SELECT COUNT(*) FROM chunks_vec').fetchone()[0]
    cache = db.execute('SELECT COUNT(*) FROM embedding_cache').fetchone()[0]
    if chunks > 1 and vectors > 1:
        print(f'Layer 4 Semantic SQLite: ✅ ({files} files, {chunks} chunks, {vectors} vectors, {cache} cached embeddings)')
    else:
        print(f'Layer 4 Semantic SQLite: ⚠️ low data ({chunks} chunks, {vectors} vectors) — may not be indexed')
except Exception as e:
    print(f'Layer 4 Semantic SQLite: ❌ {e}')
PYEOF
```

**Memory layer legend:**
- Layer 1: MEMORY.md — curated rules and context
- Layer 2: Daily notes — raw session log
- Layer 3: PostgreSQL — full WhatsApp history (2,700+ msgs)
- Layer 4: SQLite+vec — semantic/vector search across workspace files

---

## Recommendations Logic

After running all steps, generate recommendations:

```
If any PA has billing_error AND status != resolved:
  → "Fix billing for [PA list] — they can't function"

If any task has status in_progress for 2+ days:
  → "Follow up on stalled task: [task name]"

If MEMORY.md > 200 lines:
  → "Prune MEMORY.md — it's getting bloated"

If daily notes don't exist:
  → "Create today's memory file"

If last backup > 6 hours ago:
  → "Run git backup"

If API billing = 402:
  → "My own API key is out of credits — alert the admin immediately"
```

---

## Scheduling

Run eval:
- **On demand** — when owner asks
- **Weekly** — every Sunday at 09:00
- **After major incidents** — billing crisis, WA disconnect, etc.

---

## Cost Tips

- **Cheap**: Reading files, scoring, formatting — any small model
- **Expensive**: Summarizing large memory files — skip if not asked
- **Avoid**: Running all API health checks every hour — cache for 30 min
- **Batch**: Run all health checks in one pass, not one at a time

---

## Minimum Model

Any model that can:
1. Read files
2. Apply if/then scoring rules
3. Format a structured report

No advanced reasoning needed.

---

## PA Performance Scoring (Merged from pa-eval skill)

Use this section when evaluating individual PA agents (weekly self-eval or on-demand when owner gives feedback).

### Scoring Dimensions (1–5 each, max 40 points)

| Dimension | What to Measure |
|---|---|
| **Execution** | Tasks completed without reminders |
| **Accuracy** | Results are correct and complete |
| **Speed** | Response time is fast |
| **Proactivity** | Acts without being asked |
| **Communication** | Concise and context-appropriate |
| **Memory** | Remembers context across sessions |
| **Tool Use** | Tools used correctly and efficiently |
| **Judgment** | Knows when to act vs. when to ask |

**Grade:** A (36–40), B (28–35), C (20–27), D (<20)

### Owner Feedback Signals

Log these automatically when detected:

| Signal | Action |
|---|---|
| 👍 reaction / "תודה" / "great" | Log +1 positive |
| 👎 reaction / "wrong" / "לא טוב" | Log -1, record the correction |
| Owner re-asks the same question | Log -1 memory gap |
| Owner does the task themselves | Log -1 initiative gap |
| Owner surprised by proactive action | Log +2 proactivity |

**Rule:** Log feedback signals immediately — don't batch them.

### Weekly Eval File

Save to `.learnings/eval/YYYY-MM-DD.md` with: scores table, owner feedback, tasks completed/failed, what went well, what to improve, actions for next week.

### Benchmark Tests (Run Monthly)

- **Task Completion Rate:** `completed / assigned × 100%` — Target: >90%
- **Accuracy Rate:** `(tasks - corrections) / tasks × 100%` — Target: >95%
- **Memory Retention:** Ask about something discussed 7+ days ago — Target: >80% recall

---

## Skill Usage (from gateway logs)

```bash
# Which skills were used in recent sessions
for f in /tmp/openclaw/openclaw-*.log; do
  echo "=== $(basename $f) ==="
  grep -o "skills/[a-z_-]*/SKILL\.md" "$f" 2>/dev/null | sort | uniq -c | sort -rn | head -10
done
```
