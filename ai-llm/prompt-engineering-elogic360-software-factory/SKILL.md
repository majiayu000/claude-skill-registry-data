---
name: prompt-engineering
description: Prompt Engineering — Institutional capability and runbook for prompt-engineering.
---

# SKILL: Prompt Engineering
## Domain: LLM Prompt Design, Agent Orchestration, Context Management

**Activation triggers:** LLM integration, AI feature, prompt template, agent
design, context window, few-shot examples, chain-of-thought, structured output,
function calling, market intelligence AI.

---

## Prompt Architecture Principles

```
1. SYSTEM PROMPT → identity, constraints, output format
2. CONTEXT INJECTION → relevant data (account, market, history)
3. FEW-SHOT EXAMPLES → 2–3 examples for complex tasks
4. USER INSTRUCTION → specific task or question
5. OUTPUT SCHEMA → JSON schema or Pydantic model for parsing
```

---

## Market Analysis Prompt Template

```python
# integral-imi-backend/app/services/ai/market_analysis.py
from anthropic import AsyncAnthropic
from pydantic import BaseModel

client = AsyncAnthropic()

MARKET_ANALYSIS_SYSTEM = """You are a senior institutional market analyst at Integral Market.
Your analysis is used by professional traders for position decisions.

Rules:
- Cite specific price levels, not vague directional commentary
- State confidence level (High/Medium/Low) for each signal
- Always include risk level: Conservative | Moderate | Aggressive
- Never give investment advice — provide analysis, not recommendations
- Output ONLY valid JSON matching the provided schema

Analysis framework:
1. Technical structure (support/resistance, trend, momentum)
2. Key price levels (entry zones, invalidation, targets)
3. Risk context (volatility, upcoming events, spread)
4. Confluences (technical + fundamental alignment)
"""

class MarketSignal(BaseModel):
    direction: str          # "bullish" | "bearish" | "neutral"
    confidence: str         # "High" | "Medium" | "Low"
    key_levels: list[float]
    entry_zone: tuple[float, float]
    invalidation: float
    target_1: float
    target_2: float | None
    risk_level: str         # "Conservative" | "Moderate" | "Aggressive"
    rationale: str          # 2-3 sentences max
    confluences: list[str]

async def analyze_symbol(
    symbol: str,
    timeframe: str,
    ohlcv: list[dict],
    recent_news: list[str] | None = None,
) -> MarketSignal:
    context = f"""Symbol: {symbol} | Timeframe: {timeframe}
Recent OHLCV (last 20 bars):
{_format_ohlcv(ohlcv[-20:])}
"""
    if recent_news:
        context += f"\nRecent news:\n" + "\n".join(f"- {n}" for n in recent_news[:5])

    response = await client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=MARKET_ANALYSIS_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f"{context}\n\nProvide market analysis as JSON matching this schema:\n{MarketSignal.model_json_schema()}"
            }
        ],
    )

    return MarketSignal.model_validate_json(response.content[0].text)
```

---

## Structured Output with Tool Use

```python
# Use tool_use for guaranteed structured output (preferred over JSON parsing)

ANALYSIS_TOOL = {
    "name": "submit_analysis",
    "description": "Submit structured market analysis",
    "input_schema": {
        "type": "object",
        "properties": {
            "direction": {
                "type": "string",
                "enum": ["bullish", "bearish", "neutral"],
                "description": "Overall market direction bias",
            },
            "confidence": {
                "type": "string",
                "enum": ["High", "Medium", "Low"],
            },
            "key_levels": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Critical support and resistance levels",
            },
            "rationale": {
                "type": "string",
                "maxLength": 400,
            },
        },
        "required": ["direction", "confidence", "key_levels", "rationale"],
    },
}

response = await client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    tools=[ANALYSIS_TOOL],
    tool_choice={"type": "tool", "name": "submit_analysis"},  # force tool use
    messages=[{"role": "user", "content": prompt}],
)

# Parse tool use result
tool_result = next(b for b in response.content if b.type == "tool_use")
analysis = tool_result.input   # guaranteed to match schema
```

