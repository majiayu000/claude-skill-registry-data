---
name: grain-query-handler
description: Implement query handlers that read from event-sourced read models
---

# Grain Query Handler Pattern

## Required Imports

```clojure
(ns my.service.core.queries
  (:require [ai.obney.grain.event-store-v3.interface :as es]
            [ai.obney.grain.query-processor.interface :refer [defquery]]
            [my.service.interface.read-models :as rm]
            [cognitect.anomalies :as anom]))
```

## Query Template

```clojure
(defquery :namespace query-name
  "Docstring describing what the query returns."
  [{{:keys [entity-id filter-param]} :query
    :keys [event-store other-dependency]}]

  (let [entity (rm/get-entity event-store entity-id)]
    (if entity
      {:query/result {:entity entity}}
      {::anom/category ::anom/not-found
       ::anom/message "Entity not found"})))
```

## Return Patterns

### Success
```clojure
{:query/result {:entity data
                :related-data more-data}}
```

### Error
```clojure
{::anom/category ::anom/not-found
 ::anom/message "Human readable message"}
```

## Fat Query Pattern (Screen Queries)

Load all data needed for a UI screen in one query:

```clojure
(defquery :advisor meetings-screen
  "Fat query for meetings screen - returns all data needed."
  [{{:keys [student-id]} :query
    :keys [event-store]}]

  (let [;; Get primary entity
        student (rm/get-student event-store student-id)
        ;; Get related data
        meetings (rm/get-meetings-for-student event-store student-id)
        ;; Get metadata/options
        meeting-types (rm/get-meeting-types event-store)]

    (if student
      {:query/result {:student student
                      :meetings meetings
                      :meeting-types meeting-types}}
      {::anom/category ::anom/not-found
       ::anom/message "Student not found"})))
```

## List Query with Pagination

```clojure
(defquery :crm list-contacts
  "List contacts with optional filters and pagination."
  [{{:keys [type-slug status limit offset]} :query
    :keys [event-store]}]

  (let [;; Get all matching contacts
        all-contacts (cond->> (rm/get-contacts-all event-store)
                       type-slug (filter #(= type-slug (:type-slug %)))
                       status (filter #(= status (:status %))))
        total (count all-contacts)
        ;; Apply pagination
        paginated (cond->> all-contacts
                    offset (drop offset)
                    limit (take limit))]

    {:query/result {:contacts (vec paginated)
                    :total total}}))
```

## Batch Loading Pattern

Pre-load related data to avoid N+1 queries:

```clojure
(defquery :crm list-contacts-with-types
  [{{:keys [type-slug]} :query
    :keys [event-store]}]

  (let [;; Pre-load all contact types (1 query instead of N)
        types-by-id (rm/get-contact-types-by-id event-store)
        ;; Get contacts
        contacts (rm/get-contacts-by-type event-store type-slug)
        ;; Enrich with type data
        enriched (mapv #(assoc % :contact-type (get types-by-id (:type-id %)))
                       contacts)]

    {:query/result {:contacts enriched}}))
```

## Composing Read Models

```clojure
(defquery :crm get-contact
  "Get contact with attribution in single query."
  [{{:keys [contact-id]} :query
    :keys [event-store]}]

  (let [contact (rm/get-contact event-store contact-id)]
    (if contact
      (let [;; Get related data
            relationships (rm/get-relationships-for-contact event-store contact-id)
            attribution (rm/get-attribution event-store contact-id)]
        {:query/result {:contact (cond-> contact
                                   attribution (assoc :attribution attribution)
                                   (seq relationships) (assoc :relationships relationships))}})
      {::anom/category ::anom/not-found
       ::anom/message "Contact not found"})))
```

## Conventions

- Queries are read-only (never emit events)
- Use read models to get current state
- Return `{:query/result {...}}` for success
- Return anomalies for not-found and errors
- Use fat queries for screen data (reduces round trips)
- Batch load related data to avoid N+1 queries
- Include pagination metadata (`:total`) for list queries

## Reference Files

- `components/crm-service/src/ai/obney/workshop/crm_service/core/queries.clj` - CRM queries with batch loading
