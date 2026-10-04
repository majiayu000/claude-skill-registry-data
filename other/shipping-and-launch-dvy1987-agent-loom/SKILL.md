---
name: shipping-and-launch
description: >
  Prepare safe production launches — pre-launch checklist, monitoring, staged
  rollout, and rollback. Load when deploying to production, releasing a major
  change, opening beta access, or the user asks for a launch checklist, go-live
  plan, rollout strategy, or rollback plan. Not for local-only prototypes.
  Pairs with ci-cd-and-automation and app-security-hardening.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: addyosmani/agent-skills shipping-and-launch (11/12, 2026-05-29)
  resources:
    references:
      - examples.md
---

# Shipping and Launch

Ship with confidence: reversible, observable, incremental. Every launch has a rollback path and success metrics defined before traffic moves.

## Hard Rules

- **No launch without rollback** — feature flag, previous artifact, or DB migration down path.
- **Monitoring before traffic** — alerts on errors, latency, and business KPIs.
- **Staged rollout** — internal → beta → % canary → full unless risk is trivial.
- **Checklist is blocking** — unchecked security/perf/a11y items are explicit deferrals with owner.
- **Communicate** — stakeholders know window, owner, and rollback trigger.

---

## Workflow

### Step 1 — Define success and risk

Document: what ships, who is affected, success metrics, rollback triggers (error rate, latency, support tickets).

### Step 2 — Pre-launch checklist

Minimum gates:

- Tests green (unit, integration, e2e on critical paths)
- No secrets in repo; dependencies audited for critical CVEs
- Performance budgets met on changed surfaces
- Accessibility spot-check on changed UI
- Runbook: deploy steps, owner, comms channel

### Step 3 — Staged rollout

1. Deploy to staging with prod-like data volume if possible
2. Internal dogfood or feature flag to staff
3. Canary (% traffic or invite-only beta)
4. Full rollout with monitoring watch window

### Step 4 — Monitor and decide

Watch 24–72h (risk-dependent): error rate, p95 latency, Core Web Vitals, conversion/support signals.

### Step 5 — Rollback or complete

If triggers hit → rollback first, postmortem second. If stable → remove flags, archive runbook learnings.

---

## When NOT to use

- Pure local dev with no users
- Changes already live behind a flag with an existing runbook (update runbook only)

---

## Gotchas

- "Green staging" with 10x less data than prod hides query issues.
- Launch without feature flags forces redeploy to rollback.
- Announcing before monitoring is wired means flying blind.
- Skipping comms strands on-call.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's a small change" | Small deploys still need rollback and error visibility. |
| "We'll add alerts after launch" | You discover outages from users instead of dashboards. |
| "Full send is faster" | One incident costs more than a canary day. |
| "Rollback is unlikely" | Plan for it anyway — Hyrum's Law applies in prod. |
| "Checklist is bureaucracy" | It's how you remember security and a11y under time pressure. |

---

## Output Format

```markdown
## Launch plan — [feature]

Risk: [low/med/high] | Rollback: [how]
Stages: [list] | Metrics: [list]
Checklist: [pass/deferred items]
Owner / window: [who / when]
```

---

## Examples

<examples>
  <example>
    <input>"Ship new billing flow Friday."</input>
    <output>Feature flag at 5% → 25% → 100%; dashboards on payment errors; rollback = disable flag; checklist signed.</output>
  </example>
</examples>

---

## Verification

- [ ] Rollback path documented and tested (or dry-run)
- [ ] Monitoring/alerts live before user traffic
- [ ] Staged rollout plan matches risk level
- [ ] Pre-launch checklist complete or deferrals explicit
- [ ] Success metrics and rollback triggers defined

---

## Red Flags

- Launch without rollback path or previous artifact
- Traffic shifted before error and KPI monitors exist
- Full rollout for non-trivial change without canary
- Staging-only validation at fraction of prod data volume

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Feature: [name] | Risk: [level]
Stages: N | Rollback: [ready/deferred]
Checklist: [N pass / M deferred]
```
