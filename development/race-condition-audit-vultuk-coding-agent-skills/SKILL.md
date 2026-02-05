---
name: race-condition-audit
description: Systematic identification of race conditions, concurrency bugs, and thread-safety issues across codebases. Use when asked to find race conditions, audit concurrent code, debug non-deterministic behavior, review thread safety, find data races, or analyze async/parallel code. Supports TypeScript, JavaScript, Python, Go, Rust, and C++.
---

# Race Condition Audit

Systematic process for finding concurrency bugs that cause data corruption, deadlocks, or non-deterministic behavior.

## Process

### Step 1: Map Concurrency Entry Points

Find where concurrent execution begins:

```bash
# TypeScript/JavaScript
grep -rn "async \|Promise\|Worker\|fork" --include="*.ts" --include="*.js"

# Python
grep -rn "threading\|asyncio\|async def" --include="*.py"

# Go
grep -rn "go func\|go \w\+(" --include="*.go"

# Rust
grep -rn "thread::spawn\|tokio::spawn\|async fn" --include="*.rs"

# C++
grep -rn "std::thread\|std::async\|pthread" --include="*.cpp" --include="*.hpp"
```

### Step 2: Identify Shared Mutable State

For each entry point, trace:
1. What variables/state are accessed?
2. Are any accessed from multiple concurrent contexts?
3. Is the state mutable?

### Step 3: Verify Synchronization

For each shared mutable state:
1. Is there a lock/mutex/atomic protecting it?
2. Is protection held for the entire critical section?
3. Are ALL access paths protected, including error paths?

### Step 4: Check for Anti-Patterns

Scan for these categories (see language references for specific patterns):

| Category | What to Find |
|----------|--------------|
| Check-Then-Act | `if (x) use(x)` where x can change between check and use |
| Read-Modify-Write | `counter++` or `x = x + 1` without atomics |
| Lazy Init | Double-checked locking, memoization races |
| Publication | Object shared before fully constructed |
| Deadlock | Inconsistent lock ordering, lock held across await |
| Collection Mutation | Iterating while modifying, concurrent map access |
| Async Races | Missing await, Promise.all with shared state |
| Resource Lifecycle | Use after close, double close |
| Memory Ordering | Missing barriers (C++), false sharing |

### Step 5: Report Findings

Use this format:

```markdown
## [RC-001] Brief Title
**File:** `path/to/file.ext:line`
**Category:** Check-Then-Act
**Severity:** Critical | High | Medium | Low

**Code:**
[snippet]

**Bug:** [one sentence explanation]

**Scenario:** [how this manifests]

**Fix:**
[corrected code]
```

## Severity Criteria

- **Critical:** Security bypass, data corruption with financial/legal impact, crashes
- **High:** Data corruption, deadlocks, payment/transaction races
- **Medium:** Non-deterministic tests, resource leaks under contention
- **Low:** Theoretical races, deprecated code, performance issues

## Language References

Load the appropriate reference based on codebase languages:

- **TypeScript/JavaScript:** See [references/typescript-javascript.md](references/typescript-javascript.md)
- **Python:** See [references/python.md](references/python.md)
- **Go:** See [references/go.md](references/go.md)
- **Rust:** See [references/rust.md](references/rust.md)
- **C++:** See [references/cpp.md](references/cpp.md)

Each reference contains language-specific anti-patterns with buggy/fixed code examples.

## Quick Detection Commands

```bash
# Go: Run race detector
go test -race ./...

# C++: Compile with ThreadSanitizer
clang++ -fsanitize=thread -g source.cpp

# Find non-atomic increments (JS/TS)
grep -rn "++" --include="*.ts" | grep -v "for\|while\|i++"

# Find Python threading without locks
grep -rn "threading.Thread" --include="*.py" -A5 | grep -v Lock
```
