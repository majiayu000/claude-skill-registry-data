---
name: genkit-architect
description: Expert guidance on building AI features with Google Genkit (v1.21.0+)
---

# Genkit Architect

This skill provides patterns and best practices for implementing Genkit flows, models, and tools.

## Folder Structure (Backend)

Recommended structure for a Node.js/Express app:

```text
backend/
├── src/
│   ├── flows/              # Define flows here
│   │   ├── email-classifier.ts
│   │   └── rfq-extraction.ts
│   ├── genkit.config.ts    # Main configuration
│   └── index.ts            # App entry point
```

## 1. Defining a Flow

Use `defineFlow` with Zod schemas for strict type safety.

```typescript
// src/flows/my-flow.ts
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';
import { generate } from '@genkit-ai/ai';
import { googleAI, gemini15Flash } from '@genkit-ai/googleai';

export const myFlow = defineFlow(
  {
    name: 'myFlow',
    inputSchema: z.object({ topic: z.string() }),
    outputSchema: z.object({ advice: z.string() }),
  },
  async (input) => {
    const llmResponse = await generate({
      model: gemini15Flash,
      prompt: `Give advice about ${input.topic}`,
      config: { temperature: 0.7 },
    });

    return { advice: llmResponse.text() };
  }
);
```

## 2. Configuration (`genkit.config.ts`)

```typescript
import { configureGenkit } from '@genkit-ai/core';
import { googleAI } from '@genkit-ai/googleai';
import { dotprompt } from '@genkit-ai/dotprompt';

export default configureGenkit({
  plugins: [
    googleAI(),
    dotprompt(),
  ],
  logLevel: 'debug',
  enableTracingAndMetrics: true,
});
```

## 3. Invoking Flows

Inside your Express routes or services:

```typescript
import { runFlow } from '@genkit-ai/flow';
import { myFlow } from './flows/my-flow';

const result = await runFlow(myFlow, { topic: "Node.js" });
console.log(result.advice);
```

## Best Practices
1.  **Zod Everything**: Always define input/output schemas. Genkit uses them to validate LLM output.
2.  **Separate Prompts**: Use Dotprompt (`.prompt` files) for complex prompts to keep code clean.
3.  **Error Handling**: Wrap `runFlow` in try/catch. Genkit throws structured errors.
4.  **Tracing**: Enbale tracing in dev to debug flow modifications.
