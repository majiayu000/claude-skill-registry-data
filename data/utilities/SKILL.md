---
name: utilities
description: Generate utility functions and helpers following established patterns. Use when creating formatters, validators, data transformers, type guards, or any pure functions.
---

# Utilities Generator

Generate utility functions following established patterns.

## Directory Structure

```
src/lib/
├── utils.ts              # Main utilities (cn, etc.)
├── formatters.ts         # Number/currency/date formatters
├── validators.ts         # Validation helpers
├── transformers.ts       # Data transformation
├── store-utils.ts        # Store migrations & preprocessing
└── type-guards.ts        # Type checking utilities
```

## Number Formatting

### formatCompactNumber

Format large numbers with K/M/B suffixes.

```tsx
// src/lib/formatters.ts

/**
 * Format large numbers compactly (1000 → 1K, 1500000 → 1.5M)
 */
export const formatCompactNumber = (value: number): string => {
  const format = (n: number, suffix: string) => {
    const formatted = parseFloat(n.toFixed(1));
    return formatted.toString().replace(/\.0$/, '') + suffix;
  };

  if (value < 1_000) return value.toString();
  if (value < 1_000_000) return format(value / 1_000, 'K');
  if (value < 1_000_000_000) return format(value / 1_000_000, 'M');
  return format(value / 1_000_000_000, 'B');
};
```

#### Usage Examples

```tsx
formatCompactNumber(500); // "500"
formatCompactNumber(1500); // "1.5K"
formatCompactNumber(1000000); // "1M"
formatCompactNumber(2300000); // "2.3M"
formatCompactNumber(1500000000); // "1.5B"
```

**Common Use Cases:**

- Social media counts (followers, likes)
- Chart labels
- File sizes
- Population numbers
- Any large number display

---

### formatCurrency

Format currency with proper localization.

```tsx
// src/lib/formatters.ts

/**
 * Format currency with symbol and decimals
 */
export const formatCurrency = (amount: number, currency: string = 'USD', locale: string = 'en-US'): string => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};
```

#### Usage Examples

```tsx
formatCurrency(1234.56); // "$1,234.56"
formatCurrency(1234.56, 'EUR', 'de-DE'); // "1.234,56 €"
formatCurrency(1234.56, 'GBP', 'en-GB'); // "£1,234.56"
formatCurrency(1234.56, 'JPY', 'ja-JP'); // "¥1,235"
```

**Common Use Cases:**

- Product prices
- Cart totals
- Financial dashboards
- Transaction history
- Budget displays

---

### formatPercentage

Format numbers as percentages.

```tsx
// src/lib/formatters.ts

/**
 * Format number as percentage
 */
export const formatPercentage = (value: number, decimals: number = 1): string => {
  return `${(value * 100).toFixed(decimals)}%`;
};
```

#### Usage Examples

```tsx
formatPercentage(0.156); // "15.6%"
formatPercentage(0.156, 0); // "16%"
formatPercentage(0.156, 2); // "15.60%"
formatPercentage(1); // "100.0%"
```

**Common Use Cases:**

- Progress indicators
- Statistics
- Completion rates
- Interest rates
- Discounts

---

## Date/Time Formatting

### formatDate

Format dates with various patterns.

```tsx
// src/lib/formatters.ts

type DateFormat = 'short' | 'long' | 'full' | 'iso';

/**
 * Format date with specified pattern
 */
export const formatDate = (date: Date | string, format: DateFormat = 'short'): string => {
  const d = typeof date === 'string' ? new Date(date) : date;

  switch (format) {
    case 'short':
      return d.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });
    case 'long':
      return d.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      });
    case 'full':
      return d.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      });
    case 'iso':
      return d.toISOString().split('T')[0];
    default:
      return d.toLocaleDateString();
  }
};
```

#### Usage Examples

```tsx
const date = new Date('2025-01-21');

formatDate(date, 'short'); // "Jan 21, 2025"
formatDate(date, 'long'); // "January 21, 2025"
formatDate(date, 'full'); // "Tuesday, January 21, 2025"
formatDate(date, 'iso'); // "2025-01-21"
```

