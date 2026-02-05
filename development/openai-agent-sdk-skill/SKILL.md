---
name: openai-agent-sdk-skill
description: Create OpenAI Agents SDK applications in TypeScript/JavaScript. Use when building AI agents, multi-agent systems, voice agents, or any agentic workflow with the OpenAI Agents SDK. Covers agents, tools, handoffs, guardrails, streaming, MCP, and realtime voice agents.
---

# OpenAI Agents SDK Skill

Build powerful AI agents using the OpenAI Agents SDK for TypeScript/JavaScript.

## Setup

```bash
# Create project
mkdir my-agent && cd my-agent
npm init -y

# Install dependencies
npm install @openai/agents zod@3

# Set API key
export OPENAI_API_KEY=sk-...
```

Or programmatically:
```typescript
import { setDefaultOpenAIKey } from '@openai/agents';
setDefaultOpenAIKey(process.env.OPENAI_API_KEY!);
```

---

## Basic Agent

**IMPORTANT: Always use `gpt-5-nano` as the default model for most agents.**

```typescript
import { Agent, run } from '@openai/agents';

const agent = new Agent({
  name: 'Assistant',
  instructions: 'You are a helpful assistant.',
  model: 'gpt-5-nano', // Use gpt-5-nano for most agents
});

const result = await run(agent, 'Hello!');
console.log(result.finalOutput);
```

### Agent Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Human-readable identifier |
| `instructions` | Yes | System prompt (string or function) |
| `model` | No | Model name (use `gpt-5-nano`) |
| `modelSettings` | No | Temperature, top_p, etc. |
| `tools` | No | Array of tools |
| `handoffs` | No | Array of agents to hand off to |
| `outputType` | No | Zod schema for structured output |
| `inputGuardrails` | No | Input validation guardrails |
| `outputGuardrails` | No | Output validation guardrails |

---

## Tools

### Function Tools

```typescript
import { Agent, tool, run } from '@openai/agents';
import { z } from 'zod';

const getWeather = tool({
  name: 'get_weather',
  description: 'Get weather for a city',
  parameters: z.object({
    city: z.string(),
  }),
  async execute({ city }) {
    return `Weather in ${city}: Sunny, 72°F`;
  },
});

const agent = new Agent({
  name: 'Weather Bot',
  instructions: 'Help with weather queries.',
  model: 'gpt-5-nano',
  tools: [getWeather],
});

const result = await run(agent, 'Weather in Tokyo?');
```

### Tool with Context

```typescript
import { Agent, tool, run, RunContext } from '@openai/agents';
import { z } from 'zod';

interface UserContext {
  userId: string;
  isAdmin: boolean;
}

const getUserData = tool({
  name: 'get_user_data',
  description: 'Get current user data',
  parameters: z.object({}),
  execute: async (_args, runContext?: RunContext<UserContext>) => {
    const ctx = runContext?.context;
    return `User: ${ctx?.userId}, Admin: ${ctx?.isAdmin}`;
  },
});

const agent = new Agent<UserContext>({
  name: 'User Bot',
  instructions: 'Help users with their data.',
  model: 'gpt-5-nano',
  tools: [getUserData],
});

const result = await run(agent, 'Show my data', {
  context: { userId: '123', isAdmin: true },
});
```

### Hosted Tools

Available hosted tools that run on OpenAI servers:

| Tool | Function | Purpose |
|------|----------|---------|
| Web Search | `webSearchTool()` | Internet search |
| File Search | `fileSearchTool('vector_store_id')` | Query vector stores |
| Computer Use | `computerTool()` | Automate GUI interactions |
| Code Interpreter | `codeInterpreterTool()` | Run code in sandbox |
| Image Generation | `imageGenerationTool()` | Generate images from text |

```typescript
import { Agent, webSearchTool, fileSearchTool, codeInterpreterTool } from '@openai/agents';

const agent = new Agent({
  name: 'Research Bot',
  instructions: 'Research and answer questions using web search.',
  model: 'gpt-5-nano',
  tools: [
    webSearchTool(),  // Internet search
    fileSearchTool('vs_your_vector_store_id'),  // Vector store search
    codeInterpreterTool(),  // Execute code
  ],
});
```

