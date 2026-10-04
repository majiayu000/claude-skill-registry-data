---
name: coding-standards
description:
  MUST load this BEFORE writing or editing any .ts or .tsx file in this repo.
---

## General Rules

- Components MUST be `export const Foo = memo(function Foo(props) { ... })`.
- UI MUST use Mantine (`@mantine/core`) components, not raw HTML elements.
- Styling MUST prefer CSS variables (Mantine `--mantine-*`) over hard-coded
  values.
- `/src/ioc` MUST contain DI wiring only (Context + Provider + useService hook).
  Application Hooks/logic MUST go in `/src/hooks`.
- `/src/ioc/AppProviders.tsx` MUST list every singleton service's Provider in
  `appProviders`.
- Class methods MUST use `foo() {}`, not arrow class fields.
- Interface/class fields MUST be `readonly` unless mutation is intentional.
- Important app-level constants MUST live in `/src/common/Config.ts`, named with
  the prefix of the feature/area that owns them (e.g. `AUTH_*`).
- Services publishing events MUST use `eventemitter3` (typed `EventEmitter`).
- Event types MUST be fine-grained enough listeners can't pick the wrong one,
  but not so many they're a pain to listen to.
- Code (services, components, hooks, etc.) MUST NOT read `import.meta.env` or
  any other config source directly; config MUST be injected via
  constructor/props (read/validated in `/src/ioc`).
- AVOID ReturnType<T>. Declare type properly.

## Comments & Docs Best Practices

- Add inline comments for each code block.
- Inline comment MUST explain INTENTION of the next code block ("when X, do Y"),
  not mechanics. MUST keep it short, I recommend 2 sentences MAX.

Good: // Retrieve the user from database. DynamoDB client is used because.. (The
intention, then the "why") Bad: // DynamoDB is used because user is stored here
(What's the intention?)

- Wite as a linguist expert in jsdoc, comments, classes, methods, variable
  naming, etc. Writing MUST flow nice, simple, and easy to understand.
- jsdoc MUST NOT exceed 2 sentences. DO NOT leak implementation details.
- Exported classes, public methods, and public APIs, constants MUST have a super
  short JSDoc: what it does, not how.
- Non-obvious constants MUST have a one-line jsdoc saying what they are.

## Error Handling

- MUST try/catch only the line of code that potentially throw an exception,
  narrow down by exception code/type. Otherwise, you wil catch wrong exception,
  swallowing real errors.
- Methods that can throw MUST have a `@throws` JSDoc explaining when, so callers
  can avoid/handle it. Include throws from downstream services/calls, not just
  direct `throw`s.
- All throws indicate expected errors MUST be documented, except those to
  indicate bugs - unexpected errors, like OutOfMemory etc.
- NEVER catch-all error, only catch DOCUMENTED errors (@throws). Except when
  you're at the top of the callstack (e.g. a top-level request handler, an app
  error boundary).
- MUST log error (console.error()) when catching at the top of the callstack.
- When catching exceptions from `autoassure-server-sdk`, use `ServiceError`
  (`src/models/ServiceError.ts`) to parse the exception. If can't be handled,
  you SHOULD rethrow as ServiceError or a custom error that extends
  `ServiceError`.
