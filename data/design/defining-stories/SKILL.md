---
name: defining-stories
description: Guides creation of user stories and epic design documents. Use when defining new features, writing Given-When-Then criteria, creating story logs, or designing larger features that need scope definition.
---

# Defining Stories

## Epic vs Story

| Document | Purpose | When to Create |
|----------|---------|----------------|
| **Epic** | Design document defining scope and technical approach | Starting a larger feature |
| **Story** | Incremental deliverable with acceptance criteria | As needed during development |

**Agile approach**: Stories emerge during development. Create each story when ready to implement.

## User Story Format

```
As a [role], I want [capability], so that [benefit].
```

## Acceptance Criteria

```markdown
- [ ] **Given** [precondition], **When** you [action], **Then** [expected result]
```

- Focus on user-observable behavior
- Include happy paths AND error cases
- Leave checkboxes unchecked (PO checks them)

## Verification Approach

Define how criteria will be verified:

| Project Type | Options |
|--------------|---------|
| CLI | Direct command execution |
| API | curl/httpie, API testing tools |
| Web UI | E2E tests, browser MCP tools |
| Mobile | Device/emulator, MCP tools |
| Library | Unit/integration tests |

If MCP tools or skills for testing are available, use them. If unsure, ask PO.

## Story Log

File: `docs/stories/<YYYYMMDDTHHMMSS>_<name>.story.md`

```bash
date -u +"%Y%m%dT%H%M%S"  # Generate timestamp
```

See [STORY_TEMPLATE.md](STORY_TEMPLATE.md) for structure.

## Epic Documents

Directory: `docs/stories/<YYYYMMDD>_<epic-name>/`
File: `<YYYYMMDDTHHMMSS>_<epic-name>.epic.md`

See [EPIC_TEMPLATE.md](EPIC_TEMPLATE.md) for structure.
