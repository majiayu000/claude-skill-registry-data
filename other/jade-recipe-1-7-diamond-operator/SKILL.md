---
name: jade-recipe-1.7-diamond-operator
description: >-
  Replaces explicit generic type arguments with Java 7 diamond operator (<>).
  Scans +/-2 lines for the pattern, skips already-converted lines.
  Removes JADE-FLAG:DIAMOND_OPERATOR comments. Atomic write.
  Invoked by jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-1.7-diamond-operator

Converts `new HashMap<String, String>()` → `new HashMap<>()` for Java 7
type inference. Handles the edge case where the flag comment is adjacent
to (not on) the matched line. Skips lines already using `<>`.
