---
name: attack-graphql-dos
description: "GraphQL DoS and amplification — depth/complexity abuse, query batching, alias amplification, pagination loops (authorization-gated)"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - graphql
  - dos
  - batching
  - amplification
tech_stack:
  - graphql
cwe_ids:
  - CWE-770
  - CWE-400
chains_with:
  - attack-graphql
  - attack-application-dos
prerequisites:
  - attack-graphql
---

# GraphQL DoS & Amplification

## Authorization gate — read first

DoS testing on real programs is almost always OUT OF SCOPE without explicit permission.
Demonstrate amplification with SINGLE requests that show the multiplier, not sustained
floods. Amplification-proofs are in scope on most programs; sustained floods never are.

## Methodology

### 1. Depth abuse (single request, self-recursive nesting)

```text
{ user { posts { author { posts { author { posts { ... } } } } } } }
# Depth 20-30 nesting of a recursive connection = N× DB work per request
# Measure: server response time at depth 5 vs 25 (same total size)
```

### 2. Alias amplification (one request → N backend queries)

```text
{ a1: user(id:1){...} a2: user(id:2){...} ... a999: user(id:999){...} }
# Aliases are FREE per request — batching limits that count REQUESTS don't apply
```

### 3. Real batching (the array transport)

```json
[{"query":"{user(id:1){email}}"},{"query":"{user(id:2){email}}"}, ...100s]
```

- Some servers execute array items sequentially = resource amplification in one hit
- Others PARALLELIZE = worse. Detect: total latency vs single-query latency

### 4. Directive abuse

```text
query @skip/@include combinatorics — server evaluates all branches for cost, client
receives one → cheap amplification when cost analysis ignores directives
{ expensive @skip(if:true) @include(if:true) }
```

### 5. Cyclic field reuse (fragment cycles)

```text
fragment A on User { ...B }
fragment B on User { ...A }   ← some parsers infinite-loop; others reject cleanly
```

### 6. Cost-proof framing

| What you show | Why it passes triage |
|---|---|
| One request, 100 aliases, response time ×50 | amplification, single request |
| Depth-25 query, measured DB time growth | complexity, single request |
| 10k-alias request, 500 server error | limit absence, single request |
| Sustained flood | OUT OF SCOPE — do not |

## Proof

- Timing/memory deltas from SINGLE requests (three samples each)
- The exact queries (they're the payload)
- Server error responses (500/timeout) as limit-absence evidence

## Notes

- If the server implements a depth limit: find it (document), then test whether ALIASES
  and BATCHING respect the same counter — they often don't
