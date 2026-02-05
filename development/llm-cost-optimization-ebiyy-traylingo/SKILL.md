---
name: llm-cost-optimization
description: Reduce LLM API costs without sacrificing quality. Covers prompt caching (Anthropic), local response caching, prompt compression, debouncing triggers, and cost analysis. Use when building LLM-powered features, analyzing API costs, optimizing prompts, or implementing caching strategies.
---

# LLM Cost Optimization

Practical techniques to reduce LLM API costs by 35-65%.

## Quick Reference

| Technique | Savings | When to Use | Reference |
|-----------|---------|-------------|-----------|
| Prompt Caching | 25-45% | Same system prompt, frequent calls | [caching.md](references/caching.md) |
| Response Cache | 100% | Repeated identical requests | [caching.md](references/caching.md) |
| Prompt Compression | 10-20% | Long system prompts | [prompts.md](references/prompts.md) |
| Debouncing | 50%+ | Duplicate triggers | [triggers.md](references/triggers.md) |

## The 80/20 of LLM Costs

For short user inputs, **system prompts dominate costs**:

| Text Length | Input Tokens | System Prompt % |
|-------------|--------------|-----------------|
| Short (~100 chars) | ~250 | **80-87%** |
| Medium (~500 chars) | ~450 | **44%** |
| Long (~2000 chars) | ~900 | **22%** |

**Optimization priority:**
1. Cache system prompts (biggest impact)
2. Cache identical requests (free repeats)
3. Debounce triggers (prevent waste)
4. Compress prompts (last resort)

## Cost Estimation (Claude Haiku 3.5)

| Text Length | Est. Cost |
|-------------|-----------|
| Short (~100 chars) | ~$0.0004 |
| Medium (~500 chars) | ~$0.0008 |
| Long (~2000 chars) | ~$0.002 |

**Benchmark:** 1000 translations ≈ $0.80 (before optimization)

## Implementation Checklist

### Before Building

- [ ] Add logging to every AI trigger point
- [ ] Verify triggers fire exactly once per user action
- [ ] Check for Pressed/Released event duplicates

### Caching Strategy

- [ ] Enable Anthropic Prompt Caching for system prompts
- [ ] Implement local response cache (hash-based)
- [ ] Include model name in cache key
- [ ] Set reasonable cache limits (e.g., 500 entries LRU)

### Prompt Design

- [ ] Measure current token count
- [ ] Identify critical rules (security, output format)
- [ ] Test quality after compression
- [ ] Document WHY for each rule kept

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Trigger fires twice | 2x cost | Check event.state |
| No prompt caching | Full price every call | Use cache_control |
| Aggressive prompt compression | Quality drops | Keep critical rules |
| Cache key missing model | Wrong results | Include model in key |

## Quick Wins

### 1. Check for Duplicate Triggers

```rust
// Before ANY optimization, verify this
log::info!("AI trigger fired: {:?}", event);
if event.state != ShortcutState::Pressed {
    return;  // Ignore Released events
}
```

### 2. Enable Prompt Caching (Anthropic)

```rust
let system = vec![SystemBlock {
    block_type: "text".to_string(),
    text: system_prompt,
    cache_control: CacheControl { cache_type: "ephemeral".to_string() },
}];
```

### 3. Add Response Cache

```rust
// Check cache before API call
if let Some(cached) = get_cached(&text, &model) {
    return Ok(cached);  // Free!
}

// Save after API call
save_to_cache(&text, &result, &model)?;
```

## Anti-Patterns

- **TOON format for plain text** - Only helps with structured data
- **Caching without model key** - Haiku vs Sonnet give different results
- **Prompt compression first** - Optimize triggers and caching before touching prompts
