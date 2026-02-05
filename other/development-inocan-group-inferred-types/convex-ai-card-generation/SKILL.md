---
name: convex-ai-card-generation
description: Generate Pictionary drawing cards using AI (Groq) with fallback to hardcoded libraries. Use when creating new game cards, implementing category-based card selection, or handling AI card generation with graceful degradation.
compatibility: Requires Convex actions, Vercel AI SDK, Groq API access, fallback card libraries
metadata:
  author: PictionAI
  category: backend, ai
  frameworks: Convex, Vercel AI SDK, Groq
  models: groq-mixtral-8x7b, groq-llama2
---

# Convex AI Card Generation

## Overview

This skill handles AI-powered card generation for PictionAI's Pictionary gameplay. Cards are generated dynamically using Groq LLM with Vercel AI SDK's `generateText` function, including structured output validation via Zod schemas and automatic fallback to hardcoded card libraries when API limits are reached.

## Architecture

### Generation Flow

```
1. Request card for category
   ↓
2. Check card availability/balance
   ↓
3. Try Groq (primary) → Fallback to other models → Fallback to hardcoded library
   ↓
4. Validate with Zod schema
   ↓
5. Return structured card object { word, description, difficulty, category }
```

### AI Models (Priority Order)

1. **groq-mixtral-8x7b-instruct** (Primary) - Best quality, lower latency
2. **groq-llama2-70b-chat** (Secondary) - If Mixtral unavailable
3. **groq-llama-3.1-70b** (Tertiary) - Fallback option
4. **Hardcoded Library** (Final) - When all API models fail

## Key Action

### generateCards

Generate one or multiple drawing cards for a specific category with AI.

```typescript
action generateCards {
  args: {
    category: "animals" | "objects" | "actions" | "movies" | "sports",
    count?: number  // Default: 1, Max: 5
  }
  // Returns:
  // {
  //   cards: Array<{
  //     word: string,
  //     description: string,
  //     difficulty: "easy" | "medium" | "hard",
  //     category: string
  //   }>,
  //   source: "ai" | "fallback"  // Indicates if AI or hardcoded
  // }
}
```

## Card Data Structure

```typescript
interface Card {
  word: string; // Single word to draw (required)
  description: string; // Drawing hints/clues (1-100 chars)
  difficulty: "easy" | "medium" | "hard";
  category: string; // Category name
  created_at?: number; // Timestamp
  ai_generated?: boolean; // True if from Groq
}
```

## Supported Categories

- **animals** - Creatures, pets, wildlife
- **objects** - Inanimate items, tools, furniture
- **actions** - Verbs, activities, gestures
- **movies** - Film titles, characters, scenes
- **sports** - Sports, games, athletic activities
- **food** - Dishes, ingredients, cuisine
- **technology** - Gadgets, software, digital items

## Implementation Details

### Groq Configuration

```typescript
const groq = new Groq({
  apiKey: env.GROQ_API_KEY, // Environment variable
  baseURL: "https://api.groq.com/openai/v1",
});
```

### Zod Schema for Validation

```typescript
const cardSchema = z.object({
  word: z.string().min(1).max(30),
  description: z.string().min(10).max(100),
  difficulty: z.enum(["easy", "medium", "hard"]),
  category: z.string(),
});

const cardsResponseSchema = z.object({
  cards: z.array(cardSchema),
});
```

### AI Prompt Template

```
Generate {count} unique Pictionary drawing cards for the "{category}" category.
For each card, provide:
- word: A single word to draw
- description: A brief hint (1-100 characters)
- difficulty: easy, medium, or hard
- category: {category}

Format as JSON array. Make words creative and diverse.
```

## Fallback Card Libraries

When all AI models fail, the system falls back to hardcoded libraries:

```typescript
const cardLibraries = {
  animals: [
    {
      word: "elephant",
      description: "Large animal with long trunk",
      difficulty: "easy",
      category: "animals",
    },
    {
      word: "giraffe",
      description: "Tall with spotted pattern",
      difficulty: "easy",
      category: "animals",
    },
    // ... more animals
  ],
  objects: [
    {
      word: "bicycle",
      description: "Two-wheeled vehicle",
      difficulty: "easy",
      category: "objects",
    },
    // ... more objects
  ],
  // ... other categories
};
```

## React Integration

```typescript
// In game setup, generate initial card
const generateCardsAction = useAction(api.actions.generateCards);

async function setupGameCards(category: string) {
  const result = await generateCardsAction({
    category,
    count: 5, // Generate 5 cards per round
  });

  console.log(`Cards generated from ${result.source}`);
  return result.cards;
}
```

## Error Handling

### Graceful Degradation

1. **API Quota Exceeded** → Automatically switch to fallback
2. **Network Error** → Retry once, then use fallback
3. **Invalid Response** → Log error, use fallback
4. **Schema Validation Fail** → Discard AI response, use fallback

### Logging

```typescript
console.log(`Generated cards from ${source} for category: ${category}`);
// source: "ai" or "fallback"
```

## Performance Considerations

- **AI Generation**: ~500-1000ms per card (includes API latency)
- **Fallback Lookup**: ~50ms per card
- **Caching**: Consider caching generated cards per category/session
- **Batch Generation**: Generate 5-10 cards at game start, not on-demand per turn

## Best Practices

### Do's

✅ Generate multiple cards at game start (not per turn)
✅ Cache cards for session duration
✅ Log both AI and fallback usage for monitoring
✅ Validate all AI responses against Zod schema
✅ Handle quota errors gracefully

### Don'ts

❌ Don't wait for card generation on each turn
❌ Don't expose Groq API key in frontend
❌ Don't retry forever on network errors
❌ Don't mix AI and fallback for same category in single game

## Example: Complete Card Setup

```typescript
// Game initialization
export const initializeGameCards = action({
  args: { game_id: v.id("games"), category: v.string() },
  handler: async (ctx, args) => {
    const generateCards = await ctx.runAction(api.actions.generateCards, {
      category: args.category,
      count: 10,
    });

    // Store cards in game doc
    await ctx.runMutation(api.mutations.games.storeGameCards, {
      game_id: args.game_id,
      cards: generateCards.cards,
    });

    return {
      count: generateCards.cards.length,
      source: generateCards.source,
    };
  },
});
```

## See Also

- `convex/actions/generateCards.ts` - Complete action implementation
- Groq API docs: https://console.groq.com/docs
- Vercel AI SDK: https://sdk.vercel.ai
