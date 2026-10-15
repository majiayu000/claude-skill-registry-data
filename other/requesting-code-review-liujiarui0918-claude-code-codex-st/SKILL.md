---
name: requesting-code-review
description: Use BEFORE handing off / committing. Self-review checklist to run between tasks.
---

# Requesting Code Review

Before another set of eyes — yours or a reviewer's — do the cheap pass yourself. Self-review catches 60% of issues without burning anyone else's attention.

## When to run this

- Before `git commit`
- Before opening a PR
- Before handing work off to another agent / human
- Before invoking the `code-reviewer` subagent (don't waste its budget on lint issues)

## Iron Law

**Read your own diff before anyone else does.** Open the diff, scroll top-to-bottom, every line. No skipping.

## Self-Review Checklist

### Correctness
- [ ] Tests pass (see [[verification-before-completion]] — don't assume)
- [ ] The change actually does what the task asked
- [ ] Edge cases handled: empty input, null, zero, negative, very large, unicode
- [ ] Error paths considered — not just the happy path

### Cleanliness
- [ ] No `print` / `console.log` / `Write-Host` debug statements left behind
- [ ] No commented-out code blocks ("might need later" — no, delete it, git remembers)
- [ ] No TODOs added without a ticket / follow-up
- [ ] No dead code (unreachable branches, unused imports/vars)

### Naming & Clarity
- [ ] Variable / function names communicate intent, not type (`userList` not `arr`)
- [ ] No abbreviations only you understand
- [ ] Functions do one thing; if a name needs "and", split it

### DRY / Reuse
- [ ] Not duplicating an existing helper — searched the codebase first
- [ ] If duplicating intentionally (different abstraction), noted why
- [ ] Not introducing a third copy of something — extract instead

### Error Handling
- [ ] Failures throw / return meaningfully (not swallowed)
- [ ] Resources released on error path (files closed, connections returned)
- [ ] User-facing errors are actionable, not stack traces

### Security
- [ ] No hardcoded secrets / tokens / passwords
- [ ] User input validated before use in query / shell / path
- [ ] Authn / authz check on any new endpoint or sensitive path
- [ ] Dependencies are pinned and from trusted sources

### Diff Hygiene
- [ ] Diff is the *minimum* needed for the task
- [ ] No unrelated reformatting (that goes in a separate commit)
- [ ] No accidental file deletions / renames
- [ ] Generated files / build artifacts not committed

## Red Flags during self-review

- "I'll clean that up later" — clean it now, "later" is a lie.
- "This part is ugly but it works" — reviewer will land on exactly that line.
- Files in the diff you didn't intend to touch.
- A function over ~50 lines you added in one sitting.
- A test you wrote that has never seen the code fail.

## After self-review

1. Fix what the checklist flagged.
2. Re-run verification ([[verification-before-completion]]).
3. *Now* invoke the `code-reviewer` agent / open the PR / hand off.
4. Approach feedback per [[receiving-code-review]].

## MUST

You MUST run the checklist top-to-bottom. Cherry-picking items defeats the point — the items you skip are the ones that catch you.

## Cross-references

- [[verification-before-completion]] — verification is a prerequisite, not a substitute.
- [[receiving-code-review]] — how to handle the feedback you'll get next.
- [[finishing-a-development-branch]] — self-review is part of wrap-up.
