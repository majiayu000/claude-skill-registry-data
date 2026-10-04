---
name: create-agent
description: Scaffold and develop AI agents — use when asked to create, build, or set up a new AI agent, including agent definition, instructions, tools, guardrails, handoffs, context, RAG pipelines, streaming, API routes, testing, and debugging.
---

Scaffold or develop an agent: $ARGUMENTS

## Before Starting

1. Search OpenAI docs for the latest Agents SDK patterns:
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK agent definition" to confirm current `Agent` constructor and `run()` patterns
   - Use `mcp__openai-docs__search_openai_docs` with query "Agents SDK tools" for tool definition patterns
2. Read existing agent definitions to understand project conventions:
   - `{{AGENTS_DIR}}/chat-coaches/index.ts` — simple agent (tenant-driven prompt, single model)
   - Read 1-2 files in the ai-lab-agent repo at `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/index.ts` for the function-based config pattern (instructions/tools/modelSettings as functions receiving RunContext)
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/writing-assistant/index.ts` — multi-mode agent with per-mode temperature/token configs
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/seo-expert/index.ts` — tool-heavy agent with ordered tool execution
3. Read the shared infrastructure:
   - `{{AGENTS_DIR}}/shared/enhanced-agent-bridge.ts` — bridge class that wraps agent execution
   - `{{AGENTS_DIR}}/shared/types.ts` — ChatKitRequest, ChatKitEvent, WritingContext types

---

## Part 1: Agent Scaffolding

### Step 1: Agent Definition

Create `{{AGENTS_DIR}}/<name>/index.ts`:

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

Create `{{AGENTS_DIR}}/<name>/instructions.ts` with composable instruction sections. Follow the pattern in ai-lab-agent where instructions are split into identity, context, and mode sections.

### Step 3: Tools File (if needed)

Create `{{AGENTS_DIR}}/<name>/tools.ts` using the `tool()` helper from `@openai/agents` with Zod parameter schemas. See the Tools section below for detailed patterns.

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

Add to `{{AGENTS_DIR}}/shared/handoffs.ts`:
```typescript
import { <name>Agent } from '@/agents/<name>';
agentRegistry.register('<name>', <name>Agent);
```

### Step 6: Export from Index

Create or update `{{AGENTS_DIR}}/index.ts` to export the new agent.

---

## Part 2: Tools

### Before Starting

1. Search OpenAI docs: `mcp__openai-docs__search_openai_docs` with query "Agents SDK tool definition" for current `tool()` helper signature
2. Read existing implementations:
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/tools/base.ts` — search_books, file_search tools with caching + metrics
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/seo-expert/tools.ts` — 9-tool suite
   - `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/tools/utils.ts` — `executeToolWithMetrics()`, timeout constants
3. Read: `{{PROJECT_ROOT}}/src/services/toolCacheService.ts` — param-based LRU caching with TTL

### Tool Template

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
    const cacheKey = `my_tool:${params.query}`;
    const cached = await toolCacheService.get(cacheKey);
    if (cached) return cached;

    const { result } = await executeToolWithMetrics('my_tool', async () => {
      return { data: 'result' };
    }, TOOL_TIMEOUTS.MEDIUM);

    toolCacheService.set(cacheKey, result).catch(() => {});
    return result;
  },
});
```

### Patterns by Tool Type

**Search / Retrieval Tools**: Return structured results with title, snippet, url/slug, relevance score. Always include `maxResults`. Gracefully degrade when unavailable.

**Analysis / Computation Tools**: Accept content as string input. Return structured analysis object with scores/categories/suggestions. Include confidence scores.

**API Integration Tools**: Validate API keys before calling. Set appropriate timeouts (SHORT=5s, MEDIUM=15s, LONG=30s). Return user-friendly errors. Never expose API keys.

**Database Query Tools**: Use the service layer (never raw SQL). Scope by `organizationId` for multi-tenant safety. Return only needed fields.

### Tool Registration

**Static** (simple agents):
```typescript
import { myTool } from './tools';
export const myAgent = new Agent({ tools: [myTool, existingTool1] });
```

**Dynamic** (function-based agents):
```typescript
export function getToolsForConfiguration(context: RunContext<MyContext>): Tool[] {
  const tools = [...getBaseTools()];
  if (context.context.someCondition) tools.push(myTool);
  return tools;
}
```

### Tool Rules

- Tool names must be snake_case
- Descriptions should tell the agent WHEN to use the tool, not just what it does
- Parameters must use Zod schemas with `.describe()` on every field
- Always handle errors gracefully — return error objects, never throw
- Cache results when the tool calls external services
- Wrap execution in `executeToolWithMetrics()` for observability
- Tool results are sent to the LLM — keep payloads concise

---

## Part 3: Instructions

### Before Starting

Read the existing instruction architecture:
- `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/core.ts` — identity + voice markers + failure modes
- `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/themes.ts` — theme-specific layers
- `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/modes.ts` — pedagogical modes
- `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/styles.ts` — interaction styles
- `{{PROJECT_ROOT}}/{{AGENTS_DIR}}/ai-lab/instructions/context.ts` — dynamic user context per run

### Instruction Architecture

Instructions are composed from **layers** concatenated at runtime:

```
STATIC (cached by dimension key)
  Core Identity — who the agent IS, voice markers, failure modes
  + Theme Layer — theological/framework lens
  + Mode Layer — pedagogical approach
  + Style Layer — interaction pattern

