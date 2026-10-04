---
name: jade-recipe-1.5-1.6-arrays-copyof
description: >-
  Replaces System.arraycopy() calls with Java 6 Arrays.copyOf()/copyOfRange().
  Handles three cases: same-source copy, destPos=0 copy, and non-zero
  destPos (leaves a NOTE comment). Invoked by jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-1.5-1.6-arrays-copyof — System.arraycopy → Arrays.copyOf

Java 6 introduced `java.util.Arrays.copyOf()` and `java.util.Arrays.copyOfRange()`,
which are more readable and less error-prone than `System.arraycopy()`.
This recipe replaces simple `System.arraycopy` calls with the new API.

## Automated transform (apply.py)

The `scripts/apply.py` subprocess handles three cases:

1. **Same source + destPos=0:** `System.arraycopy(arr, 0, arr, 0, newLen)`
   → `arr = java.util.Arrays.copyOf(arr, newLen)`

2. **Any source + destPos=0:** `System.arraycopy(src, sp, dest, 0, len)`
   → `dest = java.util.Arrays.copyOf(src, len)`

3. **Non-zero destPos:** Leaves the call as-is with a `// NOTE:` comment
   suggesting `Arrays.copyOfRange` for manual review.

The automated transform preserves the `// JADE-FLAG:ARRAYS_COPY_OF_UPGRADE` comment
in the trailing portion of the matched line. After applying, check that the flag
comment is cleaned up (the agent fallback step 7 handles this).

Note: `import java.util.Arrays` is **not** injected by apply.py. The agent must
add it manually — see agent fallback step 6.

## Agent fallback (when apply.py fails or the pattern is complex)

For each flagged `System.arraycopy` call:

1. Read the source file and the flagged line
2. Identify: source array, source position, destination array, destination position, length
3. **If destPos is 0:**
   - Replace with `destinationArray = java.util.Arrays.copyOf(sourceArray, length)`
   - If source and destination are the same, just: `arr = java.util.Arrays.copyOf(arr, newLen)`
4. **If destPos is non-zero:**
   - Replace with `System.arraycopy(src, srcPos, dest, destPos, length)` followed by
     `// NOTE: Consider Arrays.copyOfRange(src, srcPos, srcPos+length) for Java 6+`
5. **If the call is too complex to parse** (inline expressions, method calls as args):
   - Leave as-is with `// NOTE: Consider Arrays.copyOf/copyOfRange for Java 6+`
6. Add `import java.util.Arrays;` if not already present
7. Remove the `// JADE-FLAG:ARRAYS_COPY_OF_UPGRADE` comment

## Edge cases

- `System.arraycopy` inside a loop or conditional — the transform is still valid
- Non-literal arguments (method calls) — the regex may not parse; fall back to agent
- Source and dest are different arrays with non-zero destPos — use copyOfRange, add NOTE
