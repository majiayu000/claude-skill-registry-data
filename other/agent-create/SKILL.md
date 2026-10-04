---
name: agent-create
description: Scaffold a new OpenAI Agents SDK agent with instructions, tools, API route, and bridge wiring. Use when creating a new specialized agent from scratch.
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, mcp__openai-docs__search_openai_docs, mcp__openai-docs__fetch_openai_doc
---

Scaffold a new agent: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for the latest Agents SDK patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK agent definition" to confirm current `Agent` constructor and `run()` patterns
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK tools" for tool definition patterns
2. Read existing agent definitions to understand project conventions:
   - `src/agents/chat-coaches/index.ts` — simple agent (tenant-driven prompt, single model)
   - Read 1-2 files in the ai-lab-agent repo at `/Users/joshuashepherd/Desktop/dev/repos/ai-lab-agent/src/agents/ai-lab/index.ts` for the function-based config pattern (instructions/tools/modelSettings as functions receiving RunContext)
   - `/Users/joshuashepherd/Desktop/dev/repos/movemental-dashboard/src/agents/writing-assistant/index.ts` — multi-mode agent with per-mode temperature/token configs
   - `/Users/joshuashepherd/Desktop/dev/repos/movemental-dashboard/src/agents/seo-expert/index.ts` — tool-heavy agent with ordered tool execution
3. Read the shared infrastructure:
   - `src/agents/shared/enhanced-agent-bridge.ts` — bridge class that wraps agent execution
   - `src/agents/shared/types.ts` — ChatKitRequest, ChatKitEvent, WritingContext types

## Scaffold Steps

### Step 1: Agent Definition

Create `src/agents/<name>/index.ts`:

```typescript
import { Agent } from '@openai/agents';

export const <name>Agent = new Agent({
  name: '<Display Name>',
  instructions: '<system prompt — or import from instructions.ts>',
  model: '<model-id>',  // gpt-4o, gpt-4o-mini, etc.
  tools: [],  // or import from tools.ts
  modelSettings: {
    temperature: 0.7,
    maxTokens: 2000,
  },
});
```

For complex agents that need runtime adaptation, use the function-based pattern from ai-lab-agent:

```typescript
export const <name>Agent = new Agent({
  name: '<Display Name>',
  instructions: (context: RunContext<MyContext>) => generateInstructions(context),
  tools: (context: RunContext<MyContext>) => getToolsForAgent(context),
  modelSettings: (context: RunContext<MyContext>) => getModelSettings(context),
});
```

### Step 2: Instructions File (if complex)

Create `src/agents/<name>/instructions.ts` with composable instruction sections. Follow the pattern in ai-lab-agent where instructions are split into identity, context, and mode sections.

### Step 3: Tools File (if needed)

Create `src/agents/<name>/tools.ts` using the `tool()` helper from `@openai/agents` with Zod parameter schemas. See the `agent-tool` skill for detailed tool patterns.

### Step 4: API Route

Create `src/app/api/agents/<name>/route.ts`:

```typescript
import { NextRequest } from 'next/server';
import { createServerClient } from '@/lib/supabase/server';
import { createEnhancedAgentBridge } from '@/agents/shared/enhanced-agent-bridge';
import { nonEmpty, maxLength, contentFilter } from '@/agents/shared/guardrails';
import { noErrors } from '@/agents/shared/guardrails';
import { defaultDynamicInstructions } from '@/agents/shared/dynamic-instructions';
import { <name>Agent } from '@/agents/<name>';

export const maxDuration = 60;

export async function POST(req: NextRequest) {
  const supabase = await createServerClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return new Response('Unauthorized', { status: 401 });

  const bridge = createEnhancedAgentBridge(<name>Agent, {
    agentId: '<name>',
    inputGuardrails: [nonEmpty(), maxLength(10000), contentFilter()],
    outputGuardrails: [nonEmpty(), noErrors()],
    dynamicInstructions: defaultDynamicInstructions,
    enableHandoffs: false,
    tracing: { workflowName: '<name>-agent' },
  });

  return bridge.handleRequest(req);
}
```

### Step 5: Register in Agent Registry (if handoffs needed)

Add to `src/agents/shared/handoffs.ts`:
```typescript
import { <name>Agent } from '@/agents/<name>';
agentRegistry.register('<name>', <name>Agent);
```

### Step 6: Export from Index

Create or update `src/agents/index.ts` to export the new agent.

## Rules

- Use `tenantConfig` for any tenant-specific strings in the system prompt — never hardcode
- Agent instructions should reference the thought leader's voice and content when relevant
- Always wire through EnhancedAgentBridge for guardrails, tracing, and metrics
- Use streaming (SSE) responses via the bridge — never return plain JSON for chat
- Follow the Result<T> pattern in any service calls within tools
- Check OpenAI docs MCP for any SDK changes before generating agent code
