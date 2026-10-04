---
name: review
description: "Review a diff, commit, branch, PR, or implementation for actionable correctness and risk issues without duplicate reviewer loops or invented findings."
---

# Review

Review the code against its intended behavior and repository reality. Findings come before praise, process narration, or stylistic preference.

## Establish the review target

Determine:

- Diff, commit range, branch, PR, or files in scope
- Requested behavior or acceptance criteria
- Applicable repository instructions
- Relevant tests, schemas, or contracts
- Baseline branch when needed
- The applicable authorized goal and programme authority when the change can reorder work, widen a trust boundary, or introduce generalized infrastructure

Inspect enough surrounding code to understand the change. Do not review a diff in isolation when its correctness depends on state or callers.

## Review priorities

Look for:

1. **Correctness**
   - Wrong state transitions
   - Stale or inconsistent data
   - Edge cases
   - Error handling
   - Partial failure behavior

2. **Data and compatibility**
   - Schema drift
   - Migration safety
   - Backward compatibility
   - Serialization or pagination contracts
   - Idempotency

3. **Security and privacy**
   - Authorization
   - Input validation
   - Secret or sensitive data exposure
   - Injection or unsafe execution
   - Trust-boundary errors

4. **Concurrency and performance**
   - Races
   - Lost updates
   - Unbounded work
   - N+1 behavior
   - Expensive hot paths

5. **Tests and verification**
   - Missing regression coverage
   - Tests that cannot catch the bug
   - Assertions tied to implementation details
   - Unverified platform or migration behavior

6. **Complexity**
   - New abstractions without a present use
   - Duplicate sources of truth
   - Hidden coupling
   - A simpler implementation that reduces risk

Ignore cosmetic style unless it obscures behavior, violates an enforced convention, or creates maintainability risk.

## Goal integrity

When a change could alter product meaning, programme order, trust boundaries, or generalized infrastructure, choose exactly one goal-integrity verdict for each implicated scope. Apply the first matching verdict in this order:

- **authority unclear:** the governing authority or accepted goal cannot be determined from the available evidence.
- **diverges:** authority is known and the change contradicts, displaces, or self-reorders the applicable authorized programme.
- **advances:** authority is known and the change stays within the applicable authorized goal and current programme.
- **research-only:** authority is known and the work is technically useful and compatible with the current programme, but has not been adopted as a product dependency or current programme step.

Agent-authored specifications, decision logs, handoffs, PR descriptions, and implementation commits do not approve themselves. Review implementation quality and goal integrity separately: clean code and green CI can still be `research-only` or `diverges`.

Do not combine verdicts for the same scope. For a mixed change, record separate verdicts for materially different scopes when one label would hide the difference between authorized work and speculative additions. Omit the verdict when the change does not implicate a goal-integrity boundary.

## Validate each finding

Before reporting an issue:

- Identify the exact location.
- Trace the triggering path.
- Check whether existing code or tests already handle it.
- Distinguish a real bug from a hypothetical preference.
- Assess severity based on impact and likelihood.

Do not report speculative concerns as facts.

## Severity

Use:

- **P0:** Immediate data loss, security compromise, or system-wide outage risk.
- **P1:** Likely incorrect behavior, broken contract, serious regression, or blocked release.
- **P2:** Real but bounded defect, fragile behavior, meaningful test gap, or maintainability problem likely to cause errors.

Omit P3-style polish unless the user asks for exhaustive feedback.

## Finding format

For each finding include:

- Severity and concise title
- File and line or symbol
- Triggering condition
- Concrete impact
- Evidence or reasoning
- Smallest credible fix

Keep findings independent and deduplicated.

## Review shape

Perform one integrated review covering requirement compliance and code quality. Do not automatically create separate spec and quality reviewer agents.

A specialist or independent reviewer can be useful for a large, high-risk change. Use at most one by default, and verify its findings yourself before reporting them.

## Output

Start with findings ordered by severity.

Then include, only when useful:

- Goal-integrity verdict, when applicable
- Questions or assumptions
- Verification gaps
- A compact overall assessment

When there are no material findings, say so directly and identify any tests or environments that were not exercised. Do not invent an issue to make the review look substantial.
