---
name: distributed-system-audit
description: Audit distributed systems where the highest-impact findings live between the components, not inside any one of them. Covers architecture mapping, trust boundary enumeration, per-channel protocol review (replay, ordering, forgery), STRIDE-lite threat modeling, failure-mode analysis, and forensic accountability. Invoke when auditing client / server, microservices, IoT backends, or agent-platform architectures.
---

# Distributed System Audit

A separate skill from [`codebase-audit`](../codebase-audit/SKILL.md). That one walks the code in one repo; this one walks the **system**: many processes, many trust boundaries, protocols between them, and the failure modes that don't exist when everything runs in one process.

The biggest mistake auditors make on distributed systems is treating them as N independent code audits. The interesting findings live *between* the components, in the assumptions they make about each other.

## When to invoke

- Auditing a client/server product (native agents + control plane)
- Auditing a microservices or service-mesh setup
- Auditing an IoT or fleet-management backend
- Auditing a multi-tenant SaaS with worker / job-runner architecture
- Acquisition due-diligence on a distributed product
- Handing over operations of a multi-component system
- After an incident that crossed component boundaries

Pairs with [`codebase-audit`](../codebase-audit/SKILL.md) for the per-component code-level work, [`kubernetes-security`](../kubernetes-security/SKILL.md) if the control plane is K8s, [`message-bus-security`](../message-bus-security/SKILL.md) for the messaging layer, [`agent-client-security`](../agent-client-security/SKILL.md) for the client-side.

## Step 0 — Map first, judge later

The first deliverable of a distributed-system audit is **an architecture diagram you produced**, not the findings. Until you can draw every component and every channel between them, you don't understand the system well enough to audit it.

Spend the first 30% of the engagement on the map. It pays off triple.

```
                                ┌────────────────────┐
                                │  Web Admin UI      │
                                └─────────┬──────────┘
                                          │ HTTPS + session cookie
                                ┌─────────▼──────────┐
              ┌─────────────────│  Control Plane API ├───────────────────┐
              │                 └─────────┬──────────┘                   │
              │                           │                              │
        write events                      │ writes                       │ writes
              │                           ▼                              ▼
        ┌─────▼─────┐              ┌────────────┐              ┌────────────────┐
        │ Audit log │              │ Postgres   │              │ Object storage │
        └───────────┘              │ (tenancy)  │              │ (user uploads) │
                                   └─────┬──────┘              └────────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  Message bus (NATS) │
                              └──────────┬──────────┘
                                  publishes commands
                                         │
                            ┌────────────┼────────────┐
                            ▼            ▼            ▼
                     ┌────────────┐  Agent_1   Agent_2  ...
                     │ Agent_n    │  (host A)  (host B)
                     │ (host Z)   │  customer machines
                     └────────────┘
```

For each arrow, you need to know: protocol, auth, encryption, who-trusts-whom, replay protection, ordering guarantees.

## Step 1 — Inventory every component and every channel

For each component, capture:

- Name and role
- Runs where (cloud account, region, customer device)
- Process identity (how it authenticates)
- What persistent state it owns
- What other components it calls
- What other components call it

For each channel:

- Protocol (HTTPS, gRPC, NATS, MQTT, raw TCP, ...)
- Authentication (mTLS, JWT, API key, none)
- Encryption (TLS, end-to-end, none)
- Direction (one-way, request/response, pub/sub)
- Replay protection (nonce, sequence, timestamp + window)
- Ordering guarantee (FIFO per session? exactly-once? at-least-once?)
- Backpressure or rate-limit

The matrix often surfaces the first findings: a channel with no auth, a channel with auth but no replay protection, two channels that share a credential, etc.

## Step 2 — Trust boundaries

Draw the trust boundaries on the diagram. A trust boundary is where data crosses from a context with one trust level to a context with another. Common boundaries:

- Internet ↔ control plane (public internet → your API)
- Control plane ↔ customer machines (your infra → agent on customer's box)
- Tenant A ↔ Tenant B (multi-tenant isolation)
- Privileged operations ↔ regular ops (admin actions vs user actions)
- Build/CI ↔ production (artifact promotion)
- Internal team ↔ contractor team (access scoping)

For each boundary, ask:

- What authenticates the crossing?
- What input validation happens at the boundary?
- What guarantees does the receiver assume about the sender?
- What happens if those assumptions are wrong?

A trust-boundary failure typically produces the highest-severity findings in a distributed audit.

## Step 3 — Threat-modeling-lite (STRIDE)

For each component and each channel, walk STRIDE:

| Letter | Threat | Distributed-system flavor |
|---|---|---|
| **S** Spoofing | Pretending to be a different identity | A rogue agent impersonating a legitimate one |
| **T** Tampering | Modifying data in transit or at rest | A man-in-the-middle on the agent ↔ control-plane channel |
| **R** Repudiation | Denying an action you took | An agent that did something but the log shows nothing |
| **I** Information disclosure | Leaking data | Telemetry containing customer data sent to all agents |
| **D** Denial of service | Making the system unavailable | One rogue agent flooding the bus |
| **E** Elevation of privilege | Acting beyond your authority | A worker agent accepting commands from another agent rather than the control plane |

Full STRIDE per channel is a long exercise. For a small-team audit, a 30-minute pass per major component identifies the high-risk threats. Document them; the rest of the audit then targets them.

## Step 4 — Protocol audit

For every channel, three classes of issue to chase:

### Replay

Can a captured message be re-sent later and be accepted as new?

- Is there a nonce, sequence number, or timestamp?
- If timestamp, is there a tolerance window? How wide?
- Is the validation actually done at the receiver, or only at the sender?
- Does the receiver remember recent nonces (within the tolerance window)?

Replay protection is the single most-skipped distributed-system control. Search for "we use HMAC so the message is signed" — signature without freshness is replay-vulnerable.

### Ordering

Can messages arrive out of order, and does that break the receiver?

- Pub/sub buses (NATS without JetStream, MQTT QoS 0) do not guarantee ordering
- Even with ordering, a multi-partition Kafka topic does not order across partitions
- TCP guarantees ordering within a connection, not across reconnects

Findings here look like: "agent receives commands A then B; B depends on A; if reconnect happens between them, agent sees B first and acts on stale state."

### Forgery / authentication

Can a participant inject messages that look like they come from another participant?

- Is each message authenticated, or only the channel establishment?
- If shared symmetric keys, can any participant forge as any other?
- Is the broker / bus enforcing publish permissions per subject/topic?
- See [`message-bus-security`](../message-bus-security/SKILL.md) for bus-specific concerns

## Step 5 — Time-related findings

Distributed systems live in distributed time. Common findings:

- **Clock skew** — agent clocks drift from control plane; signed-token tolerance windows fail or open replay windows wider than intended
- **Token expiry assumptions** — control plane assumes token validity, agent clock is wrong, token is "valid" for hours longer than designed
- **Time-of-check / time-of-use across components** — control plane checks user is authorized, then sends command to agent; user is de-authorized; agent still executes
- **Leader-election timing** — split-brain when network partitions cause two nodes to think they're leader
- **Retry storms** — a transient failure causes a retry, which causes load, which causes more transient failures, which causes more retries

For each, the audit asks: is there an explicit handling? What's the tolerance?

## Step 6 — Failure-mode audit

A distributed system has failure modes a monolith doesn't. Walk:

- **One agent crashes mid-task** — does the work resume? Was something half-done left in a bad state?
- **Network partition (agent ↔ control plane)** — does the agent keep operating with stale state? For how long? With what authority?
- **Control plane is down** — what do agents do? Refuse work? Continue with last instruction? Drift?
- **One service depends on another that's down** — graceful degradation or cascading failure?
- **Message bus is down** — fall back to direct connection? Buffer? Drop?
- **Storage is down** — read-only mode? Refuse writes? Lose writes?

Each unhandled mode is a finding. "It's never happened" is not a defense — it will eventually.

## Step 7 — Forensic accountability

When something bad happens, can you tell what happened?

- Does every state-changing action produce an audit-log entry?
- Does the audit log record the **identity** of the actor (which agent, which user, which service account)?
- Does the audit log record **before** and **after** state for sensitive changes?
- Is the audit log itself tamper-resistant (append-only, separate store, hash chain)?
- Can you correlate a customer complaint timestamp to specific log entries across all components?

Common audit findings:

- Per-component logs exist but are not correlated (no request_id threading across services)
- Audit log lives next to the production database (compromise wipes both)
- Audit log captures the action but not the actor (everything attributed to "service")
- No log of agent activity — only control-plane log — so agent-side issues are invisible

See [`log-strategy`](../log-strategy/SKILL.md) for the broader pattern.

## Step 8 — Multi-tenant isolation

If multiple tenants share the system:

- Can tenant A's commands ever reach tenant B's agents?
- Is the message bus subject scheme enforced (per-tenant subjects, not just by convention)?
- Are database queries always tenant-scoped (RLS or per-query filter)?
- Are object storage paths tenant-prefixed and access-controlled?
- Are agents tenant-scoped (one agent serves only one tenant), or can they serve multiple?
- What's the failure mode if a tenant's credential is compromised — does it expose other tenants?

For high-stakes multi-tenancy (regulated data, large customers), the audit recommendation is often "harden current setup *and* plan a per-tenant isolation level."

## Step 9 — Common findings classes specific to distributed systems

Catalog of typical findings in real audits:

- **Shared secret used across instances** — one credential leak compromises every node
- **Agent → control-plane authentication is one-way** — agent verifies the control plane, but control plane accepts any agent claiming a valid token (no agent-side identity proof)
- **Heartbeat is unauthenticated** — anyone on the network can heartbeat as any agent, causing collisions or denial-of-service
- **Commands carry parameters but no version pin** — agent runs an old version, gets a command with newer-schema parameters, misinterprets
- **Message bus subjects are broad-wildcard** — `agent.>` subscribers receive other tenants' messages
- **No idempotency on commands** — replay or duplicate delivery causes double-execution
- **Logs ship through the same channel as commands** — log volume can starve command throughput
- **Update channel is HTTP without signing** — an attacker on the network swaps the update binary
- **Control plane is the single point of trust for everything** — its compromise compromises every agent

Each maps to a specific check during the audit.

## Step 10 — Producing the report

Same general shape as [`codebase-audit`](../codebase-audit/SKILL.md):

- Group by severity, then by component / boundary
- Per finding: summary, evidence, impact, remediation, severity reasoning, suggested owner, deadline
- Architecture diagram appended as the orientation aid
- Trust-boundary table appended as the audit map
- Threat-model summary appended

Critical findings are communicated to the client the same day they're discovered — see [`incident-response`](../incident-response/SKILL.md).

## Checklist — am I done with the system-level audit?

- [ ] Architecture diagram drawn and confirmed with the team
- [ ] Component inventory complete (name, role, location, identity, state, callers, callees)
- [ ] Channel inventory complete (protocol, auth, encryption, replay, ordering)
- [ ] Trust boundaries marked on the diagram
- [ ] STRIDE pass on the high-risk components and channels
- [ ] Protocol audit done per channel (replay, ordering, forgery)
- [ ] Time-related issues walked
- [ ] Failure-mode audit walked
- [ ] Forensic accountability assessed (per state-changing operation)
- [ ] Multi-tenancy isolation walked (if applicable)
- [ ] Findings reproduced where possible
- [ ] Report grouped, prioritized, with remediation

## What this skill will not do

- Help audit a system you do not have written authorization for
- Replace a full red-team engagement for adversarial testing
- Provide attack tooling — findings describe issues and fixes, not exploit scripts
