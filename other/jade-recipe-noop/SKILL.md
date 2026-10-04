---
name: jade-recipe-noop
description: >-
  Fallback recipe for rules with no specific transform. Marks flagged
  lines as SKIPPED — no source change needed. Used when the fix is
  informational (e.g., "LinkedList already implements Deque in Java 6").
  Invoked by jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-noop — No-Operation Fallback

Returns `SKIPPED` for every invocation. No source file is modified.

## When this skill applies

The dispatcher routes here when:
- A rule has no dedicated recipe skill registered
- The rule is informational (no code change required)
- The change was already addressed by a prior migration

## Agent fallback (when subprocess is unavailable)

1. Read the flagged file at the given `--line`
2. Read the manifest entry for the rule to understand what it flags
3. If the rule is informational (Java 6 already provides the feature):
   - Mark the file as SKIPPED — no code change needed
   - Optionally add a `// NOTE: <explanation>` comment for future readers
4. If the rule requires a transform but no recipe exists:
   - Mark as DEFERRED with `// JADE-MODERNIZATION-DEFERRED:<rule_id>`.
   - Write a summary of what the agent would need to do

## Edge cases

- Some manifest rules reference recipe skills that don't exist yet (e.g., an entry in
  the manifest with a `fix_strategy` like `recipe:jade-recipe-X-Y-feature` but no
  corresponding skill directory). These route through this fallback. The agent should
  read the manifest entry to understand what transform was intended.
