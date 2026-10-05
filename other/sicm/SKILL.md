---
name: sicm
description: '- **Generic arithmetic** extensible across numeric types'
metadata:
  interface_ports:
  - References
  - Commands
  - Integration with
trit: 0
---
# SICM Skill - Structure and Interpretation of Classical Mechanics

> *"The variational formulation of mechanics is coordinate-independent and leads to a systematic computational approach."*
> — Sussman & Wisdom

## Overview

**SICMUtils** is a Clojure/ClojureScript implementation of scmutils—the computer algebra system from MIT's SICM course. It provides:

- **Generic arithmetic** extensible across numeric types
- **Symbolic computation** with automatic differentiation  
- **Functional differential geometry** on manifolds
- **Lagrangian/Hamiltonian mechanics** with Noether's theorem

**Trit**: 0 (ERGODIC - Coordinator between SICP abstractions and physical mechanics)

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    sicmutils.env                           │
│           (batteries-included namespace)                   │
└─────────────────────────┬──────────────────────────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼────────┐      ┌─────▼──────┐       ┌──────▼─────┐
│ mechanics/ │      │  calculus/ │       │ numerical/ │
│ Lagrangian │      │  manifold  │       │ integration│
│ Hamiltonian│      │ vector-fld │       │ optimize   │
│ Noether    │      │ form-field │       │ ODE solve  │
└────────────┘      └────────────┘       └────────────┘
        │                 │                    │
        └─────────────────┼────────────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼────────┐      ┌─────▼──────┐       ┌──────▼─────┐
│ simplify/  │      │ operator   │       │ derivative │
│ polynomial │      │ composition│       │ D, partial │
│ rules      │      │ algebra    │       │ dual nums  │
└────────────┘      └────────────┘       └────────────┘
        │                 │                    │
        └─────────────────┼────────────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼────────┐      ┌─────▼──────┐       ┌──────▼─────┐
