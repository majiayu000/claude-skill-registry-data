---
name: evaluate-side-project
description: Use when evaluating, filtering, scoring, validating, or pressure-testing a side project, startup idea, app idea, AI product idea, MVP, weekend build, or one-sentence product concept before implementation.
---

# Evaluate Side Project

## Overview

Turn a rough side project idea into a structured build/no-build decision. Optimize for killing weak ideas early, sharpening promising ones, and keeping the MVP constrained to one measurable value proof.

## Input

Require one sentence describing the idea. If missing, ask for it before running the evaluation.

Optional context to use if provided: target user, pricing model, distribution channel, constraints, existing competitors, available build time.

## Workflow

Run all three checks in order. Be direct; do not make weak ideas sound better than they are.

### 1. Reddit Problem Mining

Generate 10 messy, emotionally charged, first-person vent phrases a real user might type when frustrated by the problem.

Rules:

- Use informal, specific, late-night language.
- Avoid marketing polish.
- Tie phrases to the proposed target user.
- Suggest 3-5 relevant subreddits or communities.
- List recurring themes to look for in posts and comments.
- Do not fabricate actual post URLs. If the user asks for real URLs, browse/search and label findings as sourced.

### 2. Kaufman 10-Factor Score

Score each factor from 1 to 10 and give 1-2 sentences explaining the score:

| Factor                    | What to judge                            |
| ------------------------- | ---------------------------------------- |
| Urgency                   | Do users actively seek relief now?       |
| Market Size               | Are there enough reachable buyers?       |
| Pricing Potential         | Will users pay enough to matter?         |
| Customer Acquisition Cost | Can users be reached cheaply?            |
| Cost of Value Delivery    | Is delivery cheap and scalable?          |
| Uniqueness                | Is the idea meaningfully differentiated? |
| Speed to Market           | Can a useful version launch quickly?     |
| Upfront Investment        | Can it start with low capital/time?      |
| Upsell Potential          | Can value expand after first use?        |
| Evergreen Potential       | Will the problem remain relevant?        |

Then total the score out of 100.

Interpretation:

- 80-100: strong candidate; validate fast.
- 60-79: plausible; fix weak factors before building.
- 40-59: risky; only build if learning value is high.
- Below 40: do not spend a weekend on it.

### 3. PASTA MVP Test

Define a one-feature MVP:

- Job Story: `When [situation], I want to [action], so I can [outcome].`
- Success metric: measurable and time-bound.
- Not-Doing list: exactly what is excluded from the MVP.
- Minimal scope: one user, one action, one result, one metric.
- PASTA Skeptic: ask 5 blunt first-time-user questions about value, speed, clarity, trust, and willingness to use/pay.
- Verdict: `PASS` or `FAIL` with one-line rationale.

## Output Format

```markdown
# Side Project Evaluation: [Idea]

## Verdict

- Decision: PASS/FAIL
- Score: [N]/100
- One-line rationale: [...]

## 1. Reddit Problem Mining

### Vent phrases

1. [...]

### Communities

- r/[...]: [...]

### Themes to look for

- [...]

## 2. Kaufman 10-Factor Score

| Factor  | Score | Rationale |
| ------- | ----: | --------- |
| Urgency |     N | ...       |

**Total:** [N]/100

**Summary:** [...]

## 3. PASTA MVP Test

**Job Story:** When [...], I want to [...], so I can [...].

**Success Metric:** [...]

**Not-Doing List:**

- [...]

**PASTA Skeptic Questions:**

1. [...]

**MVP Verdict:** PASS/FAIL - [...]

## Next Action

[One concrete next step: research, interview, landing page, smoke test, or kill.]
```

## Quality Bar

- Prefer a clear `FAIL` over a polite maybe.
- Call out assumptions explicitly.
- Separate evidence from guesses.
- Keep scope small enough to test in one week.
- If two ideas are provided, run the full evaluation for each and recommend the higher-scoring idea.
