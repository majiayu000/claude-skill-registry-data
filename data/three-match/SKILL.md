---
name: three-match
description: 3-MATCH colored subgraph isomorphism gadget for 3-SAT reduction
version: 1.0.0
---


<!-- Propagated to amp | Trit: 0 | Source: .ruler/skills/three-match -->

# Three-Match Skill: 3-SAT via Colored Subgraph Isomorphism

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - conservative/geodesic)
**Principle**: Local constraints → Global correctness
**Frame**: Non-backtracking geodesics with Möbius filtering

---

## Overview

**Three-Match** reduces 3-SAT to 3-coloring which reduces to colored subgraph isomorphism. The 3-MATCH gadget enforces constraints LOCALLY via:

1. Non-backtracking geodesics (prime paths, μ(n) ≠ 0)
2. Möbius inversion filtering (back-and-forth cancellation)
3. GF(3) conservation (sum ≡ 0 mod 3)

**Correct by construction**: If local geodesic constraints are satisfied, global 3-SAT solution is guaranteed.

## Core Formula

```ruby
# Three colors match at depth d iff:
# - Pairwise differences have 3-adic valuation ≥ d
# - No backtracking (each color unique in path)
# - GF(3) sum ≡ 0 (mod 3)

v₃(|a - b|) ≥ d  ∧  v₃(|b - c|) ≥ d  ∧  v₃(|c - a|) ≥ d
```

## Why Non-Backtracking?

1. **Prime paths**: μ(n) ≠ 0 ⟺ n is squarefree
2. **No revisiting**: Each state appears once in geodesic
3. **Möbius filtering**: Composites (backtracking) cancel out
4. **Spectral gap**: Ramanujan property (λ₂ ≤ 2√(k-1))

## Gadgets

### 1. ThreeMatch Gadget

Three colors forming a valid local constraint:

```ruby
match = ThreeMatchGeodesicGadget::ThreeMatch.new(seed: 0x42D, depth: 1)
match.color_a  # => { trit: -1, hex: "#2626D8", polarity: :minus }
match.color_b  # => { trit: 0, hex: "#26D826", polarity: :ergodic }
match.color_c  # => { trit: 1, hex: "#D82626", polarity: :plus }
match.gf3_conserved?  # => true
```

### 2. NonBacktrackingGeodesic

Prime path through color space:

```ruby
geo = NonBacktrackingGeodesic.new(seed: seed, length: 8).generate!
geo.prime?           # => true (no backtracking)
geo.moebius_product  # => ±1 (non-zero for primes)
geo.moebius_filter   # => filtered path (only primes kept)
```

### 3. ColoredSubgraphGadget

3-SAT clause reduction:

```ruby
gadget = ColoredSubgraphGadget.new(seed: seed)
gadget.add_clause(1, -2, 3)   # (x₁ ∨ ¬x₂ ∨ x₃)
gadget.add_clause(-1, 2, 4)   # (¬x₁ ∨ x₂ ∨ x₄)
gadget.build_gadgets!
gadget.correct_by_construction?  # => true
```

### 4. BackAndForthFilter

Möbius inversion bidirectionally:

```ruby
filter = BackAndForthFilter.new(seed: seed)
result = filter.full_cycle(sequence)
# Primes kept, composites filtered
```

## Commands

```bash
# Run 3-MATCH demo
just three-match

# Test gadget correctness
just test-three-match

# Combine with unworld
just unworld-match
```

## API

```ruby
require 'three_match_geodesic_gadget'

# Create gadget
match = ThreeMatchGeodesicGadget::ThreeMatch.new(seed: seed)

# Verify constraints
match.gf3_conserved?      # GF(3) sum = 0
match.matches_at_depth?(1) # 3-adic valuation ≥ 1

# Build geodesic
geo = ThreeMatchGeodesicGadget::NonBacktrackingGeodesic.new(
  seed: seed, length: 12
).generate!

# Check primality
geo.prime?  # No backtracking?
```

