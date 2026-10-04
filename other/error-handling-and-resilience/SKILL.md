---
name: error-handling-and-resilience
description: Use when establishing error handling patterns for a project, when adding retry logic, circuit breakers, or graceful degradation, when reviewing how a service handles failures, or when an incident reveals that a failure mode was silently swallowed.
---

# Error Handling and Resilience

## Overview

Define the project's failure philosophy *before* failures happen. Output is `.forge/error-handling.md` — an error-class taxonomy, retry and timeout discipline, circuit breaker policy, graceful degradation paths, user-facing error message rules, and rollback/compensation patterns for irreversible flows. Downstream skills (`observability`, `incident-response-and-postmortems`) consume this file.

## When to Use

- A new service is being designed and needs an error model before code lands
- An incident revealed a silently-swallowed failure
- External calls (DB, API, queue, LLM) are being added to a hot path
- Code review is flagging inconsistent error handling across modules
- Production logs are full of unclassified errors with no caller action

## When NOT to Use

- The codebase already has a documented error taxonomy and the change is local to one module
- One-off scripts or throwaway prototypes
- The work is a config tweak with no failure surface

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "try-catch is enough" | Bare catch swallows context. Without classification, the same handler runs for transient DB blips and bad user input. |
| "We'll add retries later" | Retries are architectural — adding them after the fact requires every caller to change. |
| "Errors are rare" | Rare errors in production are the ones that page you at 3am. They're rare *because* they require specific conditions, not because they don't matter. |
| "Just log and continue" | Silent failures compound. Downstream code now sees inconsistent state and no signal that something went wrong. |
| "External call without timeout is fine, the library has defaults" | Library defaults are usually 30s-infinity. Your user is gone in 8 seconds. |
| "Retry forever, eventually it'll work" | Retry storms amplify outages. Without a cap, you DDoS yourself. |

## Red Flags

- `try { ... } catch (e) {}` — empty catch
- `console.log(err); return` — log and continue without classification
- `while (true) { try { ... } catch { } }` — unbounded retry
- `if (err.message.includes("not found"))` — string-matching errors
- Promise without `.catch` or async function without `try`
- `fetch(url)` with no timeout, no AbortController, no deadline
- No distinction between transient (retry) and permanent (escalate) failures
- "Error handling: TBD" anywhere in a contract

## Core Process

### Step 1: Inventory failure modes per component

For each component (service, module, integration), list every operation that can fail. For each:
- What goes wrong (network, validation, business rule, dependency, race)
- What state is left behind (partial write, dangling lock, orphan record)
- Who notices (user, ops, no one)

### Step 2: Classify each failure mode

Three classes:
- **Transient** — retry with backoff (network blips, rate limits, lock contention, 5xx from a dependency)
- **Permanent** — do not retry, escalate (bad input, 4xx, business rule violation, deleted resource)
- **User-correctable** — surface a non-technical message; the user can fix and retry (missing field, expired card, insufficient funds)

### Step 3: Assign handling pattern per class

| Class | Pattern |
|-------|---------|
| Transient | Exponential backoff with jitter, max attempts, deadline, idempotency key |
| Permanent | Wrap with structured error type, return upward, do NOT retry, alert if unexpected |
| User-correctable | Map to user-facing message in catalog, return 4xx, log only at DEBUG |

### Step 4: Write the error taxonomy

In `.forge/error-handling.md`:
- Named error types per class with conditions and HTTP/exit codes
- Retry config (max attempts, base delay, jitter, deadline) per call type
- Circuit breaker thresholds per dependency
- Timeout per external call (NEVER unbounded)
- User-facing message catalog with stable codes

### Step 5: Define logging + alerting per class

- Transient at INFO during retries, WARN after max attempts exceeded
- Permanent at ERROR, alert if rate exceeds threshold
- User-correctable at DEBUG (do not page humans for user typos)
- Cross-reference `observability` skill for correlation IDs

### Step 6: Write rollback / compensation for irreversible flows

For any operation that crosses a boundary (payment, email send, external write, queue publish):
- Define the idempotency key
- Define the compensation action if a downstream step fails
- Document the reconciliation job

### Step 7: Header

Prepend a `forge:meta` header to `.forge/error-handling.md` (`generated_by: error-handling-and-resilience`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/architecture.md]` — paths only, never hashes, `generated_from: {.forge/architecture.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] `.forge/error-handling.md` written
- [ ] Every external call in the codebase has an explicit timeout
- [ ] Every retry has max attempts + backoff + deadline
- [ ] Every error type has a class (transient / permanent / user-correctable)
- [ ] Every user-facing error has a non-technical message in the catalog
- [ ] No bare `catch (e) {}` in the codebase (grep verified)
- [ ] Every irreversible flow has a documented compensation path
- [ ] Circuit breaker thresholds defined for every external dependency
