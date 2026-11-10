---
name: tools-and-structured-output
description: Writes and fixes Vercel AI SDK (npm package `ai`, version 7) code for tool calling, multi-step tool loops, agents and structured output, and tests it with the SDK's mock models. Use when code imports from 'ai' or 'ai/test' and calls generateText, streamText, tool(), ToolLoopAgent, Output.object, generateObject, stopWhen/isStepCount, or MockLanguageModelV4; when adding tools or an agent loop to a chatbot; when extracting typed JSON from an LLM; when persisting chat history with tool calls; or when upgrading from AI SDK 4, 5 or 6 (parameters, maxSteps, maxTokens, experimental_context, response.messages, system messages).
license: MIT
---

# AI SDK 7: tools, loops and structured output

Checked against `ai@7.0.159` (October 2026) with `zod@4.6.7`. AI SDK 7 is ESM-only and needs Node 22+.

Most AI SDK mistakes do not throw. Old option names from v4-v6 are silently ignored, so the code
"works" with a real model and quietly does less: the loop stops after one step, the model never
sees the tool's schema, the token cap is not applied, persisted history loses the tool calls. Treat
everything below as rules, and prove the behaviour with a mock-model test before calling it done.

## First, find out what is installed

1. Read `package.json` and `node_modules/ai/package.json` for the real version. Everything here is
   for 7.x. If the project is on 5 or 6, see [the migration table](references/migration-v4-to-v7.md)
   for what differs, and do not "upgrade" APIs the installed version does not have.
2. The `ai` package ships its own docs for the exact installed version in `node_modules/ai/docs/`
   (MDX). When unsure about an option, grep there before guessing:
   `grep -rn "toolsContext" node_modules/ai/docs/`.
3. Run the project's type check (`npx tsc --noEmit`) after every change. In 7.x it reports
   `parameters`, `maxSteps`, `maxTokens`, `experimental_context`, `toolCall.args` and
   `usage.promptTokens` as errors. It does **not** catch the two worst runtime problems: system
   messages inside `messages`, and reading `result.response.messages` after a multi-step run.

## The rules that silently break

| Write this (7.x) | Not this | What the old form does in 7.0.159 |
| --- | --- | --- |
| `tool({ inputSchema: z.object(...) })` | `parameters:` | Ignored. The model receives an empty `{ properties: {} }` schema and input is not validated. |
| `stopWhen: isStepCount(n)` on `generateText`/`streamText` | `maxSteps: n`, or nothing | Ignored. Default is one step: the tool runs, then the call returns with `text === ''`. |
| `maxOutputTokens: n` | `maxTokens: n` | Ignored. No cap is sent to the provider. |
| `instructions: '...'` | `{ role: 'system' }` inside `messages`/`prompt` | Throws `InvalidPromptError` ("System messages are not allowed..."). `system:` still works as a deprecated alias. |
| `result.responseMessages` to persist a turn | `result.response.messages` | Holds only the **final step's** messages; earlier tool calls and results are dropped. |
| per-request closure, or `contextSchema` + `toolsContext` | `experimental_context` | Not passed. The tool's `context` is `undefined`, so `experimental_context.accountId` throws inside the tool. |
| `output: Output.object({ schema })`, read `result.output` | `experimental_output` | Removed: ignored, no JSON response format is requested, `result.experimental_output` is `undefined`. |
| `toolCall.input`, `toolResult.output` | `.args`, `.result` | `undefined`. |
| `usage.inputTokens`, `usage.outputTokens` | `promptTokens`, `completionTokens` | `undefined`. |

Deprecated in 7.x but still working (fine to leave, prefer the new name in new code):
`stepCountIs` (alias of `isStepCount`), `system` (use `instructions`), `generateObject`/`streamObject`
(use `generateText`/`streamText` with `output`), `totalUsage` (use `usage`), `fullStream` (use
`stream`), `onFinish`/`onStepFinish` (use `onEnd`/`onStepEnd`), `needsApproval` on a tool (use
`toolApproval` on the call), `Experimental_Agent` (alias of `ToolLoopAgent`).

## Result shapes changed in 7.0: whole run vs final step

On a `generateText` result (and awaited `streamText` promises):

- **Whole run, all steps:** `text` is the final text, but `toolCalls`, `toolResults`, `content`,
  `files`, `sources`, `warnings`, `usage` and `responseMessages` accumulate across every step.
  In v5/v6, `toolCalls`, `toolResults` and `usage` were final-step only.
