---
name: finwiz-flow-architecture
description: "Critical Flow architecture lessons for FinWiz including business logic flow, state management, and crew integration patterns. Use when designing or debugging CrewAI Flows."
allowed-tools: ["Read", "Edit"]
---

# FinWiz Flow Architecture Lessons

Critical lessons from deep portfolio analysis implementation and flow sequence corrections.

## Lesson 1: Flow Sequence Must Match Business Logic

### The Problem

The original flow had discovery crews running BEFORE portfolio analysis. This is backwards from the logical business process.

### Correct Business Flow

1. **Analyze what you have** - Portfolio holdings analysis
2. **Find alternatives** - Replace underperforming holdings
3. **Discover new opportunities** - Find additional A+ investments
4. **Propose rebalancing** - Optimize allocation
5. **Present report** - Consolidated recommendations

### Implementation Rule

**ALWAYS design flow sequences to match the logical business process, not technical convenience.**

```python
# ✅ CORRECT: Portfolio analysis before discovery
@start()
def validate_data_integration(self):
    pass

@listen("validate_data_integration")
def check_portfolio(self):  # Portfolio analysis FIRST
    pass

@listen("analyze_and_update_portfolio")
def check_crypto(self):  # Discovery AFTER
    pass

# ❌ WRONG: Discovery before portfolio analysis
@listen("validate_data_integration")
def check_crypto(self):  # Discovery crew
    pass

@listen(and_("check_crypto", "check_stock", "check_etf"))
def check_portfolio(self):  # Portfolio analysis
    pass
```

## Lesson 2: Consolidate Related Operations

### The Problem

Three separate Flow methods performed related operations sequentially:

1. `analyze_holdings_deep()` - Run crews
2. `match_alternatives()` - Find alternatives
3. `update_portfolio_review_with_deep_analysis()` - Regenerate portfolio

This caused:

- Portfolio review generated TWICE (inefficient)
- Race conditions (discovery could start before portfolio update)
- Complex dependency chains (3 @listen decorators)

### Solution

Consolidate into ONE atomic operation:

```python
@listen("check_portfolio")
def analyze_and_update_portfolio(self) -> dict[str, Any]:
    """Atomic operation: deep analysis + alternatives + portfolio update."""
    # Step 1: Deep analysis
    deep_results = self._run_deep_analysis_on_holdings()
    
    # Step 2: Match alternatives
    alternatives = self._match_alternatives_for_holdings(deep_results)
    
    # Step 3: Update portfolio (ONCE)
    portfolio_updated = self._update_portfolio_review_with_enriched_data()
    
    return consolidated_results
```

### Implementation Rule

**When operations are logically related and sequential, consolidate them into a single atomic method with helper functions.**

Benefits:

- ✅ Single portfolio generation (not twice)
- ✅ No race conditions
- ✅ Simpler dependency chain
- ✅ Atomic semantics (all-or-nothing)

## Lesson 3: Fix Listener Dependencies Carefully

### The Problem

```python
@listen(and_("match_alternatives", "check_portfolio_rebalancing"))
def check_investment_discovery(self):
    pass
```

This listener waited for `match_alternatives` but NOT for `update_portfolio_review_with_deep_analysis`, which also listened to `match_alternatives`. This created a race condition.

### Solution

After consolidation, the listener waits for the complete atomic operation:

```python
@listen(and_("analyze_and_update_portfolio", "check_portfolio_rebalancing"))
def check_investment_discovery(self):
    pass
```

### Implementation Rule

**When using @listen decorators, ensure dependencies wait for COMPLETE operations, not intermediate steps.**

## Lesson 4: Discovery vs Deep Analysis Separation

### The Problem

Discovery crews (StockCrew, EtfCrew, CryptoCrew) were being misused for single-ticker deep analysis, causing:

- 3-6 hour hangs
- Reasoning agents asking for "10 tickers"
- Infinite loops with `'ready': False`

### Solution

Create separate crews with clear purposes:

**Discovery Crews** (existing):

- Purpose: Screen and find "top 10" assets
- Input: No specific tickers
- Output: List of opportunities
- Use case: Investment discovery

**Deep Analysis Crew** (new):

- Purpose: Analyze ONE specific ticker
- Input: ticker + asset_class
- Output: DeepAnalysisResult with grade
- Use case: Portfolio holdings evaluation

### Implementation Rule

**Create separate crews for different use cases. Don't force a "top 10" crew to analyze single tickers.**

## Lesson 5: Dynamic Tool Routing Eliminates Duplication

### The Problem Avoided

Could have created 3 separate deep analysis crews (StockDeepAnalysisCrew, EtfDeepAnalysisCrew, CryptoDeepAnalysisCrew), leading to code duplication.

### Solution

ONE unified crew with dynamic tool routing:

