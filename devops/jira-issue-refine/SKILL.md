---
name: jira-issue-refine
description: Refine one draft or existing Jira issue into a clear, evidence-backed, bounded delivery contract without implementing it. Use when creating or revising an issue before engineering handoff, especially when behavior, repository ownership, acceptance evidence, dependencies, risk, environment needs, or scope remain unclear.
---

# Jira Issue Refinement

Turn one issue into a concise contract that an engineer or coding agent can implement and verify without guessing. Preserve confirmed intent, resolve discoverable facts, and expose decisions that still require a person.

## Establish the issue boundary

1. Read the complete draft or existing issue, including structured fields, comments, links, attachments, parent or child issues, and user-supplied context when available.
2. Identify the affected actor or system, current behavior, required outcome, business or operational reason, and requested issue type.
3. Separate confirmed requirements from observations, assumptions, implementation suggestions, and unrelated follow-up ideas. Do not silently promote an engineering suggestion into required behavior.
4. Preserve the author's confirmed intent and terminology. Change meaning only when evidence or an explicit user decision requires it.
5. Keep Jira access read-only unless the user explicitly authorizes creating or updating an issue. Do not implement the requested product or engineering change under this skill.

## Assess what the issue still needs

Check each concern only to the depth material to delivery:

- **Behavior:** State the observable result, inputs or preconditions, boundaries, failure behavior, and unchanged behavior. Do not reward detail that merely prescribes an implementation.
- **Evidence:** For a bug, capture observed and expected behavior, reproduction, environment, diagnostics, and regression evidence. For a feature, capture concrete scenarios and constraints. For infrastructure or data work, capture current and target state, ordering, idempotency, recovery, and rollback constraints.
- **Ownership:** Identify the owning repository and component from authoritative evidence. Record a multi-repository dependency explicitly; do not force uncertain ownership into one repository.
- **Verification:** Define deterministic evidence that will prove success and important failure or regression behavior. Prefer established repository tests, builds, static checks, and CI. Do not demand a new exact-value test for a simple declarative or version update when native checks already prove the contract.
- **Scope:** Keep one coherent outcome with a clear completion boundary. Separate an epic, open-ended investigation, rewrite, or independently deliverable changes into linked issues when they do not need one atomic delivery.
- **Independence:** Expose unresolved product decisions, unavailable inputs, other-team actions, external systems, sequencing, credentials, or access that can block delivery.
- **Safety:** State relevant trust boundaries, state changes, compatibility constraints, rollout, rollback, and recovery needs. Treat authentication, authorization, tenant isolation, billing, personal data, migrations, public contracts, infrastructure, secrets, and destructive actions conservatively.
- **Environment:** Confirm that a coding workflow can make the change and obtain credible verification locally or through established CI. Name essential runtimes, services, platforms, test data, or privileged capabilities only when they materially apply.
- **Effort:** Keep the issue small enough for one focused delivery. Split work whose exploration, implementation, or validation has independent completion boundaries.

Classify a material gap as a discoverable fact, a product or architecture decision, an external dependency, or a genuine unknown. Do not fill gaps with plausible prose.

## Resolve material gaps

1. Use `system-investigate` when repository tracing, bounded runtime evidence, linked system context, or current public technical research can resolve a material fact. Give it one explicit question and stopping condition. Keep private Jira and repository content out of public searches.
2. Incorporate only findings supported by observed evidence. Link repository files, issue references, commands, documentation, or public primary sources near the resulting claim.
3. Use existing product behavior and repository contracts to clarify mechanics, constraints, and vocabulary, but do not let current implementation override an explicit desired behavior.
4. Ask the user one focused question when an unresolved value or architecture decision changes required behavior or scope and cannot be discovered. Present concrete alternatives and consequences when useful.
5. Leave a dependency or unknown explicit when another team, unavailable system, missing authority, or conflicting source prevents resolution. Never disguise a blocker as an acceptance criterion.

## Rewrite the issue

Use only the sections that help the reader, but make the following information easy to find:

- A specific title that names the affected behavior and desired outcome.
- Context that states the current condition, affected actor or system, impact, and decisive evidence.
- Required behavior written as observable outcomes rather than a preferred code change.
- Acceptance criteria that each describe a condition or input, an action or event, and an observable result. Include boundary, failure, recovery, and regression behavior only where the change makes them material.
- Non-goals that prevent a likely scope misunderstanding; omit obvious or speculative exclusions.
- Engineering notes containing confirmed repository ownership, relevant current behavior, likely change surface, established verification paths, dependencies, compatibility constraints, and safety or rollout requirements. Keep uncertain implementation ideas labelled as options.

Keep criteria direct and independently checkable. Avoid vague verbs such as “improve,” “support,” “handle,” or “work correctly” unless the issue defines the observable result. Remove repeated context, stale discussion, and instructions that constrain implementation without protecting a contract or risk.

When the issue will be created with `jira-issue-create`, fit the content into its three sections: put required behavior in Context or Acceptance criteria, and non-goals in Engineering notes.

## Report the result

Return the Jira-ready issue text first. Then list the decisive evidence, the unresolved decisions or blockers, and any suggested issue splits. If the user authorized a Jira write, show the final text before writing unless the user explicitly requested autonomous creation or update.

Finish when every required behavior has observable acceptance evidence; no requirements contradict each other; ownership is supported, explicitly uncertain, or multi-repository; the implementation and verification path needs no unstated capability; material dependencies, safety, compatibility, rollback, and recovery are stated; and facts, assumptions, options, and blockers stay distinguishable. Never claim that the issue is ready while a material behavior decision or delivery blocker remains hidden.
