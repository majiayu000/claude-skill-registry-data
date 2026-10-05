---
name: catp
description: Category-theoretic pipes with GF(3) flow balance checking. Validates
  data transformation pipelines using triadic trit algebra.
metadata:
  interface_ports:
  - Integration Points
trit: 1
---
# catp: Categorical Pipes

**Trit**: +1 (PLUS)  
**Principle**: Balanced data flows through morphism chains  
**Algebra**: GF(3) flow conservation

## Why GF(3)?

Three-phase data flow:
- **Source** (-1): Read/Fetch ingestion
- **Transform** (0): Shape-preserving operations  
- **Sink** (+1): Write/Output operations

Sum must = 0 (mod 3) for balanced pipeline.

## Operations by Trit

| Trit | Category | Operations |
|------|----------|-----------|
| -1 | MINUS (Sources) | slurp, read, fetch, query, search, list |
| 0 | ERGODIC (Transforms) | map, filter, select, rename, mutate, reduce, join, group-by |
| +1 | PLUS (Sinks) | println, print, write, save, spit, create, send |

## Usage

```bash
# Check balance of a pipe
bb catp.bb --check '(->> [1 2 3] (map inc) (filter odd?) (reduce +))'

# Output:
# Operations: map %>% filter %>% reduce
# Trits: {"map" 0, "filter" 0, "reduce" 0}
# Sum: 0 (mod 3 = 0)
# GF(3) Balanced: ✓
```

## Example: Unbalanced Pipeline

```clojure
;; WRONG: Two transforms, one sink (missing source)
(->> (map inc)           ; 0
     (filter odd?)       ; 0
     (reduce +))         ; 0
     
; Sum: 0 ✓ (looks balanced but logically missing source!)
```

## Example: Properly Balanced

```clojure
;; CORRECT: Source → Transform → Sink
(->> [1 2 3]             ; implicit source (-1)
     (map inc)           ; transform (0)
     (filter odd?)       ; transform (0)
     (println))          ; sink (+1)

; GF(3): -1 + 0 + 0 + 1 = 0 ✓
```

---

## End-of-Skill Interface

## Integration Points

- **babashka** (->> threading)
- **drive-acset** (query chains)
- **l-space** (narrative pipes)
- **dplyr** %>% (R interop)


---

## Autopoietic Marginalia

> **The interaction IS the skill improving itself.**

Every use of this skill is an opportunity for worlding:
- **MEMORY** (-1): Record what was learned
- **REMEMBERING** (0): Connect patterns to other skills  
- **WORLDING** (+1): Evolve the skill based on use



*Add Interaction Exemplars here as the skill is used.*
