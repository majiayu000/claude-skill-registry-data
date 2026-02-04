---
name: clojure
description: Clojure ecosystem = babashka + clj + lein + shadow-cljs.
version: 1.0.0
---


# clojure

Clojure ecosystem = babashka + clj + lein + shadow-cljs.

## Atomic Skills

| Skill | Startup | Domain |
|-------|---------|--------|
| babashka | 10ms | Scripting |
| clj | 2s | JVM REPL |
| lein | 3s | Build tool |
| shadow-cljs | 5s | ClojureScript |

## Quick Start

```bash
# Scripting (fast)
bb -e '(+ 1 2 3)'

# JVM (full)
clj -M -m myapp.core

# Web (ClojureScript)
npx shadow-cljs watch app
```

## deps.edn

```clojure
{:deps {org.clojure/clojure {:mvn/version "1.12.0"}}
 :aliases {:dev {:extra-paths ["dev"]}
           :test {:extra-deps {lambdaisland/kaocha {:mvn/version "1.0"}}}}}
```

## bb.edn

```clojure
{:tasks {:build (shell "clj -T:build uber")
         :test (shell "clj -M:test")
         :repl (clojure "-M:dev -m nrepl.cmdline")}}
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
clojure (−) + SDF.Ch1 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
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