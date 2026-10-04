---
name: tester-mindset
description: Testing mindset skill for context-driven test strategy, exploratory testing, validation design, acceptance criteria, oracles, weak-test detection, edge cases, heuristics, checklists, and evidence review for code, products, plans, or claims. Use when the user asks what to test, how to test, whether evidence is enough, or to bring a tester mindset. Do not use for merely running an existing test command.
---

# Tester Mindset

Design evidence that can reveal a meaningful failure in the claim being tested.
Use this as an orthogonal workflow alongside the relevant domain guidance.

For planning or review, return a strategy or findings without editing code or
changing external state. For exploratory work, run only authorized, bounded
probes. Existing implementation authority covers relevant test changes; do not
turn design feedback into an unrelated production refactor.

Load [exploration and oracle prompts](references/exploration-and-oracles.md)
when a context map, risk category, test-idea tour, or alternative perspective
would expose a missing case. Do not exhaust those catalogs for routine work.

## When To Use

- design a test plan, validation strategy, QA approach, or acceptance criteria
- identify edge cases, failure modes, adversarial cases, or missing evidence
- decide whether existing tests, metrics, benchmarks, or demos prove enough
- plan or debrief exploratory testing, chartered sessions, or bug hunts
- review test quality and detect weak, tautological, or proof-theater tests
- turn a vague claim such as "this works" into observable checks
- review a change through the question "what consequence was invited?"

## Not For

- simply running an existing test command
- broad debugging when the failure is already reproduced and the next step is diagnosis
- security exploit analysis that needs the full `security` workflow
- routine implementation work where ordinary repo validation is enough

## Core Workflow

1. **Map the context.**
   Identify the mission, stakeholders, risks, constraints, team skills,
   available evidence, and cost of being wrong. There are no universal testing
   best practices, only practices that fit a context.
2. **Name the claim.**
   State the belief being tested in falsifiable language. If the claim is vague,
   split it into behavior, contract, performance, safety, usability, security,
   trust, maintenance, or process claims.
3. **Separate testing from checking.**
   Checking applies explicit pass/fail rules to known expectations. Testing is
   investigation: learning, modeling, exploring, questioning, and interpreting.
   Automate checks, but do not pretend automation replaces judgment.
4. **Invite consequence.**
   Name an observation that would disprove the claim or change the next action.
   If no outcome could change the conclusion, revise the probe.
5. **Choose a survivable scale.**
   Make the test strong enough to teach and small enough to survive. Prefer
   cheap probes first, then increase fidelity where risk, irreversibility, or
   user harm justifies it.
6. **Choose oracles deliberately.**
   Name how a problem would be recognized: requirements, prior behavior,
   comparable products, standards, stakeholder expectations, user goals,
   internal consistency, product purpose, statutes, or expert judgment. Treat
   every oracle as fallible.
7. **Inspect the apparatus.**
   Question fixtures, mocks, datasets, metrics, timing, environments, prompts,
   observers, and definitions of "pass." A failing test may expose a broken
   question, not only a broken system. Ask whether the fixture, mock, metric,
   benchmark, prompt, dataset, or environment is the thing actually being
   validated.
8. **Let reality disagree.**
   Include paths that can contradict the preferred story: boundary data,
   malformed input, slow dependencies, retries, concurrency, time, state
   transitions, upgrade paths, human behavior, adversarial pressure, or
   conflicting stakeholder values.
9. **Interpret narrowly.**
   Say what the result proves, what it only suggests, who it matters to, and
   what remains untouched. Passing evidence reduces uncertainty; it does not
   convert partial coverage into certainty.
10. **Choose the next consequence.**
   If risk remains material, recommend the next smallest higher-fidelity check:
   integration test, exploratory session, benchmark, canary, monitoring, user
   trial, chaos probe, manual smoke, or review.

## Exploratory Sessions

Use a charter when scripted checks are too narrow or unknowns matter.

Charter format:

```text
Explore <target>
with <resources, tools, data, or conditions>
to discover <information, risks, or surprises>
```

Session discipline:

- Take notes during the session, not after.
- Tag findings as `BUG`, `QUESTION`, `IDEA`, `RISK`, or `NOTE`.
- Pause on anomalies: reproduce, vary conditions, collect evidence, assess impact.
- Debrief with what was covered, what was not covered, what surprised you, and what follows.
- Convert reproducible exploratory findings into automated regression checks
  when the behavior is stable and the oracle is clear.

## Weak Test Detector

Reject tests that cannot meaningfully fail for the right reason.

Before writing or approving test code:

- Read the requirement or acceptance criteria.
- Read the implementation or behavior under test.
- Select a technique: equivalence partitioning, boundary values, decision table,
  state transition, error category, or exploratory charter.
- Enumerate cases before writing code.
- Use Arrange, Act, Assert for executable tests.
- Self-verify: would this fail if the production behavior were genuinely broken?

Reject these when they cannot detect a defect in the stated contract:

- tautological assertions such as `expect(true).toBe(true)`
- self-referential assertions such as `expect(x).toBe(x)`
- truthiness-only assertions when presence is insufficient for the contract
- empty checks, disabled assertions, or checks that neither exercise real
  behavior nor inspect an authentic artifact
- replacing the behavior being proved with a mock
- format-only checks when the claim also promises computed or persisted values
- literal roundtrips that only prove the test built its own fixture

## Heuristics And Checklists

- Use heuristics for decisions under uncertainty; validate them against outcomes.
- Use checklists for error-prone procedures with critical steps.
- Keep checklists short: critical skipped-often steps only.
- Use `READ-DO` for unfamiliar or irreversible procedures.
- Use `DO-CONFIRM` for expert routine procedures.
- Prefer forcing functions over reminders when a critical check can be automated.
- Revisit heuristics and checklists when the environment changes.

## Evidence Choices

- Use unit checks for stable pure behavior and fast feedback.
- Use integration checks for collaboration contracts and real boundaries.
- Use end-to-end or smoke checks sparingly for critical user journeys.
- Use exploratory sessions when the unknowns matter more than repeatability.
- Use monitoring, canaries, synthetic checks, or staged rollout when time,
  scale, or production context is the real risk.

## Decision Rules

- Test claims and contracts before testing implementation details.
- Treat hard-to-test behavior as design feedback. Recommend a clearer seam;
  refactor it only when production changes are within the requested scope.
- Name executable tests as behavior specifications, not implementation details.
- Prefer pressure with fidelity: too little pressure teaches nothing, the wrong
  pressure teaches the wrong lesson.
- Treat coverage, green checks, dashboards, and sign-off as evidence, not truth.
- Prefer real boundaries over mocks when the risk lives in integration,
  serialization, time, identity, permissions, or external behavior.
- Add adversarial and negative cases when failure would be costly, silent, or
  exploitable.
- Scale effort to blast radius, reversibility, novelty, and user harm.
- Name what is excluded from the room: time, data diversity, production traffic,
  user incentives, hardware, network behavior, organizational incentives, or
  maintenance burden.
- Avoid proof theater: tests designed to preserve confidence rather than risk it.
- Prefer clarity over coverage; coverage says what ran, not what was understood.
- Preserve uncertainty and contrary observations in the report.

## Stopping Rule

Stop when the claim has risk-appropriate evidence, remaining uncertainty is
named, and the next check would cost more than the confidence it can reasonably
add. If material risk remains but more pre-release testing is inefficient, shift
to monitoring, staged rollout, rollback planning, or explicit acceptance of
risk.

## Output Shape

For a testing recommendation, use only the sections that help assess the claim.
A narrow recommendation can fit in a paragraph:

```markdown
## Context
Mission, stakeholders, risks, constraints, and evidence so far.

## Claim
What belief or contract is being tested.

## Consequence
What result would change our mind or behavior.

## Oracles
How problems will be recognized, and where those oracles are fallible.

## Tests Or Probes
Concrete checks, exploratory charters, or experiments ordered from cheapest
credible probe to higher-fidelity evidence.

## Apparatus Risks
Where mocks, data, metrics, environments, prompts, or definitions could mislead us.

## Remaining Uncertainty
What passing still would not prove, and the next consequence to invite if needed.
```

## Examples

- "Bring a tester mindset to this checkout refactor." -> identify stakeholders,
  contracts, risks, oracles, integration boundaries, weak tests, and a validation ladder.
- "Do these benchmarks prove the new parser is faster?" -> inspect workload,
  measurement setup, excluded cases, metric incentives, and remaining uncertainty.
- "Does this rollout plan have enough evidence?" -> identify trust, adoption,
  reversibility, monitoring, rollback, and excluded real-world conditions.
- "Plan exploratory testing for the billing flow." -> write charters, choose
  heuristics, time-box sessions, define notes, and decide what findings become checks.
- "Review these tests for slop." -> reject tautologies, no-production-call tests,
  truthiness-only assertions, mock-the-SUT patterns, and tests that cannot fail usefully.
- "What tests should cover this password reset flow?" -> compose with
  `security` and `security-identity-access` when exploit paths and identity
  boundaries are the main risk.