DYNAMIC (fresh per run)
  User Context — name, role, language, kairos, engagement
  + Conversation History — continuity from prior turns
  + Page/Content Context — what the user is currently viewing
```

Static sections are cached by key `{theme}-{mode}-{style}` (max 100 entries). Dynamic sections are NEVER cached.

### Writing Instructions

**Core Identity**: Role statement, voice markers (3-5 dimensions), signature elements, failure modes (what NOT to do).

**Theme/Mode/Style Layers**: Each adds a focused paragraph or two. Keep modular — should make sense in any combination.

**Dynamic Context** via `DynamicInstructionsGenerator`:
```typescript
export const myDynamicInstructions: DynamicInstructionsGenerator = async (
  baseInstructions: string,
  context: Record<string, unknown>
) => {
  const sections: string[] = [baseInstructions];
  if (context.userName) {
    sections.push(`## User Context\nYou are speaking with ${context.userName}.`);
  }
  return sections.join('\n\n');
};
```

### Instruction Rules

- Never hardcode tenant-specific names — use `brandConfig` or DB-backed content
- Keep total instruction length under 10,000 tokens
- Voice markers should be descriptive enough for the LLM to calibrate tone
- Failure modes are as important as positive instructions
- For book-related agents, include mandatory retrieval instructions

---

## Part 4: Context

### Context Architecture

```
UI Drawer (client) → AILabNewContextDraft (Zod) → buildRunContractPayload() (validates slugs)
  → RunContract (sent to agent) → buildUserContextInstructions() → Dynamic Instructions
```

### Context Schema

```typescript
export const aiLabNewContextDraftSchema = z.object({
  name: z.string().optional(),
  location: z.string().optional(),
  vocational: z.object({ role: z.string().optional(), context: z.string().optional() }).optional(),
  personality: z.object({ type: z.string().optional(), details: z.string().optional() }).optional(),
  neighborhood: z.object({ description: z.string().optional(), challenges: z.string().optional() }).optional(),
  kairos: z.object({ worldEvents: z.string().optional(), lifeEvents: z.string().optional() }).optional(),
  engagement: z.enum(['exploring', 'learning', 'applying', 'leading']).optional(),
  booksFocus: z.array(z.string()).optional(),
  topicsSelected: z.array(z.string()).optional(),
  language: z.string().default('en'),
});
```

### Adding New Context Fields

1. Add to the Zod schema (`context-schema-template.ts`)
2. Add UI collection in the context drawer
3. Map to RunContract in `assemble-user-context.ts`
4. Render as a context block in `build-user-context-blocks.ts`
5. Use in dynamic instructions

### Context Rules

- Context schemas must be Zod-validated
- Validate book/topic slugs against the catalog — drop unknowns silently
- Dynamic context is NEVER cached
- Never include sensitive user data in context blocks
- User context shapes the conversation; agent content shapes the voice — keep them separate

---

## Part 5: Guardrails

### Input Guardrails

Validate user messages BEFORE they reach the agent:

```typescript
export function myInputGuardrail(): InputGuardrail {
  return {
    name: 'my_guardrail',
    validate: async (message: string) => {
      if (someCondition(message)) {
        return { passed: false, reason: 'Specific reason for rejection' };
      }
      return { passed: true };
    },
  };
}
```

### Output Guardrails

Validate agent responses BEFORE they reach the user. Same interface.

### Built-in Guardrails

| Name | Type | What it does |
|------|------|-------------|
| `nonEmpty()` | Input & Output | Rejects empty/whitespace-only messages |
| `maxLength(n)` | Input | Rejects messages over n characters |
| `contentFilter()` | Input | Blocks XSS patterns |
| `noErrors()` | Output | Detects error indicators in output |

### Guardrail Rules

- Guardrails must be fast — avoid LLM calls
- Input guardrails protect the agent; output guardrails protect the user
- Return clear, user-friendly rejection messages
- Order matters: put cheap checks before expensive ones

---

## Part 6: Handoffs

### Agent Registry

```typescript
import { agentRegistry } from '@/agents/shared/handoffs';
agentRegistry.register('my-agent', myAgent);
agentRegistry.register('expert', expertAgent);
```

### Handoff Decision Logic

```typescript
export const myHandoffHandler: HandoffHandler = async (
  message: string, context: Record<string, unknown>, currentAgent: string
): Promise<HandoffDecision> => {
  const seoKeywords = /\b(seo|search engine|meta tags)\b/i;
  if (seoKeywords.test(message) && currentAgent !== 'seo-expert') {
    return { shouldHandoff: true, targetAgent: 'seo-expert', reason: 'SEO question' };
  }
  return { shouldHandoff: false };
};
```

Enable in the bridge: `enableHandoffs: true`

### Handoff Rules

- Register agents in `agentRegistry` before enabling handoffs
- Use keyword matching, not LLM calls, for handoff decisions
- Prevent circular handoffs — max depth: 3
- Preserve conversation context across handoffs
- Check OpenAI docs for SDK-native handoff support

---

## Part 7: RAG Pipeline

### Architecture

```
User Message → Intent Router (classify query type) → File Search (vector store)
  → Post-Filter + Re-Sort (by user context) → Fallback Search (if needed)
  → Citation Render (file path → book/chapter) → EnrichedResultItem[]
