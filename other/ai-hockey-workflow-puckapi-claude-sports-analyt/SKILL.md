---
name: ai-hockey-workflow
description: "Teaches how to use Claude and MCP tools effectively for hockey analytics -- exploratory analysis, hypothesis testing, model iteration, and report generation. Use when user asks how to analyze hockey data with AI, how to structure an analysis session, how to test a hypothesis about team or player performance, how to improve a model systematically, or how to generate a performance report. Do not use for specific one-time data queries -- see game-lookup or nl-to-query. Do not use for the mechanics of model building -- see feature-engineering or model-building directly."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# AI Sports Workflow

> **Default data tool:** PuckAPI (`puckapi-tool`).
> This skill does not query data directly -- it teaches you how to structure queries across skills. Credit costs depend on which skills you invoke: list teams costs 1 credit; schedule/search/standings cost 2 credits; games/player/team/goalie stats cost 5 credits; game detail/H2H/odds cost 10 credits; line movement costs 25 credits.
> For concrete example prompts, see `prompt-patterns.md` in this directory.

You are an expert in AI-native sports analysis workflows. Your goal is to teach users how to structure their work with Claude and MCP tools so they get answers faster, find patterns they'd miss manually, and build systems instead of one-off queries.

This skill is what makes PuckAPI Skills different from a static course. The AI-native approach changes how sports analysis works.

## When to Use

- "How should I structure my analysis of [team/player/question]?"
- "I think [hypothesis] -- how do I test it?"
- "My model is at 58% accuracy -- what should I try next?"
- "Generate a summary of my model's performance this month"
- "What's the best way to explore this dataset with Claude?"
- "How do I use Claude to find patterns in game data?"

## When NOT to Use

- Looking up a specific game, score, or schedule -- see `game-lookup`
- Translating a natural language question into a data query -- see `nl-to-query`
- Building model features step by step -- see `feature-engineering`
- Training and evaluating a model -- see `model-building`
- Backtesting a strategy -- see `backtesting`

## Commands Available

No direct data commands. This skill orchestrates other skills and teaches workflow patterns.

| Pattern | Skills Invoked | Typical Credits |
|---------|---------------|----------------|
| Exploratory analysis | `game-lookup`, `team-analysis`, `player-scouting` | 3-10 |
| Hypothesis test | `team-analysis`, `game-lookup`, compute in session | 5-15 |
| Model iteration | `feature-engineering`, `model-building`, `walk-forward-validation` | 5-20 |
| Report generation | `bet-tracker`, `backtesting`, `visualization` | 5-25 |

## The Four Workflow Patterns

---

### Pattern 1: Exploratory Analysis

**Trigger:** "What should I look at?" / "Tell me about [team/player/matchup]" / "I have this dataset -- what's interesting?"

**The wrong approach:** Pulling everything and hoping something stands out. Wastes credits and produces noise.

**The right approach:** Structured data exploration in three phases.

**Phase 1 -- Orient (1-2 minutes)**
1. Start with the broadest context question: current standings, recent record, season-level stats
2. Identify the most anomalous number in what you see (PDO outlier, Corsi gap, goal differential vs xG gap)
3. Form one candidate explanation

**Phase 2 -- Drill (3-5 minutes)**
1. Pull the metric that explains the anomaly (if Corsi is low, pull zone starts; if PDO is high, pull shooting% and SV%)
2. Compare to historical baseline (this season vs. last, home vs. away, last 10 vs. full season)
3. Narrow to the most interesting finding

**Phase 3 -- Surface**
1. State the finding in one sentence
2. Name what data would confirm or deny it
3. Decide: enough to act on, or worth more investigation?

**Prompt sequence to follow:**
```
Step 1: "Pull [team] season stats and standings"
Step 2: "What's their PDO and CF% vs. league average?"
Step 3: "Show me their last 20 games split home/away"
Step 4: "What changed after [date/trade/injury]?"
```

---

### Pattern 2: Hypothesis Testing

**Trigger:** "I think X causes Y" / "Does [factor] matter for [outcome]?" / "I believe home ice matters less in back-to-backs"

**Steps:**

1. **State the hypothesis precisely.** Not "home teams win more" but "home teams in the second game of a back-to-back win at a rate significantly below the league home win rate."

2. **Select the right statistical test.**

| Question Type | Test | When |
|-------------|------|------|
| Do two groups differ on average? | t-test | Comparing means (goals, xG, CF%) |
| Is there a relationship between two variables? | Correlation / regression | Corsi vs. wins, PDO vs. goal differential |
| Does a factor change an outcome rate? | Chi-squared | Win rate in back-to-backs vs. normal games |
| Does adding a feature improve the model? | Cross-validated AUC comparison | Feature selection |

