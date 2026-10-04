---
name: grain-service
description: Create a complete Grain domain service with schemas, read models, commands, queries, and tests
---

# Create a Grain Domain Service (ORC Library)

This skill walks through creating a domain service component in the ORC library. No UI, no web layer — services expose data through commands, queries, and read models.

**Naming conventions:**
- Service name: `widgets` (kebab-case for ns, used as event/command prefix)
- Entity name: `widget` (singular)
- Component dir: `components/widget-service/`

---

## Step 1: Create Component Structure

```
components/widget-service/
  deps.edn
  src/ai/obney/orc/widget_service/
    interface.clj
    interface/schemas.clj
    core/
      read_models.clj
      commands.clj
      queries.clj
      todo_processors.clj
  test/ai/obney/orc/widget_service/
    test_helpers.clj
    commands_test.clj
```

**`deps.edn`:**
```clojure
{:paths ["src" "resources"]
 :deps {}
 :aliases {:test {:extra-paths ["test"]
                  :extra-deps {}}}}
```

---

## Step 2: Define Schemas (`interface/schemas.clj`)

```clojure
(ns ai.obney.orc.widget-service.interface.schemas
  (:require [ai.obney.grain.schema-util.interface :refer [defschemas]]))

(defschemas events
  {:widgets/widget-created [:map [:widget-id :uuid] [:name :string] [:description [:maybe :string]]]
   :widgets/widget-updated [:map [:widget-id :uuid] [:name :string] [:description [:maybe :string]]]
   :widgets/widget-deleted [:map [:widget-id :uuid]]})

(defschemas commands
  {:widgets/create-widget [:map
                           [:name [:string {:min 1 :error/message "Name is required"}]]
                           [:description {:optional true} [:maybe :string]]]
   :widgets/update-widget [:map
                           [:widget-id :uuid]
                           [:name [:string {:min 1 :error/message "Name is required"}]]
                           [:description {:optional true} [:maybe :string]]]
   :widgets/delete-widget [:map
                           [:widget-id :uuid]]})

(defschemas queries
  {:widgets/get-all [:map]
   :widgets/get-by-id [:map [:widget-id :uuid]]})
```

---

## Step 3: Build Read Model (`core/read_models.clj`)

```clojure
(ns ai.obney.orc.widget-service.core.read-models
  (:require [ai.obney.grain.read-model-processor-v2.interface :as rmp :refer [defreadmodel]]))

(def widget-event-types
  #{:widgets/widget-created
    :widgets/widget-updated
    :widgets/widget-deleted})

(defmulti widgets* (fn [_state event] (:event/type event)))

(defmethod widgets* :widgets/widget-created
  [state {:keys [widget-id name description]}]
  (assoc state widget-id {:widget-id widget-id :name name :description description :active true}))

(defmethod widgets* :widgets/widget-updated
  [state {:keys [widget-id name description]}]
  (update state widget-id merge {:name name :description description}))

(defmethod widgets* :widgets/widget-deleted
  [state {:keys [widget-id]}]
  (dissoc state widget-id))

(defmethod widgets* :default [state _] state)

(defreadmodel :widgets widgets
  {:events widget-event-types :version 1}
  [state event]
  (widgets* state event))

;; Query helpers
(defn get-widget [ctx widget-id]
  (get (rmp/project ctx :widgets/widgets {:tags #{[:widget widget-id]}})
       widget-id))

(defn get-all-widgets [ctx]
  (->> (vals (rmp/project ctx :widgets/widgets))
       (filter :active)
       (sort-by :name)))
```

---

## Step 4: Implement Commands (`core/commands.clj`)

