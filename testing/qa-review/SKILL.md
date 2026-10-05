---
name: qa-review
description: Use when reviewing a feature for release readiness. Covers acceptance-criteria verification, edge-case enumeration, regression risk assessment, and a release decision that is a judgment rather than a vibe.
metadata:
  category: testing
  version: 1.0.0
  tags: [qa, release, acceptance, risk, review]
---

# QA Review

## Purpose

Decide whether a change is ready to ship, on evidence. The output is a judgment with reasons — not "looks good to me", and not a list of every conceivable improvement.

## When to Use

- Before releasing a feature.
- Reviewing a change for regression risk.
- Assessing whether the test coverage for a change is adequate.
- Sign-off on a release candidate.

## Capabilities

- Acceptance-criteria verification against the actual behavior.
- Edge-case enumeration.
- Regression-risk assessment based on what the change touches.
- Test-coverage gap analysis.
- Release recommendation with explicit residual risk.

## Inputs

- The change: the diff, the feature, and its acceptance criteria.
- The test evidence: what was tested, at what level, and what passed.
- The rollback capability.

## Outputs

A release recommendation:

- **Ship** — Criteria met, risk understood and acceptable.
- **Ship with mitigation** — Ship behind a flag, or with a specific monitor in place.
- **Hold** — A specific, stated defect or gap must be closed first.

Each with the evidence behind it.

## Workflow

1. **Verify the criteria, one by one** — Against the running system, not against the pull request description. A criterion that cannot be verified was not a criterion.
2. **Enumerate the edges** — For each input: empty, maximum, invalid, hostile. For each dependency: slow, down, wrong. Which of these are handled, and which were never considered?
3. **Assess the regression radius** — What else touches the code that changed? A change to a shared utility has a far wider blast radius than a change to one route handler.
4. **Find the coverage gaps** — Not "is coverage above 80%", but "is the new logic tested, and would the test fail if the logic were wrong?"
5. **Check the operational readiness** — Can this be rolled back? Is it behind a flag? Will a failure be visible in monitoring, or will it be silent?
6. **Make the call, and state the residual risk** — Shipping with known risk is legitimate. Shipping with unstated risk is not.

## Best Practices

- Verify against the requirement, not against the implementation. The two agreeing proves only that the developer read their own code.
- A feature with no rollback path and no flag is a feature you are committing to permanently in the moment you deploy it. Say so.
- "The tests pass" is not release readiness. The tests pass on code that has never seen a real user.
- Identify the silent failure modes: what breaks in a way that no alert fires and no error is logged? Those are the ones that are discovered by a customer six weeks later.
- A hold must name a specific, closeable defect. "It feels risky" is not a hold; it is an anxiety, and it will be overruled.
- Record what was not tested. That is what makes the residual risk honest.

## Examples

**A release review that is a judgment, not a rubber stamp:**

```markdown
## Feature: partial refunds — release review

### Acceptance criteria
- [x] An admin can refund less than the order total.        Verified: ord_01HX, $12 of $42.
- [x] The remaining refundable balance is displayed.          Verified.
- [x] A refund cannot exceed the remaining balance.           Verified: API returns 422.
- [ ] The customer receives an email confirmation.            NOT IMPLEMENTED — the
      email template exists but is not wired to the refund event. This is in
      the acceptance criteria and is not in the change.

### Edge cases
- Zero-amount refund:          rejected correctly.
- Refund exceeding balance:    rejected by the API, but the UI shows a success
                               toast (defect #4412, fixed in this branch).
- Concurrent refunds:          idempotency key prevents a double refund. Verified
                               with two simultaneous requests.
- Gateway timeout mid-refund:  NOT TESTED. The gateway sandbox cannot be made to
                               time out. The code path exists and is unit-tested
                               with a mock, but has never run against the real
                               gateway.

### Regression radius
`OrderBalance` is shared with invoicing and with the accounting export. Both
have test coverage and both suites pass. The accounting export was manually
verified against a refunded order — the figures reconcile.

### Operational readiness
- Behind flag `refunds.partial` — default off. Rollback is a flag flip.
- A metric exists for refund failures; an alert does not.

### Recommendation: SHIP WITH MITIGATION

Ship behind the flag, enabled for internal accounts only, for one week.

Blocking for general availability:
  1. The confirmation email (an acceptance criterion, not delivered).
  2. An alert on the refund failure rate — without it, a gateway problem is
     silent until a customer complains.

Residual risk accepted for the internal rollout: the gateway-timeout path is
untested against the real gateway. Impact is bounded to internal orders.
```

## Notes

- "Ship with mitigation" is the most useful and most under-used outcome. It unblocks the team while being honest about what is not finished.
- The most valuable line in most QA reviews is the "not tested" section. It converts an unknown risk into a known one, which is the entire job.
- A review that always says ship is not a review. A review that never says ship is an obstacle. The value is in the discrimination.
