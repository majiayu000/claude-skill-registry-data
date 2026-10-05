---
name: documentation-standards
description: This skill should be used when the user asks to "document code", "add documentation", "write docstrings", "add JSDoc", "fix documentation", "update docs", "check documentation quality", "add doc comments", or "generate API docs". Provides language-specific documentation format knowledge and quality standards for generating, updating, and auditing code documentation.
version: 1.0.0
---

# Documentation Standards

## Purpose

Define language-specific documentation formats, quality standards, and writing principles for generating, auditing, and maintaining code documentation. Apply these standards consistently across all documentation-related operations.

## Core Principles

### Explain the Why, Not the What

Focus documentation on intent, rationale, and context rather than restating what the code already expresses. A function named `calculateTax` does not need a description that says "calculates tax." Instead, describe which tax rules apply, what edge cases exist, and why a particular algorithm was chosen.

**Weak:**
```javascript
/** Sorts the array. */
function sortUsers(users) { ... }
```

**Strong:**
```javascript
/**
 * Sort users by subscription tier (premium first), then by join date.
 *
 * Premium users appear first to ensure priority support routing.
 * Within the same tier, older accounts take precedence per SLA policy.
 */
function sortUsers(users) { ... }
```

### Use Active Voice

Write descriptions in active voice, present tense. Start function descriptions with a verb.

| Preferred | Avoid |
|-----------|-------|
| "Validate user credentials against the auth database" | "User credentials are validated" |
| "Return the cached result if available" | "The cached result is returned" |
| "Parse the CSV file into a list of records" | "A list of records is parsed from the CSV" |

### Completeness Requirements

Document every public API with all of the following:

1. **Brief summary** -- one sentence stating what the function does
2. **Parameters** -- every parameter with type, description, default value, and constraints
3. **Return value** -- type, meaning, and edge-case values (e.g., `null` when not found)
4. **Exceptions/errors** -- every error condition with its cause
5. **Side effects** -- I/O operations, state mutations, event emissions, network calls
6. **At least one example** -- realistic, runnable usage demonstrating the common case

Mark internal/private APIs as lower priority but still document non-trivial logic. When a private function contains a complex algorithm, business rule, or non-obvious workaround, treat it as high priority regardless of visibility.

## Language Format Quick Reference

| Language | Format | Summary Start | Param Tag | Return Tag | Throws Tag |
|----------|--------|---------------|-----------|------------|------------|
| JavaScript/TypeScript | JSDoc `/** */` | Verb phrase | `@param {Type} name` | `@returns {Type}` | `@throws {Type}` |
| Python | Google-style docstring `"""` | Verb phrase | `Args:` section | `Returns:` section | `Raises:` section |
| Java/Kotlin | Javadoc `/** */` | Verb phrase with `<p>` | `@param name` | `@return` | `@throws Type` |
| Go | `//` comment block | `FuncName verb-phrase.` | Prose description | Prose description | Prose description |
| Rust | `///` doc comment | Verb phrase | `# Arguments` section | `# Returns` section | `# Errors` section |
| C# | XML `/// <summary>` | Verb phrase | `<param name="">` | `<returns>` | `<exception cref="">` |
| Ruby | YARD `#` | Verb phrase | `@param [Type] name` | `@return [Type]` | `@raise [Type]` |
| PHP | PHPDoc `/** */` | Verb phrase | `@param Type $name` | `@return Type` | `@throws Type` |

For complete templates, before/after examples, and per-language standards checklists, see **`references/language-formats.md`**.

## Documentation Quality Severity Levels

Use these severity levels when auditing or reporting documentation issues.

### Critical -- Must Fix Immediately

Issues that cause incorrect understanding or hide dangerous behavior.

| Issue | Example |
|-------|---------|
| Documentation contradicts implementation | Doc says returns `User`, code returns `Optional<User>` |
| Parameter count mismatch | Doc lists 2 params, function accepts 4 |
| Missing error documentation for throwing functions | Function throws `AuthError` but doc omits it |
| Undocumented public API | Exported function with zero documentation |
| Documented side effects that no longer occur | Doc says "sends email" but that behavior was removed |

### High -- Fix This Sprint

Issues that cause confusion or leave important gaps.

| Issue | Example |
|-------|---------|
| Missing parameter documentation | 3 of 5 parameters undocumented |
| Missing return value documentation | Complex return object with no description |
| Outdated examples | Example uses removed API or old signatures |
| No documentation on complex logic | 80-line algorithm with no explanation |
| Missing type information in typed contexts | `@param name` without `{string}` |

