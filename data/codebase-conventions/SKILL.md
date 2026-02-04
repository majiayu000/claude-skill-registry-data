---
name: codebase-conventions
description: >-
  Load when starting work in 10x-Mapmaster or when unsure about project standards.
  Covers file organization, naming conventions, type constraints, SQL style,
  and project-specific limits (200-char descriptions, answer enums). Use to
  understand how the codebase is structured and what standards to follow.
---

# Codebase Conventions

Project standards and constraints for 10x-Mapmaster.

> **Announce:** "I'm checking codebase-conventions to ensure I follow project standards."

## File Organization

```
src/                          # Vue 3 frontend (presentation only)
├── components/               # Reusable components
│   ├── game/                 # Game-specific components
│   ├── map/                  # MapLibre components
│   └── ui/                   # shadcn-vue components
├── composables/              # Shared reactive logic
│   ├── game/                 # Game-related composables
│   └── map/                  # Map-related composables
├── stores/                   # Pinia stores
├── views/                    # Page-level components
├── lib/                      # Utilities, API, types
│   ├── api/                  # RPC call wrappers
│   └── places/               # Place-related utilities
├── types/                    # TypeScript types
└── i18n/                     # Translations

supabase/
├── db/                       # Database source files
│   ├── schema/               # Tables, types, RLS policies
│   ├── game_logic/           # Internal functions (scoring, questions)
│   │   ├── functions/        # Function definitions
│   │   └── data/             # Seed data
│   └── public/               # Player-facing RPC entrypoints
│       └── functions/
├── functions/                # Deno edge functions
├── migrations/               # Generated (never edit directly)
├── seeds/                    # Development data
└── tests/                    # pgTAP tests

openspec/                     # Specifications
├── specs/                    # Capability specs
└── changes/                  # Active change proposals

docs/                         # Human-readable documentation
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files (frontend) | kebab-case | `game-session.ts`, `PlaceView.vue` |
| Vue components | PascalCase | `GameActive.vue`, `PlacesLayer.vue` |
| Composables | camelCase with `use` prefix | `useMapCamera`, `useGameMap` |
| Pinia stores | camelCase with `use...Store` | `useGameSessionStore` |
| SQL identifiers | snake_case | `game_sessions`, `user_id` |
| SQL keywords | UPPERCASE | `SELECT`, `FROM`, `WHERE` |
| Database functions | snake_case | `start_game`, `play_turn` |
| TypeScript types | PascalCase | `GameSession`, `Candidate` |

## Project-Specific Constraints

### Description Limit
Player descriptions are limited to **200 characters**:
```sql
-- Enforced by database constraint
CONSTRAINT check_description_length 
  CHECK (char_length(description) <= 200)
```

### Answer Enum
Valid answers are strictly typed:
```sql
CREATE TYPE answer_value AS ENUM('yes', 'no', 'not_sure');
```
- `yes` / `no` - For both questions AND guesses
- `not_sure` - ONLY for questions, never for guesses

### Game Session Status
```sql
CREATE TYPE game_session_status AS ENUM(
  'active',           -- Game in progress
  'won',              -- System guessed correctly
  'ended',            -- Max turns reached without win
  'needs_submission'  -- Awaiting player to submit correct place
);
```

## SQL Style

```sql
-- CORRECT style
SELECT 
  p.id,
  p.name,
  1 - (p.embedding <=> v_query) AS similarity
FROM places p
JOIN place_traits pt ON pt.place_id = p.id
WHERE p.status = 'active'
  AND similarity > 0.5
ORDER BY similarity DESC
LIMIT 10;

-- WRONG: lowercase keywords, SELECT *
select * from places where status = 'active'
```

**Rules:**
- UPPERCASE keywords: `SELECT`, `FROM`, `WHERE`, `JOIN`, `ORDER BY`
- lowercase identifiers: `places`, `user_id`, `created_at`
- Explicit column lists (no `SELECT *`)
- Aliases for complex expressions
- One clause per line for readability

## TypeScript Standards

- **Strict mode** enabled
- **No `any`** in application code
- **Explicit return types** on exported functions
- **Non-null assertions** only with prior type narrowing

```typescript
// CORRECT
export function useMapCamera(): UseMapCameraReturn {
  const center = ref<{ lng: number; lat: number }>({ lng: 0, lat: 20 })
  // ...
  return { center, flyTo, isAnimating }
}

// WRONG
export function useMapCamera() {  // Missing return type
  const center: any = ref({ lng: 0, lat: 20 })  // any usage
  // ...
}
```

## File Size Limit

**Max 200 lines per file.** If larger, split:
- Components → Extract child components
- Composables → Extract helper functions
- Stores → Extract into multiple stores

## Git Conventions

- **Branch naming:** `feat/`, `fix/`, `chore/`, `docs/`
- **Commit format:** Conventional commits
  ```
  feat: add candidate scoring function
  fix: prevent camera feedback loop
  chore: update dependencies
  docs: add algorithm documentation
  ```

## Development Workflow

### Database Changes
1. Edit source files in `supabase/db/`
2. Run `bun run db:rebuild` (generates migration + resets)
3. Test with `supabase test db`
4. Commit BOTH source AND migration

### Frontend Changes
1. Edit source files in `src/`
2. Run `bun run type-check`
3. Run `bun run test:unit`
4. Verify in browser

## References

See `references/glossary.md` for domain term definitions.
