---
name: jade-recipe-1.5-1.6-deque-retrofit
description: >-
  Informational rule. LinkedList already implements Deque in Java 6.
  No code change required. Invoked by jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-1.5-1.6-deque-retrofit

Java 6 added the `java.util.Deque` interface, and `java.util.LinkedList`
already implements it. No source code change is required.

## Automated transform (apply.py)

Returns `SKIPPED` for every file — informational rule only.

## Agent fallback

1. Verify the flagged file uses `LinkedList`
2. Confirm the code compiles on Java 6+ (LinkedList implements Deque natively)
3. Mark as SKIPPED — no transform needed
4. Optionally replace `List<X> x = new LinkedList<>()` with `Deque<X> x = new LinkedList<>()` if the variable is used only with Deque methods
