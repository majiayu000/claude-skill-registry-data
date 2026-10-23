---
name: github-actions-authoring
description: Design event-driven GitHub Actions without remote-state polling.
---

# GitHub Actions authoring

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/github-actions-authoring/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Never poll in CI. A workflow reacts to a state transition. Read
[github-actions-checklist](../github-actions-checklist/SKILL.md) first, then every applicable
`AGENTS.md`. Repository-local policy and the consumer wrapper own runner labels,
permissions, action pins, concurrency, secrets, and required-check names.

## Design the event graph

- Name the producer, the durable transition it emits, and the consumer that owns the next action.
- Use `needs` for jobs in one workflow. Use `workflow_call` when the caller must await a reusable
  workflow. When a consumer must run after failure or skip, give it an explicit status condition and
  read `needs.<job>.result`. The implicit success condition skips it otherwise.
- Use `workflow_run` when a completed workflow is the trusted event boundary. Validate the source
  workflow, repository, branch or pull-request head, conclusion, and artifacts before acting.
- The `workflow_run` receiver must already exist on the default branch. GitHub chains at most three
  `workflow_run` levels. Plan that rollout, and collapse a deeper chain into one DAG.
- Use `repository_dispatch` for a cross-repository transition or an authenticated external callback.
  Authenticate the sender, pass immutable correlation data, validate it against the source, and make
  duplicate delivery safe. The receiver must already exist on the default branch before senders are
  enabled.
- Prefer a provider-native completion event, callback, queue, or state-machine transition for a
  deployment or service.
- A scheduled reconciliation workflow may repair a missed event. It inspects one snapshot and exits.
  It does not wait for convergence.

## Persistent workspaces

Apply the persistent-workspace rules in
[github-actions-checklist](../github-actions-checklist/SKILL.md).

## Reject polling designs

- Do not add a sleep-and-read loop, a repeated query of a run, check, deployment, lease, or
  service, a CLI waiter, or a recursive redispatch whose purpose is to watch remote state change.
- A timeout caps cost. It does not make polling event-driven.
- If the producer cannot emit a usable event, add the bridge at the producer or provider boundary
  and let that bridge dispatch the correlated completion event.
- Bounded retries are allowed only for the same failed operation, and only when the failure is
  transient and the operation is idempotent.
- A local process readiness check is allowed when that process runs inside the job and cannot emit
  a workflow event.
- Neither exception allows repeated observation of remote state.

## Validate the result

- Test accepted, rejected, duplicate, stale, and out-of-order events.
- Preserve required-check names. Prove that every terminal producer outcome causes one terminal
  consumer outcome.
- Run the local workflow checker and affected tests. Inspect the event graph for credentials
  crossing an untrusted boundary, a missing correlation field, and any remaining polling path.

Consumer wrapper owns: runner labels, permissions, action pins, concurrency, secrets, and
required-check names.
