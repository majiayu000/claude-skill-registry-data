---
name: room-manager-digest
description: >
  Generate 12-hour activity digests for all department heads. Reads rolling.md feeds
  from each dept room, summarizes team activity from the last 12h, and sends a concise
  digest via SendMessage to each dept head. Run standalone every 12h or alongside the
  main RoomManager cycle. Idempotent — only sends when there are new entries. When to
  trigger: on a 12h cron schedule as a standalone job; merged into the main RoomManager
  cycle on its 12h digest check; manually via /room-manager-digest when a dept head
  requests a fresh report; after a long gap where several RoomManager cycles may have
  been missed; and when agency-wide visibility into cross-PD activity is needed for a
  planning meeting. Key capabilities: per-dept one-paragraph-per-person summaries that
  distill repeated rolling.md bullets into cohesive prose, team status counts (active/
  blocked/idle), strict 12h window filtering (no stale entries), and idempotent sends
  that skip depts with zero new activity. Ideal for VPs, department heads, and PM
  leads who want a concise team activity snapshot without logging into each room.
  Also useful for async standup replacements and for feeding into external dashboards
  or AI summarization pipelines.
---

# RoomManager Digest — 12-Hour Dept Head Report

This skill generates and sends one-paragraph digests to each department head.
It is safe to run as a standalone cron or merged into the main RoomManager cycle.

---

## Dept Head Mapping

| Dept | Head | Room |
|---|---|---|
| engineering | engineering-lead | engineering |
| marketing | marketing-lead | marketing |
| sales | sales-lead | sales |
| specialized | specialized-lead | specialized |
| operations | operations-lead | operations |
| testing | testing-lead | testing |
| product | product-lead | product |
| project-management | project-management-lead | project-management |

---

## State Check

Read `~/.claude/agency-rooms/.room-manager/state.json`:
- If `last_digest` is within 12 hours of now → **skip entirely**. No action needed.
- If `last_digest` is null, absent, or > 12 hours ago → proceed.

---

## Digest Generation

For each dept room in the mapping above:

1. **Read** `~/.claude/agency-rooms/{dept}/context/rolling.md`
2. **Filter entries** from the last 12 hours only (compare timestamps to current time minus 12h)
3. **If no new entries** in the last 12h → skip this dept. No digest sent.
4. **Group by team member** — collect all entries for each person in the last 12h
5. **Generate one-paragraph summary** per team member (condense repeated "Working On" bullets into a cohesive sentence)
6. **Count overall status**: active (has entries), blocked (has a blocker noted), idle (no entries)
7. **Generate digest** (see format below)
8. **Send** via SendMessage to the dept head
9. **Mark sent** — update `last_digest` to now in state.json after ALL depts are processed

---

## Digest Format (SendMessage to dept head)

```
Subject: {Dept} Team Digest — {date}

Overall: {N active}, {M blocked}, {K idle}

---

### {member-name}
{one-paragraph summary of their last 12h of work. Include blockers if present.}

---

Full rolling feed: ~/.claude/agency-rooms/{dept}/context/rolling.md
```

**Paragraph rule:** The digest must be readable in under 30 seconds. One paragraph per
person — no bullet lists in the digest itself. Details live in rolling.md.

---

## Digest Logic Rules

- **Idempotent:** If digest was already sent this 12h window, skip silently
- **Non-blocking entries:** "None" blockers should be noted briefly, not omitted
- **Skip empty depts:** A dept with 0 team members assigned → skip, no message sent
- **Update last_digest only after all sends succeed** — if one fails, don't mark the digest
  as sent; log the failure and retry next cycle
- **Log every send** to `~/.claude/agency-rooms/.room-manager/log.md`

---

## Log Entry

After processing all depts, append to `~/.claude/agency-rooms/.room-manager/log.md`:

```markdown
[YYYY-MM-DD HH:MM] Digest cycle — N depts checked, M digests sent, K skipped (no activity)
```

If a SendMessage fails for a dept head, log separately:

```markdown
[YYYY-MM-DD HH:MM] Digest send FAILED for {dept-head}: {reason}
```
