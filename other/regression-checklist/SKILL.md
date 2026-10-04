---
name: regression-checklist
category: qa
description: Use after the targeted cases pass - choosing the adjacent behaviour this change can break from the PR's files and the component's links, and the per-repository smoke set
---
# Regression Checklist

After the targeted scenarios pass, run a quick regression sweep of adjacent behaviour. Choose what to sweep from:

- **The PR's changed files** (the named re-test-scope exception lets you read the file list, not the implementation).
- **`list_links`** — who else calls this component; a change to a shared API or schema can break every caller.
- **Shared surfaces** and their main consumers: tokens/layout, router, API client, auth/session, migrations/schema — a change here radiates wider than the task's own screen.

## Per-repository smoke set

Keep it in project memory (`search_memory "regression smoke"`) so it accumulates across rounds instead of being reinvented each time: app boots, login works, primary navigation works, the main create/read flow works, the landing page renders with no console errors (Lighthouse `errors-in-console` or a manual console check). When a regression escapes to UAT, extend the set with `save_memory` so the next round catches it.

## Visual adjacency

One screenshot at 360 and 1440 of the one or two most-used *unchanged* screens that share the changed component or design tokens — a token/layout change can break a screen nobody touched in this task.

## Recording

Record swept cases as `category: regression`.
