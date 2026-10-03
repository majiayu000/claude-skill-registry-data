---
name: overkill
description: Propose advanced, maximalist alternatives to whatever solution is being discussed — the techniques, data structures, frameworks, and tooling that lie beyond the pragmatic answer. Invoke when the user says "overkill", "overkill this", "/overkill", "make it enterprise", "what's the advanced version", or otherwise asks for the maximalist, future-proofed, or frontier take on a problem. Supports flags `--max` (only show 🔥 7+ options), `--advanced` (operator-focused comparison table), and `--current` (use web search to fetch up-to-date references and verify project health, when web access is available). Returns a ranked set of alternatives — advanced data structures, distributed-systems algorithms, niche frameworks, design patterns, and frontier tooling — each scored on a calibrated complexity scale, with links to learn more, the skills the path develops, and the future-scale scenarios in which it pays off. This skill expands the user's map of what is possible; it is not a pragmatic recommendation engine and should not be used when the user wants the simplest sufficient answer.
---

# Overkill

Take the current problem a step beyond its pragmatic answer. Surface advanced data structures, distributed-systems algorithms, niche frameworks, design patterns, and frontier tooling that go further than the baseline requires — and rank them on a calibrated complexity scale so the user can see the true scope and learning surface of each.

## When to Use This Skill

- The user has a working or proposed solution and asks `overkill`, `overkill this`, `/overkill`, `overkill --max`, `overkill --advanced`, or `overkill --current`.
- The user asks "what's the advanced version of this?", "make it enterprise / FAANG-grade / future-proof", "give me the maximalist take", or "show me what's past the pragmatic answer."
- The user is exploring the design space for learning, technical due diligence, or curiosity about what frontier techniques exist for a class of problem.

Do not use this skill when the user wants the simplest sufficient solution, an MVP, or a direct production recommendation. The skill explores the maximalist end of the design space; presenting its output as a default recommendation would mislead. If unsure of the user's intent, ask one clarifying question first.

## What This Skill Does

1. **Restates the baseline**: identifies the current pragmatic solution in one sentence so every alternative has a fixed reference point.
2. **Proposes 3–6 advanced alternatives**: each from a distinct category (data structures, algorithms, frameworks, design patterns, tooling), ordered from most well-known to most obscure within the requested complexity range.
3. **Scores each option on a calibrated complexity scale** (🔥 1–10) anchored across responses, so scores are comparable across invocations.
4. **Produces a comparison table** tailored to the requested mode — a learner-focused table by default, or an operator-focused table in `--advanced` mode.
5. **Surfaces learning resources and a skill profile** for each option so the user can act on the suggestion as a study path, not just an architectural reference.

## How to Use

### Basic Usage

```
overkill
```

When the user invokes `overkill` without any flags, **pause and ask which modes to apply before producing output.** Present the three modes as a multi-select picker (or, in environments without structured prompts, a numbered list) so the user can opt in to any combination — or none, for default behavior. Use this exact phrasing for each option:

- **`--max`** — Restrict suggestions to the highest-complexity options (🔥 7/10 and above). Pick this when you already know the moderate options and want only the frontier.
- **`--advanced`** — Switch the comparison table to operator-focused columns (ops burden, hiring difficulty, time to first commit). Pick this if you are evaluating real adoption cost rather than learning.
- **`--current`** — Use web search to fetch up-to-date references and verify project health. Adds latency. Pick this for research or when references must reflect the current state of a fast-moving area.

After the user selects (any subset, including nothing), proceed to produce the response with the chosen modes applied. The selection is per-invocation — do not carry it across future `overkill` calls in the same conversation; ask again each time.

If the user invokes `overkill` with **any** flag already passed (e.g., `overkill --max`, `overkill --current`, `overkill --advanced --current`), skip the picker entirely and run with exactly the flags they passed. The picker exists to surface modes to users who do not know they exist; users who pass flags have already chosen.

In all cases the response returns 3–6 ranked alternatives with complexity scores, learning links, skills profile, and the future-scale scenarios in which each pays off.

### Advanced Usage

```
overkill --max
```

Restricts the proposed alternatives to options at 🔥 7/10 and above. Useful when the user already knows the moderate-complexity options and wants only the frontier.

```
overkill --advanced
```

Switches the comparison table to the operator-focused columns — ops burden, hiring difficulty, time to first commit — instead of the default learner-focused columns. Intended for managers, staff engineers, or platform leads evaluating real adoption cost.

```
overkill --current
```

Opts in to web search. The skill verifies that recommended frameworks/runtimes/libraries are still maintained, surfaces papers or primary documentation released after the model's training cutoff, and prefers fresh canonical references over older ones in the "Learn more" field. Use when the user is doing research, technical due diligence, or wants citations that reflect the current state of a fast-moving area. Default mode stays offline and deterministic; `--current` trades latency and consistency for currency.

Flags can be combined freely: `overkill --max --advanced --current`.