**Common Use Cases:**

- Event dates
- Post timestamps
- Deadlines
- Date pickers
- Historical data

---

### formatTime12Hour

Convert 24-hour time to 12-hour format.

```tsx
// src/lib/formatters.ts

/**
 * Convert 24h time to 12h format (e.g., "14:30" → "2:30 PM")
 */
export const formatTime12Hour = (time24: string): string => {
  const [hours, minutes] = time24.split(':').map(Number);
  const period = hours >= 12 ? 'PM' : 'AM';
  const hours12 = hours % 12 || 12;
  return `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`;
};
```

#### Usage Examples

```tsx
formatTime12Hour('09:30'); // "9:30 AM"
formatTime12Hour('14:30'); // "2:30 PM"
formatTime12Hour('00:00'); // "12:00 AM"
formatTime12Hour('12:00'); // "12:00 PM"
formatTime12Hour('23:59'); // "11:59 PM"
```

**Common Use Cases:**

- Time pickers
- Schedule displays
- Appointment times
- Event times
- Clock displays

---

### formatRelativeTime

Format relative time (e.g., "2 hours ago").

```tsx
// src/lib/formatters.ts

/**
 * Format time relative to now (e.g., "2 hours ago")
 */
export const formatRelativeTime = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSecs / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffSecs < 60) return 'just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) !== 1 ? 's' : ''} ago`;
  return formatDate(d, 'short');
};
```

#### Usage Examples

```tsx
const now = new Date();
const min30Ago = new Date(now.getTime() - 30 * 60 * 1000);
const hours2Ago = new Date(now.getTime() - 2 * 60 * 60 * 1000);
const days3Ago = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000);

formatRelativeTime(min30Ago); // "30 minutes ago"
formatRelativeTime(hours2Ago); // "2 hours ago"
formatRelativeTime(days3Ago); // "3 days ago"
```

**Common Use Cases:**

- Social media posts
- Comments
- Chat messages
- Activity feeds
- Notification timestamps

---

## String Utilities

### capitalize

Capitalize first letter of string.

```tsx
// src/lib/utils.ts

/**
 * Capitalize first letter of string
 */
export const capitalize = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};
```

#### Usage Examples

```tsx
capitalize('hello'); // "Hello"
capitalize('WORLD'); // "World"
capitalize('react native'); // "React native"
```

---

### truncate

Truncate string with ellipsis.

```tsx
// src/lib/utils.ts

/**
 * Truncate string with ellipsis
 */
export const truncate = (str: string, maxLength: number, ellipsis: string = '...'): string => {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - ellipsis.length) + ellipsis;
};
```

#### Usage Examples

```tsx
truncate('This is a long text', 10); // "This is..."
truncate('Short', 10); // "Short"
truncate('Hello World', 8, '…'); // "Hello W…"
```

**Common Use Cases:**

- List item previews
- Card titles
- Notification text
- Table cells
- Menu items

---

### slugify

Convert string to URL-friendly slug.

```tsx
// src/lib/utils.ts

/**
 * Convert string to URL-friendly slug
 */
export const slugify = (str: string): string => {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
};
```

#### Usage Examples

```tsx
slugify('Hello World'); // "hello-world"
slugify('React Native App'); // "react-native-app"
slugify('  Trim   Spaces  '); // "trim-spaces"
slugify('Special@#$Characters'); // "specialcharacters"
```

**Common Use Cases:**

- URL generation
- File names
- IDs
- SEO-friendly names
- Route paths

---

## Array Utilities

### groupBy

Group array items by key.

```tsx
// src/lib/utils.ts

/**
 * Group array items by key
 */
export const groupBy = <T, K extends keyof T>(array: T[], key: K): Record<string, T[]> => {
  return array.reduce(
    (result, item) => {
      const groupKey = String(item[key]);
      if (!result[groupKey]) {
        result[groupKey] = [];
      }
      result[groupKey].push(item);
      return result;
    },
    {} as Record<string, T[]>,
  );
};
```

#### Usage Examples

```tsx
const users = [
  { name: 'Alice', role: 'admin' },
  { name: 'Bob', role: 'user' },
  { name: 'Charlie', role: 'admin' },
];

