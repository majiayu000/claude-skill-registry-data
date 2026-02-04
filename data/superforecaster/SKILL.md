---
name: superforecaster
description: Make well-calibrated probability estimates using superforecasting methodology. Use when user asks about probability, likelihood, chance, odds, "will X happen", "when will X happen", "how much will X cost", "what could go wrong", failure modes, risk assessment, forecasting, or any question involving uncertainty and estimation.
---

# Superforecaster Skill

Make well-calibrated probability estimates. Adapts methodology based on question attributes and desired output.

## Forecasting Cookbook

Questions have overlapping attributes. Mix and match these heuristics based on what applies.

### By information availability

**Public/searchable topic**:

- Check prediction markets first (Polymarket, Metaculus, Manifold)
- Search for expert forecasts, news analysis
- Look for historical base rates in public data

**Personal/private situation**:

- Fall back on reference class base rates
- Ask user for specifics that affect the estimate
- Example: "When will I get a job?" → ask: field, experience, how long since last job, actively applying?, then search: current hiring rates in that field, unemployment trends, typical job search duration by seniority

**Sparse data**:

- Use hierarchical priors (general → specific)
- Fermi decomposition into estimable parts
- Widen confidence intervals

### By output type needed

**Binary (yes/no)**:

- State probability + 90% CI on the probability itself

**Quantity (how much/many)**:

- Point estimate + 90% CI
- Fermi breakdown if complex
- Consider: inflation, trends, comparable anchors

**Timeline (when/how long)**:

- Median + 90% CI (not just mean—distributions are often right-skewed)
- Apply planning fallacy correction (+50-100% for personal projects)
- Note distribution shape (symmetric vs heavy right tail)

**Distribution/trajectories**:

- Model the process, simulate, show percentiles
- Plot survival curves, CDFs, or sample paths
- Report both conditional and unconditional stats

**Failure modes / risks**:

- Enumerate systematically, don't just list top 3
- Score: P(occur) × Impact
- Identify correlated failure modes

### By time direction

**Past events (verification)**:

- Direct search, fact-checking
- Triangulate across sources
- Output: boolean + confidence in the answer

**Future events**:

- Outside view first (base rates, markets)
- Inside view adjustments (specific factors)
- Pre-mortem: "if wrong, why?"

### By complexity

**Single-factor**:

- Find the base rate, adjust, done

**Multi-factor but independent**:

- Estimate each, multiply/combine analytically or via simple simulation

**Multi-factor with dependencies**:

- Model the dependency structure (event tree, Bayesian network)
- Simulate through the network
- Example: "Will I be able to buy a house?" depends on savings, income trajectory, home prices, interest rates, down payment requirements—model jointly

**Sequential/process**:

- Step through time, update state
- Handle branching paths with probabilities
- Example trajectory output:

```
[Filed I-485] ─┬─ 65% → [Direct Approval] → 8-14 months
               ├─ 25% → [RFE] ─┬─ 80% → [Approved] → +2-4 months
               │               └─ 20% → [Denied]
               └─ 10% → [NOID] ─┬─ 40% → [Approved]
                                └─ 60% → [Denied]
```

### By domain (common patterns)

**Personal finance**:

- Monte Carlo with historical returns
- Account for sequence risk, inflation, expense variance
- Ask about: allocation, withdrawal strategy, risk tolerance

**Job/career**:

- Base rates by field, seniority, market conditions
- Ask about: field, experience, active search status, location flexibility

**Applications/approvals**:

- Published approval rates by category
- Processing time distributions (often right-skewed)
- Ask about: application type, any red flags, supporting evidence strength

**Health/medical**:

- Published outcome statistics by condition/treatment
- Adjust for age, comorbidities, specific circumstances
- Note: sensitive—frame as "questions to ask your doctor"

**Startups/ventures**:

- Power law outcomes, high failure rates
- Stage-specific survival rates
- Factor in: team, market, traction, funding

## Related Search Strategy

Map questions to searchable topics:

