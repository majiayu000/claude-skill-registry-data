---
name: evolve-scale
description: Scale AICP from single-host single-operator to multi-host fleet — multi-machine LocalAI cluster (per CLAUDE.md `## Infrastructure target`), per-host agent server, replicated DLQ/state, multi-operator concurrency. Distinct from `ops-scale` (runtime scaling — replicas/resources within current architecture); this skill is the architecture-evolving scale lifecycle. Loads when the operator says "scale to fleet" / "multi-host AICP" / "second machine" / "concurrent operators" / "scale beyond single-GPU".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# evolve-scale

Evolve AICP's scale envelope from its current single-host single-operator
shape toward fleet operation. Distinct from `ops-scale` (which adjusts
replicas/resources within the existing architecture); this skill is for
ARCHITECTURE-LEVEL scale changes.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "scale to fleet", "multi-host AICP", "second machine",
  "concurrent operators", "scale beyond single-GPU"
- **Capacity ceiling**: operator notices AICP can't handle the workload
  with current architecture (not just resources)
- **Fleet rollout**: per CLAUDE.md `## Infrastructure target`, planning
  the two-machine + multi-agent setup

Do NOT load when:

- The concern is replica/resource tuning within current architecture
  (load `ops-scale`)
- The concern is a single-machine GPU upgrade (CLAUDE.md `## Identity
  Profile` Phase row mentions the 19GB upgrade — that's hardware, not
  scale architecture)
- The concern is a NEW system to integrate (load `evolve-integrate`)

## Operations

### Operation 1 — Inventory current single-host architecture

**When**: pre-scale audit.

**Process**:

1. Per CLAUDE.md `## Architecture` and `## Infrastructure target`:
   - LocalAI runs on one host, GPU-bound (single-active-backend pattern)
   - DLQ in `~/.aicp/dlq/` (operator-local files)
   - Task manager in-process (per-invocation)
   - MCP server stdio (per-process)
   - Agent server optional, single-host
2. Identify scale assumptions baked into the architecture:
   - Single GPU model active (per single-active-backend)
   - File-based DLQ (per per-day-jsonl pattern)
   - Operator-local config in `~/.aicp/`
3. Document the current ceiling: what concurrent load exhausts current
   architecture?

**Quality bar**: scale planning starts with HONEST current-state assessment.
Don't propose multi-host plans without understanding what single-host
actually supports.

### Operation 2 — Plan the multi-host architecture

**When**: Operation 1 confirmed scale ceiling reached.

**Process**:

1. Per CLAUDE.md `## Infrastructure target`, the planned topology:
   ```
   Machine 1: Fleet Alpha    Machine 2: Fleet Bravo
   ├── LocalAI Cluster 1     ├── LocalAI Cluster 2
   ├── OpenClaw + MC         ├── OpenClaw + MC
   ├── Fleet Daemons         ├── Fleet Daemons
   └── 10 Agents (alpha-*)   └── 10 Agents (bravo-*)
   ```
2. Author decision page in `wiki/decisions/00_inbox/scale-multi-host.md`:
   - WHY: capacity / availability / geographic distribution?
   - ALTERNATIVES: vertical scale (bigger GPU) vs horizontal (multi-host)
   - REVERSIBILITY: can we collapse back to single-host?
3. Identify which AICP layers need scale changes:
   - LocalAI: P2P cluster peering (planned, partial per Stage 4)
   - DLQ: migrate to a shared queue per `infra-queue` if cross-host
     access needed
   - State: `.aicp/state.yaml` per-operator → does fleet need shared state?
4. Coordinate with `infra-networking` for cross-host network design

**Quality bar**: NEVER ship multi-host architecture without the decision
page. Inheriting "obvious" multi-host from someone else is operationally
brittle.

### Operation 3 — Execute scale evolution incrementally

**When**: decision approved; build toward the multi-host topology.

**Process**:

1. Phase 1: enable LocalAI P2P cluster peering between two LocalAI
   instances (per CLAUDE.md `## The Mission` Stage 4 status: pending)
