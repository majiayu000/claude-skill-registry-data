---
name: documentation-hygiene
description: Use when reviewing documentation quality, when establishing README and changelog standards, when preventing doc rot, when in-code comments duplicate code instead of explaining intent, or when subdirectories of a repo have no documentation entry point.
---

# Documentation Hygiene

## Overview

Define the project's documentation contract — what gets documented, where it lives, how it stays current — *before* docs rot. Output is `.forge/docs-policy.md`: README standard per repo and subdirectory, in-code comment policy (WHY not WHAT), doc-rot prevention rules (dates, code links, generated docs), public-vs-internal doc split, and changelog discipline. Pairs with `code-review-and-quality` (review enforces the policy) and `shipping-and-launch` (CHANGELOG updated per release).

## When to Use

- A repo is older than 3 months and the README hasn't been touched since the first commit
- Subdirectories have grown to 5+ files with no entry-point doc
- In-code comments are mostly restating the code instead of explaining intent
- A new contributor takes >2 hours to figure out where things live
- A release shipped without a CHANGELOG entry
- A doc references a system that no longer exists

## When NOT to Use

- Greenfield project, day one — README will exist; full policy can wait until week 2
- Throwaway prototype
- A single typo fix in one doc

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "The code is self-documenting" | Code shows *what*, not *why*. Two months later the original author cannot reconstruct why. |
| "Docs get stale anyway, why bother" | Dated docs with code links rot slower than undated docs. The half-life of a comment near its code is years; far from its code, weeks. |
| "README is enough" | README without subdirectory docs creates a treasure hunt for every new contributor. |
| "We'll document before launch" | You won't. And if you do, the doc will be wrong because you'll write it from memory. |
| "Comments are noise" | Comments that explain WHY are signal. Comments that restate the code are noise. The fix is to write the right comments, not to delete all comments. |
| "Generated docs are good enough" | Generated docs answer "what does this function take" — not "when should I call it" or "what changes if I don't." |

## Red Flags

- A README that hasn't been touched since the repo was created
- A subdirectory with 10+ files and no entry-point doc
- A comment that restates the code: `// increment i by 1` next to `i++`
- A doc with no last-updated date or commit reference
- A dead link in any doc (broken internal link or 404 external)
- A CHANGELOG missing entries for the last 2 releases
- A doc describing a system that was deleted or renamed 3 months ago
- "TODO: document this" markers older than 90 days

## Core Process

### Step 1: Define the README standard

In `.forge/docs-policy.md`, the README contract for every repo top-level:

```markdown
# <project name>
One-sentence description.

## What this is
2-3 sentence description.

## Status
Stable / Beta / Experimental — and what that means for breaking changes.

## Quick start
The single command (or 3) that gets a developer running.

## Where things live
Pointers to subdirectory READMEs.

## Contributing
How to propose a change. Link to CONTRIBUTING.md if it exists.

## License
SPDX identifier.
```

For every subdirectory with >5 files: a README that answers "what is in here, why is it here, who owns it."

### Step 2: Set the in-code comment policy

The rule: **explain WHY, not WHAT.**

| Bad (WHAT) | Good (WHY) |
|---|---|
| `// increment i` | `// skip the sentinel row at index 0` |
| `// loop over users` | `// fan-out concurrency capped at 5 to respect upstream rate limit` |
| `// returns null` | `// returns null when the user has been soft-deleted; callers must filter` |
| `// magic number 86400` | `// 86400 = 24h in seconds; matches the auth token TTL in config.ts` |

Comments are required for:
- Non-obvious algorithmic choices (why this sort order, why this caching)
- Workarounds (`// workaround for issue-1234 in upstream-lib v3.x`)
- Cross-file invariants (`// invariant: ordersByUser is updated by users.ts:create()`)
- Hot-path performance decisions

Comments are forbidden for:
- Restating the obvious
- Commented-out code (delete it; git remembers)
- Personal opinions

### Step 3: Establish doc-rot prevention

Every doc carries:
- **Last-updated date** at the top (or a `<!-- updated: YYYY-MM-DD -->` footer)
- **Code links** that resolve at HEAD (use permalinks to `main`, not commit hashes) — if the link 404s, CI fails
- **A scope statement** — what this doc covers, what it doesn't
- **An owner** — a person or team responsible for keeping it current

Prefer generated docs (typedoc, rustdoc, godoc) for API reference. Hand-written docs for *concepts*, *workflows*, and *decisions* (ADRs).

### Step 4: Define the public-vs-internal doc split

In `.forge/docs-policy.md`:
- **Public docs** — user-facing, marketing-grade, versioned (cross-ref `api-design` for endpoint docs)
- **Internal docs** — engineering-facing, in-repo, allowed to assume context (`CONTRIBUTING.md`, ADRs, runbooks)
- **Confidential docs** — credentials, customer data, financials — never in the repo

Each doc has a banner indicating its tier.

### Step 5: Set changelog discipline

Follow [Keep a Changelog](https://keepachangelog.com): one entry per user-visible change, grouped by `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Breaking changes flagged with `BREAKING:` prefix. Refactors don't get entries unless they affect performance, security, or behavior. Updated *in the PR that makes the change*, not at release time.

### Step 6: Audit for dead links and stale docs

CI job runs weekly:
- Check every internal link resolves
- Check every external link returns 2xx
- Flag any doc with last-updated > 180 days where the linked code has changed since
- Flag any TODO older than 90 days

Failures open tickets, not block CI (these are guideposts, not gates).

## Verification

- [ ] `.forge/docs-policy.md` written
- [ ] Every repo top-level has a README following the standard
- [ ] Every subdirectory with 5+ files has a README
- [ ] No comment in the codebase restates obvious code (spot-check via review)
- [ ] No commented-out code in the codebase (grep `^// .*[a-zA-Z(]` for obvious patterns)
- [ ] Every doc has a last-updated date and an owner
- [ ] CHANGELOG entries exist for the last 5 releases, grouped by Keep-a-Changelog categories
- [ ] No dead links in any in-repo doc (CI verified)
- [ ] No TODO comments older than 90 days without a tracking issue
