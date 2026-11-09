---
name: unity-integrate-netcode
description: Integrate explicitly selected Netcode for GameObjects with server authority, lifecycle-safe replication, and failure testing.
engines: [UNITY]
---

# Unity Integrate Netcode

## When to use

Integrate explicitly selected Netcode for GameObjects with server authority, lifecycle-safe replication, and failure testing. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-integrate-netcode` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Require an explicit Netcode for GameObjects selection and compatible package/Editor versions, selected transport, session topology, target platforms, authority model and bandwidth/latency budgets. Do not substitute Netcode for Entities or a hosted service.

## Workflow

1. Map NetworkManager startup, approval, shutdown and reconnect lifetimes. Separate session discovery/authentication from replication; transport configuration and any relay or lobby service remain explicit dependencies. Selected MPS Sessions/matchmaking/Relay orchestration belongs to `unity-integrate-multiplayer-services`; neither successful service membership nor session ownership establishes simulation authority.
2. Define NetworkObject spawn/despawn and ownership policy, registered network prefabs and server-side validation. Use NetworkBehaviour spawn/despawn callbacks for network lifetime rather than assuming MonoBehaviour Start means replication is ready.
3. Choose replicated state and RPCs by durability. Use NetworkVariable or the package-supported equivalent for persistent shared state; use version-supported RPC syntax for requests/events, with sender, ownership, bounds and rate validation.
4. Keep authoritative simulation on the chosen server/owner and presentation interpolation separate. State authority, prediction and reconciliation are design decisions; do not label client anticipation as complete rollback prediction.
5. Implement late join snapshots, scene synchronization, respawn and disconnect cleanup. Stable domain IDs and save schemas must not rely solely on transient network object IDs.
6. Keep serialization bounded and version-aware. Validate sizes, optional fields and content identifiers before applying remote data; unknown or malicious messages must not create assets, execute code or bypass gameplay rules.
7. Reconcile audiovisual and haptic event identities across prediction, retransmission and correction. Prevent duplicate local feedback without suppressing the actual authoritative result.

Read [replication and service handoffs](references/replication-handoffs.md) when integrating session, transport and scene readiness.

## Verification

- Run separate server/host and at least two clients; test ownership violations, invalid requests, late join, scene transitions and despawn during pending callbacks.
- Exercise latency, loss, jitter, reconnect and transport failure using the selected project's test facilities; record packet and bandwidth measurements.
- Distinguish local simulated transports from deployed target-platform tests. No service account, relay spend or public endpoint is authorized implicitly.

## Output

Network ownership/replication map, package-bound components and serialization contracts, lifecycle and abuse tests, multi-process evidence and network budgets. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Fail clearly if NGO or its selected transport is unavailable. Installing packages, adopting online services or accepting service terms requires a separate explicit decision. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Netcode for GameObjects](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.7/manual/index.html). Use the documentation matching the installed project version.
- [Unity Transport](https://docs.unity3d.com/Packages/com.unity.transport@2.4/manual/index.html). Use the documentation matching the installed project version.

