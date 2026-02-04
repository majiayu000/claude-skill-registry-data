---
name: model-coordination
description: Use this skill when coordinating multiple AI models (Claude, GPT, Gemini, DeepSeek) for competitive trading analysis, running parallel model execution, aggregating decisions, or managing model performance tracking. Essential for multi-model trading arena operations.
---

# Multi-Model Coordination Skill

## When to Use
Activate this skill when:
- Running multiple AI models in parallel for trading decisions
- Comparing performance across different LLMs
- Aggregating decisions from multiple models
- Managing model portfolios and tracking P&L
- Setting up competitive trading arena
- Logging ModelChat decisions for transparency

## Architecture Overview

### Competition Arena Pattern (refs/AI-Trader/)

```
Multi-Model Trading Arena
├── Model 1: Claude Sonnet 4.5    ($10,000 starting capital)
├── Model 2: GPT-5                ($10,000 starting capital)
├── Model 3: Gemini 2.5 Pro       ($10,000 starting capital)
├── Model 4: DeepSeek v3.1        ($10,000 starting capital)
└── Model 5: Qwen3 Max            ($10,000 starting capital)

Each model:
✓ Independent decision-making
✓ Same data access
✓ Isolated portfolio
✓ Performance tracking
✓ ModelChat logging
```

## OpenRouter Integration

### Unified API Access
```python
from openai import OpenAI

# Single API for ALL models
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Model mapping
MODELS = {
    "claude": "anthropic/claude-sonnet-4.5",
    "gpt5": "openai/gpt-5",
    "gemini": "google/gemini-2.5-pro",
    "deepseek": "deepseek/deepseek-chat-v3.1",
    "qwen": "qwen/qwen3-max"
}

# Make requests (same interface for all)
response = client.chat.completions.create(
    model=MODELS["claude"],
    messages=[{"role": "user", "content": "Analyze AAPL"}]
)
```

### Benefits
- ✅ One API key for all models
- ✅ Automatic fallback handling
- ✅ Built-in rate limiting
- ✅ Usage tracking per model
- ✅ Pay-as-you-go (no subscriptions)
- ✅ Cost: ~$0.50-2/day for moderate usage

## Configuration (refs/AI-Trader/configs/default_config.json)

```json
{
  "models": [
    {
      "name": "claude-sonnet-4.5",
      "basemodel": "anthropic/claude-sonnet-4.5",
      "signature": "claude-4.5",
      "enabled": true
    },
    {
      "name": "gpt-5",
      "basemodel": "openai/gpt-5",
      "signature": "gpt-5",
      "enabled": true
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "max_retries": 3,
    "base_delay": 1.0,
    "initial_cash": 10000.0
  },
  "log_config": {
    "log_path": "./data/agent_data"
  }
}
```

## Parallel Execution Pattern

### From AI-Trader BaseAgent (refs/AI-Trader/agent/base_agent/base_agent.py:31-100)

```python
import asyncio
from typing import List, Dict, Any

async def run_model_analysis(
    model_name: str,
    ticker: str,
    date: str,
    market_data: Dict
) -> Dict:
    """Execute analysis for a single model"""

    # 1. Initialize agent
    agent = create_agent_for_model(model_name)

    # 2. Provide context
    context = {
        "ticker": ticker,
        "date": date,
        "market_data": market_data,
        "portfolio": get_model_portfolio(model_name),
        "cash": get_model_cash(model_name)
    }

    # 3. Get decision with retry logic
    decision = await execute_with_retry(
        lambda: agent.analyze_and_decide(context),
        max_retries=3,
        base_delay=1.0
    )

    # 4. Log to ModelChat
    await log_model_chat(model_name, ticker, decision)

    return {
        "model": model_name,
        "decision": decision["action"],  # BUY/SELL/HOLD
        "reasoning": decision["reasoning"],
        "confidence": decision.get("confidence", 0.5)
    }

async def run_all_models_parallel(
    tickers: List[str],
    date: str,
    market_data: Dict
) -> List[Dict]:
    """Execute all enabled models in parallel"""

    enabled_models = get_enabled_models()
    tasks = []

    for ticker in tickers:
        for model in enabled_models:
            task = run_model_analysis(
                model_name=model["name"],
                ticker=ticker,
                date=date,
                market_data=market_data[ticker]
            )
            tasks.append(task)

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions
    successful_results = [r for r in results if not isinstance(r, Exception)]
    failed_results = [r for r in results if isinstance(r, Exception)]

    if failed_results:
        print(f"Warning: {len(failed_results)} model(s) failed")

    return successful_results
```

