---
name: swiftui-interop
description: "Bridge SwiftUI with UIKit or AppKit using representables, hosting, coordinators, delegates, text systems, and explicit lifecycle ownership."
---

# UIKit and AppKit interoperability

## Inputs

Identify the concrete capability SwiftUI cannot currently provide, target platform/minimum, view ownership, delegate flow, sizing behavior, and teardown obligations.

## Rules

- **BRIDGE-001 — Bridge a capability, not the app.** Prefer native SwiftUI where it meets the need; use a narrow public-platform adapter when it does not.
- **BRIDGE-002 — Separate creation and update.** Create owned objects once per representable lifecycle; make updates idempotent and based on current inputs.
- **BRIDGE-003 — Keep callbacks current.** Coordinators and delegates must not retain stale bindings or recreate update feedback loops.
- **BRIDGE-004 — Tear down resources.** Release observers, delegates, tasks, and external resources; account for repeated removal and recreation.
- **BRIDGE-005 — Preserve platform semantics.** Respect main-actor UI ownership, focus, accessibility, sizing, responder chains, and controller containment.

## Workflow

1. Document the public API gap and the smallest adapter interface.
2. Define make/update/dismantle responsibilities and ownership of every callback.
3. Reconcile model-driven updates without echoing them as new user changes.
4. Support proposed sizing, focus, accessibility, and reparenting behavior.
5. Test lifecycle repetition and callback ordering before broad integration.

## Verify

Test initial creation, input changes, user callbacks, identity replacement, removal/recreation, repeated teardown, focus, resizing, accessibility, and memory/resource release.

## Output

Return the bridge contract, lifecycle map, reason native SwiftUI was insufficient, and focused tests.

## References

Read the [playbook](references/interop-patterns.md) for decisions, failure cases, and source links.

For representable updates and teardown, read the [focused reference](references/representable-lifecycle.md).