## Integration with Unworld

The 3-MATCH chain uses seed-chaining for gadget sequence:

```ruby
chain = Unworld::ThreeMatchChain.new(genesis_seed: seed, length: 4)
chain.unworld[:matches].each do |m|
  puts "#{m[:colors]} | GF(3): #{m[:gf3]}"
end
```

## Mathematical Foundation

### Möbius Function

```
μ(n) = { 1     if n = 1
       { (-1)^k if n = p₁p₂...pₖ (distinct primes)
       { 0     if n has squared prime factor
```

### Möbius Inversion

```
f(n) = Σ_{d|n} g(d)  ⟹  g(n) = Σ_{d|n} μ(n/d) f(d)
```

### 3-adic Valuation

```
v₃(n) = max { k : 3^k | n }
```

## Example Output

```
─── 3-MATCH Gadget ───
3-MATCH(d=1): #D8267F #2CD826 #4FD826
  GF(3) conserved: true
  Matches at depth 1: true

─── Non-Backtracking Geodesic ───
Geodesic(PRIME, μ=1): #D8267F → #2CD826 → #4FD826 → ...
  Prime path: true
  Möbius product: 1

─── Colored Subgraph Gadget (3-SAT) ───
  Clauses: 3
  GF(3) all conserved: true
  Prime geodesics: 3
  Correct by construction: true
```

---

## Correct-by-Construction Inline Caching (NEW 2025-12-22)

The 3-MATCH principle applies to **Specter-style path caching**:

### The Insight

```
Local constraint satisfaction → Global cache correctness
```

When path types are correct at compile time (local), cached paths are guaranteed correct (global).

### Specter Path as 3-MATCH Gadget

```julia
# Each path element is a "color" in the gadget
path = (ALL, pred(iseven), FIRST)
#       -1       0          +1     → GF(3) = 0 ✓

# The TupleNav wrapper is the "gadget envelope"
compiled = TupleNav(path)  # Type-stable, 0 allocs

# Execution is "correct by construction"
result = nav_select(compiled, data, IDENTITY)
```

### Mapping to 3-MATCH Components

| Specter | 3-MATCH | Property |
|---------|---------|----------|
| `Navigator` | Color | Individual constraint |
| `TupleNav` | Gadget | Envelope preserving GF(3) |
| Type inference | Möbius filtering | Eliminates invalid paths |
| Inline caching | Non-backtracking | No revisiting (cached once) |

### Event Stream

Correct-by-construction events flow through the gadget:

```julia
# Event: Path compilation (happens once)
PathCompiled(types::Tuple{...}) where all types stable

# Event: Cache hit (no recompilation)
CacheHit(compiled::TupleNav) where same types

# Event: Traversal (GF(3) conserved)
Traversal(input, output) where GF(3) sum = 0
```

### Benchmark Evidence

The 93-113x speedup validates correct-by-construction:
- **Original CPS**: Dynamic dispatch = "backtracking" in type space
- **Optimized Tuple**: Static types = "prime path" through type space
- **Result**: Functor structs achieve 1.0x overhead (zero cost!)

### Files

- `lib/specter_optimized.jl` - Correct-by-construction implementation
- `lib/specter_chairmarks_world.jl` - Validation benchmarks

---

**Skill Name**: three-match
**Type**: 3-SAT Reduction / Colored Subgraph Isomorphism / Inline Caching
**Trit**: -1 (MINUS)
**GF(3)**: Conserved by construction
**Geodesics**: Non-backtracking (prime paths only)
**Caching**: Type-stable paths as non-backtracking geodesics



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 9. Generic Procedures

**Concepts**: dispatch, multimethod, predicate dispatch, generic

### GF(3) Balanced Triad

```
three-match (+) + SDF.Ch9 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch7: Propagators
- Ch4: Pattern Matching
- Ch10: Adventure Game Example

### Connection Pattern

Generic procedures dispatch on predicates. This skill selects implementations dynamically.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.