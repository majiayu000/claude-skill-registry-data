---
name: detect-hidden-contracts
description: Use when investigating implicit assumptions in code — ordering dependencies, unvalidated environment variables, assumed object shapes, or temporal state requirements that aren't enforced by types or tests
---

## Announce at start: "Using codebase-analyzer to detect hidden contracts."

## Overview

Find implicit contracts not documented in types, interfaces, or API schemas. These are the assumptions that code makes but never states — where real bugs and hidden behaviors live. Every codebase has them: runtime expectations that compile-time checks can't catch, sequencing rules that nothing enforces, data shapes that code assumes but never validates. These hidden contracts are the gap between what the code says it does and what it actually requires.

## Boundary with inventorying-api-surface

API surface (`inventorying-api-surface`) finds implicit ENTRY POINTS (how you get in). This skill finds implicit BEHAVIORAL ASSUMPTIONS (what the code assumes about how it's used). Same codebase, different lens. API surface maps the doors; hidden contracts maps the load-bearing walls that nobody drew on the blueprint.

## Five Contract Types

### 1. Environment Variable Contracts

Code reads `process.env.X` without validation, defaults, or existence checks. The contract: "this variable will always be set in production." When it isn't, behavior ranges from silent wrong answers to crashes.

**Detection**: Search for `process.env.` usage without accompanying `||`, `??`, or `if (!process.env.X)` guards. Also check `os.Getenv`, `os.environ.get`, and similar in other languages.

**Interrogation pattern**: "What breaks when these ENV vars don't exist? Which ones are required vs optional? Which ones change behavior silently vs fail loudly?"

### 2. Ordering Contracts

Function A must be called before function B, but nothing enforces the sequence. Typically manifests as shared mutable state: a global variable set in one function and read in another, or an initialization step that must precede usage.

**Detection**: Search for shared mutable state, global variables set in one function and read in another, singletons that require explicit initialization, state machines with implicit transitions.

**Interrogation pattern**: "What if B is called before A? What if A is called twice? What if A is never called?"

### 3. Shape Contracts

Code accesses `obj.field.subfield` without null checks or runtime validation. The contract: "the object will always have this exact shape." Works until it doesn't — API responses change, deserialization adds wrapping, or a refactor renames a field.

**Detection**: Search for chained property access without optional chaining (`?.`). Look for object destructuring that assumes specific keys exist. Find type assertions (`as SomeType`) that bypass runtime checks.

**Interrogation pattern**: "What shape does this code assume? What happens when the shape is wrong — silent corruption, exception, or wrong output?"

### 4. Temporal Contracts

Code assumes certain state exists at certain times. Initialization flags, lifecycle hooks, readiness booleans — the code works only during specific phases of execution. Violating the temporal order produces subtle, hard-to-reproduce bugs.

**Detection**: Search for state flags, booleans that gate behavior (`initialized`, `ready`, `isConnected`), lifecycle methods that must run in sequence, event listeners attached at specific times.

**Interrogation pattern**: "What if this runs at the wrong time? What state must exist before this code runs? Who guarantees that state?"

### 5. Error Contracts

Code catches specific error types but throwers may throw differently. A function catches `NetworkError` but the underlying library throws `ConnectionRefusedError`. A catch block inspects `error.code` but the error might not have that property.

**Detection**: Search for `catch (e)` vs `catch (SpecificError)`, generic re-throws that lose context, error property access without type narrowing (`e.response.status`), try/catch blocks that silently swallow errors.

**Interrogation pattern**: "What errors does this code expect vs what actually gets thrown? Which catch blocks would miss the real error? Where do errors get silently swallowed?"

## SECURITY_SIGNAL

Hidden contracts become security vulnerabilities when they exist in critical paths. Specifically flag:

- Unvalidated ENV vars in security-critical paths (auth secrets, database URLs, encryption keys)
- Ordering contracts in authentication or authorization flows (e.g., "must call `verify()` before `checkAccess()`")
- Shape contracts in data handling (e.g., assuming request body shape without validation)
- Temporal contracts in session management (e.g., assuming session exists during request processing)
- Error contracts that silently swallow auth failures or permission errors

## Adversarial Lens

Hidden contracts are where the most dangerous bugs live. If code assumes a specific ENV var exists, what happens when an attacker controls that ENV var? If code assumes function A runs before function B, what happens when an attacker calls B first? Hidden contracts are attack vectors.

## Red Flags

- Only finding explicit contracts (types/interfaces) — the hidden ones are the point
- Not checking for runtime vs compile-time enforcement gaps
- Skipping error contracts because "errors are handled" without verifying what's actually thrown
- Ignoring ordering contracts because "it works in tests" (tests often run in the right order by accident)

## Output Contract

Write `docs/analysis/hidden-contracts.md`.
Include: each contract type with specific instances found, severity assessment, which code locations depend on each contract, and recommended enforcement mechanisms (runtime validation, state machines, type narrowing, explicit initialization sequences).
