---
name: jade-recipe-1.7-strings-in-switch
description: >-
  Converts .equals() if-chains to Java 7 switch statements.
  Handles sequential if-return and if-else-if-else patterns.
  Defers unconvertible single branches via JADE-MODERNIZATION-DEFERRED.
  Removes JADE-FLAG:STRINGS_IN_SWITCH comments on success.
  Invoked by jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-1.7-strings-in-switch

Converts multi-branch `if (var.equals("X"))` chains to `switch (var)` with
string case labels. Two patterns supported:

- **Sequential if-return:** `if (v.equals("A")) return ...; if (v.equals("B")) return ...;`
- **If-else-if-else:** `if (v.equals("A")) {...} else if (v.equals("B")) {...} else {...}`

Single-branch flags are deferred via `JADE-MODERNIZATION-DEFERRED:STRINGS_IN_SWITCH`
for manual review.
