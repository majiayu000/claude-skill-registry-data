---
name: wire
description: Find orphaned code (exports with no consumers, signals with no listeners, built features with no UI entry) and connect them. Use when user says /wire, "connect orphans", "what's disconnected", "wiring pass", or after a build wave leaves unconnected pieces.
---

# WIRE (Connect Orphaned Code)

## Purpose

After build waves produce isolated features, find what's built but disconnected and wire it into the live system.

## Procedure

### Phase 1: Discover Orphans

Run these scans (parallel agents recommended):

1. **Exported but never imported:**
   - Grep for `export function` / `export const` / `export default` in `lib/`
   - Cross-reference with import statements across codebase
   - Flag exports with zero consumers

2. **Actions with no UI trigger:**
   - Find server actions (`'use server'` files)
   - Check if each exported action is called from any component
   - Flag actions nobody invokes

3. **Components with no mount point:**
   - Find component files in `components/`
   - Check if they're imported anywhere in `app/`
   - Flag unmounted components

4. **Routes with no navigation:**
   - List all `page.tsx` files in `app/`
   - Check if any nav, link, or redirect points to each route
   - Flag unreachable pages

5. **Database tables with no query:**
   - List tables in schema
   - Check if `lib/` queries reference each table
   - Flag unqueried tables

### Phase 2: Prioritize

Score each orphan:

- **High:** Feature is referenced in build queue as PARTIAL/DONE but has no consumer
- **Medium:** Useful utility/component that would improve existing flows
- **Low:** Speculative/future code, unclear if needed yet

Present top 10 high-priority orphans.

### Phase 3: Wire

For each high-priority orphan, determine the correct connection:

- Action needs a button/form? Add it to the relevant page.
- Component needs mounting? Import it in the appropriate layout/page.
- Signal needs a listener? Wire it into the consumer that should react.
- Route needs nav entry? Add to appropriate navigation.

Build the connections. Each wire = one atomic commit.

### Phase 4: Verify

- `npx tsc --noEmit --skipLibCheck` passes
- Wired features are reachable in browser
- No circular dependencies introduced

## Constraints

- NEVER delete orphaned code (it may be WIP from another agent)
- Only wire things that have a clear, obvious consumer
- If unsure where something connects, skip it and report it
- Respect existing patterns (use the same nav system, same action patterns)

## Output

```
## Wiring Report [date]
| Orphan | Type | Connected To | Commit |
|--------|------|-------------|--------|
```
