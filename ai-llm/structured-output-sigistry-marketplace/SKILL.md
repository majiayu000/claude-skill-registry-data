---
name: structured-output
description: This skill should be used when the user mentions "structured output", "json mode", "tool schema", "function calling", "json parse error", "response_format", "pydantic ai", "invalid json from the model", or "the model's JSON keeps breaking". It provides a methodology for getting reliably valid, schema-conformant structured output from LLMs across providers, plus a validate-and-retry fallback.
---

# Structured Output

## Purpose
Standardize how an LLM app gets machine-readable output it can trust. Asking a model for JSON in the prompt and calling `JSON.parse` / `json.loads` on the result fails on a non-trivial fraction of calls, a stray markdown fence, a trailing comma, a hallucinated field, an unescaped quote, and those failures surface as production exceptions on a code path that "worked in testing." Provider-native structured output (schema-constrained decoding or strict tool schemas) drops the invalid-output rate by one to two orders of magnitude. This skill gives the decision order: use the strongest native mechanism the provider offers, validate every response against a schema, and wrap it in a bounded retry-with-error-feedback loop.

## The reliability ladder (strongest first)
1. **Schema-constrained output**: the provider constrains decoding to your JSON Schema, *guaranteeing* the response validates. Anthropic `output_config.format` (`json_schema`), OpenAI `response_format: json_schema` with `strict: true`, Gemini/Vertex `responseSchema`. Use this whenever the model supports it.
2. **Strict tool / function schema**: when the value is really an argument to an action, route it through a tool with `strict: true` and `additionalProperties: false`. The provider validates the tool input against the schema.
3. **Bare JSON mode**: `{"type": "json_object"}` / "json" mode guarantees *syntactically* valid JSON but **not** your schema. Only acceptable with validation + retry on top.
4. **Prompt-and-pray**: "respond only with JSON" and hope. Never rely on this; it is the pattern this skill exists to replace.

Always add layers 1–3 with the validate-and-retry loop below, native constraints can still be interrupted by a length cap or a refusal.

## The non-negotiable pair: validate, then retry with feedback
Even with native constraints, parse defensively:
1. **Define the schema once** (Zod / Pydantic / JSON Schema) and reuse it for both the request constraint and the response check.
2. **Validate** every response against it, never trust a raw parse.
3. On a validation failure, **retry a bounded number of times**, feeding the *validator's error message* back into the next request ("your previous output failed validation: <error>; return output matching the schema"). This self-correction recovers most transient failures.
4. **Cap the attempts** and surface a typed failure when exhausted, an unbounded correction loop is a cost and latency hazard.

## Anti-patterns to replace
| Anti-pattern | Why it breaks | Replace with |
|---|---|---|
| `JSON.parse(resp)` right after a completion | No schema check; throws on any malformation | Native schema output + validated parse |
| `re.search(r"\{.*\}", text)` / strip ```` ```json ```` fences | Regex can't parse nested/escaped JSON; brittle | Native structured output; stop asking for fenced JSON |
| Bare `json_object` mode with no schema | Valid JSON, wrong shape | Schema-constrained output, or JSON mode + validate + retry |
| `data["field"]` straight off the parse | KeyError when the field is missing/renamed | Validate into a typed model, then access |
| Prompt-only "return JSON" | Highest failure rate | The reliability ladder above |

## Cross-cutting cautions
- **Model support varies**: schema-constrained output is only on certain models/tiers per provider. If the detected model lacks it, drop to JSON mode + validate + retry and say so; don't claim a capability the model doesn't have.
- **Schema feature limits**: providers reject or ignore parts of JSON Schema (recursion, numeric/length constraints, `additionalProperties` other than `false`). Keep schemas flat and closed; validate the unsupported constraints client-side.
- **Composition**: structured output can conflict with other features (e.g. citations, prefilling) per provider. Check before assuming it composes.

## Additional Resources
### Reference Files
- **`references/structured-output-apis.md`**: the native structured-output / tool-schema API for each provider (Anthropic tool use + `output_config.format`, OpenAI `response_format` json_schema, Gemini/Vertex `responseSchema`, Vercel AI SDK `generateObject`, Pydantic AI `result_type`), which models guarantee valid output, and the schema-feature limits per provider.
- **`references/validate-and-retry.md`**: the schema-validation + retry-with-error-feedback loop in Zod and Pydantic, why regex/`JSON.parse` extraction is fragile, and how to make retries cheap and bounded.
