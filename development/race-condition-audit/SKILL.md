---
name: race-condition-audit
description: Systematic identification of race conditions, concurrency bugs, and thread-safety issues across codebases. Use when asked to find race conditions, audit concurrent code, debug non-deterministic behavior, review thread safety, find data races, or analyze async/parallel code. Supports TypeScript, JavaScript, Python, Go, Rust, C++, Java, and Kotlin.
triggers:
  - "find race conditions"
  - "audit concurrent code"
  - "check thread safety"
  - "find data races"
  - "debug non-deterministic"
  - "review async code"
prerequisites:
  - "Language-specific tools (optional): Go race detector, ThreadSanitizer (C++), FindBugs/SpotBugs (Java)"
arguments:
  - name: SCOPE
    required: false
    description: Path or pattern to audit (defaults to entire repository)
  - name: LANGUAGE
    required: false
    description: Primary language to focus on (auto-detected if not provided)
---

# Race Condition Audit

Systematic process for finding concurrency bugs that cause data corruption, deadlocks, or non-deterministic behavior.

**Codex note:** This skill references Claude Code subagents (`Task(...)`). In Codex, run the equivalent steps with tool calls (for example `functions.shell_command` and `multi_tool_use.parallel`) or run them sequentially. See [`../../COMPATIBILITY.md`](../../COMPATIBILITY.md).

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

# Java/Kotlin
grep -rn "new Thread\|ExecutorService\|CompletableFuture\|suspend fun\|launch\|async {" --include="*.java" --include="*.kt"
```

### Step 2: Identify Shared Mutable State

For each entry point, trace:
1. What variables/state are accessed?
2. Are any accessed from multiple concurrent contexts?
3. Is the state mutable?

### Step 3: Verify Synchronisation

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
| Lazy Init | Double-checked locking, memoisation races |
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

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Critical** | Security bypass, data corruption with financial/legal impact, crashes in production | Payment double-processing, auth bypass, data loss |
| **High** | Data corruption, deadlocks, payment/transaction races | Inventory oversell, session corruption, API timeout deadlock |
| **Medium** | Non-deterministic tests, resource leaks under contention | Flaky tests, connection pool exhaustion |
| **Low** | Theoretical races, deprecated code, performance issues | Unlikely timing windows, benign data races |

## Scoring Race Conditions

When reporting, include a risk score:

```
Risk = Likelihood x Impact

Likelihood:
- High: Occurs regularly in normal operation
- Medium: Occurs under load or specific timing
- Low: Requires precise timing or unusual conditions

Impact:
- High: Data loss, security breach, financial impact
- Medium: Degraded service, incorrect results
- Low: Cosmetic issues, minor inconsistencies
```

## Testing for Race Conditions

### Automated Tools

```bash
# Go: Run race detector
go test -race ./...

# C++: Compile with ThreadSanitizer
clang++ -fsanitize=thread -g source.cpp

# Java: Use jcstress for stress testing
java -jar jcstress.jar

# Python: Use pytest with hypothesis for property testing
pytest --hypothesis-seed=random
```

### Manual Stress Testing

1. **Increase concurrency**: Run with 10x normal thread/connection count
2. **Add delays**: Insert random delays in critical sections
3. **Reduce timeouts**: Make timing windows smaller
4. **Run repeatedly**: Execute tests 100+ times to catch intermittent failures

## Language References

Load the appropriate reference based on codebase languages:

- **TypeScript/JavaScript:** See [references/typescript-javascript.md](references/typescript-javascript.md)
- **Python:** See [references/python.md](references/python.md)
- **Go:** See [references/go.md](references/go.md)
- **Rust:** See [references/rust.md](references/rust.md)
- **C++:** See [references/cpp.md](references/cpp.md)
- **Java/Kotlin:** See [references/java-kotlin.md](references/java-kotlin.md)

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

# Find Java synchronized methods (potential bottlenecks)
grep -rn "synchronized" --include="*.java"

# Find Kotlin coroutines with shared state
grep -rn "var.*=.*mutableListOf\|var.*=.*mutableMapOf" --include="*.kt"
```

## Subagent Usage

Use subagents to parallelize analysis across languages and anti-pattern categories.