## Output Format

A single response with three sections, in this order.

### 1. The baseline, restated

One sentence on what's currently being discussed. If the conversation is too vague to identify a baseline, ask the user one clarifying question before proceeding.

### 2. Overkill alternatives (3–6 options)

Each option follows this template:

```
#### <Name of the approach> — Complexity: 🔥 N/10

**What it is:** one or two sentences on the actual mechanics.
**How it goes beyond the baseline:** the specific capability or guarantee it adds that the baseline lacks.
**Skills developed by this path:** the concrete technical knowledge a practitioner gains from adopting it (e.g., "lock-free programming, memory ordering, ABA-problem mitigation").
**Learn more:** 1–3 high-signal links — original papers, canonical posts, primary documentation. Prefer durable sources (papers, language/library docs, well-cited blog posts) over news articles.
**Scenario where it pays off:** the concrete future state in which this option becomes the correct choice — be specific about scale, latency, consistency, or team conditions.
```

Order options from **most well-known → most obscure** within the chosen complexity range. Mix categories — do not return six frameworks. Aim for variety across:

- **Data structures**: skip lists, persistent / immutable trees, HAMTs, Bloom / Cuckoo / Quotient filters, Count-Min Sketch, HyperLogLog, succinct data structures, wavelet trees, finger trees, Roaring bitmaps, Y-Fast Trie, van Emde Boas trees.
- **Algorithms**: lock-free / wait-free variants, MVCC, CRDTs, Raft / Paxos, vector clocks, consistent hashing with bounded loads, hopscotch / Robin Hood hashing, FM-index, learned indexes, approximate nearest neighbor (HNSW, FAISS).
- **Frameworks / runtimes (well-known → niche)**: Kubernetes, gRPC, Kafka → Temporal, NATS JetStream, Materialize, ScyllaDB → Pony, Pharo, Unison, Roc, Gleam on BEAM, Verona.
- **Design patterns**: CQRS + Event Sourcing, Hexagonal / Ports & Adapters, Saga, Outbox, Actor Model, Free monads / tagless final, dependency-inverted plugin architectures, capability-based security.
- **Tooling / infra**: OpenTelemetry + Tempo + Loki + Grafana + Prometheus, eBPF observability (Pixie, Parca), service meshes (Istio, Linkerd, Cilium), Nix flakes + devShells, Bazel / Pants / Buck2, formal verification (TLA+, Alloy, Coq, Lean), property-based + mutation + fuzz testing, chaos engineering (Litmus, Chaos Mesh).

### 3. Comparison table

**Default mode** — learner-focused columns:

| Approach | Complexity | Skills developed | Learn more | Payoff horizon |

**`--advanced` mode** — operator-focused columns:

| Approach | Complexity | Time to first commit | Ops burden | Hiring difficulty | Payoff horizon |

In both modes, use the same 🔥 N/10 scale for Complexity. "Payoff horizon" should be expressed as the concrete scale, load, or organizational condition under which the option starts to earn its cost (e.g., "≥10⁹ events/day", "multi-region active-active with RPO=0", "team size >50 with independent deploy cadence").

## Behavior with `--current`

When the user passes `--current`, use web search and web fetch as part of preparing the response. Concretely:

1. **Verify project health** for any recommended framework, runtime, or library that is younger or less mainstream than the well-established options. Check the project's primary repository or website for recent commit activity, the most recent release date, and any explicit deprecation or hand-off notices. If a project is dormant, abandoned, or has been superseded, either replace it with the current equivalent or annotate the "What it is" line so the user is not led to dead tooling.
2. **Refresh "Learn more" links.** Prefer references that are both authoritative *and* recent enough to reflect the current state of the technique: the canonical paper plus a follow-up or revision from the last 1–2 years when one exists; primary documentation at its current URL rather than a snapshot from training data; a well-cited recent blog post over an older one if the technique has materially evolved. Keep the link count to 1–3 per option — currency, not volume, is the goal.
3. **Surface significant new options** that did not exist at the model's training cutoff if they would meaningfully reshape the response (e.g., a new consensus protocol, a runtime that has crossed into production-readiness, a paper that supersedes an older technique). Place them in the order rule (well-known → obscure) on their current standing, not their novelty.
4. **Budget search calls.** Aim for one focused search per option that needs refreshing, not exhaustive sweeps. Skip search entirely for options where the references are durable and stable (e.g., a 1990s paper on a foundational data structure does not need re-checking).
5. **Degrade gracefully.** If web search or web fetch is unavailable in the current environment, do not block the response. Fall back to the offline behavior and add a one-line note to the user: "`--current` requested but web access is not available in this environment; response uses training-cutoff references." Do not silently produce stale-looking content as if it were current.

## The complexity scale

Anchor the 🔥 N/10 scores so they stay calibrated across responses:

