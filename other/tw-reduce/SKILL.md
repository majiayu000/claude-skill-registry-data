---
name: tw-reduce
description: Audit over-engineered codebases by factoring layers into live obligations, quotienting redundant distinctions, ablating unearned surface, and normalizing survivors while preserving required behavior. Use when change latency or agent difficulty comes from frameworks, plugins, DI, codegen, task runners, config indirection, ORMs, GraphQL, monorepo/infra tooling, or web stacks, or when asked to remove layers. Produces an evidence-backed Reduction Certificate, cuts, migration phases, proof signals, and rollback. Not for one local readability cleanup (use tw-complexity-mitigator).
---

# Reduce

## Purpose

Act as the architecture **winnowing** reviewer. Find costly abstractions whose live obligation is unproven, expired, moved, duplicated, invalid, or outweighed by their change tax. Recommend lower-level normal forms while preserving essential truth.

The default product is a decision package and a Reduction Certificate, not a patch. Implement only when the user explicitly asks.

## Doctrine

```text
WINNOWING = FACTORING -> QUOTIENTING -> ABLATIVE -> NORMALIZING
guard: REFINEMENT-PRESERVING
```

- **Factoring**: decompose each layer into distinct obligations, owners, inputs, outputs, dependencies, observations, and recomposition roles.
- **Quotienting**: collapse distinctions or layers no live observation can distinguish, after congruence checks.
- **Ablative**: remove, collapse, privatize, slice, or decommission factors with no distinct live obligation.
- **Normalizing**: recompose retained factors around canonical owners and lower-level primitives.
- **Refinement-preserving**: preserve required behavior and obligations while allowing obsolete, invalid, duplicated, or unrequired behavior to disappear.

`Isomorphic` and `observationally-equivalent` are stricter proof relations, not reduction objectives.

## When to use

- frameworks, plugins, decorators, middleware, DI/service locators, factories, adapters, reflection wiring;
- code generation, generated clients, schema/build generators, task runners, monorepo tooling, config inheritance;
- ORMs, GraphQL gateways, repository layers, event buses, workflow engines, queues, microservice boundaries;
- Helm/Kustomize/Terraform/Kubernetes/CI wrappers;
- web stacks where native platform primitives may replace framework/build layers;
- any architecture where a simple change crosses many files, tools, generated artifacts, conventions, or hidden control flow.

Do not use for one local readability cleanup — route that to `tw-complexity-mitigator`. If the system lacks essential structural shape (the real problem is missing abstraction, not excess), that is a *climb*, not a reduction — say so and stop.

## Operating rules

1. Preserve required behavior unless explicit authority changes the contract.
2. Preserve essential truth: invariants, protocols, authorization, data integrity, auditability, public contracts, external obligations.
3. Use repo-local evidence first.
4. Treat absent evidence as uncertainty, not permission to delete.
5. Prefer reversible cuts and staged migration.
6. Do not add tools to remove tools unless total complexity falls and the user accepts the trade.
7. If evidence is incomplete, mark the audit provisional and cap destructive verdicts at `hold`, `wrap`, `split`, or `validate-first`.
8. Separate the reduction operator from the preservation relation.
9. Every removed factor needs obligation discharge. Every proposed normal form needs recomposition proof.

## Workflow

### 1. Build an altitude and boundary map
Identify layers at altitudes 0–5, the lower primitives beneath them, public/wire/storage boundaries, proof surfaces, and any invariant each layer carries.

### 2. Trace real paths
For each major abstraction, trace at least one real change/request/command path: entrypoint → factors/layers crossed → generated/configured behavior → runtime side effects → proof surfaces → where reasoning becomes expensive.

### 3. Factor by live obligation
For every candidate, fill:

| factor | live obligation | owner | inputs/outputs | dependencies | observations | external commitment | recomposition role |
|---|---|---|---|---|---|---|---|

Obligation status is exactly one of: `live | moved | expired | duplicated | invalid | unknown`.

### 4. Measure tax and value
Record edit/lookup/tool/hidden/deploy hops, diff opacity, proof latency, coupling and lifecycle constraints, proven value, external-obligation risk, and confidence. Keep value and obligation risk separate.

### 5. Find quotient candidates
Ask whether multiple factors differ only in implementation, naming, or historical layering. Before quotienting: state the observation set, define the equivalence relation, test congruence across accepted operations/transitions, and preserve every witnessed distinction.

### 6. Essential-abstraction check
Before replacement or deletion, check for product, coproduct, refinement/equalizer, pullback/agreement, supplied-behavior/exponential, free construction, protocol, or external obligation. If essential shape exists: reduce wrapper tax first, preserve or improve the invariant representation, and flag a *climb* if the missing shape is the real problem.

### 7. Score candidates
```text
T = change/agent tax   V = proven value   D = T - V
dominance = dominant | dominated | incomparable | unknown
```
A factor is `dominated` only when another route covers its live obligation with lower total semantic surface or stronger proof.

### 8. Select an operator-level verdict
`keep | hold | factor | quotient | wrap | split | collapse | ablate | privatize | decommission | normalize | replace | validate-first | climb`

### 9. Produce the Reduction Certificate (RC)
For technical debt, default the proof relation to `refinement-preserving`. Use `observationally-equivalent` only with an explicit observation set. Use `isomorphic` only with a witnessed reversible correspondence.

```text
Reduction Certificate
- target factor / layer:
- live obligation status:
- operator verdict:
- proof relation: refinement-preserving | observationally-equivalent | isomorphic
- observation set (if any):
- recomposition proof:
- removed obligation discharge:
- residual risk / unknowns:
```

### 10. Migration plan
For each approved cut: first safe phase, allowed files/commands, proof signal, rollback, owner of unknowns, stop condition, recomposition check.

## Required output

1. Scope and assumptions
2. Altitude / boundary map
3. Evidence ledger
4. Factorization map
5. Tax/value/dominance table
6. Quotient candidates and congruence status
7. Essential-abstraction check
8. Prioritized winnowing decisions
9. Target normal form
10. Reduction Certificate(s)
11. Migration plan
12. Risks and unknowns
13. Winnowing Bottom Line

```text
Winnowing Bottom Line:
- factor:
- quotient:
- ablate:
- normalize:
- preserve because:
- proof relation:
- first safe move:
```

## Implementation mode

When explicitly asked to implement: do exactly one certified reduction seam at a time; preserve the old surface until the selected proof relation passes (unless direct deletion is already proven safe); run a recomposition audit before moving to the next seam; stop on any new observation or lost obligation.