| Question                        | Related Searchable Topics                                                           |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| "How much will groceries cost?" | "USA inflation 2026", "food price index forecast", "grocery CPI"                    |
| "Will my visa get approved?"    | "[visa type] approval rate [year]", "[country] visa processing statistics"          |
| "When will project finish?"     | "software project delay statistics", "[similar project type] timeline"              |
| "Will startup X succeed?"       | "startup success rate by stage", "YC company outcomes", "[sector] startup survival" |

**Search expansion rules**:

1. Identify the category/domain
2. Find statistical base rates for that category
3. Look for recent trends/changes
4. Check for expert forecasts on related topics

## Prediction Market References

### Major Markets

| Market     | URL              | Best For                         | Notes                                         |
| ---------- | ---------------- | -------------------------------- | --------------------------------------------- |
| Polymarket | polymarket.com   | Crypto, politics, current events | Largest volume, real money                    |
| Metaculus  | metaculus.com    | Science, tech, long-term         | High-quality forecasters, detailed rationales |
| Manifold   | manifold.markets | Wide variety, niche topics       | Easy to find obscure questions                |
| PredictIt  | predictit.org    | US politics                      | Legal US market, capped stakes                |
| Kalshi     | kalshi.com       | Economics, events                | CFTC-regulated                                |

**Search patterns**:

```
site:polymarket.com [topic]
site:metaculus.com [topic]
site:manifold.markets [topic]
```

**How to use market prices**:

- Market at 70% = strong prior toward 70%
- Diverge only with specific inside information
- Note liquidity (low volume = less reliable)
- Check when market was created (stale = less reliable)

### Creating Prediction Markets

**When to suggest creating a Manifold question**:

- Question is resolvable with clear criteria
- Public interest (others might want to forecast too)
- Time horizon is reasonable (weeks to years, not hours)
- No existing market covers the question well
- User would benefit from crowd wisdom / tracking

**Good Manifold question types**:

- Binary: "Will X happen by [date]?"
- Numeric: "How many Y by [date]?"
- Multiple choice: "Which of A/B/C will happen first?"
- Date: "When will X happen?"

**Question design principles**:

- Precise resolution criteria (who judges, what counts)
- Reasonable close date
- Unambiguous wording
- Include relevant context in description

**Suggestion format**:

```
This question might benefit from a prediction market. Consider creating on Manifold:

**Title**: "Will OpenAI have a tender offer or IPO by end of 2025?"
**Type**: Binary
**Close date**: 2025-12-31
**Resolution**: Resolves YES if OpenAI completes any liquidity event
(IPO, tender offer, or acquisition) allowing employee stock sales by Dec 31, 2025.

This would let you:
1. Get crowd wisdom from other forecasters
2. Track how probability changes over time
3. Potentially profit if you have better information

Want me to help draft the full question description?
```

**Note**: User has a Manifold Markets account for creating questions.

## Statistical Sources

**General statistics**:

- Our World in Data (ourworldindata.org)
- Statista (statista.com)
- US government (census.gov, bls.gov, data.gov)
- Eurostat (ec.europa.eu/eurostat)

**Domain-specific**:

- Software: Standish Group, Stack Overflow surveys
- Startups: CB Insights, Crunchbase
- Science: Nature Index, PubMed meta-analyses
- Economics: FRED, IMF, World Bank

**Base rate queries**:

```
"[category] success rate"
"[type] approval rate [year]"
"[event type] historical frequency"
"[domain] statistics meta-analysis"
```

## Output Formats

### Binary probability (yes/no questions)

```
**Probability**: X%
**90% CI**: [low]% - [high]%
**Verbal**: [Almost certainly not | Unlikely | Toss-up | Likely | Almost certain]
```

### Quantity estimate

```
**Estimate**: [value] [units]
**90% CI**: [low] - [high]
**Fermi breakdown**: (if applicable)
  - Component 1: X
  - Component 2: Y
  - Combined: X × Y = Z
```

### Timeline estimate

```
**Median**: [time]
**90% CI**: [earliest] - [latest]
**Distribution shape**: [symmetric | right-skewed (delays likely) | ...]
```

### Failure modes