│  generic   │      │   value    │       │ structure  │
│  +,-,*,/   │      │  protocol  │       │  up/down   │
│  extensible│      │ kind,zero? │       │  vectors   │
└────────────┘      └────────────┘       └────────────┘
```

## Core Namespaces (GF(3) Decomposition)

### MINUS (-1): Verification/Structure

| Namespace | Purpose |
|-----------|---------|
| `sicmutils.value` | Value protocol: `zero?`, `one?`, `kind` |
| `sicmutils.generic` | Generic arithmetic operations |
| `sicmutils.structure` | Up/down tuple vectors |
| `sicmutils.matrix` | Linear algebra |
| `sicmutils.simplify.*` | Expression simplification |

### ERGODIC (0): Coordination/Transformation

| Namespace | Purpose |
|-----------|---------|
| `sicmutils.expression` | Symbolic expression trees |
| `sicmutils.operator` | Operator algebra composition |
| `sicmutils.function` | Higher-order function utilities |
| `sicmutils.calculus.derivative` | D operator, partials |
| `sicmutils.calculus.manifold` | Differentiable manifolds |
| `sicmutils.calculus.coordinate` | Coordinate systems |

### PLUS (+1): Generation/Execution

| Namespace | Purpose |
|-----------|---------|
| `sicmutils.differential` | Dual numbers for AD |
| `sicmutils.abstract.number` | Symbolic numeric literals |
| `sicmutils.abstract.function` | Literal functions |
| `sicmutils.mechanics.lagrange` | Lagrangian mechanics |
| `sicmutils.mechanics.hamilton` | Hamiltonian mechanics |
| `sicmutils.numerical.*` | Numerical integration |

## Key Concepts

### 1. Generic Arithmetic (Extensible Tower)

```clojure
(require '[sicmutils.env :as e])

;; Works on numbers
(e/* 3 4) ;=> 12

;; Works on symbols
(e/* 'x 'y) ;=> (* x y)

;; Works on functions
((e/* e/sin e/cos) 'x) ;=> (* (sin x) (cos x))

;; Extend to custom types via protocols
```

### 2. Automatic Differentiation (D Operator)

```clojure
;; D is the derivative operator
(e/D e/sin)          ;=> cos
((e/D e/sin) 'x)     ;=> (cos x)

;; Higher derivatives
((e/expt e/D 2) e/sin)  ;=> -sin

;; Partial derivatives
((e/partial 0) (fn [[x y]] (e/* x y)))  ; ∂/∂x(xy) = y
```

### 3. Structures (Up/Down Vectors)

```clojure
;; Up = contravariant (coordinate-like)
(e/up 1 2 3)

;; Down = covariant (momentum-like)
(e/down 1 2 3)

;; Lagrangian state: (t, q, q̇)
(e/up 't (e/up 'x 'y) (e/up 'vx 'vy))

;; Hamiltonian state: (t, q, p)
(e/up 't (e/up 'x 'y) (e/down 'px 'py))
```

### 4. Lagrangian Mechanics

```clojure
(require '[sicmutils.mechanics.lagrange :as L])

;; Free particle Lagrangian: L = T - V = ½mv²
(defn L-free-particle [mass]
  (fn [[_ _ v]]
    (e/* (e// 1 2) mass (e/square v))))

;; Euler-Lagrange equations
(L/Lagrange-equations (L-free-particle 'm))

;; Action functional
(L/Lagrangian-action L q t1 t2)
```

### 5. Manifolds and Differential Geometry

```clojure
(require '[sicmutils.calculus.manifold :as m])
(require '[sicmutils.calculus.coordinate :as c])

;; Define R² with rectangular coordinates
(def R2 (m/make-manifold m/Rn 2))
(def rect (c/coordinate-system-at 'rectangular :origin R2))

;; Vector fields
(def d:dx (c/vector-field rect 0))
(def d:dy (c/vector-field rect 1))

;; Differential forms
(def dx (c/oneform-field rect 0))
(def dy (c/oneform-field rect 1))

;; Lie derivative, exterior derivative, etc.
```

### 6. Simplification

```clojure
(require '[sicmutils.simplify :as s])

;; Simplify expressions
(s/simplify (e/+ (e/square (e/sin 'x)) 
                  (e/square (e/cos 'x))))
;=> 1

;; Render to LaTeX
(e/->TeX (e/simplify expr))

;; Render to infix
(e/->infix (e/simplify expr))
```

## SICP → SICM Bridge

The progression from SICP to SICM:

| SICP Chapter | SICM Connection |
|--------------|-----------------|
| Ch 1: Procedures | Generic operations, function composition |
| Ch 2: Data abstraction | Structures, symbolic expressions |
| Ch 3: Assignment & state | Lagrangian/Hamiltonian state |
| Ch 4: Metalinguistic | Expression simplifier, rule system |
| Ch 5: Register machines | Numerical integrators |

### Shared Patterns

```scheme
;; SICP: deriv procedure
(define (deriv exp var) ...)

;; SICM: D operator on symbolic expressions
((D (literal-function 'f)) 'x)
```

## Incremental Update Schema

For semantic world closure with incremental updates:

```clojure
(def sicm-acset-schema
  {:objects [:Namespace :Symbol :Expression :Operator]
   :morphisms {:depends [:Namespace :Namespace]
               :defines [:Namespace :Symbol]
               :uses [:Expression :Symbol]
               :applies [:Operator :Expression]}
   :attributes {:trit [:Namespace :GF3]
                :kind [:Symbol :Keyword]
                :arity [:Operator :Int]}})

;; Incremental update: only recompute changed subgraph
(defn incremental-update [delta-expr sicm-graph]
  (let [affected (transitive-deps delta-expr sicm-graph)
        unchanged (set/difference (all-nodes sicm-graph) affected)]
    (-> sicm-graph
        (invalidate-nodes affected)
        (recompute-nodes affected)
        (verify-gf3-conservation))))
```

## World Closure

SICM completes the semantic world by bridging:

```
SICP (abstraction)  ←→  SICM (mechanics)  ←→  FDG (geometry)
     λ-calculus              variational         manifolds
     procedures              Lagrangians         vector fields
     data abstraction        state tuples        differential forms
     interpreters            simplifiers         coordinate systems
```

---

## End-of-Skill Interface

## Commands

```bash
# Add dependency
clj -Sdeps '{:deps {sicmutils/sicmutils {:mvn/version "0.23.0"}}}'

# REPL with SICMUtils
clj -M -e "(require '[sicmutils.env :refer :all])"

# ClojureScript (browser/Node)
shadow-cljs watch sicm-app

# With Babashka (limited - no symbolic)
bb -e "(require '[sicmutils.value :as v]) (v/zero? 0)"
```

## Integration with Gay.jl / GF(3)

### Namespace → Trit Mapping

```clojure
;; Use Gay.jl colors to track namespace triads
(def namespace-trits
  {"sicmutils.value"       -1  ; foundation
   "sicmutils.generic"     -1  ; arithmetic
   "sicmutils.structure"   -1  ; data
   "sicmutils.operator"     0  ; coordination
   "sicmutils.expression"   0  ; symbolic
   "sicmutils.derivative"   0  ; calculus bridge
   "sicmutils.lagrange"    +1  ; mechanics
   "sicmutils.hamilton"    +1  ; dynamics
   "sicmutils.numerical"   +1  ; execution
   })

;; GF(3) conserved per layer:
;; 3×(-1) + 3×(0) + 3×(+1) = 0 ✓
```

### Color Coding for Expressions

```clojure
;; Map expression types to Gay.jl palette
(defn expr-color [expr seed]
  (let [kind (value/kind expr)
        idx (case kind
              ::number 1
              ::symbol 2
              ::structure 3
              ::operator 4
              ::function 5
              6)]
    (gay/color-at seed idx)))
```

## References

- [SICM Book](https://mitpress.mit.edu/sites/default/files/sicm/book.html) (Sussman & Wisdom)
- [SICMUtils GitHub](https://github.com/sicmutils/sicmutils)
- [Emmy (successor)](https://github.com/mentat-collective/emmy)
- [FDG Book](https://mitpress.mit.edu/9780262019347/) (Functional Differential Geometry)
- [cljdoc Reference](https://cljdoc.org/d/sicmutils/sicmutils)

---

**Skill**: sicm  
**Trit**: 0 (ERGODIC - bridges SICP abstraction to physical mechanics)  
**GF(3) Triad**: `sicp (-1) ⊗ sicm (0) ⊗ fdg (+1) = 0`  
**Status**: Ready for incremental semantic updates


---

## Autopoietic Marginalia

> **The interaction IS the skill improving itself.**

Every use of this skill is an opportunity for worlding:
- **MEMORY** (-1): Record what was learned
- **REMEMBERING** (0): Connect patterns to other skills  
- **WORLDING** (+1): Evolve the skill based on use



*Add Interaction Exemplars here as the skill is used.*


## REPL siblings

Julia family: `sicmutils` · `sicp` · `julia-scientific` · `julia-gay` · `julia-gpu-kernels` · `julia-tempering` · `quarto-julia`. Atlas: `repl-commons`.