---

## Structured Output

```typescript
import { Agent, run } from '@openai/agents';
import { z } from 'zod';

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const agent = new Agent({
  name: 'Calendar Extractor',
  instructions: 'Extract calendar events from text.',
  model: 'gpt-5-nano',
  outputType: CalendarEvent,
});

const result = await run(agent, 'Meeting with John tomorrow at 3pm');
console.log(result.finalOutput); // { name: '...', date: '...', participants: [...] }
```

---

## Handoffs (Multi-Agent)

```typescript
import { Agent, run } from '@openai/agents';

const billingAgent = new Agent({
  name: 'Billing Agent',
  instructions: 'Handle billing questions.',
  model: 'gpt-5-nano',
});

const supportAgent = new Agent({
  name: 'Support Agent',
  instructions: 'Handle technical support.',
  model: 'gpt-5-nano',
});

// Use Agent.create for proper type inference with handoffs
const triageAgent = Agent.create({
  name: 'Triage Agent',
  instructions: `Route users to the right agent:
    - Billing questions -> Billing Agent
    - Technical issues -> Support Agent`,
  model: 'gpt-5-nano',
  handoffs: [billingAgent, supportAgent],
});

const result = await run(triageAgent, 'I have a billing question');
console.log(result.finalOutput);
console.log(`Handled by: ${result.lastAgent.name}`);
```

### Handoff with Input Filter

```typescript
import { Agent, handoff } from '@openai/agents';
import { removeAllTools } from '@openai/agents-core/extensions';

const specialistAgent = new Agent({
  name: 'Specialist',
  instructions: 'Handle specialized queries.',
  model: 'gpt-5-nano',
});

const handoffObj = handoff(specialistAgent, {
  toolNameOverride: 'transfer_to_specialist',
  toolDescriptionOverride: 'Transfer to specialist for complex issues',
  inputFilter: removeAllTools, // Filter conversation history
});
```

---

## Agents as Tools

Use an agent as a tool (keeps control with parent agent):

```typescript
import { Agent, run } from '@openai/agents';

const summarizer = new Agent({
  name: 'Summarizer',
  instructions: 'Create concise summaries.',
  model: 'gpt-5-nano',
});

const summarizerTool = summarizer.asTool({
  toolName: 'summarize',
  toolDescription: 'Summarize provided text.',
});

const mainAgent = new Agent({
  name: 'Research Assistant',
  instructions: 'Help with research tasks.',
  model: 'gpt-5-nano',
  tools: [summarizerTool],
});
```

---

## Guardrails

### Input Guardrail

```typescript
import { Agent, run, InputGuardrail, InputGuardrailTripwireTriggered } from '@openai/agents';
import { z } from 'zod';

const guardrailAgent = new Agent({
  name: 'Guardrail',
  instructions: 'Check if input is inappropriate.',
  model: 'gpt-5-nano',
  outputType: z.object({
    isInappropriate: z.boolean(),
    reason: z.string(),
  }),
});

const contentGuardrail: InputGuardrail = {
  name: 'Content Filter',
  execute: async ({ input, context }) => {
    const result = await run(guardrailAgent, input, { context });
    return {
      outputInfo: result.finalOutput,
      tripwireTriggered: result.finalOutput?.isInappropriate ?? false,
    };
  },
};

const agent = new Agent({
  name: 'Assistant',
  instructions: 'Help users.',
  model: 'gpt-5-nano',
  inputGuardrails: [contentGuardrail],
});

try {
  await run(agent, 'Some input');
} catch (e) {
  if (e instanceof InputGuardrailTripwireTriggered) {
    console.log('Guardrail tripped!');
  }
}
```

---

## Streaming

```typescript
import { Agent, run } from '@openai/agents';

const agent = new Agent({
  name: 'Storyteller',
  instructions: 'Tell engaging stories.',
  model: 'gpt-5-nano',
});

const result = await run(agent, 'Tell me a story', { stream: true });

// Stream text output
result.toTextStream({ compatibleWithNodeStreams: true }).pipe(process.stdout);

// Or listen to all events
for await (const event of result) {
  if (event.type === 'raw_model_stream_event') {
    console.log(event.data);
  }
}

await result.completed;
```

