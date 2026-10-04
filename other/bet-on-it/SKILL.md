---
name: bet-on-it
description: Use when debugging or changing behavior based on an uncertain causal hypothesis that the next action can test.
---

# Bet On It

Make each action earn or lose confidence. Never rewrite a prediction after its result.

## Record the bet

When an action depends on an uncertain causal explanation, record this in working notes or commentary—not a repository file:

```text
Hypothesis: <current causal explanation>
Expected observation: <specific result expected from the next action>
Expected change: <files, state, metric, or behavior; none for observation-only steps>
Disproof: <result that would make this hypothesis untenable>
```

Use observable signals. One bet may cover coupled steps. Skip bets for mechanical work or settled requirements.

## Run the smallest discriminating step

Choose the cheapest safe step that separates plausible alternatives. Prefer read-only observation or temporary instrumentation before a persistent edit. Preserve baselines; separate unrelated changes.

## Settle the bet

After the action, preserve the original prediction and append:

```text
Observed: <actual result, including unexpected changes>
Verdict: matched | partially matched | failed | inconclusive
Next action: <continue, refine, abandon, revert, or gather a better signal>
```

Apply the verdicts consistently:

- **Matched**: Expected results occurred and disproof did not. This raises confidence but does not prove causality when rivals predict the same result.
- **Partially matched**: Some predictions held; narrow or revise the hypothesis.
- **Failed**: A valid discriminator produced disproof or failed a required prediction. Abandon or revise.
- **Inconclusive**: The step or measurement could not distinguish alternatives. Do not count it as support.

Revert speculative changes after a failed hypothesis when they lack independent justification. To keep one, state the new reason and test it under a new prediction.

## Example

For a duplicate checkout request, Bet 1 predicts that instrumentation will show two client handler invocations; one invocation with two requests disproves it. Make no behavior change.

Only if Bet 1 matches, Bet 2 predicts that removing the duplicate binding in `Checkout.tsx` will reduce invocations and requests from two to one; two requests after one invocation disproves it.

If Bet 1 fails, do not make or retain the client fix. Form a retry or idempotency hypothesis.
