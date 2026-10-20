---
name: write-less-code
description: >-
  The write-less-code minimalism standard: the full ladder and what never to simplify away.
disable-model-invocation: false
user-invocable: false
license: MIT
---

# Write less code

The best code is the code never written. This skill is the _positive_ half of
minimalism — what to reach for first. The `agent-coding-contract` skill owns the
_negative_ half (no new dependencies, no speculative abstractions, minimal
diffs); apply both, don't restate it here.

## Procedure

Before writing any code, stop at the first rung that holds:

1. **Does this need to exist at all?** Speculative need → skip it, say so in one line. (YAGNI)
2. **Stdlib does it?** Use it.
3. **Native platform feature covers it?** `<input type="date">` over a picker lib, CSS over JS, a DB constraint over app code, an HTTP cache header over a cache layer.
4. **Already-installed dependency solves it?** Use it. Never add a new dependency for what a few lines do.
5. **Can it be one line?** One line.
6. **Only then:** the minimum code that works.

The ladder is a reflex, not a research project. Two rungs work → take the higher
one and move on. The first lazy solution that works is the right one.

Rungs 4 and 6 fail most often because nobody looked. Before writing custom code, spend one search:
grep the repo for a helper that already does it, read the dependency manifest for an installed
package that does, and check the session's skill list for one that covers the task. Search a
package registry only when the user has allowed a new dependency.

## Rules

- No unrequested abstractions: no interface with one implementation, no factory for one product, no config for a value that never changes.
- Deletion over addition. Boring over clever — clever is what someone decodes at 3am. Fewest files; shortest working diff wins.
- Complex request? Ship the lazy version and question it in the same response: "Did X; Y covers it. Need full X? Say so." Never stall on an answer you can default.
- Two stdlib options the same size? Take the one correct on edge cases. Lazy means less code, not the flimsier algorithm.
- Check at the boundary, trust inside. Parse and validate input once, where it enters, into a type that cannot hold a bad value. Code past the boundary takes that type and does not re-check, because repeated defensive checks are code nobody can prove reachable.
- Count what a reader must hold in mind, not lines. Fewer names, layers, and flags in play at once beats a shorter file that makes the reader jump between five.
- Mark deliberate simplifications with a `// less-code:` comment so a shortcut reads as intent, not ignorance. If the shortcut has a known ceiling (global lock, O(n²) scan, naive heuristic), the comment names the ceiling and the upgrade path: `# less-code: global lock; per-account locks if throughput matters`.

### When not to be lazy

Never simplify away: input validation at trust boundaries, error handling that
prevents data loss, security measures, accessibility basics, anything explicitly
requested. User insists on the full version → build it, no re-arguing.

Non-trivial logic (a branch, a loop, a parser, a money/security path) earns ONE
runnable check — the smallest thing that fails if the logic breaks: an
`assert`-based self-check or one small test file. No frameworks, no fixtures.
Write it only when tests are in scope; otherwise suggest it in one line.
Trivial one-liners need no test; YAGNI applies to tests too.

## Output

Code first. Then at most three short lines: what was skipped, when to add it. If
the explanation is longer than the code, delete the explanation — every
paragraph defending a simplification is complexity smuggled back as prose.

Pattern: `[code] → skipped: [X], add when [Y].`

---

_Inspired by [ponytail](https://github.com/DietrichGebert/ponytail) (MIT, DietrichGebert)._
