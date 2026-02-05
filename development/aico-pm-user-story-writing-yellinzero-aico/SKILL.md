---
name: aico-pm-user-story-writing
description: |
  Transform requirements into well-structured User Stories using "As a [user], I want [goal], So that [benefit]" format with Given/When/Then acceptance criteria.

  Use this skill when:
  - User asks to "write user story", "create story", "add story"
  - User mentions "user story", "backlog item", "story"
  - Running /pm.plan and need to break PRD into implementable stories
  - Creating backlog items for development team
  - Need to formalize a requirement into standard story format
  - Converting feature request into actionable story with acceptance criteria

  Output: ALWAYS write story files to docs/reference/pm/stories/{story-name}.md
---

# User Story Writing

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Identify user type**: Who benefits from this feature
2. **Define goal**: What they want to do
3. **Clarify value**: Why it matters to them
4. **Write acceptance criteria**: 3-5 Given/When/Then scenarios
5. **Add metadata**: Priority, complexity, dependencies
6. **Save story**: ALWAYS write to `docs/reference/pm/stories/{story-name}.md`

## Story Template

```markdown
# [STORY-ID] Story Title

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD

**As a** [user type]
**I want** [goal/action]
**So that** [benefit/value]

### Acceptance Criteria

- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]

### Notes

- Priority: P1/P2/P3
- Estimated complexity: S/M/L/XL
- Dependencies: [list any dependencies]
```

## Key Rules

- ALWAYS specify the user type (who benefits)
- MUST focus on user value, not technical solution
- ALWAYS include 3-5 testable acceptance criteria
- Use Given/When/Then format for all criteria
- MUST save to `docs/reference/pm/stories/` directory

## Common Mistakes

- ❌ Vague acceptance criteria → ✅ Specific, testable conditions
- ❌ Solution-focused stories → ✅ Focus on user value
- ❌ Missing user type → ✅ Always specify who benefits
