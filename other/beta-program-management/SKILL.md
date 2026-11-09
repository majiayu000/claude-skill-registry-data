---
name: "beta-program-management"
description: "Running closed and open betas that produce real signal. Beta participant selection, structured feedback collection, beta-to-GA decision criteria, and the difference between soft-launch (no structure, no signal), kitchen-sink (everyone in, no actionable feedback), and structured beta (calibrated cohort, intentional feedback loops, clear graduation criteria). Triggers on beta program, alpha test, beta cohort, beta participant, beta feedback, beta to GA decision, design partner, early access program, closed beta, open beta, RC release. Also triggers when a feature is approaching launch and the team needs structured pre-GA validation, when prior betas produced noise rather than signal, or when the team has soft-launched before but wants more structured feedback this time."
---

# Beta Program Management

A senior product leader's playbook for running betas that produce real signal. Closed and open betas, alpha programs, design partner programs, early access. Participant selection, structured feedback collection, beta-to-GA decision criteria, and the difference between soft-launch (no structure, no signal), kitchen-sink (everyone in, no actionable feedback), and structured beta (calibrated cohort, intentional feedback loops, clear graduation criteria).

Most betas underperform. Teams ship a beta because they think they should run a beta; participants are recruited loosely or open-flooded; feedback is collected ad-hoc through whatever channels exist; the decision to graduate to GA happens on calendar rather than on signal. The beta produced activity but not learning; the team launches with the same uncertainty they had before the beta.

This skill is the discipline that turns betas into decision input. Calibrated cohorts who match the post-launch user profile. Structured feedback that captures what the team needs to know. Mid-beta triage that uses what is being learned. Graduation criteria that distinguish "ready" from "we are tired of running the beta." The discipline is not bureaucratic; it is the difference between a beta that informs the GA launch and a beta that produces noise.

The voice is the senior product leader who has run betas with real signal and watched plenty of betas produce nothing. Concrete, opinionated about what produces signal, willing to call out where beta programs slide into ceremony.

When to use this skill: planning a beta for an upcoming launch, auditing why prior betas have not produced actionable signal, designing the beta participant experience, or deciding whether a feature is ready to graduate from beta to GA.

---

## What this skill is for

This skill spans beta program design and execution. The PM and engineering distinction:

- `feature-flagging` is rollout mechanics; the technical layer for controlling who gets which features.
- **`beta-program-management` (this skill)** is participant management and feedback discipline; the human layer.
- `feature-launch-playbook` is the full launch (post-GA); this skill is what happens BEFORE GA.
- `experiment-design` is rigorous A/B testing; betas are softer, qualitative-leaning, smaller-N.
- `user-feedback-aggregation` is ongoing feedback streams; beta feedback is bounded to the beta period.
- `discovery-research-synthesis` is one-off discovery research; betas are validation-stage rather than discovery-stage.

The audience: senior PMs, product directors, engineering leads coordinating with product, customer success and support running beta cohorts, anyone planning a closed or open beta.

What is not in scope: the broader feature launch (covered by `feature-launch-playbook`); the technical rollout mechanics (covered by `feature-flagging`); the rigorous experimentation methodology (covered by `experiment-design`); the discovery-stage research that informs whether to build the feature in the first place.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/beta-type-decisions.md`](references/beta-type-decisions.md) - Closed/open, alpha/beta/RC, internal/external, time-bounded/open-ended. The combination decision and how it matches signal need.
- [`references/participant-selection-criteria.md`](references/participant-selection-criteria.md) - Criteria that produce calibrated cohorts. Common selection failures. The cohort size question.
- [`references/cohort-sizing-patterns.md`](references/cohort-sizing-patterns.md) - Saturation patterns by feedback type. Sizing decisions for different beta goals. The size-matches-signal principle.
- [`references/beta-onboarding-templates.md`](references/beta-onboarding-templates.md) - Welcome communication structure. NDAs, feedback channels, support paths, incentives. The expectations contract.
- [`references/feedback-collection-patterns.md`](references/feedback-collection-patterns.md) - Structured surveys, async forms, interviews, in-product widgets, beta-aware support. Channels that work and fail. Channel mix discipline.
- [`references/mid-beta-triage-and-iteration.md`](references/mid-beta-triage-and-iteration.md) - Triage cadence. Iteration discipline (what to fix during, what to defer). Communication with participants.
- [`references/beta-to-ga-graduation-criteria.md`](references/beta-to-ga-graduation-criteria.md) - The six graduation criteria. The "tired of the beta" anti-pattern. Perpetual beta anti-pattern.
- [`references/beta-wind-down-communication.md`](references/beta-wind-down-communication.md) - Graduation announcement, transition, recognition, postmortem. Treating participants well.
- [`references/common-beta-failures.md`](references/common-beta-failures.md) - 10+ failure patterns with diagnoses and cures.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- Soft-launch vs kitchen-sink vs structured-beta: [method](references/domain-guide.md#soft-launch-vs-kitchen-sink-vs-structured-beta).
- Beta type decisions: [method](references/domain-guide.md#beta-type-decisions).
- Participant selection criteria: [method](references/domain-guide.md#participant-selection-criteria).
- Beta cohort sizing: [method](references/domain-guide.md#beta-cohort-sizing).
- Onboarding beta participants: [method](references/domain-guide.md#onboarding-beta-participants).
- Feedback collection patterns: [method](references/domain-guide.md#feedback-collection-patterns).
- Mid-beta triage and iteration: [method](references/domain-guide.md#mid-beta-triage-and-iteration).
- Beta-to-GA decision criteria: [method](references/domain-guide.md#beta-to-ga-decision-criteria).
- Beta wind-down and participant communication: [method](references/domain-guide.md#beta-wind-down-and-participant-communication).
- Common failure modes: [method](references/domain-guide.md#common-failure-modes).
- The framework: 12 considerations for beta program management: [method](references/domain-guide.md#the-framework-12-considerations-for-beta-program-management).
- Closing: betas earn their keep with structure: [method](references/domain-guide.md#closing-betas-earn-their-keep-with-structure).
