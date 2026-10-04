---
name: openrouter-docs-skill
description: USE THIS SKILL for any question about OpenRouter API, model routing, pricing, available AI models, API keys, or provider configuration. This skill has complete local documentation — do not use web search or WebFetch instead.
---

# OpenRouter Documentation Skill

Single source of truth for OpenRouter API, model selection, pricing, and capabilities.

## Path Resolution

Use `${CLAUDE_SKILL_DIR}` to reference this skill's directory — it resolves automatically whether the skill is symlinked or local.

## Reference Files

| Tier | File                             | Size  | Use For                                                               |
| ---- | -------------------------------- | ----- | --------------------------------------------------------------------- |
| 1    | `references/quick-reference.md`  | 3KB   | Authentication, base URL, common endpoints, basic examples            |
| 2    | `references/models-reference.md` | 126KB | All 338+ models grouped by provider, pricing, context lengths         |
| 3    | `references/openapi.yaml`        | 666KB | Complete OpenAPI spec — every endpoint, parameter, schema, error code |

Supporting: `references/models.json` (raw API data)

## How to Use This Skill

### Step 1: Understand the Question

**Quick fact** — "What's the OpenRouter base URL?"
Load Tier 1 only. Answer in one line.

**Model selection** — "What's the cheapest model with 128k context?"
Load Tier 2, scan for context lengths and pricing.

**Model comparison** — "Compare Claude Sonnet vs GPT-4o pricing"
Load Tier 2, grep for both providers, present side-by-side.

**API details** — "What parameters does the completions endpoint accept?"
Use Tier 1 to orient, then grep Tier 3 for the full schema.

**Implementation** — "Set up streaming with OpenRouter"
May need Tier 1 (auth/basics) + Tier 3 (streaming schema).

### Step 2: Load the Right Tiers

1. For basic questions → load `quick-reference.md` first. If it answers, stop.
2. For model/pricing questions → load `models-reference.md`. Search by provider or model name.
3. For detailed API questions → grep into `openapi.yaml` (never load the whole file).

**Search patterns:**

```bash
# Models: find a provider section
grep -A 50 "### ANTHROPIC" references/models-reference.md

# Models: find a specific model
grep -B 2 -A 5 "claude-opus" references/models-reference.md

# API: find an endpoint
grep -A 100 "/chat/completions:" references/openapi.yaml

# API: find a schema
grep -A 50 "ChatCompletionRequest:" references/openapi.yaml

# API: use line numbers for larger sections
grep -n "/chat/completions:" references/openapi.yaml
sed -n '1234,1334p' references/openapi.yaml
```

### Step 3: Cite Sources

Always tell the user where the answer came from:

- "From the quick reference: ..."
- "From the models reference (Anthropic section): ..."
- "From the OpenAPI spec (completions endpoint): ..."

When comparing models, always include pricing context (per million tokens).

## Updating Documentation

When user asks to update (trigger: "update openrouter documentation"):

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-openrouter-docs.sh"
```

Updates openapi.yaml, models.json, models-reference.md, and quick-reference.md in ~30 seconds.

**Selective update:**

```bash
"${CLAUDE_SKILL_DIR}/scripts/update-openrouter-docs.sh" --models  # Models and pricing only
```

Update frequently — new models are added 2-3 times per week and pricing changes regularly.

## Coverage

**What this skill covers:**

- OpenRouter API endpoints and authentication
- 338+ models from 15+ providers (Claude, GPT, Gemini, Llama, Mistral, Cohere, etc.)
- Current pricing and context lengths for all models
- Request/response schemas, streaming, function calling
- Error codes and rate limiting

**What this skill does NOT cover:**

- OpenRouter dashboard/UI usage
- Billing and account management
- Claude API directly (use claude-docs-skill)
- Model training or fine-tuning

## Rules

1. **Always check current docs** — don't answer model questions from memory. Pricing and availability change.
2. **Never load full openapi.yaml** — always use grep/sed to extract relevant sections.
3. **Include pricing context** — when discussing models, show per-million-token costs.
4. **Compare when asked** — if the user is choosing between models, show a comparison table.
5. **Cite every answer** — name the file and section.

---

**Skill Version:** 2.0.0
**Sources:** openrouter.ai/openapi.yaml, openrouter.ai/api/v1/models
