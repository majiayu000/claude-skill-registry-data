---
name: hig-navigation
description: "Repair information architecture, wayfinding, search, navigation continuity, and task flows without deleting existing capabilities."
---

# Make location, scope, and next steps predictable

Follow the [root contract](../../SKILL.md). Load relevant cards in [apple-rule-cards.md](../../references/apple-rule-cards.md): HIG-008, HIG-009, HIG-010, APPLE-002. Detailed sidebar and search-field HIG pages remain fresh-read topics; do not pretend this pack contains every variant.

## Establish the navigation model

Identify destinations, content hierarchy, actions, and transient tasks. Draw the current route graph, including deep links and permission-dependent destinations. A creation action is not automatically a destination; a filtered result set is not automatically a new top-level section.

Record each destination’s title, entry methods, parent, return behavior, preserved state, and unavailable states. Check the user’s mental categories against product terminology rather than copying backend table names. Preserve stable paths and bookmarks, or provide an explicit migration when authorized.

## Choose the least disruptive repair

Use a local label or placement fix when the structure is sound. Use a shared navigation component repair when selection, focus, or spacing breaks consistently. Propose structural IA changes only when users cannot predict grouping or reach important tasks and the evidence is stronger than a stylistic preference.

For each proposed merge, move, or removal, provide the old-to-new capability map. Important features must remain reachable by an understandable route. Preserve expert shortcuts when they do not harm the primary flow.

For platform selection, consult the current HIG rather than treating bottom tabs, sidebars, or toolbar positions as universal. On the web, distinguish links that navigate to pages from tabs that switch related panels; implement appropriate native link or tab behavior instead of assigning one ARIA role to both.

## Search repair protocol

Write a search contract before styling:

- **Scope:** global product, collection, current list, selected folder, or detail view.
- **Input:** known-item lookup, open-ended discovery, structured filter, or mixed.
- **State:** query, selected filters, sorting, pagination/cursor, active suggestion, and results.
- **Transitions:** submit, clear, cancel, refine, open result, return, and restore.
- **Outcomes:** idle, suggestions, loading, results, no matches, failure, and insufficient access.

Choose placement based on the navigation model and scope. Review Apple’s 2026 search session for native pattern differences, including dedicated search destinations and prominent search entry. Do not copy an iOS search animation onto a desktop website without a task-based reason.

Make active filters visible and removable. Distinguish a query with zero matches from a failed request and a collection that has no data yet. Do not silently broaden a scoped search, discard filters, or report a truncated result set as exhaustive.

Inspect concurrent requests: a slow response for an earlier query must not overwrite a later query’s results. Cancellation, request identity, and URL/state ownership belong in the implementation contract. Suggestions must be operable with the actual supported inputs; do not create a custom combobox without verifying its complete keyboard and assistive behavior.

## Continuity tests

Open a result, return, and compare query, filters, sort, page, scroll position, and focus against the documented contract. Repeat through browser history, an external deep link, a tab/destination switch, and an expired session where relevant. Not all state should persist forever: record expiry and privacy expectations.

For nested flows, distinguish Back, Cancel, Close, and Done. Verify whether each abandons a transaction, dismisses presentation, saves work, or returns to a parent. A modal should not become the only escape from a broken navigation hierarchy.

Test long/localized labels, missing titles, duplicate names, empty sections, restricted resources, deleted content, and compact windows. Check that selected location and result context remain understandable without relying on color alone.

## Output and gate

Deliver the current/proposed flow map, source-qualified component choices, old-to-new capability mapping, state-restoration contract, and test cases. A pass requires reachable destinations, unambiguous scope, predictable return behavior, and no unauthorized loss of features or deep links.
