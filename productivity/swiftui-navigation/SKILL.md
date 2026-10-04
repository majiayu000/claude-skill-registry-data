---
name: swiftui-navigation
description: "Build or fix SwiftUI NavigationStack, NavigationSplitView, tabs, sheets, deep links, route restoration, and scene-specific selection."
---

# Navigation and presentation

## Inputs

Identify platform, deployment minimum, hierarchy versus task presentation, scene ownership, route identifiers, and deep-link or restoration requirements.

## Rules

- **NAV-001 — Model meaning, not view instances.** Use lightweight stable route values or IDs; re-fetch current data and authorization at the destination.
- **NAV-002 — Match the container to the task.** Use stacks for hierarchy, split views for persistent selection/detail, tabs for peer destinations, and sheets for focused tasks.
- **NAV-003 — Own each presentation once.** Avoid independent flags that allow incompatible sheets. Give each scene its own route/selection unless shared navigation is intentional.
- **NAV-004 — Preserve native exits.** Keep back, cancel, dismissal, keyboard, and restoration behavior coherent. Do not persist a draft merely because a sheet closes.
- **NAV-005 — Validate external routes.** Parse untrusted URLs, allow supported destinations, resolve authentication, and handle deleted or inaccessible records.

## Workflow

1. Map the journey and presentation owner before choosing APIs.
2. Prefer typed routes for controlled navigation; register destinations in a stable scope outside lazy row creation.
3. Keep data-driven selection and navigation synchronized without circular update loops.
4. Define deep-link, cancellation, and restoration behavior, including unavailable destinations.
5. Test compact/expanded transitions and independent windows.

## Verify

Exercise push/back, repeated deep links, sheet switching, cancelled drafts, deleted selection, cold launch, restored invalid routes, and width changes. Check actual target availability instead of applying all modern APIs unconditionally.

## Output

Return the route/presentation model, ownership boundaries, fallback behavior, and journey tests.

## References

Read the [playbook](references/navigation-patterns.md) for decisions, failure cases, and source links.

For deep links, restoration, and presentation identity, read the [focused reference](references/routing-and-restoration.md).