---

## Trading Journal AI Coach Prompt

```python
JOURNAL_COACH_SYSTEM = """You are an AI trading psychology coach reviewing a trader's journal entry.

Your role:
- Identify emotional patterns that affected decision-making
- Highlight rule violations (if trading rules are provided)
- Suggest specific, actionable improvements
- Be direct and specific — avoid generic advice
- Never validate poor risk management

Output format:
1. Emotional pattern identified (1 sentence)
2. What went well (if anything)
3. Primary improvement (specific and actionable)
4. Rule violation (if any)
"""

async def coach_journal_entry(
    trade: dict,
    journal_entry: str,
    trading_rules: list[str] | None = None,
) -> str:
    rules_section = ""
    if trading_rules:
        rules_section = "\n\nTrader's rules:\n" + "\n".join(f"- {r}" for r in trading_rules)

    prompt = f"""Trade details:
Symbol: {trade['symbol']} | Direction: {trade['direction']}
Entry: {trade['entry_price']} | Exit: {trade['exit_price']}
PnL: {trade['profit']:+.2f} | Duration: {trade['duration_minutes']} minutes

Trader's notes: "{journal_entry}"{rules_section}

Provide coaching feedback:"""

    response = await client.messages.create(
        model="claude-haiku-4-5",   # coaching is high-volume; use cheaper model
        max_tokens=512,
        system=JOURNAL_COACH_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
```

---

## Context Window Management

```python
# Context window limits (as of 2025):
# claude-opus-4-5:    200k tokens input, 16k output
# claude-sonnet-4-5:  200k tokens input, 16k output
# claude-haiku-4-5:   200k tokens input, 8k output

# Rule: never send more than 50k tokens of market data to an analysis call
# Compress OHLCV: send only LAST N bars needed for the timeframe

def _format_ohlcv(bars: list[dict], max_bars: int = 50) -> str:
    """Compact OHLCV format — uses ~20 tokens per bar."""
    recent = bars[-max_bars:]
    lines = [f"{b['time']}|O:{b['open']:.5f}|H:{b['high']:.5f}|L:{b['low']:.5f}|C:{b['close']:.5f}|V:{b['volume']:.0f}"
             for b in recent]
    return "\n".join(lines)

# Use claude-haiku for high-frequency, low-complexity tasks:
#   - journal coaching, sentiment classification, tag extraction
# Use claude-sonnet for medium-complexity:
#   - technical analysis, news summarization
# Use claude-opus for high-stakes, complex reasoning:
#   - portfolio-level analysis, strategic market narrative
```

---

## Prompt Versioning

```python
# Always version prompts so you can A/B test and roll back
# software-factory/prompts/market-analysis/v3.py

PROMPT_VERSION = "market-analysis-v3"
PROMPT_CHANGELOG = """
v3: Added confluences field, reduced max_tokens 2048→1024
v2: Added risk_level classification
v1: Initial market analysis prompt
"""

# Log which prompt version produced which output
logger.info("AI analysis complete", extra={
    "symbol": symbol,
    "prompt_version": PROMPT_VERSION,
    "model": "claude-opus-4-5",
    "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
    "confidence": analysis.confidence,
})
```

---

## Anti-Patterns

```
✗ No system prompt (model has no identity or constraints)
✗ Asking for JSON output without a schema (hallucinated structure)
✗ Sending full trade history (10k rows) in context (use summaries)
✗ Retrying on every failure (implement exponential backoff)
✗ Trusting LLM output without validation (always parse with Pydantic)
✗ Using opus for every call (5× more expensive than haiku for simple tasks)
✗ No prompt versioning (can't diagnose regressions)
✗ Logging full prompt text in production (may contain PII)
✗ Hardcoded API key in source (use ANTHROPIC_API_KEY env var)
```
