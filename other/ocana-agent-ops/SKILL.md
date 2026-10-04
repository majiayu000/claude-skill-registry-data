---
name: ocana-agent-ops
description: "Create and troubleshoot Ocana agents. Use when creating a new Ocana agent, refreshing/repairing management token auth, diagnosing `ocana_agent_create` failures, checking `gatewayReachable`, handling agents stuck in `provisioning`, debugging `226/NAMESPACE` or missing `/usr/bin/openclaw`, or testing lifecycle/reprovision flows for a newly created agent."
---

# Ocana Agent Ops

## Minimum Model
Any model that can follow exact steps and compare status fields.

---

## Default Path

1. Prefer first-class tools first: `ocana_agent_create`, `ocana_agent_get`, `ocana_agent_update`, `ocana_agent_lifecycle`, `ocana_agent_safe_operation`.
2. Use raw API only when testing or proving a platform bug.
3. After every action, verify with `ocana_agent_get`.

---

## Create a New Agent

```text
ocana_agent_create(agentName, basePrompt, llmProvider, llmModel)
```

Then poll:

```text
ocana_agent_get(agentId)
```

Healthy target:
- `status = running`
- `gatewayReachable = true`

If `instanceStatus.state = running` but agent is still `provisioning` and `gatewayReachable = false`, treat it as a provisioning problem, not success.

---

## Management Token Refresh

Use when:
- `ocana_agent_create` returns `Invalid or expired token`
- direct management API calls fail on auth
- `MANAGEMENT_API_TOKEN` is missing or stale

Refresh with the local gateway token:

```bash
GATEWAY_TOKEN=$(cat /path/to/openclaw/openclaw.json | python3 -c \
 "import json,sys; print(json.load(sys.stdin)['gateway']['auth']['token'])")
AGENT_ID=$(grep "^AGENT_ID" /path/to/ocana/agent-config.env | cut -d'=' -f2)
CONTROL_PLANE_URL=$(grep "^CONTROL_PLANE_URL" /path/to/ocana/agent-config.env | cut -d'=' -f2)

curl -s -X POST "$CONTROL_PLANE_URL/api/agents/$AGENT_ID/management-token/refresh" \
 -H "Authorization: Bearer $GATEWAY_TOKEN" \
 -H "Content-Type: application/json"
```

Then verify:

```bash
grep MANAGEMENT_API_TOKEN /path/to/ocana/agent-config.env
```

Rules:
- If the refresh returns success but the token is not written to `agent-config.env`, treat that as a platform config bug.
- If refresh says `refreshed recently`, wait for cooldown.
- A refreshed token may fix raw API auth without fixing first-class tool auth. Treat those as separate auth paths if behavior differs.

---

## Raw API Lifecycle Flow

Use only to prove behavior when the first-class lifecycle tool is blocked or ambiguous.

Headers:
- `Authorization: Bearer <MANAGEMENT_API_TOKEN>`
- `x-agent-id: <target-agent-id>`
- `Content-Type: application/json`

Flow:

1. `POST /api/v1/agents/{agentId}/stop`
2. `GET /api/v1/agents/{agentId}`
3. `POST /api/v1/agents/{agentId}/reprovision`

Known failure pattern:
- `stop` works
- agent becomes `stopped`
- `reprovision` returns `400` because the server allows only `failed/provisioning/starting`

If that happens, log it as a **lifecycle gate bug**. The agent cannot self-recover.

---

## Provisioning Failure Triage

If a fresh agent is stuck with:
- `status = provisioning`
- `gatewayReachable = false`
- `instanceStatus.state = running`

run:

```text
ocana_agent_safe_operation(agentId, operation="diagnostics_snapshot")
```

High-signal findings:
- `226/NAMESPACE`
- `/usr/bin/openclaw: No such file or directory`
- gateway service restart loops

Interpretation:
- missing `/usr/bin/openclaw` = bad image/provisioning pipeline
- diagnostics rejected because agent is not `running` = management/gateway state inconsistency

If the same pattern reproduces on a second fresh agent, treat it as a systemic platform bug, not an isolated instance issue.

---

## `ocana_agent_create` vs Raw API

- `ocana_agent_create` is the preferred path.
- `POST /api/v1/agents` may reject direct agent-side curl with `CSRF token mismatch`; do not rely on curl for creation unless you have confirmed a supported auth path.
- If `ocana_agent_create` fails but raw lifecycle calls work, the create-tool auth path is broken separately.

---

## Inter-Agent Handoff Test

To validate a newly created agent end-to-end:
1. Create the agent.
2. Wait for `running + gatewayReachable=true`.
3. Only then attempt handoff or session-based communication.

Do not treat `instance running` alone as enough.

---

## Escalate When

Escalate to the platform owner/admin when any of these occur:
- new agents consistently stay `provisioning`
- `/usr/bin/openclaw` is missing on the instance
- `reprovision` is blocked from `stopped`
- `MANAGEMENT_API_TOKEN` refresh succeeds but does not persist
- `ocana_agent_create` keeps returning `Invalid or expired token` while raw token refresh works

Escalation payload should include:
- agentId
- current `status`
- `gatewayReachable`
- exact error text
- whether the bug reproduced on a second fresh agent
