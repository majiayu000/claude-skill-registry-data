---
name: test
description: Run Kaocha tests
allowed-tools: Bash(just test*, just), Read, Grep, Glob, mcp__clojure-mcp__clojure_eval
---

# Test

Run tests and debug failures. Before writing tests, read `docs/testing.org`.

## Running Tests

```bash
just test              # Full test suite
just test :e2e         # E2E tests only
just test :generative  # Generative tests only
just test :unit        # Unit tests only
```

## REPL-Based Testing

For rapid iteration (requires nREPL on port 9999):

```clojure
;; Run all tests in a namespace
(require '[clojure.test :refer [run-tests]])
(run-tests 'bits.foo-test)

;; Run a single test
(require '[clojure.test :refer [test-var]])
(test-var #'bits.foo-test/my-test)

;; Reload and test
(require '[bits.foo :as foo] :reload)
(run-tests 'bits.foo-test)
```

## Test Writing Conventions

**BANNED:**

- Arbitrary `Thread/sleep` — use condition-based waits
- `println` in test helpers — return data, assert with `is`
- Visual selectors (color classes) — use ARIA attributes

**REQUIRED:**

- Tests use `^:e2e` or `^:generative` metadata for filtering
- Customize test system with `assoc-in`, never add params to `t/system`
- Check semantic state via ARIA, not visual presentation

## Debugging Failures

### Generative Test Failures

The log shows the shrunk failing sequence:

```
Failed: [[[:type :number "aAA"] ...]]
```

Reproduce in REPL:

```clojure
(require '[bits.form.gen-test :as gen-test])
;; Execute the shrunk actions manually
```

### E2E Test Failures

Common patterns:
| Pattern | Cause |
|---------|-------|
| `Timeout (7):` | Element/condition didn't appear |
| `aria-busy` stuck | Form validation not completing |

Browser screenshots are uploaded as CI artifacts on failure.

$ARGUMENTS
