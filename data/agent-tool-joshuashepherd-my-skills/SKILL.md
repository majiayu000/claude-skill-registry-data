---
name: agent-tool
description: Create or modify an OpenAI Agents SDK tool with Zod params, caching, metrics, and agent registration. Use when adding tools to agents.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, mcp__openai-docs__search_openai_docs, mcp__openai-docs__fetch_openai_doc
---

Create or modify an agent tool: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for latest tool patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK tool definition" for current `tool()` helper signature
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK function tools parameters" for parameter schema patterns
2. Read existing tool implementations:
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/tools/base.ts` — search_books, file_search tools with caching + metrics
   - `/Users/joshuashepherd/Desktop/dev/repos/movemental-dashboard/src/agents/seo-expert/tools.ts` — 9-tool suite (analyze, research, score, optimize, generate)
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/tools/utils.ts` — `executeToolWithMetrics()`, timeout constants
3. Read the shared tool infrastructure:
   - `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/services/toolCacheService.ts` — param-based LRU caching with TTL

## Tool Template

```typescript
import { tool } from '@openai/agents';
import { z } from 'zod';
import type { RunContext } from '@openai/agents';

export const myTool = tool({
  name: 'my_tool',
  description: 'Clear, specific description of what this tool does and when the agent should use it.',
  parameters: z.object({
    query: z.string().describe('What to search for'),
    maxResults: z.number().optional().default(5).describe('Maximum results to return'),
  }),
  strict: true,
  execute: async (params, context?: RunContext<MyContext>) => {
    // 1. Check cache (if applicable)
    const cacheKey = `my_tool:${params.query}`;
    const cached = await toolCacheService.get(cacheKey);
    if (cached) return cached;

    // 2. Execute with metrics and timeout
    const { result } = await executeToolWithMetrics('my_tool', async () => {
      // Tool implementation here
      return { data: 'result' };
    }, TOOL_TIMEOUTS.MEDIUM);

    // 3. Cache result
    toolCacheService.set(cacheKey, result).catch(() => {});

    return result;
  },
});
```

## Patterns by Tool Type

### Search / Retrieval Tools
- Return structured results with title, snippet, url/slug, relevance score
- Always include a `maxResults` parameter with sensible default
- Gracefully degrade when external service is unavailable (return empty array, not error)
- Add citation metadata when results reference source material

### Analysis / Computation Tools
- Accept content as string input
- Return structured analysis object (scores, categories, suggestions)
- Include confidence scores where applicable
- Keep descriptions prescriptive so the agent knows when to invoke

### API Integration Tools
- Validate API keys exist before calling
- Set appropriate timeouts (TOOL_TIMEOUTS: SHORT=5s, MEDIUM=15s, LONG=30s)
- Return user-friendly error messages, not raw API errors
- Never expose API keys in tool results

### Database Query Tools
- Use the service layer (never raw SQL in tools)
- Scope by `organizationId` from context for multi-tenant safety
- Return only fields the agent needs, not entire rows

## Registration

After creating the tool, register it with the target agent:

**Static registration** (simple agents):
```typescript
// In the agent's index.ts
import { myTool } from './tools';
export const myAgent = new Agent({
  tools: [myTool, existingTool1],
});
```

**Dynamic registration** (function-based agents):
```typescript
// In the agent's tools/index.ts
export function getToolsForConfiguration(context: RunContext<MyContext>): Tool[] {
  const tools = [...getBaseTools()];
  if (context.context.someCondition) {
    tools.push(myTool);
  }
  return tools;
}
```

## Rules

- Tool names must be snake_case
- Descriptions should tell the agent WHEN to use the tool, not just what it does
- Parameters must use Zod schemas with `.describe()` on every field
- Always handle errors gracefully — return error objects, never throw
- Cache results when the tool calls external services
- Wrap execution in `executeToolWithMetrics()` for observability
- Tool results are sent to the LLM — keep payloads concise (truncate large results)
- Check OpenAI docs MCP for any SDK changes to the `tool()` helper before generating code
