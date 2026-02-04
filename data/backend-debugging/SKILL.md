---
name: backend-debugging
description: Systematic debugging for Encore.ts backend incidents using diagnostic scripts, database queries, and structured logging. Use when backend tests fail, services crash, or async flows stall.
---

# Backend Debugging Skill

## Mission
Restore failing Encore.ts flows quickly by combining structured logs, targeted SQL queries, and the diagnostic script arsenal. This skill keeps the top-level procedure concise; each reference file contains deep dive playbooks.

## When to Use
- `encore test` failures or flaky integration tests
- Stalled workers (runs stuck `queued`/`in_progress`)
- Graph projector or subscription issues
- CI regressions surfaced by `task backend:test` or smoke suites

## Rapid Response Workflow
1. **Reproduce & capture context** – Re-run the failing test with `encore test …` and collect assertion + log data.
2. **Inspect database state** – Use targeted queries from `references/debug-queries.md` to confirm run status, events, and projector outcomes.
3. **Run diagnostic scripts** – Leverage the tools catalogued in `references/diagnostic-scripts.md` to inspect timelines, cursors, and agent snapshots.
4. **Apply fix & verify** – Update code, rerun tests, and document the outcome in Graphiti (include root cause + remediation).

## Triage Aids
- `references/common-failures.md` – Symptom ➜ cause ➜ fix matrix for the most frequent issues (queued runs, hanging services, alias errors, projector lag, budget exhaustion).
- `references/detailed-examples.md` – Step-by-step walkthroughs, including the "0 screens discovered" scenario and RCA templates.

## Debugging Checklist
- Worker claimed the run (status not `queued`)
- Subscription imports present in test file
- Run completed (`status = 'completed'`)
- Events emitted and projector outcomes present
- Async processing given time to complete (polling, not sleeps)
- Appium/device online when required
- Structured logs inspected for module/actor context

## Critical Rules
- **Structured Logging:** Use `encore.dev/log` with `module`, `actor`, and identifiers (`runId`).
- **Subscriptions:** Import every PubSub worker in tests before publishing events.
- **Polling:** Prefer polling loops with timeouts over fixed `setTimeout` sleeps.

## Reference Library
- `references/debug-queries.md` – SQL snippets for runs, events, projector state, and lag analysis
- `references/diagnostic-scripts.md` – CLI usage notes for `inspect-run.ts`, `check-agent-state.ts`, `check-cursor-ordering.ts`, and friends
- `references/common-failures.md` – Symptom → cause → fix catalogue for top regressions
- `references/detailed-examples.md` – Expanded case studies (e.g., projector lag, budget exhaustion)

## Testing in CI/CD
```yaml
# .github/workflows/test.yml
- name: Run backend tests
  run: |
    cd backend
    encore test
```
**Prerequisites:** Appium + device available for integration suites, environment variables configured, Run logs streamed via `task backend:logs` when debugging CI.

## Related Skills
- `backend-development_skill` – Integration-first testing patterns that prevent regressions
- `e2e-testing_skill` – Playwright coverage for verifying frontend/backends flows end-to-end
- `graphiti-mcp-usage_skill` – Capture debugging RCA and permanent fixes in the knowledge graph
