---
name: code-intelligence-contract
description: Use when dependency, call-chain, blast-radius, architecture, domain-flow, or unfamiliar-codebase analysis needs an optional vendor-neutral code-intelligence provider.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: gate
    lifecycle_stage: discover
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: code-intelligence-evidence.json
    required_evidence: [provider, provider-version, repository-revision, index-state, query-result, limitations]
    owner: HoaTV Studio
    reviewer: QA Lead
    maturity: experimental
    last_reviewed: 2026-08-26
    provenance:
      derived_from: none
      patterns_from: [Graphify edge provenance, GitNexus impact workflows, Understand Anything onboarding graph]
      copied_text: none
---
# Code Intelligence Contract

## Overview
Use one provider-neutral capability contract for optional code intelligence. Graph output can guide source inspection, but it never replaces source ownership, tests, runtime evidence, mutation approval, or reviewer judgment.

## When to use
Use for pre-change impact analysis, independent post-change comparison, cross-subsystem debugging, changed-symbol review, unfamiliar-project onboarding, architecture or domain-flow discovery, and cross-repository contract analysis when a provider is available.

## When NOT to use
Do not use this skill for pure project intake, pure debugging, or pure mutation work that does not need graph context. Do not use graph output as runtime proof, source authority, generated-file authority, or permission to install, index, clean, hook, or expand write scope.

## Required inputs and context discovery
Collect a stable query ID; provider and resolved version; repository, revision, worktree identity, capability, required languages, and artifacts; an explicit privacy-safe untracked content identity when untracked files are present; index identity and state; query subject; edge provenance; affected paths; generated authorities; side-effect observations; reviewer; and the owning workflow's source/test fallback.

## Safety and risk level
The graph lane is read-only. Provider installation, index creation or refresh, hooks, generated project-local skills, and cleanup are mutations outside this contract. Any observed provider write is `SIDE_EFFECT_VIOLATION`, blocks the graph lane, and requires separate report-only planning and approval.

## Workflow
1. For each recorded preference/opt-in candidate, probe installed provider version and index status without mutation.
   Completion criterion: discovered version and index facts are recorded without install, refresh, hooks, cleanup, or writes.
2. Before selection, require repository scope plus repository/HEAD/worktree/language/side-effect binding. Do not read untracked file contents; when untracked files are present, require the provider wrapper to supply a privacy-safe content identity or keep repository identity incomplete and the graph lane BLOCKED. Treat `USER_DISABLED` as ineligible, filter for the exact required capability and language, then select the highest-priority `FRESH` eligible provider. If no exact match exists, selection remains BLOCKED; never silently substitute a weaker capability.
   Completion criterion: query ID, binding, eligibility filters, priority, and selection blocker are recorded.
3. Classify index state before using output. Use `STALE_HEAD` when indexed revision differs, `STALE_WORKTREE` when worktree identity differs, `PARTIAL_LANGUAGE` when any required language is unsupported, `SIDE_EFFECT_VIOLATION` when the read-only boundary is broken, and `EMPTY_UNCERTAIN` when the provider returns no result. Broken, unavailable, disabled, and unsupported providers are also BLOCKED.
   Completion criterion: only a fresh, read-only, language-complete result proceeds; every other state records a source/test fallback.
4. Run the smallest provider-neutral capability query: context, dependency path, impact, cross-repository contract, architecture, onboarding, or domain flow.
   Completion criterion: query ID, subject, affected paths, artifacts, limitations, and exact provider output are recorded without widening write ownership.
5. Resolve exactly one query subject before classifying edges. Only source-derived `EXTRACTED` edges may be `Verified`, and only for extraction at the bound snapshot. `confidence=INFERRED` and semantic/LLM evidence stay `Snapshot` or `Unverified`; zero or multiple resolved subjects and other unresolved ambiguity are `BLOCKED`.
   Completion criterion: extraction, inference, semantic interpretation, and runtime behavior have separate labels.
6. Confirm material paths against source owners, generated authorities, tests, logs, or runtime evidence. The implementer runs pre-change impact before editing. The verifier independently runs a fresh post-change query with the same query ID and compares pre/post affected paths.
   Completion criterion: source disagreements, dynamic dispatch, reflection, generated paths, and post-change freshness limits are explicit.
