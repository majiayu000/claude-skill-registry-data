---
name: weeklyreview
description: Use when the user runs /weeklyreview or wants to do their weekly review. Processes the inbox, writes the weekly review note, and updates soul files (Now, Goals, Beliefs, Someday Maybe, Values).
---

# Weekly Review

Process the past week's inbox, synthesize learnings, write the review note, and keep soul files current.

## Step 1 — Determine the week

- Today's date → compute current ISO week number (YYYY-Www)
- The review covers **Monday–Sunday of the completed week**
- If today is Monday–Wednesday, the review is for the *previous* week
- If today is Thursday–Sunday, the review is for the *current* week (Mon–today)
- Review file path: `Reviews/YYYY-Www.md`

## Step 2 — Read all sources in parallel

| Source | What to extract |
|--------|----------------|
| `Inbox.md` | Every bullet point or paragraph — categorise each one |
| `Daily Notes/YYYY-MM-DD.md` for each day of the week | Todo list (checked/unchecked), Logs, reflections, Chinese entries |
| `Reviews/YYYY-Www.md` (existing file if any) | Weekly todo list (checked/unchecked items) |
| `Now.md` | Current 3-month focus — what has changed? |
| `Goals.md` | Current quarter goals — any progress or gaps? |
| `Beliefs.md` | Existing beliefs — any new ones surfaced this week? |
| `Someday Maybe.md` | Existing list — anything from inbox to add? |
| `Values.md` | Check if anything from the week deserves reflection here |
| `Knowledge/` (recent files) | Any new knowledge notes created this week |

## Step 3 — Process the Inbox

For every item in `Inbox.md`, decide its destination:

| Item type | Destination |
|-----------|-------------|
| Insight / belief / stance on something | → `Beliefs.md` (appropriate section) |
| Habit / reminder / recurring action | → relevant `Areas/` file |
| Long-term aspiration, book, resource, idea for later | → `Someday Maybe.md` |
| Rich enough insight to stand alone | → new `Knowledge/` note |
| Practical task with a deadline | → relevant `Projects/` or `Areas/` file |
| Already actioned / stale | → delete, no destination needed |

After categorising all items:
- Update each destination file with the new content
- Create new `Knowledge/` notes where warranted
- **Overwrite `Inbox.md`** with only the header line and Someday Maybe link (empty, ready for next week):

```markdown
Dump thoughts here, don't organize. Process weekly.

For long-term ideas, places to go, books to read → [[Someday Maybe]]
```

## Step 4 — Write the weekly review

Use this template. Fill every section — never leave a section blank.

```markdown
---
type: review
review-type: weekly
date: YYYY-MM-DD
week: YYYY-Www
---

Weekly Todo:
[copy the weekly todo checklist from the existing review file if it exists, or leave blank]

# Weekly Review — YYYY-Www

## 这周完成了什么
- [concrete completions from daily logs + checked todos]

## 这周没完成什么 & 为什么
- [unchecked todos + honest reason why]

## 这周学到了什么
- [insights, knowledge notes created, concepts understood — link to Knowledge notes where relevant]

## 下周最重要的 3 件事
1.
2.
3.

## 状态检查
- Energy level (1-5):
- Focus quality (1-5):
- 最大的阻碍是什么:

## 随想
[free prose — synthesise the week's emotional/motivational arc; include Chinese where natural]

---
*Links:* [[HOME]] | [[Reviews/Reviews Home]]
```

Rules for filling the review:
- Pull facts from daily note Logs only — don't invent
- For 下周最重要的 3 件事: derive from unchecked todos, Now.md priorities, and any upcoming deadlines
- For 状态检查: infer energy from daily note start times and tone; infer focus from how much got done vs planned
- 随想: synthesise the week's main theme — what was the thread running through it? Be honest, not performative
- Chinese reflections from daily notes: include them directly; don't translate

## Step 5 — Update soul files

Only update if there's a genuine change. Don't pad entries.

**`Now.md`** — update if:
- A project's status changed (new interview confirmed, application submitted, project stalled)
- A new active focus emerged from the week
- Update the `Last updated:` date

**`Goals.md`** — update if:
- A quarterly goal was achieved (mark it ✓)
- A goal needs to be revised based on what actually happened

**`Beliefs.md`** — add if:
- A new stance crystallised this week
- Add to the most specific section; add a new section heading if truly a new domain
- Keep entries short — one or two sentences max

**`Someday Maybe.md`** — add if:
- Any inbox items were flagged as long-term aspirations
- Add to the most relevant subsection; add a subsection if needed

**`Values.md`** — update only if:
- A core value was genuinely challenged, refined, or earned this week
- Don't add for minor events

## Output to user

After all writes are complete, output a compact summary:

---

**Week YYYY-Www reviewed.**

**Inbox cleared:** N items → [Beliefs: N | Knowledge: N | Someday Maybe: N | Areas: N | Deleted: N]

**Review written:** `Reviews/YYYY-Www.md`

**Soul files updated:** [list only the ones actually changed]

**Next week's top 3:**
1.
2.
3.

---

## Rules

- Write to files — don't just output to screen
- If the review file already exists, preserve the Weekly Todo checklist at the top; rewrite everything below it
- Never fabricate tasks — only use what appears in the daily notes
- If a daily note is missing for a day, skip that day silently
- Keep all Chinese text as-is — do not translate
