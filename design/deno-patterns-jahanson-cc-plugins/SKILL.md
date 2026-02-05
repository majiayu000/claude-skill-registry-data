---
name: deno-patterns
description: "Modern TypeScript patterns and migration guidance for Deno: resource management with 'using', async generators, error handling, and Web Standard APIs. Use when migrating from Node.js, implementing cleanup logic, or learning modern JS/TS patterns."
---

# Deno Modern Patterns & Migration

## When to Use This Skill

Use this skill when:
- Migrating from Node.js to Deno
- Learning modern JavaScript/TypeScript patterns
- Implementing resource management
- Working with timers, polling, or cleanup logic
- Handling errors in Deno
- Choosing between old and new patterns

**Note:** Always read `deno-core.md` first for essential configuration and practices.

---

## Resource Management with `using`

### The Problem with Manual Cleanup

**Old Pattern:**

```javascript
// Manual timer cleanup - error-prone
const id = setInterval(() => {
  console.log("Tick!");
}, 1000);

// Later, cleanup (easy to forget!)
clearInterval(id);
```

**Problems:**
- Resource leaks if cleanup is missed
- Not exception-safe
- Resource not tied to lexical scope
- Cleanup code separated from acquisition

### The `using` Statement (Deno >= v2.4)

**New Pattern:**

```typescript
// Automatic, exception-safe cleanup
class Timer {
  #handle: number;

  constructor(cb: () => void, ms: number) {
    this.#handle = setInterval(cb, ms);
  }

  [Symbol.dispose]() {
    clearInterval(this.#handle);
    console.log("Timer disposed");
  }
}

using timer = new Timer(() => {
  console.log("Tick!");
}, 1000);
// Timer automatically cleaned up at end of scope
```

**Benefits:**
- Automatic cleanup at scope exit
- Exception-safe (cleanup happens even if errors occur)
- Follows RAII (Resource Acquisition Is Initialization) principles
- Prevents resource leaks in complex control flows
- Composable with multiple `using` declarations

### Async Resource Management

For async cleanup, use `await using` with `Symbol.asyncDispose`:

```typescript
class DatabaseConnection {
  #conn: Connection;

  constructor(conn: Connection) {
    this.#conn = conn;
  }

  async [Symbol.asyncDispose]() {
    await this.#conn.close();
    console.log("Database connection closed");
  }
}

// Automatically closes when scope exits
await using db = new DatabaseConnection(conn);
await db.query("SELECT * FROM users");
// Connection closed here, even if query throws
```

### When to Use `using`

Use `using` for any resource that needs cleanup:
- Timers (setInterval, setTimeout)
- File handles
- Database connections
- Network connections
- Locks and mutexes
- Any object with teardown logic

---

## Async Iteration Over Polling

### The Problem with Traditional Polling

**Old Pattern:**

```javascript
// Traditional polling - not cancelable, drift-prone
let running = true;

function poll() {
  if (!running) return;
  // ...check something...
  setTimeout(poll, 1000);
}

poll();
running = false;  // Unreliable cancellation
```

**Problems:**
- Timer drift accumulates over time
- Race conditions with cancellation flag
- Hard to compose or integrate with other async code
- Not part of the structured concurrency model

### Async Generators for Polling

**New Pattern:**

```typescript
// Async generator - naturally cancelable
async function* interval(ms: number) {
  while (true) {
    yield;
    await new Promise((r) => setTimeout(r, ms));
  }
}

// Usage with for-await-of
for await (const _ of interval(1000)) {
  // ...do work...
  if (shouldStop()) break;  // Clean, immediate cancellation
}
```

**Benefits:**
- Natural cancellation by breaking the loop
- No timer drift - explicit timing control
- Composable with Promise.race, yield*, etc.
- Integrates with all async iterable APIs
- Clear control flow

### Advanced Polling Patterns

**Polling with timeout:**

```typescript
async function* intervalWithTimeout(intervalMs: number, timeoutMs: number) {
  const startTime = Date.now();

  while (Date.now() - startTime < timeoutMs) {
    yield;
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}

for await (const _ of intervalWithTimeout(1000, 10000)) {
  // Polls every 1s, stops after 10s
  await checkCondition();
}
```

---

## Async/Promise Best Practices

### Remove Unnecessary `async`

**Incorrect:**

```typescript
// BAD - Unnecessary async wrapper
async function validateMemory(content: string): boolean {
  if (content.trim().length === 0) {
    throw new Error("Content cannot be empty");
  }
  return true;
}
```

**Correct:**

```typescript
// GOOD - No async needed
function validateMemory(content: string): boolean {
  if (content.trim().length === 0) {
    throw new Error("Content cannot be empty");
  }
  return true;
}
```

### Interface Compliance with Promise.resolve()

When implementing an interface that requires `Promise<T>` but your logic is synchronous:

```typescript
interface QueueMessageHandler {
  handle(message: QueueMessage): Promise<void>;
}

// GOOD - Return Promise.resolve() explicitly
class SyncMessageHandler implements QueueMessageHandler {
  handle(message: QueueMessage): Promise<void> {
    this.processSync(message);
    return Promise.resolve();
  }
}

// GOOD - Return Promise.reject() for errors
class ValidatingHandler implements QueueMessageHandler {
  handle(message: QueueMessage): Promise<void> {
    if (message.corrupted) {
      return Promise.reject(new Error("Message corrupted"));
    }
    return Promise.resolve();
  }
}
```

### Only Use `async` When You Actually `await`

```typescript
// GOOD - async because we await
async function processMemory(content: string): Promise<ProcessedMemory> {
  const embedding = await ollama.generateEmbedding(content);
  const entities = await ollama.extractEntities(content);
  return { content, embedding, entities };
}

// GOOD - no async because no await
function validateConfig(config: Config): boolean {
  return config.apiKey !== undefined;
}
```

---

## Error Handling

### Deno's Class-Based Errors

**Old Pattern (Node.js):**

```javascript
// String-based error codes
try {
  fs.readFileSync('file');
} catch (err) {
  if (err.code === 'ENOENT') {
    // handle not found
  }
}
```

**New Pattern (Deno):**

```typescript
// Type-safe error classes
try {
  await Deno.readTextFile("file.txt");
} catch (err) {
  if (err instanceof Deno.errors.NotFound) {
    // handle not found
  } else if (err instanceof Deno.errors.PermissionDenied) {
    // handle permission error
  }
}
```

### Available Deno Error Classes

```typescript
Deno.errors.NotFound
Deno.errors.PermissionDenied
Deno.errors.ConnectionRefused
Deno.errors.ConnectionReset
Deno.errors.ConnectionAborted
Deno.errors.NotConnected
Deno.errors.AddrInUse
Deno.errors.AddrNotAvailable
Deno.errors.BrokenPipe
Deno.errors.AlreadyExists
Deno.errors.InvalidData
Deno.errors.TimedOut
Deno.errors.Interrupted
Deno.errors.WriteZero
Deno.errors.UnexpectedEof
Deno.errors.BadResource
Deno.errors.Busy
```

### Error Handling Best Practices

```typescript
// Specific error handling
async function loadConfig(path: string): Promise<Config> {
  try {
    const content = await Deno.readTextFile(path);
    return JSON.parse(content);
  } catch (err) {
    if (err instanceof Deno.errors.NotFound) {
      throw new Error(`Config file not found: ${path}`);
    } else if (err instanceof Deno.errors.PermissionDenied) {
      throw new Error(`Permission denied reading config: ${path}`);
    } else if (err instanceof SyntaxError) {
      throw new Error(`Invalid JSON in config: ${path}`);
    }
    throw err;  // Re-throw unknown errors
  }
}
```

**Benefits:**
- Type-safe - no magic string codes
- Better IDE autocomplete
- Easier refactoring
- Clear error hierarchies

---

## Web-Standard APIs

### HTTP Server

**Old (Node.js):**

```javascript
// Node.js style
const http = require("http");
http.createServer((req, res) => {
  res.writeHead(200);
  res.end("OK");
}).listen(8000);
```

**New (Deno):**

```typescript
// Deno - serverless-compatible
Deno.serve((req) => new Response("OK"));
```

**Benefits:**
- Simpler, cleaner API
- Native Request/Response objects
- Works with serverless platforms
- No legacy API constraints

### File Operations

**Old (Node.js):**

```javascript
// Node.js callbacks
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});
```

**New (Deno):**

```typescript
// Deno - async/await
const data = await Deno.readTextFile("file.txt");
console.log(data);
```

### Fetch API

Deno has native `fetch()` with no imports needed:

```typescript
// Native fetch - no imports
const response = await fetch("https://api.example.com/data");
const data = await response.json();
```

### Streams

Use Web Streams API:

```typescript
// Web Streams
const file = await Deno.open("large-file.txt");
const readable = file.readable;

for await (const chunk of readable) {
  // Process chunk
}
```

### Crypto

Use Web Crypto API:

```typescript
// Web Crypto
const data = new TextEncoder().encode("hello");
const hashBuffer = await crypto.subtle.digest("SHA-256", data);
const hashArray = Array.from(new Uint8Array(hashBuffer));
const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
```

---

## Standard Library Utilities

### Path Operations

```typescript
import { join, dirname, basename } from "@std/path";

const fullPath = join("/users", "alice", "documents", "file.txt");
const dir = dirname(fullPath);  // /users/alice/documents
const file = basename(fullPath);  // file.txt
```

### File System

```typescript
import { ensureDir, exists } from "@std/fs";

// Ensure directory exists
await ensureDir("./data/cache");

// Check if file exists
if (await exists("config.json")) {
  // ...
}
```

