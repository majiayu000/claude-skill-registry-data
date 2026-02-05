---
name: ultracite
description: Enforce strict type safety, accessibility standards, and code quality for TypeScript/JavaScript projects using Biome's formatter and linter. Use when writing, reviewing, or fixing TS/JS/TSX/JSX code, checking for a11y issues, linting errors, type safety problems, or when the user mentions code quality, formatting, accessibility, or best practices.
allowed-tools: Read, Grep, Glob, Edit
---

# Ultracite - AI-Ready Formatter and Linter

Ultracite enforces strict type safety, accessibility standards, and consistent code quality for JavaScript/TypeScript projects using Biome's lightning-fast formatter and linter.

## Key Principles

- **Zero configuration required**: Works out of the box
- **Subsecond performance**: Lightning-fast checks and fixes
- **Maximum type safety**: Catch errors before runtime
- **AI-friendly code generation**: Optimized for AI-assisted development

## Before Writing Code

When writing or reviewing code, follow this checklist:

1. **Analyze existing patterns** in the codebase
2. **Consider edge cases** and error scenarios
3. **Follow the rules** below strictly
4. **Validate accessibility** requirements

## Common Commands

```bash
# Initialize Ultracite in your project
npx ultracite init

# Format and fix code automatically
npx ultracite fix

# Check for issues without fixing
npx ultracite check
```

## Instructions

When working with TypeScript/JavaScript code:

1. **Read the code** using the Read tool before making changes
2. **Check for violations** of the rules below
3. **Apply fixes** using the Edit tool
4. **Verify accessibility** standards are met
5. **Ensure type safety** with TypeScript

## Core Rule Categories

### 1. Accessibility (a11y)

**Critical accessibility requirements:**

- ❌ Don't use `accessKey` attribute on any HTML element
- ❌ Don't set `aria-hidden="true"` on focusable elements
- ❌ Don't use distracting elements like `<marquee>` or `<blink>`
- ❌ Don't include "image", "picture", or "photo" in img alt prop
- ✅ Make sure label elements have text content and are associated with an input
- ✅ Give all elements requiring alt text meaningful information for screen readers
- ✅ Always include a `type` attribute for button elements
- ✅ Always include a `lang` attribute on the html element
- ✅ Always include a `title` attribute for iframe elements
- ✅ Accompany `onClick` with at least one of: `onKeyUp`, `onKeyDown`, or `onKeyPress`
- ✅ Accompany `onMouseOver`/`onMouseOut` with `onFocus`/`onBlur`
- ✅ Include caption tracks for audio and video elements
- ✅ Use semantic elements instead of role attributes in JSX
- ✅ Always include a `title` element for SVG elements

**Example - Good Accessibility:**

```tsx
// ✅ Good: Proper button with type and accessible events
<button
  type="button"
  onClick={handleClick}
  onKeyDown={handleKeyDown}
>
  Submit
</button>

// ✅ Good: Accessible image with meaningful alt
<img src="/photo.jpg" alt="Team celebrating product launch" />

// ❌ Bad: Missing type, keyboard support, and poor alt text
<button onClick={handleClick}>Submit</button>
<img src="/photo.jpg" alt="image of photo" />
```

### 2. React and JSX Best Practices

**Critical React requirements:**

- ❌ Don't destructure props inside JSX components in Solid projects
- ❌ Don't define React components inside other components
- ❌ Don't use Array index in keys
- ❌ Don't assign JSX properties multiple times
- ❌ Don't use both `children` and `dangerouslySetInnerHTML` props
- ❌ Don't pass children as props
- ✅ Make sure all dependencies are correctly specified in React hooks
- ✅ Make sure all React hooks are called from the top level
- ✅ Don't forget key props in iterators and collection literals
- ✅ Use `<>...</>` instead of `<Fragment>...</Fragment>`

**Example - Good React Patterns:**

