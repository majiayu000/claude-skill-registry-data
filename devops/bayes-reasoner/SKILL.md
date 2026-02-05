---
name: bayes-reasoner
description: An internal cognitive engine for quantitative root cause analysis. Use this autonomously when you need to weigh competing hypotheses, prevent anchoring bias, or determine the most efficient next diagnostic step.
---

# Bayes Reasoner (Agent Protocol)

This is an **internal reasoning tool** for you, the agent. It provides a mathematical scratchpad to prevent cognitive limitations when reasoning under uncertainty—specifically anchoring on first impressions or flip-flopping based on recent inputs.

**Role:** You are the investigator. The Python script is your calculator. The user is a stakeholder who wants realistic probability distributions, not overconfident guesses or vague hedging.

## State Management

State is stored in `.claude/.bayes_state.json` relative to the current working directory. This creates a project-local audit trail.

## CLI Reference

Script location: `~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py`

All commands support `--json` for machine-readable output.

### `init` — Initialize Hypotheses

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py init H1:prob H2:prob ...
```

Probabilities are normalized automatically. Use rough estimates based on base rates and initial evidence.

**You MUST include an "Other" hypothesis.** A closed hypothesis space assumes one of your guesses is definitely correct—this is rarely true. Reserve 10–20% for unlisted causes.

**Example:**
```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py init Database:0.35 Network:0.30 CodeBug:0.20 Other:0.15
```

### `define` — Define a Test

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py define TestName H1:likelihood H2:likelihood ...
```

Likelihoods represent **P(test passes | hypothesis is true)**. Values must be between 0 and 1.

- Unmentioned hypotheses default to 0.5 (neutral evidence)
- Tests persist after use—you can apply the same test to multiple evidence instances

**Example:**
```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py define CheckErrorLogs Network:0.9 Database:0.3 CodeBug:0.1
```
*"If it's a Network issue, there's a 90% chance the logs show timeout errors."*

### `recommend` — Get Optimal Next Test

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py recommend
```

Returns tests ranked by **Expected Information Gain** (in bits). Higher is better—these tests most efficiently discriminate between hypotheses.

### `update` — Apply Evidence

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py update TestName result
```

**Result values:**
- Positive: `true`, `pass`, `yes`, `1`
- Negative: `false`, `fail`, `no`, `0`

The test definition is preserved for reuse.

**Example:**
```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py update CheckErrorLogs pass
```

### `status` — View Current State

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py status
```

Shows current probability distribution and defined tests.

### `undefine` — Remove a Test

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py undefine TestName
```

### `split` — Refine a Named Hypothesis Into Sub-Categories

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py split SourceHypothesis NewH1:ratio NewH2:ratio ...
```

Replaces a *named, concrete* hypothesis with more specific sub-hypotheses, redistributing its probability mass.

**Do NOT split "Other."** "Other" is not a hypothesis—it's an admission of model incompleteness. When you identify a new candidate cause, use `inject` instead (see below). This ensures the new hypothesis gets probability based on evidence strength, not artificially capped by Other's current value.

**Example:**
```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py split Network NetworkTimeout:0.6 NetworkDNS:0.4
```
*Replaces "Network" entirely with two specific sub-hypotheses.*

**Note:** Existing tests will use likelihood=0.5 (neutral) for new hypotheses. Consider redefining tests with specific likelihoods.

### `inject` — Add New Hypothesis Based on Evidence

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py inject Hypothesis:probability [--likelihoods Test1:L1 Test2:L2 ...]
```

Adds a new hypothesis at the specified probability, **shrinking all existing hypotheses proportionally** to make room. Use this when:
- You've identified a new candidate cause (including from investigating what "Other" might be)
- A smoking gun emerges that demands a high-probability new hypothesis
- Evidence points to something outside your current named hypotheses

The probability you assign should reflect the evidence strength given all context, not be constrained by any existing hypothesis's current value.

**If tests are already defined, you MUST provide `--likelihoods`** for the new hypothesis on each test. This ensures future `recommend` calculations remain valid. Ask yourself: "If this new hypothesis were true, what's the probability each test would pass?"

**Examples:**
```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py inject DNS:0.25 --likelihoods CheckLogs:0.7 PingTest:0.3
```
*Adds DNS at 25% with explicit likelihoods for existing tests.*

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py inject BuildCache:0.90 --likelihoods CheckLogs:0.1 PingTest:0.5
```
*Smoking gun: adds BuildCache at 90%, crushes everything else to 10% total (preserving relative ordering).*

**Note:** The injected probability must be less than 1. If no tests are defined, `--likelihoods` is not required.

### `reset` — Clear All State

```
python3 ~/.claude/skills/bayes-reasoner/scripts/bayes_engine.py reset
```

## Operational Procedure

Execute these steps autonomously. **Do not** show CLI commands to the user. **Do not** ask the user to run these commands.

### 1. Initialization

When a complex problem with multiple potential causes is presented:

1. Parse the issue into distinct, mutually exclusive hypotheses
2. **Always include an "Other" hypothesis** (10–20% prior) to represent causes outside your named categories
3. Assign prior probabilities based on your knowledge of base rates
4. Run `init` with your estimates

### 2. Strategic Planning

1. Brainstorm possible tests/checks
2. For each test, estimate: "If Hypothesis X is true, what's the probability this test passes?"
3. Run `define` for each test
4. Run `recommend` to identify the highest information-gain test

### 3. Execution

1. Perform the recommended test yourself (if possible) or ask the user to perform it
2. **Explain why** you're choosing this test: "I recommend checking X first because it most effectively distinguishes between the Database and Network hypotheses."

### 4. Update

1. Run `update` with the test result
2. Run `status` to see the new distribution
3. Report the shift naturally: "That timeout error makes Network issues significantly more likely (now ~75%, up from 35%)."
4. Repeat from step 2 until one hypothesis dominates or you have enough confidence to act

## Rules of Engagement

1. **Invisible Tooling:** The user sees insights, not CLI commands. Hide the mechanics; show the reasoning.

2. **Trust the Math:** If your intuition contradicts the calculated posteriors, either trust the math or explicitly revise your likelihood definitions. Do not silently override.

3. **Handle Impossibilities:** If `update` returns "Evidence impossible under all hypotheses," your model is wrong. Tell the user you need to "re-evaluate the problem space" and reinitialize with revised hypotheses.

4. **Communicate Uncertainty:** Report probabilities, not certainties. "The evidence suggests X (85% likely)" is better than "It's definitely X."

5. **Watch "Other":** If "Other" starts climbing, your named hypotheses don't fit the data well. Brainstorm what concrete causes might be hiding in "Other", then use `inject` to add them at evidence-appropriate probabilities.

6. **Never Split "Other":** "Other" is not a hypothesis—it's model incompleteness. When you identify a new candidate cause, `inject` it at a probability reflecting the evidence. Don't artificially cap it at whatever "Other" happened to be. Use `split` only for refining named hypotheses into sub-categories (e.g., "Network" → "NetworkTimeout" + "NetworkDNS").
