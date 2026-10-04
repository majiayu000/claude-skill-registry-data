---
name: ascent-feature-brief
description: Creates concise feature briefs for handoff to Claude Code. Use when users want to document a feature for implementation, need a spec for coding, want to capture architecture decisions for handoff, or are planning features to be built by an AI coding agent. Generates token-efficient implementation directives that communicate intent while delegating schema discovery to the coding agent.
---

# Feature Brief Generator

Create concise, token-efficient feature briefs that communicate implementation intent to Claude Code while delegating technical discovery to the coding agent.

## Design Philosophy

Feature briefs are **implementation directives**, not detailed design specs. They:

- Communicate *what* to build and *why*, not *how*
- Set boundaries and constraints clearly
- Delegate schema/codebase discovery to Claude Code
- Preserve context window for actual implementation work

## Brief Structure

### Task List Link (When Available)

**When a task list exists for the feature, include a link to it immediately after the title.**

This creates bidirectional linking between the brief and task list for easy navigation in Obsidian.

```markdown
# Feature Brief: [Feature Name]

**Task List:** [feature-name-tasks.md](feature-name-tasks.md)
```

**Guidelines:**
- Place the link on the line immediately after the main title
- Use Obsidian-compatible format: `[filename.md]` or `[filename.md](filename.md)`
- The filename should match the actual task list filename in the same folder
- Only add this link if a task list has been created
- This enables automatic linking in Obsidian and ensures traceability

### Content Sections

Generate briefs using this structure:

### 1. Summary (2-3 sentences)

State what we're building and the core user value. Be specific about the outcome.

**Good**: "Add workout sync functionality that pulls completed workouts from HealthKit and stores them in the app's database. This enables users to see their training history without manual entry."

**Weak**: "Implement HealthKit integration for workouts."

### 2. User Stories (bulleted, concise)

Key workflows in "As a user, I can..." format. Focus on observable behaviors, not implementation.

```
- As a user, I can see my completed workouts from Apple Watch in the app
- As a user, I can view workout details including duration, distance, and heart rate
- As a user, I can manually refresh to pull latest workouts
```

Limit to 3-6 stories. If more are needed, the feature may need splitting.

### 3. Behavior & Rules

How the feature should work. Include:

- Core business logic
- Data flow (conceptually)
- Edge cases worth highlighting
- Error states and how to handle them

Write as prose or short bullets. Avoid implementation details—focus on *what happens*, not *how it's coded*.

```
Workouts sync on app launch and manual refresh. Only workouts completed after 
the user's account creation date should sync. Duplicate detection uses the 
HealthKit workout UUID. If a workout already exists, skip it silently.

For workouts without GPS data, distance may be nil—display "—" in the UI.
```

### 4. Boundaries

Explicit scope limits. What this feature does NOT do.

```
Out of scope:
- Real-time streaming of in-progress workouts
- Editing or deleting synced workouts
- Syncing to other platforms (Strava, Garmin)
- Background sync (manual/app-launch only for v1)
```

This prevents scope creep during implementation.

### 5. Implementation Guidance

Instructions for Claude Code. This is the prompt engineering section.

Standard template:

```
## Implementation Guidance

Before implementing:
1. Query the database schema to understand current table structures
2. Examine existing patterns in [relevant area/module]
3. Review how similar features handle [relevant concern]

Propose a plan before writing code. Include:
- Which tables/models will be created or modified
- Key functions or services needed
- How this integrates with existing code

[Any feature-specific technical hints, e.g.:]
- Use the existing HealthKitService for Apple Health integration
- Follow the medallion architecture pattern (Bronze → Silver → Gold)
- Coordinate with the existing sync queue for background operations
```

Adjust based on what's relevant to the feature.

## Output Format

Present the brief in a clean, copy-paste-ready format with **Obsidian-compatible YAML frontmatter**:

```markdown
---
status: not_started
priority: [high | medium | low]
agent: claude-code
created: YYYY-MM-DD
tags: [tag1, tag2]
---
# Feature Brief: [Feature Name]

**Task List:** [feature-name-tasks.md](feature-name-tasks.md) _(Add this link when task list is created)_

## Summary
[2-3 sentences]

## User Stories
- As a user, I can...
- As a user, I can...

## Behavior & Rules
[Prose describing how it works]

## Boundaries
Out of scope:
- [Item]
- [Item]

## Implementation Guidance
[Instructions for Claude Code]
```

