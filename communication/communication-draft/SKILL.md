---
name: communication-draft
description: Draft professional communications. Use when writing emails, Slack messages, meeting follow-ups, status updates, or any professional correspondence. Triggers on "draft email", "write message", "meeting follow-up", "send update", or "compose response".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Communication Draft

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Draft professional communications across contexts with appropriate tone.

## Communication Types

- **Email:** `draft email to [person] about [topic]`
- **Slack:** `draft slack message for [channel/person]`
- **Meeting follow-up:** `draft follow-up after [meeting]`
- **Status update:** `draft status update for [project]`

## Context-Aware Tone

| Context | Tone |
|---------|------|
| Work | Professional, collaborative, technically accessible |
| Community | Community-focused, inclusive, consensus-building |
| Consulting | Formal, contractor-appropriate, deliverable-focused |
| Side Project | Business-professional, risk-aware, technical leadership |

> Customize these to match your own contexts.

## Templates

### Standard Email
```
Subject: [Clear, actionable subject]
Hi [Name],
[Context/Reference]
[Body — 2-3 paragraphs max]
[Action items or next steps]
[Closing]
```

### Meeting Follow-up
```
Subject: Follow-up: [Meeting] - [Date]
**Key Decisions:** bullet list
**Action Items:** table (Item | Owner | Due)
**Next Steps:** paragraph
```

### Status Update
```
Subject: [Project] Status Update - Week of [Date]
**Summary:** one line
**Progress:** bullets
**In Progress:** bullets
**Blockers/Risks:** bullets
**Next Week:** bullets
```

### Slack Quick Update
```
:rocket: **[Project] Update**
- Point 1
- Point 2
```

## Autonomy Levels

| Communication | Level | Behavior |
|---------------|-------|----------|
| Internal status/notes | 1 | Draft and present |
| Internal team message | 2 | Draft, review, send |
| External (known contact) | 2 | Draft for approval |
| External (new) / sensitive | 3 | Draft for approval |

## Output Format

```
## Draft: [Type]
**To:** [Recipients] | **Context:** [context] | **Tone:** [tone]
---
[Full draft content]
---
**Ready to send?** Let me know if you'd like changes.
```

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
