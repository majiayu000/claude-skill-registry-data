---
name: "gpt-integration"
description: "Use this skill ONLY when modifying GPT calls, agent prompts, or structured output. Do not use for other AI/ML tasks."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- All GPT calls go through `src/alpacalyzer/gpt/call_gpt.py`
- Agent prompts are defined in agent files (`src/alpacalyzer/agents/*.py`)
- Tests must mock the OpenAI client (automatically done in `conftest.py`)

# GPT Integration Overview

Alpacalyzer uses OpenAI's GPT-4 for AI-powered agent analysis. All API calls are centralized in `call_gpt.py` using structured output with Pydantic models.

# Procedural Steps

## 1. Review Existing GPT Integration

```bash
# See how GPT is called
cat src/alpacalyzer/gpt/call_gpt.py

# See agent prompt examples
cat src/alpacalyzer/agents/warren_buffet_agent.py
cat src/alpacalyzer/agents/technicals_agent.py

# See test mocking
cat tests/conftest.py
```

**Key patterns**:

- GPT-4 is used via `call_gpt()` function
- Responses use Pydantic models for structured output
- OpenAI client is auto-mocked in tests
- System prompts define agent personality/approach

## 2. Understand call_gpt() Function

**Location**: `src/alpacalyzer/gpt/call_gpt.py`

**Function signature**:

```python
def call_gpt(
    system_prompt: str,
    user_prompt: str,
    response_model: Type[BaseModel],
    model: str = "gpt-4",
    temperature: float = 0.7
) -> BaseModel:
    """
    Call GPT-4 with structured output.

    Args:
        system_prompt: System message (agent personality, instructions)
        user_prompt: User message (data to analyze)
        response_model: Pydantic model for structured response
        model: OpenAI model to use
        temperature: Sampling temperature (0-1)

    Returns:
        Instance of response_model with parsed response
    """
```

## 3. Modify or Create Agent Prompts

**When modifying existing prompts**:

Edit the `SYSTEM_PROMPT` constant in the agent file:

```python
# src/alpacalyzer/agents/warren_buffet_agent.py

SYSTEM_PROMPT = """You are Warren Buffett, the legendary value investor.

Your investment philosophy:
- <principle 1>
- <principle 2>
- <principle 3>

<Additional instructions>

Analyze the following opportunity and provide your recommendation."""
```

**Best practices for prompts**:

1. **Clear identity**: Define who the agent is
2. **Philosophy/approach**: State key principles
3. **Output format**: Describe what you expect (handled by Pydantic model)
4. **Constraints**: Mention any limitations or focus areas

## 4. Define Response Models

**Location**: `src/alpacalyzer/data/models.py` (for shared models)

**Template for new response model**:

```python
from pydantic import BaseModel, Field


class <Agent>Response(BaseModel):
    """Structured response from <Agent> analysis."""

    analysis: str = Field(
        ...,
        description="Detailed analysis of the trading opportunity"
    )

    recommendation: str = Field(
        ...,
        description="Trading recommendation: 'buy', 'sell', or 'hold'"
    )

    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence level (0-100)"
    )

    key_factors: list[str] = Field(
        default_factory=list,
        description="Key factors influencing the recommendation"
    )

    risks: list[str] = Field(
        default_factory=list,
        description="Identified risks or concerns"
    )
```

**Pydantic best practices**:

- Use `Field()` with descriptions for GPT guidance
- Add validators with `ge`, `le` for numeric ranges
- Use enums for constrained choices
- Provide defaults where appropriate

## 5. Call GPT in Agent

**Pattern**:

```python
from alpacalyzer.gpt.call_gpt import call_gpt
from alpacalyzer.data.models import AgentResponse


SYSTEM_PROMPT = """<Your agent prompt>"""


def analyze_<agent>(ticker: str, trading_signals: dict, **kwargs) -> dict:
    """Agent analysis function."""

    # Prepare context for GPT
    context = f"""
Ticker: {ticker}
Price: ${trading_signals['price']:.2f}
Technical Score: {trading_signals['score']:.2f}
Momentum: {trading_signals['momentum']:.1f}%
Signals: {', '.join(trading_signals['signals'])}

Additional context:
{kwargs.get('context', 'Not available')}

Provide your analysis.
"""

    # Call GPT
    response = call_gpt(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=context,
        response_model=AgentResponse,
        model="gpt-4",
        temperature=0.7  # Lower for more deterministic, higher for creative
    )

    # Return structured data
    return {
        "<agent>_analysis": response.analysis,
        "<agent>_recommendation": response.recommendation,
        "<agent>_confidence": response.confidence,
        "<agent>_factors": response.key_factors,
        "<agent>_risks": response.risks
    }
```

## 6. Test GPT Integration

**OpenAI client is auto-mocked** in all tests via `conftest.py`.

**Test template**:

