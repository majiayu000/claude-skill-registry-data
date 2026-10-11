---
name: factory-config
description: Use when creating, editing, or validating an Agent Relay Factory factory.config.json file, including repo routing, Linear state/team settings, GitHub issue ingestion, live mode, babysitter options, and Relayflows dispatch wiring boundaries.
---

# Factory Config

Create valid `factory.config.json` files for `@agent-relay/factory`.

## Source of Truth

Use the factory repo schema before inventing fields:

- `factory/src/config/schema.ts` exports `FactoryConfigSchema`.
- `factory/src/config/schema.test.ts` shows valid examples and defaults.
- There is currently no checked-in JSON Schema artifact; the authoritative schema is Zod.

Validate with the installed or local factory:

```bash
factory run-once --config ./factory.config.json --dry-run
```

If the current CLI defaults are available, `factory start` uses `./factory.config.json` and starts live mode. Otherwise use the explicit form:

```bash
factory start --mode live --config ./factory.config.json
```

## Recommended Shape

Prefer compact repo config. `workspaceId` is optional; omit it to use the active relayfile cloud workspace.

```json
{
  "subscription": {
    "teams": ["AR"]
  },
  "repos": {
    "org": "AgentWorkforce",
    "cloneRoot": "/Users/khaliqgant/Projects/AgentWorkforce",
    "names": ["relayfile-adapters"],
    "default": "AgentWorkforce/relayfile-adapters"
  },
  "safety": {
    "requireTitlePrefix": "[factory]",
    "requireLabel": "factory",
    "requireTeamKey": "AR"
  },
  "linear": {
    "states": {
      "readyForAgent": "Ready for Agent",
      "agentImplementing": "Agent Implementing",
      "inPlanning": "In Planning",
      "done": "Done",
      "humanReview": "In Human Review"
    }
  },
  "mergePolicy": "never"
}
```

Compact repo config derives:

- `repos.byLabel.<name>` as `<org>/<name>`, with `repos.overrides` for exceptions.
- `repos.clonePaths.<owner/repo>` from `cloneRoot`.
- `subscription.labels` from `repos.names` unless explicitly set.

Use explicit `repos.byLabel` when a label should route to a repo not derivable from `org` and `names`.

## GitHub Issue to Linear to PR

For GitHub issues labeled `factory`, include the GitHub repo in `repos.names` or `repos.byLabel`. The factory mirrors matching GitHub issues to Linear, then dispatches once the Linear mirror is in Ready for Agent.

For Linear create writeback, prefer the team key only: `safety.requireTeamKey` and `subscription.teams` should use the Linear team key such as `AR`. GitHub mirrors carry `team.key`; the Linear writeback provider resolves that key to the provider-side team ID. `linear.teamIds` remains an optional escape hatch for workspaces that explicitly need UUID pinning, but do not add it by default.

## Relayflows and Integration Event Dispatch

Factory can launch dynamic Relayflows from Relayfile integration events when the deployment wires a Relayflows port/template registry into the factory runtime. Treat that as SDK wiring, not as an automatic `factory.config.json` field. Do not invent JSON keys unless `FactoryConfigSchema` exposes them.

The clean model is:

1. Factory subscribes to Relayfile provider events such as Linear issue created, GitHub PR review submitted, or status check changed.
2. The runtime suppresses replayed/high-watermark events before dispatch.
3. A Relayflow template registry maps the event to a template, for example `linear.issue.created -> templates/linear-issue-triage.yaml`.
4. Factory calls the Relayflows SDK directly to run the selected workflow. It must not shell out to `relayflows`, `gh`, `linear`, or other local CLIs.
5. The Relayflow template declares `integrations.relayfile: {}` and uses subscriptions, `waitFor`, or integration steps for provider interaction.

`workspaceId` remains optional in config and should be omitted by default so the active Relayfile cloud workspace is used. For code-changing workflows, ensure `repos.clonePaths` or compact `repos.cloneRoot`/`repos.names` resolve to real local checkouts; the factory runtime can start mounts for those clone paths so spawned agents see `.integrations` writebacks.

When configuring live event-driven Relayflows, prefer `liveSubscription.transport: "subscribe"` if the deployment exposes that option. Polling transports are fallback/compatibility modes, not the intended path for new Relayfile event dispatch.

Use Relayflows when the task needs a multi-agent graph, human-assistance gate, long-lived provider subscription, or a PR babysitter loop. Use Factory's direct task dispatch when a Linear/GitHub item can be handled by a single existing factory agent flow without a workflow graph.

## Linear States

Prefer dynamic state-name resolution:

```json
{
  "linear": {
    "states": {
      "readyForAgent": "Ready for Agent",
      "agentImplementing": "Agent Implementing",
      "inPlanning": "In Planning",
      "done": "Done",
      "humanReview": "In Human Review"
    },
    "statesByTeam": {}
  }
}
```

The resolver first uses `/linear/states` when available. If that catalog is absent but synced Linear issue records include `state.name` plus `stateId`, it derives the role IDs from those real Linear records. `stateIds` is only an escape hatch for setups with neither a states catalog nor enough synced issue state data, and may omit roles that resolve by name.

For teams that use different workflow state names, scope overrides by team key:

```json
{
  "linear": {
    "states": {
      "readyForAgent": "Ready for Agent",
      "agentImplementing": "Agent Implementing",
      "inPlanning": "In Planning",
      "done": "Done",
      "humanReview": "In Human Review"
    },
    "statesByTeam": {
      "ENG": {
        "readyForAgent": "To Do",
        "agentImplementing": "Building",
        "inPlanning": "Backlog",
        "done": "Shipped"
      }
    }
  }
}
```

## Babysitter

The PR babysitter is **off by default**:

```json
{
  "babysitter": { "enabled": false },
  "models": { "babysitter": "sonnet" }
}
```

Enable it when the factory should spawn a follow-up agent after an implementer opens a PR:

```json
{
  "babysitter": { "enabled": true },
  "terminalState": "human-review",
  "models": { "babysitter": "sonnet" }
}
```

With babysitter enabled, PR-open completion is webhook-driven: the babysitter shepherds review comments, conflicts, and CI, then signals readiness before the issue advances.

## Common Defaults

- `batchSize`: `5`
- `mergePolicy`: `"never"`
- `safety.requireLabel`: `"factory"`
- `safety.requireTeamKey`: `"AR"`
- `models.babysitter`: `"sonnet"`
- `babysitter.enabled`: `false`
- `terminalState`: `"human-review"`
- `loop.maxIterations`: `3`
- `liveSubscription.transport`: `"subscribe-and-poll"`

## Checklist

Before finishing a config:

1. Confirm every repo label used by issues maps through `repos.byLabel` or compact `repos.names`.
2. Confirm `cloneRoot`/`clonePaths` point to real local checkouts.
3. Confirm `subscription.teams` and `safety.requireTeamKey` use Linear team keys, not UUIDs.
4. Confirm state names match the target Linear workspace, using `linear.statesByTeam` for teams with different names.
5. For Relayflows dispatch deployments, confirm the SDK template registry and Relayflows port are wired in code, not invented as unsupported config keys.
6. Confirm Relayflow templates use `integrations.relayfile: {}` and do not require `workspaceId`, tokens, or local provider CLIs.
7. Run `factory run-once --config ./factory.config.json --dry-run`.
