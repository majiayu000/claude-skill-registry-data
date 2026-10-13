---
name: adversarial-debate
description: "AGI: FREE-MAD adversarial debate protocol — three agents (Bull/Bear/Market) stress-test any investment thesis using heterogeneous models. Triggers when user asks to 'debate', 'stress test', 'devil's advocate', 'bull bear case', 'challenge this thesis', 'poke holes in', or any request to evaluate an investment from multiple angles. Also triggers on 'what could go wrong', 'what am I missing', 'counter-argument', or 'is this a good investment'."
---

# Adversarial Investment Debate (FREE-MAD Protocol)

Structured three-agent debate for investment thesis stress-testing. Based on FREE-MAD (Free-form Multi-Agent Debate) research showing 91% accuracy with heterogeneous models vs. 82% for single-model analysis.

## Prerequisites

- Read `_shared/plugin-context.md` for domain vocabulary and data sources
- Available MCP tools: BigData.com, Nexus MCP (optional), PitchBook (optional)
- Works with or without MCP — debate can use uploaded documents or manually provided data

## Protocol Overview

```
Data Collection → Bull Presents → Bear Challenges → Bull Rebuts → Bear Final → Market Synthesizes
     (parallel)        (round 1)       (round 2)       (round 3)     (round 4)      (round 5)
```

## Phase 0: Data Collection

Before the debate, gather a shared fact base using all available sources:

1. **Company financials**: revenue, EBITDA, margins, leverage, FCF (BigData.com, Nexus MCP, uploaded docs)
2. **Market context**: sector trends, peer performance, macro environment (BigData.com, LSEG, web search)
3. **Credit/risk data**: ratings, spread levels, default rates (Moody's, BigData.com)
4. **Deal specifics**: price, structure, terms (Nexus MCP, uploaded materials)
5. **Recent news**: earnings, events, catalysts (BigData.com, Aiera, web search)

All three agents share the same fact base. They disagree on **interpretation**, not data.

## Phase 1: Bull Agent (Round 1)

**System prompt**: "You are the Bull agent. Your role is to construct the strongest possible case FOR this investment. Present your thesis with specific evidence, quantitative support, and historical precedents. Be thorough and persuasive, but honest — acknowledge at least 2 genuine risks even while advocating."

**Output structure**:
- Core thesis statement (1-2 sentences)
- 5-8 supporting arguments, each with:
  - Claim
  - Evidence (specific data points)
  - Quantitative backing (multiples, returns, margins)
- Upside catalysts with timeline
- Favorable comparisons (successful precedents)
- Acknowledged risks (at least 2)

## Phase 2: Bear Agent (Round 2)

**System prompt**: "You are the Bear agent operating in ANTI-CONFORMITY MODE. You are explicitly instructed to DISAGREE with the Bull case. Your job is to find flaws, contrary evidence, and risks that the Bull agent minimized or ignored. Challenge every assumption. Find counter-examples. Stress-test the financials. Do NOT converge with the Bull agent's view. Acknowledge at least 1 genuine strength even while attacking."

**FREE-MAD anti-conformity rules**:
- Must challenge EVERY Bull argument (no silent agreement)
- Must provide counter-evidence, not just skepticism
- Must quantify downside scenarios
- Must identify the single biggest reason this investment fails

**Output structure**:
- Point-by-point rebuttal of each Bull argument:
  - Bull claim → Bear counter-evidence
  - Financial stress test (what if margins compress 200bps? revenue declines 10%?)
- Overlooked risks the Bull ignored
- Counter-comparables (failed investments with similar thesis)
- "If wrong about nothing else, I'm right about THIS" — the killer risk
- Acknowledged strength (at least 1)

## Phase 3: Bull Rebuttal (Round 3)

**System prompt**: "The Bear agent has challenged your thesis. Review each challenge and either defend your position with additional evidence or concede the point. Be intellectually honest — conceding weak points strengthens your remaining arguments. Focus your defense on the strongest elements of your thesis."

**Output structure**:
- Response to each Bear challenge:
  - Defended (with new evidence) OR
  - Conceded (with mitigant framing — "yes, but...")
- Reinforcement of strongest surviving arguments
- Updated thesis incorporating Bear's valid points

## Phase 4: Bear Final Challenge (Round 4)

**System prompt**: "The Bull agent has rebutted your challenges. Deliver your FINAL objections — the strongest remaining concerns after hearing the rebuttal. Focus on the 2-3 points that the Bull could NOT adequately address. These are the risks an investor must accept if they proceed."

**Output structure**:
- 2-3 strongest remaining objections
- Why the Bull's rebuttal was insufficient for each
- The irreducible risk an investor must accept
- Recommendation: Proceed with caution / Do not proceed / Proceed only if [condition]

## Phase 5: Market Agent Synthesis (Round 5)

**System prompt**: "You are the Market agent. You have observed the full 4-round debate between Bull and Bear. Your role is to objectively weigh both sides and produce a synthesized view. Identify which Bull arguments SURVIVED Bear's scrutiny, which Bear risks are MATERIAL vs. theoretical, and produce the final defensible investment view. Apply confidence calibration."

**Output structure**:
- **Surviving Bull Arguments**: Which points held up under challenge
- **Material Bear Risks**: Which risks are genuine, not just theoretical
- **Dismissed Arguments**: Bull claims that were effectively rebutted
- **Dismissed Risks**: Bear concerns that were adequately addressed
- **Synthesized View**: The defensible investment thesis after debate
- **Killer Risks**: 1-2 risks that could not be rebutted and must be monitored
- **Confidence Assessment**: Three-pass calibrated score per `confidence-calibration` skill

## Heterogeneous Model Selection

For maximum accuracy, use different model families for each agent:

| Agent | Preferred Model | Fallback |
|-------|----------------|----------|
| Bull | Claude Opus | Claude Sonnet |
| Bear | GPT-5.4 | Gemini 3 Pro |
| Market | Gemini 3 Pro | Claude Opus |

If only one model is available, the debate still works — but with lower accuracy (82% vs. 91% for heterogeneous models). The anti-conformity prompting provides value even with a single model.

## Quality Checks

1. **Bear challenged every Bull argument** — no silent agreement
2. **Bull conceded at least 1 point** — intellectual honesty
3. **Market referenced specific debate moments** — not a generic summary
4. **Confidence score reflects debate outcome** — high agreement = higher confidence
5. **Data gaps identified** — what additional data would resolve remaining disagreements
6. **Killer risks are specific and actionable** — not vague concerns
7. **Surviving thesis is narrower than original** — debate should sharpen, not confirm

## Integration

- Called by `/nexus-debate` command
- Called by `debate-team` agent
- Available as `nexus_debate_thesis` MCP tool via Nexus remote server
- Can be invoked mid-analysis by any other skill when thesis stress-testing is needed
