---
name: incident-followup
description: 'Composite skill — runs the postmortem chain after any production incident (`/hotfix`, rollback, or prod outage acknowledged). Chains adt-research (root-cause learning) → adr-write (decision capture) → generate-tests (regression test) → security-sweep (conditional, only if root cause is auth/input/secret-related) → knowledge-loop (memory + RAG curation) → handoff. Stops the silent-postmortem failure mode where a hotfix ships and the lessons evaporate. Auto-queues after `/hotfix` Phase 10 completes; also fires when user says "postmortem", "what did we learn", "write up the incident".'
user-invocable: true
auto-invoke: '"postmortem", "incident review", "what did we learn from", "write up the incident", post-hotfix Phase 10, post-rollback'
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/incident-followup
---

# Incident Followup

The postmortem composite. Runs after the bleed has stopped, not during.

The purpose is durability: a hotfix that ships without an ADR + regression test +
captured memory will repeat itself within months. This composite makes that
chain non-skippable.

## When this fires

- Auto-queued by `/hotfix` Phase 10 (cherry-pick back to release) on success
- Manual: user says "postmortem", "incident review", "what did we learn"
- After a revert / rollback lands on `main`
- After a Sentry alert was acknowledged + suppressed without a code fix (the
  "we just bumped the ignore threshold" anti-pattern)

If less than 6 hours have passed since the incident and the user is still in
mitigation mode, defer this composite — print a one-line reminder and exit:
`incident-followup queued: re-run after the bleed has fully stopped`.

## Workflow

### Phase 1 — Scope the incident (always)

Gather, in this order:
- The triggering artifact: `/hotfix` PR URL, revert SHA, or Sentry issue URL
- Timeline: when it started, when detected, when mitigated (rough is fine)
- Blast radius: % of users / requests / regions affected (best estimate)
- The exact commit that introduced the regression, if known (use `git log -S` or
  `git bisect` only if cheap; otherwise mark as "unknown — see ADR")

Capture into a scratch incident packet at `.claude/incidents/<date>-<slug>.md`
(create directory if missing). This packet is the input for the next phases.

### Phase 2 — Root-cause research (adt-research)

Invoke `adt-research` with the failure mode as the query. Goal: find prior art —
has this class of bug happened before in this repo or any of the user's tracked
repos? Look for:
- Similar Sentry signatures in the last 12 months
- Past ADRs naming the same component
- Past skill outputs / handoffs that warned about this surface

If `adt-research` returns weak hits (cosine < 0.40 on the strongest match),
note it in the incident packet — the lack of prior art is itself a signal that
no one was watching this surface.

### Phase 3 — Decision capture (adr-write)

Invoke `adr-write`. The ADR must answer:
- What happened (1 paragraph, blame-free)
- Why the existing safeguards (tests, types, review, CI) did not catch it
- What changes (code or process) prevent recurrence
- What is explicitly NOT being changed and why (cost/benefit)

Place the ADR under the repo's `docs/adr/` or `.agents/adr/` (whichever already
exists; if neither, create `docs/adr/`). Number it sequentially.

### Phase 4 — Regression test (generate-tests)

Invoke `generate-tests` scoped to the regressing code path. Requirements:
- The test must fail against the pre-hotfix HEAD (verify by checking out parent
  and running it once)
- The test must pass on the current HEAD
- It must live in the same suite as its neighbors (do not introduce a new
  integration tier just for this)
- Name it after the incident slug, not the bug detail: `test_incident_<slug>`

If a suitable test already exists in the hotfix PR, skip generation but verify
the pre-hotfix-fail / post-hotfix-pass property holds. Note the verification
in the incident packet.

### Phase 5 — Security sweep (conditional)

Run `security-sweep` ONLY IF the root cause involved one of:
- Authentication, authorization, session handling
- User-controlled input crossing a trust boundary (SQL, shell, template, regex)
- Secret handling (envs, tokens, signing keys)
- Dependency with a known CVE
- Data exposure / leakage (logs, error messages, response payloads)

Skip and record `security-sweep skipped: root cause is <category>` if the
incident was, e.g., a config drift, race condition in app logic, or external
service outage.

### Phase 6 — Knowledge capture (knowledge-loop)

Invoke `knowledge-loop` to:
- Write a project-scoped memory: `incident-<slug>.md` with `type: project`,
  linking `[[adr-NNN]]` and `[[release-branch-model]]` if relevant
- Update the repo's RAG index so future `recall` queries surface the ADR + test
- If the memory `gotchas.md` standard exists for this repo, append a one-liner

### Phase 7 — Handoff (always)

Invoke `handoff` with the incident packet path + ADR path + test path + memory
path bundled into the next-action block. This guarantees the next session can
pick up if any later verification step (e.g., 7-day Sentry watch) is still
pending.

## Reconciliation block (mandatory output)

```
INCIDENT FOLLOWUP — <incident-slug>
  Scope:        <packet path>
  Prior art:    <n hits, top cosine, or "no prior art found">
  ADR:          <path> (decision: <one-line>)
  Regression:   <test path> (verified: pre-fail ✓ / post-pass ✓)
  Security:     <sweep result | skipped: <category>>
  Memory:       <memory path>
  Snapshot:     <handoff path>
  Open watch:   <e.g., "7-day Sentry re-occurrence check on <date>" or "none">
```

If any phase failed or was deferred, mark it explicitly (`(deferred: <reason>)`
or `(failed: <reason>)`). Never silently skip — the contract is that every
phase reports.

## Stop conditions

- If Phase 4 cannot produce a failing-before-fix test (e.g., the regression is
  in a path that cannot be unit-tested), surface this as `Regression: NOT
  POSSIBLE — needs manual <integration / e2e / chaos> test` and continue. Do
  not block the chain; flag for the next session.
- If `adt-research` is unavailable (no RAG index for this repo), substitute
  with `grep -r` over recent commit messages + open issues, and note the
  fallback in the reconciliation block.
- Refuse to run if Phase 1 cannot identify a triggering artifact — there is
  nothing to be postmortem-of without it.

## Negative rules

- Do NOT assign blame to a person in the ADR or memory. Always describe the
  failure as a system/process gap.
- Do NOT skip Phase 4 because "the fix is obvious". The regression test is the
  durable artifact; the fix code drifts.
- Do NOT mark the composite complete without a handoff — open watches are real
  and need to survive session boundaries.
