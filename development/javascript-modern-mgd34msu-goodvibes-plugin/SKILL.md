---
name: javascript-modern
description: Implements modern JavaScript features from ES2020-ES2024 including optional chaining, nullish coalescing, private fields, Promise methods, and array transformations. Use when modernizing JavaScript code, using ES2024 features, or when user asks about latest ECMAScript standards.
---

# Modern JavaScript (ES2020-ES2024)

Latest ECMAScript features for cleaner, more expressive code.

## ES2024 Features

### Object.groupBy / Map.groupBy

```javascript
const products = [
  { name: 'Apple', category: 'fruit', price: 1.5 },
  { name: 'Banana', category: 'fruit', price: 0.75 },
  { name: 'Carrot', category: 'vegetable', price: 0.5 },
  { name: 'Broccoli', category: 'vegetable', price: 2.0 },
];

// Group into object
const byCategory = Object.groupBy(products, (item) => item.category);
// {
//   fruit: [{ name: 'Apple', ... }, { name: 'Banana', ... }],
//   vegetable: [{ name: 'Carrot', ... }, { name: 'Broccoli', ... }]
// }

// Group into Map (preserves non-string keys)
const byPriceRange = Map.groupBy(products, (item) =>
  item.price >= 1 ? 'expensive' : 'cheap'
);
// Map { 'expensive' => [...], 'cheap' => [...] }

// Complex grouping
const users = [
  { name: 'Alice', role: 'admin', active: true },
  { name: 'Bob', role: 'user', active: false },
  { name: 'Charlie', role: 'admin', active: false },
];

const groupedUsers = Object.groupBy(users, (user) =>
  `${user.role}-${user.active ? 'active' : 'inactive'}`
);
```

### Promise.withResolvers()

```javascript
// Before: Awkward pattern
let resolve, reject;
const promise = new Promise((res, rej) => {
  resolve = res;
  reject = rej;
});

// After: Clean extraction
const { promise, resolve, reject } = Promise.withResolvers();

// Practical example: Timeout wrapper
function timeout(ms) {
  const { promise, resolve } = Promise.withResolvers();
  setTimeout(resolve, ms);
  return promise;
}

// Event-based promise
function waitForClick(element) {
  const { promise, resolve } = Promise.withResolvers();
  element.addEventListener('click', resolve, { once: true });
  return promise;
}

// Cancellable fetch
function cancellableFetch(url) {
  const { promise, resolve, reject } = Promise.withResolvers();
  const controller = new AbortController();

  fetch(url, { signal: controller.signal })
    .then(resolve)
    .catch(reject);

  return {
    promise,
    cancel: () => controller.abort(),
  };
}
```

### Immutable Array Methods

```javascript
const numbers = [3, 1, 4, 1, 5, 9];

// toSorted() - Returns new sorted array
const sorted = numbers.toSorted((a, b) => a - b);
// sorted: [1, 1, 3, 4, 5, 9]
// numbers: [3, 1, 4, 1, 5, 9] (unchanged)

// toReversed() - Returns new reversed array
const reversed = numbers.toReversed();
// reversed: [9, 5, 1, 4, 1, 3]

// toSpliced() - Returns new spliced array
const spliced = numbers.toSpliced(2, 1, 100, 200);
// spliced: [3, 1, 100, 200, 1, 5, 9]

// with() - Returns new array with element replaced
const replaced = numbers.with(0, 999);
// replaced: [999, 1, 4, 1, 5, 9]

// Chaining immutable operations
const result = numbers
  .toSorted((a, b) => b - a)
  .toSpliced(0, 2)
  .with(0, 0);
```

### Set Methods

```javascript
const setA = new Set([1, 2, 3, 4]);
const setB = new Set([3, 4, 5, 6]);

// Union - All elements from both sets
const union = setA.union(setB);
// Set { 1, 2, 3, 4, 5, 6 }

// Intersection - Elements in both sets
const intersection = setA.intersection(setB);
// Set { 3, 4 }

// Difference - Elements in A but not in B
const difference = setA.difference(setB);
// Set { 1, 2 }

// Symmetric Difference - Elements in either but not both
const symmetricDiff = setA.symmetricDifference(setB);
// Set { 1, 2, 5, 6 }

// Subset/Superset checks
const subset = new Set([2, 3]);
subset.isSubsetOf(setA);       // true
setA.isSupersetOf(subset);     // true
setA.isDisjointFrom(new Set([7, 8])); // true
```

### RegExp /v Flag (Unicode Sets)

```javascript
// Match any emoji
const emojiPattern = /\p{Emoji}/v;
emojiPattern.test('Hello 👋'); // true

// Set operations in regex
const greekOrCyrillic = /[\p{Script=Greek}--\p{Letter}]/v;

// String properties
const pattern = /^\p{RGI_Emoji}$/v;
pattern.test('👨‍👩‍👧‍👦'); // true (family emoji)
```

