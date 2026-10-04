---
name: grain-periodic-task
description: Create scheduled background jobs that run on cron schedules
---

# Grain Periodic Task Pattern

Periodic tasks are scheduled background jobs that run on cron schedules. They use `defperiodic` to emit trigger events, and a corresponding `defprocessor` handles the actual work.

See **Pattern Compendium section 1.4.1** for the authoritative reference.

## Two-File Pattern

Periodic tasks are split into two parts:

1. **`periodic_tasks.clj`** -- `defperiodic` emits a lightweight trigger event per tenant on schedule
2. **`todo_processors.clj`** -- `defprocessor` subscribes to the trigger event and does the real work

The framework iterates over all tenants automatically. The `defperiodic` handler receives `[tenant-id time]` (NOT `[context time]`) and returns `{:result/events [...]}`. The framework appends the events per-tenant.

## Periodic Task File (`core/periodic_tasks.clj`)

```clojure
(ns ai.obney.orc.my-service.core.periodic-tasks
  "Scheduled trigger events for my-service."
  (:require [ai.obney.grain.event-store-v3.interface :refer [->event]]
            [ai.obney.grain.periodic-task.interface :refer [defperiodic]]))

(defperiodic :my-service send-reminders
  {:schedule {:cron "0 * * * *" :timezone "America/Chicago"}}
  "Emit reminder-check trigger for each tenant every hour."
  [_tenant-id time]
  {:result/events
   [(->event {:type :my-service/reminder-check-triggered
              :tags #{[:reminder-check (random-uuid)]}
              :body {:triggered-at (str time)}})]})
```

The generated var name is `my-service-send-reminders`.

## Corresponding Processor (`core/todo_processors.clj`)

```clojure
(ns ai.obney.orc.my-service.core.todo-processors
  (:require [ai.obney.orc.my-service.core.read-models :as rm]
            [ai.obney.grain.command-processor-v2.interface :as cp]
            [ai.obney.grain.time.interface :as time]
            [ai.obney.grain.todo-processor-v2.interface :refer [defprocessor]]
            [com.brunobonacci.mulog :as u]))

(defprocessor :my-service reminder-runner
  {:topics #{:my-service/reminder-check-triggered}}
  "Process pending reminders when trigger fires."
  [context]
  (let [items (rm/get-pending-items context)]
    (u/log ::reminder-runner :count (count items))
    (doseq [item items]
      (cp/process-command
       (assoc context :command {:command/id (random-uuid)
                                :command/timestamp (time/now)
                                :command/name :my-service/send-reminder
                                :item-id (:id item)})))
    {}))
```

## Complete Example: Membership Billing

```clojure
;; periodic_tasks.clj
(defperiodic :membership billing-check
  {:schedule {:cron "0 6 * * *" :timezone "America/Chicago"}}
  "Daily billing check trigger."
  [_tenant-id time]
  {:result/events [(->event {:type :membership/billing-check-triggered
                             :tags #{[:billing-check (random-uuid)]}
                             :body {:triggered-at (str time)}})]})

;; todo_processors.clj
(defprocessor :membership billing-runner
  {:topics #{:membership/billing-check-triggered}}
  "Process memberships due for billing."
  [context]
  (let [today (str (java.time.LocalDate/now))
        due (rm/get-memberships-due-for-billing context today)]
    (doseq [m due]
      (cp/process-command
       (assoc context :command {:command/id (random-uuid)
                                :command/timestamp (time/now)
                                :command/name :membership/initiate-billing
                                :membership-id (:membership-id m)})))
    {}))
```

## Schedule Formats

| Format | Example | Description |
|--------|---------|-------------|
| Cron | `{:cron "0 * * * *" :timezone "America/Chicago"}` | Standard cron (minute hour day month weekday) |

Common cron patterns:
- `"0 * * * *"` -- every hour on the hour
- `"*/15 * * * *"` -- every 15 minutes
- `"0 3 * * *"` -- daily at 3 AM
- `"0 6 * * *"` -- daily at 6 AM
- `"0 0 * * 1"` -- weekly on Monday at midnight

## CAS for Idempotency

When a trigger event must be processed at most once, use CAS inside the `defprocessor`:

```clojure
(defprocessor :my-service digest-sender
  {:topics #{:my-service/digest-triggered}}
  "Send daily digest -- at most once per user per day."
  [context]
  (let [users (rm/get-users-needing-digest context)]
    (doseq [user users]
      (es/append (:event-store context)
                 {:tenant-id (:tenant-id context)
                  :events [(->event {:type :my-service/digest-sent
                                     :tags #{[:user (:user-id user)]}
                                     :body {:user-id (:user-id user)
                                            :date (str (java.time.LocalDate/now))}})]
                  :cas {:types #{:my-service/digest-sent}
                        :tags #{[:user (:user-id user)]}
                        :predicate-fn (fn [existing]
                                        (empty? (into [] existing)))}}))
    {}))
```

The CAS predicate checks that no `:my-service/digest-sent` event exists for this user with these tags. If another instance already emitted one, the append silently fails.

## Auto-Registration and Wiring

Both `defperiodic` and `defprocessor` register in global registries automatically. No manual registry maps are needed.

**Interface.clj** only needs bare side-effect requires:

```clojure
(ns ai.obney.orc.my-service.interface
  (:require [ai.obney.orc.my-service.core.commands]
            [ai.obney.orc.my-service.core.queries]
            [ai.obney.orc.my-service.core.todo-processors]   ;; bare require
            [ai.obney.orc.my-service.core.periodic-tasks]    ;; bare require
            [ai.obney.orc.my-service.core.read-models :as rm]))

;; No periodic-tasks or todo-processors re-export needed
(def get-item rm/get-item)
```

No manual wiring is needed. `pt/start-periodic-triggers!` discovers periodic tasks from the global registry. The control plane discovers todo processors the same way.

## Reference Files

- `components/membership-service/src/.../core/periodic_tasks.clj` -- Billing check trigger
- `components/scheduling-service/src/.../core/periodic_tasks.clj` -- Scheduling triggers
- `components/user-service/src/.../core/periodic_tasks.clj` -- User maintenance
- `docs/contributors/CONTRIBUTOR-GRAIN-PATTERNS.md` section 1.4.1 -- Authoritative periodic task reference
