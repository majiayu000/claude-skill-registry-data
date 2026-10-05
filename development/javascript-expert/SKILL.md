---
name: javascript-expert
description: Deep JavaScript expertise for modern application development. Use when writing JavaScript code, implementing async patterns, working with closures and.
---

# JavaScript Expert

Specialized expertise in JavaScript programming, providing deep guidance on modern syntax and patterns, closures and the event loop, async programming, functional patterns, error handling, Node.js development, and runtime performance optimization.

## When to Use This Skill

Use this skill for:

- Writing modern JavaScript with ES2020+ features
- Implementing async/await and Promise-based patterns
- Understanding closures, scope chains, and the event loop
- Applying functional programming techniques
- Building robust error handling strategies
- Developing Node.js services and CLI tools
- Optimizing JavaScript runtime performance

**Trigger phrases**: "javascript", "js", "node.js", "async await", "promise", "closure", "event loop", "V8", "npm", "ES modules"

## What This Skill Does

Provides JavaScript expertise including:

- **Modern Syntax**: Destructuring, optional chaining, private fields, iterators
- **Closures and Scope**: Lexical scope, closure patterns, memory implications
- **Async Programming**: Promises, async/await, cancellation, error propagation
- **Functional Patterns**: Composition, currying, immutability, higher-order functions
- **Error Handling**: Custom errors, structured handling, debugging techniques
- **Node.js**: Streams, worker threads, EventEmitter, child processes
- **Performance**: V8 internals, memory profiling, lazy loading, Web Workers

## Instructions

### Step 1: Master Modern Syntax and Patterns

**Destructuring and Spread/Rest**:

```javascript
// Object destructuring with defaults and renaming
const { name, age = 25, address: { city } = {} } = user;

// Array destructuring with skip and rest
const [first, , third, ...remaining] = scores;

// Nested destructuring in function parameters
function createUser({ name, email, preferences: { theme = "dark", lang = "en" } = {} }) {
    return { name, email, theme, lang };
}

// Spread for shallow cloning and merging
const merged = { ...defaults, ...userConfig, timestamp: Date.now() };
const extended = [...baseItems, newItem, ...extraItems];
```

**Optional Chaining and Nullish Coalescing**:

```javascript
// Optional chaining for deep property access, method calls, and indexing
const street = user?.address?.street;
const firstScore = scores?.[0];
const result = callback?.();

// Nullish coalescing (only null/undefined, not 0 or "")
const port = config.port ?? 3000;
const theme = user?.preferences?.theme ?? "light";

// Logical assignment operators
options.timeout ??= 5000;       // Assign only if null/undefined
options.verbose ||= false;      // Assign only if falsy
options.retries &&= options.retries - 1; // Assign only if truthy
```

**Private Class Fields, Symbols, and Iterators**:

```javascript
// Private class fields and methods
class BankAccount {
    #balance = 0;

    constructor(initialBalance) { this.#balance = initialBalance; }

    deposit(amount) {
        this.#validateAmount(amount);
        this.#balance += amount;
    }

    get balance() { return this.#balance; }

    #validateAmount(amount) {
        if (typeof amount !== "number" || amount <= 0) {
            throw new TypeError("Amount must be a positive number");
        }
    }
}

// Symbols for unique property keys
const SERIALIZE = Symbol("serialize");
const TYPE_ID = Symbol.for("typeId"); // Global symbol registry

// Custom iterators with Symbol.iterator
class Range {
    constructor(start, end, step = 1) {
        this.start = start;
        this.end = end;
        this.step = step;
    }

    [Symbol.iterator]() {
        let current = this.start;
        const { end, step } = this;
        return {
            next() {
                if (current <= end) {
                    const value = current;
                    current += step;
                    return { value, done: false };
                }
                return { done: true };
            },
        };
    }
}

// Iterators work with for-of, spread, and destructuring
for (const n of new Range(1, 10, 2)) console.log(n); // 1, 3, 5, 7, 9
const values = [...new Range(0, 4)];                   // [0, 1, 2, 3, 4]
```

### Step 2: Understand Closures, Scope, and the Event Loop

**Lexical Scope and Closure Patterns**:

