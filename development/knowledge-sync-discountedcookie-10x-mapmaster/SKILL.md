---
name: knowledge-sync
description: >-
  Use after completing a refactor, implementing a major feature, or when skills
  may be outdated. Analyzes code changes, identifies affected skills, and proposes
  updates to keep team knowledge current. Also use when you notice a skill contains
  outdated patterns. Ask clarifying questions if changes are confusing.
---

# Knowledge Sync

Keep skills and documentation in sync with codebase changes.

> **Announce:** "I'm using knowledge-sync to update team knowledge after these changes."

## When to Use

- After completing an OpenSpec change (especially refactors)
- When you notice a skill references outdated code
- When a new pattern is established that should be documented
- When asked to run `/sync-knowledge`

## Process

### Phase 1: Identify What Changed

Check recent changes:
```bash
git log --oneline -20
git diff HEAD~10 --name-only
```

Categorize changes by domain:
- **Database**: `supabase/db/` changes
- **Frontend**: `src/` changes  
- **Edge Functions**: `supabase/functions/` changes
- **Config**: `opencode.jsonc`, AGENTS.md, skill changes

### Phase 2: Map Changes to Skills

Use the skill-pattern map to identify affected skills:

| Code Area | Affected Skills |
|-----------|-----------------|
| `supabase/db/game_logic/` | `database-first`, `game-scoring`, `postgres-vectors`, `postgis-spatial` |
| `src/composables/map/` | `maplibre-camera`, `maplibre-layers` |
| `src/composables/` | `vue-composables` |
| `src/stores/` | `vue-composables`, `database-first` |
| `supabase/functions/` | `edge-functions` |
| `src/components/ui/` | `shadcn-vue` |

### Phase 3: Analyze Impact

For each affected skill, check:

1. **Do code examples still work?** Read the actual code, compare to skill examples
2. **Are anti-patterns still relevant?** Maybe they're now the correct pattern
3. **Are new patterns worth documenting?** Repeated patterns should be captured
4. **Is the description still accurate?** Trigger words should match current functionality

### Phase 4: Ask Clarifying Questions

If something is confusing, ASK before assuming:

```
I noticed [observation]. Questions:

1. [Specific question about intent]
2. [Question about whether this is a new pattern]
3. [Question about whether old pattern should be deprecated]

Please clarify before I update the skills.
```

### Phase 5: Propose Updates

Present changes in structured format:

```markdown
## Skill Updates Required

### [skill-name]

**Reason:** [Why this needs updating]

**Current content (outdated):**
```
[snippet]
```

**Proposed content:**
```
[snippet]
```

---

Approve these changes?
```

### Phase 6: Apply Updates (with approval)

After approval:
1. Update the affected SKILL.md files
2. Update references/ if needed
3. Verify skill still loads correctly
4. Summarize what was changed

## What NOT to Update

- **Workflow skills** (openspec-*, executing-tasks, etc.) - These are process, not code
- **Glossary entries** - Unless domain terms changed meaning
- **External API references** - Unless we changed how we use them

## Creating New Skills

If a new pattern emerges that doesn't fit existing skills:

1. Identify the pattern clearly
2. Check if it should extend an existing skill or be new
3. If new, propose the skill structure:
   ```
   skill-name/
   ├── SKILL.md
   └── references/
       └── examples.md
   ```
4. Get approval before creating

## Red Flags

- **Don't update based on assumptions** - Read the actual code
- **Don't remove patterns without asking** - They may still be valid
- **Don't add every code change** - Only patterns worth repeating
- **Don't update skills during a refactor** - Wait until it's complete

## References

See `references/skill-pattern-map.md` for the full mapping.
