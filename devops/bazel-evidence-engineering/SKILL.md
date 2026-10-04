---
name: bazel-evidence-engineering
description: Use when Bazel controls—or is being evaluated for—the relevant build, test, architecture, CI, artifact, or release surface. Choose the smallest sufficient Bazel evidence across graph, configuration, actions, execution, performance, and provenance. Skip non-Bazel build systems, runtime-only incidents, and prose tasks without a formal Bazel question.
license: MIT
metadata:
  author: kingda8
  version: "0.1.0"
---

# Bazel Evidence Engineering

Use Bazel to answer the engineering question with the smallest sufficient evidence, then widen only when dependency impact, risk, or a named acceptance gate justifies it.

This skill guides decisions. It does not expand authorization, convert inspection into mutation, or make publication, deployment, signing, remote upload, or another external effect implicit. Preserve unrelated work and distinguish moving snapshots from frozen conclusions.

Current compatibility guidance was reviewed against Bazel 9.2.0. Repository pins remain authoritative for version-sensitive work.

## Confirm that Bazel owns the question

Use this skill when Bazel controls the relevant surface or when the task explicitly evaluates adopting Bazel for it. A repository may use Bazel for only part of its build, test, package, or release flow; identify the real authority before treating Bazel as formal acceptance.

Stay out of unrelated build systems, prose-only work, and runtime-only incidents. Bring Bazel back only for an owning target, a build/configuration hypothesis, or formal regression evidence.

## Start with repository truth when it matters

Before repository-specific analysis or execution, inspect the checked-in Bazel and ruleset pins, governing instructions, effective rc/wrapper configuration, relevant targets, and authorization identity. Repository facts outrank examples in this skill.

Read [repository-first-inspection.md](references/repository-first-inspection.md) whenever revision, workspace, configuration, toolchain, platform, wrapper, remote services, or side effects can affect the conclusion. Skip it for generic conceptual guidance.

## Route to the relevant decision layer

Load only the references useful to the task.

| Mode | Typical questions | Reference |
|---|---|---|
| Repository and invocation identity | provenance, effective rc, wrappers, side effects, shared servers and worktrees | [repository-first-inspection.md](references/repository-first-inspection.md) |
| External dependencies and upgrades | Bzlmod, locks, extensions, repository rules, repo mapping, vendor/offline, upgrade ladders | [external-dependencies-and-upgrades.md](references/external-dependencies-and-upgrades.md) |
| Graph and architecture | ownership, deps/rdeps, visibility, boundaries, suites, orphans, configured universes | [graph-and-architecture.md](references/graph-and-architecture.md) |
| Starlark rule engineering | macro versus rule/aspect, providers, depsets, actions, transitions, analysis tests | [starlark-rule-engineering.md](references/starlark-rule-engineering.md) |
| Platforms and hermeticity | toolchains, exec groups, runfiles, sandboxing, declared inputs, reproducibility | [platforms-and-hermeticity.md](references/platforms-and-hermeticity.md) |
| Rust and TypeScript | language rules, translation, type-check gates, workers, pipelining, dependency code | [rust-and-typescript.md](references/rust-and-typescript.md) |
| Remote build infrastructure | remote cache/execution, dynamic execution, BwoB, trust, fallback, BES | [remote-build-infrastructure.md](references/remote-build-infrastructure.md) |
| Performance and incrementality | output bases, caches, workers, concurrency, profiles, controlled A/B tests | [incremental-performance.md](references/incremental-performance.md) |
| Tests, CI, and evidence | target selection, suites/tags, coverage, BEP, profiles, execution logs, formal results | [testing-ci-and-evidence.md](references/testing-ci-and-evidence.md) |
| Artifacts and supply chain | generated contracts, packages, OCI, licenses, SBOM, provenance, release outputs | [artifacts-and-supply-chain.md](references/artifacts-and-supply-chain.md) |
| Capability audit | active, partial, measure, deferred, inapplicable, or due for recheck | [capability-ledger.md](references/capability-ledger.md) |
| Current-version boundary | dated Bazel/ruleset baseline and experimental surfaces | [current-ecosystem.md](references/current-ecosystem.md) |
| Skill maintenance | trigger quality and decision behavior across agent clients | [evaluation-scenarios.md](references/evaluation-scenarios.md) |

