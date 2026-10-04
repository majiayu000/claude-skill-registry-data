---
name: self-learning
description: "Continuous self-improvement through systematic logging, pattern detection, and behavioral updates. Use when: the owner corrects you, a task fails, you discover a better approach, or you notice a recurring pattern. Store raw learnings in .learnings/, update the specific skill or workflow that caused the issue when appropriate, and avoid vague promises to do better."
---

# Self-Learning

Use this skill to turn corrections and failures into concrete local improvements.

## Scope

Default storage is:
- `.learnings/LEARNINGS.md` for reusable lessons
- `.learnings/ERRORS.md` for failures and breakages
- `.learnings/FEATURE_REQUESTS.md` for missing capabilities

Prefer updating the specific local skill or workflow that caused the issue.
Do not change core identity/bootstrap files unless the owner explicitly asks for that level of system change.

## Immediate loop

1. Log the event before closing the task.
2. State the root cause in one sentence.
3. Apply the smallest durable fix you can make now.
4. If no concrete fix is possible, say why and what evidence would unblock it.

## When to log

| Trigger | File | Category |
|---|---|---|
| Owner correction | `LEARNINGS.md` | `correction` |
| Task failure | `ERRORS.md` | `failure` |
| Skill produced bad output | `ERRORS.md` | `skill_failure` |
| Better approach discovered | `LEARNINGS.md` | `best_practice` |
| Missing capability | `FEATURE_REQUESTS.md` | `feature_request` |
| Repeated mistake | `LEARNINGS.md` | `pattern` |
| Good result worth repeating | `LEARNINGS.md` | `positive_signal` |

## Entry format

```markdown
## YYYY-MM-DD | category | short title
- Trigger: what happened
- Context: what you were trying to do
- Root cause: why it happened
- Durable fix: file/process/skill you changed, or `none yet`
- Verification: how to tell the problem is gone
```

## Promotion rules

Promote a learning when it is specific and repeatable.

- If the issue belongs to one skill, update that skill's `SKILL.md`.
- If the issue belongs to a reusable local workflow, update the nearest local checklist/script.
- If the issue depends on missing credentials, external systems, or policy decisions, log it and stop. Do not invent a fake fix.

## Pattern review

During reflection or cleanup work:

1. Scan `.learnings/` for repeated categories or titles.
2. Group duplicates.
3. Make one concrete change per pattern.
4. Add a short verification note to the newest entry.

## Quality bar

A learning is only complete when at least one of these is true:
- a local skill was improved
- a broken instruction was removed
- a missing prerequisite was documented clearly
- a recurring mistake was converted into a shorter, safer workflow

Not enough:
- "be more careful"
- generic promises
- long postmortems without a file or process change

## Skill Failure Tracking (inspired by agentic-stack)

Track when a skill fails or produces bad output. After a threshold, flag it for review.

### How to track
When a skill fails or gives wrong results, log it in `.learnings/ERRORS.md` with category `skill_failure`:

```markdown
## YYYY-MM-DD | skill_failure | <skill-name>: short description
- Trigger: what the user asked
- Skill: <skill-name>
- Root cause: why the skill failed
- Durable fix: what was changed, or `none yet`
```

### Auto-flag threshold
During pattern review, count `skill_failure` entries per skill in the last 14 days:
- **3+ failures in 14 days** → flag the skill for rewrite/review
- Add a `## FLAGGED FOR REVIEW` section at the top of that skill's SKILL.md
- Notify owner in the next daily summary: "Skill X failed 3+ times in 2 weeks, flagged for review"

### Resolution
- Fix the skill → remove the FLAGGED section
- If the skill is unfixable → document the limitation and stop routing to it for those cases

## Weekly Retro (inspired by gstack /retro)

Every Sunday (or when owner asks "what did we ship"), generate a structured weekly retrospective:

### Data Sources
- Git log from workspace repo (last 7 days)
- `.learnings/` entries from the week
- Daily memory notes (`memory/daily/`)
- Cron execution history

### Retro Format
```markdown
## Weekly Retro — YYYY-MM-DD

### Shipped
- [commit/action]: what was delivered

### Patterns
- Recurring issues or wins from the week

### Learnings Applied
- Which learnings led to concrete skill/workflow changes

### Failures
- What broke, root cause, fix status

### Next Week
- Top 3 priorities based on patterns
```

### Trend Tracking
Store retros in `memory/retros/YYYY-WXX.md` (e.g., `2026-W16.md`).
Compare with previous week's retro when generating:
- Are the same issues recurring? Flag them.
- Did last week's priorities get addressed?
- Is failure count trending up or down?

### Cron Setup
Add as a Sunday cron (low-cost model, ~60s):
```
Schedule: 0 10 * * 0 Asia/Jerusalem
Model: haiku
Prompt: "Run weekly retro. Check git log, learnings, daily notes from past 7 days. Write retro to memory/retros/. DM summary to owner."
```

## Cost tips

- Use short factual entries.
- Batch pattern review; do not re-scan logs after every single correction.
- Prefer editing one skill precisely over writing large reflective notes.
