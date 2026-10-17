---
name: write-user-stories
description: >
  Write user stories with acceptance criteria. Use when the user says "write user stories",
  "convert this to stories", "create acceptance criteria", "break this into tickets",
  "story map", "walking skeleton", "story for this feature", or wants to translate
  a feature idea into sprint-ready items - even if they don't explicitly say "user stories".
---

## Overview

Based on **User Story Mapping** by Jeff Patton. Stories aren't just tickets - they tell a narrative. A story map has two dimensions: the user's journey across the top (the backbone), and depth below each step showing increasing detail. Releases are horizontal slices through the map, not vertical feature silos.

## Workflow

### Step 1: Build the Narrative Spine
Before writing individual stories, map the user's journey end-to-end. List the high-level activities in sequence - this is the backbone.

Example backbone for a checkout flow:
`Browse -> Select -> Review Cart -> Enter Details -> Pay -> Confirm`

### Step 2: Identify the Walking Skeleton
The walking skeleton is the thinnest possible slice that completes the full journey. It's not an MVP of features - it's an MVP of the flow. Every step in the backbone needs at least one story.

### Step 3: Write story headlines
Format: `As a [user type], I want [goal], so that [benefit].`

The "so that" clause is non-negotiable. If you can't write it, the story may not be worth building.

### Step 4: Write Acceptance Criteria
Use Given/When/Then for each criterion:
```
Given [precondition]
When [action]
Then [expected outcome]
```

3-7 criteria per story. Cover: happy path, error states, empty state, edge cases.

### Step 5: Slice into releases
Group stories into horizontal release slices:
- **Release 1:** Walking skeleton only - the minimum to complete the journey
- **Release 2:** Fill in the most important gaps
- **Release 3:** Polish, edge cases, power-user features

### Step 6: Flag dependencies
Note stories that must complete before others. Untracked dependencies cause sprint failures.

## Anti-Patterns

**1. Vertical slices by feature**
Bad: "Sprint 1: Build entire payment module."
Good: A thin horizontal slice that covers the full user journey, even if basic.

**2. Missing "so that" clause**
Bad: "As a user, I want to reset my password."
Good: "As a user, I want to reset my password so that I can regain access without contacting support."

**3. Technical stories disguised as user stories**
Bad: "As a developer, I want to refactor the auth module."
Good: Tech work belongs in tech debt tickets. If there's no user value, say so explicitly.

**4. No walking skeleton**
Bad: Writing 50 stories with no sense of minimum viable flow.
Good: Identify the walking skeleton first. Every story outside it is enhancement.

## Quality Checklist

- [ ] Backbone (user journey) mapped before writing individual stories
- [ ] Walking skeleton identified - thinnest slice that completes the flow
- [ ] Each story follows "As a [user], I want [goal], so that [benefit]"
- [ ] "So that" clause ties to real user value
- [ ] AC uses Given/When/Then with 3-7 criteria per story
- [ ] Stories sliced into releases (R1 = walking skeleton)
- [ ] Dependencies flagged