### Step 1: Parallel Language Analysis

For multi-language codebases, launch Explore agents in parallel for each language:

```
Launch parallel Explore agents:

1. TypeScript/JavaScript Agent:
   "Audit TypeScript/JavaScript code for race conditions.
   Search for:
   - async/await patterns without proper synchronization
   - Promise.all with shared state modifications
   - Missing await statements
   - Event handler races
   - Worker thread shared memory issues

   Load patterns from references/typescript-javascript.md
   Return: List of findings with file:line, category, and severity"

2. Python Agent:
   "Audit Python code for race conditions.
   Search for:
   - threading.Thread without proper locks
   - asyncio races (shared state in coroutines)
   - GIL misconceptions (I/O bound races still exist)
   - multiprocessing shared memory issues

   Load patterns from references/python.md
   Return: List of findings with file:line, category, and severity"

3. Go Agent:
   "Audit Go code for race conditions.
   Search for:
   - goroutines accessing shared variables
   - channel misuse (send after close, range on closed)
   - map concurrent access
   - sync.WaitGroup races

   Load patterns from references/go.md
   Run: go test -race ./... if tests exist
   Return: List of findings with file:line, category, and severity"

4. Rust Agent:
   "Audit Rust code for race conditions.
   Search for:
   - unsafe blocks with shared mutable state
   - Arc<Mutex<T>> deadlock potential
   - async race conditions
   - interior mutability misuse

   Load patterns from references/rust.md
   Return: List of findings with file:line, category, and severity"
```

**Benefits:**
- Multi-language codebases analyzed concurrently
- Each agent has full context of language-specific patterns
- Main context receives synthesized findings only

### Step 4: Parallel Anti-Pattern Detection

For thorough audits, launch parallel agents for each critical anti-pattern:

```
Launch parallel Explore agents:

1. Check-Then-Act Agent:
   "Find check-then-act race conditions across the codebase.
   Pattern: if (condition) { use(value) } where value can change
   Look for:
   - File existence checks before read/write
   - Map key checks before access
   - Null checks with delayed use
   - Permission checks before action
   Return: Findings with code snippets and race scenarios"

2. Read-Modify-Write Agent:
   "Find non-atomic read-modify-write operations.
   Pattern: value = value + 1 without synchronization
   Look for:
   - counter++, counter += 1
   - x = x.concat(...), x = [...x, item]
   - Non-atomic balance updates
   - Cache invalidation races
   Return: Findings with code snippets and race scenarios"

3. Deadlock Agent:
   "Find potential deadlock scenarios.
   Look for:
   - Inconsistent lock ordering (A then B vs B then A)
   - Lock held across await/async boundaries
   - Nested synchronized blocks
   - Resource acquisition cycles
   Return: Findings with lock ordering diagrams"

4. Collection Mutation Agent:
   "Find concurrent collection access issues.
   Look for:
   - Iterating while modifying same collection
   - Concurrent map/set access without synchronization
   - Array modifications during forEach/map
   - Shared queue access patterns
   Return: Findings with code snippets and race scenarios"
```

**Benefits:**
- Thorough coverage of each anti-pattern category
- Specialized search patterns for each category
- Parallel execution on large codebases

### Synthesizing Results

After parallel agents complete, main context synthesizes:

```markdown
## Race Condition Audit Summary

### By Severity
- Critical: X findings
- High: Y findings
- Medium: Z findings

### By Category
| Category | Count | Most Affected Files |
|----------|-------|---------------------|
| Check-Then-Act | N | file1.ts, file2.py |
| Read-Modify-Write | N | file3.go, file4.rs |
| Deadlock | N | file5.java |

### Top Priority Fixes
1. [RC-001] Critical: [title] at file:line
2. [RC-002] Critical: [title] at file:line
```

**When to use subagents:**
- Multi-language codebase (> 1 language): Use parallel language agents
- Large codebase (> 10k LOC): Use parallel anti-pattern agents
- Comprehensive audit requested: Use both

**When to skip subagents:**
- Single-language, small codebase
- Focused audit on specific file or module
- Quick sanity check (use quick detection commands instead)

## Related Skills

- [code-audit](../code-audit/SKILL.md): General code audit (includes race condition checks)