- 🔥 1–2: Library swap or a single new abstraction. Shippable in hours; minimal review burden.
- 🔥 3–4: A new pattern introduced to the codebase. Days to weeks of refactor; team-wide familiarity expected.
- 🔥 5–6: A new runtime dependency (queue, cache, sidecar). Adds an operational surface and an SLO to defend.
- 🔥 7–8: Introduces a distributed-systems concern — consensus, replication, partial failure. Requires on-call coverage and runbooks.
- 🔥 9: Research-grade. Implementation depends on primary literature; few production references exist.
- 🔥 10: Requires specialist hiring or a runtime / language with a small global user base. Long-term maintenance is a strategic commitment.

If the user passes `--max`, only return options at 🔥 7+.

## Tone

Serious, technically precise, and curious. Treat the user as an engineer who already knows the pragmatic answer and wants to understand what lies beyond it — the techniques, trade-offs, and frontier ideas they would otherwise never encounter. Explain each option with the rigor of a design review: real mechanics, real failure modes, real costs. The goal is depth and exposure, not humor. Do not editorialize that an option is "absurd" or "ridiculous" — the complexity score and the skills-developed line do that work objectively.

## Example

**User**: "I'm deduplicating webhook deliveries using an in-process set keyed by delivery ID. overkill"

**Output** (abbreviated):

> **Baseline:** an in-process set keyed by delivery ID, used to deduplicate webhook deliveries on a single node.
>
> #### Redis SET with TTL — Complexity: 🔥 2/10
> **What it is:** `SADD` with a per-key `EXPIRE` providing a shared dedup window across processes.
> **How it goes beyond the baseline:** dedup state survives process restarts and is consistent across multiple delivery workers.
> **Skills developed:** Redis data-structure idioms, TTL-based memory budgeting, designing for partial-availability of a shared cache.
> **Learn more:** [Redis SET docs](https://redis.io/commands/set/), [Redis as a cache: pattern guide](https://redis.io/docs/latest/develop/use/patterns/).
> **Scenario where it pays off:** horizontally scaled delivery workers (≥2 nodes) where in-process state diverges and at-least-once semantics are no longer acceptable.
>
> #### Roaring Bitmaps over a Kafka compacted topic — Complexity: 🔥 8/10
> **What it is:** delivery IDs are hashed into dense integer space and tracked in Roaring Bitmaps, with the authoritative state replayed from a Kafka compacted topic so any consumer can deterministically rebuild the dedup set.
> **How it goes beyond the baseline:** O(1) membership tests at billions-of-ID scale, log-structured durability, and replayable state for new consumers or disaster recovery.
> **Skills developed:** compressed bitmap engineering, hash-distribution analysis, Kafka log-compaction semantics, replayable state-machine design.
> **Learn more:** [Roaring Bitmaps paper (Chambi et al., 2014)](https://arxiv.org/abs/1402.6407), [Kafka log compaction](https://kafka.apache.org/documentation/#compaction).
> **Scenario where it pays off:** ≥10⁹ delivery IDs retained across a multi-week window, with multiple independent consumers that must agree on dedup state without a shared database.
>
> *(comparison table follows in the requested mode)*

## Tips

- Identify the baseline before proposing alternatives. Without a fixed reference point, complexity scores are meaningless.
- Prefer category variety over depth in any one category. A response of six frameworks teaches less than a response spanning a data structure, an algorithm, a framework, a pattern, and a piece of tooling.
- Keep "Learn more" links durable — papers, primary documentation, well-cited writeups. Avoid blog posts that will rot. In `--current` mode, prefer recent authoritative sources over older ones when the technique has materially evolved.
- Calibrate scores against the anchor list every time. Score drift across invocations defeats the purpose of the scale.
- If the user is in `--advanced` mode, lean into the operational cost framing — the audience is making a real adoption decision, not exploring.
- In `--current` mode, budget searches deliberately. One focused query per option that needs refreshing beats four scattered ones. Foundational techniques (a 1990s data-structure paper, a settled algorithm) usually do not need re-verification at all.

## Common Use Cases

- An engineer is implementing a feature and wants to understand the full design space before committing to the simple option.
- A staff or principal engineer is preparing a tech-design document and wants a survey of advanced alternatives to cite and rule out.
- A team is doing technical due diligence on a vendor's claims ("they use X") and wants to understand where X actually sits on the complexity spectrum.
- An engineer is choosing a learning project and wants a study path anchored to a real problem rather than an abstract topic.
- A platform or staff engineer (in `--advanced` mode) is evaluating adoption cost of a frontier technology for their organization.

## Final note

This skill is for explorers and engineers who want to take a problem a step further than the pragmatic answer — to see the advanced data structures, distributed-systems techniques, and frontier tooling that exist at the edges of the field. Treat every suggestion as a serious object of study, not a punchline. The complexity score and the skills-developed line are the honest signals of cost; the user is capable of deciding what to do with it. The job of the skill is to expand the user's map of what is possible, accurately.
