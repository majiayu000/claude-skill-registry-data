---
name: structured-logging
description: Convex backend JSON logging patterns. Custom logger with levels, context objects, tag conventions. Triggers on "logger.", "log", "logging", "debug", "error", "warn", "info".
---

# Structured Logging (Convex Backend)

Custom JSON logger for Convex actions/queries/mutations. NOT Pino (that's web app only).

## Logger Import

```typescript
import { logger } from "./lib/logger";
// or
import { logger } from "../lib/logger";
```

Always import from `convex/lib/logger.ts`. Each log outputs JSON to console with timestamp.

## Log Levels

Four levels available:

```typescript
logger.debug("Message", { context });  // Development details
logger.info("Message", { context });   // Normal flow
logger.warn("Message", { context });   // Recoverable issues
logger.error("Message", { context });  // Errors, failures
```

Use:
- `debug` - internal state, variable values, flow tracking
- `info` - major milestones (router decisions, feature completions)
- `warn` - fallbacks, non-critical failures
- `error` - exceptions, failed operations, user-facing errors

## Context Object Pattern

Context is `Record<string, unknown>`. Common fields:

```typescript
// From generation.ts
logger.info("Auto router selected model", {
  conversationId: args.conversationId,
  selectedModel: modelId,
  classification: routerResult.classification.primaryCategory,
});

logger.info("Using cached system prompt", {
  tag: "Generation",
  messageCount: cachedMessages.length,
});

logger.info("Total sources", {
  tag: "Sources",
  total: allSources.length,
  perplexity: perplexitySourceCount,
  webSearch: webSearchSources.length,
});
```

Pass IDs, counts, enums, primitives. Avoid huge objects.

## Tag Field Convention

Use `tag` field to categorize logs by feature/subsystem:

```typescript
logger.info("...", { tag: "Generation" });
logger.info("...", { tag: "Sources" });
logger.error("...", { tag: "HybridSearch" });
```

Common tags: `Generation`, `Sources`, `HybridSearch`, `Memory`, `Tools`, `Router`

Tag helps filter logs in Convex dashboard. Use PascalCase.

## Error Context

Always include full context on errors:

```typescript
// From generation.ts - full error details
logger.error("Generation error", {
  tag: "Generation",
  error: String(error),
});

logger.error("Full gateway error", {
  tag: "Generation",
  statusCode: causeObj.statusCode || (error as any).statusCode,
  model: args.modelId,
  errorMessage: parsedBody?.error?.message,
  fullResponse: parsedBody,
});

// From hybrid.ts - fallback scenario
logger.error("Vector search failed, falling back to text-only", {
  tag: "HybridSearch",
  error: String(error),
});
```

Pattern: `String(error)` to stringify, include model/operation/resource IDs, preserve full API responses for debugging.

## When to Log vs Throw

**Log + throw**: User errors, expected failures, retryable errors
```typescript
logger.error("Generation error", { tag: "Generation", error: String(error) });
await ctx.runMutation(internal.messages.markError, { messageId, error: userMessage });
throw error; // Propagate for error boundary
```

**Log only (warn)**: Fallbacks, degraded mode
```typescript
logger.error("Failed to parse cached prompt, falling back", { tag: "Generation" });
// Continue with fallback logic
```

**Log only (info)**: Success paths, milestones
```typescript
logger.info("Continuation successful", { tag: "Generation", charCount: accumulated.length });
```

**Don't log**: Internal helpers, tight loops. Keep logs meaningful.

## Common Patterns

### Router decisions
```typescript
logger.info("Auto router selected model", {
  conversationId: args.conversationId,
  selectedModel: modelId,
  classification: routerResult.classification.primaryCategory,
});
```

### Cache hits
```typescript
logger.info("Using cached system prompt", {
  tag: "Generation",
  messageCount: cachedMessages.length,
});
```

### Feature extraction
```typescript
logger.info("Extracted sources from result.sources (Perplexity)", {
  tag: "Sources",
  count: sources.length,
});
```

### Error fallbacks
```typescript
logger.error("Continuation failed, using fallback", {
  tag: "Generation",
  error: String(continuationError),
});
```

### Resource processing
```typescript
logger.info("Processing generated files", {
  tag: "Generation",
  count: files.length,
});
```

## Anti-Patterns

- ❌ Don't log before every operation - only milestones/errors
- ❌ Don't log huge objects - extract key fields
- ❌ Don't use console.log directly - always use logger
- ❌ Don't skip `tag` field in feature-specific logs
- ❌ Don't log in tight loops (per-message iterations)
- ❌ Don't use template literals in context - use separate fields

## Output Format

Logger outputs JSON:
```json
{
  "level": "info",
  "message": "Auto router selected model",
  "timestamp": "2026-01-16T12:34:56.789Z",
  "conversationId": "k17abc123",
  "selectedModel": "openai:gpt-4o",
  "classification": "code"
}
```

Convex dashboard automatically parses and displays.

## Key Files

- `packages/backend/convex/lib/logger.ts` - Logger implementation
- `packages/backend/convex/generation.ts` - Extensive usage examples
- `packages/backend/convex/search/hybrid.ts` - Error logging pattern

## Notes

- Logger is synchronous (console.log/warn/error wrappers)
- Timestamps are ISO8601 strings
- All logs visible in Convex dashboard logs tab
- Use structured fields for filtering/searching in dashboard
- Fire-and-forget analytics use `.catch(() => {})` pattern
