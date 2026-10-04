---
name: deploy
description: Use this skill during Phase 6 to deploy code that has passed Phase 5 Test. Updates tickets with deployment details when a ticketing system is configured; otherwise generates deployment artifacts as markdown or JSON under .claude/sdlc/deployments/. Never auto-executes a deployment — always proposes and waits for explicit human confirmation. Trigger after test is signed off, or when the user says "deploy", "release", or "ship".
next_suggestions:
  - when: deploy_gate_signed
    suggest: "run /support to wire observability for the deployment"
  - when: phase_active_gate_unsigned
    suggest: "open gates/deploy-<task-slug>.md and sign it manually, then run /support"
---

# Deploy (Phase 6)

Release code that has passed Test — under explicit human approval.

## Prerequisite

`.claude/sdlc/gates/test-<task-slug>.md` must exist and be signed. Without it, this skill refuses to run.

## Step 1 — Propose the deployment

Produce a deployment proposal, not a deployment. Include:

- Target environment (dev / staging / production)
- Commit SHA / tag / image reference
- Changed files and services
- DB migrations? (yes/no, reversible?)
- Feature flags? (default state)
- Rollback plan
- Blast radius (users/services affected)
- Deployment window / maintenance window if applicable

## Step 2 — Human approval gate

**This is non-negotiable.** Deployments never auto-execute. Ask the human to confirm the proposal. Record the approval at `.claude/sdlc/gates/deploy-<task-slug>.md` with timestamp and approver.

## Step 3 — Execute (under human supervision)

Execute the deployment via the configured pipeline/runbook. Stream output. Halt on the first error and ask for direction — do not retry automatically.

## Step 4 — Record

Update the ticket(s) with:

- Commit SHA, environment, timestamp, approver
- Link to pipeline run / deployment log
- Post-deploy verification results (smoke tests)

Detection:

- GitHub/GitLab Issues via `.claude/sdlc/env.json` → comment on the issue
- Jira/Linear via MCP → transition to "Deployed" (or equivalent) with a comment
- None configured → write `.claude/sdlc/deployments/<YYYY-MM-DD>-<task-slug>.md` (or `.json` if configured)

## Step 5 — Post-deploy verification

Run the smoke-test subset of the test suite against the deployed environment. If any fail:

- Execute the rollback from Step 1
- Log a defect (see `test` skill)
- Do not mark the deployment complete

## What this skill must NEVER do

- Auto-execute a deployment.
- Skip the rollback plan.
- Close a ticket before post-deploy verification passes.
- Deploy code that does not have a signed test gate.

## References

- `templates/deployment.md`
- `templates/gate.md`
- `docs/SDLC.md` Deploy

## Next step hint

After the deployment record is written, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'deploy_gate_signed|run /support to wire observability for the deployment' \
  'phase_active_gate_unsigned|open gates/deploy-<task-slug>.md and sign it manually, then run /support' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing, add nothing.