### Time-Based Identifiers

Use `@std/ulid` for sortable IDs:

```typescript
import { ulid } from "@std/ulid";

// Generate ULID (sortable by creation time)
const id = ulid();  // 01ARZ3NDEKTSV4RRFFQ69G5FAV

// ULIDs are lexicographically sortable by time
const ids = [ulid(), ulid(), ulid()];
ids.sort();  // Automatically sorted by creation time
```

**When to use ULID:**
- Need UUID-like identifiers sortable by time
- Want to avoid UUID v4 random collisions
- Need efficient database indexing by creation time
- Want to extract timestamp from ID

---

## Pattern Migration Guide

### Quick Reference

| Use Case         | Old Pattern                        | Modern (Deno) Pattern                      |
|------------------|------------------------------------|--------------------------------------------|
| Timer            | `setInterval` + `clearInterval`    | `using` + class w/ `Symbol.dispose`        |
| Polling          | Repeated `setTimeout`              | Async generator (`for await...of`)         |
| Cleanup          | Manual try/finally                 | `using`/`await using`                      |
| Error Handling   | `if (err.code === ...)`            | `if (err instanceof Deno.errors.*)`        |
| HTTP Server      | `http.createServer`                | `Deno.serve`                               |
| File Reading     | `fs.readFileSync`                  | `await Deno.readTextFile`                  |
| Environment Vars | `process.env.VAR`                  | `Deno.env.get("VAR")`                      |
| Module Format    | CommonJS (`require`)               | ESM (`import`)                             |

### Migration Examples

**Timer Management:**

```typescript
// Old:
const id = setInterval(doWork, 1000);
// ... later ...
clearInterval(id);

// New:
class Timer {
  #id;
  constructor(cb, ms) { this.#id = setInterval(cb, ms); }
  [Symbol.dispose]() { clearInterval(this.#id); }
}
using t = new Timer(doWork, 1000);
// Automatically disposed at end of scope
```

**Async Polling:**

```typescript
// Old:
let running = true;
const poll = () => {
  if (!running) return;
  doWork();
  setTimeout(poll, 1000);
};
poll();
running = false;  // To stop

// New:
async function* poller(ms) {
  while (true) {
    yield;
    await new Promise(r => setTimeout(r, ms));
  }
}
for await (const _ of poller(1000)) {
  doWork();
  if (shouldStop()) break;  // Natural cancellation
}
```

**File Operations:**

```typescript
// Old (Node.js):
const fs = require('fs');
const data = fs.readFileSync('file.txt', 'utf8');

// New (Deno):
const data = await Deno.readTextFile("file.txt");
```

**Environment Variables:**

```typescript
// Old (Node.js):
const apiKey = process.env.API_KEY;

// New (Deno):
const apiKey = Deno.env.get("API_KEY");
// Requires: --allow-env=API_KEY
```

---

## Structured Concurrency

### AbortController for Cancellation

```typescript
async function fetchWithTimeout(url: string, timeoutMs: number): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

// Usage:
try {
  const response = await fetchWithTimeout("https://slow-api.com", 5000);
} catch (err) {
  if (err.name === 'AbortError') {
    console.log("Request timed out");
  }
}
```

### Racing Multiple Promises

```typescript
// First successful response wins
const response = await Promise.race([
  fetch("https://api1.com/data"),
  fetch("https://api2.com/data"),
  fetch("https://api3.com/data"),
]);

// All must succeed
const [user, posts, comments] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
  fetchComments(id),
]);
```

---

## Performance Considerations

### Resource Management

**No Runtime Overhead:**
- `using` has no performance penalty vs manual cleanup
- More robust in exception paths
- Prevents resource leaks that degrade performance

### Async Generators

**Minimal Overhead:**
- Async generators are efficient
- No additional allocations per iteration
- Better than callback-based patterns

### Type-Only Imports

**Build-Time Optimization:**

```typescript
// GOOD - Erased at runtime
import type { User } from "./types.ts";

// BAD - Bundled even if only used for types
import { User } from "./types.ts";
```

---

## Summary: Modern Pattern Principles

1. **Use `using` for any resource needing cleanup**
2. **Prefer async generators over polling loops**
3. **Remove `async` if no `await` is present**
4. **Use Promise.resolve() for interface compliance**
5. **Handle errors with Deno's class-based system**
6. **Prefer Web Standard APIs over Node.js patterns**
7. **Use AbortController for cancellable operations**
8. **Leverage @std library for common operations**
9. **Use ULID for time-based sortable IDs**
10. **Always prefer structured, composable patterns**

---

## Additional Resources

- **TC39 Explicit Resource Management:** https://github.com/tc39/proposal-explicit-resource-management
- **Deno Web APIs:** https://docs.deno.com/runtime/manual/runtime/web_platform_apis
- **Async Iterators:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/asyncIterator
