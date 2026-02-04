---
name: database-first
description: >-
  REQUIRED before implementing any game feature, scoring logic, state transition,
  or decision-making. ALL business logic lives in PostgreSQL - frontend is
  presentation only. Load this to understand where code belongs: database
  function vs component. Covers RPC patterns, SECURITY DEFINER, and anti-patterns.
---

# Database-First Architecture

The Iron Law of this project: **ALL business logic lives in PostgreSQL.**

> **Announce:** "I'm using database-first to ensure this logic goes in the right place."

## The Rule

```
FRONTEND (src/)         → Presentation + User Input ONLY
DATABASE (supabase/db/) → Game Logic + State + Decisions
EDGE FUNCTIONS          → LLM/Embedding Integration ONLY
```

## Where Does This Code Go?

| Feature | Database | Frontend |
|---------|----------|----------|
| Calculate confidence score | `game_logic.calculate_confidence()` | NEVER |
| Determine next question | `game_logic.get_next_turn()` | NEVER |
| Filter candidates | `game_logic.filter_*_candidates()` | NEVER |
| Check win condition | `game_logic.check_guess_decision()` | NEVER |
| Validate game state | DB constraints + RLS | NEVER |
| Render question UI | NEVER | Vue component |
| Display map markers | NEVER | MapLibre layer |
| Fetch game state | RPC returns it | Store calls RPC |
| Handle user input | NEVER | Vue event handler |

## Anti-Pattern: Logic in Frontend

```typescript
// WRONG: Scoring logic in Vue component
const confidence = computed(() => {
  const probabilities = candidates.value.map(c => c.score)
  const maxProb = Math.max(...probabilities)
  const margin = maxProb - (probabilities[1] || 0)
  // THIS IS GAME LOGIC - SHOULD BE IN DATABASE
  return { maxProb, margin }
})
```

**Why it's wrong:**
- Different clients would calculate differently
- Can't use for learning/training data
- No single source of truth
- Violates architecture

```sql
-- CORRECT: Scoring in database function
CREATE FUNCTION game_logic.calculate_confidence(p_candidates jsonb)
RETURNS jsonb AS $$
  -- Calculate max_prob, margin, entropy HERE
  -- Return as structured JSON
$$ LANGUAGE plpgsql;
```

## RPC Call Pattern

Frontend ONLY calls RPCs and reads views:

```typescript
// src/lib/api/index.ts
export const gameApi = {
  async startGame(description: string): Promise<string> {
    const { data, error } = await supabase.rpc('start_game', {
      p_description: description,
      p_language_code: 'en'
    })
    if (error) throw error
    return data  // Just the session_id
  },
  
  async playTurn(sessionId: string, answer: Answer): Promise<void> {
    const { error } = await supabase.rpc('play_turn', {
      p_session_id: sessionId,
      p_answer: answer
    })
    if (error) throw error
  }
}
```

Game state comes from database views, NOT computed in frontend:
```typescript
// Read state from view (computed by database)
const { data } = await supabase
  .from('game_session_state')  // VIEW, not table
  .select('*')
  .eq('id', sessionId)
  .single()

// data.next_turn contains: question, candidates, confidence
// ALL computed by database, frontend just displays it
```

## SECURITY DEFINER Pattern

Public-facing functions use SECURITY DEFINER to access `game_logic` schema:

```sql
-- supabase/db/public/functions/start_game.sql
CREATE FUNCTION public.start_game(p_description text, p_language_code text)
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, game_logic, extensions
AS $$
DECLARE
  v_user_id uuid;
BEGIN
  -- Always validate auth
  v_user_id := auth.uid();
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'Authentication required';
  END IF;
  
  -- Rate limiting
  PERFORM check_rate_limit('start_game');
  
  -- Internal logic in game_logic schema
  RETURN game_logic.create_game_session(v_user_id, p_description, p_language_code);
END;
$$;
```

**Key points:**
- `SECURITY DEFINER` = runs with function owner's privileges
- Always validate `auth.uid()` first
- Set `search_path` explicitly
- Public function is thin wrapper around game_logic function

## Red Flags - STOP

If you're about to write in `src/`:
- Sorting or filtering candidates → STOP, use database
- Calculating scores or probabilities → STOP, use database
- Determining game state transitions → STOP, use database
- Validating user actions → STOP, use database (+ RLS)

If you see these in frontend code, FLAG IT for migration to database.

## References

See `references/rpc-patterns.md` for more examples.
