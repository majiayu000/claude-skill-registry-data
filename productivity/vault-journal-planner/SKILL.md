---
name: vault-journal-planner
description: Manage periodic notes — daily/weekly/monthly/yearly journaling, planning, and reviews with the vault's period-note templates. Use when the user says "open today's note", "plan my month", "yearly review", or wants time-based organization. NOT for the personal weekly review + next-week plan ritual (use eos-week-review) or cross-week trend reflection (use eos-life-insights).
---

# Journal & Planner

Comprehensive skill for all time-based notes: daily, weekly, monthly, yearly.

## File Locations

| Type | Path Pattern | Template | Naming |
|------|--------------|----------|--------|
| Daily | `50_Journal/YYYY/YYYY-MM-DD.md` | `template/daily.md` | `2026-01-05.md` |
| Weekly | `50_Journal/YYYY/YYYY-WNN.md` | (see note-templates.md) | `2026-W02.md` |
| Monthly | `50_Journal/YYYY/YYYY-MM.md` | `template/monthly.md` | `2026-01.md` |
| Yearly | `50_Journal/YYYY/YYYY.md` | (manual) | `2026.md` |

## Reference files (read on demand)

`SKILL_DIR` = `{home}/.claude/skills/vault-journal-planner/`. The harness loads only this file; read a sibling with the Read tool when you reach the step that needs it.

| File | Priority | Read when |
|---|---|---|
| `<SKILL_DIR>/note-templates.md` | Required | Creating or filling any daily / weekly / monthly / yearly note |
| `<SKILL_DIR>/task-system.md` | Required | Any task syntax, query, or time-block work |
| `<SKILL_DIR>/cli-reference.md` | Reference | Driving Obsidian via obs.sh / task-manager.py |

---

## Hierarchy

```
YYYY.md (年度目标 + 季度重点)
  └── YYYY-MM.md (月度计划 + 生活领域)
        ├── YYYY-WNN.md (周计划 + 每日安排)
        │     └── YYYY-MM-DD.md (每日日志)
        └── Weekly Reviews 区块 (链接到周笔记)
```

---

## Daily Notes

Structure template: see `note-templates.md` → Daily Notes.

### Quick Journal Entry

**User says**: "journal today" / "I did X, Y, Z"

**Workflow**:
1. Create/open `50_Journal/YYYY/YYYY-MM-DD.md`
2. Fill Journal section with activities
3. Link people: `[[@Person]]` + (platform)
4. Infer Three Successful Things
5. Add Reflection if appropriate

### Activity Formatting

| Type | Format |
|------|--------|
| General | `- Went to library` |
| Person | `- Talked with [[@Person]] (phone/WeChat/IG)` |
| Place | `- Went to [[Place Name]]` |
| Creative | `- Produced songs` |
| Blocker | `- Blocker: description` |

---

## Weekly Notes

Structure template: see `note-templates.md` → Weekly Notes.

### Weekly Planning

**User says**: "plan next week" / "周计划"

**Workflow**:
1. Determine week number (W01, W02, etc.)
2. Create `50_Journal/YYYY/YYYY-WNN.md`
3. Fill Schedule table with:
   - Fixed events (运动、会议)
   - Key tasks by day
   - Links to daily notes and places
4. Set Focus section with week theme and key tasks
5. Link from monthly note's Weekly Reviews section

### Weekly Review

**User says**: "weekly review" / "这周怎么样"

**Workflow**:
1. Open current week's note
2. Check Schedule - what was done vs planned
3. Fill Review section:
   - 完成: List completed items
   - 未完成: List incomplete items
   - 下周改进: Lessons learned
4. Update monthly note's Hours Log if applicable

---

## Monthly Notes

Structure template: see `note-templates.md` → Monthly Notes.

### Monthly Planning

**User says**: "plan this month" / "月度计划"

**Workflow**:
1. Open/create monthly note
2. Review yearly goals for context
3. Set month theme
4. Update life area sections with goals
5. Add key tasks with due dates

### Monthly Review

**User says**: "monthly review"

**Workflow**:
1. Review all weekly notes from that month
2. Summarize by life area
3. Score each area (完成度)
4. Update Hours Log totals
5. Note progress toward yearly goals

---

## Yearly Notes

Structure template: see `note-templates.md` → Yearly Notes.

---

## Quick Commands

| User Says | Claude Does |
|-----------|-------------|
| "journal today" | Create/update daily note |
| "plan next week" | Create weekly note with schedule |
| "weekly review" | Summarize and review the week |
| "plan this month" | Create/update monthly note |
| "monthly review" | Summarize month by life area |
| "year in review" | Comprehensive yearly analysis |
| "what did I do on [date]" | Read that daily note |

---

## Cross-Cutting Workflows

### Add Event to Calendar

**User says**: "周一 5:30pm Zumba at Chatswood"

**Workflow**:
1. Identify: day, time, activity, location
2. Add to weekly note's Schedule table
3. Create/link Place note if new location
4. Add recurring pattern if applicable

### Log Person Interaction

When person mentioned:
1. Link: `[[@Person]]` + (platform)
2. Consider updating `last_contact` in person note
3. Add to daily note's Journal section

### Navigate Time

| User Says | Action |
|-----------|--------|
| "yesterday" | Previous day's note |
| "last week" | Previous week's note |
| "this week" | Current week's note |
| "next week" | Create/open next week's note |

---

## Entity Detection

When processing entries, detect and offer to create notes:

| Entity | Trigger | Routes To |
|--------|---------|-----------|
| Person | "talked to X" | → note-factory → people-manager |
| Place | "went to X" | → note-factory |
| Book | "reading X" | → note-factory → media-library |
| Movie | "watched X" | → note-factory → media-library |

---

## Task Management System

Full reference — time-blocks vs tasks, architecture, locations, syntax, queries, and patterns: see `task-system.md`.

---

## Events Integration

Events (重要多人事件) 与日记系统的联动：

| 方向 | 实现 |
|------|------|
| Event → 日记 | Event 模板自动链接到日期 `[[YYYY-MM-DD]]` |
| 日记 → Events | 日/周模板 Dataview 查询显示相关 Events |
| People → Events | People 模板自动显示涉及该人的 Events |

**相关文件:**
- Event 模板: `30_Resources/Technology/template/@ for event.md`
- Events 存放: `Timestamps/Events/`
- Events MOC: `20_Areas/_Events MOC.md`

---

## Obsidian CLI (Quick Journal Queries)

CLI snippets + fallbacks for driving Obsidian via `obs.sh` / `task-manager.py`: see `cli-reference.md`.

## Integration

- **note-factory**: Routes entity creation with pre-checks
- **people-manager**: Update `last_contact` for interactions
- **media-library**: Book/movie note templates
- **Project Trackers**: `189-Visa-Tracker`, `Job-Search-Tracker` for detailed tracking
- **Events**: 重要多人事件自动显示在日/周记和相关人物笔记

---

## Verify after writing

After writing or updating a periodic note: re-read it to confirm the frontmatter is intact and the expected sections exist. If you added `[[wikilinks]]` to people/projects, run the vault's `generate-link-index.py --broken` and fix any broken link you introduced. Never overwrite a user-written section — append.
