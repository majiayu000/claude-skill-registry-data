---
name: model-routing-patterns
description: Model routing configuration templates and strategies for cost optimization, speed optimization, quality optimization, and intelligent fallback chains. Use when building AI applications with OpenRouter, implementing model routing strategies, optimizing API costs, setting up fallback chains, implementing quality-based routing, or when user mentions model routing, cost optimization, fallback strategies, model selection, intelligent routing, or dynamic model switching.
allowed-tools: Read, Write, Bash, Edit, Glob
---

# Model Routing Patterns

Production-ready model routing configurations and strategies for OpenRouter that optimize for cost, speed, quality, or balanced performance with intelligent fallback chains.

## Purpose

This skill provides comprehensive templates, scripts, and strategies for implementing sophisticated model routing in OpenRouter-powered applications. It helps you:
- Reduce API costs by routing to cheaper models when appropriate
- Optimize for speed with fast models and streaming
- Maintain quality with premium model fallbacks
- Implement intelligent task-based routing
- Build reliable multi-tier fallback chains

## Activation Triggers

Use this skill when:
- Designing model routing strategies
- Implementing cost optimization
- Setting up fallback chains for reliability
- Building task complexity-based routing
- Configuring dynamic model selection
- Optimizing API performance vs cost tradeoffs
- Implementing A/B testing for models
- Setting up monitoring and analytics

## Available Routing Strategies

### 1. Cost-Optimized Routing
**Goal:** Minimize API costs while maintaining acceptable quality

**Strategy:**
- Use free models (google/gemma-2-9b-it:free, meta-llama/llama-3.2-3b-instruct:free)
- Fallback to budget models (anthropic/claude-4.5-sonnet, openai/gpt-4o-mini)
- Premium models only for complex tasks requiring highest quality

**Template:** `templates/cost-optimized-routing.json`

**Best for:**
- High-volume applications
- Simple tasks (classification, extraction, formatting)
- Development/testing environments
- Budget-constrained projects

### 2. Speed-Optimized Routing
**Goal:** Minimize latency and response time

**Strategy:**
- Prioritize fastest models regardless of cost
- Enable streaming for immediate feedback
- Use smaller models with quick inference
- Geographic routing to nearest endpoints

**Template:** `templates/speed-optimized-routing.json`

**Best for:**
- Real-time chat applications
- Interactive user experiences
- Low-latency requirements
- Streaming responses

### 3. Quality-Optimized Routing
**Goal:** Maximize output quality with premium models

**Strategy:**
- Use top-tier models (gpt-4o, claude-4.5-sonnet, gemini-pro)
- Fallback to other premium models for availability
- Multi-model voting for critical tasks
- Quality verification layers

**Template:** `templates/quality-optimized-routing.json`

**Best for:**
- Critical business decisions
- Content creation
- Complex reasoning tasks
- Customer-facing applications

### 4. Balanced Routing
**Goal:** Dynamically route based on task complexity

**Strategy:**
- Analyze request complexity
- Route simple tasks to cheap models
- Route complex tasks to premium models
- Adaptive based on success metrics

**Template:** `templates/balanced-routing.json`

**Best for:**
- Mixed workloads
- Production applications
- General-purpose AI services
- Optimizing cost/quality tradeoff

### 5. Custom Routing
**Goal:** Implement domain-specific routing logic

**Template:** `templates/custom-routing-template.json`

**Customizable factors:**
- User tier/subscription level
- Geographic location
- Time of day pricing
- Model availability
- Rate limit status
- Historical success rates

## Key Resources

### Scripts

**validate-routing-config.sh**
- Validates routing configuration syntax
- Checks model availability on OpenRouter
- Verifies fallback chain logic
- Ensures no circular dependencies
- Validates model IDs and parameters

**test-fallback-chain.sh**
- Tests fallback chain execution
- Simulates model failures
- Verifies graceful degradation
- Measures latency through chain
- Validates error handling

**generate-routing-config.sh**
- Generates routing config from strategy type
- Interactive configuration builder
- Validates and optimizes settings
- Exports to JSON/TypeScript/Python formats

**analyze-cost-savings.sh**
- Analyzes potential cost savings from routing
- Compares routing strategies
- Projects monthly costs
- Generates cost reports
- Identifies optimization opportunities

### Templates

**Configuration Templates (JSON):**
- `cost-optimized-routing.json` - Free/cheap models with premium fallback
- `speed-optimized-routing.json` - Fastest models with streaming
- `quality-optimized-routing.json` - Premium models with fallbacks
- `balanced-routing.json` - Task-based dynamic routing
- `custom-routing-template.json` - Template for custom strategies

**Code Templates:**
- `routing-config.ts` - TypeScript routing configuration
- `routing-config.py` - Python routing configuration

### Examples

- `cost-routing-example.md` - Complete cost-optimized routing setup
- `dynamic-routing-example.md` - Task complexity-based routing
- `fallback-chain-example.md` - 3-tier fallback strategy
- `monitoring-example.md` - Cost tracking and analytics setup

## Workflow

### 1. Identify Requirements

Determine your optimization goals:
```bash
# Interactive strategy selector
./scripts/generate-routing-config.sh
```

