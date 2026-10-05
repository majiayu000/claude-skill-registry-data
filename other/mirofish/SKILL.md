---
name: mirofish
description: "MiroFish swarm intelligence — dual-mode: (1) web research swarm with parallel WebSearch, (2) prediction/forecasting engine with multi-agent perspective simulation, scenario modeling, and probability-weighted outcomes."
triggers:
  - "research"
  - "deep dive"
  - "investigate"
  - "comprehensive search"
  - "thorough research"
  - "swarm search"
  - "mirofish"
  - "predict"
  - "forecast"
  - "what if"
  - "scenario analysis"
  - "what would happen"
  - "future prediction"
  - "simulate outcome"
linksTo:
  - "context-engineering"
  - "research"
  - "ai-agents"
  - "rag"
  - "sequential-thinking"
  - "make-decision"
---

# MiroFish — Swarm Intelligence Engine

> Dual-mode: **Research Swarm** + **Prediction Engine**.
> Inspired by [MiroFish](https://github.com/666ghj/MiroFish) multi-agent simulation.

## Mode Detection

| User says | Mode |
|-----------|------|
| "research X", "investigate", "deep dive", "what do we know about" | **Research** |
| "predict", "forecast", "what if", "what would happen if", "scenario", "simulate" | **Predict** |
| "mirofish" (no qualifier) | Ask which mode |

---

# MODE 1: Research Swarm

```
Question → Query Generation → Parallel Search → Deep Fetch → Synthesis → Report
```

## Research Protocol

### Step 1: Parse Research Question
Identify core topic, scope, time sensitivity, domain.

### Step 2: Generate 5-8 Diverse Search Queries
| Angle | Example |
|-------|---------|
| **Factual** | "[topic] statistics data 2024 2025" |
| **Contrarian** | "[topic] problems failures criticism" |
| **Data-driven** | "[topic] ROI metrics studies" |
| **Historical** | "history of [topic] evolution timeline" |
| **Expert opinion** | "[topic] expert analysis leaders opinions" |
| **Geographic** | "[topic] by country region comparison" |
| **Regulatory** | "[topic] laws regulations policy" |
| **Future-looking** | "[topic] predictions trends forecast 2026" |

### Step 3: Execute ALL Searches in Parallel
Use WebSearch for ALL queries simultaneously in a single message. This is the swarm.

### Step 4: Deep Fetch Top 3-5 Sources
WebFetch authoritative URLs in parallel. Priority: academic > industry reports > government > news.

### Step 5: Synthesize Report
```markdown
## Research Report: [Topic]
### Consensus View — [cited]
### Divergent Views — [cited]
### Key Data Points — [stat + source]
### Timeline
### Confidence: High / Medium / Low / Gaps
### Sources: [numbered, linked]
```

### Step 6: Save to Memory
Category: "research", Importance: 7, Tags: ["#research", "#mirofish"]

---

# MODE 2: Prediction / Forecasting Engine

```
Question → Data Gathering → Variable Mapping → Agent Perspectives → Scenario Modeling → Prediction Report
    │            │                │                    │                    │                  │
 "what if    WebSearch for     identify key       6-8 archetypes     3 scenarios        weighted
  X happens"  baseline data    variables &        each reasons       (base/bull/bear)   consensus
                               causal links       independently      with probabilities
```

## Prediction Protocol

### Step 1: Frame the Prediction Question
Decompose into:
- **Subject**: What entity/system is being predicted?
- **Intervention**: What change/event triggers the prediction?
- **Outcome variable**: What specifically are we predicting?
- **Time horizon**: When? (weeks, months, years)
- **Baseline**: What is the current state?

Example: "What happens to tech stocks if Fed raises rates 50bps?"
→ Subject: tech stocks (NASDAQ composite)
→ Intervention: Fed funds rate +50bps
→ Outcome: price movement (%, direction)
→ Time horizon: 6 months
→ Baseline: current rate, current NASDAQ level

### Step 2: Data Gathering (Research Swarm)
Run 5-8 parallel WebSearches focused on:
- Current state of the subject
- Historical precedents for the intervention
- Expert forecasts on related topics
- Contrarian/minority views
- Second-order effects data

This feeds real data into the prediction — not hallucinated priors.

### Step 3: Variable Mapping
Identify the **causal chain** from intervention → outcome:

```
[Intervention]
    ↓
[First-order effects] — direct, immediate
    ↓
[Second-order effects] — indirect, delayed
    ↓
[Feedback loops] — self-reinforcing or dampening
    ↓
[Outcome variable]
```

For each link, note:
- Direction (positive/negative)
- Magnitude (strong/moderate/weak)
- Confidence (data-backed or speculative)
- Time lag

### Step 4: Multi-Agent Perspective Simulation
Reason through the prediction from **6-8 distinct archetypes**, each with different priors, biases, and information weighting. Each agent MUST produce a specific prediction (number or range) with reasoning.

| Agent | Perspective | Weighs heavily |
|-------|-------------|----------------|
| **The Historian** | "This has happened before" | Historical precedent, base rates, mean reversion |
| **The Optimist** | "Markets/systems adapt" | Innovation, resilience, positive adaptation |
| **The Pessimist** | "Tail risks are underpriced" | Downside scenarios, fragility, cascading failures |
| **The Contrarian** | "Consensus is wrong because..." | Where the crowd might be systematically biased |
| **The Quant** | "The numbers say..." | Data, correlations, statistical relationships |
| **The Insider** | "Having seen this from inside..." | Domain expertise, operational knowledge |
| **The Systems Thinker** | "Second-order effects matter most" | Feedback loops, emergent behavior, non-linear dynamics |
| **The Geopolitical Analyst** | "External forces dominate" | Regulatory, political, macro forces |

For each agent, produce:
```
**[Agent Name]**: [Specific prediction with number/range]
Reasoning: [2-3 sentences]
Key assumption: [What must be true for this to hold]
Confidence: [0.0-1.0]
```

### Step 5: Scenario Modeling
Synthesize agents into **3 weighted scenarios**:

#### Bear Case (probability: X%)
- What happens: [specific outcome]
- Key drivers: [which agents' logic dominates]
- Trigger conditions: [what would cause this]

#### Base Case (probability: X%)
- What happens: [specific outcome]
- Key drivers: [weighted consensus]
- Assumptions: [what must hold]

#### Bull Case (probability: X%)
- What happens: [specific outcome]
- Key drivers: [which agents' logic dominates]
- Trigger conditions: [what would cause this]

Probabilities MUST sum to ~100%. Assign based on:
- Number of agents aligned with each scenario
- Strength of historical precedent
- Quality of supporting data

### Step 6: Prediction Report

```markdown
## Prediction Report: [Question]

### Question
[Full prediction question with time horizon]

### Baseline
[Current state with data, sourced]

### Causal Chain
[Intervention] → [Effect 1] → [Effect 2] → [Outcome]
Confidence in chain: X/10

### Agent Perspectives
| Agent | Prediction | Confidence | Key Assumption |
|-------|-----------|------------|----------------|
| Historian | ... | 0.X | ... |
| Optimist | ... | 0.X | ... |
| ... | ... | ... | ... |

### Scenarios
**Bear (X%)**: [outcome + reasoning]
**Base (X%)**: [outcome + reasoning]
**Bull (X%)**: [outcome + reasoning]

### Consensus Prediction
[Probability-weighted outcome]
Overall confidence: X/10
Time horizon: [when]

### Key Risks / What Would Change This
1. [Risk that invalidates prediction]
2. [New information to watch for]
3. [Leading indicator to monitor]

### Sources
[Numbered, linked — from data gathering phase]
```

### Step 7: Save Prediction to Memory
```
Category: "prediction"
Importance: 8
Tags: ["#prediction", "#mirofish", "#[subject]", "#[timeframe]"]
Content: "[Question] → [Consensus prediction] (confidence: X/10, base case: Y%)"
```

Also save as a **decision** if it informs a real choice:
```bash
npx tsx ./memory/scripts/memory-runner.ts decision "[title]" "[prediction summary]" "[context]"
```

---

## Quality Rules (Both Modes)

- **Minimum 5 parallel searches** — fewer is not a swarm
- **Always cite sources** — no unsourced claims in data gathering
- **Include contrarian views** — confirmation bias kills predictions
- **Specific numbers** — "stocks will decline" is not a prediction; "NASDAQ -8% to -15% over 6mo" is
- **Explicit confidence** — every claim and every agent gets a confidence score
- **Time-bound** — every prediction has a deadline for verification
- **Save to memory** — predictions are expensive, track them for calibration
- **Acknowledge uncertainty** — wide confidence intervals are honest, not weak

## Anti-Patterns

- Do NOT skip the data gathering phase — predictions without data are just vibes
- Do NOT let all agents agree — if they do, you haven't made them distinct enough
- Do NOT assign equal probabilities to all scenarios — that's a cop-out
- Do NOT predict without a time horizon — "eventually" is not a forecast
- Do NOT present research mode output as prediction — they are different products
