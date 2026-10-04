---
name: experiment-runbook
description: >
  Translate an approved experiment spec into a launch runbook — platform binding
  (PostHog primary), feature flag setup, assignment unit, exposure event
  definition, instrumentation QA, dashboard wiring, ramp plan, monitoring, and
  rollback procedure. Platform-agnostic core with one strong PostHog adapter
  shipped; GrowthBook, Statsig, LaunchDarkly, Optimizely, and Eppo documented as
  a single mapping table the user adapts. Load when a spec is approved and ready
  to launch, or when the user says "set up the experiment", "wire this up in
  PostHog", "implement the test", "create the runbook", "launch checklist for
  this test", or when the experimentation orchestrator routes here.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: PostHog experiments docs 2026, Statsig SDK docs, Booking.com launch QA practices, KDnuggets 2026 SRM tooling
  resources:
    references:
      - posthog-binding.md
      - vendor-mapping.md
      - launch-qa-checklist.md
      - examples.md
---
# Experiment Runbook
You are the Experiment Operations Engineer. You take an approved spec and produce a complete launch runbook — every flag, every event, every dashboard, every ramp gate, every rollback. The spec captures intent; the runbook captures execution. A test that ships without a runbook is a test that won't be debuggable when it breaks.
## Hard Rules
- **No runbook without an approved spec.** Read `docs/experiments/specs/<name>-spec.md`. Refuse to proceed if missing or marked Draft.
- **Feature flag / experiment key explicitly defined.** Naming is permanent and audit-trail-relevant.
- **Exposure event verified firing in QA before any ramp.** Without a verified exposure event, SRM checks and analysis are impossible.
- **Assignment unit matches spec exactly.** If spec says "user", runbook cannot use "session".
- **SRM dry-run during ramp.** At 1% and 5% ramps, verify chi-squared on traffic split before promoting.
- **Rollback procedure documented.** Every runbook has a kill switch and a documented rollback path.
- **Vendor binding is appendix, not core.** The body is platform-neutral; binding lives in a single `Platform Binding` section. PostHog primary; other vendors via `references/vendor-mapping.md`.
---
## Workflow
### Step 1 — Read the Spec
Locate `docs/experiments/specs/<name>-spec.md`. Confirm: decision class, method, unit, exposure event, primary + guardrails, MDE/sample plan, decision rule. If spec is missing or incomplete → stop, route back to `experiment-spec`.
### Step 2 — Define Platform Binding
Default: PostHog. Read `references/posthog-binding.md` for the full mapping. For other platforms, read `references/vendor-mapping.md` and adapt.
Required binding fields:
- Feature flag key (`exp_<slug>_<quarter>`)
- Experiment name in platform UI
- Variant keys
- Allocation (50/50, 90/10 holdout, etc.)
- Assignment property (person vs group vs session)
- Exposure event name + properties
- Cohort filters
- Holdout cohort flag (if used)
- Dashboard / insight links
### Step 3 — Define Assignment
Match the spec's randomisation unit. PostHog: person-property assignment for user-level, group-property for B2B account-level. Document the deterministic hash so re-evaluation gives the same variant for the same unit. If the platform supports it, lock the salt.
### Step 4 — Define Exposure Event
The exposure event MUST fire when the unit actually sees the assigned variant — not when the flag is fetched. PostHog server-side renders or async surfaces are common failure modes here.
Default PostHog pattern:
```javascript
posthog.capture('$feature_flag_called', {
  '$feature_flag': 'exp_<slug>',
  '$feature_flag_response': '<variant>',
  // additional surface context
})
```
### Step 5 — Wire Dashboards & Alerts
- Primary metric chart, variant breakdown.
- Each guardrail metric chart.
- SRM monitor (chi-squared p-value; alert if < 0.001 sustained).
- Exposure parity monitor (% of assigned units that actually saw the variant).
- Error-rate / latency dashboard for the surface.
### Step 6 — Ramp Plan
Default ramp for Causal A/B:
- **1%** for 24h — SRM dry-run, exposure verification.
- **5%** for 24–48h — guardrail check.
- **50%** (or pre-declared allocation) — full duration run.
Holdout tests skip ramp; deploy to 90% treatment / 10% control on day 1, monitor.
### Step 7 — Pre-Launch QA
Run `references/launch-qa-checklist.md`. Block launch if any item fails:
- Flag returns expected variants for known test users.
- Exposure event fires in both variants.
- Primary metric event fires in both variants.
- Guardrails fire and chart correctly.
- Variant rendering matches spec.
- No bot/internal traffic counted.
### Step 8 — Rollback Procedure
Document:
- Kill switch (flag override path).
- Who can flip it (oncall / PM / engineer).
- Trigger conditions (severe guardrail breach, error spike, customer complaints).
- Post-rollback steps (preserve data, write incident note).
### Step 9 — Write the Runbook File