## Choose the evidence surface

Use the Bazel layer that can answer the actual claim.

| Question | Preferred surface |
|---|---|
| Which version, workspace, output base, configuration, rc, wrapper, or remote endpoint is active? | checked-in config plus version-matched `bazel info`, help, or canonical command evidence when execution is allowed |
| Why is an external module or generated repository present? | `bazel mod` graph/path/explain/show surfaces, extension inputs, repo mapping, and the lock |
| What targets or dependency paths exist independent of configuration? | `bazel query` |
| What survives `select()`, transitions, platforms, aspects, and toolchain resolution? | `bazel cquery` with an explicit universe and relevant configuration |
| What command, inputs, outputs, tools, environment, or mnemonic would Bazel register? | `bazel aquery` |
| Can the graph load and analyze without executing actions? | a scoped `bazel build --nobuild` |
| Did the smallest relevant target build, test, or cover successfully? | `bazel build`, `test`, or `coverage` |
| What happened across an executed invocation and which tests or artifacts resulted? | complete Build Event Protocol evidence |
| Where did elapsed time and the critical path go? | retained JSON profile and version-matched profile analysis |
| Why did comparable runs produce different spawn keys or reexecute actions? | matching compact execution logs and canonical commands; use `aquery` for registered actions and BEP/profile metrics for outcomes |

Keep the boundaries explicit:

- `query` describes the unconfigured target graph.
- `cquery` describes configured target instances after flags, transitions, platforms, aspects, and `select()` choices.
- `aquery` describes registered actions without executing them.
- An execution log describes executed spawns and their inputs, arguments, environment, outputs, and cacheability; it is not the configured action graph or invocation outcome.
- BEP describes an invocation's event graph. BES transports BEP to an external service and has its own completion and privacy boundary.
- A profile explains time and critical paths; action counts alone do not establish elapsed-time impact.

When one surface resolves the question, more surfaces are optional. When evidence differs, identify the configuration, invocation, and phase represented by each.

## Climb the validation ladder deliberately

1. **Provenance and static inspection:** revision, dirty state, pins, effective configuration, labels, and existing evidence.
2. **Analysis without action execution:** `mod`, `query`, `cquery`, `aquery`, analysis tests, or a scoped `build --nobuild`.
3. **Smallest executable target:** exact owning target or reproducer.
4. **Affected closure:** relevant reverse dependencies, suites, generated consumers, output groups, or another supported platform.
5. **Named broad gate:** full suites, live canaries, E2E, packaging, or release gates only when an acceptance criterion or demonstrated impact calls for them.

Widen for graph-shaping changes such as modules, locks, rc files, shared Starlark, transitions, toolchains, platforms, public contracts, generated artifacts, suites, or release outputs. Keep diagnosis, formal acceptance, publication, and live product proof as separate authority states.

## Apply working defaults with evidence escape hatches

- State the default, reason, evidence that would justify another path, and expected proof. Reserve absolutes for authorization, secrets, destructive state, or binding release policy.
- Prefer exact labels and the smallest relevant target for diagnosis. Broad scopes remain useful for named gates and graph-wide risk.
- Treat the Bazel graph as primary dependency evidence and text search as complementary evidence for manifests, dynamic loading, credentials, and intent the graph cannot model.
- Use maintained ecosystem tools for scoped diagnosis when helpful, but return formal validation to the surface that actually owns acceptance.
- Preserve warm incremental state. Reset only for reclamation, a clean-state requirement, or a concrete corruption hypothesis.
- Measure caches, jobs, workers, pipelining, dynamic execution, filesystem strategies, and remote policies with controlled comparisons and correctness checks.
- If an expected target or capability is absent, report the control-plane gap. Repair it only when implementation is in scope.

## Stop and report honestly

Conclude when evidence answers the requested scope or a blocker prevents further decision-relevant work. A first failure is not a stopping condition for an explicitly broad audit unless it invalidates the remaining evidence or makes continued work impossible.

Do not rerun unchanged broad suites without a changed input, falsifiable flake/cache hypothesis, or named consecutive-run gate.

For a formal result, identify the revision and dirty state, exact label and command, configuration and platform, evidence layer, first failing operation, artifact identity, observed facts versus inference, remaining uncertainty, and why the investigation stopped or widened.
