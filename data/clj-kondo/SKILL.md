---
name: clj-kondo
description: A guide to using clj-kondo for Clojure code linting, including configuration, built-in linters, and writing custom hooks.
---

# clj-kondo Skill Guide

A comprehensive guide to using clj-kondo for Clojure code linting, including configuration, built-in linters, and writing custom hooks.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Configuration](#configuration)
5. [Built-in Linters](#built-in-linters)
6. [Custom Hooks](#custom-hooks)
7. [IDE Integration](#ide-integration)
8. [CI/CD Integration](#cicd-integration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Introduction

### What is clj-kondo?

clj-kondo is a fast, static analyzer and linter for Clojure code. It:

- Catches syntax errors and common mistakes
- Enforces code style and best practices
- Provides immediate feedback during development
- Supports custom linting rules via hooks
- Integrates with all major editors and CI systems
- Requires no project dependencies or runtime

### Why Use clj-kondo?

- **Fast**: Native binary with instant startup
- **Accurate**: Deep understanding of Clojure semantics
- **Extensible**: Custom hooks for domain-specific rules
- **Zero configuration**: Works out of the box
- **Cross-platform**: Native binaries for Linux, macOS, Windows
- **IDE integration**: Works with Emacs, VS Code, IntelliJ, Vim, etc.

## Installation

### macOS/Linux (Homebrew)

```bash
brew install clj-kondo/brew/clj-kondo
```

### Manual Binary Installation

Download from [GitHub Releases](https://github.com/clj-kondo/clj-kondo/releases):

```bash
# Linux
curl -sLO https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/script/install-clj-kondo
chmod +x install-clj-kondo
./install-clj-kondo

# Place in PATH
sudo mv clj-kondo /usr/local/bin/
```

### Via Clojure CLI

```bash
clojure -Ttools install-latest :lib io.github.clj-kondo/clj-kondo :as clj-kondo
clojure -Tclj-kondo run :lint '"src"'
```

### Verify Installation

```bash
clj-kondo --version
# clj-kondo v2024.11.14
```

## Getting Started

### Basic Usage

Lint a single file:

```bash
clj-kondo --lint src/myapp/core.clj
```

Lint a directory:

```bash
clj-kondo --lint src
```

Lint multiple paths:

```bash
clj-kondo --lint src test
```

### Understanding Output

```
src/myapp/core.clj:12:3: warning: unused binding x
src/myapp/core.clj:25:1: error: duplicate key :name
linting took 23ms, errors: 1, warnings: 1
```

Format: `file:line:column: level: message`

### Output Formats

**Human-readable (default):**
```bash
clj-kondo --lint src
```

**JSON (for tooling):**
```bash
clj-kondo --lint src --config '{:output {:format :json}}'
```

**EDN:**
```bash
clj-kondo --lint src --config '{:output {:format :edn}}'
```

### Creating Cache

For better performance on subsequent runs:

```bash
clj-kondo --lint "$(clojure -Spath)" --dependencies --parallel --copy-configs
```

This caches analysis of dependencies and copies their configurations.

## Configuration

### Configuration File Location

clj-kondo looks for `.clj-kondo/config.edn` in:
1. Current directory
2. Parent directories (walking up)
3. Home directory (`~/.config/clj-kondo/config.edn`)

### Basic Configuration

`.clj-kondo/config.edn`:

```clojure
{:linters {:unused-binding {:level :warning}
           :unused-namespace {:level :warning}
           :unresolved-symbol {:level :error}
           :invalid-arity {:level :error}}
 :output {:pattern "{{LEVEL}} {{filename}}:{{row}}:{{col}} {{message}}"}}
```

### Linter Levels

- `:off` - Disable the linter
- `:info` - Informational message
- `:warning` - Warning (default for most)
- `:error` - Error (fails build)

### Global Configuration

Disable specific linters:

```clojure
{:linters {:unused-binding {:level :off}}}
```

Configure linter options:

```clojure
{:linters {:consistent-alias {:aliases {clojure.string str
                                        clojure.set set}}}}
```

### Local Configuration

Suppress warnings in specific namespaces:

```clojure
{:linters {:unused-binding {:level :off
                            :exclude-ns [myapp.test-helpers]}}}
```

### Inline Configuration

In source files:

```clojure
;; Disable for entire namespace
(ns myapp.core
  {:clj-kondo/config '{:linters {:unused-binding {:level :off}}}})

;; Disable for specific form
#_{:clj-kondo/ignore [:unused-binding]}
(let [x 1] 2)

;; Disable all linters for form
#_{:clj-kondo/ignore true}
(some-legacy-code)
```

### Configuration Merging

Configurations merge in this order:
1. Built-in defaults
2. Home directory config
3. Project config (`.clj-kondo/config.edn`)
4. Inline metadata

## Built-in Linters

### Namespace and Require Linters

**`:unused-namespace`** - Warns about unused required namespaces

```clojure
(ns myapp.core
  (:require [clojure.string :as str])) ;; Warning if 'str' never used

;; Fix: Remove unused require
```

**`:unsorted-required-namespaces`** - Enforces sorted requires

```clojure
{:linters {:unsorted-required-namespaces {:level :warning}}}
```

**`:namespace-name-mismatch`** - Ensures namespace matches file path

```clojure
;; In src/myapp/utils.clj
(ns myapp.helpers) ;; Error: should be myapp.utils
```

### Binding and Symbol Linters

**`:unused-binding`** - Warns about unused let bindings

```clojure
(let [x 1
      y 2] ;; Warning: y is unused
  x)

;; Fix: Remove or prefix with underscore
(let [x 1
      _y 2]
  x)
```

**`:unresolved-symbol`** - Catches typos and undefined symbols

```clojure
(defn foo []
  (bar)) ;; Error: unresolved symbol bar

;; Fix: Define bar or require it
```

**`:unused-private-var`** - Warns about unused private definitions

```clojure
(defn- helper []) ;; Warning if never called

;; Fix: Remove or use it
```

### Function and Arity Linters

**`:invalid-arity`** - Catches incorrect function call arities

```clojure
(defn add [a b] (+ a b))
(add 1) ;; Error: wrong arity, expected 2 args

;; Fix: Provide correct number of arguments
```

**`:missing-body-in-when`** - Warns about empty when blocks

```clojure
(when condition) ;; Warning: missing body

;; Fix: Add body or use when-not/if
```

### Collection and Syntax Linters

**`:duplicate-map-key`** - Catches duplicate keys in maps

```clojure
{:name "Alice"
 :age 30
 :name "Bob"} ;; Error: duplicate key :name
```

**`:duplicate-set-key`** - Catches duplicate values in sets

```clojure
#{1 2 1} ;; Error: duplicate set element
```

**`:misplaced-docstring`** - Warns about incorrectly placed docstrings

```clojure
(defn foo
  [x]
  "This is wrong" ;; Warning: docstring after params
  x)

;; Fix: Place before params
(defn foo
  "This is correct"
  [x]
  x)
```

### Type and Spec Linters

**`:type-mismatch`** - Basic type checking

```clojure
(inc "string") ;; Warning: expected number
```

**`:invalid-arities`** - Checks arities for core functions

```clojure
(map) ;; Error: map requires at least 2 arguments
```

## Custom Hooks

### What Are Hooks?

Hooks are custom linting rules written in Clojure that analyze your code using clj-kondo's analysis data. They enable:

- Domain-specific linting rules
- API usage validation
- Deprecation warnings
- Team convention enforcement
- Advanced static analysis

### When to Use Hooks

Use hooks when:
- Built-in linters don't cover your needs
- You have library-specific patterns to enforce
- You want to warn about deprecated APIs
- You need to validate domain-specific logic
- You want to enforce team coding standards

### Hook Architecture

Hooks receive:
1. **Analysis context** - Information about the code being analyzed
2. **Node** - The AST node being examined

Hooks return:
1. **Findings** - Lint warnings/errors to report
2. **Updated analysis** - Modified context for downstream analysis

### Creating Your First Hook

#### 1. Hook Directory Structure

```
.clj-kondo/
  config.edn
  hooks/
    my_hooks.clj
```

#### 2. Basic Hook Template

`.clj-kondo/hooks/my_hooks.clj`:

```clojure
(ns hooks.my-hooks
  (:require [clj-kondo.hooks-api :as api]))

(defn my-hook
  "Description of what this hook does"
  [{:keys [node]}]
  (let [sexpr (api/sexpr node)]
    (when (some-condition? sexpr)
      {:findings [{:message "Custom warning message"
                   :type :my-custom-warning
                   :row (api/row node)
                   :col (api/col node)}]})))
```

#### 3. Register Hook

`.clj-kondo/config.edn`:

```clojure
{:hooks {:analyze-call {my.ns/my-macro hooks.my-hooks/my-hook}}}
```

### Hook Types

#### `:analyze-call` Hooks

Triggered when analyzing function/macro calls:

```clojure
;; Hook for analyzing (deprecated-fn ...) calls
{:hooks {:analyze-call {my.api/deprecated-fn hooks.deprecation/check}}}
```

Hook implementation:

```clojure
(defn check [{:keys [node]}]
  {:findings [{:message "my.api/deprecated-fn is deprecated, use new-fn instead"
               :type :deprecated-api
               :row (api/row node)
               :col (api/col node)
               :level :warning}]})
```

#### `:macroexpand` Hooks

Transform macro calls for better analysis:

```clojure
;; For macros that expand to def forms
{:hooks {:macroexpand {my.dsl/defentity hooks.dsl/expand-defentity}}}
```

Hook implementation:

```clojure
(defn expand-defentity [{:keys [node]}]
  (let [[_ name-node & body] (rest (:children node))
        new-node (api/list-node
                  [(api/token-node 'def)
                   name-node
                   (api/map-node body)])]
    {:node new-node}))
```

### Hook API Reference

#### Node Functions

```clojure
;; Get node type
(api/tag node) ;; => :list, :vector, :map, :token, etc.

;; Get children nodes
(api/children node)

;; Convert node to s-expression
(api/sexpr node)

;; Get position
(api/row node)
(api/col node)
(api/end-row node)
(api/end-col node)

;; String representation
(api/string node)
```

#### Node Constructors

```clojure
;; Create nodes
(api/token-node 'symbol)
(api/keyword-node :keyword)
(api/string-node "string")
(api/number-node 42)

(api/list-node [node1 node2 node3])
(api/vector-node [node1 node2])
(api/map-node [key-node val-node key-node val-node])
(api/set-node [node1 node2])
```

#### Node Predicates

```clojure
(api/token-node? node)
(api/keyword-node? node)
(api/string-node? node)
(api/list-node? node)
(api/vector-node? node)
(api/map-node? node)
```

### Practical Hook Examples

#### Example 1: Deprecation Warning

Warn about deprecated function usage:

```clojure
(ns hooks.deprecation
  (:require [clj-kondo.hooks-api :as api]))

(defn warn-deprecated-fn [{:keys [node]}]
  {:findings [{:message "old-api is deprecated. Use new-api instead."
               :type :deprecated-function
               :row (api/row node)
               :col (api/col node)
               :level :warning}]})
```

Config:

```clojure
{:hooks {:analyze-call {mylib/old-api hooks.deprecation/warn-deprecated-fn}}}
```

#### Example 2: Argument Validation

Ensure specific argument types:

```clojure
(ns hooks.validation
  (:require [clj-kondo.hooks-api :as api]))

(defn validate-query-args [{:keys [node]}]
  (let [args (rest (:children node))
        first-arg (first args)]
    (when-not (and first-arg (api/keyword-node? first-arg))
      {:findings [{:message "First argument to query must be a keyword"
                   :type :invalid-argument
                   :row (api/row node)
                   :col (api/col node)
                   :level :error}]})))
```

Config:

```clojure
{:hooks {:analyze-call {mylib/query hooks.validation/validate-query-args}}}
```

#### Example 3: DSL Expansion

Expand custom DSL for better analysis:

```clojure
(ns hooks.dsl
  (:require [clj-kondo.hooks-api :as api]))

(defn expand-defrequest
  "Expand (defrequest name & body) to (def name (request & body))"
  [{:keys [node]}]
  (let [[_ name-node & body-nodes] (:children node)
        request-call (api/list-node
                      (list* (api/token-node 'request)
                             body-nodes))
        expanded (api/list-node
                  [(api/token-node 'def)
                   name-node
                   request-call])]
    {:node expanded}))
```

Config:

```clojure
{:hooks {:macroexpand {myapp.http/defrequest hooks.dsl/expand-defrequest}}}
```

#### Example 4: Thread-Safety Check

Warn about unsafe concurrent usage:

```clojure
(ns hooks.concurrency
  (:require [clj-kondo.hooks-api :as api]))

(defn check-atom-swap [{:keys [node]}]
  (let [args (rest (:children node))
        fn-arg (second args)]
    (when (and fn-arg
               (api/list-node? fn-arg)
               (= 'fn (api/sexpr (first (:children fn-arg)))))
      {:findings [{:message "Consider using swap-vals! for atomicity"
                   :type :concurrency-hint
                   :row (api/row node)
                   :col (api/col node)
                   :level :info}]})))
```

#### Example 5: Required Keys Validation

Ensure maps have required keys:

```clojure
(ns hooks.maps
  (:require [clj-kondo.hooks-api :as api]))

(defn validate-config-keys [{:keys [node]}]
  (let [args (rest (:children node))
        config-map (first args)]
    (when (api/map-node? config-map)
      (let [keys (->> (:children config-map)
                      (take-nth 2)
                      (map api/sexpr)
                      (set))
            required #{:host :port :timeout}
            missing (clojure.set/difference required keys)]
        (when (seq missing)
          {:findings [{:message (str "Missing required keys: " missing)
                       :type :missing-config-keys
                       :row (api/row node)
                       :col (api/col node)
                       :level :error}]})))))
```

### Testing Hooks

#### Manual Testing

1. Create test file:

```clojure
;; test-hook.clj
(ns test-hook
  (:require [mylib :as lib]))

(lib/deprecated-fn) ;; Should trigger warning
```

2. Run clj-kondo:

```bash
clj-kondo --lint test-hook.clj
```

#### Unit Testing Hooks

Use `clj-kondo.core` for testing:

```clojure
(ns hooks.my-hooks-test
  (:require [clojure.test :refer [deftest is testing]]
            [clj-kondo.core :as clj-kondo]))

(deftest test-my-hook
  (testing "detects deprecated function usage"
    (let [result (with-in-str "(ns test) (mylib/old-api)"
                   (clj-kondo/run!
                    {:lint ["-"]
                     :config {:hooks {:analyze-call
                                      {mylib/old-api
                                       hooks.deprecation/warn-deprecated-fn}}}}))]
      (is (= 1 (count (:findings result))))
      (is (= :deprecated-function
             (-> result :findings first :type))))))
```

### Distributing Hooks

#### As Library Config

Include hooks with your library:

```
my-library/
  .clj-kondo/
    config.edn          # Hook registration
    hooks/
      my_library.clj    # Hook implementations
  src/
    my_library/
      core.clj
```

Users get hooks automatically via `--copy-configs`.

#### Standalone Hook Library

Create a dedicated hook library:

```clojure
;; deps.edn
{:paths ["."]
 :deps {clj-kondo/clj-kondo {:mvn/version "2024.11.14"}}}
```

Users install via:

```bash
clj-kondo --lint "$(clojure -Spath -Sdeps '{:deps {my/hooks {:git/url \"...\"}}}')" --dependencies --copy-configs
```

### Hook Best Practices

1. **Performance**: Keep hooks fast - they run on every lint
2. **Specificity**: Target specific forms, not every function call
3. **Clear messages**: Provide actionable error messages
4. **Documentation**: Document what hooks check and why
5. **Testing**: Test hooks with various inputs
6. **Versioning**: Version hooks with your library
7. **Graceful degradation**: Handle malformed code gracefully

## IDE Integration

### VS Code

Install [Calva](https://marketplace.visualstudio.com/items?itemName=betterthantomorrow.calva):

- clj-kondo linting enabled by default
- Real-time feedback as you type
- Automatic `.clj-kondo` directory recognition

### Emacs

With `flycheck-clj-kondo`:

```elisp
(use-package flycheck-clj-kondo
  :ensure t)
```

### IntelliJ IDEA / Cursive

- Native clj-kondo integration
- Configure via Preferences → Editor → Inspections

### Vim/Neovim

With ALE:

```vim
let g:ale_linters = {'clojure': ['clj-kondo']}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Lint
on: [push, pull_request]
jobs:
  clj-kondo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install clj-kondo
        run: |
          curl -sLO https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/script/install-clj-kondo
          chmod +x install-clj-kondo
          ./install-clj-kondo
      - name: Run clj-kondo
        run: clj-kondo --lint src test
```

### GitLab CI

```yaml
lint:
  image: cljkondo/clj-kondo:latest
  script:
    - clj-kondo --lint src test
```

### Pre-commit Hook

`.git/hooks/pre-commit`:

```bash
#!/bin/bash
clj-kondo --lint src test
exit $?
```

## Best Practices

### 1. Start with Defaults

Begin with zero configuration - clj-kondo's defaults catch most issues.

### 2. Gradual Adoption

For existing projects:

```bash
# Generate baseline
clj-kondo --lint src --config '{:output {:exclude-warnings true}}'

# Fix incrementally
```

### 3. Team Configuration

Standardize via `.clj-kondo/config.edn`:

```clojure
{:linters {:consistent-alias {:level :warning
                              :aliases {clojure.string str
                                        clojure.set set}}}
 :output {:exclude-files ["generated/"]}}
```

### 4. Leverage Hooks for Domain Logic

Write hooks for:
- API deprecations
- Team conventions
- Domain-specific validations

### 5. Cache Dependencies

```bash
# Run once after dep changes
clj-kondo --lint "$(clojure -Spath)" --dependencies --parallel --copy-configs
```

### 6. Ignore Thoughtfully

Prefer fixing over ignoring. When ignoring:

```clojure
;; Document why
#_{:clj-kondo/ignore [:unresolved-symbol]
   :reason "Macro generates this symbol"}
(some-macro)
```

## Troubleshooting

### False Positives

**Unresolved symbol in macro:**

```clojure
;; Add to config
{:lint-as {myapp/my-macro clojure.core/let}}
```

**Incorrect arity for variadic macro:**

Write a macroexpand hook (see Custom Hooks section).

### Performance Issues

**Slow linting:**

```bash
# Cache dependencies
clj-kondo --lint "$(clojure -Spath)" --dependencies --parallel

# Exclude large dirs
{:output {:exclude-files ["node_modules/" "target/"]}}
```

### Hook Debugging

**Hook not triggering:**

1. Check hook registration in config.edn
2. Verify namespace matches
3. Test with minimal example
4. Check for typos in qualified symbols

**Hook errors:**

```bash
# Run with debug output
clj-kondo --lint src --debug
```

### Configuration Not Loading

Check:
1. File is named `.clj-kondo/config.edn` (note the dot)
2. EDN syntax is valid
3. File is in project root or parent directory

## Resources

- [Official Documentation](https://github.com/clj-kondo/clj-kondo/tree/master/doc)
- [Hook Examples](https://github.com/clj-kondo/clj-kondo/tree/master/examples)
- [Configuration Reference](https://github.com/clj-kondo/clj-kondo/blob/master/doc/config.md)
- [Hooks API Reference](https://github.com/clj-kondo/clj-kondo/blob/master/doc/hooks.md)
- [Linters Reference](https://github.com/clj-kondo/clj-kondo/blob/master/doc/linters.md)

## Summary

clj-kondo is an essential tool for Clojure development offering:
- Immediate feedback on code quality
- Extensive built-in linting rules
- Powerful custom hooks for domain-specific rules
- Seamless IDE and CI/CD integration
- Zero-configuration operation with extensive customization options

Start with the defaults, customize as needed, and leverage hooks for your specific requirements.