Answer questions about:
- Primary goal (cost/speed/quality/balanced)
- Budget constraints
- Latency requirements
- Quality thresholds
- Supported model providers

### 2. Generate Configuration

```bash
# Generate from strategy type
./scripts/generate-routing-config.sh cost-optimized > config.json

# Or copy template
cp templates/cost-optimized-routing.json config.json
```

### 3. Validate Configuration

```bash
# Validate syntax and model availability
./scripts/validate-routing-config.sh config.json
```

Checks:
- JSON syntax
- Model IDs exist on OpenRouter
- Fallback chain is valid
- No circular references
- Required fields present

### 4. Test Fallback Chain

```bash
# Test fallback behavior
./scripts/test-fallback-chain.sh config.json
```

Simulates failures to ensure graceful degradation.

### 5. Analyze Cost Impact

```bash
# Compare routing strategies
./scripts/analyze-cost-savings.sh config.json baseline-config.json
```

Shows projected savings and performance tradeoffs.

### 6. Deploy and Monitor

- Deploy configuration to production
- Monitor using examples/monitoring-example.md
- Track metrics: cost, latency, success rate, quality
- Iterate based on real-world performance

## Common Routing Patterns

### Pattern 1: Simple Fallback Chain
```json
{
  "primary": "meta-llama/llama-3.2-3b-instruct:free",
  "fallback": [
    "anthropic/claude-4.5-sonnet",
    "openai/gpt-4o-mini"
  ]
}
```

### Pattern 2: Task Complexity Routing
```json
{
  "simple_tasks": {
    "models": ["google/gemma-2-9b-it:free"]
  },
  "medium_tasks": {
    "models": ["anthropic/claude-4.5-sonnet"]
  },
  "complex_tasks": {
    "models": ["openai/gpt-4o"]
  }
}
```

### Pattern 3: Time-Based Routing
```json
{
  "peak_hours": {
    "models": ["openai/gpt-4o-mini"],
    "max_latency_ms": 1000
  },
  "off_peak": {
    "models": ["google/gemini-pro"],
    "max_latency_ms": 3000
  }
}
```

### Pattern 4: User Tier Routing
```json
{
  "free_tier": {
    "models": ["meta-llama/llama-3.2-3b-instruct:free"],
    "rate_limit": 10
  },
  "premium_tier": {
    "models": ["anthropic/claude-4.5-sonnet"],
    "rate_limit": 1000
  }
}
```

## Model Categories for Routing

### Free Models (Cost: $0)
- `google/gemma-2-9b-it:free`
- `meta-llama/llama-3.2-3b-instruct:free`
- `meta-llama/llama-3.2-1b-instruct:free`
- `microsoft/phi-3-mini-128k-instruct:free`

**Use for:** High-volume, simple tasks, development

### Budget Models (Cost: $0.10-0.50/1M tokens)
- `openai/gpt-4o-mini`
- `google/gemini-flash-1.5`

**Use for:** Production workloads, balanced cost/quality

### Premium Models (Cost: $3-15/1M tokens)
- `anthropic/claude-4.5-sonnet`
- `openai/gpt-4o`
- `google/gemini-pro-1.5`

**Use for:** Complex reasoning, critical tasks, high quality

### Specialized Models
- **Vision:** `openai/gpt-4-vision-preview`
- **Code:** `anthropic/claude-4.5-sonnet` (code-specific)
- **Long Context:** `google/gemini-pro-1.5` (1M+ tokens)

## Best Practices

1. **Always implement fallback chains** - Single points of failure cause downtime
2. **Monitor actual costs** - Theoretical savings may differ from real usage
3. **Test quality degradation** - Ensure cheaper models meet quality thresholds
4. **Set timeout limits** - Prevent slow models from blocking requests
5. **Track model availability** - Some models have rate limits or downtime
6. **Use task classification** - Route based on complexity, not one-size-fits-all
7. **Implement retry logic** - Handle transient failures gracefully
8. **Cache responses** - Reduce API calls for repeated queries
9. **A/B test routing strategies** - Validate improvements with data
10. **Budget alerting** - Get notified before exceeding cost limits

## Troubleshooting

**All models in fallback chain failing:**
- Check OpenRouter status page
- Verify API key has credits
- Test with a known-working model
- Review rate limit status

**Higher costs than expected:**
- Analyze actual request distribution
- Check if complex tasks are routed to premium models
- Verify caching is working
- Review retry/fallback patterns

**Quality degradation:**
- Review which model is actually being used
- Test free models against quality benchmarks
- Consider upgrading routing strategy
- Implement quality verification layer

**High latency:**
- Check if using slow models
- Enable streaming for faster perceived response
- Use geographic routing
- Implement parallel model requests with first-response-wins

## Integration Examples

See examples directory for complete implementations:
- Cost-optimized chat application
- Dynamic routing based on conversation context
- Multi-tier fallback with monitoring
- Real-time cost tracking dashboard

---

**Skill Location:** `plugins/openrouter/skills/model-routing-patterns/`
**Version:** 1.0.0
**Supported Frameworks:** Node.js, Python, TypeScript, any OpenRouter-compatible client
