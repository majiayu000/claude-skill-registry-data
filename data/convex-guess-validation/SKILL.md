---
name: convex-guess-validation
description: Validate and score player guesses against drawing cards with fuzzy matching and scoring logic. Use when implementing guess submission, determining correctness, calculating bonus points, and handling scoring edge cases.
compatibility: Requires Convex mutations, string matching algorithms, scoring calculations
metadata:
  author: PictionAI
  category: backend
  frameworks: Convex, Next.js
---

# Convex Guess Validation

## Overview

This skill handles guess validation and scoring for PictionAI, including exact/fuzzy matching against card words, time-based bonus calculation, and atomic score updates for both guesser and drawer.

## Guess Validation Logic

### Validation Steps

1. **Exact Match**: Check if guess exactly matches card word (case-insensitive)
2. **Fuzzy Match**: If no exact match, apply fuzzy matching algorithm (Levenshtein distance)
3. **Partial Match**: Allow word containment (e.g., "gray elephant" matches "elephant")
4. **Synonym Recognition** (Optional): Check against known synonyms

### String Matching Algorithms

#### Exact Match

```typescript
function isExactMatch(guess: string, cardWord: string): boolean {
  return guess.toLowerCase().trim() === cardWord.toLowerCase().trim();
}
```

#### Fuzzy Match (Levenshtein Distance)

```typescript
function levenshteinDistance(str1: string, str2: string): number {
  const len1 = str1.length;
  const len2 = str2.length;
  const matrix: number[][] = [];

  for (let i = 0; i <= len2; i++) {
    matrix[i] = [i];
  }
  for (let j = 0; j <= len1; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= len2; i++) {
    for (let j = 1; j <= len1; j++) {
      const cost = str1[j - 1] === str2[i - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i][j - 1] + 1, // Insertion
        matrix[i - 1][j] + 1, // Deletion
        matrix[i - 1][j - 1] + cost // Substitution
      );
    }
  }

  return matrix[len2][len1];
}

function isFuzzyMatch(guess: string, cardWord: string): boolean {
  const maxDistance = Math.ceil(cardWord.length * 0.3); // 30% tolerance
  const distance = levenshteinDistance(
    guess.toLowerCase().trim(),
    cardWord.toLowerCase().trim()
  );
  return distance <= maxDistance;
}
```

#### Partial Match (Word Containment)

```typescript
function isPartialMatch(guess: string, cardWord: string): boolean {
  const words = guess.toLowerCase().split(/\s+/);
  return words.some(
    (word) => cardWord.toLowerCase().includes(word) && word.length > 2
  );
}
```

## Guess Data Structure

```typescript
interface Guess {
  guesser_id: Id<"users">;
  guess: string; // Raw user input
  timestamp: number; // When submitted (server time)
  is_correct: boolean; // Validation result
  match_type: "exact" | "fuzzy" | "partial" | "none";
  points_awarded?: number; // Scorer earns
  drawer_points?: number; // Drawer earns
}
```

## Scoring System

### Guesser Points (When Correct)

```typescript
function calculateGuesserScore(
  elapsedSeconds: number,
  timeLimit: number
): number {
  // Base score: 50 points
  // Time bonus: 50 - elapsed_seconds (minimum 5 points)

  const timeBonus = Math.max(5, timeLimit - elapsedSeconds);
  const baseScore = 50;
  const totalScore = baseScore + timeBonus;

  return Math.round(totalScore);
}

// Examples:
// Guess in 10 seconds (120s limit): 50 + (120 - 10) = 160 points
// Guess in 100 seconds: 50 + (120 - 100) = 70 points
// Guess in 119 seconds: 50 + (120 - 119) = 51 points
```

### Drawer Points (When Guesser Correct)

```typescript
function calculateDrawerScore(guesserScore: number): number {
  // Drawer gets 25% of guesser's score, minimum 10 points
  const percentage = Math.floor(guesserScore * 0.25);
  return Math.max(10, percentage);
}

// Examples:
// Guesser: 160 points → Drawer: max(40, 10) = 40 points
// Guesser: 55 points → Drawer: max(13, 10) = 13 points
```

### Manual Winner Selection (Time Expired)

```typescript
// When drawer selects a guesser as winner after time expires
const guesserScore = 30; // Fixed
const drawerScore = 25; // Fixed
```

## Mutation: validateGuess

Validate a guess submission and update scores.

```typescript
export const validateGuess = mutation({
  args: {
    game_id: v.id("games"),
    turn_id: v.id("turns"),
    guesser_id: v.id("users"),
    guess: v.string(),
    elapsed_time: v.number(),
    card_word: v.string(),
  },
  handler: async (ctx, args) => {
    // 1. Check match type
    let isCorrect = false;
    let matchType: "exact" | "fuzzy" | "partial" | "none" = "none";

    if (isExactMatch(args.guess, args.card_word)) {
      isCorrect = true;
      matchType = "exact";
    } else if (isFuzzyMatch(args.guess, args.card_word)) {
      isCorrect = true;
      matchType = "fuzzy";
    } else if (isPartialMatch(args.guess, args.card_word)) {
      isCorrect = true;
      matchType = "partial";
    }

    // 2. Calculate scores
    const guesserPoints = isCorrect
      ? calculateGuesserScore(args.elapsed_time, 120)
      : 0;
    const drawerPoints = isCorrect ? calculateDrawerScore(guesserPoints) : 0;

    // 3. Store guess in database
    const turn = await ctx.db.get(args.turn_id);
    const guesses = turn?.guesses || [];

    guesses.push({
      guesser_id: args.guesser_id,
      guess: args.guess,
      timestamp: Date.now(),
      is_correct: isCorrect,
      match_type: matchType,
      points_awarded: guesserPoints,
    });

    // 4. Update turn with guess
    await ctx.db.patch(args.turn_id, { guesses });

    return {
      is_correct: isCorrect,
      match_type: matchType,
      guesser_points: guesserPoints,
      drawer_points: drawerPoints,
    };
  },
});
```

