---
name: tw-ideate
description: Mine a codebase for breakthrough, evidence-backed opportunities — features, additions, refactors, simplifications, DX, UX, reliability, performance, or architecture cleanup. Researches project reality first, then forces two escalation gates (reject the merely-adequate idea; expand ambition 10x then collapse to the smallest proof-bearing artifact). Outputs ranked opportunities, an escalation ledger, and one plan seed. Does not implement or create tickets.
---

# Ideate

Turn a repository, product surface, or fuzzy improvement area into a ranked portfolio of original, evidence-backed opportunities and one sharp plan seed.

Do not stop at plausible improvement ideas. First mine project reality, then force two escalation gates:

1. **Material-delta gate** — reject the merely adequate answer; require a new frame, invariant, mechanism, architecture, or artifact (not just stronger adjectives).
2. **Ambition gate** — expand the ambition horizon 10x, then collapse that larger frame into the smallest proof-bearing artifact that can be built, tested, or used next.

The result should feel surprising only because the repository evidence makes it feel obvious in hindsight.

## Core stance

- Research first. Do not ask for facts the repo can reveal.
- Default scope is the current repository or the files the user provided.
- Treat code, tests, docs, examples, issue exports, and git history as opportunity evidence.
- Prefer evidence-backed originality over generic cleanup; leverage over ornament; user/maintainer value over novelty.
- A breakthrough idea must cash out as at least one concrete mechanism, interface, proof surface, or strategy.
- Do not create tickets, task graphs, or implementation plans. Stop before implementation.

## Workflow

### 1. Establish scope and posture
Infer scope from the prompt; default to the current repo and state the assumption.

### 2. Ground in reality
Inspect available artifacts before asking questions: `AGENTS.md`/`CLAUDE.md`, `README*`, `docs/`, ADRs, roadmap/backlog/TODOs/changelog, tests/benchmarks/fixtures/examples, package manifests/build/CI, public APIs/CLI/routes/UI entry points, and git history. Capture a compact internal snapshot of repo shape, surfaces, constraints, and opportunity signals.

### 3. Harvest opportunity signals (read-only)
Look especially for:
- **User-surface signals**: CLI commands, routes, public APIs, UI flows, examples, docs promises, error messages.
- **Friction signals**: TODO/FIXME/HACK, repeated workarounds, confusing names, defensive code, manual steps in docs.
- **Architecture-seam signals**: duplicated logic, unstable boundaries, circular deps, large modules, leaky abstractions.
- **Test-intent signals**: tests revealing intended behavior, missing tests on critical paths, overcomplicated fixtures.
- **Reliability signals**: retry logic, partial-failure paths, validation gaps, cleanup, idempotency assumptions.
- **Performance signals**: hot loops, repeated I/O, N+1 access, expensive startup, slow test/build commands.
- **Negative-space signals**: names, docs, types, tests, or examples that imply a capability that does not exist yet.
- **Refactor-enabler signals**: behavior-preserving simplifications that unlock future feature work.

Capture an opportunity map with evidence; prefer exact `path:line` references.

### 4. Ask only material questions
Ask 1–3 atomic questions only after inspecting artifacts, and only for decisions that change the portfolio (target user/maintainer priority, appetite for behavior change vs preservation, near-term direction not in artifacts, constraints not inferable). Otherwise proceed with explicit assumptions.

### 5. Generate ~30 baseline candidates
Distinct, concrete, each with evidence. Suggested quotas (reallocate if the repo type makes one irrelevant): 6 user-facing features, 5 DX/CLI/API/workflow, 5 refactor/simplification, 4 reliability/correctness, 3 observability/diagnostics, 3 performance/scalability, 2 docs/onboarding (not merely "write more docs"), 2 wild-card from negative-space or hidden-primitive lenses.

Originality lenses — every shortlisted idea names one: hidden primitive, repeated workaround, negative space, sharp edge, asymmetric leverage, behavior-preserving unlock, diagnostic inversion, default-basin escape.

### 6. First winnow: 30 → 5 → 15
Hard-cut fatal flaws, weak evidence, duplication, poor fit. Score the rest. Pick the best 5 and explain why they beat the rest; add the 10 most complementary; re-rank; choose a *preliminary* leading direction. This is the input to the gates, not the final answer.

### 7. Material-delta gate
For each top-5 idea ask: why is the obvious version merely adequate? What new frame, invariant, mechanism, interface/protocol, architecture move, or artifact was absent from the baseline? What stronger move now dominates? A valid pass produces at least one material delta; intensified wording does not count. If an idea cannot improve materially, cut or demote it.

### 8. Ambition gate
For the strongest survivors (usually top 3), produce: the 10x ambition horizon, the systemic leverage point it exposes, the smallest artifact that preserves the 10x insight, why that artifact carries the larger frame without grandiosity, and the first proof signal. A valid pass cashes out as a concrete mechanism, interface/protocol, proof surface, or strategy. No hype.

### 9. Breakthrough synthesis
Re-score escalated candidates. For each survivor keep a compact escalation chain:
```md
- Baseline idea:
- Why the obvious version loses:
- Material delta:
- 10x frame:
- Smallest proof-bearing artifact:
- Cash-out type: Mechanism | Interface | Proof surface | Strategy
- First proof signal:
- Evidence anchor (path:line):
```
The final leading direction must beat alternatives on both ordinary value and escalation quality.

### 10. Check overlap
Inspect artifacts (roadmap, TODOs, issue exports, past/reverted work, naming collisions, flagged features) and classify each shortlisted idea: direct duplicate / adjacent / conflicts with direction / genuinely net-new / unknown. Use `rg`, `grep`, `fd`, `git log`.

### 11. Refine the leading direction
Run critique passes: (1) value & shape, (2) architecture & behavior risk, (3) evidence & originality, (4) material delta, (5) ambition cash-out & proof. Do not overspecify implementation — produce a strong starting shape, not a disguised design.

## Output contract

1. Compressed repo snapshot
2. Opportunity map grouped by signal theme
3. Escalation ledger (the material-delta and ambition transformations)
4. Top 5 breakthrough ideas (rank, evidence, originality source, material delta, 10x frame, proof-bearing artifact, validation path, overlap status)
5. Next 10 ideas (shorter, evidence-backed)
6. Ideas cut and why (including escalation failures)
7. Overlap findings
8. Chosen direction
9. One plan seed (problem, target user/maintainer, smallest artifact, first proof signal, key risks) — self-contained enough that a later planning pass can pick it up

If no candidate passes both gates, say so explicitly and present the strongest grounded portfolio as non-breakthrough rather than manufacturing novelty.

## Anti-patterns

Do not: brainstorm before inspecting artifacts; ask for facts the repo answers; reward flashiness over usefulness; confuse ambition with scope bloat; let the gates become rhetoric or grandiosity; stop at "here are some ideas" with no ranking logic; propose generic "add tests/docs" without a sharper underlying opportunity; convert results into tickets; or confuse a plan seed with a detailed plan.