groupBy(users, 'role');
// {
//   admin: [{ name: 'Alice', ... }, { name: 'Charlie', ... }],
//   user: [{ name: 'Bob', ... }]
// }
```

**Common Use Cases:**

- Categorize data
- Section lists
- Group by date
- Aggregate statistics
- Organize items

---

### sortBy

Sort array by key.

```tsx
// src/lib/utils.ts

/**
 * Sort array by key (ascending)
 */
export const sortBy = <T, K extends keyof T>(array: T[], key: K, order: 'asc' | 'desc' = 'asc'): T[] => {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];

    if (aVal < bVal) return order === 'asc' ? -1 : 1;
    if (aVal > bVal) return order === 'asc' ? 1 : -1;
    return 0;
  });
};
```

#### Usage Examples

```tsx
const items = [
  { name: 'Charlie', age: 30 },
  { name: 'Alice', age: 25 },
  { name: 'Bob', age: 35 },
];

sortBy(items, 'name'); // Alice, Bob, Charlie
sortBy(items, 'age', 'desc'); // Bob (35), Charlie (30), Alice (25)
```

---

### unique

Get unique values from array.

```tsx
// src/lib/utils.ts

/**
 * Get unique values from array
 */
export const unique = <T>(array: T[]): T[] => {
  return Array.from(new Set(array));
};

/**
 * Get unique items by key
 */
export const uniqueBy = <T, K extends keyof T>(array: T[], key: K): T[] => {
  const seen = new Set<T[K]>();
  return array.filter(item => {
    const value = item[key];
    if (seen.has(value)) return false;
    seen.add(value);
    return true;
  });
};
```

#### Usage Examples

```tsx
unique([1, 2, 2, 3, 3, 3]); // [1, 2, 3]
unique(['a', 'b', 'a']); // ['a', 'b']

const items = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  { id: 1, name: 'Alice Duplicate' },
];

uniqueBy(items, 'id'); // [{ id: 1, ... }, { id: 2, ... }]
```

---

## Object Utilities

### deepClone

Deep clone an object.

```tsx
// src/lib/utils.ts

/**
 * Deep clone an object
 */
export const deepClone = <T>(obj: T): T => {
  return JSON.parse(JSON.stringify(obj));
};
```

#### Usage Examples

```tsx
const original = { a: 1, b: { c: 2 } };
const cloned = deepClone(original);

cloned.b.c = 3;
console.log(original.b.c); // 2 (unchanged)
```

**Notes:**

- Only works with JSON-serializable values
- Loses Date objects, functions, undefined, symbols
- Use for plain data objects only

---

### omit

Omit keys from object.

```tsx
// src/lib/utils.ts

/**
 * Omit specified keys from object
 */
export const omit = <T extends Record<string, any>, K extends keyof T>(obj: T, keys: K[]): Omit<T, K> => {
  const result = { ...obj };
  keys.forEach(key => delete result[key]);
  return result;
};
```

#### Usage Examples

```tsx
const user = { id: 1, name: 'Alice', password: 'secret', email: 'alice@example.com' };

omit(user, ['password']); // { id: 1, name: 'Alice', email: '...' }
omit(user, ['password', 'email']); // { id: 1, name: 'Alice' }
```

**Common Use Cases:**

- Remove sensitive data
- Filter API responses
- Clean form data
- Prepare for serialization

---

### pick

Pick keys from object.

```tsx
// src/lib/utils.ts

/**
 * Pick specified keys from object
 */
export const pick = <T extends Record<string, any>, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> => {
  const result = {} as Pick<T, K>;
  keys.forEach(key => {
    if (key in obj) {
      result[key] = obj[key];
    }
  });
  return result;
};
```

#### Usage Examples

```tsx
const user = { id: 1, name: 'Alice', email: 'alice@example.com', age: 25 };

