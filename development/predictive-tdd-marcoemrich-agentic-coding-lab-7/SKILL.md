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

Inspect the current code and predict the narrowest test's load/compile/execution outcome, failure category, and relevant message or values. Run it and compare.

If loading or compilation prevents the assertion from running, add only enough scaffold to reach the behavioral failure. Predict and check again. Do not implement the behavior until Red fails for the intended reason.

If the new test already passes, confirm that prediction, record that no production change was needed, and do not manufacture a failure.

After comparing the prediction with reality, consult `.claude/skills/exact-coding-shared/human-in-the-loop.md` and apply the Red checkpoint for the active Autonomy Level.

### 3. Reach Green minimally

Make the smallest production change likely to pass the active test without anticipating inactive examples. Hardcoded values and narrow conditionals are valid intermediate steps.

Predict and run the focused test. Include expected pass/fail and todo counts when available. Compare the result; investigate any mismatch before continuing.

### 4. Inspect and refactor

While green, review the code against the Four Rules of Simple Design, in order:

1. Passes the tests
2. Reveals intention
3. Contains no duplication, including duplicated knowledge
4. Has the fewest elements

Use domain-appropriate names and do not leak temporary implementation details into them. Linters and smell detectors are evidence, not substitutes for this review.

#### Domain responsibility review

Apply the Single Responsibility Principle as part of Rule 2, using Domain-Driven Design's ubiquitous-language idea as the semantic anchor. This is a domain-language review, not a request to introduce DDD patterns or architecture layers.

For each production unit under review:

- State its responsibility as a short domain sentence using terms from the specification. A mechanical description such as "process data", "calculate result", or "handle scenario" is too broad to establish cohesion.
- Name the policy decisions and domain knowledge the unit owns. Ask which rules could change independently because the business meaning, policy, or actor differs—not merely which lines could be extracted.
- Challenge broad responsibility names with a change counterfactual: if one named policy changed while another stayed fixed, would this unit change for both reasons? If so, treat that as a candidate domain seam rather than hiding both beneath an umbrella such as "calculate quote".
- Separate independently changing domain decisions behind names that explain their policy. Also separate domain decisions from application orchestration and adapters such as transport, persistence, parsing, or presentation.
- Keep cohesive knowledge together. Do not split code merely to shorten a function, satisfy a metric, or imitate a design pattern.

**Priority over Rule 4:** A well-named element that isolates independently changing domain knowledge is necessary because it reveals intent. It is not an "extra element" for Rule 4 to remove. Apply "fewest elements" only after the domain responsibilities and their boundaries are explicit; never inline or reject a domain boundary solely because fewer functions, classes, or modules would result.

#### Mandatory domain-boundary trial

Analysis alone is not the refactoring attempt. When the review finds a credible domain seam, select the strongest candidate and try the structural change using the predictive check-and-undo process below. Do not dismiss the candidate merely because extraction adds a function, class, module, parameter, or invocation.

Use the smallest move that makes the policy boundary visible, such as:

- extract a policy calculation under a name from the specification
- extract a domain predicate that states when a rule applies
- separate application orchestration from a domain decision
- separate adapter translation from domain behavior
- consolidate duplicated domain knowledge behind its owning concept

Submit the trial to the predictive REFACTOR process below. Keep it only when the resulting names and dependencies make the independent policy easier to locate and change without altering behavior. Otherwise undo the entire trial before continuing. An undone trial still satisfies the attempt; explain why the proposed boundary did not reveal intent.

Before the trial, record:

```text
Domain responsibility: <the unit's responsibility in specification language>
Independent change axes: <the policy decisions that can change independently>
Boundary candidate: <the strongest semantic seam and the concrete move to try>
```

After verification, record:

```text
Boundary outcome: <retained or undone>
Semantic change: <how the resulting boundary improves domain ownership, or why the trial did not>
Fewest Elements check: <why every retained element is necessary after intent is explicit>
```

When no credible domain seam exists, record the same before/after form with `Boundary candidate: none` and identify the domain evidence that makes the unit one cohesive decision. A generic claim that the code is small, simple, or already cohesive is not sufficient. The decision must refer to the actual domain rules in the current unit.

Use the active stack profile only for language- and framework-specific application guidance.

Make at most one refactoring at a time. Predict and run the smallest relevant check after each. If no refactoring improves the Four Rules, leave the code unchanged.

**The invoking EXACT Coding profile selects the Refactor execution context.** Apply the Four Rules and domain-boundary contract through that profile's inline or isolated mechanism. After the review, consult `.claude/skills/exact-coding-shared/human-in-the-loop.md` and apply the Refactor checkpoint for the active Autonomy Level, including when no change improves the code.

### 5. Close once

Predict and run the complete suite and all other applicable gates from the stack profile. Do not run the complete suite both before and during this closing step unless investigating a mismatch.

Close with a compact record of the behavior, Red evidence, minimal Green change or already-green result, refactoring decision, final gates, and next inactive behavior. Then start the next cycle immediately.

## Prediction mismatch

When actual and predicted outcomes differ:

1. State that the prediction was incorrect and preserve both outcomes.
2. Stop feature implementation and consult `.claude/skills/exact-coding-shared/human-in-the-loop.md`. Unless the Autonomy Level is `autonomous`, report the discrepancy and wait for the human's decision.
3. Use the smallest deterministic check to explain whether the cause is existing behavior, test setup, command/environment, load/compile failure, quality tooling, coupling, or regression.
4. Make a new evidence-based prediction and check it.
5. Resume only after the discrepancy is understood.

Never change production behavior merely to make an unexplained failure disappear.

## Completion

A feature is complete only when every specified example has an executable test, all behavior tests and applicable quality gates pass, mismatches are explained, the Four Rules review is complete, and no unagreed behavior was added.