### YAML Frontmatter Fields

All feature briefs **must include** these frontmatter fields for Obsidian dashboard tracking:

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `status` | Yes | `in_progress`, `testing`, `not_started`, `blocked`, `complete` | Current state of the feature |
| `priority` | Yes (in_progress/not_started) | `critical`, `high`, `medium`, `low` | Feature priority level |
| `agent` | Yes | `claude-code`, `human`, `team` | Who/what is working on it |
| `created` | Yes | `YYYY-MM-DD` | Date the brief was created |
| `started` | Yes | `YYYY-MM-DD` | When work started |
| `completed` | If complete | `YYYY-MM-DD` | Completion date |
| `tags` | Yes | Array of strings | Searchable tags |
| `notes` | Yes | Multi-line string | Brief description |
| `dependencies` | Optional | Array of strings | Other features/tasks that must complete first (e.g., `["feature-name (complete)"]`) |

### Tags

Include relevant tags for cross-cutting concern filtering. Common tags:

| Tag | When to use |
|-----|-------------|
| `ios` | Features with iOS/Swift implementation |
| `supabase` | Features touching database or Edge Functions |
| `ai` | Features using Claude API or AI processing |
| `ui` | Frontend/UI focused features |
| `backend` | Backend/API focused features |
| `analytics` | Data analytics features |
| `onboarding` | User onboarding related |

Example with all fields:
```yaml
---
status: in_progress
priority: high
agent: claude-code
created: 2025-12-12
started: 2025-12-15
tags: [ios, supabase, ai]
notes: |
  This feature depends on the workout sync infrastructure being complete.
  Priority: After hydration testing, before advanced dimensionality.
dependencies:
  - workout-sync (complete)
---
```

Minimal example (required fields only):
```yaml
---
status: not_started
priority: high
agent: claude-code
created: 2025-12-12
started: 2025-12-12
tags: [ios, supabase]
notes: |
  Brief description of the feature.
---
```

**Status transitions:**
- New briefs start as `not_started` with `created: YYYY-MM-DD`
- When implementation begins, change to `in_progress` and add `started: YYYY-MM-DD`
- When ready for testing, change to `testing`
- Use `blocked` if waiting on external dependencies
- Use `complete` when feature is done and add `completed: YYYY-MM-DD` (before archiving)

**Priority Requirements:**
- Required for `status: in_progress` and `status: not_started`
- Optional for `status: complete`, `status: testing`, `status: blocked`
- Priority values: `critical` (highest) → `high` → `medium` → `low` (lowest)

## Generating Briefs

When the user requests a feature brief:

1. **Clarify scope** if the feature is ambiguous—ask what's in/out before writing
2. **Extract user value** from the discussion—why does this matter?
3. **Identify boundaries** from what was discussed vs. deferred
4. **Write concisely**—every sentence should earn its tokens
5. **Include discovery instructions** appropriate to their codebase

## File Location & Folder Creation

**IMPORTANT:** Create folder first (`mkdir -p`), then write brief file, confirm location.

**Path:** `Docs/AscentTraining_Docs/features/[Feature-Name]/[feature-name]-brief.md`

**Naming:** Folders Title-Case with hyphens, files lowercase with hyphens. Reference `Docs/AscentTraining_Docs/README.md` for structure.

## Quality Checklist

Before delivering a brief, verify:

- [ ] **YAML frontmatter** includes status, priority, agent, and created fields
- [ ] **Task list link** is added at the top when a task list exists (using Obsidian format `[filename.md]`)
- [ ] Summary states clear user value, not just technical action
- [ ] User stories describe observable behaviors
- [ ] Behavior section covers happy path AND edge cases
- [ ] Boundaries explicitly list what's out of scope
- [ ] Implementation guidance tells Claude Code what to discover
- [ ] Total length is under ~400 words (token-efficient)
- [ ] No implementation details that Claude Code should discover itself
- [ ] **File saved** in `Docs/AscentTraining_Docs/features/[Feature-Name]/`

## Post-Creation Updates

**Note:** Dashboard auto-tracks file modification times. No manual `last_worked` updates needed.
