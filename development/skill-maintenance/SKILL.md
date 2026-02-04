---
name: skill-maintenance
description: Guidelines for when and how to update Claude Code skills after codebase changes. Use after completing significant features, architectural changes, or discovering new patterns/anti-patterns. NOT for every commit - only meaningful changes that affect how agents should work.
---

# Skill Maintenance Guide

This skill helps development agents know when and how to update the ChainGraph skill tree after making codebase changes.

## Core Principle: Balanced Updates

Skills should stay current but not churn constantly. Update skills for **meaningful changes** that affect how future agents should work.

```
                    ┌─────────────────────────────────────┐
                    │         SKILL UPDATE DECISION       │
                    └─────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
            ┌──────────────┐                 ┌──────────────┐
            │   UPDATE     │                 │  DON'T UPDATE │
            └──────────────┘                 └──────────────┘
            • New architecture               • Bug fixes
            • New patterns                   • Small features
            • New anti-patterns              • Refactoring
            • API changes                    • Test changes
            • Critical constraints           • Documentation
```

## When to UPDATE Skills

### Architectural Changes
- New store domain added
- New component pattern established
- New file organization structure
- New package added to monorepo

### Pattern Discovery
- Found a better way to do something common
- Discovered a pattern that should be standard
- Created a reusable hook/utility worth documenting

### Anti-Pattern Discovery
- Found code that causes bugs/issues
- Discovered performance problems from certain patterns
- Identified security concerns

### API/Interface Changes
- tRPC procedure signature changed
- Store API changed (new events, effects)
- Decorator API changed
- DBOS workflow patterns changed

### Critical Constraints
- New rule that MUST be followed
- Breaking change that affects existing code
- Deprecation of old patterns

## When NOT to Update Skills

### Routine Development
- Bug fixes (unless revealing anti-pattern)
- Small feature additions
- Refactoring that doesn't change patterns
- Test additions/modifications

### Documentation Changes
- README updates
- Code comments
- JSDoc additions

### Cosmetic Changes
- Renaming (unless widespread)
- Code formatting
- Import reorganization

### Work in Progress
- Experimental features
- Incomplete implementations
- Features behind feature flags

## How to Update Skills

### Step 1: Identify Affected Skills

Ask: "Which skills would an agent need to know about this change?"

| Change Type | Likely Affected Skills |
|-------------|----------------------|
| New Effector pattern | `effector-patterns` |
| Frontend architecture | `frontend-architecture` |
| New port type | `port-system`, `types-architecture` |
| DBOS workflow change | `dbos-patterns`, `executor-architecture` |
| Subscription change | `subscription-sync` |
| New node pattern | `node-creation`, `types-architecture` |

### Step 2: Determine Update Type

**Add Pattern**: New recommended way to do something
```markdown
## Patterns

### New: Using usePortValue hook
Prefer `usePortValue(portKey)` over direct store subscription...
```

**Add Anti-Pattern**: New thing to avoid
```markdown
## Anti-Patterns

### Avoid: Direct $portValues subscription in components
❌ Bad: `useUnit($portValues)` - causes re-render on ANY port change
✅ Good: `usePortValue(portKey)` - subscribes to single port
```

**Update Example**: Code example is outdated
```markdown
// Updated: Now uses ports-v2 API
const value = usePortValue(portKey)
```

**Update File Reference**: File moved or renamed
```markdown
| `src/store/ports-v2/stores.ts` | Port value stores (was ports/stores.ts) |
```

**Deprecate Pattern**: Old way is no longer recommended
```markdown
### Deprecated: Legacy port stores
The `ports/` store is deprecated. Use `ports-v2/` instead.
Migration guide: [link to migration docs]
```

### Step 3: Make Minimal Changes

- Add new information, don't rewrite everything
- Keep existing structure
- Add date/context in comments if helpful:
  ```markdown
  ### Using CommandController (added after dd543528)
  ```

### Step 4: Verify Consistency

- Does this change conflict with other skills?
- Should other skills reference this new pattern?
- Is the skill still under 500 lines?

## Skill Update Checklist

After significant development work, ask:

- [ ] Did I introduce a new **pattern** that should be documented?
- [ ] Did I discover an **anti-pattern** that others should avoid?
- [ ] Did I change **architecture** that affects how agents work?
- [ ] Did I add **new files/folders** that should be in Key Files?
- [ ] Did I create **new constraints** that MUST be followed?
- [ ] Did I **deprecate** something that skills still recommend?

If any are YES, update the relevant skill(s).

## Update Frequency Guidelines

| Skill Type | Update Frequency |
|------------|-----------------|
| Foundation (`chaingraph-concepts`) | Rarely - core concepts stable |
| Package (`*-architecture`) | Monthly - as architecture evolves |
| Technology (`*-patterns`) | When patterns discovered/deprecated |
| Feature (`port-system`, etc.) | When feature area changes significantly |
| Meta (`skill-*`) | When skill conventions change |

## Example: When to Update

### Scenario: Added new echo detection mechanism

**Changes made:**
- Added `echo-detection.ts` in `ports-v2/`
- New 3-step detection: mutation match → staleness → duplicate
- Added `$pendingPortMutations` store

**Skills to update:**

1. **`optimistic-updates`** (Primary)
   - Add section on 3-step echo detection
   - Document `$pendingPortMutations` store
   - Add anti-pattern: forgetting to track mutations

2. **`frontend-architecture`** (Reference)
   - Add `echo-detection.ts` to Key Files
   - Mention echo detection in ports-v2 section

3. **`effector-patterns`** (Optional)
   - If the pattern is reusable beyond ports

### Scenario: Fixed a bug in array port rendering

**Changes made:**
- Fixed race condition in `ArrayPort.tsx`
- Added null check

**Skills to update:** NONE
- This is a bug fix, not a pattern change
- Unless: the bug revealed an anti-pattern worth documenting

### Scenario: Refactored store structure

**Changes made:**
- Renamed `ports/` → `ports-v2/`
- Migration mode: disabled → dual-write → read-only → full
- All new code should use ports-v2

**Skills to update:**

1. **`frontend-architecture`**
   - Update folder structure
   - Document migration modes
   - Add deprecation notice for old `ports/`

2. **`effector-patterns`**
   - Document migration pattern if reusable

3. **`port-system`**
   - Update all references to use ports-v2
   - Add migration guide section

## Commit Message Convention

When updating skills, use clear commit messages:

```
docs(skills): update effector-patterns with new sample() usage

- Added pattern for combining multiple sources
- Documented anti-pattern for nested samples
- Updated Key Files with new store locations
```

## Skill Health Metrics

Periodically review skills for staleness:

| Metric | Healthy | Needs Review |
|--------|---------|--------------|
| Last updated | < 3 months | > 6 months |
| Key Files exist | All exist | Files missing |
| Patterns work | Code compiles | Outdated syntax |
| Anti-patterns relevant | Still problematic | Fixed in codebase |

## Related Skills

- `skill-authoring` - For creating new skills
- See package-specific skills for what to update in each area