## TradingAgents Integration

### Each Model Uses Full Agent Framework (refs/TradingAgents/)

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

async def run_model_with_agents(
    model_name: str,
    ticker: str,
    date: str
) -> Dict:
    """
    Each model gets its own TradingAgents graph
    with complete analyst -> researcher -> trader -> risk flow
    """

    # 1. Create custom config for this model
    config = {
        "llm_provider": "openai",  # OpenRouter compatible
        "deep_think_llm": get_model_id(model_name),
        "quick_think_llm": get_model_id(model_name),
        "backend_url": "https://openrouter.ai/api/v1",
        "max_debate_rounds": 1,
        "data_vendors": {
            "core_stock_apis": "yfinance",
            "technical_indicators": "yfinance",
            "fundamental_data": "alpha_vantage",
            "news_data": "alpha_vantage"
        }
    }

    # 2. Initialize graph
    ta = TradingAgentsGraph(
        config=config,
        selected_analysts=["market", "news", "fundamentals", "social"]
    )

    # 3. Run propagation
    final_state, decision = ta.propagate(ticker, date)

    # 4. Extract complete reasoning trace
    model_chat = {
        "model": model_name,
        "ticker": ticker,
        "date": date,
        "analysis": {
            "market": final_state["market_report"],
            "news": final_state["news_report"],
            "fundamentals": final_state["fundamentals_report"],
            "sentiment": final_state["sentiment_report"]
        },
        "research_debate": {
            "bull_argument": final_state["investment_debate_state"]["bull_history"],
            "bear_argument": final_state["investment_debate_state"]["bear_history"],
            "judge_decision": final_state["investment_debate_state"]["judge_decision"]
        },
        "trader_plan": final_state["trader_investment_plan"],
        "risk_assessment": final_state["risk_debate_state"]["judge_decision"],
        "final_decision": decision
    }

    return model_chat
```

## Decision Aggregation

### Consensus Analysis
```python
def aggregate_model_decisions(
    model_results: List[Dict]
) -> Dict:
    """
    Combine decisions from multiple models
    Identify consensus and outliers
    """

    # Count votes
    buy_count = sum(1 for r in model_results if r["decision"] == "BUY")
    sell_count = sum(1 for r in model_results if r["decision"] == "SELL")
    hold_count = sum(1 for r in model_results if r["decision"] == "HOLD")

    total = len(model_results)

    # Determine majority
    max_votes = max(buy_count, sell_count, hold_count)
    consensus_pct = max_votes / total

    if buy_count > sell_count and buy_count > hold_count:
        majority = "BUY"
    elif sell_count > buy_count and sell_count > hold_count:
        majority = "SELL"
    else:
        majority = "HOLD"

    # Calculate average confidence
    avg_confidence = sum(r.get("confidence", 0.5) for r in model_results) / total

    return {
        "ticker": model_results[0]["ticker"],
        "timestamp": model_results[0]["date"],
        "majority_decision": majority,
        "consensus_level": consensus_pct,
        "high_consensus": consensus_pct >= 0.7,
        "average_confidence": avg_confidence,
        "vote_breakdown": {
            "BUY": buy_count,
            "SELL": sell_count,
            "HOLD": hold_count
        },
        "individual_decisions": model_results,
        "outliers": identify_outliers(model_results, majority)
    }

def identify_outliers(results: List[Dict], majority: str) -> List[str]:
    """Find models that disagree with majority"""
    return [
        r["model"] for r in results
        if r["decision"] != majority
    ]
