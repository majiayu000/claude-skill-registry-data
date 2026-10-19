---
name: javascript-development
description: >
  Develop, refactor, and review modern JavaScript (ES2022+) applications using
  standard ECMAScript features. Use when writing ES modules, managing async
  flows with Promises and async/await, understanding event loop microtasks,
  avoiding prototype and closure traps, or writing clean vanilla JavaScript.
compatibility: >
  Agent Skills-compatible coding agents operating on Node.js or browser
  JavaScript codebases.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "javascript, esm, async, promises, event-loop, ecmascript, nodejs"
  topics: "programming-languages, software-development"
---

# Modern JavaScript Development

Write clean, robust, and performant JavaScript using modern ECMAScript standards (ES2022+). Favor ES Modules (ESM), strict mode, asynchronous coordination with `async`/`await`, immutable state operations, and proper error boundaries.

## Core Rules

1. **Use ES Modules (ESM) by default**: Always use standard `import` and `export` rather than CommonJS `require()`.
2. **Always declare variables with `const` or `let`**: Never use `var`. Prefer `const` for immutability; use `let` only for reassigned loop or accumulator variables.
3. **Always use strict equality (`===` and `!==`)**: Never use loose equality (`==` or `!=`) to avoid unexpected type coercion.
4. **Never ignore unhandled Promise rejections**: Always handle Promise errors with `.catch()` or `try/catch` around `await`.
5. **Protect against `null` and `undefined` safely**: Use optional chaining (`?.`) and nullish coalescing (`??`) instead of truthiness hacks (`||`).
6. **Understand the Event Loop**: Keep microtasks short; never perform synchronous CPU loops that block the main thread.

---

## 1. Modern Syntax and Data Operations

### Optional Chaining and Nullish Coalescing
```javascript
// Safely access deeply nested properties
const port = config?.server?.port ?? 8080;

// Calling optional methods
user.logger?.info?.("Request received");
```

### Structured Clone & Immutability
Do not mutate function arguments or shared objects. Use `structuredClone()` for deep copies:

```javascript
// Deep clone nested objects and arrays
const deepCopy = structuredClone(originalState);

// Shallow updates with object spread
const updatedUser = {
  ...currentUser,
  lastLogin: new Date().toISOString(),
};
```

---

## 2. Asynchronous Programming and Promises

### `Promise.allSettled` vs `Promise.all`
- Use `Promise.all` when all operations must succeed (fails fast on first error).
- Use `Promise.allSettled` when operations are independent and you need to inspect all results:

```javascript
export async function syncServices(services) {
  const results = await Promise.allSettled(
    services.map(s => s.ping())
  );

  const healthy = results.filter(r => r.status === "fulfilled").map(r => r.value);
  const failures = results.filter(r => r.status === "rejected").map(r => r.reason);

  return { healthy, failures };
}
```

### Avoiding Async in Array Methods
Methods like `Array.prototype.forEach` do NOT await promises!

```javascript
// BUG: forEach does not await; requests run uncoordinated in background
// users.forEach(async user => await sendEmail(user));

// CORRECT: Use for...of loop for sequential execution
for (const user of users) {
  await sendEmail(user);
}

// OR Promise.all for concurrent execution
await Promise.all(users.map(user => sendEmail(user)));
```

---

## 3. Error Handling and Custom Errors

Extend `Error` and pass the underlying cause using the standard `cause` option (ES2022):

```javascript
export class ApiError extends Error {
  constructor(message, statusCode, options = {}) {
    super(message, options);
    this.name = "ApiError";
    this.statusCode = statusCode;
  }
}

export async function fetchUserData(userId) {
  try {
    const res = await fetch(`/api/users/${userId}`);
    if (!res.ok) {
      throw new ApiError(`HTTP request failed with status ${res.status}`, res.status);
    }
    return await res.json();
  } catch (err) {
    if (err instanceof ApiError) {
      throw err;
    }
    // Wrap low-level network failure with cause
    throw new ApiError(`Network failed while fetching user ${userId}`, 500, { cause: err });
  }
}
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `val || defaultValue` | Replaces valid `0`, `""`, or `false` with default | Use nullish coalescing: `val ?? defaultValue` |
| Floating promises without `await` or `.catch()` | Unhandled rejection crashes Node process | Always `await` or return promise chain |
| `== null` checks | Inadvertently coerces unrelated types | Use strict check: `val === null \|\| val === undefined` |
| Modifying `Array.prototype` | Global prototype pollution breaking third-party libraries | Never pollute built-in prototypes |
| Synchronous file I/O in web handlers | Freezes server event loop for all concurrent users | Use `fs.promises` / asynchronous methods |

---

## 5. Verification Checklist

- [ ] Zero usage of `var` in entire codebase.
- [ ] All Promise calls are handled with `await` or `.catch()`.
- [ ] No loose equality (`==` / `!=`).
- [ ] Error objects include meaningful error messages and original `cause`.
- [ ] Code passes ESLint/Prettier verification cleanly.