```clojure
(ns ai.obney.orc.widget-service.core.commands
  (:require [ai.obney.orc.widget-service.core.read-models :as rm]
            [ai.obney.grain.event-store-v3.interface :refer [->event]]
            [ai.obney.grain.command-processor-v2.interface :refer [defcommand]]
            [cognitect.anomalies :as anom]))

(defcommand :widgets create-widget
  "Create a new widget."
  [{{:keys [name description]} :command :as ctx}]
  (let [widget-id (random-uuid)]
    {:command-result/events
     [(->event {:type :widgets/widget-created
                :tags #{[:widget widget-id]}
                :body {:widget-id widget-id
                       :name name
                       :description description}})]}))

(defcommand :widgets delete-widget
  "Delete a widget."
  [{{:keys [widget-id]} :command :as ctx}]
  (if-let [widget (rm/get-widget ctx widget-id)]
    {:command-result/events
     [(->event {:type :widgets/widget-deleted
                :tags #{[:widget widget-id]}
                :body {:widget-id widget-id}})]}
    {::anom/category ::anom/not-found
     ::anom/message "Widget not found."}))
```

---

## Step 5: Implement Queries (`core/queries.clj`)

Queries return data — no UI rendering in a library.

```clojure
(ns ai.obney.orc.widget-service.core.queries
  (:require [ai.obney.orc.widget-service.core.read-models :as rm]
            [ai.obney.grain.query-processor.interface :refer [defquery]]))

(defquery :widgets get-all
  "Get all active widgets."
  [ctx]
  {:query/result {:widgets (rm/get-all-widgets ctx)}})

(defquery :widgets get-by-id
  "Get a widget by ID."
  [{{:keys [widget-id]} :query :as ctx}]
  (let [widget (rm/get-widget ctx (parse-uuid widget-id))]
    (if widget
      {:query/result {:widget widget}}
      {:query/result {:widget nil}})))
```

---

## Step 6: Create Interface (`interface.clj`)

```clojure
(ns ai.obney.orc.widget-service.interface
  (:require ;; Side-effect requires — registers commands/queries/processors
            [ai.obney.orc.widget-service.core.commands]
            [ai.obney.orc.widget-service.core.queries]
            [ai.obney.orc.widget-service.core.todo-processors]
            ;; Re-export read model helpers
            [ai.obney.orc.widget-service.core.read-models :as rm]))

(def get-widget rm/get-widget)
(def get-all-widgets rm/get-all-widgets)
```

---

## Step 7: Todo Processors (`core/todo_processors.clj`)

```clojure
(ns ai.obney.orc.widget-service.core.todo-processors
  (:require [ai.obney.grain.todo-processor-v2.interface :refer [defprocessor]]))

;; Add defprocessor forms here when event-driven side effects are needed
```

---

## Step 8: Write Tests

```clojure
(ns ai.obney.orc.widget-service.commands-test
  (:require [clojure.test :refer [deftest testing is]]
            [ai.obney.orc.grain-test-utils.interface :as tu]
            [ai.obney.orc.widget-service.core.commands]
            [ai.obney.orc.widget-service.interface.schemas]
            [cognitect.anomalies :as anom]))

(deftest create-widget-test
  (testing "creates a widget"
    (tu/with-test-context [ctx]
      (let [result (tu/process-command! ctx
                     {:command/name :widgets/create-widget
                      :name "Test Widget"
                      :description "A test"})]
        (is (tu/event-of-type? result :widgets/widget-created))
        (let [event (tu/find-event result :widgets/widget-created)]
          (is (= "Test Widget" (:name event))))))))
```

---

## Step 9: Register in `deps.edn`

### Root `deps.edn`

Add to `:aliases > :dev > :extra-deps`:

```clojure
orc/widget-service {:local/root "components/widget-service"}
```

### `projects/orc/deps.edn`

Add to `:deps`:

```clojure
orc/widget-service {:local/root "../../components/widget-service"}
```

---

## Reference Files

- `components/orc-service/` — Core ORC service (comprehensive example)
- `components/colbert/` — ColBERT service (commands, read models, queries)
- `components/ontology/` — Ontology service (event sourcing patterns)