```

## Performance Tracking & Leaderboard

### Track Each Model's Portfolio (refs/AI-Trader/)

```python
class ModelPerformanceTracker:
    """
    Track trading performance for each model
    Similar to Alpha Arena leaderboard
    """

    def __init__(self, initial_cash: float = 10000.0):
        self.models = {}
        self.initial_cash = initial_cash

    def initialize_model(self, model_name: str):
        """Set up new model with starting capital"""
        self.models[model_name] = {
            "cash": self.initial_cash,
            "positions": {},  # {ticker: shares}
            "trade_history": [],
            "pnl": 0.0,
            "total_return_pct": 0.0,
            "num_trades": 0,
            "win_rate": 0.0
        }

    def execute_trade(
        self,
        model_name: str,
        action: str,
        ticker: str,
        shares: int,
        price: float,
        timestamp: str
    ):
        """Record and execute trade"""
        model = self.models[model_name]

        if action == "BUY":
            cost = shares * price
            if model["cash"] >= cost:
                model["cash"] -= cost
                model["positions"][ticker] = model["positions"].get(ticker, 0) + shares
                success = True
            else:
                success = False  # Insufficient funds

        elif action == "SELL":
            current_shares = model["positions"].get(ticker, 0)
            if current_shares >= shares:
                model["cash"] += shares * price
                model["positions"][ticker] -= shares
                success = True
            else:
                success = False  # Insufficient shares

        else:
            success = True  # HOLD - no action needed

        # Log trade
        trade = {
            "timestamp": timestamp,
            "action": action,
            "ticker": ticker,
            "shares": shares,
            "price": price,
            "value": shares * price,
            "success": success
        }
        model["trade_history"].append(trade)

        if success and action in ["BUY", "SELL"]:
            model["num_trades"] += 1

        return success

    def calculate_performance(
        self,
        model_name: str,
        current_prices: Dict[str, float]
    ) -> Dict:
        """Calculate current portfolio value and metrics"""
        model = self.models[model_name]

        # Portfolio value = cash + (shares * current_price)
        portfolio_value = model["cash"]
        for ticker, shares in model["positions"].items():
            if shares > 0:
                portfolio_value += shares * current_prices.get(ticker, 0)

        # Calculate returns
        pnl = portfolio_value - self.initial_cash
        total_return_pct = (pnl / self.initial_cash) * 100

        return {
            "model": model_name,
            "portfolio_value": round(portfolio_value, 2),
            "cash": round(model["cash"], 2),
            "positions": model["positions"],
            "pnl": round(pnl, 2),
            "total_return_pct": round(total_return_pct, 2),
            "num_trades": model["num_trades"]
        }

    def get_leaderboard(
        self,
        current_prices: Dict[str, float]
    ) -> List[Dict]:
        """Generate sorted leaderboard"""
        rankings = []

        for model_name in self.models:
            perf = self.calculate_performance(model_name, current_prices)
            rankings.append(perf)

        # Sort by P&L (descending)
        rankings.sort(key=lambda x: x["pnl"], reverse=True)

        # Add rank
        for i, rank in enumerate(rankings, 1):
            rank["rank"] = i
            rank["medal"] = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "")

        return rankings
```

## ModelChat Logging

### Transparent Decision Tracking
```python
async def log_model_chat(
    model_name: str,
    ticker: str,
    decision_data: Dict
):
    """
    Log complete reasoning process
    Similar to Alpha Arena's ModelChat transparency
    """

    model_chat_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "ticker": ticker,
        "reasoning_trace": [
            {
                "stage": "market_analysis",
                "output": decision_data["analysis"]["market"],
                "key_insights": extract_key_points(decision_data["analysis"]["market"])
            },
            {
                "stage": "fundamental_analysis",
                "output": decision_data["analysis"]["fundamentals"],
                "metrics": extract_metrics(decision_data["analysis"]["fundamentals"])
            },
            {
                "stage": "news_sentiment",
                "output": decision_data["analysis"]["news"],
                "sentiment": calculate_sentiment(decision_data["analysis"]["news"])
            },
            {
                "stage": "bull_bear_debate",
                "bull": decision_data["research_debate"]["bull_argument"],
                "bear": decision_data["research_debate"]["bear_argument"],
                "winner": decision_data["research_debate"]["judge_decision"]
            },
            {
                "stage": "trader_decision",
                "output": decision_data["trader_plan"]
            },
            {
                "stage": "risk_check",
                "output": decision_data["risk_assessment"]
            },
            {
                "stage": "final_decision",
                "decision": decision_data["final_decision"],
                "confidence": decision_data.get("confidence"),
                "reasoning": decision_data.get("final_reasoning")
            }
        ]
    }

    # Save to database (Supabase)
    await save_to_supabase("model_chats", model_chat_entry)

    # Also save as JSON for archival
    save_json_log(model_name, ticker, model_chat_entry)
