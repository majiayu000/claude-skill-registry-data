---
name: prototype
description: Build a throwaway prototype to answer a design or behavior question. Use for state-model demonstrations, UI alternatives, or bounded API and timing probes.
---

# Prototype

A prototype is throwaway code that answers a question. The question determines the artifact and the evidence.

## Pick a branch

Select the branch from the requested question:

- A person needs to explore logic or state transitions: [LOGIC.md](LOGIC.md). Produce a shareable HTML demonstration.
- A visual design needs comparison: [UI.md](UI.md). Produce distinguishable variants with a visible selection control.
- An API, runtime behavior, or timing claim needs observation: [PROBE.md](PROBE.md). Produce a minimal representative probe.

Ask the user when an unresolved product preference changes the question.
Use available evidence directly when it already answers the question.

## Shared rules

1. Name the decision and completion condition before implementation. Limit work to evidence that can inform that decision.
2. Isolate the artifact from production behavior. Use a scratch location for probes or a clearly marked, non-production route for contextual UI variants.
3. Use memory or explicitly disposable local data by default. Obtain authorization before external effects or access to shared state.
4. Expose relevant state, inputs, and results. Provide a simple command or file that reproduces the observation.
5. Report the answer, tradeoffs, artifact location, and uncertainty. Preserve agreed artifacts and remove temporary instrumentation that no longer serves the task.

Use tests when they help answer the question.
Keep security and error behavior appropriate to the probe's actual access and side effects.

## Completion boundary

A prototype-only request ends with the decision and its evidence.
Continue into production implementation only when the user's task already authorizes it.
Assess prototype code against the production contract before reuse.
Create a commit, branch, issue comment, or pull request only when the user or repository workflow authorizes that action.
