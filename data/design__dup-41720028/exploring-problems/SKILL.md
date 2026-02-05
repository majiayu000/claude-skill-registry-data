---
name: exploration
description: Technical exploration within existing projects. USE WHEN user says "think through", "explore options", "investigate", "how should we approach", or needs to evaluate approaches before implementation. Creates exploration documents in project's explorations/ folder. Not for new project ideas—use ideation skill for that.
---

# Exploration

Technical deep dives within existing projects. Think through problems, evaluate options, investigate approaches. Captures insights to explorations/ for future iterations.

## Available Environment Variables

These env vars are available in bash commands (use `${VAR}` syntax):

- `${PROJECT_NAME}` - Current project name
- `${PROJECT_ROOT}` - Current project code directory (e.g., `~/development/projects/argus`)
- `${WORKFLOW_PROJECTS}` - Obsidian projects root (e.g., `~/obsidian/projects`)

**Output location:**
- Explorations save to: `{WORKFLOW_PROJECTS}/{PROJECT_NAME}/explorations/`
- This is the Obsidian projects folder, not the code repo

## Mindset

**Explore WITH them** — not interviews, real collaborative thinking. Follow their energy, challenge assumptions, stay concrete.

**Read actual code** — Use Read and Grep to examine how things work. Evidence over speculation.

**Find hidden gems:**
- The constraint that isn't real
- The simple solution they dismissed
- The pattern from another domain

## Process

1. **Engage immediately** — No meta-commentary, just start thinking together
2. **Investigate real code** — Use Read/Grep, reference file:line locations, build on what exists
3. **Track patterns mentally** — Problems crystallizing, approaches forming, decisions being made
4. **Challenge constructively** — "What about edge case X?", "What happens at scale?"
5. **Build on energy** — Dig deeper into excitement, connect across domains

## Examples

**Example 1: Architecture decision**
```
User: "How should we structure the plugin system?"
→ Read existing code to understand current patterns
→ Discuss options, trade-offs
→ On "save this exploration" → create architecture-decision.md
```

**Example 2: Technical investigation**
```
User: "The auth flow feels slow, let's explore why"
→ Use Grep/Read to trace the flow
→ Identify bottlenecks together
→ On "document these insights" → create auth-performance.md
```

**Example 3: Options evaluation**
```
User: "Should we use SQLite or Postgres for this?"
→ Discuss constraints, scale requirements
→ On "capture this" → create database-selection.md
```

## When to Save

User signals with: "save this exploration", "capture this", "document these insights", "write this down"

**Do NOT ask if they want to save** — wait for the trigger.

## Saving Explorations

**Location:** `{WORKFLOW_PROJECTS}/{PROJECT_NAME}/explorations/{slug}.md`

**Slug:** Descriptive, lowercase-hyphen (`skills-vs-routing.md`), not timestamps (`exploration-20251017.md`)

**Template:** Reference `assets/EXPLORATION_TEMPLATE.md`, adapt as needed

**Required:** Title, date, context, key insights, decisions (if any)

**Critical:** Capture the JOURNEY, not just destination. Show how thinking evolved.

**Write concretely:**
- Good: "Discovered routing can't scale beyond 20 skills due to token costs"
- Bad: "We discussed various approaches"

**Include file references** if code was examined: `src/hooks/hook.ts:45`

## Resources

### assets/

Contains `EXPLORATION_TEMPLATE.md` - the template structure for saving explorations. Adapt sections as needed for each exploration.

### references/

Contains example explorations demonstrating different styles:

- `lore-mvp-event-system.md` - Clean architectural exploration
- `skills-vs-routing-architecture.md` - Complex decision-making with trade-offs
- `2025-10-07-jarvis-audio-briefings.md` - Feature design exploration

These examples show different approaches to capturing explorations. Use them for inspiration, not strict templates.
