---
name: grain-todo-processor
description: Implement event-driven side effects that react to domain events
---

# Grain Todo Processor Pattern

Todo processors are policies that react to domain events and emit follow-up events or perform side effects.

## Required Imports

```clojure
(ns ai.obney.orc.my-service.core.todo-processors
  (:require [ai.obney.orc.my-service.core.read-models :as rm]
            [ai.obney.grain.event-store-v3.interface :refer [->event]]
            [ai.obney.grain.todo-processor-v2.interface :refer [defprocessor]]
            [ai.obney.grain.time.interface :as time]))
```

## Processor Template

```clojure
(defprocessor :ns processor-name
  {:topics #{:ns/triggering-event}}
  "Docstring explaining what this processor does and when."
  [context]
  (let [event (:event context)
        entity-id (:entity-id event)
        ;; Check current state using read models
        entity (rm/get-entity context entity-id)]
    (if (should-take-action? entity)
      ;; Emit follow-up events
      {:result/events
       [(->event
         {:type :ns/follow-up-action
          :tags #{[:entity entity-id]}
          :body {:entity-id entity-id
                 :triggered-by (:event/type event)
                 :processed-at (str (time/now))}})]}
      ;; No action needed
      {})))
```

The generated var name is `ns-processor-name` (e.g., `(defprocessor :crm ensure-attribution ...)` creates var `crm-ensure-attribution`).

## Return Patterns

### Emit Events (pure -- batch checkpointed)
```clojure
{:result/events [event1 event2]}
```

### Side Effect with Checkpoint Control
```clojure
{:result/effect (fn [] (send-email! ...))
 :result/checkpoint :after}  ;; or :before
```

### No Action
```clojure
{}
```

## Auto-Registration

`defprocessor` registers the processor in a global registry automatically. There is no manual registry map (`def todo-processors`) needed. The control plane discovers processors from the registry and starts them when a tenant is assigned to the node.

**Interface.clj** only needs a bare side-effect require to load the namespace:

```clojure
(ns ai.obney.orc.my-service.interface
  (:require ;; Side-effect requires
            [ai.obney.orc.my-service.core.commands]
            [ai.obney.orc.my-service.core.queries]
            [ai.obney.orc.my-service.core.todo-processors]  ;; bare require, no alias
            ...))

;; No todo-processors re-export needed
```

No manual wiring is needed -- the control plane discovers processors from the global registry.

## Common Use Cases

### Ensure Default Value

```clojure
(defprocessor :crm ensure-attribution
  {:topics #{:crm/contact-created}}
  "Record default attribution if none exists."
  [context]
  (let [{:keys [contact-id]} (:event context)
        existing (rm/get-contact context contact-id)]
    (if (:attribution existing)
      {}  ;; Already has attribution
      {:result/events
       [(->event
         {:type :crm/attribution-recorded
          :tags #{[:contact contact-id]}
          :body {:contact-id contact-id
                 :attribution {:source :manual_entry
                               :recorded-at (str (time/now))}}})]})))
```

### Duplicate Detection

```clojure
(defprocessor :crm check-for-duplicates
  {:topics #{:crm/contact-created}}
  "Check for duplicates when contact is created."
  [context]
  (let [{:keys [contact-id]} (:event context)
        email (normalize-email (get-in (:event context) [:field-values :email]))
        existing (rm/get-contacts-by-email context email)]
    (if (seq (remove #(= contact-id (:id %)) existing))
      {:result/events
       [(->event
         {:type :crm/duplicate-detected
          :tags #{[:contact contact-id]}
          :body {:contact-id contact-id
                 :match-type :email
                 :match-value email}})]}
      {})))
```

### Cascade Operations

```clojure
(defprocessor :crm end-relationships-on-archive
  {:topics #{:crm/contact-archived}}
  "End all relationships when contact is archived."
  [context]
  (let [{:keys [contact-id]} (:event context)
        rels (rm/get-relationships-for-contact context contact-id)
        active-rels (filter #(nil? (:end-date %)) rels)]
    (if (seq active-rels)
      {:result/events
       (mapv (fn [rel]
               (->event
                {:type :crm/relationship-ended
                 :tags #{[:relationship (:id rel)]}
                 :body {:relationship-id (:id rel)
                        :end-date (str (java.time.LocalDate/now))
                        :reason "Contact archived"}}))
             active-rels)}
      {})))
```

### Transform Source Data

```clojure
(defprocessor :crm record-lead-attribution
  {:topics #{:crm/lead-captured}}
  "Map lead form type to attribution source."
  [context]
  (let [{:keys [contact-id form-type form-id]} (:event context)
        source (case form-type
                 :application :application_form
                 :intake :intake_form
                 :interest :interest_form
                 :manual_entry)]
    {:result/events
     [(->event
       {:type :crm/attribution-recorded
        :tags #{[:contact contact-id]}
        :body {:contact-id contact-id
               :attribution {:source source
                             :form-id form-id}}})]}))
```

## Conventions

- Processors receive a context map with `:event`, `:event-store`, `:tenant-id`
- Use read models to check current state before acting
- Return `{:result/events [...]}` or `{}` (empty map)
- One processor can listen to multiple topics via the `:topics` set
- Multiple processors can listen to the same topic
- Normalize data before comparison (email lowercase, phone digits only)
- Include reason/context in generated events for audit trail

## Reference Files

- `components/user-service/src/ai/obney/workshop/user_service/core/todo_processors.clj` - Email notifications
- `components/crm-service/src/ai/obney/workshop/crm_service/core/todo_processors.clj` - Attribution & duplicates
