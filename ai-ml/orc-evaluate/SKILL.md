---
name: orc-evaluate
description: Set up LLM-as-judge evaluation for ORC workflows
---

# ORC Evaluation (LLM-as-Judge)

Set up automated quality evaluation for ORC workflow outputs. Read `docs/EVALUATION-COMPONENT.md` for the full reference.

## Require

```clojure
(require '[ai.obney.orc.evaluation.interface :as eval])
```

## Overview

The evaluation component provides LLM-as-judge scoring:
- **Grounding** — Is the output faithful to the input?
- **Instruction-following** — Does the output follow the instruction?
- **Reasoning** — Is the reasoning sound?
- **Completeness** — Does the output address all aspects?

Each judge returns a score (0.0-1.0) with structured feedback.

## Built-in Judges

### Evaluate one trace
```clojure
(eval/evaluate-trace
  {:instruction "Summarize the article covering all main points"
   :inputs {:article "Long article text..."}
   :outputs {:summary "Short summary..."}}
  {:judges [:grounding :completeness]})
;; => ScoreWithFeedback with :score, :feedback, :dimensions, and—when
;;    model-backed—durable :model-provenance on the recorded score event
```

## Workflow Judges (DSL Integration)

Attach judges to workflow nodes for automatic scoring during execution:

```clojure
(orc/workflow "evaluated-pipeline"
  (orc/blackboard {:question :string :answer :string})

  ;; Define judge configurations
  (orc/judges
    {:grounding    {:type :grounding :weight 0.5}
     :completeness {:type :completeness :weight 0.5}})

  ;; Attach judges to a node
  (orc/llm "answer"
    :instruction "Answer the question thoroughly."
    :reads [:question]
    :writes [:answer]
    :judges [:grounding :completeness]))
```

When executed with tracing enabled, each judged node produces evaluation scores in the trace.

## Batch Evaluation

Evaluate a workflow across multiple test cases:

```clojure
(eval/evaluate-traces
  [{:instruction "Answer the question"
    :inputs {:question "What is AI?"}
    :outputs {:answer "Artificial intelligence..."}}
   {:instruction "Answer the question"
    :inputs {:question "What is ML?"}
    :outputs {:answer "Machine learning..."}}]
  {:judges [:grounding :completeness]})
;; => {:avg-score 0.82 :results [...] :min-score ... :max-score ...}
```

## GEPA Integration

Evaluation judges feed directly into GEPA optimization. When GEPA proposes instruction candidates, judges score them — the scores drive Pareto selection.

```clojure
;; GEPA uses judges automatically when configured
(gepa/optimize! ctx
  {:sheet-id sheet-id
   :node-name "answer"
   :judges {:grounding 0.5 :completeness 0.5}
   ...})
```

## Reference
- `docs/EVALUATION-COMPONENT.md` — Full evaluation guide
- `docs/SELF-IMPROVING-LOOP.md` — Evaluation and continuous improvement
- `docs/GEPA-GUIDE.md` — How judges integrate with optimization