```tsx
// ✅ Good: Component defined at top level with proper hooks
function UserList({ users }) {
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    // All dependencies listed
    loadData();
  }, [loadData]);

  return (
    <>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </>
  );
}

// ❌ Bad: Component defined inside, index as key, missing deps
function ParentComponent() {
  function ChildComponent() { // Bad: nested component
    useEffect(() => {
      doSomething(); // Bad: missing dependency
    }, []);
    return <div>Child</div>;
  }

  return items.map((item, i) => (
    <div key={i}>{item}</div> // Bad: index as key
  ));
}
```

### 3. TypeScript Best Practices

**Critical TypeScript requirements:**

- ❌ Don't use TypeScript enums (use `as const` objects instead)
- ❌ Don't use the `any` type
- ❌ Don't use non-null assertions with the exclamation mark postfix operator
- ❌ Don't use TypeScript namespaces
- ❌ Don't use parameter properties in class constructors
- ❌ Don't declare empty interfaces
- ✅ Use `export type` for types
- ✅ Use `import type` for types
- ✅ Use `as const` instead of literal types and type annotations
- ✅ Use either `T[]` or `Array<T>` consistently

**Example - Good TypeScript Patterns:**

```typescript
// ✅ Good: Use const objects instead of enums
const Status = {
  PENDING: 'pending',
  ACTIVE: 'active',
  COMPLETED: 'completed'
} as const;
type Status = typeof Status[keyof typeof Status];

// ✅ Good: Import/export types properly
import type { User } from './types';
export type { User };

// ✅ Good: Specific types, no any
function processUser(user: User): Result<User> {
  return { success: true, data: user };
}

// ❌ Bad: Using enum, any, and non-null assertion
enum Status { PENDING, ACTIVE }  // Bad: use const object
function process(data: any) {    // Bad: use specific type
  return data!.value;            // Bad: avoid non-null assertion
}
```

### 4. Code Quality and Correctness

**Critical correctness requirements:**

- ❌ Don't use `arguments` object (use rest parameters)
- ❌ Don't use unnecessary nested block statements
- ❌ Don't use the void operators
- ❌ Don't reassign const variables
- ❌ Don't use constant expressions in conditions
- ❌ Don't use variables before they're declared
- ❌ Don't use await inside loops
- ❌ Don't shadow variables from outer scopes
- ✅ Use arrow functions instead of function expressions
- ✅ Use `for...of` statements instead of `Array.forEach`
- ✅ Use concise optional chaining
- ✅ Make sure Promise-like statements are handled appropriately

**Example - Good Code Quality:**

```typescript
// ✅ Good: Arrow functions, for-of, proper async handling
const processItems = async (items: Item[]) => {
  const results = [];

  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }

  return results;
};

// ✅ Good: Optional chaining
const userName = user?.profile?.name ?? 'Anonymous';

// ❌ Bad: Function expression, forEach, await in loop
const processItems = function(items) {
  const results = [];
  items.forEach(async (item) => {  // Bad: async in forEach
    await processItem(item);        // Bad: await in loop (via forEach)
  });
  return results;
};
```

### 5. Error Handling

**Error handling best practices:**

- ✅ Always throw Error objects (not strings or other values)
- ✅ Use `new` when throwing an error
- ✅ Handle promises appropriately (await or .catch())
- ✅ Don't use control flow statements in finally blocks
- ✅ Make sure to pass a message value when creating built-in errors

**Example - Good Error Handling:**

```typescript
// ✅ Good: Comprehensive error handling
async function fetchData(url: string): Promise<Result<Data>> {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('API call failed:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// ❌ Bad: Swallowing errors, throwing strings
async function fetchData(url: string) {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (e) {
    console.log(e);              // Bad: just logging
    throw 'Failed to fetch';     // Bad: throwing string
  }
}
```

### 6. Style and Consistency

**Key style requirements:**