pick(user, ['id', 'name']); // { id: 1, name: 'Alice' }
pick(user, ['email', 'age']); // { email: '...', age: 25 }
```

---

### isEqual

Deep equality check.

```tsx
// src/lib/utils.ts

/**
 * Deep equality check for objects
 */
export const isEqual = (a: any, b: any): boolean => {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (typeof a !== 'object' || typeof b !== 'object') return false;

  const keysA = Object.keys(a);
  const keysB = Object.keys(b);

  if (keysA.length !== keysB.length) return false;

  return keysA.every(key => isEqual(a[key], b[key]));
};
```

#### Usage Examples

```tsx
isEqual({ a: 1 }, { a: 1 }); // true
isEqual({ a: 1, b: 2 }, { b: 2, a: 1 }); // true
isEqual({ a: { b: 1 } }, { a: { b: 1 } }); // true
isEqual({ a: 1 }, { a: 2 }); // false
```

---

## Function Composition

### pipeFunctions

Compose functions left-to-right.

```tsx
// src/lib/utils.ts

/**
 * Pipe functions left to right (f(g(h(x))))
 */
export const pipeFunctions = <T>(...fns: ((x: T) => T)[]): ((x: T) => T) => {
  return (value: T) => fns.reduce((v, fn) => fn(v), value);
};
```

#### Usage Examples

```tsx
const sanitize = (str: string) => str.trim();
const lowercase = (str: string) => str.toLowerCase();
const removeSpaces = (str: string) => str.replace(/\s/g, '');

const processInput = pipeFunctions(sanitize, lowercase, removeSpaces);

processInput('  Hello World  '); // "helloworld"
```

**Common Use Cases:**

- Data transformation pipelines
- Form input processing
- Validation chains
- Data sanitization
- Multi-step calculations

---

### compose

Compose functions right-to-left.

```tsx
// src/lib/utils.ts

/**
 * Compose functions right to left (f(g(h(x))))
 */
export const compose = <T>(...fns: ((x: T) => T)[]): ((x: T) => T) => {
  return (value: T) => fns.reduceRight((v, fn) => fn(v), value);
};
```

#### Usage Examples

```tsx
const add5 = (x: number) => x + 5;
const multiply2 = (x: number) => x * 2;
const square = (x: number) => x * x;

const calculate = compose(add5, multiply2, square);

calculate(3); // add5(multiply2(square(3))) = add5(multiply2(9)) = add5(18) = 23
```

---

## Validation Utilities

### isValidEmail

Validate email format.

```tsx
// src/lib/validators.ts

/**
 * Validate email format
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};
```

#### Usage Examples

```tsx
isValidEmail('user@example.com'); // true
isValidEmail('invalid.email'); // false
isValidEmail('user@domain'); // false
```

---

### isValidURL

Validate URL format.

```tsx
// src/lib/validators.ts

/**
 * Validate URL format
 */
export const isValidURL = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};
```

#### Usage Examples

```tsx
isValidURL('https://example.com'); // true
isValidURL('http://example.com'); // true
isValidURL('not-a-url'); // false
```

---

### isValidPhone

Validate phone number (basic).

```tsx
// src/lib/validators.ts

/**
 * Validate phone number (basic US format)
 */
export const isValidPhone = (phone: string): boolean => {
  const phoneRegex = /^\+?[\d\s\-()]{10,}$/;
  return phoneRegex.test(phone);
};
```

#### Usage Examples

```tsx
isValidPhone('(123) 456-7890'); // true
isValidPhone('123-456-7890'); // true
isValidPhone('+1 123 456 7890'); // true
isValidPhone('123'); // false
```

---

## Class Name Utilities

### cn (already in boilerplate)

Class name merging with clsx and tailwind-merge.

```tsx
// src/lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge class names with Tailwind CSS conflict resolution
 */
