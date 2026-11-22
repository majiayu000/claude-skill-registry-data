---
name: ha
description: High Availability control plane for Yuzu — the canonical entry point for any work on ADR-2002 (active-active server tier, gateway-fronted routing, Postgres-backed coordination seam, HA Postgres storage). Use when the user says "/ha", "/high-availability", "/ha-matrix", asks to plan or implement an HA workstream (WS-0…WS-14), asks "what's our HA gap" or "is it safe to run a second replica yet", asks to audit HA readiness, or starts work touching the coordination seam (leader election / fenced epochs / transactional outbox), gateway intra-cluster routing, shared `AgentRegistry` presence, PKI/CA HA, or the `deploy/docker/*ha*` / `scripts/ha/` surface. The skill bundles the two-axis model, the safe-to-scale gate, the delivery matrix (current-state + reviewers + status), the per-workstream workflow, and the load order for the routed reference docs.
---

# High Availability skill

The single entry point for any HA work in Yuzu. Bundles three things:

1. **The model** — the two independent axes and the safe-to-scale gate (get
   this wrong and a second replica double-dispatches destructive commands).
2. **The delivery matrix** — every workstream WS-0…WS-15: what it delivers,
   current state, dependencies, whether it gates a second replica, routed
   reviewers, and status.
3. **Gap/priority + workflow** — what to build next and the standard
   procedure for landing a workstream slice.

This skill does NOT replace ADR-2002 or the routed docs. It tells you which
to load, in which order, and what to confirm before you start cutting code.
**On any conflict, ADR-2002 governs the model and
`docs/ha-delivery-matrix.md` governs delivery** — this file is a pointer and
loses to both.

---

## Usage

```
/ha                       # default: print the matrix + the safe-to-scale gate, ask which WS to work on
/ha audit                 # snapshot of HA readiness — which WS are done, whether a 2nd replica is safe yet
/ha plan <WS>             # plan-only walk-through for a single workstream (e.g. WS-3, WS-7)
/ha implement <WS>        # full workflow: plan → governance → implement → test → docs for one WS slice
```

If invoked without a subcommand, default to printing **the matrix (Section 2)
+ the safe-to-scale gate (Section 1)** and asking which workstream to work on.

---

## 1. The model — read before sequencing anything

Authoritative reference: `docs/adr/2002-high-availability-architecture.md`
(the decisions) and `docs/ha-delivery-matrix.md` (the delivery spine). Read
them before this skill claims anything is "done."

### 1a. Two independent axes

- **Server-tier HA** — N presentation + core replicas (WS-0…WS-6, WS-8,
  WS-10, WS-11, WS-13, WS-15).
- **Storage HA** — HA Postgres (WS-7). **A single Postgres is a valid,
  supported deployment; server-tier HA does not require it.**

"HA" as a *customer claim* = **both** axes + WS-9 (validation) + WS-11/WS-12
(operability). Do not conflate the axes: WS-7 shipping does not make the
server tier highly available, and a second replica is safe against a single
Postgres.

### 1b. ⚠️ The safe-to-scale gate (the load-bearing constraint)

**Do not equate "Phase A done" with "safe to run a second replica."** The
three-model adversarial review's strongest, unanimous finding:

> **A second server replica may be enabled only when WS-0, WS-1, WS-2(2a
> outbox), WS-3, WS-4, WS-5, WS-6, WS-10 are done, WS-8's per-tier
> `/readyz` exists, the WS-11 leader-observability subset (#4014:
> leader/epoch metrics and the split-brain alert; **shipped**) ships, AND, for
> gateway-fronted fleets, WS-13 is done.** (The last two clauses were added
> 2026-10-13; the rest of WS-11 does not gate. Shipping #4014 satisfies only
> that one clause: **the gate is NOT lifted**, and a durable cluster-capability
> admission gate, #6528, is separately unbuilt, and the epoch fence is not
> monotonic across a lossy asynchronous Postgres promotion, #6535, which must be
> closed or explicitly accepted by the owner before the gate is lifted.)

Miss any one and the failure is **not cosmetic**:
- No **WS-3** (fenced leader) → both replicas run the singleton workers →
  **double-dispatch of destructive commands** (software-deployment,
  quarantine, policy-remediation).
- No **WS-4/WS-5** → commands can't reach agents / scope evaluation drops
  agents on the replica lacking the local stream → **mis-targeting**.
- No **WS-6** → CRL numbering / enrollment **diverge** across replicas.

**WS-7 (HA Postgres) is NOT in this gate set** — it gates the storage axis
(no SPOF / RPO=0), not the second server replica. The "Gates 2nd replica?"
column in the matrix encodes this per row.

### 1c. Split ↔ HA — RATIFIED: decoupled (the split is NOT a prerequisite)

**Is the presentation/core split (ADR-0031) a prerequisite for active-active?
No — decoupled. Ratified by the ADR-1005 owner (Dave Rae), 2026-09-07.** Monolith
active-active is the target; the split is a parallel programme, not a gate for a
2nd replica. The one in-process blocker (direct agent `Subscribe` stream) is solved
by **gateway-fronting (WS-4)**, not the split.
- **Kimi's dissent (recorded, rebutted):** Kimi called the split a hard safety
  prerequisite. Every safety property it could mean — singleton double-dispatch
  (WS-3), in-memory sessions (WS-1a, **done**), stream routing (WS-4) — is closed in
  the monolith. What the split buys is presentation scale-out + separate readiness
  signals: **capacity, not safety.**
- **One-way dependency:** the split *consumes* HA (inherits WS-1 sessions, rides
  WS-2a's durable `event_outbox` for its event spine, takes MCP replay durability from
  WS-2b) — never the reverse. WS-2b spine and WS-8 tier-split `/readyz` are no-ops on
  the monolith and land with the split. Delivery lives in its own control plane:
  `docs/presentation-core-split-delivery-matrix.md` (the `/split` skill).

### 1d. Non-obvious model decisions (survived two+ adversarial reviews)