2. Phase 2: deploy AICP on the second host with `--profile fleet-light`
   (or similar)
3. Phase 3: migrate DLQ to shared store if cross-host visibility needed
   (per `infra-queue` Operation 2)
4. Phase 4: validate with multi-host workload; rollback per phase if
   issues

**Quality bar**: each phase is independently rollback-able. NEVER bundle
phases — each is a discrete scale increment with its own validation.

### Operation 4 — Diagnose scale issues post-deployment

**When**: multi-host AICP shows unexpected behavior.

**Process**:

1. Run `aicp --check` on each host — is each individual AICP healthy?
2. Run `aicp --metrics` on each — are the per-backend tasks splitting
   as expected?
3. Check fleet-coordinated state: do both hosts agree on shared state?
4. Per `aicp-ops-dlq`, inspect each host's DLQ for cross-host coordination
   failures
5. If hosts diverge: investigate the shared state surface (often DLQ or
   profile config drift)

**Quality bar**: multi-host diagnosis is local-first (`--check` per host),
then cross-host (state agreement). Don't assume cross-host issues without
verifying single-host health first.

## Gotchas

- **Detection**: agent recommends multi-host scale without measuring single-host ceiling.
  **Rule**: confirm scale ceiling before adding architecture complexity.
  **Reasoning**: vertical scale (GPU upgrade — already done in CLAUDE.md
  to 19GB) is often cheaper than horizontal. Verify the ceiling first.

- **Detection**: agent ships multi-host changes without phasing.
  **Rule**: each scale increment (P2P peering / second host / shared DLQ)
  is a separate phase with independent validation + rollback.
  **Reasoning**: bundled changes mean bundled failures; phased changes
  isolate issues to specific layers.

- **Detection**: agent confuses `evolve-scale` with `ops-scale`.
  **Rule**: `ops-scale` adjusts replicas/resources within current
  architecture; `evolve-scale` changes the architecture itself.
  **Reasoning**: scoping correctly avoids over-engineering for what's
  actually a tuning problem.

- **Detection**: agent doesn't update CLAUDE.md after scale architecture changes.
  **Rule**: CLAUDE.md `## Architecture` and `## Infrastructure target`
  must reflect the new topology after scale changes.
  **Reasoning**: docs that describe single-host while reality is
  multi-host produces wrong mental models for new operators.

- **Detection**: agent skips P2P cluster peering (the foundation of multi-host LocalAI).
  **Rule**: per CLAUDE.md `## Infrastructure target`, LocalAI P2P is the
  load-balance + failover foundation. Skipping it means multi-host AICP
  can't share inference load.
  **Reasoning**: the planned topology depends on cluster peering; without
  it, multi-host degenerates to two single-host AICPs that can't coordinate.

## Reference exemplars

- CLAUDE.md `## Infrastructure target` — the canonical planned topology
- CLAUDE.md `## The Mission` Stage 4 — partial cluster peering status
- `config/fleet.yaml.template` — fleet config starting point
- `wiki/decisions/01_drafts/aicp-active-state-mechanism-for-hooks.md` —
  example of a state-mechanism decision (relevant for shared state in fleet)
- `wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md` —
  pattern doc that flags JSONL's scale ceiling (when to migrate)

## Domain context

AICP starts single-operator + single-host. The fleet ecosystem (per
CLAUDE.md fleet table — openfleet 10 agents, two machines) is the
documented scale target. Each scale step is operator-deliberate;
nothing in AICP currently auto-scales. P2P cluster peering for
LocalAI is the load-balance foundation; DLQ + state surfaces may
need additional architecture for cross-host operation.

## Related skills

| Skill | When to use |
|-------|-------------|
| `ops-scale` | When tuning replicas/resources within current architecture |
| `infra-networking` | When designing cross-host network for fleet rollout |
| `infra-queue` | When DLQ needs cross-host visibility (migration to real queue) |
| `architecture-propose` | When the scale change requires major architecture redesign |
| `aicp-ops-runtime` | When diagnosing per-host health post-scale-out |