export const cn = (...inputs: ClassValue[]) => {
  return twMerge(clsx(inputs));
};
```

#### Usage Examples

```tsx
cn('px-4 py-2', 'bg-primary'); // "px-4 py-2 bg-primary"
cn('px-4', condition && 'bg-red-500'); // Conditional classes
cn('px-4 py-2', 'px-8'); // "px-8 py-2" (tailwind-merge resolves conflict)
```

---

## Store Utilities

### Zustand Migration Pattern

Helper for versioned store migrations.

```tsx
// src/lib/store-utils.ts

/**
 * Create migration function for a single item
 */
export const createMigration = <T>(
  migrationFn: (item: T, id: string) => T
) => {
  return (persistedState: any): any => {
    const store = persistedState;
    const migratedItems: Record<string, T> = {};

    Object.entries(store.items || {}).forEach(([id, item]) => {
      try {
        migratedItems[id] = migrationFn(item as T, id);
      } catch (error) {
        console.error(`Error migrating item ${id}:`, error);
        migratedItems[id] = item as T;
      }
    });

    return { ...store, items: migratedItems };
  };
};

/**
 * Migration map for version-based migrations
 */
export const createMigrationMap = <T>(
  migrations: Record<number, (item: T, id: string) => T>
): Map<number, (state: any) => any> => {
  return new Map(
    Object.entries(migrations).map(([version, fn]) => [
      Number(version),
      createMigration(fn),
    ])
  );
};
```

#### Usage Example

```tsx
// src/store/useItemStore.ts
import { createMigrationMap } from '@/lib/store-utils';

const migrateV0ToV1 = (item: Item) => ({
  ...item,
  newField: 'default',
});

const migrateV1ToV2 = (item: Item) => {
  const { oldField, ...rest } = item;
  return { ...rest, renamedField: oldField };
};

const migrationMap = createMigrationMap({
  1: migrateV0ToV1,
  2: migrateV1ToV2,
});

const STORE_VERSION = 2;

export const useItemStore = create<ItemStore>()(
  persist(
    (set, get) => ({
      /* ... */
    }),
    {
      name: 'item-storage',
      version: STORE_VERSION,
      storage: createJSONStorage(() => AsyncStorage),
      migrate: (persistedState, version) => {
        let state = persistedState;
        for (let v = version + 1; v <= STORE_VERSION; v++) {
          if (migrationMap.has(v)) {
            state = migrationMap.get(v)!(state);
          }
        }
        return state;
      },
    },
  ),
);
```

---

### Data Preprocessing Pattern

Deserialize and transform data after rehydration.

```tsx
// src/lib/store-utils.ts

/**
 * Preprocess items after rehydration (e.g., parse dates)
 */
export const preprocessData = <T extends Record<string, any>>(
  items: Record<string, T>,
  transformFn: (item: T) => T,
): Record<string, T> => {
  const processed: Record<string, T> = {};

  Object.entries(items).forEach(([id, item]) => {
    try {
      processed[id] = transformFn(item);
    } catch (error) {
      console.error(`Error preprocessing item ${id}:`, error);
      processed[id] = item;
    }
  });

  return processed;
};
```

#### Usage Example

```tsx
// src/store/useEventStore.ts

const parseDates = (event: Event): Event => ({
  ...event,
  startDate: new Date(event.startDate),
  endDate: new Date(event.endDate),
  createdAt: new Date(event.createdAt),
});

export const useEventStore = create<EventStore>()(
  persist(
    (set, get) => ({
      /* ... */
    }),
    {
      name: 'event-storage',
      storage: createJSONStorage(() => AsyncStorage),
      onRehydrateStorage: () => state => {
        if (state) {
          state.events = preprocessData(state.events, parseDates);
        }
      },
    },
  ),
);
```

**Common Use Cases:**

- Parse ISO date strings back to Date objects
- Instantiate class instances from plain objects
- Transform deprecated data structures
- Add computed properties
- Validate and sanitize stored data

---

## Type Guards

### Basic Type Guards

```tsx
// src/lib/type-guards.ts

/**
 * Check if value is string
 */
export const isString = (value: unknown): value is string => {
  return typeof value === 'string';
};

/**
 * Check if value is number
 */
