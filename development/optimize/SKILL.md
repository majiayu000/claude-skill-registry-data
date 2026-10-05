---
name: optimize
description: "Analyzes code for performance bottlenecks and produces prioritized, actionable optimization recommendations with before/after code. Use before shipping performance-critical features or when code feels slow."
argument-hint: "[file, function, or 'all' for project-wide scan]"
allowed-tools: Read, Grep, Glob, Bash
---

# Performance Optimization Analysis

## Project Context
!`ls package.json requirements.txt go.mod Cargo.toml *.csproj pom.xml 2>/dev/null`
!`wc -l $(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.cs" -o -name "*.rb" \) -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" 2>/dev/null | head -5) 2>/dev/null | tail -1`

---

## Analysis Categories

Examine the specified code for issues in each category. For every issue found:
1. Show the **problematic code snippet** (with file:line)
2. Explain **why** it's a problem with complexity analysis
3. Show the **optimized version**
4. Rate **impact**: High / Medium / Low

### 1. Algorithmic Complexity
- O(n²) or worse loops that can be reduced
- Redundant iterations over the same data
- Sorting in loops (sort once, iterate many)
- Nested loops that can be replaced with hash maps/sets
- Unnecessary full-collection scans when early exit is possible

### 2. Database & I/O
- N+1 query patterns (loop of individual queries instead of batch)
- Missing database indexes for frequent queries
- Unbounded queries without LIMIT/pagination
- Sequential I/O that could be parallelized
- Missing connection pooling
- Redundant file reads (read once, use many)

### 3. Memory & Allocation
- Large object copies that could use references/pointers
- String concatenation in loops (use builder/buffer)
- Accumulating data in memory that could be streamed
- Memory leaks: event listeners not removed, subscriptions not cancelled
- Caching opportunities for expensive computations

### 4. Concurrency & Async
- Sequential `await` calls that could use `Promise.all` / `asyncio.gather` / goroutines
- Blocking the main thread/event loop with CPU-heavy work
- Missing cancellation for abandoned async operations
- Thread-safety issues with shared mutable state

### 5. Language-Specific
**JavaScript/TypeScript:**
- Unnecessary re-renders (missing React.memo, useMemo, useCallback)
- Barrel imports pulling in entire modules
- Missing tree-shaking opportunities
- Synchronous operations that should be async

**Python:**
- Using lists where sets/dicts provide O(1) lookup
- Not using generators for large sequences
- Global interpreter lock (GIL) bottlenecks
- Missing `__slots__` for memory-heavy classes

**Go:**
- Unnecessary goroutine creation
- Unbuffered channels causing blocking
- Excessive garbage collection from short-lived allocations

**General:**
- Missing HTTP caching headers
- Uncompressed API responses
- Missing lazy loading for heavy resources

---

## Output Format

### Findings Table

| # | File:Line | Issue | Impact | Category |
|---|-----------|-------|--------|----------|
| 1 | ... | ... | High | ... |

### Detailed Findings
For each finding, show before/after code.

### Top 3 Priority Actions
Rank the three most impactful optimizations to implement first, with estimated effort (S/M/L) and expected improvement.
