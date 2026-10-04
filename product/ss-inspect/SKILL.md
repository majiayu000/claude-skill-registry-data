---
name: ss-inspect
description: Use when investigating any technical issue — a bug, alert, performance regression, or unexpected behavior — that needs evidence-based root-cause analysis rather than a guess. Runs a report-only six-phase process with L0 Local, L1 Runtime, and L2 Systemic evidence budgets, automatic risk promotion, and a structured repair/verification report.
---

# Root Cause Investigation

Systematically investigate technical issues by gathering evidence from multiple independent sources, tracing the root cause through the full call chain, and designing a verified repair at the correct abstraction boundary. Never guess — follow the evidence.

This skill is **report-only**. It never edits code or configuration, changes runtime state, creates a branch, applies a mitigation, or invokes a coding workflow. Execution belongs to a downstream workflow after the report is complete and its root cause is confirmed.

**Core principle:** always establish root cause before designing a permanent repair. A single source of evidence can mislead; corroborating evidence from independent sources confirms.

## When to use

Use this for any technical issue: bugs, alerts, performance problems, unexpected behavior, integration failures.

Use it *especially* when:
- You're under time pressure — guessing under pressure is what makes incidents drag on; being systematic is faster, not slower.
- "Just restart it" looks like the easy fix.
- A previous fix attempt didn't work.
- You don't yet fully understand the issue.
- Different people have different theories about the cause.

Don't skip it because the issue looks simple (simple bugs have root causes too), because you're in a hurry (rushing guarantees rework), or because someone suggests "just try X" (guessing costs more time than investigating).

## The iron law

```text
NO FIX WITHOUT A ROOT CAUSE CONFIRMED BY EVIDENCE FROM 2+ INDEPENDENT SOURCES
NO PERMANENT REPAIR PLAN BEFORE UNDERSTANDING THE RELEVANT DESIGN AND IMPLEMENTATION
```

These are separate, mandatory gates. Evidence confirms *why* the failure occurs; design and
implementation understanding determines *where* the system owns the behavior and therefore where
the repair belongs. Investigation tier changes evidence breadth and explanation depth only — it
never permits skipping the design-understanding gate.

If you haven't gathered corroborating evidence from at least two independent sources (e.g., logs + traces, metrics + code), you cannot propose a fix.

**One variable at a time.** When testing a hypothesis, vary one reproducible test condition at a time. Do not edit source/configuration or mutate a live environment from this skill.

**Emergency exception.** For an active, high-severity incident, recommend the smallest authorized mitigation (rollback, config revert, feature-flag toggle) that could stop the impact before root cause is fully confirmed. This skill documents but never applies it. Mitigation does not replace investigation — complete the full six-phase process afterward regardless.

## Inputs

Ask for (or infer from context) whichever of these is available:
- An issue link, alert ID, or a plain-language description of the symptom.
- The application/service name, if not obvious from the current repository.
- The environment (local, test, staging, production) and rough timeframe the issue started.
- **Investigation tier** — `auto` (default), `L0 Local`, `L1 Runtime`, or `L2 Systemic`. An explicit tier is a minimum floor: honor a requested higher tier, while a requested lower tier must still promote when its conditions fail.

If none of this is clear, do not start investigating — go to Phase 1 and ask the user to pin it down.

Derive `**Problem ID:**` once, before Phase 1, and persist it verbatim in every downstream artifact:

- issue URL → its canonical identity URL: lowercase scheme and host, remove the default port and fragment, remove a trailing slash except for the root path, retain every query key/value pair, sort pairs lexicographically by key then value (preserving duplicates), and serialize them with standard percent-encoding; never guess which parameters are identity-bearing;
- alert/ticket ID → the exact stable ID supplied by the source system;
- plain text → `problem:<first-12-lowercase-hex-of-SHA-256>`, hashing the UTF-8 text after trimming, lowercasing, and collapsing each whitespace run to one space.

Never regenerate the ID from a later summary. Resume and hand-off consumers copy the persisted value verbatim.

## Investigation intensity

After Phase 1, derive the lowest tier whose issue conditions are proven, then set the effective
tier to `max(evidence-derived tier, explicit tier floor)`. An explicit higher floor needs no claim
that the issue itself satisfies that tier's risk conditions; record both values. Uncertainty raises
the evidence-derived tier. The effective tier controls evidence breadth and report depth, never the
HIGH-confidence requirement,
hypothesis verification, affected-path completeness, or report-only boundary.

