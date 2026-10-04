---
name: jade-recipe-1.5-1.6-navigable-set-map
description: >-
  Informational rule. TreeSet/TreeMap already implement NavigableSet/
  NavigableMap in Java 6. No code change required. Invoked by
  jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-1.5-1.6-navigable-set-map

Java 6 added `java.util.NavigableSet` and `java.util.NavigableMap` interfaces.
`java.util.TreeSet` and `java.util.TreeMap` already implement them natively.
No source code change is required.

## Automated transform (apply.py)

Returns `SKIPPED` for every file — informational rule only.

## Agent fallback

1. Verify the flagged file uses `TreeSet` or `TreeMap`
2. Confirm the code compiles on Java 6+ (these classes implement Navigable* natively)
3. Mark as SKIPPED — no transform needed
4. Optionally retype variables from `SortedSet`/`SortedMap` to `NavigableSet`/`NavigableMap`
   if the code uses navigation methods (ceiling, floor, higher, lower, etc.)
