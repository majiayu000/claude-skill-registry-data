---
name: pricing-guidance
description: Claude API pricing, tier recommendations, token cost optimization, and ROI calculations for CDP features.
---

# Pricing Guidance Skill

## When to Use
- Questions about Claude API pricing
- Token cost concerns
- ROI of CDP features
- Tier recommendations
- Cost comparison requests

## Claude API Pricing (as of 2024)

### Model Tiers

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Opus 4 | $15.00 | $75.00 |
| Claude Sonnet 4 | $3.00 | $15.00 |
| Claude Haiku | $0.25 | $1.25 |

### Common Use Cases

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Complex analysis | Opus | Best quality |
| General chat | Sonnet | Good balance |
| High volume | Haiku | Cost efficient |
| Code generation | Sonnet | Strong at code |

## Context Editing ROI

### Token Savings Formula
```
Savings = (Original Tokens - Compressed Tokens) × Price per Token
```

### Example: 50-turn conversation

**Without Context Editing**:
- Turn 50 context: 10,000 tokens
- Cumulative API calls: ~250,000 tokens
- Cost at Sonnet: $0.75 input + $3.75 output = ~$4.50

**With Context Editing**:
- Turn 50 context: 3,000 tokens
- Cumulative API calls: ~85,000 tokens
- Cost at Sonnet: $0.26 input + $1.28 output = ~$1.54
- **Savings: ~66%**

## Response Guidelines

1. **Be transparent**: Share published pricing openly
2. **Focus on value**: Connect pricing to business outcomes
3. **Use specific numbers**: Calculate actual savings
4. **Recommend appropriately**: Match tier to use case
