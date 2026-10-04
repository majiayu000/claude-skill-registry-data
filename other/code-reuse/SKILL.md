---
name: code-reuse
description: "Reuse before writing: find the existing function, util, hook, or component and extend it instead of adding a near-duplicate. Use when adding a helper or utility, consolidating duplicate or copy-paste code, or reviewing a diff for reuse."
license: MIT
metadata:
  display-name: "Code Reuse"
  version: "1.0"
  platforms: "claude-code codex"
  tags: "reuse duplication refactoring clean-code"
---

# Code reuse

Before writing a function, hook, component, or script, assume it already exists somewhere in the repo. Go find it.

## Search before you write

- Grep for the *concept*, not the name you were about to give it - the existing function probably isn't called what you'd call it.
- Check the project's existing dependencies before hand-rolling something a library already does.
- When you report the change, name the search you actually ran. "Grepped for `debounce`, `throttle`; found none" is a claim someone can check. "Nothing else did this" is not.

## Extend, do not fork

- A near-duplicate function with one different line is a sign the original needs a parameter, not a sibling.
- Exception: a boolean flag that switches between two behaviors is two functions wearing one name. Splitting them is not the duplication this skill is about - see `architect-review`'s flag-parameter rule.

## Rule of three, both directions

- Don't abstract at two instances - a two-case abstraction usually fits neither case well.
- Don't tolerate a third copy - by copy three, the shared shape is real. This is `architect-review`'s rule; this skill exists to catch the moment before copy two.

## What is not reuse

- A wrapper around one call site that will only ever have one call site.
- A re-export with no added behavior.
- Reaching into a `utils.ts` grab-bag because it's *there*, when nothing in it is related to the problem.
- Pulling in a new dependency to save five lines you could write directly.

## Finish the move

Delete the code the reuse replaced. Two implementations of the same job outlive their reason to exist far longer than anyone plans for.

## Reviewing for reuse

For every new function, file, or component in a diff, ask what already did this job. Answer with a symbol and a file path, or state plainly that you looked and found nothing.

## What this skill is not

Not DRY absolutism. Two call sites that happen to share five lines by coincidence, not by concept, are not duplication - forcing them to share a helper couples things that should be free to diverge.
