---
name: component
description: Create a new Clojure component
allowed-tools: Read, Edit, Write, Grep, Glob, mcp__clojure-mcp__*
---

# Create Component

Create a new Clojure component following project conventions. Before starting,
read `docs/clojure.org`.

## Component Structure

Every component namespace follows this structure:

```clojure
(ns bits.foo
  (:require
   [bits.spec]
   [clojure.spec.alpha :as s]
   [com.stuartsierra.component :as component]))

;;; ----------------------------------------------------------------------------
;;; API

(defn do-thing
  [foo-component arg]
  ;; Component as first argument
  ...)

;;; ----------------------------------------------------------------------------
;;; Component

(defrecord Foo [config-val other-val]
  component/Lifecycle
  (start [this]
    ;; Initialize, return updated this
    this)
  (stop [this]
    ;; Cleanup, return this
    this))

(defn make-foo
  [config]
  {:pre [(s/valid? :bits.foo/config config)]}
  (map->Foo config))

(defmethod print-method Foo
  [foo ^java.io.Writer w]
  (.write w "#<Foo>"))
```

## Specs in bits.spec

To avoid cyclic dependencies, put component config specs in `bits.spec`:

```clojure
;; In bits.spec (use literal keywords)
(s/def :bits.foo/config-val string?)
(s/def :bits.foo/config
  (s/keys :req-un [:bits.foo/config-val]))
```

## Configuration in bits.app

All defaults live in `bits.app/read-config`:

```clojure
;; In bits.app
(defn read-config []
  {:foo {:config-val "default"}
   ...})
```

**BANNED:**

- Defaults in component namespace
- `System/getenv` outside bits.app
- Optional parameters on `make-*` functions

## Wire into System

Add to `bits.app/make-system`:

```clojure
(component/system-map
  ...
  :foo (component/using
         (foo/make-foo (:foo config))
         [:dependency-component]))
```

## Checklist

1. [ ] Spec in `bits.spec` with literal keywords
2. [ ] Config defaults in `bits.app/read-config`
3. [ ] Record implements `component/Lifecycle`
4. [ ] Factory is `make-<name>` with `:pre` validation
5. [ ] Print method hides sensitive data
6. [ ] API functions take component as first arg
7. [ ] Wired into system with dependencies

$ARGUMENTS
