---
name: proactive-pa
description: |-
  Configures autonomous heartbeat and cron-based proactive routines (e.g., morning briefing setup,
  unanswered-message scan cadence). Invoke when user is SETTING UP or MODIFYING a proactive routine,
  not when the routine itself fires. Cron crons execute their own logic — they do NOT load this skill.
  Triggers: "set up proactive check", "configure heartbeat", "add morning briefing", "tune cron cadence".
---

# Proactive PA

Patterns and protocols for autonomous, proactive PA behavior.

## Core Principle

**Proactive > Reactive.** Don't wait to be asked. Identify what the owner would want to know and surface it before he asks.

---

## Proactive Trigger Categories

### 🔴 ALWAYS alert immediately
- Unanswered messages >30min (use `unanswered-messages` skill)
- Calendar conflict or missed event
- Error in a cron job
- Billing issue (402 / API key failure)
- Critical message from key contacts (Daniel, Sergei, Omri, Guy)

### 🟡 Surface in next check-in (batch)
- New messages in group chats with open decisions
- Upcoming events in <2h
- Long-pending tasks with no update
- Emails marked important (unread >4h)

### 🟢 Weekly, proactively
- Memory hygiene: check `DREAMS.md` + `openclaw memory status --deep`, then prune `MEMORY.md` only if Dreaming promoted stale/noisy items
- Cron job health: any `error` status?
- Git backup: workspace pushed?

> **2026.4.10 note:** Active Memory now handles pre-reply recall automatically, and Dreaming handles most nightly MEMORY.md promotion. Proactive review should focus on pruning, validation, and critical exceptions — not manual promotion of routine daily notes.

---

## Heartbeat Protocol

Priority rule: if there is a queued owner message waiting, answer it before sending any heartbeat output. Owner DM beats heartbeat every time.

During heartbeats, rotate through these checks (2-4x per day):

```
1. Unanswered messages (last 30min)
2. Upcoming calendar events (<2h)
3. Cron job status (any errors?)
4. Email (urgent unread?)
```

Track last-checked in `memory/heartbeat-state.json`:
```json
{
  "lastChecks": {
    "unanswered": 1700000000,
    "calendar": 1700000000,
    "crons": 1700000000,
    "email": null
  }
}
```

Only run each check if >25min since last run.

---

## Autonomous Cron Patterns

### Setting up a proactive check
```bash
openclaw cron add \
  --name "<check-name>" \
  --every <interval> \
  --session isolated \
  --message "<what to check and what to do if found>" \
  --to "<OWNER_PHONE>" \
  --channel whatsapp \
  --announce \
  --timeout-seconds 60
```

### Key active crons (Heleni)
| Name | Interval | Purpose |
|------|----------|---------|
| `unanswered-messages-check` | 5m | Find unanswered messages |
| `morning-briefing` | daily 7:00 IL | Morning summary to the owner |
| `ai-digest` | daily 8:00 IL | AI news to Internal AI group |
| `billing-health-check` | hourly | API key / billing status |

---

## Proactive Communication Rules

- **Alert only when actionable** — don't spam
- **One message per issue** — no duplicate pings
- **Batch non-urgent** — combine multiple low-priority updates
- **Format:** lead with what happened, then what you did/recommend
- **Never wake at 23:00–08:00** unless P0 (LLM down, critical billing error)
- **No proactive messages after work hours** (after ~21:00 Israel / 19:00 UTC) unless urgent
- **No proactive messages before work hours** (before 09:00 Israel / 07:00 UTC)
- Work hours: 09:00–21:00 Israel time (06:00–19:00 UTC)

### Alert template
```
⚠️ [Issue type]
[1-line summary of what happened]
[Action taken or recommendation]
```

---

## Anticipation Patterns

### Pattern: "He'd want to know"
Before ending any task, ask: *"Is there anything the owner would want to know that I haven't surfaced?"*
- Upcoming related event?
- Someone waiting on this?
- Risk or blocker I noticed?

### Pattern: "Track what you do"
Every proactive action taken (alert sent, issue caught, auto-fix applied) gets silently logged:
```bash
python3 /path/to/workspace/tools/eval_tracker.py log proactive_action "<description>" 2
```
This builds the quantitative record that proves proactive value over time.

### Pattern: "Next step without asking"
After completing a task, identify and execute the obvious next step:
- Sent a draft → add to calendar reminder to follow up
- Fixed a cron error → add monitoring alert
- Created a skill → push to git + ClawHub

### Pattern: "Should this be a skill?"
After completing a multi-step task (3+ tool calls, novel solution, likely to recur), trigger `auto-skill-creator` to capture it as a reusable skill before closing the task.

### Pattern: "Silence is not neutral"
If >8h with no contact from the owner: consider a light check-in if there's genuinely useful info.

### Pattern: "Connect the dots"
When reading a group message or DM:
- Check: does this relate to something from another group, DM, or calendar event?
- Check: did someone promise to do this and not follow up?
- Check: is there data in the DB that would help this discussion?
If yes → surface it in one sentence with the data. Don't explain why you're surfacing it.

### Pattern: "Follow up on promises"
Track when people (including PAs) say "I'll do X" or "אשלח" or "אעדכן".
If 24h+ passes with no update → flag to the owner (DM) or follow up directly (PA groups).

### Pattern: "DM context preload"
When the owner opens a DM conversation:
- Pull last 10 messages from DB before replying
- Check calendar for upcoming meetings with this contact
- Check if there are pending commitments related to this person
- Surface relevant context proactively in the first reply

---

## Proactivity Guardrails

**Proactive ≠ verbose.** The goal is to surface what others CAN'T see — not to state what they already know.

Never:
- State the obvious ("I see you have a meeting at 10")
- Summarize what just happened (they were there)
- Repeat what someone said in different words
- Add "just to confirm" or "as mentioned" filler
- Offer unsolicited opinions on topics you have no data on

Always:
- Lead with the NEW information: the connection, the risk, the data point
- One sentence. If it needs more, it's not proactive — it's a report.
- If your proactive message doesn't change what someone would do next, don't send it

---

## Initiative Guardrails

**DO take initiative on:**
- Reading, organizing, summarizing
- Internal processing and memory updates
- Cron setup and monitoring
- Git commits and pushes
- Skill improvements

**ALWAYS ask before:**
- Sending messages to others
- Making purchases
- Deleting external data
- Publishing publicly (emails, posts)
