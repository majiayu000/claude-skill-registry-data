---
name: apple-app-intents
description: "Implement App Intents, App Entities, entity queries, App Shortcuts, and system actions with shared commands, authorization, process isolation, and runtime registration evidence."
---

# App Intents, entities, and system actions

## Inputs

Identify the user action, intent/entity types, process and actor, target membership, data access, authentication, confirmation, and supported system entry points.

## Rules

- **INT-001 — Share command semantics.** Resolve parameters then call the same validated domain command as the app UI; do not duplicate persistence or bypass authorization.
- **INT-002 — Separate registration and execution.** Compiled metadata, discoverability, entity resolution, and successful perform execution need distinct evidence.
- **INT-003 — Keep entity identity durable.** Use stable IDs and current account-scoped queries; handle deleted, unavailable, or unauthorized entities without recreating them.
- **INT-004 — Protect system surfaces.** Minimize display representations, suggestions, logs, and results; apply authentication/confirmation where the operation requires them.
- **INT-005 — Respect execution context.** Do not assume a foreground scene, initialized singleton, unrestricted background time, or shared in-memory state across processes.

## Workflow

1. Map the action to a typed command and authorization contract.
2. Define entity identifiers and query behavior for missing/stale data.
3. Verify target embedding, metadata extraction, and supported invocation modes.
4. Test from the real system surface and reconcile outcome with in-app state.

## Verify

Test cold invocation, locked/unauthenticated state, account switch, stale entity ID, cancellation, duplicate delivery, offline failure, and UI parity.

## Output

Return action/entity mapping, registration proof, tested invocation paths, and remaining account/device gates.

## References

- [Entities, commands, and invocation proof](references/entities-and-actions.md).
