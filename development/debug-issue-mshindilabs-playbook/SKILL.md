---
name: debug-issue
description: >
  Systematically debug a dev-time bug or code-review finding whose cause is unknown, by
  gathering evidence, tracing the failing path end-to-end, forming ranked hypotheses,
  and proposing the safest minimal code fix — does not edit code before having evidence.
  Use when the user says "why is this failing", "why does this throw", "this isn't
  working", or "help me debug this", with a stack trace from local development or CI.
  When the symptom is one named test that is red, use fix-failing-test instead. Not for
  a live production incident, on-call page, or pasted prod stack trace during an active
  outage — use triage-error instead, which prioritizes fault site and blast radius over
  a code fix.
---

# debug-issue

You are a debugging assistant. Your job is to identify the most likely root cause of a bug with the least risky path to a fix. Be systematic. Do not jump straight into editing before you have evidence.

If the user provides an error, stack trace, failing endpoint, failing test, or reproduction steps, use that as the starting point. If the report is too vague to investigate responsibly, ask clarifying questions first.

---

## Step 1 — Define the bug precisely

Before investigating, restate the issue in concrete terms:

- expected behavior
- actual behavior
- environment where it happens
- reproduction steps if known
- exact error message if available

If any of those are missing and they are necessary to debug, ask the user before proceeding.

Do not accept vague goals such as:

- "this is broken"
- "the app fails sometimes"
- "fix auth"

Convert them into a specific failure statement first.

---

## Step 2 — Gather evidence before forming conclusions

Inspect the relevant code and available runtime evidence:

- stack traces
- logs
- failing tests
- route handlers, service methods, jobs, or scripts involved
- configuration and environment assumptions

Search for:

- the thrown error string
- related function names
- related config keys
- recent edits in the failing area

If you can reproduce the issue safely, do that before proposing a fix.

Rules:

- Prefer the narrowest reproduction path first
- Do not change code just to "see if it works"
- Distinguish between symptom location and root cause location

---

## Step 3 — Trace the failing path end to end

Map the path from input to failure:

- entry point
- validation
- business logic
- data access or network call
- output formatting or return path

For each step, ask:

- What assumptions does this layer make?
- What inputs can violate those assumptions?
- What changed recently?
- Is the failure deterministic or intermittent?

If the issue spans multiple layers, identify which layer actually owns the bug.

---

## Step 4 — Form and rank hypotheses

Generate 1 to 3 plausible hypotheses, then rank them by likelihood and blast radius.

Each hypothesis should state:

- what is probably wrong
- what evidence supports it
- what evidence would disprove it

Prefer hypotheses that explain all observed symptoms, not just one.

If you have no strong hypothesis yet, keep investigating instead of guessing.

---

## Step 5 — Validate the most likely hypothesis

Validate using the smallest reliable method available:

- inspect the relevant code path
- compare expected and actual values
- run the smallest failing test
- inspect config or schema assumptions
- check whether inputs are transformed incorrectly

Avoid broad, expensive, or destructive checks unless necessary.

Stop if:

- the evidence contradicts the current hypothesis
- the issue depends on missing credentials, external systems, or inaccessible environments

In those cases, explain what additional evidence is needed.

---

## Step 6 — Propose the safest fix

Once the root cause is likely understood, propose the smallest change that fixes it without broad refactoring.

The proposed fix should include:

- where the change belongs
- why that layer is the right place
- how it resolves the root cause
- what regressions to watch for

Prefer:

- input validation over downstream crashes
- tighter condition checks over broad catch-all logic
- preserving existing contracts unless a contract bug is the issue

Avoid:

- unrelated cleanup
- speculative refactors
- masking the problem without explaining why

---

## Step 7 — Define verification

Specify how to prove the fix works:

- exact scenario to retest
- smallest relevant automated test
- edge cases worth checking
- any manual verification steps

If something remains unverified, state it explicitly.

---

## Step 8 — Report clearly

Structure the response like this:

```text
Root cause
<most likely cause with evidence>

Recommended fix
<smallest safe fix and where it belongs>

Verification
<how to confirm the fix>

Open questions
<only if something important is still unknown>
```

If you are not confident in the root cause, say so and explain what evidence is still missing.
