---
name: "Convex Agents Debugging"
description: "Troubleshoots agent behavior, logs LLM interactions, and inspects database state. Use this when responses are unexpected, to understand context the LLM receives, or to diagnose data issues."
---

## Purpose

Debugging tools help understand what's happening inside agents, what the LLM receives, and what's stored. Essential for developing reliable agent applications.

## When to Use This Skill

- Agent behavior is unexpected
- LLM responses are off-target
- Investigating why certain context isn't being used
- Understanding message ordering
- Checking file storage and references
- Auditing tool calls and results
- Profiling token usage

## Log Raw LLM Requests and Responses

```typescript
const myAgent = new Agent(components.agent, {
  name: "My Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  rawRequestResponseHandler: async (ctx, { request, response }) => {
    console.log("LLM Request:", JSON.stringify(request, null, 2));
    console.log("LLM Response:", JSON.stringify(response, null, 2));

    await ctx.runMutation(internal.logging.saveLLMCall, {
      request,
      response,
      timestamp: Date.now(),
    });
  },
});
```

## Log Context Messages

See exactly what context the LLM receives:

```typescript
const myAgent = new Agent(components.agent, {
  name: "My Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  contextHandler: async (ctx, args) => {
    console.log("Context Messages:", {
      recent: args.recent.length,
      search: args.search.length,
      input: args.inputMessages.length,
    });

    args.allMessages.forEach((msg, i) => {
      console.log(`Message ${i}:`, {
        role: msg.role,
        contentLength: typeof msg.content === "string"
          ? msg.content.length
          : JSON.stringify(msg.content).length,
      });
    });

    return args.allMessages;
  },
});
```

## Inspect Database Tables

Query agent data directly:

```typescript
export const getThreadMessages = query({
  args: { threadId: v.string() },
  handler: async (ctx, { threadId }) => {
    return await ctx.db
      .query(components.agent.tables.messages)
      .filter((msg) => msg.threadId === threadId)
      .collect();
  },
});
```

## Fetch Context Manually

Inspect what context would be used:

```typescript
import { fetchContextWithPrompt } from "@convex-dev/agent";

export const inspectContext = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { messages } = await fetchContextWithPrompt(ctx, components.agent, {
      threadId,
      prompt,
    });

    return {
      contextMessages: messages.length,
      messages: messages.map((msg) => ({
        role: msg.role,
        contentType: typeof msg.content,
      })),
    };
  },
});
```

## More Techniques

The remaining debugging techniques and their code are in the reference file.

Sections in `references/more-techniques.md`:

- Trace Tool Calls
- Fix Type Errors
- Analyze Message Structure

## Key Principles

- **Log early**: Capture data while developing
- **Use console for quick checks**: Fast iteration
- **Save important events**: Archive LLM calls for analysis
- **Explicit return types**: Prevents circular references
- **Dashboard inspection**: Easiest way to see database state

## Next Steps

- See **playground** for interactive debugging
- See **fundamentals** for agent setup
- See **context** for context-aware debugging
