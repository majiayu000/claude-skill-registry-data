---
name: mathguard
description: Math-heavy escalation for n >= 10^6 — Bloom, HyperLogLog, Count-Min, MinHash/LSH, FFT, JL projection, sweep line. Use when classical O(n log n) is the floor and approximate or math wins. 
category: Document Processing
source: antigravity
tags: [claude, ai, design, document, image, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/mathguard
---


# mathguard — Math-Heavy Optimization for AI Code

`lemmaly` makes you pick the right classical algorithm. `mathguard` kicks in when the classical algorithm is already optimal but **mathematics gives a better bound** — usually by accepting bounded approximation, exploiting structure, or moving to a smarter algebraic space.

The model knows these techniques. It almost never proposes them spontaneously. mathguard fixes that.

**Violating the letter of these rules is violating the spirit of the skill.** A Bloom filter where the caller assumed exact answers is a production incident, not an optimization.

## When to Use This Skill

Use **mathguard** when:

- Working with large-scale data (`n ≥ 10⁶`): similarity search, deduplication, top-K / heavy-hitters, streaming analytics, cardinality estimation, embeddings, recommender systems.
- Doing signal/image processing, polynomial or big-integer arithmetic, convolution, graph distance, computational geometry, randomized algorithms.
- The classical O(n log n) is already the floor and you need an asymptotic win (Bloom filter, HyperLogLog, Count-Min Sketch, MinHash/LSH, FFT/NTT, Johnson-Lindenstrauss projection, sweep line, kd-tree/BVH, fast exponentiation, monoid parallel reduction, amortized potential method).
- Loaded *after* `lemmaly` has confirmed the classical answer is not enough.

Do **not** use mathguard when:
- The caller needs exact answers (auth, billing, dedup-for-correctness, primary keys).
- `n` is small (n < 10⁴) and the path is not hot.
- The bottleneck is I/O, not CPU/memory.

## The Iron Law

```text
NO APPROXIMATE STRUCTURE WITHOUT WRITTEN ε/δ AND EXPLICIT CALLER ACCEPTANCE
```

Probabilistic data structures (Bloom, HyperLogLog, Count-Min, MinHash/LSH, t-digest), randomized projections (JL), and lossy transforms (floating FFT) all change the answer's meaning. Before proposing one:

1. Write the error parameter the caller will see (false-positive rate, relative error, distortion bound).
2. Identify the caller and state, in one sentence, that they tolerate this kind of wrong answer.
3. If you cannot identify the caller, or they need exact (auth checks, billing, dedup keys, deduplication for correctness, anything that flows into a primary key), DO NOT propose the approximate structure. Keep classical, or escalate to a sharded/streaming exact design.

This rule has saved more incidents than any other in this skill. Do not soften it.

## Non-negotiable rules

1. **Declare exact vs approximate up front.** Before suggesting a math-level technique, state:
   - `mode: exact` or `mode: approximate`
   - If approximate: the error parameter (ε, δ, false-positive rate) and a sentence on whether the caller can tolerate it.
   - If the caller needs exact and there is no exact win, say so and stop — do not silently degrade to approximate.

2. **Cite the technique by name.** Never describe a probabilistic or numerical trick in vague terms. Name it: `Bloom filter`, `HyperLogLog`, `Count-Min Sketch`, `MinHash + LSH`, `Johnson–Lindenstrauss projection`, `FFT`, `NTT`, `fast exponentiation`, `Karatsuba`, `Strassen`, `sweep line`, `kd-tree`, `BVH`, `union-find with path compression`, `Floyd's cycle detection`, `Boyer-Moore majority`, `reservoir sampling`, `Knuth shuffle`, `Aho-Corasick`, `suffix automaton`, `segment tree with lazy propagation`, `Fenwick tree`, `monoid scan / parallel prefix`. A named technique is auditable; "a smart approximation" is not.

3. **State the trade you are making.** Every math-level optimization buys something at a cost. In one line:
   - Buys: `space`, `time`, `wall-clock`, `parallelism`.
   - Costs: `accuracy ε=?`, `code complexity`, `dependency`, `non-determinism`, `numerical stability`.
   - If the cost is invisible to the caller, write "callers see no change".

4. **Justify the asymptotic win.** Do not propose a math technique without a one-line bound argument:
   - "HyperLogLog: count uniques in O(log log n) bits at standard error 1.04/√m."
   - "FFT: polynomial multiplication O(n log n) vs schoolbook O(n²)."
   - "JL projection: preserves pairwise distances within (1±ε) using O(log n / ε²) dimensions."
   - "Sweep line: rectangle overlap from O(n²) pair checks to O(n log n) events."
   No bound, no proposal.

5. **Forbid math cargo-culting.** Do not introduce these techniques when:
   - n is small enough that a linear scan finishes in microseconds (n < ~10⁴ unless it is a hot path).
   - The problem is I/O-bound — the math win disappears behind network/disk.
   - Exact answers are required and no exact technique exists.
   - The team will not maintain it (write that down: "team familiarity: ?").

## The pre-proposal protocol

Before suggesting a math-level technique, your message must contain — in this order:

1. **The classical floor** — what is the best non-mathy algorithm and its Big-O? ("Hash join is O(n+m); we're already there.")
2. **Why classical is not enough** — n too large, space blows up, real-time deadline, etc.
3. **The mat
