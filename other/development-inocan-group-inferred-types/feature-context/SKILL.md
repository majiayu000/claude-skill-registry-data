---
name: feature-context
description: Load feature requirements, design, and implementation plan when working on in-progress features. Use when user is implementing code, debugging, asking about requirements, or making changes related to a tracked feature. Silently loads context files to inform responses.
allowed-tools: Read, Glob
---

# Feature Context

Automatically load feature documentation when the user is working on an in-progress feature.

## When to Use

Invoke this skill when the user:
- Is implementing code for a feature
- Asks about requirements or acceptance criteria
- Asks about design decisions
- Debugs or troubleshoots feature-related code
- References work on "the current feature" or a specific feature name

## Instructions

### Step 1: Identify In-Progress Features

```
Read: docs/planning/backlog.json
```

Filter items where `status === "in-progress"`.

If multiple features are in-progress, determine which is relevant:
1. Check if user mentioned a specific feature name/ID
2. Look at recent file edits to infer which feature
3. If unclear, list in-progress features and ask which one

### Step 2: Load Feature Context

For the relevant feature, load these files (if they exist):

```
docs/planning/features/[feature-id]/
├── requirements.md    # Acceptance criteria, user stories
├── design.md          # Architecture, component design
└── plan.md            # Implementation steps, progress log
```

Read each file silently to build context.

### Step 3: Extract Key Information

From **requirements.md**:
- User stories and acceptance criteria
- Technical requirements
- Dependencies and prerequisites

From **design.md** (if exists):
- Architecture decisions
- Component relationships
- API contracts

From **plan.md**:
- Implementation steps (which are done/pending)
- Testing strategy
- Known risks and unknowns
- Progress log entries

### Step 4: Use Context in Responses

When responding to the user:
- Reference requirements when discussing what to build
- Reference design when discussing how to build
- Reference plan when discussing what's next
- Note progress log entries for recent decisions

**Do NOT dump the entire context.** Reference it naturally:
```
According to the requirements, this feature needs to [specific requirement].
The design specifies [relevant design decision].
Looking at your plan, the next step is [uncompleted step].
```

## Output Format

Context should inform your responses, not dominate them.

When explicitly asked about the feature:
```
## Current Feature: [name]

**Status**: In Progress (started [date])
**Progress**: [X/Y] implementation steps complete

### Key Requirements
- [Most relevant acceptance criteria]

### Current Focus
- [Current/next implementation step from plan]

### Recent Progress
- [Latest progress log entries]
```

## Integration Notes

This skill works with:
- `progress-tracker` skill - Updates the plan.md this skill reads
- `scope-guard` skill - Uses requirements.md to check scope
- `/feature-ship` - Uses these files for completion review
