---
name: exact-search-engineering
description: "Build and verify performance-critical exact searches in FLINT, Nemo, Julia, C++ or Rust when a general computer algebra system is too slow or exhaustive coverage has to be engineered explicitly."
---

# Nadle-im-Heustock (exact-search-engineering)

Turn a mathematically defined finite search into a deterministic search engine and a separate exact verifier. Preserve exactness, coverage, and replay while improving speed.

## Route by bottleneck

Read [references/implementation-routing.md](references/implementation-routing.md) before changing language or library.

- Use FLINT when the hot kernel is exact integer, rational, finite-field, or polynomial arithmetic and low-level control pays.
- Use Nemo when Julia-level composition and FLINT-backed exact arithmetic shorten the implementation without obscuring the model.
- Use C++ or Rust for tight loops, data-layout control, parallel scheduling, or a small standalone search binary.
- Use Julia for rapid specialization and orchestration when measurements show acceptable runtime and allocation behavior.

## Build contract

1. Freeze the mathematical domain, enumeration order, symmetry reductions, and acceptance predicate.
2. Create a small reference implementation and known fixtures before optimizing.
3. Measure the baseline. Profile before moving languages, adding threads, or rewriting arithmetic.
4. Move only the measured hot path. Keep the verifier simpler than the searcher and free of search-only pruning.
5. Use exact types and prove or check every narrowing conversion and overflow bound.
6. Make sharding deterministic and disjoint. Checkpoints must record the exact covered interval or canonical shard ID.
7. Compare optimized and reference implementations on exhaustive small domains plus randomized larger fixtures.
8. Preserve the receipt in [references/search-receipt.md](references/search-receipt.md).

## Claim boundaries

- A found witness is valid only after the separate verifier accepts it.
- No witness found means only that the recorded coverage was searched.
- Exhaustiveness requires a complete, duplicate-aware coverage manifest with zero unclassified skips.
- A speedup is relative to a named baseline, input distribution, build, host, and correctness gate.

Do not install toolchains, start paid compute, or reserve remote capacity without the authority required for that environment.