```javascript
// Closures capture the lexical environment, not a snapshot of values
function createCounter(initial = 0) {
    let count = initial;
    return {
        increment() { return ++count; },
        decrement() { return --count; },
        value()     { return count; },
    };
}

// Module pattern: closures encapsulate private state
function createCache(maxSize = 100) {
    const store = new Map();
    return {
        get(key) {
            const item = store.get(key);
            if (!item) return undefined;
            if (Date.now() > item.expiry) { store.delete(key); return undefined; }
            return item.value;
        },
        set(key, value, ttlMs = 60000) {
            if (store.size >= maxSize) store.delete(store.keys().next().value);
            store.set(key, { value, expiry: Date.now() + ttlMs });
        },
    };
}

// Closure pitfall: loop variable capture
for (var i = 0; i < 5; i++) {
    setTimeout(() => console.log(i), 100); // Prints 5 five times (var is function-scoped)
}
for (let i = 0; i < 5; i++) {
    setTimeout(() => console.log(i), 100); // Prints 0, 1, 2, 3, 4 (let is block-scoped)
}

// Memory management: extract only what you need to avoid retaining large objects
function createHandler(heavyData) {
    const length = heavyData.length; // Capture the scalar, not the entire object
    return () => console.log(length);
}
```

**Event Loop, Microtasks, and Macrotasks**:

```javascript
// Execution order: synchronous > microtasks > macrotasks
console.log("1: synchronous");
setTimeout(() => console.log("2: macrotask (setTimeout)"), 0);
Promise.resolve().then(() => console.log("3: microtask (Promise.then)"));
queueMicrotask(() => console.log("4: microtask (queueMicrotask)"));
console.log("5: synchronous");
// Output: 1, 5, 3, 4, 2

// Microtask starvation: recursive microtasks block macrotasks indefinitely
function floodMicrotasks() {
    let count = 0;
    function addMore() {
        if (++count < 1000) queueMicrotask(addMore);
    }
    queueMicrotask(addMore);
}
```

### Step 3: Master Async Patterns

**Promises and async/await Fundamentals**:

```javascript
// Wrapping callback APIs in Promises
function fetchUserData(userId) {
    return new Promise((resolve, reject) => {
        if (!userId) { reject(new Error("userId is required")); return; }
        database.query("SELECT * FROM users WHERE id = ?", [userId], (err, rows) => {
            if (err) reject(err); else resolve(rows[0]);
        });
    });
}

// async/await with proper error handling
async function getUserProfile(userId) {
    try {
        const user = await fetchUserData(userId);
        return { ...user, preferences: await fetchPreferences(user.id) };
    } catch (error) {
        if (error.code === "NOT_FOUND") return null;
        throw error;
    }
}

// Parallel execution with Promise.all
const [user, posts, notifs] = await Promise.all([
    getUser(userId), getPosts(userId), getNotifications(userId),
]);
```

**Promise Combinators and Cancellation**:

```javascript
// Promise.allSettled: wait for all, regardless of outcome
async function batchProcess(items) {
    const results = await Promise.allSettled(items.map(item => processItem(item)));
    const succeeded = results.filter(r => r.status === "fulfilled").map(r => r.value);
    const failed = results.filter(r => r.status === "rejected").map(r => r.reason);
    return { succeeded, failed };
}

// Promise.race + AbortController for timeout
async function fetchWithTimeout(url, ms = 5000) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), ms);
    try { return await fetch(url, { signal: ctrl.signal }); }
    finally { clearTimeout(timer); }
}

// Promise.any: first to fulfill wins; throws AggregateError if all fail
const fastest = await Promise.any(
    ["mirror1", "mirror2"].map(h => fetch(`https://${h}.example.com/data`))
);

// Async iterators for paginated APIs
async function* paginate(baseUrl) {
    let page = 1, hasMore = true;
    while (hasMore) {
        const { items, hasNextPage } = await fetch(`${baseUrl}?page=${page}`).then(r => r.json());
        yield* items;
        hasMore = hasNextPage;
        page++;
    }
}
for await (const item of paginate("/api/records")) await processItem(item);
```

### Step 4: Apply Functional Programming Patterns

**Higher-Order Functions and Composition**:

```javascript
// Higher-order function: retry wrapper with linear backoff
function withRetry(fn, retries = 3, delayMs = 1000) {
    return async (...args) => {
        let lastErr;
        for (let i = 1; i <= retries; i++) {
            try { return await fn(...args); }
            catch (e) { lastErr = e; if (i < retries) await new Promise(r => setTimeout(r, delayMs * i)); }
        }
        throw lastErr;
    };
}

