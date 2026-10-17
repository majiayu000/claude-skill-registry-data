---
name: retro-synthesizer
description: |
  Synthesize sprint retrospective notes into categorized action items and patterns. Use this skill when:
  - You have sprint retro notes (raw text, meeting transcript, or structured notes) to process
  - You need to identify recurring patterns across multiple retros
  - You want categorized action items with owners and deadlines from retro discussions
---

# Retro Synthesizer

Process sprint retrospective notes into structured action items, recurring patterns, and process improvement recommendations.

## Workflow

1. **Accept input** — User pastes retro notes or provides file path
2. **Categorize items** into: What went well, What didn't go well, Action items
3. **Tag categories**: Process, Technical, Team, External
4. **Identify patterns** — If previous retro outputs exist, compare for recurring themes
5. **Generate recommendations**
6. **Output** — Print to conversation

## Categories

| Category | Covers |
|----------|--------|
| **Process** | Sprint planning, estimation, ceremonies, communication, standups |
| **Technical** | Code quality, tech debt, tooling, CI/CD, testing, deployments |
| **Team** | Collaboration, knowledge sharing, workload balance, onboarding |
| **External** | Dependencies, stakeholder communication, blockers from outside |

## Output Format

```markdown
# Retro Summary — Sprint {N} ({Date})

## What Went Well
| Category | Item | Impact |
|----------|------|--------|
| Process | {description} | {why it mattered} |

## What Didn't Go Well
| Category | Item | Root Cause | Frequency |
|----------|------|-----------|-----------|
| Technical | {description} | {why it happened} | First time / Recurring |

## Action Items
| # | Action | Owner | Deadline | Category | Priority |
|---|--------|-------|----------|----------|----------|
| 1 | {specific action} | {name} | {date} | {category} | High/Med/Low |

## Recurring Patterns
{Items that appeared in 2+ retros — flag for systemic fix}

## Process Improvement Recommendations
1. {Specific recommendation with rationale}
2. {Specific recommendation with rationale}
```

## Rules

- Every action item MUST have an owner (name, not "team") and deadline
- Flag items recurring across 2+ retros as "Recurring" — these need systemic fixes
- Recommendations must be specific and actionable ("Add PR size limit of 400 lines" not "Improve code review")
- If no previous retros available, skip "Recurring Patterns" section

## Anti-Patterns

- Don't assign action items to "the team" — assign to a person
- Don't write vague recommendations — be specific enough to act on
- Don't ignore "went well" items — they validate what's working

## Quality Checklist

- [ ] Every action item has an owner and deadline
- [ ] Categories applied to all items
- [ ] Recurring patterns identified (if history available)
- [ ] Recommendations are specific and actionable