- **Final step only:** `result.finalStep.*` (`finishReason`, `toolCalls`, `usage`, `response`,
  `providerMetadata`, `reasoningText`). The top-level `response`, `request`, `reasoning*` and
  `providerMetadata` are deprecated aliases of the final step.
- **Per step:** `result.steps[i]`, where `step.response.messages` is that step's messages only.

Did the loop end without an answer? The step limit was hit while the model still wanted tools when
`result.finalStep.finishReason === 'tool-calls'` (and `result.text` is empty). Handle that case
explicitly; never return an empty string to a user.

## Tools

```ts
import { generateText, isStepCount, tool, type LanguageModel } from 'ai'
import { z } from 'zod'

export function flightTools(board: DepartureBoard, accountId: string) {
  return {
    getFlightStatus: tool({
      description: 'Gate and departure time of a flight on one of the traveller\'s bookings.',
      inputSchema: z.object({
        flightNumber: z.string().regex(/^[A-Z0-9]{2}\d{1,4}$/).describe('IATA flight number, e.g. TP1351'),
      }),
      execute: async ({ flightNumber }) => {
        const flight = await board.lookup(accountId, flightNumber)
        if (!flight) return { known: false, flightNumber }
        return { known: true, flightNumber, gate: flight.gate ?? null, departsAt: flight.departsAt }
      },
    }),
  }
}

const result = await generateText({
  model,
  instructions: TRAVEL_DESK_PROMPT,
  prompt: travellerQuestion,
  tools: flightTools(board, session.accountId),
  stopWhen: isStepCount(3), // at most 3 model calls; without it you get exactly 1
})
```

Decision rules:

- **Authorization data never comes from the model.** Account, workspace and permission values are
  bound in code: build tools per request in a closure (as above), or declare `contextSchema` on the
  tool and pass values through `toolsContext: { toolName: {...} }` on the call. Do not add
  `accountId` or `workspaceId` to `inputSchema`. Unknown keys the model sends are stripped by `z.object`.
- **Validate input in the schema**, not in `execute`. Invalid input never reaches `execute`: the SDK
  turns it into a `tool-error` result that is sent back to the model, and the loop continues.
- **Return expected failures as data** (`{ known: false }`) so the model can explain them. A thrown
  error inside `execute` also becomes a `tool-error` part the model sees, not an exception from
  `generateText`; throw only for genuinely unexpected failures.
- **Return small, JSON-serialisable results.** Everything you return is sent back to the model.
- **Pick the step budget deliberately.** `isStepCount(n)` counts model calls. One tool round plus an
  answer is 2. Structured `output` combined with tools needs a step for the final object too.
  `ToolLoopAgent` defaults to `isStepCount(20)`; `generateText`/`streamText` default to 1.
- Other stop conditions: `hasToolCall('finalAnswer')`, `isLoopFinished()`, or an array of
  conditions (any one stops the loop). Conditions are checked only after steps that have tool results.
- Several tool calls in one step run concurrently. Use `toolCallConcurrency: 1` when they must see
  each other's side effects.
