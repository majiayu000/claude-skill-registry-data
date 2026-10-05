---
name: breaking-change-detection
description: This skill should be used when the user mentions "breaking change", "semver", "semantic versioning", "major minor patch", "version bump", "backward compatible", "API compatibility", or "deprecation". Provides a decision matrix and per-ecosystem signals for reasoning about behavioral (not just syntactic) breaking changes.
---

# Breaking Change Detection

## Purpose

Standardize how a change is classified against Semantic Versioning by reasoning about its effect on *consumers*, including behavioral breaks that leave the syntax intact. Humans get binary compatibility right only about 60% of the time; this methodology closes the gap with an explicit decision matrix and per-ecosystem catalogs. Tech-agnostic.

## First: is the change on the public surface?

Only changes to the **public API surface** can be breaking or minor. Establish the surface before classifying (detailed per ecosystem in `references/breaking-change-catalog.md`):

| Ecosystem | Public surface |
|-----------|----------------|
| JS/TS | `package.json` `exports`/`main`, named/default exports, `.d.ts` |
| Python | `__all__`, non-`_` names, entry points |
| Go | Capitalized identifiers outside `internal/` |
| Java/C# | `public`/`protected` members of exported packages |
| Rust | `pub` items reachable from the crate root |
| CLI | flags, subcommands, arg order, exit codes, stdout format |
| HTTP | routes, methods, request/response schema, status codes |
| GraphQL | types, fields, args, nullability, enum values |
| Config | recognized keys, env vars, defaults |

A change entirely within private/internal code is at most a PATCH.

## The decision matrix

| Change | Classification |
|--------|----------------|
| Remove/rename a public export, field, route, flag, env var | **MAJOR** |
| Change a signature (add required param, reorder, retype, change return type) | **MAJOR** |
| Change a default value that alters observable behavior | **MAJOR** |
| Make validation stricter (reject formerly-valid input) | **MAJOR** |
| Change output shape, field names, units, or serialization | **MAJOR** |
| Change/narrow error or exception types, or HTTP status codes | **MAJOR** |
| Remove an enum value or change its meaning | **MAJOR** |
| Add a new public export/endpoint/optional param/flag | **MINOR** |
| Add an optional field to output (additive) | **MINOR** |
| Loosen validation (accept more input) | **MINOR** (usually) |
| Deprecate without removing | **MINOR** |
| Bug fix restoring documented behavior | **PATCH** |
| Performance improvement, no behavior change | **PATCH** |
| Internal refactor, docs, tests, CI | **PATCH** / no release |

Aggregate rule: the single highest-severity change in the range sets the bump.

## Behavioral vs syntactic breaks

Syntactic breaks (removed symbol, changed signature) are caught by compilers. **Behavioral breaks are not** and cause most surprise incompatibilities:

- Same signature, stricter validation → previously-passing inputs now throw.
- Same return type, changed field meaning/units (seconds → milliseconds).
- Same endpoint, changed default page size or sort order.
- Same function, changed default argument that flips behavior.
- Same enum type, a value's semantics changed.

Always read the *diff of behavior*, not only the diff of declarations.

## Additional Resources

### Reference Files
- **`references/breaking-change-catalog.md`**: per-language and per-interface signals (JS/TS, Python, Go, Java, Rust, HTTP/REST, GraphQL, database schema, CLI): what is a break vs an additive change, with concrete examples.
- **`references/semver-rules.md`**: a concise SemVer 2.0.0 summary, pre-1.0.0 rules, deprecation policy (deprecate before removing), and how to communicate breaks to users.
