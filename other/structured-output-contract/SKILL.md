---
name: structured-output-contract
description: Use whenever an LLM's output is consumed by code (parsed, stored, or dispatched) — define a JSON Schema and enforce it with constrained decoding or strict tool-use, instead of prompt-and-hope plus regex parsing.
stacks: [python, node]
domains: [web, data]
phases: [dev]
tags: [llm, structured-output, json-schema, constrained-decoding, tool-use, outlines]
scope: kit
---
**When to use.** Any machine-consumed model output. *Why:* free-text parsing breaks in production;
constrained decoding to a schema is ~100% valid vs 95–99% for plain function-calling.

**Procedure.**
1. Write the JSON Schema / Pydantic model. Set `additionalProperties: false`; make optional fields nullable-and-required.
2. Enforce it: native strict structured output (Anthropic/OpenAI) or constrained decoding (Outlines/XGrammar) for open models — not post-hoc regex.
3. Add a validate-then-retry layer for the residual failures.
4. **Done when:** a malformed-output test can't get past the boundary (schema rejects it), demonstrated with a pasted failing-then-passing run.

**Knowledge:** KNOWLEDGE-LIBRARY.md §A3. **Example:** the Outlines snippet there.