```python
"""Tests for <agent> with GPT integration."""

from unittest.mock import MagicMock
import pytest

from alpacalyzer.agents.<agent>_agent import analyze_<agent>
from alpacalyzer.data.models import AgentResponse


def test_<agent>_calls_gpt_correctly(mock_openai_client):
    """Test <agent> calls GPT with correct parameters."""

    # Mock GPT response
    mock_response = AgentResponse(
        analysis="Detailed analysis here...",
        recommendation="buy",
        confidence=85,
        key_factors=["Factor 1", "Factor 2"],
        risks=["Risk 1"]
    )

    # Configure mock
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Prepare test data
    trading_signals = {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.75,
        "momentum": 5.2,
        "signals": ["Golden Cross", "RSI Bullish"]
    }

    # Call agent
    result = analyze_<agent>("AAPL", trading_signals)

    # Verify GPT was called
    mock_openai_client.chat.completions.create.assert_called_once()

    # Verify response structure
    assert "<agent>_analysis" in result
    assert "<agent>_recommendation" in result
    assert result["<agent>_recommendation"] in ["buy", "sell", "hold"]


def test_<agent>_handles_gpt_errors(mock_openai_client):
    """Test <agent> handles GPT API errors gracefully."""

    # Mock GPT failure
    mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

    trading_signals = {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.75,
        "momentum": 5.2,
        "signals": []
    }

    # Should handle error without crashing
    # (Adjust based on your error handling strategy)
    with pytest.raises(Exception):
        analyze_<agent>("AAPL", trading_signals)
```

## 7. Environment Configuration

**API key must be in `.env`**:

```bash
# .env
OPENAI_API_KEY=sk-...your_key_here
```

**Never hardcode API keys!**

## 8. Run Tests

```bash
# Run agent tests (GPT mocking automatic)
uv run pytest tests/test_<agent>_agent.py -v

# Run all agent tests
uv run pytest tests/test_*_agent.py

# Verify OpenAI client is mocked
uv run pytest tests/test_<agent>_agent.py -v -s
```

# Reference: Existing Examples

- `src/alpacalyzer/gpt/call_gpt.py` - Central GPT calling logic
- `src/alpacalyzer/agents/warren_buffet_agent.py` - Value investing prompt
- `src/alpacalyzer/agents/cathie_wood_agent.py` - Innovation focus prompt
- `src/alpacalyzer/agents/technicals_agent.py` - Technical analysis prompt
- `src/alpacalyzer/data/models.py` - Response models (AgentResponse, TradingStrategy)
- `tests/conftest.py` - Auto-mocking setup

# Special Considerations

1. **Cost**: GPT-4 API calls are expensive. Minimize calls during development/testing by using mocks.

2. **Rate Limits**: OpenAI has rate limits. Implement backoff/retry if needed (see `call_gpt.py`).

3. **Determinism**: GPT responses are non-deterministic. Use lower temperature (0-0.3) for more consistent output.

4. **Token Limits**: GPT-4 has token limits. Keep prompts concise, especially with large data contexts.

5. **Testing**: **Always mock GPT in tests**. Never make real API calls during testing (expensive + slow).

6. **Structured Output**: Use Pydantic models to enforce response structure. GPT-4 is good at following schemas.

7. **Error Handling**: GPT calls can fail (rate limits, network issues). Always handle exceptions.

## Example: Advanced Prompt Engineering

```python
SYSTEM_PROMPT = """You are Ray Dalio, founder of Bridgewater Associates and creator of the "Economic Machine" framework.

Your investment philosophy:
1. **Economic Cycles**: Understand where we are in the economic cycle
2. **Debt Cycles**: Monitor credit expansion and contraction
3. **Diversification**: "Holy Grail" - 15+ uncorrelated return streams
4. **Risk Parity**: Balance risk across asset classes
5. **Radical Transparency**: Challenge assumptions with data

Analysis Framework:
- Macro context: Interest rates, inflation, growth
- Company fundamentals: Earnings, debt levels, cash flow
- Market positioning: Sentiment, valuations, flows
- Risk/reward: Asymmetric opportunities

You prefer:
- Data-driven analysis over speculation
- Long-term structural trends over short-term noise
- Risk-adjusted returns over absolute returns
- Balanced exposure to reduce downside risk

Provide a structured analysis following your principles. Be specific about:
1. Where we are in the economic cycle
2. How this asset fits in a diversified portfolio
3. Key risks and how to hedge them
4. Expected risk-adjusted returns

Format your response as a clear, actionable recommendation."""


class DalioResponse(BaseModel):
    """Structured response from Ray Dalio analysis."""

    economic_cycle_position: str = Field(
        ...,
        description="Current position in economic/debt cycle"
    )

    portfolio_role: str = Field(
        ...,
        description="How this asset fits in a diversified portfolio"
    )

    key_risks: list[str] = Field(
        ...,
        description="Identified risks and potential hedges"
    )

    expected_sharpe_ratio: float = Field(
        ...,
        description="Expected risk-adjusted return (Sharpe ratio)"
    )

    recommendation: str = Field(
        ...,
        description="buy, sell, or hold"
    )

    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence in recommendation (0-100)"
    )

    analysis: str = Field(
        ...,
        description="Detailed analysis following Dalio's framework"
    )
```

This example shows:

- Clear identity and philosophy
- Structured analysis framework
- Specific output requirements
- Custom response model matching the framework