| Tier | Use when | Required evidence and scope |
|---|---|---|
| **L0 Local** | A deterministic local/unit-test reproduction exists; the issue is pure code, single-repo, confined to one evidence-bounded module; no hard-risk signal applies | Reproduction plus 2+ independent code-level angles selected from test output, code reading, git history, or a healthy analogous path. Keep system understanding concise but identify the failing symbol's callers, invariant, affected paths, and adjacent regression surface. |
| **L1 Runtime** | A single-service environment issue needs runtime evidence, but no cross-boundary or hard-risk signal is present | Select the 2–3 sources with the highest power to distinguish competing hypotheses, such as logs + metrics, trace + code, or config/deploy history + reproduction. Expand only when evidence conflicts or leaves a material alternative alive. |
| **L2 Systemic** | The issue crosses modules/services/repos, has uncertain or expanding blast radius, or involves concurrency, consistency, shared state, security/auth, money, data loss/corruption, migration, public API/schema, irreversible operations, or weak reproduction | Run the full six-phase investigation across every applicable evidence source and complete the full impact-scoped system-understanding gate. |

**Automatic promotion:** whenever current-tier conditions fail, move directly to the lowest higher
tier whose conditions hold. Runtime evidence needs without hard risk promote L0 to L1;
cross-module/service/repository scope, unstable reproduction, conflicting evidence that leaves the
blast radius uncertain, or any hard-risk signal promotes directly to L2. Preserve collected
evidence; never restart from zero. A tier may not be lowered below the explicit floor or merely to
save time.

## The six phases

Complete each phase before moving to the next.

### Phase 1 — Understand the problem

**Gate: do not start investigating until you can state the problem precisely.**

1. Read every error message and stack trace completely — they usually contain the answer. Note file paths, line numbers, error codes, exception types. Copy the exact error text for later searching.
2. Define the symptom: what is happening (exact error/behavior/metric), when did it start (timestamp, deploy, config change), where does it happen (which environment, API, user segment), how often (always, intermittent, under specific conditions).
3. Determine scope and impact: how many users/requests are affected, is it ongoing or resolved, which services are involved.
4. Write one sentence: "I need to find out why [specific symptom] is happening in [specific context] since [specific time]."

If any of this is unclear, ask the user — do not assume.

### Phase 2 — Gather the highest-value evidence

Use the chosen tier's evidence budget. Do not query every available system by default, and do not
stop at the first clue. Start with the sources most likely to distinguish the leading hypotheses;
parallelize independent queries when that saves time.

For a relative timeframe, start with a window matching when the issue began (e.g., "30 minutes ago", "6 hours ago", "7 days ago") and widen it if a required source returns nothing.

If a required query returns nothing: widen the timeframe once; if still empty, record "no data in
this range for this source" and assess whether that is a material evidence gap. If a required tool
errors or is unauthorized, tell the user which access is needed. An inaccessible optional source
is recorded with the reason it was not needed; it does not automatically block L0/L1.

For L0 pure-code work, start with the failing reproduction and choose at least two code-level
angles: test output, current code and callers, git bisect/blame/history, or a healthy analogous path.
Skip alerts/metrics/logs/traces unless evidence promotes the investigation.

For L1, choose 2–3 discriminative runtime/code sources. For L2, check every applicable source below.
The list is a menu for L0/L1 and a completeness checklist for L2:

**Alerts.** What alerted, when, and what threshold was breached? Query your alerting system for events on this app/service in the relevant timeframe, then pull the detail of the specific alert.

**Metrics.** Quantify the problem: error rate and error-type distribution, request rate and latency (p50/p95/p99), host resource usage (CPU, memory), and runtime-level metrics (GC pauses, heap usage) if applicable. Look for an inflection point that lines up with the symptom's start time.

**Logs.** Search by error level and by keyword in the same timeframe; correlate a specific error with its trace ID if your logging platform supports it; pull the surrounding context around a specific log line. What exception was thrown, with what stack trace, on what input?

**Traces.** List traces that errored or were unusually slow in the timeframe, then expand a representative trace's full span tree. Where in the call chain does it break? Which downstream call, database query, or cache operation is implicated?

**Code and git history.** `git log --since="<timeframe>" -- <relevant-paths>` for recent changes that could cause this; grep the codebase for the literal error message text to find where it's raised.