export const isNumber = (value: unknown): value is number => {
  return typeof value === 'number' && !isNaN(value);
};

/**
 * Check if value is boolean
 */
export const isBoolean = (value: unknown): value is boolean => {
  return typeof value === 'boolean';
};

/**
 * Check if value is object
 */
export const isObject = (value: unknown): value is Record<string, any> => {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
};

/**
 * Check if value is array
 */
export const isArray = (value: unknown): value is any[] => {
  return Array.isArray(value);
};

/**
 * Check if value is null or undefined
 */
export const isNullish = (value: unknown): value is null | undefined => {
  return value === null || value === undefined;
};
```

#### Usage Examples

```tsx
const value: unknown = '123';

if (isString(value)) {
  console.log(value.toUpperCase()); // TypeScript knows it's a string
}

if (isNumber(value)) {
  console.log(value.toFixed(2)); // TypeScript knows it's a number
}
```

**Common Use Cases:**

- API response validation
- Form data validation
- Type narrowing
- Runtime type checking
- Safe property access

---

## Testing Utilities

### Factory Functions

Create test data quickly.

```tsx
// src/lib/test-helpers.ts

/**
 * Create test item with defaults
 */
export const createTestItem = (overrides?: Partial<Item>): Item => ({
  id: 'test-id',
  title: 'Test Item',
  description: 'Test description',
  createdAt: new Date(),
  updatedAt: new Date(),
  status: 'active',
  ...overrides,
});

/**
 * Create test user with defaults
 */
export const createTestUser = (overrides?: Partial<User>): User => ({
  id: 'test-user-id',
  name: 'Test User',
  email: 'test@example.com',
  role: 'user',
  ...overrides,
});
```

#### Usage Examples

```tsx
// In tests
const item = createTestItem({ title: 'Custom Title' });
const admin = createTestUser({ role: 'admin' });
```

---

### Approximate Equality

Test floating point numbers with tolerance.

```tsx
// src/lib/test-helpers.ts

/**
 * Assert approximate equality for floating point numbers
 */
export const expectApproximatelyEqual = (actual: number, expected: number, tolerance: number = 0.01) => {
  const diff = Math.abs(actual - expected);
  if (diff >= tolerance) {
    throw new Error(
      `Expected ${actual} to be approximately ${expected} (tolerance: ${tolerance}), but difference was ${diff}`,
    );
  }
};
```

#### Usage Example

```tsx
// In tests
const result = calculateInterest(1000, 0.05, 1);
expectApproximatelyEqual(result, 50.0, 0.01);
```

---

## Best Practices

### Pure Functions

Utilities should be pure (no side effects):

```tsx
// ❌ Bad - modifies input
export const sortArray = (arr: number[]) => {
  return arr.sort();
};

// ✅ Good - returns new array
export const sortArray = (arr: number[]) => {
  return [...arr].sort();
};
```

### Type Safety

Always provide TypeScript types:

```tsx
// ❌ Bad - no types
export const formatValue = (value, format) => {
  return value.toString();
};

// ✅ Good - typed
export const formatValue = (value: number, format: string): string => {
  return value.toString();
};
```

### Error Handling

Handle edge cases gracefully:

```tsx
// ✅ Good - handles null/undefined
export const capitalize = (str: string | null | undefined): string => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};
```

### Performance

Avoid unnecessary work:

```tsx
// ❌ Bad - recreates regex on every call
export const isEmail = (str: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str);
};

// ✅ Good - reuses regex
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const isEmail = (str: string) => {
  return EMAIL_REGEX.test(str);
};
```

---

## Checklist

- [ ] Pure function (no side effects)
- [ ] TypeScript types for all parameters/returns
- [ ] Unit tests for complex utilities
- [ ] JSDoc comments for public APIs (optional)
- [ ] Exported from appropriate file (`utils.ts`, `formatters.ts`, etc.)
- [ ] Error handling for edge cases
- [ ] Performance optimized (no unnecessary allocations)
- [ ] Documented common use cases
- [ ] Examples provided
- [ ] Type guards return proper type predicates
