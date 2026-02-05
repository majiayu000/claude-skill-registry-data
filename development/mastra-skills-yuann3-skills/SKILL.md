---
name: mastra-skills
description: Use when building or working with Mastra agents - establishes best practices for agent development, tool creation, and workflow orchestration
---

# Mastra Skills

**Core principle:** Build composable, observable, and testable AI agents.

## When to Use This Skill

**Always use when:**
- Creating new Mastra agents
- Implementing agent tools
- Setting up workflows
- Debugging agent behavior
- Integrating external APIs with agents

**Don't use for:**
- Non-agent-related code
- Pure frontend components without agent interaction

## Documentation Quick Links

- **[reference.md](./reference.md)** - Official API documentation links
- **[examples.md](./examples.md)** - Official examples and how to use them
- **Official Mastra Docs** - https://mastra.ai/docs/

## Development Checklist

When creating a new agent, use TodoWrite to track:

- [ ] Define clear agent purpose and capabilities
- [ ] Identify required tools and integrations
- [ ] Plan observability and logging strategy
- [ ] Design agent memory and state management
- [ ] Consider error handling and fallbacks
- [ ] Write tests for key scenarios

## Essential Requirements

### Every Agent Must Have

1. **Clear purpose and instructions** - Specific, not generic
2. **Descriptive name** - Not 'agent1' or 'myAgent'
3. **Appropriate model selection** - Choose based on task complexity
4. **Explicit tool registration** - No implicit assumptions

### Every Tool Must Have

1. **Descriptive ID** - Clear what it does
2. **Clear description** - For the LLM to understand
3. **Zod schema validation** - Type-safe inputs
4. **Error handling** - Never let tools crash agents
5. **Logging** - For debugging and observability

### Every Workflow Must Have

1. **Clear trigger schema** - Validated inputs
2. **Proper step sequencing** - Sequential vs parallel
3. **Error handling** - In each step
4. **Observability hooks** - beforeAll/afterAll for logging

## Core Patterns

### Basic Agent

```typescript
import { Agent } from '@mastra/core';

const agent = new Agent({
  name: 'descriptive-name',
  instructions: 'Clear, specific instructions',
  model: {
    provider: 'ANTHROPIC',
    name: 'claude-sonnet-4-5',
  },
  tools: { /* ... */ },
});
```

📚 **More details:** [reference.md](./reference.md) | https://mastra.ai/docs/agents/

### Basic Tool

```typescript
import { z } from 'zod';

const tool = {
  id: 'descriptive-id',
  description: 'What this tool does',
  inputSchema: z.object({
    param: z.string().describe('Parameter description'),
  }),
  execute: async ({ context }) => {
    try {
      const result = await operation();
      return { success: true, data: result };
    } catch (error) {
      logger.error('Operation failed', { error, context });
      return { success: false, error: error.message };
    }
  },
};
```

📚 **More examples:** [examples.md](./examples.md) | https://mastra.ai/docs/tools/

### Basic Workflow

```typescript
import { Workflow } from '@mastra/core';

const workflow = new Workflow({
  name: 'workflow-name',
  triggerSchema: z.object({ input: z.string() }),
});

workflow
  .step({ id: 'step1', execute: async () => { /* ... */ } })
  .then({ id: 'step2', execute: async () => { /* ... */ } })
  .commit();
```

📚 **More examples:** [examples.md](./examples.md) | https://mastra.ai/docs/workflows/

## Red Flags - Stop If You See

- Agent without clear purpose
- Tools without input validation
- No error handling in tools
- Missing observability/logging
- Hardcoded credentials
- No rate limiting for external APIs
- Unbounded memory growth

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Agent instructions don't need to be specific" | Vague instructions → unpredictable behavior |
| "Error handling adds complexity" | Unhandled errors → crashed agents |
| "We can add observability later" | Can't debug what you can't observe |
| "Tool schemas are optional" | Invalid inputs → runtime failures |

## Integration Checklist

When integrating external services, use TodoWrite to track:

- [ ] Create typed tool interface
- [ ] Add input validation with Zod
- [ ] Implement error handling
- [ ] Add logging for debugging
- [ ] Consider rate limiting
- [ ] Handle authentication securely
- [ ] Test with edge cases
- [ ] Document tool usage

## Testing Requirements

```typescript
// Unit test for tools
describe('myTool', () => {
  it('should handle valid input', async () => {
    const result = await myTool.execute({
      context: { param: 'test' },
      mastra: mockMastra,
    });
    expect(result.success).toBe(true);
  });
});

// Integration test for agents
describe('myAgent', () => {
  it('should respond to queries', async () => {
    const response = await myAgent.generate([
      { role: 'user', content: 'test query' }
    ]);
    expect(response.role).toBe('assistant');
  });
});
```

📚 **More examples:** [examples.md](./examples.md)

## Quick Workflow

1. **Need API details?** → Check [reference.md](./reference.md)
2. **Need examples?** → Check [examples.md](./examples.md)
3. **Building something?** → Follow checklists above, use TodoWrite
4. **Stuck?** → Check official docs at https://mastra.ai/docs/

## Final Rule

```
Every agent must have:
1. Clear purpose and instructions
2. Type-safe tools with validation
3. Error handling and observability
4. Tests covering key scenarios
```

Follow these principles for reliable, maintainable Mastra agents.
