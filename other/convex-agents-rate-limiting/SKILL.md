---
name: "Convex Agents Rate Limiting"
description: "Controls message frequency and token usage to prevent abuse and manage API budgets. Use this to implement per-user limits, global caps, burst capacity, and token quota management."
---

## Purpose

Rate limiting protects against abuse, manages LLM costs, and ensures fair resource allocation. Covers message frequency limits and token usage quotas.

## When to Use This Skill

- Preventing rapid-fire message spam
- Limiting total tokens per user
- Implementing burst capacity
- Global API limits to stay under provider quotas
- Fair resource allocation in multi-user systems
- Billing based on token usage

## Configure Rate Limiter

```typescript
import { RateLimiter, MINUTE, SECOND } from "@convex-dev/rate-limiter";

export const rateLimiter = new RateLimiter(components.rateLimiter, {
  sendMessage: {
    kind: "fixed window",
    period: 5 * SECOND,
    rate: 1,
    capacity: 2,
  },
  globalSendMessage: {
    kind: "token bucket",
    period: MINUTE,
    rate: 1_000,
  },
  tokenUsagePerUser: {
    kind: "token bucket",
    period: MINUTE,
    rate: 2000,
    capacity: 10000,
  },
  globalTokenUsage: {
    kind: "token bucket",
    period: MINUTE,
    rate: 100_000,
  },
});
```

## More Patterns

Message-limit checks, usage tracking and client-side checks are in the reference file.

Sections in `references/more-patterns.md`:

- Check Message Rate Limit
- Track Actual Usage
- Client-Side Rate Limit Checking

## Check Token Usage

```typescript
export const checkTokenUsage = action({
  args: { threadId: v.string(), question: v.string(), userId: v.string() },
  handler: async (ctx, { threadId, question, userId }) => {
    const estimatedTokens = await estimateTokens(ctx, threadId, question);

    try {
      await rateLimiter.check(ctx, "tokenUsagePerUser", {
        key: userId,
        count: estimatedTokens,
        throws: true,
      });

      // Proceed with generation
      const { thread } = await myAgent.continueThread(ctx, { threadId });
      const result = await thread.generateText({ prompt: question });

      return { success: true, response: result.text };
    } catch (error) {
      if (isRateLimitError(error)) {
        return {
          success: false,
          error: "Token limit exceeded",
          retryAfter: error.data.retryAfter,
        };
      }
      throw error;
    }
  },
});

async function estimateTokens(
  ctx: QueryCtx,
  threadId: string,
  question: string
): Promise<number> {
  const questionTokens = Math.ceil(question.length / 4);
  const responseTokens = Math.ceil(questionTokens * 3);
  return questionTokens + responseTokens;
}
```

## Key Principles

- **Fixed window for frequency**: Use for simple X per period
- **Token bucket for capacity**: Use for burst-friendly limits
- **Estimate before, track after**: Prevent early, record actual usage
- **Global + per-user limits**: Balance fair access with resource caps
- **Retryable errors**: Clients can retry with backoff

## Next Steps

- See **usage-tracking** for billing based on token usage
- See **fundamentals** for agent setup
- See **debugging** for troubleshooting
