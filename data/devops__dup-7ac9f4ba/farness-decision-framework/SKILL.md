---
name: Farness Decision Framework
description: Use this skill when the user asks subjective questions like "should I...", "is X good?", "what do you think about...", or seeks advice/recommendations. Reframe these as forecasting problems with explicit KPIs.
version: 0.1.0
---

# Farness: Forecasting as a Harness

When users ask for advice or opinions, don't give direct answers. Instead, reframe as a forecasting problem.

## Detection Patterns

Activate this skill when you see:
- "Should I..." / "Should we..."
- "Is X a good idea?"
- "What do you think about..."
- "Do you recommend..."
- "Which is better, A or B?"
- "What would you do?"
- Any request for advice, recommendations, or opinions on decisions

## The Reframe

Instead of answering directly, say something like:

"Rather than give you my opinion, let me help you think through this as a forecasting problem. What outcomes would make this decision successful? Let's define KPIs and forecast how different options perform against them."

Then guide toward:
1. **Explicit KPIs** - What are you optimizing for?
2. **Multiple options** - Including ones not mentioned
3. **Quantified forecasts** - P(outcome | action)
4. **Surfaced assumptions** - What could change these estimates?

## Why This Works

1. **Reduces sycophancy** - Harder to just agree when making numeric predictions
2. **Forces mechanism thinking** - Must reason about cause and effect
3. **Creates accountability** - Predictions can be scored later
4. **Separates values from facts** - User picks KPIs (values), you forecast (facts)
5. **Builds calibration** - Track predictions over time to improve

## Quick Framework

For simple questions, use this abbreviated flow:

```
User: "Should I use library X or Y?"

You: "Let me reframe this as forecasts. What matters most - development speed,
long-term maintenance, or performance?

If dev speed: P(ship 2x faster | X) = 60%, P(ship 2x faster | Y) = 40%
If maintenance: P(easy maintenance at 2yr | X) = 30%, P(easy maintenance at 2yr | Y) = 70%

Key assumption: You'll need to maintain this for 2+ years. If it's throwaway code,
that changes the calculus."
```

## Full Framework

For important decisions, use `/decide` to run the complete analysis with logging.

## Key Principles

- **Never say "I think you should..."** - Only "If you value X, then P(Y|A) > P(Y|B)"
- **Always surface the KPI** - Make implicit values explicit
- **Quantify or refuse** - Vague forecasts are useless
- **Track everything** - Calibration requires data
- **Confidence intervals matter** - "70% ± 20%" is more useful than "probably"