## ES2023 Features

### Array findLast / findLastIndex

```javascript
const numbers = [1, 2, 3, 4, 5, 4, 3];

// Find from end
const lastEven = numbers.findLast(n => n % 2 === 0);
// 4 (the second occurrence)

const lastEvenIndex = numbers.findLastIndex(n => n % 2 === 0);
// 5

// Practical: Find most recent matching item
const logs = [
  { level: 'info', message: 'Started' },
  { level: 'error', message: 'Failed' },
  { level: 'info', message: 'Retry' },
  { level: 'error', message: 'Failed again' },
];

const lastError = logs.findLast(log => log.level === 'error');
// { level: 'error', message: 'Failed again' }
```

### Hashbang Grammar

```javascript
#!/usr/bin/env node
// Valid at start of file
console.log('Script executed directly');
```

### WeakMap Symbols as Keys

```javascript
const weakMap = new WeakMap();
const key = Symbol('unique');

weakMap.set(key, 'value');
weakMap.get(key); // 'value'
```

## ES2022 Features

### Top-Level Await

```javascript
// In ES modules (.mjs or type: "module")
const response = await fetch('https://api.example.com/data');
const data = await response.json();

export { data };

// Dynamic imports with await
const { default: lodash } = await import('lodash');
```

### Private Class Fields & Methods

```javascript
class BankAccount {
  // Private fields (prefixed with #)
  #balance = 0;
  #transactions = [];

  constructor(initialBalance) {
    this.#balance = initialBalance;
  }

  // Private method
  #logTransaction(type, amount) {
    this.#transactions.push({ type, amount, date: new Date() });
  }

  deposit(amount) {
    if (amount <= 0) throw new Error('Invalid amount');
    this.#balance += amount;
    this.#logTransaction('deposit', amount);
  }

  withdraw(amount) {
    if (amount > this.#balance) throw new Error('Insufficient funds');
    this.#balance -= amount;
    this.#logTransaction('withdraw', amount);
  }

  get balance() {
    return this.#balance;
  }

  // Private static
  static #instanceCount = 0;

  static getInstanceCount() {
    return BankAccount.#instanceCount;
  }
}

const account = new BankAccount(1000);
// account.#balance; // SyntaxError: Private field
```

### Static Class Blocks

```javascript
class Config {
  static settings;

  static {
    // Complex initialization logic
    try {
      const stored = localStorage.getItem('settings');
      this.settings = stored ? JSON.parse(stored) : {};
    } catch {
      this.settings = { theme: 'light', lang: 'en' };
    }
  }
}
```

### at() Method

```javascript
const arr = [1, 2, 3, 4, 5];

// Positive index (same as bracket notation)
arr.at(0);  // 1
arr.at(2);  // 3

// Negative index (counts from end)
arr.at(-1); // 5 (last element)
arr.at(-2); // 4 (second to last)

// Works on strings too
const str = 'Hello';
str.at(-1); // 'o'
```

### Object.hasOwn()

```javascript
const obj = { name: 'Alice' };

// Before: Verbose and potentially unsafe
Object.prototype.hasOwnProperty.call(obj, 'name'); // true

// After: Clean and safe
Object.hasOwn(obj, 'name');      // true
Object.hasOwn(obj, 'toString');  // false (inherited)

// Works with objects that don't inherit from Object.prototype
const nullProto = Object.create(null);
nullProto.key = 'value';
Object.hasOwn(nullProto, 'key'); // true
// nullProto.hasOwnProperty('key'); // TypeError
```

### Error Cause

```javascript
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    return await response.json();
  } catch (error) {
    throw new Error('Failed to fetch user', { cause: error });
  }
}

try {
  await fetchUser(123);
} catch (error) {
  console.log(error.message);     // 'Failed to fetch user'
  console.log(error.cause);       // Original fetch error
  console.log(error.cause.stack); // Original stack trace
}
```

## ES2021 Features

### String replaceAll()

```javascript
const text = 'foo bar foo baz foo';

// Before: regex with global flag
text.replace(/foo/g, 'qux'); // 'qux bar qux baz qux'

// After: Simple and clear
text.replaceAll('foo', 'qux'); // 'qux bar qux baz qux'

// Works with regex too (must have global flag)
text.replaceAll(/foo/g, 'qux');
```

### Numeric Separators

```javascript
const billion = 1_000_000_000;
const bytes = 0xFF_FF_FF_FF;
const binary = 0b1010_0001_1000;
const fraction = 0.000_001;

// Readable large numbers
const price = 999_99; // $999.99 in cents
```

### Promise.any()

```javascript
const promises = [
  fetch('https://api1.example.com/data'),
  fetch('https://api2.example.com/data'),
  fetch('https://api3.example.com/data'),
];

// Returns first fulfilled promise
try {
  const fastest = await Promise.any(promises);
  console.log('Got response from:', fastest.url);
} catch (error) {
  // AggregateError if all reject
  console.log('All failed:', error.errors);
}
```

