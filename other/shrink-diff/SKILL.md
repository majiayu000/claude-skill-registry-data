---
name: shrink-diff
description: >-
  Load this skill when a feature branch works and its diff against main should shrink before
  review: duplication it added, single-caller wrappers, code it made dead. Trigger on "shrink the
  diff", "consolidate the branch". Not for whole-codebase cleanup (use refactor-repo).
argument-hint: "[base-branch]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a feature branch in a git working tree, since the whole skill
  reads `git diff main...HEAD`. Verifying the shrunk diff additionally needs whatever runtime and
  test runner the target repo already uses - none is assumed.
license: Apache-2.0
---

# Shrink diff

`write-less-code` fires at write time, inside one session. Code accreted across sessions and
commits escapes it: session three writes a helper session one already had, a later commit leaves
a wrapper with one caller, an early abstraction outlives its need. This skill applies the same
standard retroactively — one pass over the finished diff, before it goes to review.

Claude Code's built-in `/simplify` already reviews changed code for reuse and simplification. This
skill adds what it does not carry: the write-less-code ladder as the yardstick, the whole branch
against its base as the scope, and behavior preservation as the gate on every edit.

## Procedure

### Scope

The seed set is everything the branch changed relative to the base branch (the argument, default
`main`):

```bash
git diff --stat <base>...HEAD        # size baseline (three dots: merge-base, not the base tip)
git diff --name-only <base>...HEAD   # seed files
```

- Empty diff → report "nothing to shrink" and stop.
- The unit of work is the symbol (function, class, block), not the line: a symbol the branch
  touched is in the seed even where some of its lines predate the branch.

**Read anything; edit outside the seed only with cause.** The three causes:

1. **Dedupe** — seed code duplicates an existing helper; merge into the existing one, adjusting
   it if needed.
2. **Inline** — the branch left an out-of-seed helper with a single remaining caller; inline it.
3. **Dead code** — the branch made out-of-seed code unreachable; delete it.

Flag every out-of-seed edit in the summary with its cause. Anything beyond these three causes is
general cleanup — out of scope here; suggest `refactor-repo` instead.

### The retroactive ladder

Walk each piece of code in scope down the write-less-code ladder, in hindsight:

1. **Does it need to exist at all?** Dead code, an unused parameter or flag, a speculative hook
   nothing calls → delete it.
2. **Stdlib does it?** Replace the custom version.
3. **Native platform feature covers it?** Replace the custom version.
4. **An already-installed dependency solves it?** Replace the custom version. Never add a new
   dependency to shrink code: its install, supply-chain, and upgrade cost outlasts the lines saved.
5. **Can it be one line?** Make it one line.
6. **Only then:** keep it, as the minimum that works — collapse single-implementation
   abstractions, inline single-caller wrappers, turn config-for-a-constant back into a constant.

### The hunt

For each seed symbol, in order of payoff:

1. **Duplication against the repo** — before accepting new code as novel, search for an existing
   equivalent (similar names, signatures, call patterns). The highest-value finds are
   cross-session: a later commit re-implementing what an earlier one — or pre-existing code —
   already had.
2. **Dead weight the branch created** — replaced call sites, orphaned helpers, parameters and
   flags nothing passes anymore, branches now unreachable.
3. **Structure** — single-implementation interface → collapse; single-caller wrapper → inline;
   config for a value that never changes → constant.
4. **Ladder violations** — custom code a higher rung replaces.

Rank candidates by payoff (lines removed, readability gained) over risk; apply top-down. A
candidate whose own diff would blow past reviewability (the size limits in
`ceh-git-workflow:pull-request`) gets flagged, not applied.

## Rules

### Behavior preservation

A refactor changes shape, never behavior:

- Never mix a behavior change into a refactor. If shrinking reveals a bug, report it — fixing it
  is separate work.
- Where tests cover the touched code, run them before and after; both runs must be green. A red
  before-run is a finding to report, not a license to proceed.
- Where no tests cover it, apply only mechanical transforms (delete provably-dead code, inline,
  rename, extract) and flag anything riskier instead of applying it.
- For anything past a mechanical transform — an extraction across files, an implementation swap, a
  dependency or runtime upgrade — pin current behavior first with
  `ceh-testing:verify-behavior-preserved` (characterization tests, golden files, differential run)
  and commit those pins on their own before touching the code. A green existing suite is the weaker
  check: it only proves what it already covered.
- Commit refactors with the `refactor:` type, separate from any other change.

## Output

End with the before/after `git diff --stat <base>...HEAD` totals, the candidates applied, the
candidates flagged but not applied (with why), and every out-of-seed edit with its cause.
