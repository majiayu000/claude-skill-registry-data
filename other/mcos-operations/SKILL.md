---
name: mcos-operations
description: Use when operating, configuring, or troubleshooting a running Master Control Orchestration Server through the mcos-bridge MCP tools. Covers procedural runbooks for the most common live-system tasks and the trust/safety invariants that bound them.
---

# MCOS Operations Skill

You have access to the `mcos-bridge` MCP server, which exposes ~43 tools named `mcos_*`. They translate to HTTP calls against the MCOS admin API at `MCOS_BASE_URL` (default `http://localhost:7300`).

## Hard rules

These don't bend. The bridge enforces them where it can.

1. **Trust at the network layer.** ADR-001 §3 / ADR-002 §1 — there is no app-layer auth on the operator surface. The plugin reaches MCOS over the LAN; firewall scoping is the load-bearing trust control.
2. **Confirm:true on destructive ops.** `mcos_pool_drain`, `mcos_pool_remove`, `mcos_gateway_stop`, `mcos_governance_reject`, `mcos_client_disable`, `mcos_forsetti_module_disable` all return `errorCode: CONFIRM_REQUIRED` unless `confirm:true` is passed. Never auto-pass `confirm:true` — the operator approves.
3. **State the intent before each write.** One sentence describing what's about to happen and what the consequence is.
4. **Verify after every write.** Re-call the matching read tool. Don't claim a write succeeded without a follow-up read confirming the new state.
5. **No bypass of the architecture.** The bridge talks the documented HTTP API. Don't poke runtime state directly. Don't touch Forsetti vendored code (`Forsetti-Framework-Windows-main/`) — sealed by ADR-002 §11 and FORBIDDEN-CONTRACT §5.1.
6. **Honest telemetry.** When a tool returns a metric as `-1.0`, that means "unavailable" — the data source did not report it. Don't render it as `0%` (that would be `idle`). ADR-002 §9.

## Operator workflows

### Daily quick-look

```
mcos_health
mcos_dashboard
mcos_gateway_status + mcos_gateway_health
mcos_pools_list  (then per-pool mcos_pool_saturation)
mcos_telemetry_clients
mcos_governance_approvals (filter status=pending)
```

Summarize in one paragraph. Surface anomalies up top.

### "Something is wrong"

Hand off to `mcos-troubleshooter` sub-agent. Don't speculate without data — the agent walks the diagnosis chain via tool calls.

### Add a worker pool

Hand off to `mcos-pool-architect` sub-agent for design. The agent picks scale policy from workload heuristics, surfaces the diff, applies via `mcos_pool_upsert`, scales via `mcos_pool_scale`, verifies via `mcos_pool_get`.

### Apply a config change

```
1. mcos_config_get                    # read current
2. State the diff to operator
3. Wait for confirmation
4. mcos_config_update fields={...}    # write
5. mcos_config_get                    # verify
6. Note whether a service restart is needed
```

Most fields hot-apply. `mcpGateway.binaryPath`, `bindAddress`, and `instanceId` need a service restart.

### Onboard an AI client

```
1. mcos_onboarding clientType=<type>
2. Surface the manualInstructions verbatim
3. Surface configSnippets verbatim (don't paraphrase)
4. Surface verificationSteps + caveats
```

The operator copies the snippet into the AI client's config. MCOS does not push config to the client.

### Drain a pool gracefully

```
1. mcos_pool_get poolId=<id>           # current state
2. mcos_pool_leases poolId=<id>        # what's bound
3. State consequence to operator (sticky leases keep routing; new ones go elsewhere)
4. Wait for confirmation
5. mcos_pool_drain poolId=<id> confirm=true
6. mcos_pool_saturation poolId=<id>    # verify
```

### Approve / reject a governance action

Hand off to `mcos-governance-reviewer` sub-agent. The agent surfaces pending items in plain language with quoted payloads, waits for operator decision, applies via `mcos_governance_approve` or `mcos_governance_reject confirm=true`.

### Import a Forsetti module

Use the `/mcos:forsetti-import` slash command. The flow validates that the manifest's `entryPoint` matches a name registered in `src/MasterControlModules/MasterControlModules.cpp` BEFORE importing — otherwise the registration would load but `ModuleManager::makeModule` would throw `EntryPointNotFound` at runtime.

## Read-only diagnostic tools

These don't change state — use freely.

