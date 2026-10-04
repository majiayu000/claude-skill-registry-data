---
name: pr-reviewer
description: Review gate for correctness, reuse, and simplification. Produces a structured verdict with actionable findings. Trigger on any PR before merge, or on any agent-generated code before it is committed.
---

# PR Reviewer

> **Receipts, not polish.** A review that says "looks good" is not a review. A review that says "line 47 will panic on a nil pointer and here is the fix" is a review.

This skill runs a structured code review and produces a verdict: approve, approve with comments, or request changes. Every finding is actionable. No findings without evidence.

## When to use

- Before merging any PR
- When reviewing agent-generated code before committing
- When a significant refactor or new feature is complete
- As part of the `release-readiness` checklist

## Procedure

1. **Scope the review** — fetch the diff. Identify:
   - Files changed and their purpose
   - The stated intent of the PR (what problem does it solve?)
   - Any linked spec, issue, or ADR

2. **Correctness pass** — look for bugs, not style:
   - Null / nil / undefined access on values that could be absent
   - Off-by-one errors in loops or index operations
   - Error returns that are silently ignored
   - Race conditions if the code is concurrent
   - Missing input validation at trust boundaries (user input, external API responses)
   - Logic that diverges from the stated intent of the PR

3. **Reuse pass** — look for duplication:
   - Does this code reimplement something that already exists in the codebase?
   - Is there a stdlib or already-installed dependency that does this?
   - Can the new code be expressed using an existing abstraction?

4. **Simplification pass** — look for unnecessary complexity:
   - Can this be fewer lines without losing clarity?
   - Is there an abstraction that has only one implementation? (remove it)
   - Is there a dependency added for something a few lines of code would do?
   - Is there "scaffolding for later" that should not exist yet?

5. **Security and data boundary pass** — look for:
   - Secrets or credentials in code or logs
   - User-controlled input reaching a shell, SQL query, or file path without validation
   - Data crossing a tenant or trust boundary without an explicit check
   - Missing authentication or authorisation checks on new endpoints

6. **Classify findings**:
   - **BLOCKING**: must be fixed before merge (correctness bugs, security issues)
   - **SUGGESTED**: improvement worth making but not a blocker (simplification, reuse)
   - **NOTE**: observation for awareness, no action required

7. **Produce the verdict**:
   - **Approve**: no BLOCKING findings
   - **Approve with comments**: no BLOCKING findings, SUGGESTED improvements noted
   - **Request changes**: one or more BLOCKING findings

## Outputs

- Finding list: location | severity | description | suggested fix
- Verdict: Approve / Approve with comments / Request changes

## Independent second reviewer (on demand)

The writer never approves its own work. Before merging, get a verdict from a different model or a fresh reviewer subagent: `scripts/review-gate.sh --pr N` (Gemini 3.8 flash high via the `agy` or `gemini` CLI; posts the verdict on the PR) or `--staged` for what the next commit will contain. It is on demand, not a hook default, because teams work on different machines; a clone can opt in with `git config review.gate async|block`. A changed candidate gets a fresh review; `VERDICT: NONE` (lane unavailable) is never an approval.

## Guardrails

- **Every BLOCKING finding must have a suggested fix.** "This is wrong" is not actionable.
- **Style is not a BLOCKING finding.** Style enforcement belongs in the linter, not the review.
- **Reuse requires evidence.** "This might already exist" is not a finding. Find it or drop the comment.
- **The review is not a rewrite.** Surface the issues; let the author fix them.

---

See also: [`REFERENCE.md`](./REFERENCE.md) for a quick lookup of common patterns and their preferred alternatives.
