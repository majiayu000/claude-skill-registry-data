---
name: comment-cleanup
description: Remove AI-generated over-commenting, narration, and noise from code while preserving comments that carry real context (non-obvious "why", invariants, workarounds, gotchas). Use when the user asks to clean up comments, reduce comment verbosity, remove narration, or says a diff/file has too many comments — or periodically after a multi-file implementation session, since prevention rules alone (CLAUDE.md) do not fully stop verbose commenting.
---

# Comment Cleanup

Claude Code has a well-documented tendency to write verbose, narrating comments
even when a CLAUDE.md rule says not to (see [anthropics/claude-code#65961](https://github.com/anthropics/claude-code/issues/65961)).
Upfront rules reduce the *ratio* of comments but barely reduce large comment
blocks. This skill is the cleanup half — run it periodically, don't rely on
prevention alone.

## Hard scope boundary

**Edit comments only. Never touch code in this pass.**

- No renames, no extractions, no logic changes, no "improvements" to the code
  itself — even when a comment only exists because the code is unclear. If a
  comment is load-bearing because the code is confusing, flag it to the user
  instead of silently rewriting the code to make the comment unnecessary.
- Every edit in this pass must be comment-only. If you find yourself wanting
  to change a non-comment line, stop and note it as a separate suggestion —
  don't do it here.

## What to remove

- **Narration**: comments that restate what the next line does ("increment
  the counter", "loop over users", "return the result").
- **Diff/task references**: "used by the X flow", "added for issue #123",
  "fix for the bug where...", "changed to support Y" — these rot as the
  codebase evolves and belong in the commit message, not the code.
- **Restated signatures**: a comment above a function that just repeats its
  name and parameters in prose.
- **Boilerplate doc-comment padding**: multi-paragraph docstrings/doc-comments
  for simple, self-explanatory functions where the signature already says it
  all.
- **Redundant section banners**: `// ---- Helpers ----` above a single
  three-line helper, decorative comment blocks.

## What to keep

- A hidden constraint, invariant, or non-obvious reason the code is written
  this way (a subtle race condition, a platform quirk, "must run before X or
  Y breaks").
- A workaround for a specific external bug, with enough detail to know when
  it's safe to remove.
- `TODO`/`FIXME` markers that are still actionable (not already done).
- Legitimate public API documentation (rustdoc `///`, JSDoc, docstrings on
  exported/public items) that consumers actually read — trim narrative
  padding inside these, but don't strip documentation that serves external
  callers, license headers, or SPDX notices.
- Safety comments on `unsafe` blocks or anything documenting an invariant a
  compiler can't check.

## Workflow

1. **Determine scope.** Default to the current diff (`git diff` /
   `git diff --staged`) if inside a git repo and nothing else is specified.
   If the user names specific files/paths, use those instead. If asked for a
   full sweep, scan the whole file(s), not just changed lines.
2. **Walk every comment in scope.** For each one, classify it against the
   "remove" and "keep" lists above. When genuinely ambiguous, default to
   removing — the cost of a lost comment is low (git history has it), the
   cost of noise compounds every time the file is read again.
3. **Edit comments only**, per the hard scope boundary. Use the smallest
   diff that removes the noise — delete the comment line, don't rewrite
   surrounding code to compensate.
4. **Report a short summary**: how many comments removed vs. kept, and why
   any kept comment was judged non-obvious enough to survive. Don't just say
   "cleaned up comments" — name the load-bearing ones you kept so the user
   can sanity-check the judgment calls.

## Example

```rust
// Before
// Increment the retry counter by one before checking the limit
retry_count += 1;
// Check if we've exceeded the max retries and bail if so
if retry_count > MAX_RETRIES {
    return Err(Error::TooManyRetries);
}

// After
retry_count += 1;
if retry_count > MAX_RETRIES {
    return Err(Error::TooManyRetries);
}
```

A kept comment looks like: `// raw pointer here, not the safe API — the safe
API allocates every call, which was 40% of profile time in this hot loop`.
Non-obvious "why", short, survives.
