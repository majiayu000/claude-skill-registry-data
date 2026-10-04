---
name: grain-schema
description: Define Malli schemas for commands, events, and queries using defschemas
---

# Grain Schema Pattern

## Required Imports

```clojure
(ns my.service.interface.schemas
  (:require [ai.obney.grain.schema-util.interface :refer [defschemas]]))
```

## Schema Registration

Use `defschemas` to register named Malli schemas:

```clojure
(defschemas schema-group-name
  {:schema-key schema-definition
   :another-key another-definition})
```

## Command Schemas

Naming: `:namespace/action` (verb form)

```clojure
(defschemas commands
  {;; Create command
   :crm/create-contact
   [:map
    [:type-slug :string]
    [:field-values [:map-of :keyword :any]]
    [:contact-id {:optional true} :uuid]
    [:tags {:optional true} [:set :string]]]

   ;; Update command
   :crm/update-contact
   [:map
    [:contact-id :uuid]
    [:changes [:map-of :keyword :any]]]

   ;; Action command
   :advisor/start-meeting
   [:map
    [:student-id :uuid]
    [:meeting-type [:enum :intake-interview :freeform]]]})
```

## Event Schemas

Naming: `:namespace/entity-past-tense` (what happened)

```clojure
(defschemas events
  {;; Created event
   :crm/contact-created
   [:map
    [:contact-id :uuid]
    [:type-id :uuid]
    [:type-slug :string]
    [:display-name :string]
    [:field-values [:map-of :keyword :any]]
    [:tags [:set :string]]]

   ;; Updated event
   :crm/contact-updated
   [:map
    [:contact-id :uuid]
    [:changes [:map-of :keyword :any]]]

   ;; Action completed event
   :advisor/meeting-started
   [:map
    [:meeting-id :uuid]
    [:student-id :uuid]
    [:meeting-type [:enum :intake-interview :freeform]]
    [:started-at :string]]})
```

## Query Schemas

Naming: `:namespace/query-name` (what to get)

```clojure
(defschemas queries
  {:crm/get-contact
   [:map
    [:contact-id :uuid]]

   :crm/list-contacts
   [:map
    [:type-slug {:optional true} :string]
    [:status {:optional true} [:enum :active :inactive :archived]]
    [:limit {:optional true} :int]
    [:offset {:optional true} :int]]

   :advisor/meetings-screen
   [:map
    [:student-id :uuid]]})
```

## Common Malli Types

```clojure
:string                              ;; String
:int                                 ;; Integer
:double                              ;; Float
:boolean                             ;; Boolean
:uuid                                ;; UUID
:keyword                             ;; Keyword
:any                                 ;; Any value

[:enum :a :b :c]                     ;; Enum
[:set :string]                       ;; Set of strings
[:vector :uuid]                      ;; Vector of UUIDs
[:map-of :keyword :any]              ;; Map with keyword keys

[:map                                ;; Map with specific keys
 [:required-key :string]
 [:optional-key {:optional true} :int]]

[:re #"^[a-z]+$"]                    ;; Regex pattern
```

## Custom Type Registration

```clojure
(defschemas custom-types
  {:email [:re #"^[^@\s]+@[^@\s]+\.[^@\s]+$"]
   :phone [:re #"^\d{10,15}$"]
   :encrypted [:map
               [:ciphertext :string]
               [:encrypted-key :string]
               [:iv :string]]})
```

## Reusable Sub-Schemas

```clojure
(def attribution-source
  [:enum :application_form :intake_form :referral :manual_entry])

(def attribution
  [:map
   [:source attribution-source]
   [:source-details {:optional true} :any]
   [:referring-contact-id {:optional true} :uuid]
   [:recorded-at :string]])

(defschemas events
  {:crm/attribution-recorded
   [:map
    [:contact-id :uuid]
    [:attribution attribution]]})
```

## Conventions

- Group schemas by category: commands, events, queries
- Commands: `:namespace/verb` (create, update, delete, start, etc.)
- Events: `:namespace/entity-past-tense` (created, updated, started)
- Queries: `:namespace/get-entity` or `:namespace/list-entities`
- Use `{:optional true}` for optional fields
- Define reusable sub-schemas as defs
- Match event schemas to what `->event` produces

## Reference Files

- `components/user-service/src/ai/obney/workshop/user_service/interface/schemas.clj` - User schemas
- `components/crm-service/src/ai/obney/workshop/crm_service/interface/schemas.clj` - CRM schemas with custom types
