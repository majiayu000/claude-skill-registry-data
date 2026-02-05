---
name: output-meta-project-context
description: Comprehensive guide to Output.ai Framework for building durable, LLM-powered workflows orchestrated by Temporal. Covers project structure, workflow patterns, steps, LLM integration, HTTP clients, and CLI commands.
allowed-tools: [Read]
---

# Output.ai Based Project Guide

## Overview

This project uses Output Framework to build durable, LLM-powered workflows orchestrated by Temporal. Output Framework provides abstractions for creating reliable AI workflows with automatic retry, tracing, and error handling. Developers use it to build workflows like fact checkers, content generators, data extractors, research assistants, and multi-step AI agents.

### Project Overview

Each workflow lives in its own folder under `src/workflows/` and follows a consistent structure. Workflows define the orchestration logic, calling steps to perform external operations like API calls, database queries, and LLM inference. The system automatically handles retries, timeouts, and distributed execution through Temporal.

### Key Concepts

#### Built on Top of Temporal

Temporal provides durable execution guarantees - if a workflow fails mid-execution, it resumes from the last successful step rather than restarting. Output Framework wraps Temporal's workflow and activity primitives with higher-level abstractions (`workflow`, `step`, `evaluator`) that enforce best practices and provide automatic tracing.

#### Single Folder Project Structure

Each workflow is self-contained in a single folder with a predictable structure: `workflow.ts` contains the deterministic orchestration logic, `steps.ts` contains I/O operations (API calls, LLM inference), `evaluators.ts` contains analysis logic returning confidence-scored results, and `prompts/*.prompt` files define LLM prompts using Liquid.js templates with YAML frontmatter for model configuration.

## Critical Conventions

- **HTTP**: Never use axios - use `@output.ai/http` (traced, auto-retry)
- **LLM**: Never call LLM APIs directly - use `@output.ai/llm`
- **Workflows**: Must be deterministic - only call steps/evaluators, no direct I/O
- **Steps**: All external operations (APIs, DBs, LLMs) must be wrapped in steps
- **Schemas**: Use Zod (`z`) from `@output.ai/core` to define input/output schemas

## Project Structure

```
src/workflows/{name}/
  workflow.ts          # Orchestration logic (deterministic)
  steps.ts             # I/O operations (APIs, LLM, DB)
  evaluators.ts        # Analysis steps returning EvaluationResult
  prompts/*.prompt             # LLM prompts (name@v1.prompt)
  scenarios/*.json             # Test scenarios
```

## Commands

```bash
npx output dev                                      # Start dev (Temporal:8080, API:3001)
npx output workflow list                            # List workflows

# Sync execution (waits for result)
npx output workflow run <name> --input <JSON|JSON_FILE>      # Execute and wait

# Async execution
npx output workflow start <name> --input <JSON|JSON_FILE>    # Start workflow, returns ID
npx output workflow status <workflowId>             # Check execution status
npx output workflow result <workflowId>             # Get result when complete
npx output workflow stop <workflowId>               # Cancel running workflow
```

## Workflow Pattern

Workflows orchestrate steps. They must be deterministic (no direct I/O).

```typescript
import { workflow, z } from '@output.ai/core';
import { processData, callApi } from './steps.js';

export default workflow({
  name: 'my-workflow',
  description: 'What this workflow does',
  inputSchema: z.object({ query: z.string() }),
  outputSchema: z.object({ result: z.string() }),
  fn: async (input) => {
    const data = await processData(input);
    const result = await callApi(data);
    return { result };
  }
});
```

**Allowed imports**: steps.ts, evaluators.ts, shared_steps.ts, types.ts, consts.ts, utils.ts

**Forbidden in workflows**: Direct API calls, Math.random(), Date.now(), dynamic imports

## Step Pattern

Steps contain all I/O operations. They are automatically retried on failure.

