---
name: readable-code
description: Readable code rules inspired by The Art of Readable Code, for any language with TypeScript/JavaScript as the primary focus. Use when writing, reviewing, or refactoring code in TS, JS, React/JSX, Node, Python, or any other language, including when the user asks to clean up, simplify, untangle, or make code easier to follow. Enforces short functions, flat control flow, clear naming, readable structure, and language idioms.
---

# Readable Code Rules (/readable-code)

Apply these rules when writing, reviewing, or refactoring code. Inspired by
_The Art of Readable Code_ by Dustin Boswell and Trevor Foucher.

**Core principle: Code should be easy to understand.** The time it takes someone
else (or future you) to understand the code is the ultimate metric.

## How to Apply

- The general rules below apply to every language. Examples use TypeScript.
- Load the language reference for idioms:
  - TypeScript / JavaScript / JSX: [references/typescript.md](references/typescript.md)
  - Python: [references/python.md](references/python.md)
  - Other languages: apply the general rules plus that language's own idioms.
- The project's linter, formatter, and existing conventions win over these
  rules. Readability is partly familiarity, so a consistent codebase beats a
  locally "better" style.
- When editing existing code, apply the rules to the code you touch. Mention
  other problems instead of rewriting unrelated code.
- When reviewing, cite the rule number with each finding so the author can
  look up the reasoning.

## 1. Keep Functions Short and Focused

- A function should do **one thing**. If you can describe what it does with
  "and", split it.
- Aim for functions that fit on one screen (~15-25 lines). If it's longer,
  extract sub-tasks.
- Each function should operate at a **single level of abstraction** — don't mix
  high-level logic with low-level details in the same function.

## 2. Flatten Control Flow — No Deep Nesting

- **Never nest more than 2 levels deep.** If you have a loop inside a loop, or
  an `if` inside a loop inside an `if`, extract the inner block into a helper
  function with a descriptive name.
- Use **early returns / guard clauses** to handle edge cases at the top, keeping
  the main logic flat.
- Prefer `continue` or `break` to skip iterations rather than wrapping the body
  in a conditional.
- Replace complex conditionals with well-named helper functions or variables
  that explain the intent.

```ts
// Bad: nested and hard to follow
for (const user of users) {
  if (user.isActive) {
    for (const order of user.orders) {
      if (order.isPending) {
        process(order);
      }
    }
  }
}

// Good: flat, each function name explains what it does
const activeUsers = getActiveUsers(users);
for (const user of activeUsers) {
  processPendingOrders(user.orders);
}
```

## 3. Name Things Clearly

- **Pack information into names.** Use specific, concrete words — `fetchPage`
  not `get`, `retryCount` not `n`.
- **Avoid generic names** like `tmp`, `data`, `result`, `val`, `info`, `handle`
  — unless the scope is tiny (2-3 lines).
- **Use names that can't be misconstrued.** If a range is inclusive, say
  `maxItems` not `limit`. If a boolean, use `is`, `has`, `should`, `can`
  prefixes.
- **Match the name length to the scope.** Short names for small scopes,
  descriptive names for wide scopes.
- **Don't use abbreviations** unless they're universally understood (`num`,
  `max`, `min`, `err`, `id`, `url` are fine; `svcMgrCfg` is not).
- Follow the language's casing convention (`camelCase` in TS/JS, `snake_case`
  in Python) and the codebase's naming patterns.

## 4. Make Control Flow Easy to Follow

- Put the **changing/interesting value on the left** side of comparisons:
  `if (length > 10)` not `if (10 < length)`.
- Order `if/else` blocks: **positive case first**, simpler case first, or the
  more interesting case first.
- Minimize the number of variables the reader has to track. Reduce the
  **mental footprint** of each block.
- Avoid the **ternary operator** for anything non-trivial — if it's not
  immediately obvious, use an `if/else`. Never nest ternaries.

## 5. Break Down Giant Expressions

- Use **explaining variables** to break complex expressions into named pieces.
- Use **summary variables** to capture a long expression that's used more than
  once.
- Apply **De Morgan's laws** to simplify negated boolean expressions.

```ts
// Bad
if (!(age >= 18 && hasId && !isBanned)) {
  deny();
}

// Good
const isEligible = age >= 18 && hasId && !isBanned;
if (!isEligible) {
  deny();
}
```