**Configuration.** Did a configuration value or feature flag change around the same time? Compare the current value in your configuration center (or config files) against what you'd expect. Note: never paste live configuration values that might contain secrets into any report — reference where to look instead.

Correlate everything gathered before moving on. For L0/L1, stop collecting lower-value sources
once all of the following hold: 2+ independent sources support the hypothesis, the strongest
alternative is contradicted, Phase 5 has a concrete verification path, the blast radius is
justified, and no promotion signal remains. Record unqueried sources and why they were unnecessary.

### Phase 3 — Pattern analysis

Before forming a hypothesis, find the pattern:

1. **Find working examples.** Locate the nearest healthy analog within the selected tier's justified scope: a passing test/code path for L0, a comparable request/environment for L1, or cross-boundary healthy flows for L2.
2. **Compare working vs. broken.** List every **material** difference within that scope. Expand the comparison only when a difference or evidence conflict triggers promotion.
3. **Check relevant recent changes.** L0 starts with code/tests/git; L1 adds relevant configuration and deployments; L2 also checks infrastructure, migrations, shared state, and cross-service changes.
4. **Understand the tier-scoped dependency chain.** Follow only dependencies that could produce this failure mode or define its blast radius; promotion expands the chain when required.

If you can say "it works HERE but fails THERE," that difference is your lead.

### Phase 4 — Correlate and form a hypothesis

1. **Reconstruct the timeline.** Put the evidence gathered for this tier in chronological order. Line up metrics, logs, traces, tests, code, config, or deployment events only when they were selected or became material.
2. **Build an evidence table:**

   | Source | Finding | Supports hypothesis? |
   |--------|---------|----------------------|
   | Alerts | ... | yes / no / partial |
   | Metrics | ... | yes / no / partial |
   | Logs | ... | yes / no / partial |
   | Traces | ... | yes / no / partial |
   | Code | ... | yes / no / partial |
   | Config | ... | yes / no / partial |

3. **State the hypothesis:** "Root cause is [X], because evidence from [source A] shows [Y] and evidence from [source B] confirms [Z]." Before Phase 5, confidence is provisional: MEDIUM when 2+ independent sources agree, LOW when only one source supports it. Phase 5 promotes it to HIGH only when 2+ independent sources still agree **and** reproduction, prediction, or counter-testing verifies the causal claim with no material contradictory evidence. LOW returns to Phase 2; MEDIUM may be reported but cannot enter permanent repair design.
4. **Rule out alternatives.** For every plausible alternative explanation, state why the evidence contradicts it.

### Phase 5 — Verify the hypothesis

Before fixing anything, verify:

1. **Reproduce it** if at all possible — trigger the issue in a test environment, or find another trace showing the same pattern.
2. **Predict.** If the hypothesis is correct, what else should be true? Check whether the evidence supports that prediction.
3. **Counter-test.** If the hypothesis is correct, what should *not* be happening? Confirm it indeed isn't.

If verification fails, the hypothesis is wrong — return to Phase 2.

### Phase 6 — Understand the impact and design the repair

Only once the hypothesis is verified with HIGH confidence, derive the understanding needed to design a permanent repair. The scope follows the potential blast radius, not an arbitrary file, module, service, or repository boundary. Report depth is tier-proportional: L0 may be a concise RCA capsule, L1 covers the relevant single-service runtime path, and L2 provides the full cross-boundary account; no tier may omit a required report field.

1. **Justify the understanding scope.** List the boundaries included and excluded, with evidence-based reasons. A truly isolated defect may need less than one module; a violated contract, shared state, or cross-service invariant may require following the flow across modules, services, repositories, data/configuration, or runtime boundaries. Do not explore the whole system indiscriminately.
2. **Reconstruct the relevant design and implementation.** Describe component responsibilities and ownership boundaries, entry points, end-to-end control/data/state flow, dependencies, contracts and invariants, existing abstractions or extension points, healthy analogous paths, and the tests/specs/runtime evidence that encode intended behavior.
3. **Assess systemic impact.** State whether this is an isolated implementation violation or a class of failures, name the violated invariant or ownership boundary, and enumerate every plausibly affected path supported by evidence. Record remaining evidence gaps.

**Design-understanding gate — stop before writing any permanent repair proposal.** The report must
already explain the relevant component responsibilities and ownership boundaries, entry points,
end-to-end control/data/state flow, dependencies, intended contracts/invariants, existing
mechanisms or extension points, healthy analogous paths, included/excluded scope with rationale,
and every evidence-supported affected path. If any item is missing or internally inconsistent,
return to investigation. A concise L0 account may be short, but it must still be complete for its
proven scope.

