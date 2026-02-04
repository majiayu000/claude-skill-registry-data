---
name: ai-llm-development
description: |
  MANDATORY invocation for ALL LLM-related work. Invoke immediately when:
  - ANY mention of model names, IDs, or versions
  - ANY configuration of AI providers or APIs
  - ANY defaults/constants for LLM settings
  - ANY prompt engineering or modification
  - ANY discussion of model capabilities or features
  - ANY changes to AI-related dependencies
  - Reading/writing .env files with AI config
  - Modifying aiProviders.ts, prompts.ts, or similar
  - Reviewing AI-related pull requests
  - Debugging LLM integration issues

  CRITICAL: Training data lags reality by months. ALWAYS research first.
  Use WebSearch, Exa MCP, or Gemini CLI before making ANY LLM decisions.
---

# AI/LLM Development

## Core Philosophy

**Context Engineering > Prompt Engineering**: Optimize entire LLM configuration, not just wording.

**Simplicity First**: 80% of use cases need single LLM call, not multi-agent systems.

**Currency Over Memory**: Models deprecate in 6-12 months. Learn to find current ones via leaderboards.

**Empiricism**: Benchmarks guide; YOUR data decides. Test top 3-5 models with your prompts.

## RESEARCH FIRST PROTOCOL

**CRITICAL**: Your training data is ALWAYS stale for LLM work. The field changes weekly.

### Before ANY LLM-Related Action

1. **Identify what you're assuming**: Model capabilities? API syntax? Best practices?
2. **Research using live tools** (in order of preference):
   - WebSearch: "latest [model/provider] models"
   - Exa MCP: Get current documentation and examples
   - Gemini CLI: Verify against latest information with web grounding
3. **Verify your assumptions**: Don't trust training data for:
   - Model names and versions (new models release monthly)
   - API syntax and parameters (providers update frequently)
   - Best practices and recommendations (evolve constantly)
   - Pricing and limits (change without notice)
   - Deprecation status (models removed regularly)

### Research Query Templates

**Model Selection**:
- "latest [provider] models"
- "[model-name] release date and capabilities"
- "is [model-name] deprecated or superseded"
- "[provider] newest models announced"

**API Syntax**:
- "[provider] API documentation [specific-feature]"
- "[sdk-name] current version and usage"
- "OpenRouter model ID format current"

**Best Practices**:
- "[task] LLM best practices latest"
- "current recommendations for [architecture pattern]"
- "[framework] latest patterns and examples"

### Red Flags That Trigger Mandatory Research

