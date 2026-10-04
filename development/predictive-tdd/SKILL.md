---
name: predictive-tdd
description: Run strict Predictive Test-Driven Development by stating falsifiable expectations before every deterministic check, comparing predictions with reality, and proceeding in one-test Red-Green-Refactor cycles. Use when the user explicitly requests Predictive TDD, prediction-driven TDD, or asks to continue an existing Predictive TDD cycle.
---

# Predictive Test-Driven Development

Use TDD as an empirical feedback loop: predict, check, compare, and let the evidence determine the next change.

## Core rules

The prediction requirement applies only within the TDD workflow. Routine repository, file, and administrative operations do not require predictions.

1. Work on exactly one observable behavior at a time.
2. Before every deterministic check, state a concrete, falsifiable prediction and run the check immediately.
3. Compare predicted and actual outcomes explicitly. Never rewrite an unexpected result as predicted.
4. A valid Red fails because the active behavior is missing, for the predicted reason.
5. Investigate prediction mismatches before changing production behavior.
6. Implement only enough to satisfy the active behavior and keep previous behavior green.
7. Refactor only while behavior tests are green.
8. Do not invent unspecified behavior; resolve ambiguous observable contracts by stating the reading you adopt.

## Preparation

Before the first cycle:

1. Read the complete specification and identify every rule, example, boundary, and ambiguity.
2. Create or review an ordered test list. Keep future tests inactive.
3. Determine the project's stack and commands. If `stacks/` contains a matching profile, read it before changing code.
4. Establish a baseline with the applicable behavior, compilation/type, lint, and smell checks. Predict each check before running it.

## One predictive cycle

### 1. Activate one behavior

State its given/input, operation, and exact expected outcome in domain language. Choose the smallest public observation that proves it, then activate or write exactly one test.

### 2. Reach behavioral Red

Open the phase with the `## Red` marker (see "Mandatory output markers" below), then inspect the current code and predict the narrowest test's load/compile/execution outcome, failure category, and relevant message or values. Run it and compare.

If loading or compilation prevents the assertion from running, add only enough scaffold to reach the behavioral failure. Predict and check again. Do not implement the behavior until Red fails for the intended reason.

If the new test already passes, confirm that prediction, record that no production change was needed, and do not manufacture a failure.

Close the phase with the `Red Phase Complete:` block and both prediction lines.

### 3. Reach Green minimally

Open the phase with the `## Green` marker. Make the smallest production change likely to pass the active test without anticipating inactive examples. Hardcoded values and narrow conditionals are valid intermediate steps.

Predict and run the focused test. Include expected pass/fail and todo counts when available. Compare the result; investigate any mismatch before continuing.

### 4. Inspect and refactor

While green, review the code against the Four Rules of Simple Design, in order:

1. Passes the tests
2. Reveals intention
3. Contains no duplication, including duplicated knowledge
4. Has the fewest elements

Use domain-appropriate names and do not leak temporary implementation details into them. Linters and smell detectors are evidence, not substitutes for this review.

Make at most one refactoring at a time. Predict and run the smallest relevant check after each. If no refactoring improves the Four Rules, leave the code unchanged.

**In this workflow the refactoring runs in this context.** Open the phase with
the `## Refactor` marker (see below) and emit it also when the review concludes
that no refactoring improves the code.

### 5. Close once

Predict and run the complete suite and all other applicable gates from the stack profile. Do not run the complete suite both before and during this closing step unless investigating a mismatch.

Close with a compact record of the behavior, Red evidence, minimal Green change or already-green result, refactoring decision, final gates, and next inactive behavior. Then start the next cycle immediately.

## Mandatory output markers

Predictions and phases are read mechanically from your output text. Emit these markers verbatim.

| Phase     | Marker                                            |
|-----------|---------------------------------------------------|
| Test List | `## Test List` + `Test List Created:`             |
| Red       | `## Red` heading                                  |
| Red       | `Red Phase Complete:` plus both prediction lines  |
| Green     | `## Green` heading                                |
| Refactor  | `## Refactor` heading                             |

Red phase output:

```
## Red -- Test N: <test description>

<prediction and failure verification steps>

Red Phase Complete:
**Compilation Prediction**: <what you expected> Correct
**Runtime Prediction**: <what you expected> Correct

<result summary>
```

Emit **both** prediction lines, verbatim, each ending in `Correct` or `Incorrect`. Do not abbreviate them, do not summarize them as "both correct", and do not collapse them into one line. This is the mechanical form of Core rule 3: an unexpected result is recorded as `Incorrect` and investigated, never rewritten as predicted.

When the activated test already passes, write:

```
## Red -- Test N: <test description>

Test already passes -- no new failure to fix. No production change needed.
```

Green phase output:

```
## Green -- <brief summary of what was added>
```

Refactor phase output:

```
## Refactor -- <brief summary of what was improved, or "no improvement possible">
```

This heading is the only signal that the Four Rules review happened. Emit it
every cycle, including the cycles where the review changes nothing.

## Prediction mismatch

When actual and predicted outcomes differ:

1. State that the prediction was incorrect and preserve both outcomes.
2. Stop feature implementation.
3. Use the smallest deterministic check to explain whether the cause is existing behavior, test setup, command/environment, load/compile failure, quality tooling, coupling, or regression.
4. Make a new evidence-based prediction and check it.
5. Resume only after the discrepancy is understood.

Never change production behavior merely to make an unexplained failure disappear.

## Completion

A feature is complete only when every specified example has an executable test, all behavior tests and applicable quality gates pass, mismatches are explained, the Four Rules review is complete, and no unagreed behavior was added.