## Complete Turn Submission Flow

```typescript
export const submitGuessAndCompleteTurn = mutation({
  args: {
    game_id: v.id("games"),
    turn_id: v.id("turns"),
    guesser_id: v.id("users"),
    guess: v.string(),
    elapsed_time: v.number(),
  },
  handler: async (ctx, args) => {
    const turn = await ctx.db.get(args.turn_id);
    const card = await ctx.db.get(turn.card_id);
    const game = await ctx.db.get(args.game_id);

    // 1. Validate guess
    let isCorrect = false;
    let guesserPoints = 0;
    let drawerPoints = 0;

    if (
      isExactMatch(args.guess, card.word) ||
      isFuzzyMatch(args.guess, card.word)
    ) {
      isCorrect = true;
      guesserPoints = calculateGuesserScore(args.elapsed_time, 120);
      drawerPoints = calculateDrawerScore(guesserPoints);
    }

    // 2. Update scores atomically
    if (isCorrect) {
      // Update guesser
      await ctx.db.patch(args.guesser_id, {
        total_score: guesser.total_score + guesserPoints,
      });

      // Update drawer
      const drawer = await ctx.db.get(turn.drawer_id);
      await ctx.db.patch(turn.drawer_id, {
        total_score: drawer.total_score + drawerPoints,
      });

      // Mark turn as completed
      await ctx.db.patch(args.turn_id, {
        state: "completed",
        correct_guesser_id: args.guesser_id,
      });
    }

    return {
      is_correct: isCorrect,
      guesser_points: guesserPoints,
      drawer_points: drawerPoints,
    };
  },
});
```

## React Integration

```typescript
const submitGuess = useMutation(api.mutations.game.submitGuessAndCompleteTurn);

async function handleGuessSubmit(guess: string, elapsedTime: number) {
  const result = await submitGuess({
    game_id: gameId,
    turn_id: turnId,
    guesser_id: userId,
    guess,
    elapsed_time: elapsedTime,
  });

  if (result.is_correct) {
    showMessage(`🎉 Correct! +${result.guesser_points} points`);
  } else {
    showMessage(`❌ Incorrect. Try again!`);
  }
}
```

## Edge Cases & Handling

### Multiple Guesses Per Player

```typescript
// Only count once per player per turn
const existingGuess = guesses.find((g) => g.guesser_id === args.guesser_id);
if (existingGuess) {
  // Either: reject, or replace with new guess
  if (existingGuess.is_correct) {
    return { error: "Already guessed correctly" };
  }
  // Replace with new guess attempt
  guesses = guesses.filter((g) => g.guesser_id !== args.guesser_id);
}
```

### Guess After Timer Expires

```typescript
// Server validates elapsed_time on submission
if (args.elapsed_time > timeLimit) {
  return { error: "Guess submitted after timer expired" };
}
```

### Case & Whitespace Handling

```typescript
// Normalize before comparison
const normalized = guess.toLowerCase().trim();
// Remove extra spaces
const cleaned = normalized.replace(/\s+/g, " ");
```

### Special Characters

```typescript
// Option 1: Strict (require exact special chars)
// Option 2: Lenient (strip special chars before matching)
const stripped = guess.replace(/[^a-z0-9\s]/gi, "");
```

## Configuration Parameters

```typescript
const MATCHING_CONFIG = {
  EXACT_MATCH_ENABLED: true,
  FUZZY_MATCH_ENABLED: true,
  FUZZY_TOLERANCE: 0.3, // 30% character mismatch allowed
  PARTIAL_MATCH_ENABLED: true,
  MIN_PARTIAL_WORD_LENGTH: 3, // Words must be 3+ chars
  BASE_GUESSER_SCORE: 50,
  MIN_TIME_BONUS: 5,
  DRAWER_PERCENTAGE: 0.25,
  MIN_DRAWER_SCORE: 10,
  MANUAL_WINNER_GUESSER_SCORE: 30,
  MANUAL_WINNER_DRAWER_SCORE: 25,
};
```

## Testing Scenarios

```typescript
// Test cases for fuzzy matching
const tests = [
  // Exact
  { guess: "elephant", word: "elephant", expected: true, type: "exact" },
  { guess: "ELEPHANT", word: "elephant", expected: true, type: "exact" },

  // Fuzzy (typos)
  { guess: "elefant", word: "elephant", expected: true, type: "fuzzy" },
  { guess: "elepant", word: "elephant", expected: true, type: "fuzzy" },

  // Partial
  {
    guess: "large gray elephant",
    word: "elephant",
    expected: true,
    type: "partial",
  },

  // No match
  { guess: "giraffe", word: "elephant", expected: false, type: "none" },
];
```

## See Also

- `convex/mutations/game.ts` - Complete submission logic
- `components/game/guess-input.tsx` - UI for guess submission
- Levenshtein Distance: https://en.wikipedia.org/wiki/Levenshtein_distance