```
| Rank | Failure Mode | P(occur) | Impact | Risk Score |
|------|--------------|----------|--------|------------|
| 1    | [mode]       | X%       | High   | [P×I]      |
```

## Hierarchical Priors

For questions where multiple reference classes apply, layer priors from general to specific:

**Example: OpenAI stock valuation**

```
Level 1 (broadest): "It's a company"
  - Base: Companies have varied outcomes, mean reversion applies

Level 2: "It's a startup"
  - Prior: High variance, ~90% fail, but survivors grow fast
  - Power law distribution of outcomes

Level 3: "It's a late-stage AI company"
  - Prior: Currently high growth sector, but potential bubble risk
  - Relevant comps: Anthropic, Databricks, other unicorns

Level 4: "It's OpenAI specifically"
  - Unique factors: Leadership changes, Microsoft relationship, regulatory scrutiny
  - Historical: Past valuations, revenue growth rate

Level 5: "My specific situation"
  - Vesting schedule, tax implications, liquidity constraints
```

**How to combine**:

1. Start with broadest applicable reference class
2. Update Bayesian-style with each narrower class
3. Weight more specific priors higher when data is available
4. Be explicit about which level dominates your estimate

**Tail risk decomposition example**:

```
P(OpenAI worth <50% of current) by 2026:

- P(general market crash) × P(affects OpenAI | crash) = 15% × 80% = 12%
- P(AI winter / hype collapse) = 10%
- P(major competitive loss) = 8%
- P(regulatory action) = 5%
- P(internal collapse / scandal) = 5%
- P(nationalization / forced restructure) = 2%

Combined tail risk (some overlap): ~25-30%
```

## Core Methodology

### Step 1: Classify the question

- What type? (A-I from taxonomy above)
- What output format is appropriate?
- What related topics should I search?

### Step 2: Outside view first

- Find base rates for reference class
- Check prediction markets
- Look for expert forecasts

### Step 3: Inside view adjustments

- List factors that make this case different
- Estimate direction (+/-) and magnitude for each
- Adjust base rate accordingly

### Step 4: Synthesize

- Combine outside and inside views
- State confidence interval (not just point estimate)
- Identify key uncertainties

### Step 5: Pre-mortem

- "If this forecast is wrong, why?"
- List top failure modes for the forecast itself

## Calibration Reference

| Probability | Verbal               | Interpretation                 |
| ----------- | -------------------- | ------------------------------ |
| 1-5%        | Almost certainly not | Would be very surprised        |
| 10-20%      | Unlikely             | Possible but not expected      |
| 30-40%      | Probably not         | Lean against                   |
| 45-55%      | Toss-up              | Genuinely uncertain            |
| 60-70%      | Probably             | Lean toward                    |
| 80-90%      | Likely               | Expected outcome               |
| 95-99%      | Almost certain       | Would be very surprised if not |

**Common biases to counter**:

- **Planning fallacy**: Add 50-100% to time estimates
- **Overconfidence**: Default to wider CIs
- **Availability**: Check base rates, don't rely on memorable examples
- **Anchoring**: Consider multiple starting points

## Computational Tools

Write and run Python scripts when helpful. Use numpy, pandas, matplotlib.

### When to use code

- Multiple interacting uncertainties (simulation beats mental math)
- User wants to see the distribution shape
- Complex Fermi decomposition with many factors
- Trajectory analysis with many branches

### Example applications

- **Timeline Monte Carlo**: Model phases as lognormal (captures right-skew delays), combine, plot distribution
- **FIRE/Portfolio survival**: Bootstrap historical S&P returns, simulate 10k trajectories, report survival rate and percentiles
- **Bayesian updates**: Compute posteriors from priors and likelihoods
- **Sensitivity analysis**: Vary key parameters, show which dominate uncertainty
- **Distribution visualization**: Histograms, CDFs, violin plots for communicating uncertainty

### Combining distributions

When outcome Z = f(X, Y) for uncertain X and Y:

1. Sample N draws from X's distribution
2. Sample N draws from Y's distribution (jointly if correlated, independently if not)
3. Compute Z = f(X, Y) for each sample pair
4. Report percentiles of Z

