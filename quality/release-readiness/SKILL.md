---
name: release-readiness
description: Go / no-go gate before any deployment. Checks failure modes, rollback plan, cost, production bar, and definition of done. Trigger before releasing to any environment that carries real consequences.
---

# Release Readiness

> **A working demo is not evidence of production readiness. Production readiness is proven through sustained operation, incident handling, cost predictability, and controlled evolution.**

This skill enforces the production bar. It produces a go / no-go verdict with a signed checklist. No checklist = no go.

## When to use

- Before deploying to staging or production
- Before handing a system to another team
- Before declaring a sprint or milestone complete
- When someone says "it works on my machine"

## Procedure

1. **Validate the definition of done** — confirm that acceptance criteria from the spec are met. "Looks good" is not a criterion. Run the actual validation commands.

2. **Check all quality gates pass**:
   - `make lint` — style and static analysis clean
   - `make typecheck` — no type errors
   - `make test` — unit tests green
   - `make e2e` — end-to-end tests green (or equivalent for your stack)
   - No outstanding HIGH or CRITICAL findings from security scan

3. **Name the failure modes** — at minimum:
   - What happens if the service is unavailable?
   - What happens under unexpected load?
   - What happens if a dependency (external API, database, queue) is degraded?
   - What is the data-loss risk?

4. **Confirm rollback exists and is tested** — a rollback plan that has never been tested is not a rollback plan. If the rollback has not been exercised, flag it.

5. **Estimate cost impact** — LLM calls, storage writes, egress, third-party API calls. Any unbounded cost vector must be capped or accepted explicitly.

6. **Confirm monitoring and alerting** — what fires when this breaks? Who gets the alert? What is the on-call runbook?

7. **Check data boundaries** — does the release touch PII, regulated data, or cross a tenant boundary? If yes, confirm the appropriate controls are in place.

8. **Sign off** — record: who reviewed, what was checked, what was accepted as known risk, and the go/no-go verdict.

## Outputs

- Signed release checklist (append to PR or release doc)
- Go / no-go verdict
- List of accepted known risks with named owners

## Guardrails

- **No go without a rollback plan.** "We'll figure it out" is not a rollback.
- **Green CI is necessary, not sufficient.** CI validates happy paths. Release readiness validates failure modes.
- **Cost estimates are not optional.** An unbounded LLM call in a hot path is a production incident waiting to happen.
- **Monitoring must exist before go-live, not after.** "We'll add monitoring later" means the first incident is invisible.

## Anti-rationalization table

| Excuse | Counter |
|---|---|
| "CI is green, we're good to go" | CI checks known paths. Release readiness checks failure modes CI doesn't cover. |
| "We'll monitor it after launch" | The first failure will be invisible. Add monitoring before go-live. |
| "Rollback is just redeploy the previous version" | Untested. Run the rollback in staging first. |
| "Cost is fine, it's low traffic" | Low traffic + an LLM loop bug = runaway spend. Cap it. |