// Function composition pipelines
const pipe = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);

const processUser = pipe(normalizeEmail, validateAge, assignDefaultRole, formatForStorage);
const user = processUser(rawInput);

// Async pipe for promise-returning functions
const pipeAsync = (...fns) => (x) =>
    fns.reduce((acc, fn) => acc.then(fn), Promise.resolve(x));

const processOrder = pipeAsync(validateOrder, calculateTax, applyDiscount, chargePayment);
await processOrder(orderData);
```

**Immutability, Currying, and Pure Functions**:

```javascript
// Immutable updates with spread
function updateUser(user, changes) {
    return Object.freeze({ ...user, ...changes, updatedAt: Date.now() });
}

// Immutable array operations (no mutations)
const addItem = (arr, item) => [...arr, item];
const removeAt = (arr, index) => [...arr.slice(0, index), ...arr.slice(index + 1)];
const updateAt = (arr, index, fn) => arr.map((item, i) => (i === index ? fn(item) : item));

// Generic curry function
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) return fn(...args);
        return (...moreArgs) => curried(...args, ...moreArgs);
    };
}

const multiply = curry((a, b) => a * b);
const double = multiply(2);
const triple = multiply(3);
double(5); // 10

// Practical currying: reusable configuration
const createLogger = curry((level, prefix, message) => {
    console.log(`[${level}] ${prefix}: ${message}`);
});
const apiError = createLogger("ERROR")("API");
apiError("Connection refused"); // [ERROR] API: Connection refused
```

### Step 5: Implement Robust Error Handling and Debugging

**Custom Error Classes and Structured Handling**:

```javascript
// Custom error hierarchy
class AppError extends Error {
    constructor(message, { code = "UNKNOWN", statusCode = 500, context = {} } = {}) {
        super(message);
        this.name = this.constructor.name;
        this.code = code;
        this.statusCode = statusCode;
        this.context = context;
        if (Error.captureStackTrace) Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends AppError {
    constructor(message, fields = []) {
        super(message, { code: "VALIDATION_ERROR", statusCode: 400 });
        this.fields = fields;
    }
}

class NotFoundError extends AppError {
    constructor(resource, id) {
        super(`${resource} with id ${id} not found`, {
            code: "NOT_FOUND", statusCode: 404, context: { resource, id },
        });
    }
}

// Express-style error handling middleware
function errorHandler(err, req, res, next) {
    if (err instanceof AppError) {
        return res.status(err.statusCode).json({
            error: { code: err.code, message: err.message },
        });
    }
    console.error("Unexpected error:", err);
    res.status(500).json({ error: { code: "INTERNAL_ERROR", message: "An unexpected error occurred" } });
}
```

**Debugging Techniques**:

```javascript
// Structured logger with child context
function createLogger(base = {}) {
    const emit = (level, msg, ctx = {}) =>
        console[level === "error" ? "error" : "log"](JSON.stringify({ ts: new Date().toISOString(), level, msg, ...base, ...ctx }));
    return {
        info: (m, c) => emit("info", m, c),
        error: (m, c) => emit("error", m, c),
        child: (ctx) => createLogger({ ...base, ...ctx }),
    };
}

const reqLog = createLogger({ service: "api" }).child({ requestId: "abc-123" });
reqLog.info("Processing request", { path: "/users" });

// Performance measurement via the Performance API
function measureSync(label, fn) {
    performance.mark(`${label}-start`);
    const result = fn();
    performance.mark(`${label}-end`);
    performance.measure(label, `${label}-start`, `${label}-end`);
    return result;
}
```

### Step 6: Build with Node.js Patterns

**Streams for Efficient Data Processing**:

```javascript
import { createReadStream, createWriteStream } from "node:fs";
import { Transform, pipeline } from "node:stream";
import { promisify } from "node:util";

const pipelineAsync = promisify(pipeline);

// Custom transform stream
class LineTransform extends Transform {
    #buffer = "";

    _transform(chunk, encoding, callback) {
        this.#buffer += chunk.toString();
        const lines = this.#buffer.split("\n");
        this.#buffer = lines.pop(); // Keep incomplete last line
        for (const line of lines) {
            if (line.trim()) this.push(line.trim() + "\n");
        }
        callback();
    }

    _flush(callback) {
        if (this.#buffer.trim()) this.push(this.#buffer.trim() + "\n");
        callback();
    }
}

// Composable pipeline
async function processLargeFile(inputPath, outputPath) {
    await pipelineAsync(
        createReadStream(inputPath, { encoding: "utf-8" }),
        new LineTransform(),
        new Transform({
            transform(chunk, enc, cb) {
                cb(null, JSON.stringify({ line: chunk.toString().trim() }) + "\n");
            },
        }),
        createWriteStream(outputPath),
    );
}
```

**Worker Threads and EventEmitter**:

```javascript
import { Worker, isMainThread, parentPort, workerData } from "node:worker_threads";
import { cpus } from "node:os";

if (isMainThread) {
    function runWorker(data) {
        return new Promise((resolve, reject) => {
            const worker = new Worker(new URL(import.meta.url), { workerData: data });
            worker.on("message", resolve);
            worker.on("error", reject);
        });
    }

    async function parallelProcess(items) {
        const numWorkers = Math.min(cpus().length, items.length);
        const chunkSize = Math.ceil(items.length / numWorkers);
        const chunks = Array.from({ length: numWorkers }, (_, i) =>
            items.slice(i * chunkSize, (i + 1) * chunkSize)
        );
        return (await Promise.all(chunks.map(runWorker))).flat();
    }
} else {
    parentPort.postMessage(workerData.map(item => heavyComputation(item)));
}

// EventEmitter for decoupled communication
import { EventEmitter } from "node:events";

class TaskQueue extends EventEmitter {
    #queue = [];
    #processing = false;

    add(task) {
        this.#queue.push(task);
        this.emit("taskAdded", { queueLength: this.#queue.length });
        this.#drain();
    }

    async #drain() {
        if (this.#processing || this.#queue.length === 0) return;
        this.#processing = true;
        const batch = this.#queue.splice(0, 5);
        const results = await Promise.allSettled(batch.map(t => t()));
        this.emit("batchComplete", results);
        this.#processing = false;
        if (this.#queue.length > 0) this.#drain();
    }
}

// Promisified child process execution
import { execFile } from "node:child_process";
import { promisify } from "node:util";
const execFileAsync = promisify(execFile);
const { stdout } = await execFileAsync("git", ["status"], { timeout: 30000 });
```

### Step 7: Optimize Runtime Performance

**V8 Optimizations and Memory Profiling**:

```javascript
// Monomorphic functions: V8 optimizes functions called with consistent types
function addNumbers(a, b) { return a + b; }
addNumbers(1, 2); // V8 optimizes for number + number
addNumbers(3, 4); // Same types: stays optimized
// Calling with strings forces deoptimization; keep call sites type-consistent

// Hidden classes: always create objects with properties in the same order
function createPoint(x, y) { return { x, y }; } // Consistent shape = one hidden class

// Object pooling to reduce GC pressure
class ObjectPool {
    #pool = [];
    #factory;
    #reset;

    constructor(factory, reset, initialSize = 10) {
        this.#factory = factory;
        this.#reset = reset;
        for (let i = 0; i < initialSize; i++) this.#pool.push(factory());
    }

    acquire() { return this.#pool.pop() ?? this.#factory(); }
    release(obj) { this.#reset(obj); this.#pool.push(obj); }
}

const vectorPool = new ObjectPool(
    () => ({ x: 0, y: 0, z: 0 }),
    (v) => { v.x = 0; v.y = 0; v.z = 0; },
);
```

**Lazy Loading, Web Workers, and Advanced Memory APIs**:

```javascript
// Lazy loading with dynamic import
async function loadFeature(name) {
    const loaders = {
        chart: () => import("./features/chart.js"),
        editor: () => import("./features/editor.js"),
    };
    const loader = loaders[name];
    if (!loader) throw new Error(`Unknown feature: ${name}`);
    return (await loader()).default;
}

// LRU memoization with bounded Map (Map preserves insertion order)
function memoize(fn, maxSize = 100) {
    const cache = new Map();
    return (...args) => {
        const key = JSON.stringify(args);
        if (cache.has(key)) { const v = cache.get(key); cache.delete(key); cache.set(key, v); return v; }
        const result = fn(...args);
        if (cache.size >= maxSize) cache.delete(cache.keys().next().value);
        cache.set(key, result);
        return result;
    };
}

// Web Workers for offloading heavy computation (browser)
function runInWorker(fn, data) {
    return new Promise((resolve, reject) => {
        const blob = new Blob(
            [`self.onmessage = e => self.postMessage((${fn.toString()})(e.data))`],
            { type: "application/javascript" },
        );
        const worker = new Worker(URL.createObjectURL(blob));
        worker.onmessage = (e) => { resolve(e.data); worker.terminate(); };
        worker.onerror = (e) => { reject(e); worker.terminate(); };
        worker.postMessage(data);
    });
}

const sorted = await runInWorker(data => data.sort((a, b) => a - b), largeArray);

// SharedArrayBuffer for zero-copy shared memory
const shared = new SharedArrayBuffer(1024);
const view = new Int32Array(shared);
Atomics.add(view, 0, 1);      // Atomic increment
Atomics.load(view, 0);        // Atomic read
Atomics.store(view, 0, 42);   // Atomic write

// WeakRef and FinalizationRegistry for GC-aware caches
const registry = new FinalizationRegistry((key) => console.log(`"${key}" was collected`));

function weakCache() {
    const entries = new Map();
    return {
        set(key, val) { entries.set(key, new WeakRef(val)); registry.register(val, key); },
        get(key) {
            const ref = entries.get(key);
            if (!ref) return undefined;
            const val = ref.deref();
            if (!val) { entries.delete(key); return undefined; }
            return val;
        },
    };
}
```

## Best Practices

- **Use `const` by default** - Only use `let` when reassignment is necessary; never use `var`
- **Prefer async/await over raw Promises** - Clearer control flow and easier error handling
- **Handle all Promise rejections** - Unhandled rejections crash Node.js by default
- **Avoid blocking the event loop** - Offload CPU-intensive work to worker threads
- **Keep functions pure when possible** - Pure functions are easier to test, cache, and compose
- **Use structured cloning over JSON round-trips** - `structuredClone()` handles more types and is faster
- **Prefer `for...of` over `forEach`** - It supports `break`, `continue`, and `await`
- **Use `Map` and `Set` over plain objects for collections** - Better performance for frequent additions and deletions

## Common Patterns

### Pattern 1: Retry with Exponential Backoff

```javascript
async function retryWithBackoff(fn, { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = {}) {
    let lastError;
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            return await fn();
        } catch (error) {
            lastError = error;
            if (attempt === maxRetries) break;
            const delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
            await new Promise(resolve => setTimeout(resolve, delay * (0.5 + Math.random() * 0.5)));
        }
    }
    throw lastError;
}
```

### Pattern 2: Pub/Sub Event Bus

```javascript
function createEventBus() {
    const listeners = new Map();
    return {
        on(event, handler) {
            if (!listeners.has(event)) listeners.set(event, new Set());
            listeners.get(event).add(handler);
            return () => listeners.get(event)?.delete(handler);
        },
        emit(event, data) {
            for (const handler of listeners.get(event) ?? []) {
                try { handler(data); } catch (err) { console.error(`Event handler error [${event}]:`, err); }
            }
        },
        once(event, handler) {
            const unsub = this.on(event, (data) => { unsub(); handler(data); });
            return unsub;
        },
    };
}
```

## Quality Checklist

- [ ] No `var` declarations; `const` by default, `let` only when needed
- [ ] All Promises have `.catch()` or are inside try/catch
- [ ] No `any` types (if using JSDoc or TypeScript)
- [ ] Event listeners are cleaned up (removeEventListener, AbortController)
- [ ] Large data is processed with streams, not loaded into memory at once
- [ ] CPU-intensive work is offloaded to worker threads
- [ ] Error classes extend a common base with structured codes
- [ ] ESLint passes with no warnings

## Related Skills

- `performance-testing` - JavaScript benchmarking and profiling
- `cicd-architect` - Node.js CI/CD pipelines
- `code-quality` - JavaScript code standards
- `kubernetes-expert` - Node.js microservices on K8s

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: MDN Web Docs, Node.js best practices, V8 optimization guides


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