```

## Error Handling

### Retry Logic (refs/AI-Trader/agent/base_agent/base_agent.py)
```python
async def execute_with_retry(
    func,
    max_retries: int = 3,
    base_delay: float = 1.0
) -> Any:
    """
    Execute with exponential backoff
    Critical for API reliability
    """

    for attempt in range(max_retries):
        try:
            result = await func()
            return result

        except Exception as e:
            if attempt == max_retries - 1:
                # Final attempt failed
                print(f"All retries exhausted: {e}")
                raise

            # Calculate backoff
            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")

            await asyncio.sleep(delay)
```

## Telegram Integration

### Send Results to Users
```python
async def send_aggregated_decision(
    bot,
    chat_id: str,
    aggregated: Dict
):
    """Format and send decision summary"""

    message = f"📊 *Trading Decision: {aggregated['ticker']}*\n\n"

    # Consensus
    decision_emoji = {"BUY": "📈", "SELL": "📉", "HOLD": "⏸️"}
    emoji = decision_emoji[aggregated["majority_decision"]]

    message += f"{emoji} *Consensus: {aggregated['majority_decision']}*\n"
    message += f"Agreement: {aggregated['consensus_level']:.0%}\n"
    message += f"Confidence: {aggregated['average_confidence']:.0%}\n\n"

    # Vote breakdown
    message += "*Votes:*\n"
    message += f"📈 BUY: {aggregated['vote_breakdown']['BUY']}\n"
    message += f"📉 SELL: {aggregated['vote_breakdown']['SELL']}\n"
    message += f"⏸️ HOLD: {aggregated['vote_breakdown']['HOLD']}\n\n"

    # Individual decisions
    message += "*Individual Models:*\n"
    for result in aggregated["individual_decisions"]:
        emoji = decision_emoji[result["decision"]]
        message += f"{emoji} {result['model']}: {result['decision']}\n"

    # Outliers
    if aggregated["outliers"]:
        message += f"\n⚠️ *Outliers*: {', '.join(aggregated['outliers'])}\n"

    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown"
    )
```

## Code References

- AI-Trader BaseAgent: `refs/AI-Trader/agent/base_agent/base_agent.py:31-100`
- AI-Trader Config: `refs/AI-Trader/configs/default_config.json`
- TradingAgents Graph: `refs/TradingAgents/tradingagents/graph/trading_graph.py`
- TradingAgents Config: `refs/TradingAgents/tradingagents/default_config.py`

## Best Practices

1. **Isolate model state** - Each model must have independent portfolio
2. **Log everything** - ModelChat for full transparency
3. **Handle failures gracefully** - Don't let one model crash all others
4. **Respect rate limits** - Use retry with exponential backoff
5. **Track costs** - Monitor OpenRouter usage per model
6. **Fair comparison** - Same data access and timing for all models
7. **Update leaderboard real-time** - After each trading decision
8. **Archive ModelChats** - Keep decision history for analysis

## Usage Example

**User**: "Run all models on NVDA"

**Execution**:
1. Load enabled models from config
2. Fetch NVDA market data once (shared by all)
3. Run each model's TradingAgents graph in parallel
4. Collect all decisions and reasoning
5. Aggregate to find consensus
6. Log all ModelChats to database
7. Update each model's portfolio
8. Calculate updated leaderboard
9. Send summary to Telegram/Slack
