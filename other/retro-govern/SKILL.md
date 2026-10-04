---
name: retro-govern
description: "Retrospective governance. Scopes, validates, assigns, and tracks retrospective findings. Manages the feedback loop — approved lessons flow into lessons-learned.md for reinforcement learning."
---

# Retrospective Governance

Scope, validate, assign, and track retrospective findings.
Manages the feedback loop that makes lessons actionable.

## When Invoked

By the game-retrospective agent after retro-analyze completes.
Requires retro-analyze output as input. This is always sequential
(never parallel with analyze).

## What You Produce

### 1. Applicability / Scope
Where this lesson applies, and where it does NOT:
- All games? Only canvas games? Only educational games?
- Which skills/agents does it affect?
- What conditions must be true for it to apply?
- Be EXPLICIT about boundaries to prevent over-generalizing

### 2. Confidence / Validation Status
One of:
- `proposed` — Untested hypothesis (default for new entries)
- `tested` — Applied once, showed positive signal
- `confirmed` — Multiple successful validations
- `obsolete` — No longer relevant

### 3. Owner
Who is responsible for maintaining or actioning the change:
- A skill name (e.g., "game-developer skill")
- An agent name (e.g., "game-tester agent")
- A role (e.g., "the developer")

### 4. Approval Status
One of:
- `draft` — Initial write-up (default for new entries)
- `approved` — Accepted into practice
- `rejected` — Not adopted (include reason)
- `superseded` — Replaced by newer learning

### 5. Review Date
When this entry should be revisited:
- Default: 30 days from creation
- High confidence: 90 days
- Low confidence: 14 days
- Always absolute dates (YYYY-MM-DD), never relative

### 6. Success Metric
How you will know the change actually helped:
- Must be measurable and observable
- Examples: "No timing bugs in 3 consecutive projects"
- Examples: "Completion rate for under-7s increases by >10%"

### 7. Lesson Destination
Is this lesson universal or game-specific?
- `plugin` — Universal game development wisdom that applies across ALL projects (e.g., "always debounce resize handlers in canvas games")
- `project` — Lesson specific to this game's context, mechanics, or constraints (e.g., "this game's drag-sort challenge needs 44px minimum tap targets for its age group")

## Process

1. Read retro-analyze output (REQUIRED)
2. Define scope boundaries explicitly
3. Set initial confidence to `proposed`
4. Assign ownership based on which skill/agent the change affects
5. Set approval to `draft` pending user review
6. Calculate review date (30 days default, adjusted by confidence)
7. Define a concrete, measurable success metric
8. Determine lesson destination: `plugin` (universal) or `project` (game-specific)

## Feedback Loop Action

When `approval status` is set to `approved`:
1. Extract the "Rule or pattern change" from retro-analyze
2. Format it as a lessons-learned.md entry (see `references/feedback-loop.md`)
3. Route by destination:
   - `destination: plugin` → Append to plugin-level `lessons-learned.md` (in the web-game-dev plugin directory)
   - `destination: project` → Append to project-level `lessons-learned.md` (in the project root)
4. This makes the lesson immediately available to all future agents
   via the Information Capture Protocol

## Output Format

```
=== GOVERNANCE REPORT ===

**Applicability / scope:** [explicit boundaries]
**Confidence:** proposed
**Owner:** [skill/agent/role]
**Approval status:** draft
**Review date:** [YYYY-MM-DD]
**Success metric:** [measurable outcome]
**Destination:** [plugin | project]

## Feedback Loop Status
[Whether this is ready for approval, or needs more testing]

=== END GOVERNANCE ===
```