- Human sign-off for dangerous tools: `toolApproval: { wireTransfer: ({ cents }) => (cents > 50_000 ? 'user-approval' : undefined) }`
  on the call. The call then returns `tool-approval-request` parts instead of executing; see
  [agents and context](references/agents-and-context.md#approvals).

## Agents and conversations

Use `generateText`/`streamText` with `stopWhen` for a single request handler. Use `ToolLoopAgent`
when the same configuration (model, instructions, tools, stop condition) is reused across call
sites; it exposes `agent.generate({ prompt | messages })` and `agent.stream(...)` and returns the
same result shape. Details, `prepareStep`, `runtimeContext` and `callOptionsSchema`:
[agents and context](references/agents-and-context.md).

Persisting a multi-turn chat that uses tools:

```ts
const latest: ModelMessage = { role: 'user', content: chatInput }
const result = await generateText({
  model,
  instructions: CONCIERGE_PROMPT,
  // 7.x rejects system messages here. Threads saved by older code often start with one: drop it.
  messages: [...priorTurns.filter((m) => m.role !== 'system'), latest],
  tools: travelTools,
  stopWhen: isStepCount(8),
})
await threads.save(threadId, [latest, ...result.responseMessages]) // all steps, in order
```

`allowSystemInMessages: true` restores the old behaviour, but only use it when every message is
server-authored: if users can submit or edit history, they can inject a system prompt.

`ModelMessage` is the message type (`CoreMessage` was removed in v6). For UI messages from
`useChat`, convert with `await convertToModelMessages(uiMessages)` (async since v6).

## Structured output

```ts
import { generateText, NoObjectGeneratedError, Output } from 'ai'

const receiptSchema = z.object({
  merchant: z.string().min(1),
  purchasedOn: z.iso.date(),
  returnBy: z.iso.date().nullable(),             // nullable, not optional: providers want every key
  countryCode: z.string().regex(/^[A-Z]{2}$/),   // ISO 3166-1 alpha-2
  amountPaid: z.number().nonnegative(),
})

type ParsedReceipt =
  | { ok: true; receipt: z.infer<typeof receiptSchema> }
  | { ok: false; llmText: string | undefined; problem: unknown }

async function parseReceipt(model: LanguageModel, ocrText: string): Promise<ParsedReceipt> {
  try {
    const { output } = await generateText({
      model,
      prompt: ocrText,
      output: Output.object({ name: 'Receipt', schema: receiptSchema }),
      maxOutputTokens: 600,
    })
    return { ok: true, receipt: output } // typed and validated
  } catch (error) {
    // error.text = raw model text, error.cause = parse/validation error, plus error.response, error.usage
    if (NoObjectGeneratedError.isInstance(error)) return { ok: false, llmText: error.text, problem: error.cause }
    throw error
  }
}
```

- `Output.object`, `Output.array({ element, minItems, maxItems })`, `Output.choice({ options })`,
  `Output.json()`, `Output.text()` (the default). The SDK sends a JSON response format with the
  schema to providers that support it and validates the result itself either way.
- Invalid or unparseable output rejects with `NoObjectGeneratedError`. Reading `result.output` when
  the final step did not finish with `stop` (for example it ended on tool calls) throws
  `NoOutputGeneratedError`; `output` is a getter, so destructuring triggers it too.
- Streaming: `streamText({ output })` gives `partialOutputStream` (unvalidated partials),
  `elementStream` for `Output.array` (each element complete and validated) and `await result.output`.
  `streamText` does not throw: errors go to `onError` and the awaited promises reject.
- Prefer `.nullable()` over `.optional()` and give fields `.describe()` hints. More, including
  combining tools with structured output: [structured output](references/structured-output.md).

## Testing without a provider

`ai/test` exports `MockLanguageModelV4` (V2 mocks are gone; V3 still exists for v3 providers).
Inject the model as a parameter so tests can pass a mock. Usage and finish reasons are nested
objects in the v4 model spec:

```ts
import { MockLanguageModelV4 } from 'ai/test'

const usage = {
  inputTokens: { total: 10, noCache: 10, cacheRead: undefined, cacheWrite: undefined },
  outputTokens: { total: 5, text: 5, reasoning: undefined },
}
const model = new MockLanguageModelV4({
  doGenerate: [
    {
      content: [{ type: 'tool-call', toolCallId: 'call-a', toolName: 'getFlightStatus', input: '{"flightNumber":"TP1351"}' }],
      finishReason: { unified: 'tool-calls', raw: undefined },
      usage,
      warnings: [],
    },
    { content: [{ type: 'text', text: 'Boarding at gate 14.' }], finishReason: { unified: 'stop', raw: undefined }, usage, warnings: [] },
  ],
})
// ...run the code under test, then assert on what the model was sent:
model.doGenerateCalls[0].tools          // tool schemas (catches `parameters`)
model.doGenerateCalls[1].prompt         // the tool result went back to the model
model.doGenerateCalls[0].maxOutputTokens, model.doGenerateCalls[0].responseFormat
```

Gotchas: tool-call `input` is a JSON **string**; an exhausted `doGenerate` array crashes with a
TypeError, so use a function (`doGenerate: async (options) => ...`) for "model never stops" tests;
`streamText` calls `doStream`, not `doGenerate`. Full helpers and a reusable mock that serves both:
[testing](references/testing.md).

## Done checklist

- [ ] Every `tool()` uses `inputSchema`; account and workspace ids are bound in code, not model input.
- [ ] Every tool-using `generateText`/`streamText` has an explicit `stopWhen`; the step-limit case
      (`finalStep.finishReason === 'tool-calls'`) is handled.
- [ ] System prompt is `instructions`; stored histories are stripped of `system` messages.
- [ ] Persisted turns use `result.responseMessages`; counts and usage read the whole-run fields.
- [ ] Token caps use `maxOutputTokens`; structured output uses `output: Output.*` and handles
      `NoObjectGeneratedError`.
- [ ] `tsc --noEmit` is clean and a mock-model test covers a two-step tool run and the failure path.

Anti-patterns with fixes, side by side: [migration table](references/migration-v4-to-v7.md).
Sources: [references/sources.md](references/sources.md).
