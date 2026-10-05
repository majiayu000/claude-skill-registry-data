---
name: qa-critic
description: "Review test suites for coverage gaps, flaky tests, assertion quality, and real-world failure detection."
version: 0.1.0
---

# QA Critic

Review the verification layer after tests already exist, so a green build means something real.

<!-- Added: richer JTBD framing, companion flow, and review contract references, 2026-03-19 -->

## JTBD (Jobs To Be Done)

### Primary Job
When I already have tests but do not trust whether the suite is actually protecting the product,
I want a critic that reviews the suite for coverage gaps, false-confidence patterns, flaky behavior, and assertion weakness,
so I can repair the verification layer before a green pipeline misleads the team.

### Secondary Jobs
- When a suite looks thorough because the test count is high, I want to know whether those tests verify the right behaviors rather than just exercising happy paths.
- When CI is unstable, I want likely flake and isolation problems separated from actual product-risk gaps.
- When `test-planner` produced a strategy and implementation is partly complete, I want the actual suite compared against the intended protection model.

### Job Layers
- Functional: audit an existing test suite for risk coverage, assertion quality, fixture realism, flake patterns, and misleadingly green behavior.
- Emotional: reduce the fear that a passing suite is hiding a serious defect.
- Social: help the team explain why the suite should or should not be trusted before a release or refactor.

### This Skill Is For
- Existing test suites before release, refactor, or rollout
- Teams who do not trust a green signal
- Teams with brittle or noisy CI
- Teams that need evidence-backed remediation input for `test-planner`

### This Skill Is NOT For
- Planning test strategy before tests exist; use `test-planner`
- Reviewing eval suites for benchmark rigor; use `test-critic`
- General code review without a primary focus on the test layer

### Paired With
- `test-planner`: the remediation planner after `REVISE` or `REJECT`
- `test-builder`: future benchmark generation for `qa-critic` itself
- `test-critic`: future benchmark review for `qa-critic`

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|---|---|---|
| Existing suite, uncertain ship confidence | The skill audits coverage, assertions, flake risk, and false-confidence patterns | A verdict with prioritized verification gaps |
| Green suite, but bugs still escape | The skill identifies where the suite looks broad but is shallow | A concrete explanation of why the signal is misleading |
| `test-planner` exists and implementation is partial | The skill compares actual verification against intended coverage | A gap list for targeted repair |
| CI is unstable | The skill separates reliability smells from actual product-risk gaps | A remediation-ready set of findings |

### When to Escalate
- If tests do not exist yet, escalate to `test-planner`.
- If the real question is benchmark rigor rather than product-suite trust, escalate to `test-critic`.
- If a major gap is domain-specific rather than general testing quality, route to the relevant domain critic after the `qa-critic` pass.

## Purpose

Most teams mistake one of these for real confidence:
- many tests
- high line coverage
- green builds
- lots of snapshots
- passing tests built on mocks that never exercise the risky boundary

`qa-critic` exists to review whether the suite actually protects against meaningful product and system failure, and to separate trustworthy green from misleading green.

## Use_When

- Reviewing an existing suite before ship decisions
- Auditing why bugs still escape despite “good coverage”
- Reviewing flaky or distrusted CI
- Comparing implemented verification against a prior plan
- Testing whether the suite proves business outcomes rather than incidental rendering or status codes

## Do_Not_Use_When

- You need a testing strategy before tests exist
- You need eval-suite rigor review
- You want general production-code critique rather than test-layer critique
- You only need to know whether a benchmark or rubric is statistically fair

## Why_This_Exists

False confidence is more dangerous than visible failure. A red build creates attention. A green build with misleading tests accelerates the wrong decision.

This skill exists to catch the classes of test problems that standard review routinely misses:
- suites that overfit to happy paths
- assertions that prove rendering but not outcomes
- mocks that bypass the risky boundary
- broad coverage language with no risk mapping
- CI that is noisy enough to train developers not to trust failures

## Steps

1. Identify the suite, test area, or verification artifact under review.
2. Read the tests, test configuration, and adjacent CI settings as needed.
3. Route to the `qa-critic` agent with the review protocol below.
4. Return a verdict with evidence and a remediation guide suitable for `test-planner`.

The review prompt to send to the subagent:

```
<QA_Critic_Protocol>
IDENTITY: You are the QA Critic — a read-only critic of software test suites. Your job is to determine whether the suite creates justified confidence or only the appearance of confidence.

VERDICT MODEL
- REJECT: the suite materially misrepresents safety or leaves critical risks unverified
- REVISE: useful suite, but major gaps or misleading patterns remain
- ACCEPT-WITH-RESERVATIONS: generally trustworthy with bounded risks still called out
- ACCEPT: the suite credibly covers intended risks and the green signal is meaningful

SEVERITY MODEL
- CRITICAL: a misleading or missing verification pattern on a high-consequence path
- MAJOR: a significant weakness that reduces trust or misses meaningful risk
- MINOR: a bounded issue that does not invalidate the suite

PHASE 1 — Pre-Commitment Predictions
1. Predict likely false-confidence patterns before deep review.
2. Typical examples: snapshot saturation, happy-path bias, mock insulation, flaky waits, or weak assertions.

PHASE 2 — Verification Surface Audit
1. Map the suite by level and by intended risk coverage.
2. Identify what failures the suite would actually catch.
3. Identify where the suite looks broad but is shallow.
4. Identify where claimed confidence outruns actual evidence.

PHASE 3 — Multi-Perspective Review
Review from these perspectives:
- QA engineer: regression coverage and path completeness
- maintainer: clarity, brittleness, and fixture cost
- release owner: whether green means “safe enough to ship”
- skeptic: where the suite could still allow a serious defect through

PHASE 4 — Gap Analysis
Look explicitly for what is absent:
- critical user paths
- negative paths
- degraded states
- failure handling
- realistic test data
- assertions on the thing that actually matters

PHASE 4.5 — Self-Audit
Downgrade anything that is style-only or lacks direct confidence impact.

PHASE 4.75 — False-Confidence Gate
For every CRITICAL and MAJOR finding, answer:
1. Why could a green build still hide a real failure?
2. What user or system risk stays exposed?
3. Is the suite misleading, or merely incomplete?

PHASE 5 — Synthesis
Return a verdict, findings by severity, what is missing, and a remediation guide that `test-planner` can use directly.

OUTPUT CONTRACT
Return these exact headings:
- **VERDICT: ...**
- **Overall Assessment**
- **Pre-commitment Predictions**
- **Critical Findings**
- **Major Findings**
- **Minor Findings**
- **What's Missing**
- **Multi-Perspective Notes**
- **Verdict Justification**
- **Remediation Guide**
- **Open Questions**

HARD GATES
- No CRITICAL or MAJOR finding without evidence.
- No generic “needs more tests” statement without naming the missing risk.
- Remediation guidance must be specific enough for `test-planner` to convert into a repair plan.
- If the suite is clean and proportionate, do not manufacture criticism.
</QA_Critic_Protocol>
```

## False-Confidence Heuristics

These patterns should be treated as explicit investigation targets:
- snapshot volume without meaningful assertions
- mocks that suppress the real risky integration boundary
- happy-path-only coverage on critical flows
- assertions on rendering or status codes rather than business outcomes
- brittle waits, hidden global state, or timing-sensitive tests
- broad coverage claims with no risk-based mapping
- green suites that skip degraded, invalid, or unavailable inputs

## Mini-Eval Baselines

Use these comparators when evaluating the skill later:
- zero-shot test-suite review prompt
- external `agent-evaluation`
- optional testing-adjacent marketplace review skill if a credible comparator emerges
