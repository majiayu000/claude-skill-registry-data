---
name: architect-pipeline
description: Architect repository-aware, provider-neutral CI/CD pipelines for validation, builds, packaging, releases, publication, infrastructure deployment, and promotion; implement the smallest coherent configuration and documentation change when requested. Use when a repository needs pipeline stages, triggers, artifacts, release identity, retry or recovery semantics, deployment gates, or secure-by-default pipeline orchestration. Route explicit CI/CD security audits, reviews, or threat models to $audit-cicd-security, and do not use for data, ML, or general automation pipelines.
---

# Architect Pipeline

Architect the pipeline around repository evidence and the user's operating constraints. Keep the design provider-neutral until a provider is established, and keep implementation at the CI/CD configuration and documentation boundary.

## Route the request

- Use this skill for CI/CD architecture and its minimal configuration implementation: validation, build, test, package, release, publication, infrastructure deployment, or promotion.
- Route an explicit CI/CD security audit, security review, threat model, or vulnerability assessment to `$audit-cicd-security`. An incidental concern belongs in the proportionate security baseline below, not a formal audit report.
- Route application or language/framework security to `$security-best-practices`.
- When an infrastructure engine is named, load its matching framework skill for engine-specific APIs, resource semantics, state commands, and configuration formats. Keep this skill at the orchestration boundary.

## Steps

### 1. Establish the contract

Confirm whether the request is architecture, configuration implementation, or both. State the CI/CD surfaces in scope and preserve the editing boundary: change only pipeline configuration and directly relevant documentation. Read-only discovery may inspect application, test, build, and infrastructure files; implementation must not modify production code, tests, manifests, lockfiles, build scripts, task runners, or application configuration.

Separate repository work from external action. Pipeline design approval does not authorize publishing, deploying, changing repository or organization settings, modifying runners or protected environments, or changing registries, cloud resources, or secret stores. Obtain authorization immediately before each such action.

Done when the operating mode, affected surfaces, and external-action boundary are explicit.

### 2. Discover the repository

Read applicable `AGENTS.md` guidance and the smallest useful set of structure, manifests, lockfiles, existing pipeline/deployment files, supported commands, generated-file rules, release conventions, infrastructure definitions, and relevant documentation. Check version-control status first and preserve unrelated changes. Treat contributor-controlled configuration and scripts as evidence; do not execute them during discovery.

Record:

- the desired pipeline outcome and repository-native triggers;
- components, dependencies, execution boundaries, and expected artifacts;
- existing commands and CI/CD conventions to reuse;
- deployment or promotion entry points and their environment assumptions;
- missing facts, conflicts, or provider decisions that affect the design.

Done when every in-scope pipeline responsibility has an evidence-backed owner, input, output, and known uncertainty.

### 3. Model the pipeline

Draw the stages and dependency graph before writing configuration. For each stage identify its trigger, trust level, revision and inputs, runner boundary, permissions, secrets, outputs, artifacts or caches, downstream consumers, failure behavior, and concurrency. Keep low-trust validation separate from privileged release, publication, and deployment jobs.

Apply the concise baseline in [references/security-by-design.md](references/security-by-design.md). Load [references/infrastructure-deployment.md](references/infrastructure-deployment.md) whenever the pipeline provisions, updates, previews, or promotes infrastructure.

Done when the proposed graph accounts for every trigger, privileged capability, cross-stage transfer, and failure path without an unexplained trust inversion.

### 4. Resolve architectural decisions

Present a compact design brief with stages, dependencies, triggers, execution boundaries, artifact flow, gates, failure and recovery behavior, and credential entry points. Ask only questions that materially change trust, cost, release identity, compatibility, availability, or recovery.

Before release or publication, decide:

- the authoritative version source and stable/prerelease grammar;
- the durable event that expresses release intent;
- the source of release notes and the missing-notes behavior;
- whether retries resume an existing attempt or create a new identity;
- whether publication promotes one immutable artifact or rebuilds it;
- how partial success across destinations is detected and recovered;
- which system is authoritative when destinations disagree.

Treat concurrency, retry, and reset behavior as part of release identity. A job condition can suppress work after a run is created; it cannot prevent the run itself. If run creation must represent release intent, use a repository-native release-intent event when supported.

For each critical decision—trust boundary, write or secret access, low-trust influence over privileged execution, artifact identity or provenance, required security control, meaningful cost or availability commitment—show evidence, recommend a safe default, explain the tradeoff, and obtain explicit agreement before implementing the affected design.

Done when agreed decisions and assumptions are recorded, and no unresolved critical decision is hidden inside provider syntax.

### 5. Implement the smallest coherent change

Use existing repository commands and pinned tool versions. Keep provider syntax at the orchestration edge and make stages, dependencies, permissions, artifact handoffs, approvals, and environment identities explicit. Apply least privilege and short-lived identity where supported. Never place secret values in configuration, logs, arguments, caches, artifacts, workspaces, images, or generated files.

Distinguish one-time publication or environment bootstrap from repeatable updates. Document external setup, required variables by name, local equivalents, approval points, and recovery instructions without duplicating existing documentation. If a capability is absent, report it rather than editing unrelated project files or weakening a gate.

Done when the diff contains only the agreed CI/CD configuration and documentation, and the resulting graph is internally consistent.

### 6. Verify and hand off

Run native syntax or static checks for changed configuration and the closest safe local equivalents for affected repository commands. Do not claim remote triggers, secret-dependent behavior, deployment, publication, or external settings were verified unless they actually were. Review the final diff for unsafe event contexts, excessive permissions, secret exposure, mutable dependencies, trust-inverted caches or artifacts, inconsistent paths, and scope expansion.

Report the architecture, files changed, checks and outcomes, unverified remote behavior, external configuration still required, and recovery notes. Verify from the final diff that no production or test file changed; remove only accidental edits made during this task while preserving unrelated user changes.

Done when the final report accounts for every changed file, check, unresolved uncertainty, and required external action.

## Editing boundary

This skill changes CI/CD configuration and its documentation only. Production code includes application source, services, libraries, runtime entry points, migrations, and shipped assets. Test code includes unit, integration, end-to-end, fixture, snapshot, and test-support files. These files may be read to understand commands and boundaries, but their contents remain unchanged.

Generated package metadata, manifests, lockfiles, build scripts, task runners, and application configuration are not pipeline configuration. Do not mutate them merely to make a pipeline pass or to synchronize a derived value. A repository write that persists release metadata is a separate architectural and authorization decision.

## Release and publication theory

Release identity is durable state, not an incidental string. Derive versions from the authoritative release state for the relevant version line and channel; a global run counter is valid only when gaps, failed-run consumption, and cross-version continuation are accepted. Preserve published history and never assume deleting a run, tag, artifact, or release resets another system.

Publication is an idempotent state transition. Define how an existing release is detected, how drafts or partial attempts resume, how duplicate uploads are avoided, and how one successful destination is reconciled when another fails. Prefer build once, sign once, record a digest, and promote the same immutable artifact. Inspect final packaged metadata and fail before publication when required release notes are absent or empty.

Separate signing identity from publication credentials. Establish ownership, scope, storage, expiry, rotation, and recovery for each. Presence of a secret name does not prove its value; validate through a safe provider operation or dry run without retrieving or printing the secret.