### Logical Assignment Operators

```javascript
let a = null;
let b = 'hello';
let c = 0;

// Nullish coalescing assignment
a ??= 'default';  // a = 'default' (a was null)
b ??= 'default';  // b = 'hello' (b was truthy)

// Logical OR assignment
c ||= 10;  // c = 10 (c was falsy)

// Logical AND assignment
let user = { name: 'Alice' };
user &&= { ...user, updated: true };
// user = { name: 'Alice', updated: true }

// Practical: Initialize if missing
const config = {};
config.debug ??= false;
config.timeout ??= 5000;
```

### WeakRef & FinalizationRegistry

```javascript
// Weak reference to object
let obj = { data: 'important' };
const weakRef = new WeakRef(obj);

// May return undefined if object was garbage collected
const value = weakRef.deref();
if (value) {
  console.log(value.data);
}

// Cleanup callback when object is GC'd
const registry = new FinalizationRegistry((heldValue) => {
  console.log(`Object with id ${heldValue} was garbage collected`);
});

registry.register(obj, 'myObjectId');
```

## ES2020 Features

### Optional Chaining (?.)

```javascript
const user = {
  name: 'Alice',
  address: {
    city: 'NYC'
  }
};

// Safe property access
user?.address?.city;     // 'NYC'
user?.contact?.email;    // undefined (no error)

// Safe method calls
user.getName?.();        // undefined if method doesn't exist

// Safe array access
const arr = [1, 2, 3];
arr?.[0];  // 1
arr?.[10]; // undefined

// Combined with nullish coalescing
const email = user?.contact?.email ?? 'no-email@example.com';
```

### Nullish Coalescing (??)

```javascript
// Only triggers on null/undefined, not falsy values
const count = 0;
const text = '';

count ?? 10;  // 0 (count is not nullish)
text ?? 'default';  // '' (text is not nullish)

count || 10;  // 10 (different behavior with ||)
text || 'default';  // 'default'

// Perfect for optional parameters
function greet(name) {
  const displayName = name ?? 'Guest';
  return `Hello, ${displayName}!`;
}

greet('');      // 'Hello, !' (empty string is valid)
greet(null);    // 'Hello, Guest!'
greet(undefined); // 'Hello, Guest!'
```

### BigInt

```javascript
const big = 9007199254740991n;
const bigger = BigInt('123456789012345678901234567890');

// Arithmetic
big + 1n;      // 9007199254740992n
bigger * 2n;   // 246913578024691357802469135780n

// Cannot mix with regular numbers
// big + 1; // TypeError

// Comparison works
big > 1000;    // true
big === 9007199254740991n; // true

// Useful for IDs, timestamps, etc.
const snowflakeId = 1234567890123456789n;
```

### Promise.allSettled()

```javascript
const promises = [
  Promise.resolve('success'),
  Promise.reject('error'),
  Promise.resolve('another success'),
];

const results = await Promise.allSettled(promises);
// [
//   { status: 'fulfilled', value: 'success' },
//   { status: 'rejected', reason: 'error' },
//   { status: 'fulfilled', value: 'another success' }
// ]

// Filter by status
const fulfilled = results
  .filter(r => r.status === 'fulfilled')
  .map(r => r.value);
```

### Dynamic Import

```javascript
// Conditional loading
if (needsChart) {
  const { Chart } = await import('chart.js');
  new Chart(canvas, config);
}

// Route-based code splitting
const routes = {
  '/dashboard': () => import('./pages/Dashboard.js'),
  '/settings': () => import('./pages/Settings.js'),
};

async function loadPage(path) {
  const loader = routes[path];
  if (loader) {
    const module = await loader();
    return module.default;
  }
}
```

### globalThis

```javascript
// Works in browser, Node.js, Web Workers, etc.
globalThis.setTimeout === window.setTimeout; // true in browser
globalThis.setTimeout === global.setTimeout; // true in Node.js

// Safe global access
globalThis.myGlobal = 'accessible everywhere';
```

## Browser Support

| Feature | Chrome | Firefox | Safari | Node.js |
|---------|--------|---------|--------|---------|
| ES2024 (groupBy, etc.) | 117+ | 119+ | 17.4+ | 21+ |
| ES2023 (findLast, etc.) | 97+ | 104+ | 15.4+ | 18+ |
| ES2022 (private fields) | 84+ | 90+ | 14.1+ | 16+ |
| ES2021 (replaceAll) | 85+ | 77+ | 13.1+ | 15+ |
| ES2020 (?., ??) | 80+ | 72+ | 13.1+ | 14+ |

## Reference Files

- [async-patterns.md](references/async-patterns.md) - Advanced async/await patterns
- [iterators-generators.md](references/iterators-generators.md) - Iterator and generator patterns
