---
name: onboard-context-provider
description: Provides personalized assistance based on engineer's onboarding profile. Activates when engineer asks "how do I", "where should I", "what's the pattern for", shows confusion about conventions, or writes code that doesn't match project patterns. Reads .claude/onboard-profile.local.md for context.
---

# Onboard Context Provider

Provides personalized explanations and assistance based on the engineer's background from their onboarding profile.

## Activation Triggers

This skill activates when:
- Engineer asks "how do I..." or "where do I put..." questions
- Engineer asks about project conventions or patterns
- Code written doesn't match project conventions (imports, naming, structure)
- Engineer seems confused about a technology in their knowledge gaps list

## Profile Location

```
.claude/onboard-profile.local.md
```

If this file doesn't exist, this skill does nothing. The engineer needs to run `/onboard` first.

## Behavior

### 1. Read Engineer Profile

Check `.claude/onboard-profile.local.md` for:
- **Primary Stack**: What they know well
- **New To**: What's unfamiliar
- **Knowledge Gaps**: Specific gaps with priority levels
- **Current Task**: What they're working on

### 2. Personalize Response

Based on the profile, adjust explanations:

**If the concept is in their knowledge gaps (NEW):**
- Explain using analogies to their primary stack
- Show a side-by-side comparison with what they know
- Point to an example file in the codebase

**If the concept is related to something they know (TRANSFERABLE):**
- Briefly note the difference, skip the basics
- Focus on what's different, not what's the same

**If they already know it (FAMILIAR):**
- Don't explain the concept at all
- Just show the project-specific convention

### 3. Always Include

- Specific file paths from this project as examples
- The project convention (from CLAUDE.md) for whatever they're doing
- A concrete next action they can take

## Personalization Strategies

### Backend Engineer → Frontend Project

| Concept | Explain As |
|---------|-----------|
| Components | "Like views that return HTML directly" |
| State (useState) | "Like a variable that re-renders the page when changed" |
| Props | "Like function arguments for components" |
| useEffect | "Like Django signals — side effects triggered by changes" |
| Client vs Server Components | "Server = Django view, Client = JavaScript in template" |

### Frontend Engineer → Backend Project

| Concept | Explain As |
|---------|-----------|
| ORM Models | "Like TypeScript interfaces that map to database tables" |
| Migrations | "Like schema changes — versioned database updates" |
| Serializers | "Like Zod schemas for API input/output validation" |
| Views/Controllers | "Like API route handlers" |
| Middleware | "Same concept — runs before your handler" |

### Senior → New Framework

- Skip conceptual explanations entirely
- Focus on: syntax, file locations, project conventions
- Example: "API routes at `app/api/*/route.ts`, export GET/POST/etc."

### Junior → Any Framework

- Include "why" not just "how"
- Provide more context about patterns
- Suggest reading material when appropriate

## What NOT to Do

- Don't activate if no profile exists (engineer hasn't onboarded)
- Don't over-explain things the engineer already knows
- Don't provide generic advice — always reference this specific project
- Don't interrupt the engineer's flow with unsolicited lectures
