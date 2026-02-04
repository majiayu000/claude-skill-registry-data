---
name: convex-game-management
description: Manage game lifecycle, player turns, round rotation, scoring, and game state transitions. Use when implementing game creation, turn management, score updates, and game completion flows in PictionAI.
compatibility: Requires Convex backend with mutations and queries, React hooks (useQuery, useMutation)
metadata:
  author: PictionAI
  category: backend
  frameworks: Convex, Next.js
---

# Convex Game Management

## Overview

This skill handles the complete game lifecycle for PictionAI's multiplayer Pictionary game, including game creation, player management, turn-based rotation, atomic turn completion with scoring, and game state transitions.

## Core Concepts

### Game States

- **waiting** - Game created, players joining in lobby
- **started** - Game in progress, turns rotating
- **finished** - All rounds complete, winner determined

### Turn States

- **drawing** - Active turn, timer running (60-120 seconds)
- **completed** - Turn finished with correct guess
- **time_up** - Timer expired, no points awarded

### Atomic Turn System

Turns are completed atomically to ensure data consistency:

1. **Start Turn**: Drawer calls `startNewTurn` mutation
2. **Draw & Guess Phase**: Real-time canvas sync, players submit guesses
3. **Turn Completion**: Three atomic scenarios:
   - ✅ Correct guess → Both guesser and drawer earn points
   - 🏆 Manual winner selection → Drawer selects winner from guessers
   - ⏱️ Time up → No points, proceed to next turn
4. **Score Updates**: Dual scoring system (guesser time bonus + drawer base score)
5. **Next Turn**: Auto round-robin rotation to next player

## Scoring System

### Guess Scoring (Correct Answer)

- **Guesser**: Base 50 points + time bonus (50 - elapsed_seconds, min 5 points)
- **Drawer**: 25% of guesser's score, minimum 10 points

### Drawer Scoring (Manual Winner)

- **Selected Guesser**: 30 points
- **Drawer**: 25 points

## Key Mutations

### startNewTurn

Start a new drawing turn, assign card, initialize timer.

```typescript
mutation startNewTurn {
  args: {
    game_id: Id<"games">
  }
  // Returns: {
  //   turn_id: Id<"turns">,
  //   card: { word: string, category: string },
  //   drawer_id: Id<"users">,
  //   time_limit: number
  // }
}
```

### submitGuessAndCompleteTurn

Submit a guess and complete the turn with atomic scoring.

```typescript
mutation submitGuessAndCompleteTurn {
  args: {
    game_id: Id<"games">,
    turn_id: Id<"turns">,
    guesser_id: Id<"users">,
    guess: string,
    elapsed_time: number,
    is_correct?: boolean
  }
  // Handles three scenarios atomically:
  // 1. Correct guess → Award points to both
  // 2. Manual selection → Drawer chooses winner
  // 3. Time up → Skip to next turn
}
```

### selectWinner (Manual Selection)

Drawer selects a guesser as the winner when time expires.

```typescript
mutation selectWinner {
  args: {
    turn_id: Id<"turns">,
    selected_guesser_id: Id<"users">
  }
  // Awards 30 points to guesser, 25 to drawer
}
```

## Key Queries

### getGame

Fetch complete game state with players, current turn, scores.

```typescript
query getGame {
  args: { game_id: Id<"games"> }
  // Returns full game with nested players, turns, scores
}
```

### getGameTurns

Get all turns in a game with guesses and results.

```typescript
query getGameTurns {
  args: { game_id: Id<"games"> }
  // Returns array of turns with scoring details
}
```

## React Integration

```typescript
// Start a new turn
const startTurn = useMutation(api.mutations.game.startNewTurn);
await startTurn({ game_id: gameId });

// Submit guess and complete turn
const submitGuess = useMutation(api.mutations.game.submitGuessAndCompleteTurn);
await submitGuess({
  game_id: gameId,
  turn_id: turnId,
  guesser_id: userId,
  guess: "elephant",
  elapsed_time: 45,
});

// Fetch game state
const game = useQuery(api.queries.games.getGame, { game_id: gameId });
```

## Database Schema References

```typescript
// Games table
games: defineTable({
  code: v.string(), // Unique game code
  creator_id: v.id("users"),
  players: v.array(
    v.object({
      user_id: v.id("users"),
      score: v.number(),
      is_drawer: v.boolean(),
    })
  ),
  state: v.union(
    v.literal("waiting"),
    v.literal("started"),
    v.literal("finished")
  ),
  current_turn_index: v.number(),
  created_at: v.optional(v.number()),
  round_count: v.number(),
});

// Turns table
turns: defineTable({
  game_id: v.id("games"),
  drawer_id: v.id("users"),
  card_id: v.id("cards"),
  state: v.union(
    v.literal("drawing"),
    v.literal("completed"),
    v.literal("time_up")
  ),
  timer_started_at: v.number(),
  time_limit: v.number(),
  correct_guesser_id: v.optional(v.id("users")),
  guesses: v.array(
    v.object({
      guesser_id: v.id("users"),
      guess: v.string(),
      timestamp: v.number(),
      is_correct: v.optional(v.boolean()),
    })
  ),
});
```

## Common Patterns

### Monitor active turn

```typescript
const game = useQuery(api.queries.games.getGame, { game_id });
const currentTurn = game?.turns[game.current_turn_index];
const isMyTurn = currentTurn?.drawer_id === userId;
```

### Handle turn completion

```typescript
// When drawer completes turn with guess result
const completeWithCorrect = useMutation(
  api.mutations.game.submitGuessAndCompleteTurn
);
await completeWithCorrect({
  game_id: gameId,
  turn_id: turnId,
  guesser_id: guesserId,
  guess: "elephant",
  elapsed_time: 30,
  is_correct: true,
});
```

### Automatic next turn

The mutation automatically:

1. Rotates drawer (round-robin through players)
2. Assigns new card
3. Starts timer
4. Updates game state

## Edge Cases

- **Multiple guesses per player**: Allowed, only latest is scored
- **Guess submitted after timer**: System checks elapsed time on server
- **Late guess arrival**: Real-time subscription updates guess feed
- **Manual selection ambiguity**: Drawer must explicitly select one winner
- **Game with 2 players**: Drawer rotation still works with round-robin

## See Also

- [TURN_MANAGEMENT_ANALYSIS.md](../../TURN_MANAGEMENT_ANALYSIS.md) - Detailed atomic turn analysis
- `convex/mutations/game.ts` - Complete mutation implementations
- `components/game/game-board.tsx` - UI integration