```

### Intent Types

`QUOTE_REQUEST`, `CROSS_BOOK_COMPARISON`, `GLOSSARY_DEFINITION`, `RESEARCH_MODE`, `TOPIC_GUIDE`, `BOOK_SPECIFIC`, `GENERAL_CONVERSATION`

### Book Fidelity Contract

- Cache skipping for book-related requests
- Temperature override: 0.2-0.3 for book fidelity
- Mandatory tool usage: always use file_search before answering book questions
- Citation requirement: output guardrail checks for citations

### RAG Rules

- Gracefully degrade when vector store is unavailable
- Post-filter by user context (booksFocus, topicsSelected)
- Include fallback search with broadened query
- Citation rendering must be deterministic
- Keep retrieval payloads concise

---

## Part 8: Streaming

### Dual Stream Formats

**SSE** (`text/event-stream`): Primary format. Events as `data: {json}\n\n`.

**Plain Text** (`text/plain`): Vercel AI SDK compatibility. Triggered by `?format=text`. Appends `__AILAB_SESSION_ID__:uuid`.

### ChatKit Event Types

`text_delta`, `tool_call`, `tool_complete`, `image`, `done`, `error`, `progress`

### Session Continuity

- Request carries `conversationId`
- Response `done` event includes `sessionId`
- Client captures session ID for multi-turn continuity

### Streaming Rules

- Always include `Cache-Control: no-cache` and `Connection: keep-alive`
- The `done` event MUST include `sessionId`
- Window messages to prevent token overflow (max 50)
- Never buffer entire response before streaming

---

## Part 9: Testing

### Unit Tests (Vitest)

Test tools, instructions, router, citations, and guardrails:
```bash
pnpm test:run -- agents
```

### Smoke Tests

Hit running endpoints to assert tool invocation and citation presence.

### E2E Tests (Playwright)

```bash
pnpm test:e2e -- agents
```

### Testing Rules

- Unit tests must not call external APIs — mock them
- Test both happy paths and error cases
- For retrieval tests, assert tool invocation AND citation presence
- Keep test files focused — one file per concern

---

## Part 10: Debugging

### Trace Event Types

`start`, `tool_call`, `tool_complete`, `handoff`, `stream_delta`, `complete`, `error`

### Debug Flags

```bash
AI_LAB_DEBUG_TOOLS=true
AI_LAB_DEBUG_CONTEXT=true
AI_LAB_DEBUG_INSTRUCTIONS=true
AI_LAB_DEBUG_RETRIEVAL=true
```

### Analysis Patterns

- **Slow responses**: Query traces with high duration, check tool_call durations
- **Tool failures**: Check error events, validate tool params, check external service availability
- **Guardrail rejections**: Check error events with guardrail name and reason

---

## Top-Level Rules

- Use `brandConfig` for any tenant-specific strings — never hardcode
- Always wire through EnhancedAgentBridge for guardrails, tracing, and metrics
- Use streaming (SSE) responses via the bridge — never return plain JSON for chat
- Follow the Result<T> pattern in any service calls within tools
- Check OpenAI docs MCP for any SDK changes before generating agent code