## 6. Extract Unrelated Subproblems

- If a block of code is solving a **subproblem unrelated to the main goal** of
  the function, extract it.
- The helper function should be **pure and self-contained** — it shouldn't need
  to know about the calling context.
- This is the single most effective way to improve readability: separate _what_
  you're doing from _how_.

## 7. One Task at a Time

- Each section of code should do **one task**. If a function is doing parsing
  AND validation AND transformation, split them into separate steps.
- List the tasks a function does. If there's more than one, reorganize so each
  task is in its own block or function.

## 8. Reduce Variable Scope

- **Declare variables close to where they're used.** Don't declare at the top
  of a function if it's only used 30 lines later.
- **Minimize the "live time" of a variable** — the fewer lines between its
  assignment and last use, the easier it is to follow.
- **Prefer write-once variables.** Variables that are assigned once and never
  modified are easier to reason about.
- **Eliminate unnecessary variables.** If a variable is used only once and
  doesn't clarify anything, inline it.

## 9. No Magic Numbers or Strings

- Replace **magic numbers and strings** with named constants:
  `if (retries > MAX_RETRIES)` not `if (retries > 3)`.
- If a value has meaning, give it a name. The name documents the intent.
- Group related constants together.

## 10. Fewer Function Arguments

- Aim for **3 or fewer arguments** per function. More than that is a smell.
- Group related arguments into an **object or named type**.
- If a function needs many config-like options, pass a single options object.
- Boolean flag arguments are a sign the function does two things — split it
  instead. A call like `render(user, true, false)` can't be read without
  opening the definition.

## 11. Consistency

- If the codebase does something one way, **do it the same way**. Don't mix
  styles.
- Consistent naming patterns, consistent structure, consistent error handling.
- When joining an existing codebase, **match the existing conventions** even if
  you'd prefer a different style.
- Surprise is the enemy of readability — predictable code is readable code.

## 12. Write Less Code

- The best code is **no code at all**. Question whether a feature is truly
  needed before implementing.
- **Don't over-engineer.** Solve the problem at hand, not hypothetical future
  problems.
- Remove dead code. Commented-out code is dead code.
- Use the standard library and platform APIs before writing custom solutions.

## 13. Comments: Explain Why, Not What

- Don't comment **what** the code does — the code already says that. Comment
  **why** it does it.
- Comment **flaws and workarounds**: `// TODO:`, `// HACK:`, `// XXX:` with
  explanation.
- Comment **surprising behavior** or non-obvious decisions — things where a
  reader would ask "why?".
- **Don't comment bad code — rewrite it.** If you need a comment to explain
  what a block does, extract it into a well-named function instead.

## 14. Design Code to Survive Auto-Formatting

- Write code that looks good **after** the project's formatter runs, if it has
  one (Prettier, Biome, Black, Ruff). If a chained expression or repeated
  pattern would be broken across 4+ lines by the formatter, extract a helper
  function instead.
- **Prefer one-line helper calls** over long inline chains that the formatter
  will expand vertically.
- The formatter is your reader's first impression. Run it _before_ committing —
  if the result looks ugly, that's a signal to refactor, not to disable the
  formatter.

```ts
// Bad: Prettier wraps this into a tall chain in the middle of the handler
const users = await db
  .selectFrom("users")
  .where("active", "=", true)
  .leftJoin("orders", "orders.userId", "users.id")
  .orderBy("users.createdAt", "desc")
  .limit(pageSize)
  .execute();

// Good: extract a helper so the call site stays clean
function getActiveUsers(db: Database, pageSize: number) {
  return db
    .selectFrom("users")
    .where("active", "=", true)
    .leftJoin("orders", "orders.userId", "users.id")
    .orderBy("users.createdAt", "desc")
    .limit(pageSize)
    .execute();
}

const users = await getActiveUsers(db, 20);
```

```ts
// Bad: inline lookup chain — Prettier expands it to 5+ lines
const config = Object.fromEntries(
  requiredKeys.map((key) => [key, settings[key] ?? defaults[key] ?? fallbacks[key]]),
);

// Good: extract the lookup
const resolveSetting = (key: string) => settings[key] ?? defaults[key] ?? fallbacks[key];

const entries = requiredKeys.map((key) => [key, resolveSetting(key)]);
const config = Object.fromEntries(entries);
```
