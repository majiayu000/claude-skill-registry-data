---
name: continuous-learning-v2
description: Review repeated user corrections and successful workflows, then propose small evidence-backed reusable instincts. Use only when the user explicitly asks to.
---

# Conservative Continuous Learning

Convert repeated, verified patterns into reviewable proposals without silently changing the assistant's behavior.

## Non-negotiable boundaries

- Advisory by default. Do not start background observation, install hooks, read unrelated conversations, or scan email/calendar/chat history.
- Do not create or update skills, agents, commands, plugins, hooks, memory stores, or configuration without a separate explicit approval for the exact diff and path.
- Do not select or switch models/providers. If an optional reviewer is available, use the active host's current capabilities; independence matters more than a model name.
- Store no secrets, raw private conversations, credentials, or sensitive code in learned artifacts.
- A confidence score ranks evidence; it never grants write permission.

## Evidence threshold

Propose an instinct only when either:

1. the same pattern appears in at least five distinct observations and no recent correction contradicts it; or
2. one deterministic failure and its verified fix establish a narrow technical invariant.

Every proposal records the trigger, action, scope, evidence summaries, counter-evidence, confidence, expiry/review date, and a way to test or revoke it.

```yaml
id: prefer-existing-project-pattern
trigger: when adding a new module to this repository
action: follow the nearest existing module structure before introducing a new abstraction
scope: project
confidence: 0.7
evidence:
  - five reviewed changes followed the same structure
counter_evidence: []
review_after: 2026-10-01
status: proposed
```

## Workflow

1. Confirm the user requested learning or pattern review.
2. Define the observation scope and exclude sensitive sources.
3. Normalize observations into short claims; keep pointers to local evidence rather than copying raw content.
4. Cluster only semantically equivalent claims. Keep exceptions and contradictions visible.
5. Apply the evidence threshold and produce proposals, not writes.
6. Show the exact proposed artifact/diff, target path, benefit, regression risk, validation, and rollback.
7. Write only after approval. Re-read the destination immediately before editing and preserve unrelated changes.
8. Validate the learned behavior against positive, negative, and boundary examples. Roll back if it broadens beyond its evidence.

## Evolution into a skill

Evolve an instinct only when a repeatable workflow needs multiple steps, references, or tooling. Before replacing an existing skill, compare behavior and trigger coverage, run preservation tests, and keep a timestamped backup. If the proposal is not measurably better, leave the existing skill unchanged.

## Output

Report observations reviewed, proposals accepted/rejected, contradictions, files changed, validation results, and rollback location. If no pattern meets the threshold, say so and make no change.
