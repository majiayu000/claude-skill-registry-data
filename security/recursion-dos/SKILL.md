---
name: recursion-dos
description: "Detect stack overflow and infinite recursion DoS in recursive parsers, tree walkers, and serializers that lack depth limits."
metadata:
  filePattern:
    - "**/*.js"
    - "**/*.ts"
    - "**/*.py"
    - "**/*.go"
  bashPattern:
    - "grep.*(recursive|recurse|depth|maxDepth)"
  priority: 80
---

# Recursion DoS Detection

## When to Use

Audit parsers, serializers, tree walkers, deep clone/merge functions, and any recursive function that processes user-controlled data structures with unbounded nesting depth.

## Key Distinction: OOM vs RangeError

| Crash Type | Severity | Catchable? | Process Dies? |
|------------|----------|------------|---------------|
| OOM (heap exhaustion) | HIGH 7.5 | NO | YES -- uncatchable, process killed |
| RangeError (stack overflow) | MEDIUM 5.3-6.5 | YES (try/catch) | Only if uncaught |

**OOM crash** = process dies regardless of error handling. This is HIGH severity.
**RangeError** = catchable in try/catch. Only HIGH if the library does NOT catch it.

## Process

### Step 1: Find Recursive Functions

```
grep -rn "function.*recurse\|function.*recursive\|function.*walk\|function.*traverse" .
grep -rn "function.*serialize\|function.*stringify\|function.*clone\|function.*deep" .
grep -rn "function.*parse\|function.*process\|function.*visit\|function.*transform" .
```

Look for functions that call themselves:
```
# Find function definitions and then check if they self-reference
grep -rn "function\s\+\w\+" . --include="*.js" | head -50
# Then for each function name, check if it calls itself
```

### Step 2: Check for Depth Limits

```
grep -rn "maxDepth\|max_depth\|depthLimit\|depth_limit\|MAX_DEPTH" .
grep -rn "depth\s*>\|depth\s*>=\|depth\s*<\|depth\s*<=" .
grep -rn "recursion.*limit\|stack.*limit\|nesting.*limit" .
```

### Step 3: Test with Nested Input

Create deeply nested input matching the data format:

```js
// JSON-like nesting
let nested = "x";
for (let i = 0; i < 100000; i++) {
  nested = { a: nested };
}

// String-based nesting
let nested = "a";
for (let i = 0; i < 100000; i++) {
  nested = "[" + nested + "]";
}
```

### Step 4: Measure Stack Consumption

```js
// Run in subprocess to avoid crashing main process
const { execSync } = require('child_process');
try {
  execSync('node -e "const pkg = require('./'); pkg.parse(payload)"', {
    timeout: 10000,
    maxBuffer: 1024
  });
} catch (e) {
  if (e.status === null) {
    console.log('[+] OOM: process killed (HIGH severity)');
  } else {
    console.log('[!] RangeError: catchable (MEDIUM severity)');
  }
}
```

## Common Vulnerable Patterns

### Pattern 1: Recursive Parser Without Depth Limit
```js
function parse(node) {
  if (node.children) {
    return node.children.map(child => parse(child)); // No depth limit
  }
  return node.value;
}
```

### Pattern 2: Recursive Serializer
```js
function serialize(obj) {
  if (typeof obj === 'object' && obj !== null) {
    return '{' + Object.keys(obj).map(k => k + ':' + serialize(obj[k])).join(',') + '}';
  }
  return String(obj);
}
```

### Pattern 3: Deep Clone Without Limit
```js
function deepClone(obj) {
  if (typeof obj !== 'object' || obj === null) return obj;
  const clone = Array.isArray(obj) ? [] : {};
  for (const key in obj) {
    clone[key] = deepClone(obj[key]); // Unbounded recursion
  }
  return clone;
}
```

### Pattern 4: Circular Reference (Infinite Loop)
Some recursive functions do not detect circular references:
```js
const a = {}; a.self = a;
deepClone(a); // Infinite recursion -> stack overflow
```

## CVSS Guidance

- OOM crash (process dies, unauthenticated): HIGH 7.5
- OOM crash (authenticated): MEDIUM 6.5
- RangeError (catchable but uncaught): HIGH 7.5
- RangeError (caught by library): LOW -- not a vulnerability
- Infinite loop (CPU DoS): MEDIUM 5.3

## References

- [Sinks](references/sinks.md) -- Recursive operation patterns
- [False Positive Indicators](references/false-positive-indicators.md)
- [PoC Skeleton](references/poc-skeleton.md)