### Medium -- Fix This Quarter

Issues that reduce documentation usefulness.

| Issue | Example |
|-------|---------|
| Missing examples for non-trivial functions | Complex filtering function with no usage example |
| Generic descriptions | "Processes the data" without specifics |
| Missing cross-references | No `@see` or "See Also" for related functions |
| Missing performance notes | O(n^2) algorithm without complexity warning |
| Incomplete edge case documentation | Does not mention behavior with empty input |

### Low -- Fix When Convenient

Issues that affect polish and completeness.

| Issue | Example |
|-------|---------|
| Missing version tags | No `@since` annotation |
| No deprecation guidance | Deprecated without replacement suggestion |
| Inconsistent formatting | Mixed spacing or tag ordering within a file |
| Missing author or module-level overview | File lacks top-level description |

## Documentation Writing Standards

### Specificity Over Generality

Replace vague descriptions with concrete, measurable statements.

| Vague | Specific |
|-------|----------|
| "Handles errors" | "Catch `NetworkError` and retry up to 3 times with exponential backoff starting at 200ms" |
| "Processes the input" | "Parse the JSON payload, validate required fields, and normalize email addresses to lowercase" |
| "Returns the result" | "Return a `PaginatedResponse<User>` containing up to 50 users and a cursor token for the next page" |

### Terminology Consistency

Maintain consistent terminology within a project:

- Choose one term per concept and use it everywhere (e.g., always "user ID" not sometimes "userId" and sometimes "user identifier")
- Match parameter names in documentation to parameter names in code exactly
- Use the same tense and grammatical structure across all descriptions in a file

### Example Quality Standards

Write examples that meet these criteria:

1. **Realistic** -- use plausible data, not `foo`/`bar`/`baz`
2. **Runnable** -- include imports, setup, and assertions where possible
3. **Progressive** -- show the common case first, then edge cases
4. **Self-contained** -- each example should work independently without external context

```javascript
/**
 * @example
 * // Fetch active users with pagination
 * const page = await fetchUsers({ status: 'active', limit: 25, offset: 0 });
 * console.log(page.users.length); // 25
 * console.log(page.total);        // 1042
 *
 * @example
 * // Handle empty results
 * const empty = await fetchUsers({ status: 'banned', limit: 10 });
 * console.log(empty.users);  // []
 * console.log(empty.total);  // 0
 */
```

## Documentation Drift Detection

When auditing or updating documentation, watch for these drift patterns:

| Drift Pattern | Detection Method |
|---------------|-----------------|
| Parameter count mismatch | Compare `@param` tag count to function signature parameter count |
| Return type mismatch | Compare `@returns` type to actual return type or type annotation |
| Missing new parameters | Look for parameters in the signature not present in doc tags |
| Removed parameters still documented | Look for `@param` tags referencing parameters no longer in signature |
| Behavioral drift | Compare described side effects to actual function body operations |
| Stale examples | Check that example code uses current function signatures and return shapes |

When drift is detected, update the documentation to match the implementation, not the other way around. The code is the source of truth. Never modify code to match outdated documentation unless the documentation reflects the intended design and the code has a bug.

## Format Selection Rules

When generating or auditing documentation, select the format by these rules:

1. **Follow existing project conventions** -- if the project already uses a documentation style, match it exactly
2. **Follow language conventions** -- if no project style exists, use the language standard (JSDoc for JS/TS, Google-style for Python, Javadoc for Java, etc.)
3. **Prefer structured formats** -- use tagged formats (`@param`, `Args:`) over unstructured prose for API documentation
4. **Match tooling expectations** -- choose formats compatible with the project's documentation generator (TypeDoc, Sphinx, Javadoc tool, godoc, etc.)

## Module and File-Level Documentation

Beyond function-level documentation, ensure each file or module has a top-level description covering:

- **Purpose** -- what this module is responsible for
- **Dependencies** -- key external dependencies and why they are needed
- **Usage** -- how other modules should import and use this module
- **Architecture notes** -- where this module fits in the broader system

Place module-level documentation at the top of the file, before any imports or declarations. For languages that require a package declaration first (Java, Go), place the module comment immediately above the package statement.

## Additional Resources

### Reference Files

For detailed per-language templates and quality audit procedures, consult:
- **`references/language-formats.md`** -- Complete documentation templates, before/after examples, and standards checklists for JSDoc, Python, Javadoc, Go, Rust, C#, Ruby, and PHP
- **`references/quality-checklist.md`** -- Completeness, accuracy, and consistency audit procedures with documentation drift detection and writing quality criteria