- ✅ Use `const` declarations for variables that are only assigned once
- ✅ Use strict equality (===) and strict inequality (!==) instead of loose equality (==) and loose inequality (!=)
- ✅ Use template literals over string concatenation
- ✅ Use assignment operator shorthand where possible (`+=`, `-=`, etc.)
- ✅ Use the `**` operator instead of `Math.pow`
- ✅ Use `new` when throwing an error
- ✅ Don't use `var` (use `const` or `let`)
- ✅ Don't use console (except in development utilities)
- ✅ Don't use debugger statements

**Example - Good Style:**

```typescript
// ✅ Good: Modern, consistent style
const calculateTotal = (items: Item[]): number => {
  let total = 0;

  for (const item of items) {
    total += item.price * item.quantity;
  }

  return total ** 2;  // Use ** instead of Math.pow
};

const message = `Total: $${calculateTotal(items)}`;  // Template literal

// ❌ Bad: Inconsistent, outdated style
function calculateTotal(items) {
  var total = 0;                          // Bad: use const/let

  for (var i = 0; i < items.length; i++) { // Bad: use for-of
    total = total + items[i].price;       // Bad: use +=
  }

  return Math.pow(total, 2);              // Bad: use **
}

var message = 'Total: $' + calculateTotal(items);  // Bad: use template literal
```

### 7. Next.js Specific Rules

**When working with Next.js:**

- ❌ Don't use `<img>` elements (use `next/image` instead)
- ❌ Don't use `<head>` elements (use `next/head` instead)
- ❌ Don't import `next/document` outside of `pages/_document.jsx`
- ❌ Don't use the `next/head` module in `pages/_document.js`

**Example - Good Next.js Patterns:**

```tsx
// ✅ Good: Use Next.js Image component
import Image from 'next/image';

export default function Profile() {
  return (
    <Image
      src="/profile.jpg"
      alt="User profile"
      width={500}
      height={500}
    />
  );
}

// ❌ Bad: Using native img tag
export default function Profile() {
  return <img src="/profile.jpg" alt="User profile" />;
}
```

## Quick Reference

### Most Common Violations

1. **Missing key props** in list items
2. **Using `any` type** instead of specific types
3. **Missing accessibility attributes** (type, alt, aria-*)
4. **Using var** instead of const/let
5. **Index as key** in React lists
6. **Missing error handling** in async functions
7. **Using enums** instead of const objects
8. **Non-null assertions** (postfix exclamation mark) in TypeScript
9. **Await in loops** instead of Promise.all
10. **Missing dependencies** in useEffect

### Common Fixes

**Fix 1: Replace var with const/let**
```typescript
// Before
var count = 0;

// After
let count = 0;
```

**Fix 2: Replace any with specific types**
```typescript
// Before
function process(data: any) { }

// After
function process(data: User) { }
```

**Fix 3: Replace enum with const object**
```typescript
// Before
enum Status { ACTIVE, INACTIVE }

// After
const Status = {
  ACTIVE: 'active',
  INACTIVE: 'inactive'
} as const;
type Status = typeof Status[keyof typeof Status];
```

**Fix 4: Add proper error handling**
```typescript
// Before
async function fetchData() {
  return await fetch('/api/data');
}

// After
async function fetchData(): Promise<Result<Data>> {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('Fetch failed:', error);
    return { success: false, error };
  }
}
```

**Fix 5: Use proper keys in lists**
```typescript
// Before
items.map((item, i) => <div key={i}>{item}</div>)

// After
items.map(item => <div key={item.id}>{item.name}</div>)
```

## When to Use This Skill

Use this skill when:

- Writing new TypeScript/JavaScript code
- Reviewing existing code for issues
- Fixing linting or type errors
- Ensuring accessibility compliance
- Refactoring code to follow best practices
- Setting up code quality standards
- Preparing code for production

## Additional Resources

For a complete list of all rules and detailed explanations, refer to the Biome documentation at https://biomejs.dev/linter/rules/
