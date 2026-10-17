---
name: stakeholder-update
description: |
  Generate structured weekly or fortnightly status updates for leadership and stakeholders. Use this skill when:
  - You need to prepare a weekly or fortnightly status report
  - You want to summarize recent progress across git commits, tickets, and spec changes
  - You need a formatted update ready for Slack, email, or a stakeholder meeting
  - You want multi-project updates in one report
---

# Stakeholder Update

Generate status updates by aggregating data from git history, issue tracker, and spec file changes.

## Workflow

1. **Determine period** — Default: last 7 days
2. **Gather data** from 3 sources:
   - **Git:** `git log --since="{period}" --oneline --no-merges`
   - **Tickets:** Search for recently updated issues
   - **Specs:** Find recently modified spec files
3. **Categorize** items into the 5 sections below
4. **Write update** — Print to conversation

## Output Format

```markdown
# Status Update — {Start Date} to {End Date}

## Highlights
- {What shipped/completed — 2-5 bullets, lead with outcomes}

## In Progress
- {Active work with brief context — 2-5 bullets}

## Blocked
- {What needs unblocking + WHO can unblock}

## Next Period
- {Planned work — 2-4 bullets}

## Risks
- {Anything leadership should know — include likelihood H/M/L and impact}
```

Omit "Blocked" and "Risks" sections if empty.

## Writing Rules

- Start each bullet with an action verb: Shipped, Completed, Started, Drafted, Reviewed, Fixed
- Include ticket keys where relevant
- 1-2 lines per bullet max
- **Blocked** items: always include WHO can unblock
- **Risks**: include likelihood and impact
- **Highlights** focus on outcomes, not activities
- No filler language — leadership reads fast

## Multi-Project Mode

If multiple projects, repeat the 5-section structure per project:

```markdown
## Project: [Project A]
### Highlights
...

## Project: [Project B]
### Highlights
...
```

## Anti-Patterns

- Don't list activities without outcomes — "Wrote tests" vs "Increased test coverage to 85%"
- Don't leave Blocked items without naming who can unblock
- Don't include risks without likelihood/impact

## Quality Checklist

- [ ] Highlights lead with outcomes
- [ ] Blocked items name the unblocker
- [ ] Risks include likelihood and impact
- [ ] Bullets start with action verbs
- [ ] Under 2 lines per bullet