7. For mutation without usable graph evidence, record Decision: `REVIEWER_ACKNOWLEDGED_FALLBACK`; explicit missing graph coverage/blocker; authoritative source owners; known callers/consumers; generated authorities or exact `NOT_APPLICABLE`; focused test commands; named reviewer; and residual risk. Preserve existing risk, approval, backup, and restore gates. Any unresolved generated, cross-repository, or dynamic boundary remains BLOCKED, and graph verdict stays BLOCKED. Inspect every generated-source, dynamic-dispatch, language, repository, security, database, service, or release boundary; if source/tests cannot cover any unresolved boundary, the owning workflow remains BLOCKED.
   Completion criterion: the full fallback record exists, approved write scope stays bounded, and Graph verdict remains BLOCKED.

## Provider roles

| Provider | Role | Appropriate use |
|---|---|---|
| Graphify | experimental opt-in default candidate | Local deterministic context, dependency, and impact artifacts; never an automatic dependency or mutation gate. |
| GitNexus | advanced optional | cross-repository impact, PDG, taint, and API/tool maps after license and terms review. |
| Understand Anything | onboarding optional | onboarding, architecture, and domain-flow context with semantic/LLM evidence kept separate from extracted source evidence. |
| CodeGraph | legacy-compatible | preserve the callable bridge while migrating providers; legacy caller-declared `FRESH`/`EXTRACTED` evidence without complete canonical identity remains BLOCKED |

## Evidence and output contract
Produce `code-intelligence-evidence.json` or embed the normalized object in the owning workflow artifact. Include query ID; provider/version/index identity; repository/revision/worktree binding; capability; required and supported languages; artifacts; affected paths; per-edge provenance, confidence, and evidence label; side effects; limitations; source/test fallback; reviewer; residual risk; and next action.

No graph result is not proof that no dependency exists. `EMPTY_UNCERTAIN` preserves that exact warning. Graph `BLOCKED` is never a workflow or runtime PASS. A caller workflow may independently PASS only from its own source, test, log, or runtime evidence while the graph verdict remains `BLOCKED`.

## Handoff contract
Record query ID, repository/path, revision and worktree identity, provider/version/index identity, capability, required languages, artifacts, state, affected paths, ambiguity, limitations, side effects, commands and exit codes, graph/source disagreements, reviewer fallback when used, residual risk, and the next bounded action.

## Pitfalls and anti-rationalization
- Do not confuse a graph community with an authoritative subsystem owner.
- Do not treat `STALE_HEAD`, `STALE_WORKTREE`, `PARTIAL_LANGUAGE`, `SIDE_EFFECT_VIOLATION`, or `EMPTY_UNCERTAIN` as a small blast radius.
- Do not promote `confidence=INFERRED` or semantic/LLM evidence because it agrees with expectations.
- Do not expose absolute private paths or secrets in exported graph artifacts.
- Do not let a graph provider silently widen the approved write scope.
- Do not use `REVIEWER_ACKNOWLEDGED_FALLBACK` without all required source owners, known callers, known consumers, generated authorities, focused tests, reviewer acknowledgment, and residual risk fields.

## Verification checklist
- [ ] Query ID and provider/version/index identity are recorded.
- [ ] Every complete verified graph PASS has exactly one resolved subject.
- [ ] Repository, revision, worktree identity, capability, required languages, and artifacts match.
- [ ] Graph access produced no side effects.
- [ ] `EXTRACTED`, `confidence=INFERRED`, semantic/LLM, ambiguity, and runtime evidence are separated.
- [ ] Empty results use `EMPTY_UNCERTAIN` and the exact no-proof warning.
- [ ] Source owners, known callers, known consumers, generated authorities, tests, reviewer fallback, and residual risk are recorded when applicable.
- [ ] Verifier used fresh post-change identity, the same query ID, and a deterministic pre/post comparison.
- [ ] Every stale, broken, partial, unavailable, disabled, unsupported, ambiguous, or side-effect state remains BLOCKED.

## References and scripts
Use the canonical `scripts/code_intelligence.py` normalization helper in a full kit clone or its bundled `studio-project-scaffold` copy. `scripts/codegraph_adapter.py` remains the legacy-compatible adapter. Provider-specific commands are optional, non-authoritative, and must be verified in the target project before use. Full-clone maintainers may inspect `docs/case-studies/graphify-code-intelligence-dogfood.md` when present; standalone skill installs do not require that repository-only case study. Raw evidence remains under ignored `evidence/local/`.

## Negative scope
This skill does not implement code changes, authorize mutation, install or refresh providers, create hooks, clean indexes, widen ownership, claim runtime correctness, replace project intake, or replace build, test, security, database, service, and release gates.