---

## Human in the Loop (Tool Approval)

```typescript
import { Agent, run, tool } from '@openai/agents';
import { z } from 'zod';
import readline from 'node:readline/promises';

const sensitiveTool = tool({
  name: 'delete_file',
  description: 'Delete a file',
  parameters: z.object({ filename: z.string() }),
  needsApproval: true, // Requires approval
  execute: async ({ filename }) => {
    return `Deleted ${filename}`;
  },
});

const agent = new Agent({
  name: 'File Manager',
  instructions: 'Manage files.',
  model: 'gpt-5-nano',
  tools: [sensitiveTool],
});

let result = await run(agent, 'Delete temp.txt');

while (result.interruptions?.length) {
  for (const interruption of result.interruptions) {
    const approved = await confirm(`Approve ${interruption.name}?`);
    if (approved) {
      result.state.approve(interruption);
    } else {
      result.state.reject(interruption);
    }
  }
  result = await run(agent, result.state);
}
```

---

## Context Management

### Dynamic Instructions

```typescript
import { Agent, RunContext } from '@openai/agents';

interface UserContext {
  name: string;
  language: string;
}

function buildInstructions(ctx: RunContext<UserContext>) {
  return `User: ${ctx.context.name}. Respond in ${ctx.context.language}.`;
}

const agent = new Agent<UserContext>({
  name: 'Personalized Bot',
  instructions: buildInstructions,
  model: 'gpt-5-nano',
});
```

---

## MCP (Model Context Protocol)

### Stdio MCP Server

```typescript
import { Agent, run, MCPServerStdio } from '@openai/agents';

const mcpServer = new MCPServerStdio({
  name: 'Filesystem',
  fullCommand: 'npx -y @modelcontextprotocol/server-filesystem ./files',
});

await mcpServer.connect();

const agent = new Agent({
  name: 'File Assistant',
  instructions: 'Help with files.',
  model: 'gpt-5-nano',
  mcpServers: [mcpServer],
});

try {
  const result = await run(agent, 'List files');
  console.log(result.finalOutput);
} finally {
  await mcpServer.close();
}
```

### Hosted MCP (Remote)

```typescript
import { Agent, hostedMcpTool } from '@openai/agents';

const agent = new Agent({
  name: 'Docs Assistant',
  instructions: 'Answer questions using docs.',
  model: 'gpt-5-nano',
  tools: [
    hostedMcpTool({
      serverLabel: 'docs',
      serverUrl: 'https://gitmcp.io/openai/codex',
    }),
  ],
});
```

---

## Runner Configuration

```typescript
import { Agent, Runner } from '@openai/agents';

const agent = new Agent({
  name: 'Assistant',
  instructions: 'Help users.',
  model: 'gpt-5-nano',
});

const runner = new Runner({
  model: 'gpt-5-nano', // Default model for all agents
  modelSettings: { temperature: 0.7 },
  workflowName: 'Customer Support',
  maxTurns: 15,
});

const result = await runner.run(agent, 'Hello');
```

---

## Conversation History

```typescript
import { Agent, run, user } from '@openai/agents';
import type { AgentInputItem } from '@openai/agents';

const agent = new Agent({
  name: 'Assistant',
  instructions: 'Be helpful.',
  model: 'gpt-5-nano',
});

let history: AgentInputItem[] = [];

async function chat(message: string) {
  history.push(user(message));
  const result = await run(agent, history);
  history = result.history;
  return result.finalOutput;
}

await chat('My name is Alice');
await chat('What is my name?'); // Will remember Alice
```

---

## Lifecycle Hooks

```typescript
import { Agent } from '@openai/agents';

const agent = new Agent({
  name: 'Verbose Agent',
  instructions: 'Be helpful.',
  model: 'gpt-5-nano',
});

agent.on('agent_start', (ctx, agent) => {
  console.log(`[${agent.name}] started`);
});

agent.on('agent_end', (ctx, output) => {
  console.log(`Agent produced: ${output}`);
});
```

---

## Voice/Realtime Agents