| Tool | What it returns |
|---|---|
| `mcos_health` | Service responsive? |
| `mcos_dashboard` | Top-level snapshot |
| `mcos_gateway_status` / `mcos_gateway_health` / `mcos_gateway_tools` | Gateway state |
| `mcos_pools_list` / `mcos_pool_get` / `mcos_pool_leases` / `mcos_pool_saturation` | Pool state |
| `mcos_telemetry_events` / `mcos_telemetry_clients` / `mcos_telemetry_gateway` | Telemetry |
| `mcos_discovery` | What MCOS advertises on the LAN |
| `mcos_onboarding` (with optional clientType) | Onboarding profiles |
| `mcos_governance_bundle` (per platform) | Forsetti bundle |
| `mcos_governance_approvals` | Pending CLU actions |
| `mcos_clients_list` | ADR-001 operator-surface LanClients |
| `mcos_config_get` | Live `mcos.json` |
| `mcos_activity` | Legacy admin activity ring |
| `mcos_forsetti_modules` | Registered Forsetti modules |
| `mcos_service_status` | Local: `Get-Service MasterControlOrchestrationServer` |
| `mcos_logs_tail` | Local: tail `events.jsonl` |
| `mcos_firewall_check` | Local: `Get-NetFirewallRule -DisplayName 'MCOS *'` |
| `mcos_dns_sd_check` | Local: `Resolve-DnsName _mcos._tcp.local` |

## Write tools (with confirm guards where needed)

| Tool | Confirm required? | Notes |
|---|---|---|
| `mcos_config_update` | No | But state the diff first |
| `mcos_telemetry_heartbeat` | No | Test heartbeat ingest |
| `mcos_pool_upsert` | No | Upsert is reversible |
| `mcos_pool_scale` | No | Adds instances; non-destructive |
| `mcos_pool_drain` | **Yes** | Existing leases keep routing; new ones go elsewhere |
| `mcos_pool_remove` | **Yes** | Reaps running instances; not graceful |
| `mcos_lease_acquire` / `mcos_lease_release` | No | Testing only — gateway acquires for real traffic |
| `mcos_gateway_start` | No | |
| `mcos_gateway_stop` | **Yes** | Reaps gateway child tree |
| `mcos_governance_approve` | No | Operator already gave the green light to call this |
| `mcos_governance_reject` | **Yes** | Reason required |
| `mcos_client_register` / `mcos_client_privileges` / `mcos_client_enable` | No | |
| `mcos_client_disable` | **Yes** | |
| `mcos_forsetti_module_enable` | No | |
| `mcos_forsetti_module_disable` | **Yes** | |

## Failure handling

Every tool returns `{ok: bool, ...}`. Standard failure shape:

```
{
  "ok": false,
  "error": "Network error: Connection refused",
  "errorCode": "NETWORK",
  "status": null,
  "url": "http://localhost:7300/api/health",
  "hint": "Cannot reach MCOS at http://localhost:7300. Check that the service is running ..."
}
```

Common error codes:

| Code | Cause | What to do |
|---|---|---|
| `NETWORK` | MCOS unreachable | Check `mcos_service_status`. If service is stopped, recommend `Start-Service`. |
| `HTTP_STATUS` | Server returned 4xx/5xx | Surface the body; cross-reference with [Troubleshooting](https://github.com/flynn33/Master-Control-Orchestration-Server/wiki/Troubleshooting). |
| `CONFIRM_REQUIRED` | Destructive op without `confirm:true` | State the intent, get operator confirmation, retry with `confirm:true`. |
| `UNKNOWN_TOOL` | Typo in tool name | Use `tools/list` to get the canonical name. |
| `BAD_REQUEST` | Required arg missing | Re-call with the missing arg. |
| `PLATFORM` | Local-diagnostic tool called on non-Windows | Skip; rely on HTTP-based tools. |
| `TIMEOUT` | Local PowerShell command timed out | Retry with smaller scope or longer timeout. |

## Where to read more

- [Daily Operations](https://github.com/flynn33/Master-Control-Orchestration-Server/wiki/Daily-Operations) — comprehensive runbook for live-system tasks
- [Configuration](https://github.com/flynn33/Master-Control-Orchestration-Server/wiki/Configuration) — every `mcos.json` field
- [Troubleshooting](https://github.com/flynn33/Master-Control-Orchestration-Server/wiki/Troubleshooting) — symptom-first diagnosis
- [Architecture](https://github.com/flynn33/Master-Control-Orchestration-Server/wiki/Architecture) — runtime composition, the eleven required terms
- [ADR-002](https://github.com/flynn33/Master-Control-Orchestration-Server/wiki/ADR-002-gateway-first-mcp-realignment) — the governing decision