**Example: "What will my OpenAI equity be worth after taxes?"**

```
Inputs:
- shares: 10,000 (known)
- price_per_share: Lognormal(mean=$150, std=$80) — uncertainty from valuation
- P(liquidity_event_by_2026): 60%
- tax_rate: 40% federal+state (if exercised as income)

Model:
  If no liquidity event: worth = $0 realized
  If liquidity event:
    gross = shares × price_per_share
    net = gross × (1 - tax_rate)

Simulation:
  for i in 1..10000:
    if random() < 0.6:  # liquidity event happens
      price = sample_lognormal(150, 80)
      net[i] = 10000 * price * 0.6
    else:
      net[i] = 0

Output:
  P(>$0): 60%
  Median (conditional on liquidity): $900k
  90% CI (conditional): $400k - $1.8M
  Expected value: $540k (includes 40% chance of $0)
```

**Correlation handling**: If X and Y are correlated (e.g., OpenAI valuation and probability of IPO both depend on AI market sentiment), model the common factor explicitly or use copulas.

### Complex probability networks

When a question involves interconnected uncertain variables, conditional dependencies, or state that evolves through stages—don't try to solve analytically. Model the network and simulate.

**Types of structures**:

- **Sequential processes**: state evolves step-by-step (portfolio drawdown, disease progression, project phases)
- **Event trees**: branching paths with probabilities at each node (immigration outcomes, startup funding rounds)
- **Bayesian networks**: variables with conditional dependencies (diagnosis given symptoms, success given multiple factors)
- **Queuing/waiting**: arrivals and processing with random timing (application processing, service times)

**General approach**:

1. Define the state variables and their dependencies
2. Define transition/update rules (deterministic functions of random inputs)
3. Sample all random inputs, propagate through the network
4. Collect the output distribution

**Example: Portfolio drawdown**

```
Inputs:
- initial_balance: $800,000
- allocation: 70% S&P 500, 30% bonds
- monthly_expenses: Normal(mean=$5000, std=$800)  # varies month to month
- stock_returns: sample from historical monthly S&P (mean ~0.8%, std ~4.5%)
- bond_returns: sample from historical monthly bonds (mean ~0.3%, std ~1.5%)
- correlation: stocks and bonds ~0.2 correlated (model jointly)

Process (per simulation):
  balance = initial_balance
  month = 0
  while balance > 0 and month < 600:  # cap at 50 years
    # Draw correlated returns
    stock_return, bond_return = sample_correlated(rho=0.2)
    portfolio_return = 0.7 * stock_return + 0.3 * bond_return

    # Draw expenses
    expenses = sample_normal(5000, 800)

    # Update
    balance = balance * (1 + portfolio_return) - expenses
    month += 1

  record time_to_ruin = month (or "never" if survived 50 years)

Run 10,000 simulations, output:
  P(never runs out in 50 years): 45%
  Median time to ruin (if it happens): 22 years
  10th percentile: 12 years (unlucky sequence)
  90th percentile: 40+ years

  Plot: survival curve (% still solvent vs time)
```

Key modeling choices:

- **Sequence risk**: Early bad returns hurt more (less capital to recover)
- **Expense shocks**: Can add P(major expense) for medical/home repair
- **Inflation**: Expenses drift upward ~3%/year
- **Drawdown strategy**: Fixed $ vs % of portfolio vs guardrails

## Evidence Handling

**Light questions** (quick/standard):

- Cite sources inline with URLs
- No file storage

**Heavy questions** (deep analysis, user requests):

- Create `docs/forecasts/<topic-slug>/` folder
- Store evidence files, synthesis document
- Only when explicitly warranted or requested

## Depth Adaptation

### Quick (~30 sec)

- Triggered by: "roughly", "ballpark", conversational tone
- 1-2 mental models, inline response

### Standard (2-5 min)

- Default for most questions
- WebSearch for base rates + markets
- Structured output with CI

### Deep (10+ min)

- Triggered by: "thorough", "deep dive", high-stakes context
- Extensive research, multiple sources
- Optional evidence folder
- Optional subagent delegation for parallel research
