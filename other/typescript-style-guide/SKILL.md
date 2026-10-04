---
name: typescript-style-guide
description: "Conventions and best practices for writing maintainable TypeScript code based on the Google TypeScript Style Guide. Use this skill when writing new TypeScript modules or services, refactoring TypeScript code to improve readability and maintainability, enforcing consistent naming, typing, and formatting conventions, designing strongly typed APIs, interfaces, and classes, avoiding unsafe patterns such as `any`, prototype modification, or loose equality, structuring large TypeScript codebases with predictable patterns, and implementing safe and maintainable code in Node.js or browser TypeScript projects. Emphasizes strong typing, clear naming conventions, strict equality usage, minimal visibility exposure, avoiding dangerous JavaScript features, and consistent formatting. Reference: https://google.github.io/styleguide/tsguide.html"
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Skill: TypeScript (Google Style Guide)

## Overview

This skill follows the [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) and provides conventions and best practices for writing consistent, maintainable, and type-safe TypeScript code.

---

# 1. Language Rules

### Variable Declarations

- **Use `const` and `let`:** Use `const` by default. Use `let` only if reassignment is required. **Never use `var`.**
- **One variable per statement:** Do not use `let a = 1, b = 2;`.
- **Initialization:** Declare variables close to where they are used.

### Types & Inference

- **Implicit Types:** Rely on type inference for trivial initializations (e.g., `const x = 5;`, `const s = 'foo';`).
- **Explicit Types:** Use explicit type annotations when the type is not obvious or for public APIs.
- **Avoid `any`:** Never use `any`. Use `unknown` if the type is truly unknown.
- **Avoid `{}`:** Use `Record<string, unknown>` or `object` instead of the empty object type `{}`.

### Arrays & Objects

- **Literals:** Use `[]` and `{}` instead of `new Array()` or `new Object()`.
- **Array Types:** Use `T[]` for simple types and `Array<T>` for complex or nested types.
- **Iteration:** Use `for...of` to iterate over arrays. Avoid `forEach` unless necessary for side effects in a chain.

### Classes

- **Visibility:** Use TypeScript visibility modifiers (`private`, `protected`). Avoid ES private fields (`#field`).
- **Modifiers:** Restrict symbol visibility as much as possible. Do not use `public` explicitly (it is the default).
- **Parameter Properties:** Use parameter properties in constructors to reduce boilerplate.
  ```ts
  class UserService {
    constructor(private readonly db: Database) {}
  }
  ```
- **Readonly:** Mark properties `readonly` if they are not reassigned.
- **Prototype:** Never modify built-in prototypes.

### Interfaces vs. Type Aliases

- **Prefer `interface`:** Use `interface` for object structures (classes/objects).
- **Use `type`:** Use `type` for unions, intersections, or primitive aliases.
  ```ts
  interface User {
    id: string;
  }
  type ID = string | number;
  ```

### Enums

- **Plain Enums:** Use plain `enum`. **Do not use `const enum`.**
- **Safety:** Do not use enums for boolean coercion.

### Functions

- **Declarations:** Use `function Foo() {}` for named functions at the top level.
- **Arrow Functions:** Use arrow functions for expressions, nested functions, and callbacks.
- **Return Types:** Always provide explicit return types for public functions and methods.

### Control Flow & Equality

- **Braces:** Always use braces `{}` for all control structures (`if`, `else`, `for`, `while`), even for single-line statements.
- **Equality:** Always use strict equality (`===` and `!==`).
- **Null Checks:** Use `obj == null` (loose equality) specifically to check for both `null` and `undefined`.

---

# 2. Style Rules

### Semicolons & Layout

- **Semicolons:** Required at the end of every statement.
- **Line Length:** Maximum of **80 characters**.
- **Indentation:** Use **2 spaces** per level. No tabs.
- **Braces:** Use "Egyptian Braces" (opening brace on the same line).

### Naming Conventions

| Entity                   | Style            | Example       |
| :----------------------- | :--------------- | :------------ |
| **Classes / Interfaces** | `UpperCamelCase` | `UserProfile` |
| **Types / Enums**        | `UpperCamelCase` | `UserStatus`  |
| **Decorators**           | `UpperCamelCase` | `@Component`  |
| **Variables / Params**   | `lowerCamelCase` | `timeoutMs`   |
| **Functions / Methods**  | `lowerCamelCase` | `fetchData()` |
| **Constants**            | `CONSTANT_CASE`  | `MAX_RETRY`   |

- **No Prefixes:** Do not use `_` or `$` prefixes for private members or variables.

### Strings

- **Single Quotes:** Use single quotes `'` for ordinary string literals.
- **Template Literals:** Use backticks `` ` `` for complex concatenation or multi-line strings.

### Modules & Exports

- **ES Modules:** Use `import`/`export`. Do not use `require()` or `namespace`.
- **Named Exports:** **Do not use `export default`.** Use named exports for better discoverability and refactoring.
  ```ts
  export class Bar {} // Correct
  export default Bar; // Incorrect
  ```

### Comments

- **JSDoc:** Use `/** ... */` for documentation of classes, methods, and properties.
- **Implementation:** Use `//` for internal notes.
- **Parameters:** Use inline comments for boolean parameters if meaning is unclear: `start(/* shouldHeat= */ true)`.

---

# 3. Compiler & Tooling

- **Strict Mode:** Always use `strict: true` in `tsconfig.json`.
- **Directives:** Avoid `@ts-ignore`. Use `@ts-expect-error` sparingly (primarily in tests) with a comment explaining why.

---

# Key Principles

1. **Type Safety:** Prioritize strong types over `any` or loose assertions.
2. **Readability:** Follow clear naming and formatting rules to ensure long-term maintainability.
3. **Consistency:** Match the style of the existing project if it deviates slightly from these rules.
4. **Modern Features:** Use ES6+ and TypeScript-specific features effectively while avoiding dangerous JS patterns.
