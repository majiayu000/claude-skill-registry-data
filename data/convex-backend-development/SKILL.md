---
name: convex-backend-development
description: Develop and maintain Convex backend functions including queries, mutations, and actions. Use when working with database operations, authentication, game management, scoring logic, and real-time data updates in the dev-quiz-battle app.
license: MIT
metadata:
  author: dev-quiz-battle
  version: "1.0"
---

# Convex Backend Development

This skill covers building and maintaining Convex backend functions for the dev-quiz-battle application.

## Step-by-step instructions

### 1. Understanding the Project Structure

The Convex backend is located in the `convex/` directory with:

- `queries/` - Read-only functions (games, users, answers, leaderboard)
- `mutations/` - Write operations (creating games, submitting answers, updating user scores)
- `actions/` - Long-running operations (AI question generation)
- `schema.ts` - Database schema definition
- `auth.ts` - Authentication configuration

### 2. Creating Queries

Queries fetch data from the database without modifying it. Common patterns:

```typescript
import { query } from "convex/server";
import { v } from "convex/values";

export const getGameData = query({
  args: { gameCode: v.string() },
  handler: async (ctx, args) => {
    const game = await ctx.db
      .query("games")
      .filter((q) => q.eq(q.field("code"), args.gameCode))
      .first();
    return game;
  },
});
```

### 3. Creating Mutations

Mutations modify the database state. Always validate input:

```typescript
import { mutation } from "convex/server";
import { v } from "convex/values";

export const createGame = mutation({
  args: { creatorId: v.id("users"), language: v.string() },
  handler: async (ctx, args) => {
    const gameId = await ctx.db.insert("games", {
      creatorId: args.creatorId,
      language: args.language,
      code: generateUniqueCode(),
      status: "waiting",
      createdAt: Date.now(),
    });
    return gameId;
  },
});
```

### 4. Creating Actions

Actions handle async operations like API calls:

```typescript
import { action } from "convex/server";
import { v } from "convex/values";

export const generateQuestion = action({
  args: { language: v.string(), difficulty: v.string() },
  handler: async (ctx, args) => {
    // Call external API or perform async work
    const response = await fetch("https://api.example.com/questions");
    return response.json();
  },
});
```

### 5. Using Authentication

Access the authenticated user:

```typescript
const identity = await ctx.auth.getUserIdentity();
if (!identity) {
  throw new Error("Not authenticated");
}
const userId = identity.subject;
```

### 6. Validation Patterns

Always validate arguments using Convex validators:

```typescript
args: {
  email: v.string(),
  password: v.string(),
  language: v.string(),
}
```

## Common Edge Cases

- **Invalid game codes**: Check if game exists before operations
- **Concurrent submissions**: Use game status to prevent duplicate answers
- **User authentication**: Always verify identity for sensitive mutations
- **Score calculations**: Account for time-based bonuses and difficulty multipliers

## Key Files to Reference

See [Convex Schema Reference](references/CONVEX_SCHEMA.md) for complete schema definition.
