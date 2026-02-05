---
name: babashka-clj
description: Babashka scripting for fast Clojure execution. JVM-less scripting with GraalVM native compilation and sci interpreter.
version: 1.0.0
---


# Babashka Clojure Skill

**Trit**: 0 (ERGODIC - scripting mediates between REPL and production)  
**Foundation**: Babashka + sci interpreter + pods  

## Core Concept

Babashka provides instant Clojure scripting without JVM startup:
- Native binary via GraalVM
- Compatible with most clojure.core
- Pods for extending functionality

## Commands

```bash
# Run script
bb script.clj

# REPL
bb nrepl-server

# Tasks
bb tasks
bb run <task>
```

## GF(3) Integration

```clojure
(require '[babashka.process :refer [shell]])

;; Color from seed
(defn gay-color [seed idx]
  (let [h (mod (* seed idx 0x9E3779B97F4A7C15) 360)]
    {:hue h :trit (cond (< h 120) 1 (< h 240) 0 :else -1)}))
```

## Canonical Triads

```
borkdude (-1) ⊗ babashka-clj (0) ⊗ gay-mcp (+1) = 0 ✓
cider-clojure (-1) ⊗ babashka-clj (0) ⊗ squint-runtime (+1) = 0 ✓
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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