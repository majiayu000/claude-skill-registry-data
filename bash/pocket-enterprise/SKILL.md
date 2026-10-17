---
name: pocket-enterprise
description: Adds the registered Enterprise lifecycle adapter to a compatible Core installation. Use only when the user explicitly enables the Enterprise layer.
---

# Pocket Enterprise

Pocket Enterprise is an optional, additive adapter for teams that explicitly choose remote lifecycle synchronization. Install the Enterprise role beside its matching Core role; it does not bundle or copy Core skills.

**Core principle:** Core commits local state and neutral lifecycle events first. Core does not call `gh`, does not merge pull requests, and does not close issues. The adapter validates compatibility before any external operation, reconciles events deterministically, and leaves ambiguous ownership for a human.

## Release and compatibility

The `surfaces.json` manifest has schema `1` and defines exactly `pi/core`, `pi/enterprise`, `claude/core`, and `claude/enterprise`. Enterprise roles are deltas requiring their matching Core role. Release versions are package `4.2.2`, CLI `CONTRACT=3`, `PIPELINE=5`, lifecycle schema `2`, adapter contract `2`, and surface manifest `1`; these are independent version boundaries.

| Core | Enterprise | Result |
|------|------------|--------|
| v3 | v3 | Legacy installation remains operational with a v4 warning. |
| v4 | v4 | Supported. |
| v4 | absent | Core remains local-first; pending events are retained without GitHub calls. |
| v3 | v4 | Enterprise fails closed with Core upgrade guidance; v3 Core remains usable. |
| v4 | v3 | The adapter fails closed with Enterprise upgrade guidance; pending v4 events are retained. |

The v4 preflight warns about legacy v3 installations; an unchanged v3 binary cannot warn about a future release. Never infer consent from a remote or credentials. A registration must declare adapter contract `2`; reinstall the adapter after upgrading, because a contract `1` registration fails preflight with `ENTERPRISE_ADAPTER_CONTRACT_MISMATCH`. Follow `references/onboarding.md` for setup, phase-branch options, and registration.

## Activation and preflight

Run the Enterprise preflight from the project root:

```bash
node enterprise/cli.js preflight <project-root> --json
```

`enterprise/cli.js` is in the pocketto-pi package root, not in the project being checked. The command above is a checkout of this repository. A project that depends on the npm package runs `node node_modules/pocketto-pi/enterprise/cli.js preflight <project-root> --json`.

Continue only when it confirms a compatible Core installation and registered adapter. Missing Core, an unsupported contract, malformed registration, or a missing executable is fail-closed: make no GitHub call and follow the install/upgrade action in the error. Preflight is read-only.

Core provides the lifecycle commands with `--json --contract 3`:

```bash
pocketto-pi lifecycle transition <spec_dir> <event-type> --artifact <root>:<kind>:<relative-path>:<sha256> --json --contract 3
pocketto-pi lifecycle drain <spec_dir> --json --contract 3
pocketto-pi lifecycle repair <spec_dir> --json --contract 3
pocketto-pi lifecycle migrate <spec_dir> --from v3 --json --contract 3
```

`transition` commits local state and a durable event before optional delivery. `drain` replays pending events in revision order and creates no event. `repair` reconciles lifecycle-owned projection fields only when task state is recoverable; it does not emit or dispatch an event. Run `drain` only after a successful Enterprise preflight. If Enterprise is absent or unavailable, Core work remains successful and event IDs remain available for replay.

## Lifecycle routing

Core emits only neutral event names and artifact references. The event journal and protocol boundary are defined in `references/lifecycle-contract.md`.

| Event | Enterprise-owned action |
|-------|-------------------------|
| `spec-approved` | Reconcile the approved spec with its owned issue; see `references/issue-reconciliation.md`. If delivery reports `GH_UNKNOWN`, follow [Missing-label consent recovery](references/issue-reconciliation.md#missing-label-consent-recovery). |
| `phase-complete` | Reconcile an existing phase PR and its proof; see `references/phase-reconciliation.md`. A missing PR is `PR_REQUIRED`; the adapter never creates one. For stacked plans this event is deferred to `phase-closed`. |
| `phase-closed` | Stacked plans only. Publish the closed phase PR with its stack identity, summary, findings, and stack proof, pushing its phase branch only with consent; see `references/phase-reconciliation.md`. A missing consent is retryable `PUSH_CONSENT_REQUIRED`. |
| `plan-closed` | Reconcile the final tasklist proof on the linked issue; see `references/phase-reconciliation.md`. |

The adapter owns GitHub IDs, credentials, and remote proof in Enterprise-owned metadata. Core lifecycle records contain no GitHub IDs or credentials. Enterprise issue reconciliation may create one issue for `spec-approved`; it does not create an issue for phase or closure events. `create-pr` is a separate, explicit user-triggered recorder; for stacked plans it runs `publish-phase`, the same publisher the `phase-closed` handler uses.

## Ownership and human gates

- Issue, PR, comment, and remote tasklist synchronization belongs to this Enterprise adapter. Core makes no GitHub calls.
- Never copy or modify a Core skill to add remote behavior; keep Core source canonical and install Enterprise only as its declared additive delta.
- Do not guess when an issue, PR, marker, or owner is ambiguous. Stop with an actionable manual-resolution request and make no mutation.
- The adapter never merges a PR or closes an issue. Those actions remain human-controlled.

## Migration and rollback

Active v3 plans with progress stay on the v3 CLI/Enterprise path. Migration is explicit:

```bash
pocketto-pi lifecycle migrate <spec_dir> --from v3 --json --contract 3
```

Only a pristine v3 plan with no execution progress can migrate. Progress or a non-pristine plan returns `PIN_V3_REQUIRED` without changing files or making remote calls; finish the plan under v3. No v3 progress is silently converted.

To roll back Enterprise, disable or remove the adapter while retaining Core and the authoritative `lifecycle.json`. Preserve `.pocket-meta.json`, `log.json`, pending lifecycle events, and remote markers. Core continues locally. Pin a faulty adapter to the last compatible v4 release, correct it, then replay pending events with `pocketto-pi lifecycle drain <spec_dir> --json --contract 3` using their original IDs. Do not delete lifecycle state, rewrite v3 plans, or automatically downgrade v4 state.
