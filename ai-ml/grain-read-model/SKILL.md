---
name: grain-read-model
description: Build read models by reducing events into queryable state
---

# Grain Read Model Pattern

## Required Imports

```clojure
(ns my.service.core.read-models
  (:require [ai.obney.grain.event-store-v3.interface :as event-store]))
```

## Event Type Sets

Define which events affect each read model:

```clojure
(def contact-events
  #{:crm/contact-created
    :crm/contact-updated
    :crm/contact-field-set
    :crm/contact-archived
    :crm/contact-deleted})

(def relationship-events
  #{:crm/relationship-created
    :crm/relationship-updated
    :crm/relationship-ended})
```

## Projection Multimethod

```clojure
;; Dispatch on event type
(defmulti contacts*
  (fn [_state event] (:event/type event)))

;; Handle creation
(defmethod contacts* :crm/contact-created
  [state event]
  (assoc state (:contact-id event)
         {:id (:contact-id event)
          :type-slug (:type-slug event)
          :display-name (:display-name event)
          :field-values (:field-values event)
          :status :active
          :created-at (str (:event/timestamp event))}))

;; Handle update
(defmethod contacts* :crm/contact-updated
  [state event]
  (-> state
      (update (:contact-id event) merge (:changes event))
      (assoc-in [(:contact-id event) :updated-at] (str (:event/timestamp event)))))

;; Handle field set
(defmethod contacts* :crm/contact-field-set
  [state event]
  (-> state
      (assoc-in [(:contact-id event) :field-values (keyword (:field-slug event))]
                (:new-value event))
      (assoc-in [(:contact-id event) :updated-at] (str (:event/timestamp event)))))

;; Handle archive
(defmethod contacts* :crm/contact-archived
  [state event]
  (assoc-in state [(:contact-id event) :status] :archived))

;; Default: ignore unknown events
(defmethod contacts* :default [state _] state)

;; Reduction function
(defn contacts
  "Build contacts read model from events"
  [initial-state events]
  (reduce contacts* initial-state events))
```

## Query Helper Functions

### Get Single Entity

```clojure
(defn get-contact
  "Get a single contact by ID"
  [event-store contact-id]
  (let [events (event-store/read event-store
                                 {:types contact-events
                                  :tags #{[:contact contact-id]}})]
    (get (contacts {} events) contact-id)))
```

### Get All Entities

```clojure
(defn get-contacts-all
  "Get all contacts"
  [event-store]
  (let [events (event-store/read event-store {:types contact-events})]
    (vals (contacts {} events))))
```

### Get by Filter

```clojure
(defn get-contacts-by-type
  "Get contacts of a specific type"
  [event-store type-slug]
  (let [events (event-store/read event-store {:types contact-events})]
    (->> (contacts {} events)
         vals
         (filter #(= type-slug (:type-slug %))))))
```

### Batch Loading

```clojure
(defn get-contacts-batch
  "Get multiple contacts by IDs in a single read"
  [event-store contact-ids]
  (when (seq contact-ids)
    (let [tags (set (map #(vector :contact %) contact-ids))
          events (event-store/read event-store
                                   {:types contact-events
                                    :tags tags})]
      (contacts {} events))))
```

### Composing Projections

```clojure
(defn get-contact-with-attribution
  "Get contact with attribution in single query"
  [event-store contact-id]
  (let [events (event-store/read event-store
                                 {:types (into contact-events attribution-events)
                                  :tags #{[:contact contact-id]}})
        contact (get (contacts {} events) contact-id)
        attr (get (attributions {} events) contact-id)]
    (cond-> contact
      attr (assoc :attribution attr))))
```

## Event Store Read Options

```clojure
;; By event types
{:types #{:crm/contact-created :crm/contact-updated}}

;; By tags (entities)
{:tags #{[:contact contact-id]}}

;; After specific event (for incremental updates)
{:types #{:crm/contact-field-set}
 :after last-processed-event-id}

;; Combined
{:types contact-events
 :tags #{[:contact contact-id]}
 :after last-event-id}
```

## Conventions

- State is a map keyed by entity ID: `{uuid1 {...} uuid2 {...}}`
- Use `assoc` for create, `update`/`assoc-in` for modify
- Always provide `:default` method to ignore unknown events
- Query helpers read events then reduce to current state
- Use tags for efficient filtering (avoid reading all events)
- Batch load related data to avoid N+1 queries

## Reference Files

- `components/user-service/src/ai/obney/workshop/user_service/core/read_models.clj` - User projections
- `components/crm-service/src/ai/obney/workshop/crm_service/core/read_models.clj` - CRM projections