4. **Design the permanent repair only after the gate passes.** Restore the invariant at the correct abstraction boundary and reuse an existing mechanism where one exists. Explicitly name and reject the tempting symptom-only/local-special-case alternative unless the evidence proves that boundary owns the behavior.
5. **Plan verification and operations.** Specify the failing regression test, focused and full-suite commands, runtime verification, compatibility and downstream effects, migration needs, rollback strategy, observability changes, and regression coverage.
6. **Handle emergency mitigation as a recommendation only.** Document the smallest temporary rollback/config/feature-flag action that an authorized operational process could apply. Label it temporary and keep the permanent investigation and repair plan mandatory.

If the evidence cannot justify the understanding scope or affected-path list, the report is incomplete: return to Phase 2. Do not propose a permanent behavioral repair and do not hand an incomplete report to planning.

**Three failed fixes are evidence, not permission to retry.** If prior attempts are supplied, document what each revealed. Three failed attempts indicate that the understanding may be wrong or the issue systemic; require architectural review before another implementation attempt.

## Output: investigation report

At the end of every investigation, produce a report:

```markdown
# Investigation Report: <one-line problem summary>

**Problem ID:** <canonical issue URL / exact alert ID / deterministic problem:<12-hex> fingerprint>
**Investigation Tier:** <L0 Local | L1 Runtime | L2 Systemic>
**Tier Rationale:** <evidence-derived tier and reasons; explicit floor if any; effective tier; promotions>
**Evidence Budget:** <required sources/angles selected, sources intentionally not queried and why>
**Application:** <name>
**Environment:** <test / staging / production>
**Timeframe:** <issue timeframe>
**Date:** <YYYY-MM-DD>

## Problem statement
<Phase 1 sentence>

## Evidence chain

| Source | Finding | Relevance |
|--------|---------|-----------|
| Alerts | ... | ... |
| Metrics | ... | ... |
| Logs | ... | ... |
| Traces | ... | ... |
| Code | ... | ... |
| Config | ... | ... |

## Timeline
<chronological sequence>

## Root cause
**Root cause:** <clear statement>
**Confidence:** HIGH / MEDIUM
**Supporting evidence:** <2+ independent sources>
**Ruled out:** <alternative hypotheses and why>

## Relevant design and implementation
**Understanding scope:** <included and excluded boundaries, with rationale>
**Responsibilities and ownership:** <relevant components and boundaries>
**End-to-end flow:** <control/data/state path through the affected behavior>
**Contracts and invariants:** <intended behavior and relevant contracts>
**Violated Invariant:** <exact invariant broken by the failure, with evidence>
**Owning Boundary:** <component/abstraction that owns the behavior and why>
**Existing mechanisms:** <abstractions, extension points, healthy analogous paths>
**Systemic impact:** <isolated violation or broader class, with rationale>
**Evidence gaps:** <remaining gaps, or none>

**Affected Paths:**
- `<repo>:<entry point/module/data/config/runtime path>` — <why it is affected>

**Repositories Requiring Fix:**
- `<repository-name>` — <canonical local path or remote URL when known; one repository per bullet>

## Repair and verification plan
**Permanent repair:** <correct abstraction/ownership boundary and invariant restored>
**Patch-Style Alternative Rejected:** <tempting local/symptom-only patch and why it would not restore the invariant; "none" only when no plausible patch exists>
**Temporary mitigation:** <recommended authorized action / not needed; never applied by this skill>
**Compatibility and migration:** <downstream effects and migration needs>
**Rollback:** <safe rollback strategy>
**Verification:** <regression test, focused/full-suite commands, runtime signals>
**Observability:** <metrics/logs/traces/alerts needed to prove recovery>
**Regression coverage:** <all affected and healthy analogous paths to test>

## Prevention
- <additional alerting / monitoring / config guardrails>
- <defensive design or code changes>
```

## Quick reference

