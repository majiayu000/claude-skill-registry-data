---
name: decision-log
description: Decision recording + result tracking skill
author: 무펭이 🐧
---

# decision-log

Skill for recording important decisions and automatically tracking results after 30 days.

## Features

- Record decision content, rationale, alternatives, expected results
- Auto-review results after 30 days (cron integration)
- File save: `memory/decisions/YYYY-MM-DD-{slug}.md`

## Usage

Trigger keywords:
- "record decision"
- "decision log"
- "made this decision"
- "why did I do this"

Example:
```
Record decision: Decided to separate Instagram bot account
Rationale: Distribute main account ban risk
Alternatives: Use main account, manual operation
Expected results: Increased safety, increased management complexity
```

## Output Format

```markdown
# Decision: {title}

**Date**: YYYY-MM-DD  
**Status**: Decided / Review Pending / Results Confirmed

## Decision Content
...

## Rationale
- ...
- ...

## Alternatives Considered
1. **Alternative 1**: ...
   - Pros: ...
   - Cons: ...
2. **Alternative 2**: ...

## Expected Results
- Positive: ...
- Negative: ...

## Actual Results (Auto-update after 30 days)
_Review date: YYYY-MM-DD_

---

**Decision date**: YYYY-MM-DD | **Review date**: YYYY-MM-DD (scheduled)
```

## Auto-review (cron)

After 30 days, automatically:
1. Compare expected vs actual results
2. Extract lessons learned
3. Generate insights for similar future decisions

## Event Bus Integration

Publish event when recording decision:
- Path: `events/decision-YYYY-MM-DD.json`
- Format:
```json
{
  "type": "decision-logged",
  "timestamp": "2026-02-14T12:00:00Z",
  "title": "Decision title",
  "reviewDate": "2026-03-16",
  "filePath": "memory/decisions/2026-02-14-slug.md"
}
```

---

**decision-log** | 무펭이 🐧