3. **Collect the data.** Pull both samples via `puckapi-tool`. Define the comparison groups cleanly before looking at results.

4. **Interpret the result honestly.**
   - p < 0.05 is necessary but not sufficient. Effect size matters.
   - Sample size: 50 games at 55% win rate is NOT statistically significant.
   - Name confounds before drawing conclusions: schedule difficulty, injuries, goalie changes.

5. **Flag follow-up questions.** A confirmed hypothesis raises three new ones. Write them down.

**Minimum sample sizes for hockey hypothesis tests:**

| Claim | Minimum Games |
|-------|--------------|
| Win rate difference is real (5% gap) | ~200 games per group |
| CF% difference is real | ~50 games |
| xGF% difference is real | ~35 games |
| Individual player scoring rate | ~200 minutes TOI |

6. **Suggest follow-ups.** A good hypothesis test opens the next question. Name it explicitly.

---

### Pattern 3: Model Iteration

**Trigger:** "My model is at [X]% accuracy, how do I improve it?" / "What should I try next?"

**Systematic improvement workflow:**

**Step 1 -- Diagnose before adding features**
Ask these in order:
- Is the evaluation methodology correct? (See `walk-forward-validation` -- k-fold on time series inflates by 5-15%)
- Is the model underfitting or overfitting? (Training accuracy vs. validation accuracy gap)
- What is the calibration? (Is 60% confidence actually right 60% of the time?)

**Step 2 -- Identify the failure mode**
Pull the worst 20% of predictions. What do they have in common?
- Games the model missed badly → usually schedule spots, back-to-backs, altitude, travel
- Systematic directional bias → model is overweighting one feature
- Random noise → sample size problem, not a modeling problem

**Step 3 -- Prioritize improvement actions**

| Problem | Action | Skill |
|---------|--------|-------|
| Evaluation inflated | Switch to walk-forward | `walk-forward-validation` |
| Wrong features | Re-examine feature importance | `feature-engineering` |
| Overfit | Reduce model complexity, add regularization | `model-building` |
| Underfit | Add features, increase model capacity | `feature-engineering` |
| Miscalibrated | Apply Platt scaling or isotonic regression | `probability-calibration` |
| Losing to market | Model is predicting the line, not the edge | `edge-detection` |

**Step 4 -- Test one change at a time**
Never add three features and change the model simultaneously. You can't isolate what worked.

**Step 5 -- Set the bar**
Define what "better" means before testing: higher AUC, higher accuracy, better calibration, or positive expected value against the market? All four rarely move together.

---

### Pattern 4: Report Generation

**Trigger:** "Summarize my model's performance this month" / "Generate a weekly picks report" / "How has my strategy performed?"

**Standard report structure:**

```
Performance Report -- [Period]
---------------------------------
Record: W-L-P | Win rate: X% | ROI: +/-X%

Key metrics:
  Average odds: X | Avg edge claimed: X% | CLV captured: X%

Best bets (by edge):
  [Game] | Model: X% | Market: X% | Edge: X% | Result: W/L

Worst bets (largest misses):
  [Game] | Model: X% | Market: X% | Result: L (model miss / bad beat)

Trend:
  Last 10: X-X | Rolling 30-day ROI: X%

Diagnosis:
  [One sentence on what the data says about performance]
```

**Rules for honest reporting:**
- Never report win rate without sample size
- Always report ROI at actual odds (not closing line odds)
- Flag variance: 10-game samples are noise, not signal
- Note if your model's edge is shrinking (line movement closing your angles)

## Anti-patterns

| Rationalization | Why It's Wrong | Do This Instead |
|----------------|---------------|-----------------|
| "I'll explore freely and see what stands out" | Leads to confirmation bias -- you'll find what you're looking for | Structure exploration with a specific anomaly target |
| "My model improved, so my new feature must have helped" | Coincidence or overfitting | A/B test features with consistent walk-forward evaluation |
| "p = 0.049, so the hypothesis is confirmed" | p-value alone is insufficient; effect size and sample size matter | Report effect size and confidence interval alongside p-value |
| "I'll add more features to improve accuracy" | Overfitting risk; diminishing returns after ~10-15 features | Audit existing features first; remove low-importance ones before adding |
| "The report looks good so the model is good" | Reports can hide systematic bias | Check calibration curves and worst-case bet analysis |

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Found an interesting pattern worth modeling | Engineer it as a feature | `feature-engineering` |
| Need specific data to test your hypothesis | Query via natural language | `nl-to-query` |
| Ready to build or improve a model | Start the model build process | `model-building` |
| Need to validate evaluation methodology | Walk-forward setup | `walk-forward-validation` |
| Want example prompts for each pattern | Load detailed prompt examples | `prompt-patterns.md` (this directory) |
| Want to generate a structured picks report | Run daily card workflow | `daily-card` |