| Phase | Key activity | Success criteria |
|-------|--------------|-------------------|
| 1. Understand | Read errors, define the symptom, scope the impact | Problem statable in one precise sentence |
| 2. Gather evidence | Tier-budgeted collection of the most discriminative sources | Tier requirements met with 2+ independent sources/angles and no promotion signal |
| 3. Pattern analysis | Find working examples, compare, check changes | Identified what differs between working and broken |
| 4. Correlate | Timeline, evidence table, hypothesis | Provisional MEDIUM hypothesis backed by 2+ sources |
| 5. Verify | Reproduce, predict, counter-test | Causal verification promotes the 2+-source hypothesis to HIGH, or rejects it |
| 6. Design repair | Scope by blast radius, reconstruct invariants and affected paths | Complete systemic repair and verification plan |

## Signals you're going off the rails

| If you hear | It means | Do this |
|-------------|----------|---------|
| "Stop guessing" | You're proposing fixes without evidence | Return to Phase 2 |
| "Did you actually check?" | You assumed instead of verifying | Run the query, show the output |
| "That's not the issue" | Your hypothesis conflicts with their domain knowledge | Listen, ask what they know, re-analyze |
| "We already tried that" | You're repeating a failed approach | Ask what was tried and what it revealed |
| "Just show me the data" | Too much speculation, not enough evidence | Present raw evidence, let them interpret |

## When you don't know

It's fine to say "I don't understand this yet." Don't pretend to understand a system you haven't explored, and don't invent explanations to fill gaps. Say what specific context you're missing and ask for it. Saying "I don't know" is progress; guessing is not.

## When the investigation finds no root cause

If a systematic pass through every source required by the selected tier reveals no clear root cause:
1. That's a valid outcome, not a failure — as long as the process was actually completed.
2. Document what was investigated and ruled out.
3. Consider environmental or timing causes: a race condition, a transient network blip, an external dependency's own issue.
4. Recommend retry/circuit-breaker handling for transient failures, finer-grained monitoring, or structured logging at the suspected failure point to capture more data next time.
5. Report: "Root cause not definitively identified. Evidence suggests [environmental/timing/external]. Recommend [monitoring/retry] to capture more data on the next occurrence."

Before declaring this, double check: did you exhaust the evidence required by the selected tier,
follow every promotion signal, and complete Phase 3's pattern analysis? Most "no root cause"
conclusions are actually incomplete investigations.

## Anti-patterns

| Anti-pattern | Why it's harmful | Do this instead |
|--------------|-------------------|------------------|
| "Quick fix first, investigate later" | Masks the root cause, creates new bugs | Complete Phases 1–4 before fixing |
| Check only one source (e.g., only logs) | A single source can mislead | Require 2+ corroborating sources |
| Skip a source required by the tier or leading hypothesis | May hide runtime or cross-boundary evidence | Gather the tier-required discriminative evidence first |
| Assume the last deploy caused it | Correlation isn't causation | Check the metrics timeline against the deploy time |
| Fix the symptom, not the cause | The issue recurs | Trace to root cause via Phase 3 |
| Skip hypothesis verification | You may be fixing the wrong thing | Phase 5 is mandatory |
| Propose a fix at LOW confidence | Wastes time on the wrong fix | Require HIGH confidence (2+ sources) |

## Stop signs

Stop and back up if you catch yourself:
- Proposing a fix before completing Phase 2.
- Relying on a single source for root cause.
- Saying "probably" or "maybe" without evidence — that's a guess.
- Attempting a fourth fix after three failures.
- Assuming without reproducing (skipping Phase 5).
- Skipping a source that the selected tier, blast radius, or leading hypothesis makes material.

## Common rationalizations

| Excuse | Reality |
|--------|---------|
| "Logs show the error clearly, no need for anything else" | One source cannot establish causality; add the most discriminative independent source, and traces when the call chain is material |
| "It's obviously a code bug" | Prove L0 with deterministic reproduction and 2+ code-level angles; otherwise promote and check runtime/config evidence |
| "Just restart the service" | Restarting hides the issue; it will recur |
| "No time for a full investigation" | Systematic investigation is faster than thrashing through guesses |
| "Can't reproduce, so can't investigate" | Traces + logs + metrics from the incident *are* the reproduction |
| "Recent deploy caused it" | Verify with metrics — did the error start exactly at deploy time? |
| "Let me try one more fix" (after 2+ failures) | 3+ failures means an architectural problem — stop and discuss |
| "Multiple fixes at once saves time" | You can't isolate what worked — one variable at a time |

## Examples

```
Investigate: user login returns 500 in the staging environment
Investigate: alert #12345
Investigate: <link to the issue tracker item describing the bug>
```
