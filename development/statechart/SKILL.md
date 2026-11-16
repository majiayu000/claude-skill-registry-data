---
name: statechart
description: "Model a stateful flow, check its invariants within stated bounds, and explain counterexample paths."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-11-01"
  sources: "cursor/plugins 4dd1d05818d19792e7cd6e818f1667f95f7e1dbe pstack/skills/statechart/SKILL.md and pstack/skills/create-formal-verification-skill/SKILL.md (ideas distilled)"
---

# Statechart

Use for queues, retries, workflows, protocols and concurrency where ordering can break an invariant. This is optional, not a gate for routine edits. A statechart illustrates a model; passing a model checker does not prove the production implementation.

## 1. State the property

Read the actual transition handlers, persistence and existing tests. List the states, actions, actors and failures in user/domain terms. State the invariant before modeling it: for example, a failed evaluation cannot reach release, or a retry cannot charge twice. Map each action to its source location and name abstractions such as omitted timing, bounded workers or an assumed atomic write.

Work in a scratch directory outside the repo unless the user wants a maintained model. Use `domain` for disputed terms and `debug` if a concrete incident still needs diagnosis.

Done when: the property, code mapping, assumptions and finite bounds are written down.

## 2. Build and check

For event ordering, model with TLA+ and check with TLC. Read [the model-checking recipe](references/model-checking.md). If the question is better answered by an existing language-specific verifier or property-test harness, use it and state its bounds instead.

Represent retries, failures and competing actors, not only the successful path. Encode safety as invariants; check liveness only with explicit fairness assumptions. A legitimate terminal state gets a stuttering action, rather than disabling deadlock checking globally. Do not weaken the property to make the check pass.

If no checker is available, report **model drafted, unverified** with the missing prerequisite. A hand-drawn diagram or source inspection is not a completed check.

Done when: the checker terminates with its command, version, exit result, coverage and log saved, or the unavailable prerequisite is explicit.

## 3. Explain the result

Produce a Mermaid statechart with domain labels. Label it **model**, and distinguish modeled transitions from observed production behavior. For a violation, show the shortest counterexample returned by the checker; if the checker did not minimize it, call it a counterexample, not the shortest one. Include the invariant violated and the input/action sequence needed to reproduce it.

Turn a useful counterexample into a real implementation regression test via `tdd`. A model fix and a code fix need separate verification. For a reusable project verification entry point, offer the explicit `project-verify` command.

Done when: the report states what was checked, what was excluded, and whether the counterexample reproduces in real code.
