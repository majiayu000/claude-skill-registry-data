---
name: game-design-reality-check
description: Stress-test game concepts, gameplay proposals, feature specs, loops, systems, levels, and pitch claims by separating design logic from assumptions and evidence. Use when Codex should challenge whether a design is likely to work, expose self-confirming "this will be fun" reasoning, trace goals to means and tools, or define the cheapest prototype and playtest needed to validate it.
---

# Game Design Reality Check

Treat every claim about fun, novelty, tension, immersion, depth, retention, audience fit, or production feasibility as a hypothesis until relevant evidence supports it. The purpose is not to be negative or to predict fun from a document. It is to separate coherent design logic from wishful thinking, identify the weakest assumption, and turn uncertainty into a practical validation step.

Use GMT (Goal–Means–Tools) as the internal causal map, not as the public identity of the skill and not as a rigid doctrine.

## Choose the review mode

- **Quick Reality Check**: identify the central promise, three largest assumptions, likely first failure, and next test.
- **Full Design Review**: inspect goals, causal chains, evidence, contradictions, feasibility, and priorities.
- **Validation Design**: convert one important uncertainty into a greybox, playtest, metric, and decision rule.
- **Evidence Update**: review prototype observations, playtest notes, telemetry, or market evidence and revise the prior judgment.

Use the lightest mode that answers the request. Do not produce a large report when the user asks a narrow question.

For a substantive review, read `references/reality-check-framework.md`. Read `references/gmt-framework.md` when building or diagnosing the Goal–Means–Tools map. Read `references/review-output.md` for a formal report, scoring table, pitch review, or action plan.

## Normalize the design claim

Extract or infer, while labeling inference:

- the game or feature being proposed;
- target player and play context;
- player goal, intended experience, and design/product goal;
- the repeated decision or behavior expected from the player;
- the mechanisms, content, feedback, and production work claimed to create it;
- platform, controls, player count, session structure, team, schedule, and constraints;
- available evidence and requested decision.

Do not block on ordinary gaps. State material assumptions. Ask a question only when different answers would materially change the judgment and no safe assumption exists.

## Run the reality check

### 1. Rewrite promises as falsifiable hypotheses

Replace vague claims such as “the combat is strategic” or “players will feel attached” with:

```text
For [target player] in [situation],
[mechanism or content] is expected to cause [observable behavior],
which would support [intended experience or design result].
We would doubt this when [failure signal or alternative explanation].
```

Do not equate stated preference, designer enthusiasm, feature quantity, production effort, novelty, or thematic appeal with player experience.

### 2. Build the causal map

Separate player goal, experience goal, and design/product goal. For each important goal, map:

`Goal → high-level Means → concrete Tools → expected player behavior → claimed outcome`

Check whether every arrow has a plausible causal explanation. Identify missing means, missing tools, orphan features, contradictions, vague verbs, dominant strategies, and claims that depend mainly on execution quality or content volume.

GMT coherence is necessary for a readable proposal but does not prove fun.

### 3. Build an evidence ledger

Label each important statement as one of:

- **Observed**: directly seen in a relevant prototype, playtest, telemetry, or shipped result.
- **Sourced**: supported by a relevant comparable, research source, or reliable external record.
- **Derived**: follows from explicit rules or constraints but is not yet observed in player behavior.
- **Assumed**: plausible belief without adequate evidence.
- **Unknown**: missing information that prevents judgment.

Record relevance and limitations. Never invent playtest results, metrics, market facts, player motives, or certainty. One enthusiastic anecdote is evidence of that session, not proof of broad audience fit.

### 4. Try to make the design fail

Actively test alternative explanations and failure cases:

- players optimize away the intended experience;
- the claimed choice has one obvious answer;
- feedback is too weak, delayed, or ambiguous for learning;
- novelty lasts only until the rule is understood;
- the emotional outcome depends on presentation not represented in the prototype;
- content burden, technical quality, onboarding, accessibility, or matchmaking exceeds capacity;
- retention or monetization claims are inferred from moment-to-moment fun;
- the designer’s knowledge hides information new players will not have.

Challenge the claim, not the designer. Preserve deliberate tradeoffs and unconventional goals when their consequences are understood.

### 5. Judge the weakest link

Use these verdicts rather than “good/bad” or “fun/not fun”:

- **Unexamined**: the core claim is vague or its causal chain is missing.
- **Plausible but unproven**: the logic can work, but decisive evidence is absent.
- **Test-ready**: the hypothesis, prototype isolation, signals, and decision rule are clear.
- **Provisionally supported**: relevant evidence supports the claim within stated limits.
- **Contradicted**: relevant evidence or the explicit rules conflict with the claim.

Name confidence and what would change the judgment. The overall judgment should follow the earliest or most consequential broken link, not an average score.

### 6. Define the cheapest decisive test

Design the smallest test that can change a real decision:

- one central hypothesis;
- minimum mechanics and content needed to expose it;
- exclusions that prevent polishing from hiding the issue;
- representative participant criteria and play context;
- behaviors to observe before asking opinions;
- useful qualitative questions and quantitative signals;
- pass, revise, and stop thresholds where justified;
- likely confounds and alternative explanations;
- the product or design decision attached to each outcome.

Prefer behavioral evidence over “Did you have fun?” Ask what players tried, noticed, predicted, chose, repeated, avoided, misunderstood, and discussed.

## Prioritize recommendations

Order findings by decision value:

1. core goal or causal-chain break;
2. central assumption with high impact and little evidence;
3. prototype or playtest needed before more production;
4. feasibility, scope, balance, usability, or content risk;
5. optional opportunity or polish.

Recommend removing, simplifying, isolating, testing, or revising before adding features. Do not “fix” an unproven design by expanding its scope.

## Response rules

- Lead with the reality-check verdict and the single most important reason.
- Separate facts, observations, derivations, assumptions, and unknowns.
- Quote or point to proposal evidence when available.
- Explain causal breaks in plain language; use GMT terminology only when it helps.
- Distinguish a document problem from a design problem and both from missing evidence.
- State what the review cannot establish.
- End with the next decision and the lowest-cost evidence needed to make it.

## Limits

A document review cannot establish fun, emotional impact, balance, usability, retention, market fit, or production quality. GMT can expose whether the intended causal logic is coherent; only appropriately designed prototypes, playtests, telemetry, comparable evidence, production work, and market tests can reduce the remaining uncertainty.
