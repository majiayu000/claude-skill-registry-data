---
name: brainstorm-sync
description: Sync brainstorming session discoveries to project memory (CONTEXT.md, memories)
---

# Brainstorm Sync

After a brainstorming session, capture valuable discoveries in project memory so future sessions benefit.

## When to Use

- After completing a brainstorming session (feature-tree:brainstorm skill)
- When significant design decisions were made
- When user intentions or project context became clearer

## What to Sync

### 1. CONTEXT.md Updates

Brainstorming often reveals or clarifies:

| Section | What might have changed |
|---------|------------------------|
| Problem | Refined understanding of the pain point |
| Target Users | More specific user personas discovered |
| Success Criteria | Clearer metrics identified |
| Constraints | New constraints or removed assumptions |
| Key Assumptions | New assumptions marked [untested] |

**Process:**
1. Read current `.feat-tree/CONTEXT.md`
2. Ask: "Did this session reveal anything new about the problem, users, or constraints?"
3. Update relevant sections (preserve existing content, add new insights)

### 2. Memory Updates

Create or update memories based on brainstorming discoveries:

| Discovery Type | Memory File |
|----------------|-------------|
| Technical decisions | `technical_decisions.md` |
| Scope fences (explicit "nots") | `scope.md` |
| User insights (Day-In-Life) | `users.md` |
| Core assumptions (Crux) | Update CONTEXT.md assumptions |
| Pre-mortem risks | `risks.md` |

### 3. Design Reference

If a design doc was created:

```markdown
# memories/designs.md

## Recent Designs

- 2026-01-03: Bootstrap Redesign (docs/plans/2026-01-03-bootstrap-phase1-design.md)
  - Two-phase feature discovery
  - Confidence levels on all output
```

## Process

### Step 1: Review Session

Ask yourself:
- What did we learn about the user/problem?
- What technical decisions were made and why?
- What scope fences were established?
- What assumptions were identified?

### Step 2: Update CONTEXT.md

Read, identify changes, update:

```bash
# Read current context
cat .feat-tree/CONTEXT.md
```

Update sections that changed. Don't rewrite what's already accurate.

### Step 3: Update/Create Memories

For each significant discovery:
1. Check if a relevant memory file exists
2. Update existing or create new
3. Keep it dense — same info, fewer tokens

### Step 4: Confirm

```
Synced to project memory:
- CONTEXT.md: [what changed]
- memories/technical_decisions.md: [created/updated]
- memories/scope.md: [created/updated]

Future sessions will have this context.
```

## Guidelines

- **READ before WRITE** — Don't duplicate existing content
- **Dense > verbose** — Same information, fewer tokens
- **Only sync reusable insights** — Skip session-specific details
- **Preserve existing content** — Add to, don't replace
