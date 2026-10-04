---
name: orc-optimize
description: Set up GEPA prompt optimization for an ORC workflow
---

# GEPA Prompt Optimization

Optimize LLM instructions in an ORC workflow using GEPA (Genetic-Pareto Prompt Optimizer). Read `docs/GEPA-GUIDE.md` for the full reference.

## Require

```clojure
(require '[ai.obney.orc.gepa.interface :as gepa])
```

## Overview

GEPA improves LLM node instructions through:
1. **Reflective mutation** — LLM analyzes failures and proposes better instructions
2. **Pareto selection** — Maintains diversity by tracking per-example best candidates
3. **Iterative generations** — Each generation proposes and evaluates instruction variants

## Setup

### 1. Define Metrics

Metrics score how well a candidate instruction performs on each training example.

```clojure
;; Exact match (binary: 0 or 1)
(gepa/make-exact-match-metric "answer")

;; Contains check
(gepa/make-contains-metric "answer")

;; Judge-based (LLM evaluates quality)
(gepa/make-judge-metric
  {:grounding 0.35
   :completeness 0.25
   :instruction-following 0.25
   :reasoning 0.15})
```

### 2. Define Training Examples

```clojure
(def examples
  [{"question" "What is 2+2?" "expected-answer" "4"}
   {"question" "Capital of France?" "expected-answer" "Paris"}
   {"question" "Largest ocean?" "expected-answer" "Pacific"}])
```

### 3. Start Optimization

```clojure
(gepa/optimize! ctx
  {:sheet-id sheet-id
   :node-name "answer-node"          ;; which LLM node to optimize
   :trainset examples
   :valset examples
   :metric-fn (gepa/make-exact-match-metric "answer")
   :config {:max-metric-calls 30}
   :block? false})
```

### 4. Check Results

```clojure
;; Get the best candidate
(gepa/get-best-candidate ctx optimization-id)

;; Get the Pareto frontier
(gepa/get-pareto-frontier ctx optimization-id)

;; Get optimization progress
(gepa/get-progress ctx optimization-id)
```

If the process stops during an optimization, reconstruct the same Grain context
and advance one durable missing transition at a time:

```clojure
(gepa/resume! ctx optimization-id)
;; => {:status :resumed :boundary ...}
;; or {:status :already-terminal ...}
```

### 5. Apply and Publish the Winner

```clojure
;; The exact immutable source version is mandatory.
(gepa/apply-winner! ctx optimization-id 3)
;; => {:source-version 3 :target-version 4
;;     :source-fingerprint ... :target-fingerprint ...}
```

Optimization never silently mutates a published workflow. Applying a completed
winner updates the draft and publishes a new immutable version with source and
target fingerprints.

## Key Concepts

- **Candidate** — An instruction variant with scores per training example
- **Pareto frontier** — Set of non-dominated candidates (no single candidate beats another on all examples)
- **Generation** — One round of propose → evaluate → select
- **Budget** — Controls how many generations and candidates per generation

## Reference
- `docs/GEPA-GUIDE.md` — Full GEPA integration guide
- `docs/SELF-IMPROVING-LOOP.md` — How evaluation feeds continuous improvement