```typescript
import { step, z } from '@output.ai/core';
import { httpClient } from '@output.ai/http';

const client = httpClient({ prefixUrl: 'https://api.example.com' });

export const fetchData = step({
  name: 'fetchData',
  description: 'Fetch data from external API',
  inputSchema: z.object({ id: z.string() }),
  outputSchema: z.object({ data: z.any() }),
  fn: async ({ id }) => {
    const response = await client.get(`items/${id}`).json();
    return { data: response };
  },
  options: {
    retry: { maximumAttempts: 3 }
  }
});
```

## LLM Pattern

Use `@output.ai/llm` for all LLM operations. Prompts are defined in `.prompt` files.

**Prompt file** (`summarize@v1.prompt`):
```yaml
---
provider: anthropic
model: claude-sonnet
temperature: 0.7
maxTokens: 2000
---
<system>You are a helpful assistant.</system>
<user>Summarize: {{ content }}</user>
```

**Step using prompt**:
```typescript
import { step, z } from '@output.ai/core';
import { generateText, generateObject } from '@output.ai/llm';

export const summarize = step({
  name: 'summarize',
  inputSchema: z.object({ content: z.string() }),
  outputSchema: z.string(),
  fn: async ({ content }) => {
    return generateText({
      prompt: 'summarize@v1',
      variables: { content }
    });
  }
});

// For structured output
export const extractInfo = step({
  name: 'extractInfo',
  inputSchema: z.object({ text: z.string() }),
  outputSchema: z.object({ title: z.string(), summary: z.string() }),
  fn: async ({ text }) => {
    return generateObject({
      prompt: 'extract@v1',
      variables: { text },
      schema: z.object({ title: z.string(), summary: z.string() })
    });
  }
});
```

**Available functions**: `generateText`, `generateObject`, `generateArray`, `generateEnum`

**Providers**: anthropic, openai, azure

## HTTP Pattern

Use `@output.ai/http` for traced HTTP requests with automatic retry.

```typescript
import { httpClient } from '@output.ai/http';

const client = httpClient({
  prefixUrl: 'https://api.example.com',
  timeout: 30000,
  retry: { limit: 3 }
});

// In a step:
const data = await client.get('endpoint').json();
const result = await client.post('endpoint', { json: payload }).json();
```

## Evaluator Pattern

Evaluators analyze data and return confidence-scored results.

```typescript
import { evaluator, EvaluationStringResult } from '@output.ai/core';

export const judgeQuality = evaluator({
  name: 'judgeQuality',
  inputSchema: z.string(),
  fn: async (content) => {
    // Analysis logic
    return new EvaluationStringResult({
      value: 'good',
      confidence: 0.95
    });
  }
});
```

## Error Handling

```typescript
import { FatalError, ValidationError } from '@output.ai/core';

// Non-retryable error (workflow fails immediately)
throw new FatalError('Critical failure - do not retry');

// Validation error (input/output schema failure)
throw new ValidationError('Invalid input format');
```

## Sub-Agents

For workflow planning and implementation:
- workflow-planner: `.claude/agents/workflow_planner.md` - Workflow architecture specialist
- workflow-quality: `.claude/agents/workflow_quality.md` - Workflow quality and best practices specialist
- workflow-prompt-writer: `.claude/agents/workflow_prompt_writer.md` - Prompt file creation and review specialist
- workflow-context-fetcher: `.claude/agents/workflow_context_fetcher.md` - Efficient context retrieval (used by other agents)
- workflow-debugger: `.claude/agents/workflow_debugger.md` - Workflow debugging specialist

## Commands

For workflow planning and implementation:
- /plan_workflow: `.claude/commands/plan_workflow.md` - Planning command
- /build_workflow: `.claude/commands/build_workflow.md` - Implementation command
- /debug_workflow: `.claude/commands/debug_workflow.md` - Debugging command

## Configuration

See `.env` file for required environment variables (API keys, etc.)