❌ Making assumptions about version numbers (3.0 vs 2.5 doesn't mean newer)
❌ Changing model defaults without verification
❌ Assuming API syntax from training data
❌ Selecting models based on memory of capabilities
❌ Following "best practices" without checking if still current
❌ Any action based on "I think..." or "probably..." for LLM topics

### Research Before Action Checklist

Before committing any LLM-related change:

- [ ] Searched for latest information on involved models/APIs
- [ ] Verified current state vs. training data assumptions
- [ ] Checked provider documentation for API syntax
- [ ] Confirmed model is not deprecated or superseded
- [ ] Validated best practices are still current
- [ ] Tested configuration syntax in provider console/playground

**Mantra**: "When in doubt about LLM tech, RESEARCH. When certain about LLM tech, STILL RESEARCH."

## Decision Trees

### Model Selection
```
Task type → Find relevant benchmark → Check leaderboards → Test top 3 empirically
Coding: SWE-bench | Reasoning: GPQA | General: Arena Elo
```
See: `references/model-selection.md`

### Architecture Complexity
```
1. Single LLM Call (start here - 80% stop here)
2. Sequential Calls (workflows)
3. LLM + Tools (function calling)
4. Agentic System (LLM controls flow)
5. Multi-Agent (only if truly needed)
```
See: `references/architecture-patterns.md`

### Vector Storage
```
<1M vectors → Postgres pgvector or Convex
1-50M vectors → Postgres with pgvectorscale
>50M + <10ms p99 → Dedicated (Qdrant, Weaviate)
```

## Key Optimizations

- **Prompt Caching**: 60-90% cost reduction. Static content first.
- **Structured Outputs**: Native JSON Schema. Zero parsing failures.
- **Model Routing**: Simple→cheap model, Complex→expensive model.
- **Hybrid RAG**: Vector + keyword search = 15-25% better than pure vector.

See: `references/prompt-engineering.md`, `references/production-checklist.md`

## Stack Defaults (TypeScript/Next.js)

- **SDK**: Vercel AI SDK (streaming, React hooks, provider-agnostic)
- **Provider**: OpenRouter (400+ models, easy A/B testing, fallbacks)
- **Vectors**: Postgres pgvector (95% of use cases, $20-50/month)
- **Observability**: Langfuse (self-hostable, generous free tier)
- **Evaluation**: Promptfoo (CI/CD integration, security testing)

## Quality Infrastructure

**Production-grade LLM apps need:**

1. **Model Gateway** (OpenRouter, LiteLLM)
   - Multi-provider access
   - Fallback chains
   - Cost routing
   - See: `llm-gateway-routing` skill

2. **Evaluation & Testing** (Promptfoo)
   - Regression testing in CI/CD
   - Security scanning (red team)
   - Quality gates
   - See: `llm-evaluation` skill

3. **Production Observability** (Langfuse)
   - Full trace debugging
   - Cost tracking
   - Latency monitoring
   - See: `langfuse-observability` skill

4. **Quality Audit**
   - Run `/llm-gates` command to audit your LLM infrastructure
   - Identifies gaps in routing, testing, observability, security, cost

### Quick Setup

```bash
# Evaluation (Promptfoo)
npx promptfoo@latest init
npx promptfoo@latest eval

# Observability (Langfuse)
pnpm add langfuse
# Sign up at langfuse.com, add keys to .env

# Gateway (OpenRouter)
# Sign up at openrouter.ai, add OPENROUTER_API_KEY to .env
```

### Quality Gate Standards

| Stage | Checks | Time Budget |
|-------|--------|-------------|
| Pre-commit | Prompt validation, secrets scan | < 5s |
| Pre-push | Regression suite, cost estimate | < 15s |
| CI/CD | Full eval, security scan, A/B comparison | < 5 min |
| Production | Traces, cost alerts, error monitoring | Continuous |

## Scripts

- `scripts/validate_llm_config.py <dir>` - Scan for LLM anti-patterns

## References

- `references/model-selection.md` - Leaderboards, search strategies, red flags
- `references/prompt-engineering.md` - Caching, structured outputs, CoT, model-specific styles
- `references/architecture-patterns.md` - Complexity ladder, RAG, tool use, caching
- `references/production-checklist.md` - Cost, errors, security, observability, evaluation

## Related Skills

- `llm-evaluation` - Promptfoo setup, CI/CD integration, security testing
- `llm-gateway-routing` - OpenRouter, LiteLLM, routing strategies
- `langfuse-observability` - Tracing, cost tracking, production debugging

## Related Commands

- `/llm-gates` - Audit LLM infrastructure quality across 5 pillars
- `/observe` - General observability audit (includes LLM section)

## Live Research Tools

**Use these BEFORE relying on training data:**

- **WebSearch**: Latest model releases, deprecations, best practices
- **Exa MCP** (`mcp__exa__web_search_exa`): Current documentation and code examples
- **Gemini CLI** (`gemini`): Sophisticated reasoning with Google Search grounding
- **Provider Playgrounds**: OpenRouter, Google AI Studio, Anthropic Console

**Research Flow**:
1. WebSearch for latest information
2. Exa MCP for documentation and examples
3. Gemini CLI for complex verification and comparison
4. Provider playground for syntax testing