### Basic Voice Agent

```typescript
import { RealtimeAgent, RealtimeSession } from '@openai/agents/realtime';

const agent = new RealtimeAgent({
  name: 'Voice Assistant',
  instructions: 'Help users with voice queries.',
});

const session = new RealtimeSession(agent, {
  model: 'gpt-realtime',
});

// Connect with ephemeral key (browser/WebRTC)
await session.connect({
  apiKey: 'ek_...', // Ephemeral key from backend
});

// Or with API key (server/WebSocket)
await session.connect({
  apiKey: process.env.OPENAI_API_KEY!,
});
```

### Voice Agent with Tools

```typescript
import { RealtimeAgent, RealtimeSession, tool } from '@openai/agents/realtime';
import { z } from 'zod';

const getWeather = tool({
  name: 'get_weather',
  description: 'Get weather for a city',
  parameters: z.object({ city: z.string() }),
  execute: async ({ city }) => `Weather in ${city}: Sunny`,
});

const agent = new RealtimeAgent({
  name: 'Weather Voice Bot',
  instructions: 'Answer weather questions.',
  tools: [getWeather],
});

const session = new RealtimeSession(agent, { model: 'gpt-realtime' });
```

### Voice Agent Events

```typescript
session.on('audio', (event) => {
  // Handle audio output (WebSocket only)
});

session.on('audio_interrupted', () => {
  // User interrupted the agent
});

session.on('history_updated', (history) => {
  // Conversation history changed
});

session.on('tool_approval_requested', (ctx, agent, request) => {
  session.approve(request.approvalItem);
  // or session.reject(request.rawItem);
});
```

---

## Complete Multi-Agent Example

```typescript
import { Agent, run, tool } from '@openai/agents';
import { z } from 'zod';

// Tools
const searchOrders = tool({
  name: 'search_orders',
  description: 'Search customer orders',
  parameters: z.object({ query: z.string() }),
  execute: async ({ query }) => `Found orders matching: ${query}`,
});

const processRefund = tool({
  name: 'process_refund',
  description: 'Process a refund',
  parameters: z.object({ orderId: z.string(), reason: z.string() }),
  execute: async ({ orderId, reason }) => `Refund processed for ${orderId}`,
});

// Specialist agents
const orderAgent = new Agent({
  name: 'Order Specialist',
  instructions: 'Handle order inquiries and searches.',
  model: 'gpt-5-nano',
  tools: [searchOrders],
});

const refundAgent = new Agent({
  name: 'Refund Specialist',
  instructions: 'Handle refund requests professionally.',
  model: 'gpt-5-nano',
  tools: [processRefund],
});

// Triage agent with handoffs
const triageAgent = Agent.create({
  name: 'Customer Support',
  instructions: `You are the first point of contact for customers.
    - Order questions -> Order Specialist
    - Refund requests -> Refund Specialist
    - General questions -> Answer directly`,
  model: 'gpt-5-nano',
  handoffs: [orderAgent, refundAgent],
});

// Run the multi-agent system
async function main() {
  const result = await run(triageAgent, 'I want a refund for order #12345');
  console.log(`Response: ${result.finalOutput}`);
  console.log(`Handled by: ${result.lastAgent.name}`);
}

main();
```

---

## Best Practices

1. **Use `gpt-5-nano`** for most agents - it's fast and cost-effective
2. **Keep agents focused** - one responsibility per agent
3. **Use handoffs** for multi-domain tasks
4. **Add guardrails** for production safety
5. **Enable streaming** for better UX
6. **Use structured output** when you need typed responses
7. **Implement human-in-the-loop** for sensitive operations

## Error Handling

```typescript
import {
  run,
  MaxTurnsExceededError,
  InputGuardrailTripwireTriggered,
  ToolCallError
} from '@openai/agents';

try {
  const result = await run(agent, input);
} catch (e) {
  if (e instanceof MaxTurnsExceededError) {
    console.log('Too many turns');
  } else if (e instanceof InputGuardrailTripwireTriggered) {
    console.log('Guardrail blocked input');
  } else if (e instanceof ToolCallError) {
    console.log('Tool execution failed');
  }
}
```
