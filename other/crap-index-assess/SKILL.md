---
name: crap-index-assess
description: Assess method-level change risk with the Change Risk Anti-Patterns (CRAP) index and recommend focused testing or complexity reduction. Use when the user asks what CRAP means or how to calculate, interpret, or reduce a CRAP score, or when the repository's configured CRAP check covers changed methods; not as a general quality verdict or merge gate.
---

# CRAP Index Assessment

Use the CRAP index as a method-level risk signal, not as a verdict on code quality or a target to game.

## Measure

1. Confirm the source revision and the methods in scope.
2. Read repository instructions, command entrypoints, scripts, manifests, analysis configuration, and CI needed to find an existing CRAP measurement and its documented prerequisites.
3. When the repository configures a CRAP command, run that command with its existing defaults and any documented project-native prerequisite that produces its coverage input. Preserve its complexity and coverage definitions, exclusions, precision, aggregation, and configured threshold. Do not replace it with an ad hoc command, install a tool, or change its configuration.
4. If the configured command fails, report the command and failure. Do not use partial or stale output. Use a manual fallback only when reliable method-level complexity and coverage from the same revision remain available, and label the result as a fallback rather than a successful tool run.
5. Use the manual calculation only when the repository has no configured CRAP measurement or the preceding fallback condition applies.

## Manual Calculation

1. Record how the available measurement defines cyclomatic complexity and coverage. Treat complexity as one plus the decisions in a method unless the measurement defines it differently. Prefer branch or basis-path coverage from automated, repeatable tests; when only another coverage type is available, name it and state the limit.
2. Validate cyclomatic complexity `c >= 1` and coverage percentage `0 <= cov <= 100`. Do not estimate missing values, mix incompatible reports, or substitute class averages for method data.
3. Calculate uncovered proportion `u = 1 - cov / 100`, then calculate:

   `CRAP(m) = c² × u³ + c`

4. Show the inputs and substituted calculation with enough precision to reproduce the result. At full coverage the score equals complexity; at zero coverage it equals `c² + c`.
5. Rank methods by score. State the chosen boundary: `> 30` is a common fallback, while some definitions and tools use `>= 30`. Do not hide the boundary choice. For a larger scope, report the count and percentage of methods beyond it as well as the highest-risk methods; an average alone can hide hotspots.

## Interpret

- Treat a high score as evidence that a method combines change paths with weak automated protection.
- Compare scores only when the complexity and coverage definitions are compatible.
- Treat 30 as a triage threshold, not a universal quality standard. Calibrate it against the codebase and the decision being made.
- Do not infer test quality from coverage. Covered assertions may still miss important behavior.
- Do not infer sound design from a low score. CRAP does not measure cohesion, coupling, naming, duplication, side effects, concurrency, or domain difficulty.
- Note that the source material expands CRAP as both “Change Risk Anti-Patterns” and the earlier “Change Risk Analysis and Prediction”; this naming difference does not change the formula.
- Treat CRAP load as a separate, experimental measure. Do not derive it without an explicit definition.

## Improve

Choose the smallest response that addresses the score's cause:

- For low or moderate complexity with weak coverage, add deterministic tests for observable behavior, boundaries, and meaningful failures.
- For high complexity with credible coverage, simplify the control flow or separate coherent policy. Preserve behavior and keep tests passing.
- For both high complexity and weak coverage, add characterization tests first, then refactor in small steps.
- When `c > 30`, coverage alone cannot bring the score to 30 or less. When the target is `< 30`, `c >= 30` requires complexity reduction.

Prefer guard clauses, simpler conditions, and separation of distinct decisions when they make the code clearer. Do not split methods, add shallow wrappers, weaken assertions, exclude code, or add tests with no useful checks merely to lower the number.

Rerun the same project command or manual measurement after each accepted change. Report the before-and-after complexity, coverage, score, behavior protected by tests, and remaining risk. Do not install a measurement tool, edit code, or change test policy unless the user has authorized that work.

Finish with the measurement source or command, scope and definitions, available method or aggregate results, the selected threshold, prioritized findings, focused improvement options, and explicit evidence limits. Report the assessment as inconclusive when neither configured output nor reliable method-level inputs are available.