- **Coordination = a narrow seam, Postgres-backed by default** — fenced
  advisory-lock leader + LISTEN/NOTIFY-as-hint over a durable outbox +
  reconnect cursor-poll; pluggable for SaaS; ship one impl. No new SPOF
  (Postgres already bounds availability, ADR-0007 fail-closed).
- **Effectively-once, NOT exactly-once** — transactional outbox +
  claim-before-side-effect + receiver-side idempotency (agent/gateway dedup on
  `command_id`). A dup must **replay the terminal outcome**, never return a
  bare `REJECTED` (that is the "effect-once, result-maybe-lost" bug WS-0 closes).
- **Intra-cluster gateway routing is net-new work** — OTP `pg` is
  broadcast-only; per-agent lookup is node-local ETS. "pg finds the exact
  node" is false; per-agent distributed routing must be built (WS-4).
- **The routing directory must be fenced** — (agent_id, connection_epoch,
  cluster_id, session_id, lease_until) with CAS register/deregister, else a
  stale replay overwrites a newer re-home.
- **Sessions → durable Postgres (DB wall-clock)** reverses the as-built
  in-memory-monotonic design and owns the regression risk on JIT-elevation /
  MFA windows.
- **Durability is selectable; default 3-node quorum** (1 primary + 2 sync
  standbys, ANY 1) on **distinct failure domains** — unconditional 2-node
  RPO=0 was a footgun (single standby loss stalls all writes).
- **Model:** hybrid, general product capability (on-prem-first + SaaS-later),
  NOT one customer. **Gateway-fronting is mandatory in HA** (direct-connect
  kept for single-node). Don't assume HA Postgres.

---

## 2. The delivery matrix — current state, reviewers, status

Source of truth: `docs/ha-delivery-matrix.md`. Read it before this skill
claims a status. WS-0…WS-10 come from ADR-2002 §Decomposition; WS-11…WS-14 are
delivery/ops workstreams the three-model review surfaced as missing; WS-15 (gateway
failback/rebalance, roadmap 7.1.1, #5759) was added 2026-10-13 as WS-13's pair.

**WS-3 / WS-11 re-stamped 2026-10-28 (#4014, PR #6542 merged):** ONLY those two rows were re-audited (against `origin/dev`
`377cc7700` and `gh`); no other row was. The WS-11 leader-observability subset shipped (metrics published at
scrape time from a lock-free `LeaderElector::Stats`, the `yuzu-ha-leader` alerts; leadership and the elector
being open stay out of `/readyz`). Follow-ups: #6526 (remediation-claim lifecycle counters), #6527 (CRL
freshness gauge), #6528 (durable cluster-capability admission gate), #6535 (epoch fence not monotonic across a lossy async promotion; must close or be explicitly accepted before the gate lifts). The safe-to-scale gate is NOT lifted.

