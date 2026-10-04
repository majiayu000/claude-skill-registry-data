---
name: orc-workflow
description: Build an ORC behavior tree workflow using the DSL
---

# Build an ORC Workflow

Build a behavior tree workflow using the ORC DSL. Read `docs/DSL-REFERENCE.md` for the full reference.

## Require

```clojure
(require '[ai.obney.orc.orc-service.interface :as orc])
```

## Structure

Every workflow has three parts:

```clojure
(orc/workflow "workflow-name"
  ;; 1. Blackboard (input/output schema)
  (orc/blackboard {:input-key :string
                   :output-key :string})

  ;; 2. Root node (tree structure)
  (orc/sequence "main"
    (orc/llm "step-1" ...)
    (orc/code "step-2" ...)))
```

## Node Types

### LLM Node (call an LLM)
```clojure
(orc/llm "summarize"
  :instruction "Summarize the input text in 2 sentences."
  :reads [:input-text]
  :writes [:summary]
  :model "google/gemini-2.0-flash-001")  ;; optional, uses default if omitted
```

### Code Node (execute a Clojure function)
```clojure
;; :fn must be a fully-qualified function name (resolved at runtime)
;; The function receives {:keys [inputs]} and returns {:key value}
(orc/code "transform"
  :fn "my.ns/transform-fn"
  :reads [:raw-data]
  :writes [:processed-data])
```

### Sequence (run children in order, fail on first failure)
```clojure
(orc/sequence "pipeline"
  (orc/llm "extract" ...)
  (orc/code "validate" ...)
  (orc/llm "respond" ...))
```

### Fallback (try alternatives until one succeeds)
```clojure
(orc/fallback "with-retry"
  (orc/llm "try-gpt4" :model "openai/gpt-4o" ...)
  (orc/llm "try-gemini" :model "google/gemini-2.0-flash-001" ...))
```

### Parallel (run children concurrently)
```clojure
(orc/parallel "gather"
  {:success-policy :all}  ;; :all, :any, or :majority
  (orc/llm "analysis-a" ...)
  (orc/llm "analysis-b" ...))
```

### Map-Each (iterate over a collection)
```clojure
(orc/map-each "process-items"
  :source-key :items         ;; blackboard key with the collection
  :item-key :current-item   ;; blackboard key for each item
  :output-key :results      ;; blackboard key for collected results
  (orc/llm "process-one" ...))
```

### Condition (branch on a predicate)
```clojure
(orc/condition "check-length"
  :check "(fn [bb] (> (count (:text bb)) 100))"
  :reads [:text])
```

### LLM Condition (branch on LLM yes/no)
```clojure
(orc/llm-condition "is-relevant?"
  :instruction "Is this text relevant to the user's question? Answer yes or no."
  :reads [:text :question])
```

## Build and Execute

```clojure
;; Build (stores in event store, returns sheet-id)
(def sheet-id (orc/build-workflow! ctx my-workflow))

;; Execute (blocking, returns result)
(orc/execute ctx sheet-id {:input-key "value"})
;; => {:status :success, :outputs {:output-key "result"}, :duration-ms 1234}

;; Execute with options
(orc/execute ctx sheet-id inputs :timeout-ms 60000)
(orc/execute ctx sheet-id inputs :use-version 2)
```

After a processor restart against the same durable event store, recover
abandoned execution frontiers without creating replacement ticks:

```clojure
(orc/resume-in-progress! ctx)
```

The recovery call is idempotent and preserves tick, sheet, node, and task-call
identity. It is distinct from reconnecting a live stream, which does not replay
history.

## Key Rules

- All node `:reads` and `:writes` must be declared in the blackboard
- Blackboard keys are keywords throughout (schema, reads/writes, execute inputs/outputs)
- Code node `:fn` must be a namespace-qualified symbol string, not inline code
- `build-workflow!` is idempotent — same workflow name produces the same sheet-id, and unchanged definitions are a true no-op (zero events) via content hashing
- Workflows are versioned — use `orc/publish-version` for production snapshots
- Keep observability failure-isolated with `orc/start-telemetry-exporter!`; inspect
  retry/drop counters with `orc/telemetry-exporter-stats` and stop it explicitly

## Judges (optional quality gates)

```clojure
(orc/workflow "with-judges"
  (orc/blackboard {:question :string :answer :string})
  (orc/judges
    {:grounding {:type :grounding :weight 0.5}
     :completeness {:type :completeness :weight 0.5}})
  (orc/llm "answer"
    :instruction "Answer the question."
    :reads [:question]
    :writes [:answer]
    :judges [:grounding :completeness]))
```

## Reference
- `docs/DSL-REFERENCE.md` — Full DSL reference with examples
- `docs/ORC-SERVICE-GUIDE.md` — Execution engine internals
