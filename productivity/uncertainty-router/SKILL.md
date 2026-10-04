---
name: uncertainty-router
description: Use when Codex faces meaningful uncertainty and must decide whether to inspect local files, search official or live sources, run commands or experiments, ask the user, assume a safe default, use memory, or defer. Use for "how should we verify this?", "should we search or inspect?", "what is the cheapest next check?", stale/current fact decisions, ambiguous tool-choice decisions, and pre-work uncertainty triage.
---

# Uncertainty Router

Choose the cheapest honest way to reduce uncertainty. This skill is for routing unknowns to verification actions, not for performing a full research task or requirements interview.

## Workflow

1. Inventory the uncertainties.
   - Extract only unknowns that could affect correctness, scope, cost, safety, or user satisfaction.
   - Ignore trivia that does not change the next action.

2. Classify each unknown.
   - Local fact: repo files, configs, logs, tests, installed tools, current worktree.
   - Live fact: current docs, laws, prices, schedules, APIs, model names, product behavior, people/organization status.
   - User preference: taste, priority, acceptable tradeoff, private intent, desired scope.
   - Empirical behavior: can be tested by running code, rendering, screenshotting, benchmarking, or reproducing.
   - Inference: can be reasoned from available evidence but should be labeled.

3. Pick the route.
   - Inspect local files first for local facts.
   - Browse official or primary sources for live or version-sensitive facts.
   - Run the smallest command or experiment for empirical behavior.
   - Ask one concise question for preferences that materially change scope or risk.
   - Use a safe default when reversible and consistent with repo/user conventions.
   - Defer or mark as unresolved when verification is expensive and not needed for the current step.

4. Order by value.
   - Do cheap/high-impact checks before expensive/low-impact checks.
   - Prefer evidence that directly changes the decision.
   - Avoid broad searches when a local file, official doc, or targeted command can answer the question.

5. Execute or hand off.
   - If the broader task requires action and the route is obvious, perform the check instead of only listing it.
   - If operating in planning mode or the user asked only for routing, output the route map.
   - Route to `$codex-deep-interview` when the unknown is mainly requirements discovery.
   - Route to `$assumption-auditor` when the main need is exposing premises rather than choosing verification actions.

## Output Shape

Use a compact map:

`Unknown | Why it matters | Best route | Cost | Do now? | Evidence/Result`

Then include:

- First check to run
- Safe assumptions, if any
- Question to user, only if required
- Stop condition

## Routing Heuristics

- If the fact is likely to have changed and matters, verify live.
- If the fact is in the workspace and cheap to inspect, read it.
- If the behavior can be tested in under a few minutes, test it.
- If the answer depends on the user's private preference, ask.
- If the assumption is low-risk, reversible, and matches established context, proceed and record it.

## Stop Conditions

- Stop routing once the next verification action is obvious.
- Do not keep searching after a primary source or direct test has answered the operational question.
- Do not ask the user for facts that can be discovered safely from local context.
