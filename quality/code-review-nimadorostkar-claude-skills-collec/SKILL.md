---
name: code-review
description: Use when reviewing a pull request, diff, or branch. Produces severity-ranked findings covering correctness, security, performance, and maintainability, with concrete fixes rather than opinions.
metadata:
  category: development
  version: 1.0.0
  tags: [code-review, pull-request, quality, security]
---

# Code Review

## Purpose

Review changes the way a senior engineer does: correctness first, then security, then performance, then design, then style. Every finding carries a severity, a reason, and a fix.

## When to Use

- Reviewing a pull request or a local diff before pushing.
- Auditing a branch before merge to a protected branch.
- Reviewing someone else's code in an unfamiliar area of the codebase.

## Capabilities

- Correctness analysis: edge cases, off-by-one, null and error paths, concurrency.
- Security review: injection, authorization gaps, secret exposure, unsafe deserialization.
- Performance review: N+1 queries, unbounded allocations, blocking calls on hot paths.
- Design review: coupling, layering violations, missing abstractions, premature ones.
- Test review: whether the tests would actually fail if the code were wrong.

## Inputs

- A diff, PR number, or branch reference.
- The surrounding code, not just the changed lines.
- The intent of the change: linked issue, PR description, or a one-line summary.

## Outputs

A review with findings grouped by severity:

- **Blocking** — Correctness, security, or data-loss defects. Must be fixed before merge.
- **Should fix** — Design or performance problems that will cost more later than now.
- **Consider** — Improvements that are genuinely optional.

Each finding states the file and line, what is wrong, why it matters, and a suggested fix.

## Workflow

1. **Understand the intent** — Read the PR description and the issue. A change that does something other than what it claims is the first finding.
2. **Read the diff in context** — Open the surrounding functions. Most defects live in the interaction between changed and unchanged code.
3. **Trace the failure paths** — For each new branch: what happens when the input is empty, null, malformed, or hostile? What happens when the network call fails?
4. **Check the boundaries** — Anything crossing a trust boundary (HTTP, queue, file, DB) must be validated on the way in and encoded on the way out.
5. **Assess the tests** — Would the new tests fail if the implementation were subtly wrong? If not, they are coverage, not verification.
6. **Rank and report** — Sort findings by severity. Lead with the ones that block.

## Best Practices

- Review the code, not the author. Write "this returns before closing the file", not "you forgot to close the file".
- Do not report style issues that a formatter should own. Fix the formatter config instead.
- One blocking finding stated clearly beats twenty nitpicks that bury it.
- If the design is wrong, say so early and stop line-by-line reviewing. Detailed feedback on code that should be deleted wastes everyone's time.
- Approve when the change is better than what exists. Perfection is not the bar; regression is.
- Quote the exact line. A finding without a location is not actionable.

## Examples

**A well-formed finding:**

> **Blocking — `api/orders.py:88`**
> `total` is computed from `request.json["items"]` without validating quantities, so a negative quantity produces a negative total and a credit to the customer's card.
> Validate `quantity >= 1` in the request schema, and assert `total > 0` before charging.

**A finding that is not actionable:**

> ~~"The order logic feels a bit fragile."~~

## Notes

- Automated tools should catch formatting, unused imports, and obvious lint violations before a human reads the diff. If they are reaching review, fix the pipeline, not the PR.
- Large PRs receive worse reviews. If a diff exceeds roughly 400 lines, reviewing it as one unit is unreliable — ask for it to be split.
- A review that finds nothing is a valid outcome, but say what you checked.
