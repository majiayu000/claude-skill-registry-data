---
name: capability-harness
description: Apply a decision-first capability-harness pass to substantive work when a model may miss context, evidence, an observable check, or a materially different alternative. When the prompt hook selects a pre-action route, execute exactly that one route before material work and integrate its bounded result. Do not use for routine direct work, fixed pipelines, cosmetic variants, or work already owned by another controller.
---

# Capability Harness

The project-scoped prompt hook selects one strong pre-action route when the prompt makes the next source of task context clear. It never launches workers, records hidden reasoning, or blocks completion. The selected route is a binding handoff for this turn: this Skill or the active controller executes it exactly once before material work, then integrates the bounded result or explicit skip. It does not replace the active domain method or make every task a multi-step workflow.

## Capability Decision

Before materially generating, modifying, or recommending, identify:

- the requested outcome and hard constraints;
- the single highest-impact unknown, quality risk, or unsupported assumption;
- the external signal, observation, or alternative that could inform or improve the approach or result;
- the smallest action that can obtain that signal, or the reason to proceed directly;
- the permission, data, side-effect, and stop boundary.

Make this decision before implementation. A candidate signal that the hook has not named as a selected route is not a requirement. Do not search, delegate, or review merely because a tool or worker exists, but do allow bounded search when a plausible unfamiliar-domain gap could materially improve the task. Search does not need advance proof of success; its findings must simply be bounded, relevant, and integrated into the next plan. If no available action can supply useful context, use the direct path and state the intrinsic limitation or remaining uncertainty when material.

## Acceptance Seed

Before material work, establish the lightest applicable acceptance seed:

- **Outcome and target/scope** — what must be true and where it must be true;
- **Minimum observable signal** — the smallest fact that would show the requested outcome is at least met;
- **Evidence path** — how that signal can be observed, such as a focused test, build, render, runtime check, comparison, or source check;
- **Unresolved preference or risk** — a user-owned choice, subjective criterion, or material uncertainty that remains, or `none`.

Reuse the requested outcome and hard constraints from the Capability Decision; do not create a second task specification. A fixed, low-risk, direct task may keep this seed implicit and must not receive extra hook context, search, delegation, or verification merely to fill the fields. For substantive implementation, modification, external delivery, or a claim that needs observation, make at least the outcome and minimum signal explicit before acting when they are not already clear. Infer obvious, low-risk criteria rather than blocking for formatting or non-material preference details.

Block or ask only when a missing user-owned choice, target boundary, evidence path, or side-effect authorization would change the direction or invalidate the result. The seed is provisional controller data, not a new route, worker, persisted state, or completion gate. Keep `defined`, `verified`, `evaluated`, and `complete` distinct: an observed signal supports its claim, but does not by itself establish overall task completion.

Carry the applicable seed into any selected pre-action route and into a verifier brief. The active controller and domain Skill remain responsible for interpreting it, choosing the exact check, integrating evidence, and making the final acceptance decision.

When the prompt hook names `project inspection`, `focused evidence research`, or `bounded context discovery` as the selected route, perform that one route before material work. Do not silently replace it with a direct response because it is faster. Direct and explicitly controller-owned workflow prompts receive no additional hook context. A selected `context-scout` may return its bounded direct-route skip, and unavailable or unsafe evidence may be reported as such; those are the valid reasons to continue without discovery. A leading slash alone is not a controller boundary.

## Context Discovery

For an open-ended or unfamiliar task, consider `capability-harness:context-scout` when omitted domain, structural,
compositional, interaction, or medium-specific information could materially improve a named decision. Give it the original
outcome and constraints; do not make the user write the missing checklist into the prompt.

The scout first states the decision and missing context. It may return a direct-route skip when no bounded source can supply
useful task context. When it does research, it returns a Pre-action Decision Brief with evidence and explicit plan
implications. The active controller must consume that Brief before material generation or implementation. Do not paste raw
search results into the task, copy an existing artifact, or treat the scout as the final evaluator. Verification and
evaluation remain optional downstream capabilities.

For a bounded public-discovery assignment, including a hook-selected route, public and non-sensitive search is authorized by this project capability. Search queries must not include private prompt content, repository source, identifiers, credentials, or other protected data. Ask for direction when resolving the uncertainty would require crossing that boundary.

An explicit source or network constraint in the current user request overrides this generic route authorization. Do not invoke external discovery under that constraint; use only explicitly permitted local evidence or take the direct path. This is a per-request boundary, not a default project policy.

## Reference Policy

Read only the references that bear on the current decision:

- [routing policy](../../references/routing-policy.md) before selecting a module;
- [capability contracts](../../references/capability-contracts.md) before writing a leaf-agent brief or interpreting its result;
- [evidence policy](../../references/evidence-policy.md) for WebSearch/WebFetch or repository evidence;
- [evaluation policy](../../references/evaluation-policy.md) when comparing capability choices, candidates, or revisions;
- [failure recovery](../../references/failure-recovery.md) when a tool, agent, source, or decision route fails;
- [architecture](../../references/architecture.md), [design intent](../../references/design-intent.md), and [installation](../../references/installation.md) for plugin boundaries and maintenance.

These references describe the current project plugin. The current agent files and `SubagentStop` minimum headings take precedence over older or external harness examples.

## Module Selection

Use only the module that can change the selected decision:

- `capability-harness:context-scout` for one bounded missing-context question before generation or recommendation;
- `capability-harness:evidence-researcher` for one bounded repository or current public-source question;
- `capability-harness:independent-brancher` for one materially different candidate when anchoring or a real trade-off remains;
- `capability-harness:execution-verifier` for one exact claim with an identified target, permitted effects, and observable acceptance signal;
- `capability-harness:skeptical-evaluator` for actual candidate artifacts or results whose material quality is not settled by deterministic checks.

Each worker is a leaf. Give it one bounded brief, the decision it is meant to inform, actual evidence or artifact scope, constraints, permissions, return contract, and stop condition. Do not launch all workers by default. If another workflow already owns coordination, route any needed module through that controller instead of creating a second orchestration layer.

## Integration

Prefer current repository evidence for repository behavior and official or primary current sources for external claims. Match verification to the requested outcome: source syntax alone does not establish rendered, runtime, interactive, calculated, or user-visible quality. Preserve blocked, failed, stale, and unverified evidence states instead of collapsing them into success.

The active controller and domain Skill own implementation, repair count, acceptance, and final integration. Harness workers
return bounded context, evidence, candidates, verification, or evaluation; they do not limit or replace domain-workflow
repairs. Preserve the strongest result seen so far. Report a selected route and the resulting plan implication when it makes
a material decision observable; do not claim global optimality or overall task completion.