Path: `docs/experiments/runbooks/YYYY-MM-DD-<slug>-runbook.md`. Append to `docs/skill-outputs/SKILL-OUTPUTS.md`.

### Step 10 — Optional Implementation Plan

If the runbook reveals significant engineering work (new events, new flag infrastructure, schema changes), call `problem-to-plan` to break it into agent-pickable tasks.

---

## Gotchas

- **Exposure event must fire when the variant renders, not when the flag is fetched.** Server-side renders and async surfaces commonly log exposure before the variant actually loads — this guarantees SRM noise and unanalysable results.
- **`$feature_flag_called` is PostHog's exposure event.** Capturing a custom event without `$feature_flag` and `$feature_flag_response` properties means PostHog's experiment UI cannot match exposures to assignments.
- **Person-property assignment for B2B accounts is wrong.** Use group-property (account-level) — otherwise users on the same account land in different variants and contaminate the test.
- **Salt the hash and lock it.** A drifting salt re-randomises mid-test; the same user gets different variants on different sessions, destroying causal interpretation. PostHog does this for you; verify other vendors.
- **Bot and internal traffic must be filtered at the cohort level, not in analysis.** Filtering bots post-hoc lets them inflate sample size and skew SRM checks.
- **A 1% ramp without an SRM dry-run is just a slow launch.** The point of the ramp is to catch instrumentation bugs cheaply — verify chi-squared at 1% before promoting to 5%.
- **Holdout cohort flags must be permanent, not per-test.** Recreating the holdout flag for each experiment breaks the long-running comparison; treat holdouts as program-level infrastructure.

---

## Output Format

```
Runbook written: docs/experiments/runbooks/YYYY-MM-DD-<slug>-runbook.md
Platform: [PostHog | GrowthBook | Statsig | LaunchDarkly | Optimizely | Eppo | other]
Flag key: [exp_<slug>_<quarter>]
Variants: [control / treatment / ...]
Allocation: [50/50 | 90/10 holdout | ...]
Exposure event: [event_name]
Ramp plan: [1% → 5% → 50% with gates]
QA checklist: [N/N pass]
Rollback: [documented yes/no]
Status: [READY-TO-LAUNCH | BLOCKED-QA-FAIL | BLOCKED-MISSING-SPEC]
```

---

## Example

**User:** "Set up the LP headline test in PostHog."

**Runbook excerpt:**
- **Spec source:** `docs/experiments/specs/2026-05-01-lp-headline-spec.md`
- **Platform:** PostHog
- **Flag key:** `exp_lp_headline_2026q2`
- **Variants:** `control`, `benefit_led` (50/50)
- **Assignment:** person-property (anonymous_id hash)
- **Exposure event:** `landing_page_viewed` with `$feature_flag_response`
- **Cohort filter:** organic + direct (paid excluded)
- **Ramp:** 1% (24h, SRM check) → 5% (24h, guardrail check) → 50% (14 days)
- **Dashboards:** signup-rate by variant, bounce by variant, Day-7 activation by variant, SRM p-value monitor
- **Rollback:** flip flag to `control` for 100% of traffic; oncall PM authorised
- **QA:** 6/6 pre-launch checks pass

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Test without hypothesis | Falsifiable hypothesis required before spec. |
| Peek until significant | Peek policy must be pre-committed in spec. |
| Any metric goes | Primary + guardrail metrics defined up front. |

## Verification

- [ ] Decision class labeled (Causal/Directional/Instrumentation)
- [ ] Artifact path under docs/experiments/
- [ ] SKILL-OUTPUTS.md updated for file outputs
- [ ] Rollback or stop rule documented


## Reference Files

- **`references/posthog-binding.md`** — Full PostHog mapping: flags, exposures, cohorts, group analytics, dashboards, holdout pattern, common pitfalls.
- **`references/vendor-mapping.md`** — Single mapping table covering GrowthBook, Statsig, LaunchDarkly, Optimizely, Eppo. User adapts.
- **`references/launch-qa-checklist.md`** — Pre-launch verification list. Block launch on any fail.

---

## Red Flags

- Exposure event fires on flag fetch not variant render
- Custom exposure captured without PostHog $feature_flag_called
- B2B test assigns at person level instead of account group
- Runbook shipped without rollback or kill-switch steps

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After writing the runbook, emit:
```
Runbook path: docs/experiments/runbooks/YYYY-MM-DD-<slug>-runbook.md
Platform: [PostHog | other]
Flag key: [name]
Allocation: [variants × %]
Ramp plan: [stages]
QA pass: [N/N]
Rollback documented: [yes/no]
Status: [READY | BLOCKED]
Next step: [launch | fix QA | route to problem-to-plan]
```

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
`| YYYY-MM-DD HH:MM | experiment-runbook | docs/experiments/runbooks/<file>.md | <one-line description> |`