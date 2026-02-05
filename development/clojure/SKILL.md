---
name: clojure
description: Develop Clojure applications using deps.edn, tools.deps, and functional patterns. Activate when working with .clj/.cljc/.cljs files, deps.edn, or user mentions Clojure, REPL, spec, transducers, reducers, or functional programming.
---

# Clojure Development

Functional-first Clojure with **deps.edn**, **tools.deps**, and **immutability**.

## Workflow

```
1. MODEL    -> Define data with maps, records, specs
2. COMPOSE  -> Build with pure functions, ->> threading
3. TEST     -> Write tests first (clojure.test or Kaocha)
4. VALIDATE -> clojure -M:test/run && clj-kondo --lint src
5. ITERATE  -> Refactor in REPL, keep functions pure
```

## CLI

```bash
# Project setup
clojure -Tnew app :name myuser/myapp    # New app project
clojure -Tnew lib :name myuser/mylib    # New library

# Run
clojure -M -m myapp.core                # Run -main
clojure -M:run                          # Via alias
clojure -X:run                          # Exec function

# REPL
clj                                     # Basic REPL
clojure -M:repl/rebel                   # Rebel readline

# Test
clojure -X:test/run                     # Run tests (Kaocha)
clojure -M:test -m kaocha.runner        # Alternative

# Build
clojure -T:build uber                   # Uberjar
clojure -T:build jar                    # Library jar

# Dependencies
clojure -X:deps tree                    # Dependency tree
clojure -X:deps find-versions :lib clojure.java-time/clojure.java-time
clojure -M:search/outdated              # Find outdated deps
```

## Project Structure

```
myapp/
├── deps.edn
├── build.clj               # tools.build script
├── src/
│   └── myapp/
│       ├── core.clj
│       └── db.clj
├── test/
│   └── myapp/
│       └── core_test.clj
└── resources/
```

## deps.edn Configuration

```clojure
{:paths ["src" "resources"]

 :deps
 {org.clojure/clojure {:mvn/version "1.12.0"}
  org.clojure/core.async {:mvn/version "1.6.681"}
  metosin/malli {:mvn/version "0.16.4"}}

 :aliases
 {;; Run application
  :run
  {:main-opts ["-m" "myapp.core"]}

  ;; REPL with rebel-readline
  :repl/rebel
  {:extra-deps {com.bhauman/rebel-readline {:mvn/version "0.1.4"}}
   :main-opts ["-m" "rebel-readline.main"]}

  ;; Testing with Kaocha
  :test/run
  {:extra-paths ["test"]
   :extra-deps {lambdaisland/kaocha {:mvn/version "1.91.1392"}}
   :exec-fn kaocha.runner/exec-fn
   :exec-args {:fail-fast? true}}

  ;; Build
  :build
  {:replace-paths ["."]
   :replace-deps {io.github.clojure/tools.build
                  {:git/tag "v0.10.5" :git/sha "2a21b7a"}}
   :ns-default build}

  ;; Linting
  :lint
  {:extra-deps {clj-kondo/clj-kondo {:mvn/version "2024.08.01"}}
   :main-opts ["-m" "clj-kondo.main" "--lint" "src" "test"]}

  ;; Outdated deps
  :search/outdated
  {:extra-deps {com.github.liquidz/antq {:mvn/version "2.8.1201"}}
   :main-opts ["-m" "antq.core"]}}}
```

## Dependency Types

```clojure
;; Maven (most common)
{org.clojure/data.json {:mvn/version "2.5.0"}}

;; Git (latest or specific commit)
{io.github.user/lib {:git/tag "v1.0.0" :git/sha "abc1234"}}
{io.github.user/lib {:git/sha "abc1234def5678"}}

;; Local development
{mylib {:local/root "../mylib"}}
```

## Core Patterns

### Pure Functions + Immutability

```clojure
;; Immutable by default
(defn update-user [user new-email]
  (assoc user :email new-email))  ; Returns new map

;; Transform, don't mutate
(update {:count 0} :count inc)    ; => {:count 1}
(update-in m [:user :age] inc)    ; Nested update
```

### Threading Macros

```clojure
;; Thread-first: subject flows through
(-> user
    (assoc :updated-at (now))
    (update :login-count inc)
    validate
    save)

;; Thread-last: collection flows through
(->> numbers
     (filter even?)
     (map inc)
     (reduce +))

;; Conditional threading
(cond-> user
  admin? (assoc :role :admin)
  verified? (assoc :verified true))
```

### Destructuring

```clojure
;; Maps
(let [{:keys [name email]} user] ...)
(let [{:keys [name] :or {name "anon"}} user] ...)
(let [{:keys [name] :as user} data] ...)

;; Vectors
(let [[x y & rest] coords] ...)
(let [[_ second third] items] ...)

;; Function parameters
(defn greet [{:keys [name email]}]
  (format "Hello %s (%s)" name email))
```

### Higher-Order Functions

```clojure
;; Composition
(def process (comp str/upper-case str/trim))
(process "  hello  ")  ; => "HELLO"

;; Partial application
(def add-five (partial + 5))
(add-five 10)  ; => 15

;; Multiple transforms
((juxt :name :age) {:name "Alice" :age 30})
; => ["Alice" 30]
```

### Control Flow

```clojure
;; when: single truthy branch
(when (valid? user)
  (save user))

;; if-let: bind and branch
(if-let [user (find-user id)]
  (process user)
  (handle-not-found))

;; case: compile-time constants (fast)
(case status
  :pending (handle-pending)
  :active (handle-active)
  (handle-unknown))

;; cond: complex conditions
(cond
  (neg? n) "negative"
  (pos? n) "positive"
  :else "zero")
```

## Naming Conventions

```clojure
;; kebab-case for vars and functions
(def max-retry-attempts 3)
(defn calculate-total-price [items] ...)

;; Predicates end with ?
(defn valid-email? [email] ...)

;; Side-effecting functions end with !
(defn save-user! [user] ...)
(defn reset-counter! [] ...)

;; Dynamic vars use earmuffs
(def ^:dynamic *config* {...})

;; CamelCase for protocols and records
(defprotocol Storage ...)
(defrecord DatabaseStorage [conn] ...)

;; Private functions use defn-
(defn- parse [input] ...)      ; Internal helper
(defn process [data] ...)      ; Public API
```

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Mutable state everywhere | Use atoms sparingly, prefer pure functions |
| `(if (not x) ...)` | `(if-not x ...)` or `(when-not x ...)` |
| `(not (= a b))` | `(not= a b)` |
| `(first (filter pred coll))` | `(some pred coll)` |
| Deep nesting | Threading macros `->`, `->>` |
| `(into [] (map f coll))` | `(mapv f coll)` |
| String concatenation | `(str a b c)` or `(format ...)` |
| `(nth coll 0)` | `(first coll)` |
| Manual recursion | `reduce`, `iterate`, `loop/recur` |
| `def` inside functions | `let` bindings |

## References

- [reference.md](reference.md) - Data structures, best practices, idioms, error handling
- [patterns.md](cookbook/patterns.md) - Functional patterns, sequences, transducers
- [concurrency.md](cookbook/concurrency.md) - Atoms, refs, agents, core.async
- [spec.md](cookbook/spec.md) - clojure.spec validation & generative testing
- [testing.md](cookbook/testing.md) - clojure.test, Kaocha configuration
- [macros.md](cookbook/macros.md) - Metaprogramming patterns
