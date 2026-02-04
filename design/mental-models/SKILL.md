---
name: mental-models
description: Apply Charlie Munger's latticework of mental models to any problem. Use when user requests decision analysis, says "help me think", "apply mental model", mentions model names (inversion, bottlenecks, second-order thinking), or needs structured thinking frameworks.
---

# Mental Models

Apply 98 cognitive frameworks from multiple disciplines to analyze problems, make decisions, and think more clearly.

## Quick Reference

**Models by Category:**
- General Thinking (m01-m09): First principles, inversion, second-order thinking
- Science (m10-m29): Leverage, inertia, feedback loops, ecosystems
- Systems Thinking (m30-m40): Bottlenecks, scale, margin of safety, emergence
- Mathematics (m41-m47): Randomness, regression to mean, local vs global maxima
- Economics (m48-m59): Trade-offs, scarcity, creative destruction
- Art (m60-m70): Framing, audience, contrast
- Strategy (m71-m75): Asymmetric warfare, seeing the front
- Human Nature (m76-m98): Biases, incentives, social proof

## How to Use

### Quick Apply
When user mentions a specific model + context:
1. Load the model file from `models/` directory
2. Read: Description, Thinking Steps, When to Avoid
3. Apply Thinking Steps to user's context
4. Provide 3-5 actionable insights
5. Note any cautions from "When to Avoid"

**Example**: "Apply inversion to this architecture decision"

### Discovery
When user asks "what models for X":
1. Search `resources/model-index.json` for matching keywords
2. Return top 5 relevant models with brief descriptions
3. Offer to quick-apply any of them

**Example**: "What mental models help with scaling?"

### Deep Analysis
When user has complex decision:
1. Ask 2-3 clarifying questions
2. Select max 3 most relevant models
3. Apply each model's Thinking Steps systematically
4. Synthesize insights across models
5. Provide actionable recommendations

**Example**: "Help me think through whether to accept this job offer"

## Model File Structure

Each model in `models/` contains:
- **Description**: Core concept
- **When to Avoid**: Limitations
- **Keywords**: Application contexts
- **Thinking Steps**: Sequential framework (follow exactly)
- **Coaching Questions**: Prompts for deeper exploration

## Key Guidelines

1. **Quality over quantity**: Max 3 models per analysis
2. **Follow Thinking Steps exactly**: That's where the value is
3. **Check "When to Avoid"**: Alert user if model doesn't fit
4. **Latticework approach**: Show how models connect
5. **Be actionable**: Provide concrete insights, not just theory

## Resources

- `resources/model-index.json` - Searchable index of all 98 models
- `resources/quick-reference.md` - Common patterns and model combinations
