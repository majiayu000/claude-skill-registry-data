---
name: grain-command-handler
description: Implement command handlers that validate state and emit events using the Grain framework
---

# Grain Command Handler Pattern

## Required Imports

```clojure
(ns my.service.core.commands
  (:require [ai.obney.grain.event-store-v3.interface :refer [->event]]
            [ai.obney.grain.command-processor-v2.interface :refer [defcommand]]
            [ai.obney.grain.command-processor-v2.interface :as cp]
            [ai.obney.grain.time.interface :as time]
            [my.service.core.read-models :as rm]
            [cognitect.anomalies :as anom]))
```

## Command Template

```clojure
(defcommand :service command-name
  "Docstring describing what the command does."
  [{{:keys [entity-id field1 field2]} :command
    :as ctx}]

  ;; 1. Read current state from read models (pass ctx, NOT bare event-store)
  (let [entity (rm/get-entity ctx entity-id)]
    (cond
      ;; Return anomaly for validation failures
      (not entity)
      {::anom/category ::anom/not-found
       ::anom/message "Entity not found"}

      (not (:active entity))
      {::anom/category ::anom/conflict
       ::anom/message "Cannot modify inactive entity"}

      ;; Success: return events
      :else
      {:command-result/events
       [(->event
         {:type :service/entity-updated
          :tags #{[:entity entity-id]}
          :body {:entity-id entity-id
                 :field1 field1
                 :field2 field2
                 :modified-at (str (time/now))}})]})))
```

## Key Variations

### Success with Events Only

```clojure
{:command-result/events
 [(->event {:type :service/thing-created
            :tags #{[:thing thing-id]}
            :body {:thing-id thing-id :name name}})]}
```

### Anomaly Return (Error)

```clojure
{::anom/category ::anom/conflict
 ::anom/message "Name already taken."}
```

### CAS (Optimistic Concurrency)

Prevents races by checking state hasn't changed between read and write:

```clojure
{:command-result/events [...]
 :command-result/cas {:types thing-event-types
                      :predicate-fn (fn [_events]
                                      (= :active (:status (rm/get-thing ctx id))))}}
```

### Calling Other Commands

```clojure
(let [result (cp/process-command
              (assoc ctx :command {:command/id (random-uuid)
                                   :command/timestamp (time/now)
                                   :command/name :other/command-name
                                   :field1 value1}))]
  ;; result is either anomaly or {:command-result/events [...]}
  result)
```

## Common Anomaly Categories

- `::anom/not-found` -- resource does not exist
- `::anom/conflict` -- business rule violation (duplicate, invalid state)
- `::anom/incorrect` -- bad input data
- `::anom/forbidden` -- not authorized for this action

## Conventions

- Commands modify state by emitting events; never write to a database directly
- Always validate via read models before emitting events
- Read model helpers take `ctx` (the full context), not bare `event-store`
- Tag events with `#{[:entity entity-id]}` for efficient filtered reads
- Return anomalies for all error cases
- Include `modified-at` in event bodies when relevant

## Reference Files

- `components/orc-service/src/ai/obney/orc/orc_service/core/commands.clj` -- ORC sheet commands
- `components/colbert/src/ai/obney/orc/colbert/core/commands.clj` -- ColBERT commands
- `components/ontology/src/ai/obney/orc/ontology/core/commands.clj` -- Ontology commands