**WS-6 re-stamped 2026-09-23 (PR #4833):** slice 6.1 (cross-replica CRL publication, #4126) in
review; 6.1b / 6.2 / 6.3 planned; the operator decisions (shared CA key custody, not
`SecretCodec`; a one-time `.cfg` enrollment import) are recorded in ADR-2002 §8 "Update
(2026-09-23)".

**Verified 2026-09-21 (against `origin/dev`): DONE — WS-0 (#3662), WS-1 (1a+1b+1c),
WS-2a (2a-1 + 2a-2 #3924), WS-3 (3.1–3.4 — #4011/#4134/#4169/#4194), WS-4 4.1 +
4.2a + 4.2b Tasks A–D (#4245/#4299/#4344/#4355, merged) + `#4324` per-home
stream-generation fence (PR #4492, merge commit `c37306113`, 2026-09-17T22:05:58Z,
**MERGED**), WS-7 (#3627), WS-10 10.1/10.2. **4.3a DONE** (intra-cluster `pg`-group
agent→node lookup + the `fanout_terminal` cross-node fix + `remote_dispatched`
telemetry — code-complete, empirically verified, no longer inert since `#4555`
merged). **`#4555` MERGED** (2026-09-19, `495cf24c4`, PR #4604): gateway cluster
formation (`yuzu_gw_cluster_discovery` always-on redial loop, DNS-A-record +
static-override discovery, dynamic address-only node identity, cookie length
floor) implemented, Fable-adjudicated, empirically verified against a real OTP
`peer` — see `docs/ha-delivery-matrix.md`'s WS-4 row for the full mechanism.
**WS-4 4.4 DONE** (2026-09-20, ADR-2002 §7c): `gateway_node` convergence + the
`#4246` #6 replay-session writeback, closed after a Fable pre-implementation
review rejected the originally-proposed design and surfaced that
`ProxyRegister` was unconditionally wiping placement on every replay-adopted
registration (a live, single-replica bug, not just a multi-replica gap) — see
the blockquote below and ADR-2002 §7c for the full mechanism.
**WS-4 rest of 4.3 DONE** (2026-09-21, ADR-2002 §7d): cross-cluster gateway
fan-out — `AgentSession`/`GatewayPendingCmd` now carry `cluster_id` end-to-end
from the common `send_to`/`send_to_all` path (not just the 4.2b directory
fallback), a new eager `GatewayMgmtStubPool` dials the OWNING cluster per
command instead of the single legacy stub, `--gateway-cluster-addr` config,
a response-agent forgery guard (closes ONE forgery shape — a cluster answering
as a different agent — NOT a rogue gateway claiming an agent's own identity via
`ProxyRegister`, which needs no per-agent secret; **multi-cluster mode does NOT
yet provide trust-zone isolation between clusters for a given agent, tracked
as `#4669`, pr-rev-caught pre-merge**), and one small required Erlang fix
(`stream_responses/3` threads the real `command_id` so a gateway-side
"not connected on this cluster" error is no longer invisible). **Closes WS-4's
dial-selection half** — the durable re-drive-on-failure half of §7's design
remains open (`#4672`), and `#4669` above is a separate, not-yet-closed item
(non-blocking today: zero production multi-cluster deployments). The
remaining safe-to-scale gate items are WS-5, WS-6, WS-8-readyz. See the
blockquote below and ADR-2002 §7d for the full mechanism, including the 5
findings a pre-implementation Fable review caught before any code was written
(the original resolution rule would have broken every upgrade), and the
pr-rev (FortitudeEtc/Codex+Kimi) round that caught the response-forgery
overclaim plus two real code bugs (terminal-outcome double-counting; an
oversized `cluster_id` silently routing to the default cluster instead of
being rejected) before merge.
Next gate items: WS-5, WS-6, WS-8-readyz. Also open: `#4669`, `#4672`.**

**Re-verified 2026-09-24 (against `origin/dev` + `gh`):** `#4672` CLOSED; `#4669`
still OPEN (mitigation 1, agent↔cluster affinity, merged; mitigation 2, peer-identity
binding, open). **WS-5 slice 1 MERGED** (PR #4745, 2026-09-22) — decommission
cascade, plugin-capability visibility, fleet gauge and its WS-9 scenario remain.
**WS-6 6.1 MERGED** (PR #4833, 2026-09-23) — 6.1b / 6.2 / 6.3 and WS-9 scenario
#4832 remain. **WS-8 readyz DONE for the monolith** (this change): runtime
`pg_reachable` probe + `--shutdown-drain-seconds` drain grace + WS-9 scenarios
`scripts/ha/ha-readyz-scenarios.sh`; tier-split readyz lands with the ADR-1005
split; the BYO-LB doc (P2) is open and not in the gate.
**Remaining gate items: the rest of WS-5, the rest of WS-6, and WS-13 for
gateway-fronted fleets.**

**Re-verified 2026-09-29 (against `origin/dev` + `gh`; no PR number yet — commits
97e24ec6e..a81938ada on a feature branch): WS-6 slice 6.2 DONE** (enrollment tokens
+ pending-agent approvals → Postgres, closing ADR-2002 §8's "Enrollment tokens +
pending-agents → Postgres" bullet): `AuthDB` migration v2 (live `enrollment_tokens`/
`pending_agents` shape + `auth.import_meta`), `AuthManager`'s per-replica file mode
deleted outright (not deprecated), `consume_and_enroll` a single guarded-UPDATE
transaction (exactly-N winners across processes — proven by this slice's own WS-9
scenario, not just connections in one process), a one-time marker+fingerprint `.cfg`
importer (never resurrects an already-removed/denied/revoked row; a fingerprint
mismatch is refused, not merged; a genuine store error with the file present fails
boot closed). **WS-6's WS-9 scenario for 6.2 also DONE**:
`scripts/ha/ha-enrollment-concurrent-register.sh` — see the WS-9 row and
`docs/ha-delivery-matrix.md`'s WS-6 row for the full mechanism. **WS-6 is now
6.1 + 6.2 done; 6.1b (shared KEK custody/versioning polish) and 6.3 (node-admission
readyz proof) remain — see `docs/ha-delivery-matrix.md`.**
**Remaining gate items: the rest of WS-5, WS-6's 6.1b/6.3, and WS-13 for
gateway-fronted fleets.**

**Re-verified 2026-10-11 (against the `feat/ha-ws5-session-lookup` worktree branch; since MERGED as PR #5694, see the 2026-10-13 re-stamp below): WS-5 slice 2 (durable cross-replica gateway session resolution, closes `#4246` item #3, ADR-2002 §7f)** — `resolve_sessions` is store-authoritative via `GatewayRouteStore::lookup_by_sessions`; BatchHeartbeat / ProxyInventory / NotifyStreamStatus resolve on any replica; ambiguous `session_id` refused; BatchHeartbeat also LISTS store-only sessions (known to the directory, no local entry) so the gateway replays and the local registry rehydrates after a server-only restart. NotifyStreamStatus CONNECTED on a degraded directory read is accepted only for a session this replica holds locally, else refused (`connected_unverified`); on a successful read the local fallback applies only to an absent/tombstoned row or a lost-race id; DISCONNECTED and BatchHeartbeat are deliberately fail-soft. ProxyRegister adopt refuses an id another agent's committed row holds (`session_held_by_other_agent`; not a lock, the ambiguity refusal is the backstop). `hostname` is newly blank-preserved in presence (`os` since #5294). Unique partial index on `agent_routes(session_id)`, hp-1/hp-2 and the WS-9 script (PR-B) are NOT in it. **The safe-to-scale gate is NOT lifted** — remaining gate items are unchanged in kind (the rest of WS-5, WS-6's 6.1b/6.3, WS-13 for gateway-fronted fleets); see `docs/ha-delivery-matrix.md`.

**Re-verified 2026-10-13 (status re-stamp against `origin/dev` at `d81109688`, with `gh`; other rows NOT re-audited): WS-5 slice 2 MERGED** (PR #5694, merge `eabc2b639`); follow-ups merged 2026-10-12: PR #5736 (`d81109688`, closes #5682, `OfflineEndpointStore` is the cascade's seventh member) and PR #5743 (`0a4b60ac5`, closes #5684 and #5686). WS-9 is in-progress, not planned: `scripts/ha/` carries scenarios for WS-6 (CRL publication, enrollment), WS-7 and WS-8. The safe-to-scale gate is NOT lifted; remaining gate items are unchanged in kind (the rest of WS-5, WS-6's 6.1b/6.3, WS-13 for gateway-fronted fleets). See `docs/ha-delivery-matrix.md`.
>
> **WS-4 4.2a update (2026-09-13, PR #4299 round-5 review):** `#4246` item #4
> (same-session late-DISCONNECTED tombstoning a newer re-home) is **RE-SCOPED,
> not closed** by 4.2a. The tombstone closed only the late-CONNECTED
> resurrection direction (#5). #4's mechanism is real but has no producer under
> the shipped gateway (exactly one CONNECTED(S)/one DISCONNECTED(S) per session),
> so it is unreachable today; the per-home stream-generation fence (a
> `NotifyStreamStatus` protocol change) is a precondition (#4324) of the first slice that
> re-CONNECTs under a reused session id. Invariant: `session_id` ≡ exactly one
> gateway stream placement.
>
> **WS-4 4.2b update (2026-09-14):** the dispatch-wiring task landed as Tasks
> C (reader, fallback-only) + D (`route_unreadable` consumer + alert rules) —
> see `docs/ha-delivery-matrix.md`'s WS-4 row and ADR-2002 §7's 4.2b status
> paragraph for the full narrative. 4.2b's review RE-VERIFIED the
> once-per-session property (`#4324`) before Task C landed
> (`governance.d/ha-ws4-42b-4324-reverification.md`) — the property held, no
> regression found; the per-home fence itself remained deferred at that point
> to the first slice that re-CONNECTs under a reused session id
> (4.3/4.4/`#4246` #6).
>
> **WS-4 `#4324` update (2026-09-17, MERGED — PR #4492, `c37306113`):** the
> per-home stream-generation fence is **CLOSED end-to-end** — task 1
> (`46f1e72b6`, `StreamStatusNotification.stream_home_id` wire field + Erlang
> producer), task 2 (`4b248b504`, `GatewayRouteStore`'s nullable
> `stream_home_id` column + asymmetric tombstone predicate, migration v3),
> task 3 (`feabccea7`, `NotifyStreamStatus`'s DISCONNECTED branch resolving
> the fence once, before any teardown effect, against
> `AgentRegistry::gateway_stream_home_id`). Re-verified the once-per-session
> property a second time before landing
> (`governance.d/ha-ws4-4324-stream-fence-reverification.md`) — no regression.
> **Pre-merge PR-review fix (HIGH):** external reviewer FortitudeEtc
> (Codex+Kimi, empirical reproduction) found task 2's original predicate —
> `stream_home_id = $3 OR (stream_home_id IS NULL AND $3 = '')` — wrongly
> required the incoming value to also be empty before a stored-NULL row
> admitted it; a stored-NULL home can also mean "this session's own
> `announce_connected` hasn't run yet" (CONNECTED/DISCONNECTED are two
> independently `spawn_monitor`'d RPCs with no ordering guarantee), so an
> ORDINARY (non-re-home) connect/disconnect could have its DISCONNECTED
> arrive first, get misclassified `stale_home`, and let a delayed CONNECTED
> publish a route for an already-dead stream — reachable with only the FIRST
> CONNECTED/DISCONNECTED pair, no second one needed. Fixed to
> `stream_home_id IS NULL OR stream_home_id = $3` (`f7f12bd59`, mirrored in
> the in-memory fence); a Gate 8 re-review caught a second stale copy of the
> old formula in a doc comment (`5160e0eeb`). Both landed pre-merge in the
> same PR. Deliberately NOT closed: the pre-CONNECT-race ordering gap (a
> stale DISCONNECTED landing before its matching live CONNECTED still
> tombstones the row — see `gateway_route_store.hpp`'s FORWARD NOTE), left
> for 4.3; and the `duplicate_connected` desync tripwire, deferred to its own
> follow-up, `#4464`.
>
> **WS-4 4.3a update (2026-09-18):** the intra-cluster half of 4.3 (agent→node
> routing WITHIN one Erlang gateway cluster, distinct from cross-cluster
> fan-out) is **DONE** — `yuzu_gw_registry.erl`'s `lookup/1` gains a per-agent
> `pg` group (`{agent, AgentId}`) cross-node fallback on a local ETS miss;
> `yuzu_gw_agent.erl` fixes a latent bug the design review found
> (`fanout_terminal` was routed to the LOCAL node's router, stranding a
> cross-node fanout for the full 300s timeout — now routed to
> `{yuzu_gw_router, node(ReplyTo)}`); `yuzu_gw_router.erl` adds
> `remote_dispatched` telemetry. Design per ADR-2002 §7's own mechanism list
> (a per-agent `pg` group), NOT the dead `hash_ring_vnodes` config
> (`#4556`) or a server-supplied hint (both rejected by design review).
> Verified: `rebar3 compile`/`dialyzer` clean, full eunit suite green, a new
> OTP-`peer`-based 2-node test suite (4 tests) run 40+ times with zero
> flakes after two governance-round fixes (a false-green local-preference
> test, and a `pg`-propagation-delay race in the fanout-completion test).
> Also updates `gateway_route_store.hpp`'s `#4324` FORWARD NOTE: the
> pre-CONNECT-race ordering gap left open above is now resolved as
> unreachable BY INVARIANT (agent-driven reconnect + the gateway's
> `NOT_FOUND` refusal on an unknown session — no producer of a same-session
> different-home CONNECTED exists or is planned), replacing the
> previously-stated `register_fresh`-ordered-epoch/CAS resolution with a
> standing design constraint + a server-side tripwire folding into `#4464`.
> **COMPONENT-COMPLETE-AND-INERT** as of this note; **`#4555` (gateway
> cluster formation) MERGED 2026-09-19** (`495cf24c4`, PR #4604 — see the
> Verified line above), no longer inert. Remaining WS-4 work as of that
> merge: the rest of 4.3 (cross-cluster gateway fan-out — today one
> `gw_mgmt_stub_`), plus 4.4 (`gateway_node` convergence + replay-session
> writeback) — see the next blockquote for 4.4's closure.
>
> **WS-4 4.4 update (2026-09-20, `#4246` #6, ADR-2002 §7c): DONE.** A Fable
> pre-implementation review REJECTED the originally-proposed two-mechanism
> design (a periodic directory-sourced read-repair — would publish a route
> with no `wire_capabilities`, which dispatch denies outright; a
> gateway-side adoption of a server-minted session — explicitly prohibited
> by `gateway_route_store.hpp`'s FORWARD NOTE, and unworkable regardless
> since agent heartbeats carry the AGENT's own session id, which the
> gateway cannot rewrite) and surfaced the actual dominant root cause: on
> EVERY replay-adopted `ProxyRegister` — even the ordinary same-replica
> case, no core restart needed — `register_agent` unconditionally installed
> a brand-new `AgentSession`, wiping `gateway_node`/`wire_capabilities`/
> `stream_home_id` regardless of whether the session was being adopted or
> freshly minted. Fixed: `ProxyRegister` now decides ADOPT-vs-REFUSE
> *before* calling `register_agent` — whenever `GatewayRouteStore` is
> configured, the STORE governs this decision (never the in-memory
> `gateway_sessions_` map on its own — a round-2 review fix, F1, closed a
> real bug where trusting memory alone let a tombstoned-but-still-`gateway_sessions_`-known
> session go unrepaired after a >270s gateway-uplink partition, and separately
> let a stale local session overwrite a genuinely-live one on a different
> node): ADOPT (response always carries the presented session, never a
> fresh mint) on a live directory row (`renew_leases`), or the new guarded
> CAS `GatewayRouteStore::reclaim_tombstoned_session` (re-arms a
> TOMBSTONED or absent row — epoch `0` on a brand-new row, untouched on a
> re-armed tombstone, either way no higher than `register_fresh`'s
> `nextval` can mint, so a genuine `register_fresh` still always wins);
> REFUSE (`FAILED_PRECONDITION`, nothing installed) when the row is LIVE
> under a DIFFERENT session. `gateway_sessions_` alone decides ONLY when no
> store is configured. Convergence comes from the GATEWAY: on ADOPT,
> `yuzu_gw_upstream.erl` tells the still-live `yuzu_gw_agent` process
> (`reannounce/2`) to re-send its OWN CONNECTED (same session, same home)
> through the ordinary `NotifyStreamStatus` path — now backed by drop
> telemetry and drip backpressure against the `MAX_NOTIFY_INFLIGHT` cap
> (F2); on REFUSE, it feeds its circuit breaker a SUCCESS (not a failure —
> the server answered authoritatively) and calls `disconnect/1` to force
> the agent-driven reconnect the FORWARD NOTE requires. Also fixed a latent,
> pre-existing crash in `do_rpc`'s error-clause pattern (never matched what
> `grpcbox_client:unary/5` (the upstream client at the time; replaced by
> `yuzu_grpc_client`, which keeps the same result shapes) actually returned; unreachable before 4.4 since
> this RPC never previously returned a real non-OK, non-transport grpc
> status). **Round-2 Fable review found 3 more real bugs before push**: F1
> (BLOCKING) — the adopt decision let an in-memory `gateway_sessions_` hit
> override the store, missing a >270s gateway-uplink-partition tombstone
> and a cross-node zombie-session overwrite; fixed by making the store
> govern unconditionally whenever configured, memory only when no store
> exists. F2 (BLOCKING) — the reannounce CONNECTED shared
> `?MAX_NOTIFY_INFLIGHT` with everything else and dropped silently at
> capacity (I6a); fixed with drop telemetry + drip backpressure. F3
> (BLOCKING) — `yuzu_gw_heartbeat_buffer.erl` had the SAME impossible
> `do_rpc`-shaped error clause; fixed identically. **A full `/governance`
> pass (round 3) then found 3 MORE blocking issues round 2 itself
> introduced or missed**: sec-H1 — round 2's reannounce fix converges
> placement only if its notify is actually delivered, and a dropped one left
> `cluster_id` permanently NULL while BatchHeartbeat's `renew_leases` kept
> extending the row's lease AND `updated_at` forever regardless — fixed by
> making `renew_leases` freeze BOTH `lease_until` AND `updated_at` for a
> `cluster_id`-NULL row (freezing `lease_until` alone, the round-3 fix as
> first shipped, does nothing for a `register_fresh` row whose `lease_until`
> is already NULL from creation — only the `updated_at`-keyed tombstone/
> never-announced purge sweep can ever reach it; caught by a targeted
> post-build Fable review before push), so it reaches its own ordinary
> TTL+grace/purge age and gets deleted, giving the next replay another
> reclaim shot — not an instant self-heal, since convergence still needs
> that next replay or reconnect. NEW-1/NEW-2 — round 2's own claim that
> both drop reasons "now emit telemetry" was FALSE as shipped: the event was
> never wired into `yuzu_gw_telemetry.erl`'s `?EVENTS`/`handle_event`/
> `declare_metrics`, so it was a pure no-op — two Gate-6 reviewers
> independently caught the same false ADR claim in the same wave; fixed by
> wiring it for real, with a new test file that fires the REAL event through
> the real handler (every other module's tests mock `telemetry` itself,
> which can't catch this class of gap). UP-4/COMP-6 — the decision's own
> `renew_leases`/`reclaim_tombstoned_session` calls were fail-OPEN on a
> degraded Postgres read, so a degraded-store window bypassed the entire
> stale/zombie-refusal mechanism outright; fixed to fail-CLOSED, mirroring
> `register_fresh`'s own precedent for exactly this class of decision.
> Deliberately deferred as the one remaining follow-up, not WS-4-gate-blocking: the
> reap-vs-replay-drip race after a >270s outage at fleet scale — filed as
> `#4627`, with related hardening filed alongside it (`#4628`-`#4632`). The
> `yuzu_gw_cluster` gossip/adjacency gen_server `#4555`'s design notes
> named as "remaining 4.4 scope" is judged OUT of WS-4 entirely
> (capacity/rebalancing, not reachability — the WS-4 gate exists because
> "commands can't reach agents").

> **⚠️ Standing instruction — update on close.** Every PR that closes or materially
> changes the status of a workstream here MUST update its row **and** re-stamp the
> Verified line in the SAME PR (source of truth: `docs/ha-delivery-matrix.md`; this
> table mirrors it). A matrix from a stale checkout is worse than none — treat status
> drift as a review-blocking defect, exactly like a stale doc comment. (This skill was
> itself found 557 commits stale once; hence the mandate.)

**`Gates?`** = does the safe-to-scale gate depend on this row (distinct from Prio).

| WS | Delivers | Depends on | Gates? | Routed reviewers | Prio | Status |
|----|----------|-----------|:---:|------------------|------|--------|
| **WS-0** | Durable agent-side command idempotency **+ terminal-outcome replay** (dup replays stored result, not bare `REJECTED`) | — | **Y** | `cpp-safety`+`cpp-expert` | P0 | **done (PR #3662 merged)** |
| **WS-1** | Server-plane state → Postgres: (1a) sessions DB-time; (1b) `execution_tracker`+command-correlation atomic counters; (1c) HA-critical store subset | migration ladder (serializes at the migration-version counter) | **Y** | `authdb`+`security-guardian` (1a); `architect`+`sre`+`cpp-safety` (1b/1c) | P0 | **done — 1a+1b+1c** |
| **WS-2** | (2a) durable **event outbox** + NOTIFY fan-out [monolith-OK]; (2b) **core→presentation event spine** [*defers to ADR-1005*]; MCP session/replay durability | 2a: WS-1(1b); 2b: ADR-1005 split | **Y** (2a) | `architect`+`sre`+`security-guardian`(MCP)+`docs-writer` | P1 | **2a done (2a-1 + 2a-2 #3924); 2b/MCP outstanding** |
| **WS-3** | Coordination seam: **fenced `LeaderElector`** (monotonic epoch in claim txn) + leader/**transactional-outbox**/receiver-idempotency worker refactor incl. policy remediation | **WS-0, WS-1, WS-2(2a)** | **Y** | `architect`+`cpp-safety`+`security-guardian` | P1 | **3.1 done (#4011); 3.2 done (#4134); 3.3 done (#4169); 3.4 done (#4194); #4014 leader observability shipped (metrics + alerts; gate not lifted)** |
| **WS-4** | Gateway routing + multi-cluster: fenced `agent→cluster` directory, **net-new distributed intra-cluster agent→node routing**, `gateway_node` convergence | **WS-1, WS-3, WS-0** | **Y** | `gateway-erlang`+`security-guardian`+`architect`+`cpp-safety` | P1 | **4.1 + 4.2a + 4.2b Tasks A–D + `#4324` per-home stream-generation fence + `#4555` cluster formation + 4.3a intra-cluster lookup + 4.4 (`gateway_node` convergence + `#4246` #6 writeback) all MERGED to `origin/dev`; rest of 4.3 (cross-cluster fan-out) / WS-5 cross-replica lookup remain — see `docs/ha-delivery-matrix.md`** |
| **WS-5** | Shared agent presence / health / **scope-eval population** across core replicas | **WS-4, WS-1, WS-3, WS-10** | **Y** | `security-guardian`+`architect`+`sre`+`docs-writer` | P1 | **slice 1 MERGED (#4745); slice 2 (durable cross-replica session resolution, `#4246` #3) MERGED (PR #5694); follow-ups PR #5736 (decommission cascade, #5682) and PR #5743 (#5684, #5686) MERGED; capability visibility / fleet gauge / #5685 / #5278 / WS-9 scenarios remain; #5683 (unique session index) done, the tombstoned-victim residual remains (#6339); gate NOT lifted** |
| **WS-6** | PKI/CA HA: shared CA key custody + node admission (**NOT** a `SecretCodec` blob — ADR-2002 §8 Update 2026-09-23, keeps ADR-0010 Decision 6), `CaStore` → PG (**already done**, ADR-0053), **durable CRL numbering + publication state machine**, KEK versioning/rollout/rollback, enrollment → PG (one-time `.cfg` import) | WS-3 (freshness pass); `ca_store` migration done | **Y** | `security-guardian`+`cpp-safety`+`docs-writer` (+`authdb` on 6.2) | P1 | **6.1 CRL publication (#4126, PR #4833) + WS-9 #4832 done; 6.2 enrollment/pending → PG done (97e24ec6e..a81938ada) incl. its own WS-9 scenario; 6.1b / 6.3 planned** — see `docs/ha-delivery-matrix.md` |
| **WS-7** | **HA-PG delivery**: Patroni+etcd+HAProxy Compose profile, selectable durability (3-node quorum default, distinct failure domains), operator-plane LB profile | — (storage axis; parallel) | **N** | `release-deploy`+`build-ci`+`sre` | P1 | **done (PR #3627 merged to dev)** |
| **WS-8** | Per-tier health contract (`/livez` vs `/readyz`; presentation→operator LB, core→presentation routing). **BYO-LB doc** + LB/session semantics | conceptual on WS-1/WS-2; readyz before LB fronts replicas | **Y** (readyz) | `docs-writer`+`release-deploy`+`sre` | P0 readyz / P2 doc | **readyz DONE (monolith, 2026-09-24): `pg_reachable` probe + drain grace; tier-split with the split; BYO-LB doc (P2) planned** |
| **WS-9** | **Failover test harness** — continuous, incremental scenarios added as each feature lands (not a final gate): session survival, no double-dispatch, effectively-once, cursor-poll no-loss, re-home races, quorum-degrade, standby loss | scenarios track WS-0…WS-7 as they land | N | `build-ci`+`release-deploy`; scenarios by `chaos-injector` | P1 (continuous) | in-progress: scenarios for WS-6, WS-7, WS-8 landed; WS-0…WS-5 and WS-10 have none yet |
| **WS-10** | **Background-job replica-safety classification** — checked-in, CI-auditable table (job → fenced-leader-only / replica-safe / disabled-until-fixed); bring #2508 wall-clock passes to clock-guard | audit+disable need nothing; `fenced-leader-only` enforcement needs WS-3 | **Y** | `cpp-safety`+`sre`+`compliance-officer` | P0 | **10.1/10.2 done (#4092); 10.3 enforcement wired by WS-3 3.2** |
| **WS-11** | **HA-state observability** (NEW): leader identity/epoch, replica lag, quorum state, outbox backlog, failover duration, routing re-homes, split-brain alerts — Prometheus metrics + rules | WS-3, WS-7 | N, except the #4014 leader-observability subset, which **gates** (2026-10-13) and is now shipped (the gate is not lifted); the rest ships *with* the 2nd replica | `sre`+`docs-writer` (+ alert-rule gate) | P1 | **leader-observability subset DONE (#4014: `yuzu_server_leader_*` + the four `yuzu-ha-leader` alerts; `SplitBrain` promtool-verified only); the rest planned; #6526 / #6527 / #6528 open** |
| **WS-12** | **Single→HA cutover + DR** (NEW): runbook to move an existing single deployment to HA-PG + gateway-front rollout; **backup/PITR/WAL under HA-PG** (replaces superseded `disaster-recovery.md`) | WS-7 | N | `release-deploy`+`sre`+`docs-writer` | P1 | planned |
| **WS-13** | **Agent-side gateway failover rollout** (NEW): agent endpoint discovery/failover + fleet rollout flipping direct-connect fleets to gateway-front. **Tracker #291** (roadmap 14.2). Failover is one-way without WS-15 | WS-4 | Y (gateway-fronted fleets) | `cross-platform`+`security-guardian` | P1 | planned |
| **WS-14** | **Coordination-substrate security & capacity review** (NEW): threat review of advisory locks / etcd / Patroni / HAProxy / fencing tokens; capacity + failure-domain + sync-quorum latency validation | WS-3, WS-7 | N | `security-guardian`+`sre` | P2 | planned |
| **WS-15** | **Gateway adjacency, load shedding, failback + rebalance** (NEW, 2026-10-13): roadmap **7.1.1**, **#5759**: adjacency table, rate-limited/jittered GOAWAY shedding, gradual failback, hysteresis, optional latency affinity. `yuzu_gw_cluster.erl` does not exist yet | WS-4, WS-13 | N (capacity) | `gateway-erlang`+`sre`+`architect` | P2 | planned |

### Hard invariants that must NOT regress when landing any WS

Pulled from ADR-2002 and the matrix's Definition-of-Done. Every WS PR checks:

- **Effectively-once, not exactly-once** — one effect *and* the original
  outcome across an agent bounce + a primary failover. A dup never loses the
  first result.
- **Fenced leadership** — a monotonic epoch is checked inside the claim
  transaction; a stale leader's writes are rejected. No singleton worker runs
  without holding the fence.
- **No committed event lost across failover** — events are durable (outbox)
  and replayable from a cursor on a *different* replica.
- **Routing directory is fenced** with CAS register/deregister — no stale
  replay overwrites a newer re-home.
- **RPO=0 across a host failure with 3-node quorum on distinct failure
  domains; quorum loss blocks writes (fail-closed)** — unless the operator has
  explicitly opted into degrade-to-async (WS-7's `YUZU_PG_SYNC_STRICT`).
- **A new background job is classified** (fenced-leader-only / replica-safe /
  disabled) in the WS-10 table before it can run under active-active.
- **Every WS is done only when it has a passing WS-9 scenario** (WS-9 is
  continuous, so this is not circular).

---

## 3. Gap / priority — what to build next

Prio in the matrix is **build-effort**; the **safe-to-scale gate** is the real
constraint. Delivery phases (dependency-ordered):

1. **Phase A — Foundation (build now, parallel where the ladder allows):**
   `WS-1` (state→PG; 1a/1b/1c pace on the migration ladder, *not* fully
   parallel), `WS-0` (agent idempotency+replay), `WS-2a` (durable outbox),
   `WS-10` (job-safety audit), and `WS-7` (HA-PG — storage axis, fully
   parallel; **DONE, PR #3627 merged**, unblocks WS-9's stack).
2. **Phase B — Multi-instance safety (ALL required before a 2nd replica):**
   `WS-3` (fenced leader), `WS-4` (gateway routing), `WS-5` (presence),
   `WS-6` (PKI), `WS-8`-readyz, `WS-13` (agent gateway-front rollout).
   **The split question (§1c) is RESOLVED — decoupled, ratified by the ADR-1005 owner (Dave Rae, 2026-09-07); the split does not gate a 2nd replica.**
3. **Phase C — Enable, validate, operate:** flip on the second replica;
   `WS-9` runs continuously throughout B/C; `WS-11` ships *with* the second
   replica; then `WS-12` (cutover/DR), `WS-14` (security/capacity), `WS-15`
   (gateway failback/rebalance, paired with WS-13). `WS-2b`
   (spine) and `WS-8` tier-split readyz land with the ADR-1005 split.

**Suggested next slices** (as of 2026-09-29 — `docs/ha-delivery-matrix.md` row
cites are authoritative):
- **Done (dial-selection, the safe-to-scale gate's WS-4 item):** WS-0 (#3662), WS-1 (1a+1b+1c), WS-2a
  (2a-1 + 2a-2 #3924), WS-3 (3.1–3.4, #4011/#4134/#4169/#4194), **WS-4's
  dial-selection half** (4.1+4.2a+4.2b+`#4324`+`#4555` (gateway multi-node
  cluster formation, `495cf24c4`)+4.3a (intra-cluster `pg`-group agent→node
  lookup)+4.4 (`gateway_node` convergence + `#4246` #6 writeback, ADR-2002
  §7c)+rest-of-4.3 (cross-cluster gateway fan-out, ADR-2002 §7d)), WS-7
  (#3627), WS-10 10.1/10.2. The storage axis is complete. **WS-4 is NOT
  entirely done** — two named items remain open and are tracked, not
  disclosed-only: `#4669` (multi-cluster mode has no agent↔cluster
  affinity/peer-identity binding, so it does not yet provide trust-zone
  isolation — caught by pr-rev, FortitudeEtc/Codex+Kimi, pre-merge on the
  rest-of-4.3 PR) and `#4672` (§7's durable outbox re-drive was never wired
  into `forward_gateway_pending`'s terminal-failure branches). Neither blocks
  the safe-to-scale gate today (multi-cluster mode has zero production
  deployments; the re-drive gap is inherited from before 4.3, not introduced
  by it), but do not read "WS-4 done" as "WS-4's every design goal closed."
- The **highest-leverage next** is now the remaining gate set directly:
  the rest of **WS-5** (slice 1 merged, #4745 — decommission cascade,
  capability visibility, fleet gauge, WS-9 scenario) and the rest of **WS-6**
  (6.1 merged #4833 + its WS-9 scenario #4832 done; **6.2 done** — enrollment/
  pending → Postgres, commits 97e24ec6e..a81938ada, incl. its own WS-9 scenario
  `ha-enrollment-concurrent-register.sh` — 6.1b / 6.3 remain). **WS-8**-readyz
  is DONE for the monolith (2026-09-24). A loss-free cross-replica reconnect
  (durable outbox replay) is the open 2a-2 follow-up.

**Gateway failover ↔ failback are one capability in two rows (2026-10-13).** Roadmap
**14.2 "Multi-Gateway Topology" (#291)** is delivered as **WS-13** (agent fails over to a surviving
gateway). Its declared dependency, roadmap **7.1.1 "Gateway Adjacency, Load Shedding, and
Latency-Based Redistribution" (#5759)**, is delivered as **WS-15** (failback, load sharing,
rate-limited shedding). 7.1.1 had no issue and was descoped from WS-4 without a named tracker
(ADR-2002 §7, the `yuzu_gw_cluster` paragraph), which is how it went missing. Plan, scope or
review either row together with the other:
- WS-13 without WS-15 is one-way. The survivors keep the extra load, and nothing moves agents back.
- WS-15 shedding must honour WS-13's one-channel-per-session rule: a shed agent re-registers and
  mints a new session.
- Failover does not remove a reconnect storm; it moves the failed node's share (about 1/N of the fleet) onto the
  survivors. Both rows therefore depend on CONNECTED-notice delivery holding at burst (BigColin CN1:
  `notify_pending_max`/`?MAX_NOTIFY_INFLIGHT` in `yuzu_gw_upstream.erl`) and on jittered
  reconnect/shed pacing.

**Shared with ADR-1005 (do not duplicate):** engine-tier HA (incl. NVD/CVE
sync, withdrawn from WS-1), the MCP Decision-15 pre-commitments WS-2 inherits,
and the presentation/core split (WS-2b + WS-8 tier-split readyz land with it).

---

## 4. Standard workflow for a workstream slice

For every WS in the matrix:

1. **Read first, in order:**
   - This skill (gap framing + the safe-to-scale gate).
   - `docs/ha-delivery-matrix.md` for the row's current-state cites +
     dependencies + reviewers.
   - `docs/adr/2002-high-availability-architecture.md` for the decision the
     slice must satisfy (the ADR governs on any conflict).
   - `docs/postgres-migration-ladder.md` for any WS-1/store-migration slice
     (it is the authoritative per-store status).
   - `docs/adr-1005-execution-plan.md` if the slice touches a shared seam
     (presentation/core split, engine tier, MCP Decision-15).

2. **Plan.** Produce a short plan covering: the ADR-2002 guarantee it delivers;
   whether it is in the safe-to-scale gate set; schema changes (via
   `MigrationRunner` / the PG store playbook); the fence/epoch or
   idempotency/outbox mechanism if applicable; and the **WS-9 scenario** it
   must add (a WS is not done without one).

3. **The split question (§1c) is RESOLVED** — decoupled, ratified by the ADR-1005
   owner (Dave Rae, 2026-09-07). Phase-B proceeds on the monolith track; no per-slice re-confirmation needed.

4. **Implement** as a focused PR per slice, in an isolated worktree off `dev`.
   Drive schema through `MigrationRunner` / `docs/postgres-store-playbook.md`,
   fencing through the `LeaderElector` epoch contract, and receiver dedup
   through the agent/gateway `command_id` path.

5. **Test.** Run `/test` before commit; add the WS-9 failover scenario and run
   the failover harness (`scripts/ha/` for the storage axis). Note WS-7-class
   deploy-only changes are a `/test` no-op — CI's build legs + the harness are
   the real gate there.

6. **Governance.** Run `/governance dev..HEAD` before pushing — the routed
   reviewers in the WS row are unconditional (e.g. `cpp-safety` on any fencing
   /ownership change, `security-guardian` on the coordination substrate,
   `gateway-erlang` on WS-4). CRITICAL/HIGH block merge. **Self-adversarial
   review (Sol / Kimi) before pushing review-fixes on HA work** — it has
   repeatedly caught blocking findings a reviewer would hit next round.

7. **Docs + evidence.** docs-writer picks up user-manual / ops-runbook updates
   in Gate 2; ship them in the same PR. For the coordination substrate,
   WS-14's threat/capacity notes and a `docs/security-reviews/` record apply.

---

## 5. Cross-references

- **The decisions:** `docs/adr/2002-high-availability-architecture.md`
- **The delivery spine (authoritative status):** `docs/ha-delivery-matrix.md`
- **Per-store migration status:** `docs/postgres-migration-ladder.md`
- **PG store authoring recipe:** `docs/postgres-store-playbook.md`
- **Shared decomposition / engine tier / MCP Decision-15:**
  `docs/adr-1005-execution-plan.md` + `docs/adr/003{1,2,3}-*.md`
- **WS-7 shipped surface:** `deploy/docker/docker-compose.ha-postgres.yml`,
  `deploy/docker/ha-postgres/`, `scripts/ha/`,
  `docs/user-manual/ha-postgres.md`, `docs/ha-postgres-ws7-plan.md`
- **Routed reviewers** are per-row in the matrix; the coordination-substrate
  concern routes `security-guardian` + `architect`.
