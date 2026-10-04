---
name: room-manager
description: >
  Poll all agency chat rooms for new messages, route escalations, handle NEXUS
  handoffs, fan out PD statuses to department rooms, update shared context, throttle
  member notifications, and generate 12-hour digests for dept heads. Run as a
  background subagent on cron. Trigger with /room-manager or when new room activity
  is suspected. When to trigger: every 10 minutes as a background loop; when a user
  suspects new room activity; after a handoff file appears in a room handoffs/ dir;
  when an ESCALATE: pattern is spotted in any message; and when a dept head hasn't
  received their 12-hour digest yet. Key capabilities: offset-based message
  checkpointing (never re-reads old messages), 30-minute per-member notification
  throttle to prevent spam, idempotent digest sends, NEXUS handoff lifecycle
  management (pending/routed/expired), and automatic DECIDED:/ACTION:/QUESTION:
  extraction to shared agency context. Ideal for agency leads running multi-project
  coordination who need a passive, always-on coordination layer. Also for on-call
  subagents that need to stay informed about cross-project activity without
  manually polling every room.
---

# RoomManager Polling Cycle

Run this skill as a recurring background subagent. Default interval: every 10 minutes.

The digest sub-skill (Step 9) fires every 12 hours and can be run independently via
`/room-manager-digest`.

---

## Dept-to-Project Mapping

```
engineering   → (your projects)
marketing     → (your projects)
sales         → (your projects)
specialized   → (your projects)
operations    → (your projects)
testing       → (your projects)
product       → (your projects)
project-management → (your projects)
```

---

## State File

Read `~/.claude/agency-rooms/.room-manager/state.json` for:
- `last_poll`: ISO timestamp of last full cycle
- `room_checkpoints.{room}.last_msg_offset`: last line read per room
- `member_notifications.{room}.{member}`: last notification timestamp (for 30-min throttle)
- `dept_room_offsets.{dept}`: last rolling.md line count per dept room
- `last_digest`: ISO timestamp of last 12h digest run

---

## Step 1: Discover Rooms

Scan `~/.claude/agency-rooms/` for subdirectories. Each subdirectory = one room.
Exclude `.room-manager/`.

---

## Step 2: Check Each Room for New Messages

For each room, read `messages.mdl` (or `messages.md`) from the last checkpoint offset.
Update `last_msg_offset` in state.json after reading.

Project rooms to check: Scan dynamically from `~/.claude/agency-rooms/` directory.
Include agency-council, project-oversight, and all project-specific rooms.

Department rooms: engineering, marketing, sales, specialized, operations, testing,
product, project-management (read from offset 0 each cycle — no checkpoint needed for
rolling.md reads, they are write-only from RM perspective)

---

## Step 3: Route Escalations

Search all new messages for `ESCALATE:` patterns.
If found, route immediately to council-chair via SendMessage.

Pattern: any line containing `ESCALATE:` (case-insensitive).

---

## Step 4: Check NEXUS Handoffs

See `~/.claude/agency-rooms/HANDOFF-PROTOCOL.md` for the full schema and lifecycle.

Scan `~/.claude/agency-rooms/{room}/handoffs/` for `*.json` files where status is `pending`.
- Check `expires_at` — if past, set status = `expired` and move to `handoffs/archive/`
- If valid: set status = `routed`, send SendMessage to target_agent (or announce in
  target_room), rewrite file
- If priority = `high`: escalate to council-chair first
- Move acknowledged/expired files to `handoffs/archive/` after processing
- Increment `handoffs_routed` in state.json

---

## Step 5: Fan Out to Department Rooms

For each project room with new messages, extract PD status blocks (the `## {Project} Status`
sections) and push a summary to the appropriate dept room's `context/rolling.md`.

**Dept assignment** from room.json of each project room, or fallback to the mapping above.

**Rolling.md format per entry** (max 1 entry per PD per project per cycle — skip if
the most recent entry is identical):

```
### [{timestamp}] {pd-name} ({project})

**Working On:** {bullets}
**Blockers:** {bullets or "None"}
**Wins:** {bullets or "None this cycle"}
**Next:** {bullets}
```

**Rules:**
- Append new entries to the top of rolling.md (newest first)
- Keep only the **last 3 entries per PD** — trim older entries beyond that
- Deduplicate: if the "Working On" block is identical to the most recent entry for
  this PD, skip the write (no duplicate noise)
- If the project room has no status block in the new messages, skip fan-out for that room
- Dept rooms accumulate history across cycles — no auto-clear

---

## Step 6: Update Shared Context (Agency-wide)

Read all new messages and extract patterns:
- `DECIDED:` → append to `~/.claude/agency-rooms/context/shared.md` under Decisions
- `ACTION:` → append to `~/.claude/agency-rooms/context/shared.md` under Actions
- `QUESTION:` → append to `~/.claude/agency-rooms/context/shared.md` under Questions

---

## Step 7: Throttled Member Notifications

For each room with new messages, identify members who have unread messages.
Send a SendMessage notification to each member, **throttled to 30 minutes per member
per room**. Do NOT notify the sender of their own message.

Update `member_notifications` in state.json with the current timestamp.

---

## Step 8: Update State

Write updated `state.json`:
- Set `last_poll` to current timestamp
- Update `room_checkpoints.{room}.last_msg_offset` for each room
- Increment `escalations_routed` if any
- Increment `handoffs_routed` if any

---

## Step 9: 12-Hour Dept Head Digest (sub-skill)

Check `state.json` — if `last_digest` is more than 12 hours ago OR missing,
generate digests for all department heads.

### Digest Generation

For each dept room, read `context/rolling.md` and:
1. Extract all entries from the last 12 hours (filter by timestamp)
2. If no new entries: skip — no digest needed
3. Generate a **one-paragraph summary per team member** (condense their entries)
4. Generate a **one-line team status** (e.g. "3 active, 1 blocked, 0 idle")

### Digest Format (SendMessage to dept head)

```
Engineering Team Digest — {date}

Overall: 3 active, 1 blocked, 0 idle

### {member-name}
{one-paragraph summary of their last 12h of work}

---
Sent by RoomManager digest. Check full status feed at:
~/.claude/agency-rooms/engineering/context/rolling.md
```

### Digest Rules
- Only send if there are **new entries** in the last 12 hours — don't send empty digests
- Skip if `last_digest` is < 12 hours ago
- After sending, update `last_digest` to now in state.json

---

## Step 10: Log

Append to `~/.claude/agency-rooms/.room-manager/log.md`:
```markdown
[YYYY-MM-DD HH:MM] Polled N rooms, X new messages, Y escalations, Z handoffs, W dept fans, Digest sent: {yes/no}
```

---

## Run as Subagent

**RoomManager (10 min cycle):**
```
/loop 10m /room-manager
```

**Digest only (12h cycle — fires inside /room-manager but can also run standalone):**
```
/loop 12h /room-manager-digest
```
Or invoke directly as a separate cron. The digest sub-skill (Step 9) checks `last_digest`
internally, so running it standalone or alongside the main cycle is safe — it will
only send when 12+ hours have passed.

Or spawn as a persistent background agent:
```
Agent → room-manager (loop) → die on explicit shutdown
```
