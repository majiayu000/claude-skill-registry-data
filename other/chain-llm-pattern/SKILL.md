---
name: chain-llm-pattern
description: Build multi-step LLM reasoning chains in n8n using Groq, OpenAI, or Claude for structured data extraction, categorization, scoring, and analysis. Use this skill whenever the user wants to chain multiple LLM calls together in an n8n workflow — phrases like "extract entities then categorize", "multi-step LLM prompt", "chain_llm", "LLM pipeline", "classify and score", "entity extraction then enrichment". Also use when processing call transcripts, customer messages, or any unstructured text through multiple analysis passes in n8n. Prefer this pattern over single-shot prompts whenever the output requires both extraction AND reasoning, since single-shot hallucinates categories while chains let each step verify the previous.
---

# Chain LLM Pattern for n8n

Multi-step LLM chains outperform single-shot prompts on any task that combines extraction + reasoning. This skill encodes the production pattern.

## When to use a chain vs a single prompt

| Single prompt works | Chain is better |
|---|---|
| "Summarize this email" | "Extract entities, then categorize by urgency, then decide routing" |
| "Translate this to English" | "Detect language, translate, then extract structured fields" |
| "Is this spam? yes/no" | "Score spam probability from email, phone, IP, content separately, then combine" |

Rule of thumb: if the task has ≥2 distinct reasoning steps OR the final decision depends on intermediate structured data, use a chain.

## The pattern (3-stage default)

```
Input → [Extract] → [Analyze/Classify] → [Score/Decide] → Output
```

Each stage is its own LLM node with its own prompt. Between stages, use `Set` or `Code` nodes to transform and validate.

### Stage 1: Extract (schema-bound)

Use **`Information Extractor`** node (LangChain). NOT a generic `AI Agent` or raw HTTP call.

Why: `Information Extractor` binds output to a JSON schema. It parses, retries on invalid JSON, and fails loudly — instead of silently returning prose you then regex.

Define schema explicitly:

```json
{
  "type": "object",
  "properties": {
    "customer_name": { "type": "string" },
    "product_mentioned": { "type": "string" },
    "sentiment": { "enum": ["positive", "neutral", "negative"] },
    "urgency_score": { "type": "number", "minimum": 0, "maximum": 10 }
  },
  "required": ["customer_name", "sentiment"]
}
```

System prompt for this stage: short, one job. "Extract the fields defined in the schema from the transcript. If a field is absent, omit it. Do not infer or guess."

### Stage 2: Analyze (reason over extracted data)

Use **`Basic LLM Chain`** with the extracted JSON from Stage 1 as input.

This stage reasons: categorize, cluster, identify patterns, detect issues. The input is structured (from Stage 1) so the model isn't juggling parsing + reasoning simultaneously.

Example system prompt:
> Given the extracted customer data below, classify into one of: [technical_issue, billing_question, cancellation_risk, upsell_opportunity]. Then identify the single most important next action. Return JSON with `category` and `next_action`.

### Stage 3: Score / decide (deterministic where possible)

If the final step is arithmetic (e.g., composite scoring: 0.4 × email_score + 0.3 × phone_score + 0.3 × content_score), use a **`Code` node**, NOT an LLM.

LLMs are bad at arithmetic. They fail silently. Use `Code` (JavaScript) for any math involving weights, thresholds, or aggregation.

## Model selection

| Stage | Recommended model | Why |
|---|---|---|
| Extract | Groq `llama-3.3-70b-versatile` or `openai/gpt-4o-mini` | Fast, cheap, good at schema adherence |
| Analyze | Claude Sonnet 4 or GPT-4o | Reasoning quality matters more |
| Score (if LLM) | `gpt-4o-mini` | Arithmetic weakness, keep cheap |

Groq is the fastest provider for extract stages — 500+ tokens/sec. Use it unless you need Claude/OpenAI specifically.

## Production rules

1. **Pin example data at each stage during development.** Right-click node → "Pin Data". Without pinning, changing Stage 1 invalidates all downstream test data and you waste API calls.

2. **Budget tokens explicitly.** Set `maxTokens` on every LLM node. Stage 1 extract rarely needs >500. Stage 2 analyze rarely >1000.

3. **Validate between stages.** Insert a `Code` node between LLM stages that checks required fields exist. Fail fast with a clear error — don't let a missing field propagate and produce a confusing Stage 3 failure.

4. **Log stage outputs.** Add a `MySQL` or `Google Sheets` insert after Stage 1 and Stage 2 that records the raw output (truncated to 1000 chars). You WILL need this for debugging.

5. **Temperature: 0 for extract, 0.2–0.4 for analyze, 0 for scoring.** Extract must be deterministic. Analysis benefits from slight variance. Scoring must be deterministic.

## Common multi-language variant (EN/ES/PT)

For transcripts in mixed languages, add a Stage 0:

```
Stage 0 (Groq): Detect language → route to language-specific prompts
Stage 1 (language-specific): Extract in source language
Stage 2: Translate structured output to English (cheap, short)
Stage 3: Analyze in English
```

Language-specific prompts extract better than a single multilingual prompt because entity names (cities, products) follow different patterns per language.

## Anti-patterns

- **Don't use `AI Agent` for extraction.** Agents are for tool use, not structured output. Use `Information Extractor`.
- **Don't concatenate all steps into one mega-prompt.** Each hallucination compounds. Separate stages let you evaluate each independently.
- **Don't loop an LLM on retry without a counter.** Infinite loops cost money. Cap retries at 3 via a counter in a `Set` node.

## Reference

- `references/groq-chain-example.json` — a working 4-node chain ready to import into n8n