```python
def get_tools_for_asset_class(self, asset_class: str) -> list:
    """Route to appropriate tool set based on asset class."""
    if asset_class.lower() == "stock":
        return get_stock_crew_tools(...)
    elif asset_class.lower() == "etf":
        return get_etf_crew_tools(...)
    elif asset_class.lower() == "crypto":
        return get_crypto_crew_tools(...)
    else:
        raise ValueError(f"Invalid asset_class: {asset_class}")
```

### Implementation Rule

**When crews differ only in tool selection, use dynamic routing instead of creating separate crew classes.**

## Lesson 6: Test What You Control, Not AI Behavior

### The Problem Avoided

Initial test plans included testing agent behavior, LLM calls, and crew execution results.

### Solution

Focus tests on:

- ✅ Tool routing logic
- ✅ Configuration loading
- ✅ Helper methods with mocks
- ✅ Flow state management
- ✅ Error handling
- ✅ Data parsing

Do NOT test:

- ❌ Agent behavior
- ❌ LLM calls
- ❌ Crew execution
- ❌ Reasoning loops

### Implementation Rule

**Only test deterministic logic you control. Mock all AI/LLM behavior.**

## Lesson 7: Reasoning-Compatible Task Descriptions

### The Problem

Task descriptions with "top 10" language caused reasoning agents to request multiple tickers when only one was provided.

### Solution

Explicit single-ticker task descriptions:

```yaml
deep_analysis_task:
  description: >
    Perform comprehensive analysis of the provided {asset_class} ticker: {ticker}
    
    SINGLE TICKER MODE: You are analyzing ONE specific {asset_class}, not screening multiple assets.
    The ticker {ticker} is provided as input. Do NOT request additional tickers.
    
    Analysis Steps for {asset_class}:
    1. Validate {ticker} using TickerValidationTool
    2. Fetch {asset_class}-specific data for {ticker}
    ...
```

### Implementation Rule

**When using reasoning=True, task descriptions must explicitly state the mode (single ticker vs multiple) and repeat the input variable throughout.**

Key phrases:

- "SINGLE TICKER MODE"
- "the provided ticker: {ticker}"
- "Do NOT request additional tickers"
- Repeat "{ticker}" throughout description

## Lesson 8: Final Reporter Must Have Empty Tools

### The Problem Avoided

Final reporters should consolidate from context, not make external API calls.

### Solution

Use `@final_reporter` decorator to enforce empty tools:

```python
@final_reporter
@agent
def investment_reporter(self) -> Agent:
    return Agent(
        config=self.agents_config["investment_reporter"],
        tools=[],  # MUST be empty - enforced by decorator
        verbose=True
    )
```

### Implementation Rule

**Final reporters in crews must have empty tools lists. Use @final_reporter decorator to enforce this at framework level.**

## Lesson 9: JSON Serialization of Datetime Objects

### The Problem

Tools returning JSON strings with `json.dumps()` failed when data contained datetime objects:

```
ERROR - Error in technical analysis: Object of type datetime is not JSON serializable
```

### Solution

Always use `default=str` parameter with `json.dumps()`:

```python
# ❌ WRONG - Will fail with datetime objects
tech_data = {"timestamp": datetime.now(), "value": 123.45}
return json.dumps(tech_data, indent=2)

# ✅ CORRECT - Handles datetime and other non-serializable types
tech_data = {"timestamp": datetime.now(), "value": 123.45}
return json.dumps(tech_data, indent=2, default=str)
```

### Alternative: Use Pydantic Serialization

```python
# ✅ BEST - Pydantic handles datetime serialization automatically
result = QuantitativeBacktestResult(
    backtest_start_date=datetime.now(),
    backtest_end_date=datetime.now(),
    # ... other fields
)
return result.model_dump_json(indent=2)
```

### Implementation Rule

**When manually serializing data with `json.dumps()`, always include `default=str` to handle datetime, numpy types, and other non-JSON-serializable objects. Prefer Pydantic's `model_dump_json()` when working with models.**

## Summary Checklist

When designing CrewAI Flows:

- [ ] Flow sequence matches logical business process
- [ ] Related operations consolidated into atomic methods
- [ ] Listener dependencies wait for complete operations
- [ ] Discovery and deep analysis crews are separate
- [ ] Dynamic tool routing used instead of duplicate crews
- [ ] Tests focus on logic, not AI behavior
- [ ] Task descriptions are reasoning-compatible
- [ ] Final reporters have empty tools (enforced by decorator)
- [ ] Portfolio/data generated once, not multiple times
- [ ] No race conditions in parallel listeners
- [ ] JSON serialization uses `default=str` or Pydantic's `model_dump_json()`

Apply these architectural patterns to avoid common Flow design pitfalls and ensure robust, maintainable CrewAI implementations.
