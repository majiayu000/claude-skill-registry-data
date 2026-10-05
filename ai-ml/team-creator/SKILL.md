---
name: team-creator
description: |
  Compose a provider-neutral AI team by tiering accessible models on
  cost-efficiency, capability, latency, and governance, then mapping
  the 8 processkit role archetypes onto catalog Roles + RoleSlots
  inside a chartering Scope. Use when bootstrapping a new project
  team, rotating after a provider change, or quarterly rebalancing.
  Triggers: "create my AI team", "compose a team", "rebalance the
  team", "review the team".
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-team-creator
    version: "2.0.0"
    created: 2026-04-15T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: model-recommender
        purpose: >
          Query, score, and filter accessible models via
          query_models, get_pricing, check_availability.
      - skill: team-manager
        purpose: >
          Open RoleSlot entities (create_role_slot) inside the
          chartering Scope and fill them via fill_role_slot. Replaces
          v1's archetype Role + Actor + role-assignment writes.
      - skill: binding-management
        purpose: >
          End superseded role-slot-fill Bindings via end_binding when
          re-running the charter.
      - skill: decision-record
        purpose: >
          Write the chartering DecisionRecord; read stored
          formula weights on rebalance via get_decision.
    provides:
      primitives: []
      mcp_tools: []
    commands:
      - name: pk-team-create
        args: "--subscription <provider>:<tier> --providers <list|any> --parallelism-cap <int> --governance-floor <0-5>"
        description: "Derive a full team from scratch: roles, actors, bindings, roster, and chartering DecisionRecord"
      - name: pk-team-review
        args: "[--landscape-artifact <ART-id>] [--threshold <float>]"
        description: "Read-only team health-check against the latest landscape snapshot"
      - name: pk-team-rebalance
        args: "--roles <list|all> --confirm --reason <string>"
        description: "Apply a pk-team-review recommendation: targeted re-tiering of one or more roles"
---

# Team Creator

## Intro

`team-creator` derives a provider-neutral AI team by scoring all
accessible models on four weighted dimensions (Capability, Cost,
Latency, Governance) and mapping the 8 processkit role archetypes
onto the resulting heavy / medium / light tiers. It composes 5
existing skills — no new primitives or MCP tools are introduced.

## Overview

### When to use

| Trigger | Command |
|---|---|
| New project or provider subscription | `pk-team-create` |
| Quarterly landscape shift | `pk-team-review` → `pk-team-rebalance` |
| Provider outage, rapid rotation | `pk-team-rebalance --roles all` |
| Spot-check current assignments | `pk-team-review` |

### Inputs (key parameters)

| Parameter | Required | Default | Notes |
|---|---|---|---|
| `--subscription <provider>:<tier>` | yes | — | e.g. `anthropic:max-5x` |
| `--governance-floor <0-5>` | no | 3 | Models below excluded before scoring |
| `--parallelism-cap <1-10>` | no | 5 | PM always capped at 1 |
| `--weight-overrides <json>` | no | see formula | Must sum to 1.0 ± 0.001; CLI > DEC-*-TeamWeights > defaults |
| `--threshold-overrides <json>` | no | `{"heavy_min":0.70,"medium_min":0.40}` | CLI > DEC-*-TeamWeights > defaults |
| `--landscape-artifact <ART-id>` | no | 3-level discovery | Explicit > project-tag > kit default; see `references/landscape-resolution.md` |
| `--landscape <ART-id>` | no | alias for `--landscape-artifact` | Kept for backwards compatibility |

### Catalog-driven archetype mapping (v2)

`team-creator` v2 selects existing `context/roles/ROLE-*` entries from
the 51-role catalog rather than writing 8 archetype Role entities. The
mapping ships in
`assets/archetype-catalog-mapping.yaml`; projects may layer a delta
override at `context/team/archetype-catalog-mapping.yaml`. Archetypes
are not stored as Roles — they are keys in the mapping file. See
`references/role-archetypes.md` and the kit-default mapping asset for
the 8 archetype → catalog Role + seniority pairs.

For every selected archetype, `pk-team-create` opens a **RoleSlot**
under the chartering Scope via `team-manager.create_role_slot` (one slot
per parallelism unit; `rank=1` is the primary). When a TeamMember is
chosen to fill a slot, `team-manager.fill_role_slot` writes the
`role-slot-fill` Binding. No archetype Role entities are written; v1
`role-assignment` Bindings remain readable for one minor version.

### Tiering formula (summary)

**Defaults rebalanced 2026-04-15 after the 2026-04-15 internal review (see ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff §7).** Capability weight raised from 0.40 to 0.60 to prevent tier inversion on same-provider candidate sets where cost and capability are anti-correlated.

| Dim | Weight | Source |
|---|---|---|
| Capability (C) | 0.60 | swe_bench + community rating, normalised |
| Cost efficiency (K) | 0.20 | 1 / (output_price × quota_burn), normalised |
| Latency fit (L) | 0.10 | output_tokens_per_sec, normalised |
| Governance (G) | 0.10 | G-score from model-recommender, normalised |

`TierScore ≥ 0.70 → heavy | 0.40–0.69 → medium | < 0.40 → light`

See `references/tiering-formula.md` for normalisation, thresholds,
and a full worked example.

### Role archetypes → tier mapping

| Role | Tier pin | Override? |
|---|---|---|
| project-manager | heavy | Never (immutable) |
| senior-architect | heavy | Medium only if no heavy clears G-floor + owner approval |
| senior-researcher | heavy | Same as senior-architect |
| junior-architect | medium | Heavy if capability gap > 15pp on SWE-bench |
| developer | medium | Heavy if `--security-critical` flag set |
| junior-researcher | medium | No override |
| junior-developer | light | Medium if no light model accessible |
| assistant | light | No override; shares junior-developer model if no light available |

See `references/role-archetypes.md` for full override-when rules.

Project-level overrides: if `context/team/role-archetypes.yaml`
exists, it is loaded before archetype mapping and validated eagerly.
See `references/role-archetypes-override.md` for schema and invariants.

### Commands

**`pk-team-create`** runs the full derivation: queries models, applies
the tiering formula, maps archetypes, **opens one RoleSlot per
parallelism unit** under the chartering Scope via
`team-manager.create_role_slot`, rewrites `context/team/roster.md`,
and emits a chartering DecisionRecord that explicitly supersedes the
prior team DecisionRecord. Archetype Roles are NOT written — the
catalog-mapping file is read instead. Use `--dry-run` to print the
plan without writing.

**`pk-team-review`** is read-only. Re-scores current assignments against
the latest landscape snapshot, diffs tier scores against those stored
in the governing DecisionRecord, and surfaces tier-shifts, unavailable
models, and new outperformers. Surfaces RoleSlots by their archetype
name (resolved through the mapping file). No entities are written.

**`pk-team-rebalance`** applies a review recommendation. Requires
`--confirm`. For `--roles all`, the full create logic re-runs and a
new DecisionRecord is written. For named roles, the operator names an
archetype (`developer`, `senior-architect`, ...); the skill resolves
to the (role, seniority) pair via the mapping and operates on the
matching RoleSlot(s) in the active chartering Scope. The governing
DecisionRecord's `progress_notes` are amended.

### Outputs

| Output | `pk-team-create` | `pk-team-review` | `pk-team-rebalance` |
|---|---|---|---|
| RoleSlot entities (per parallelism unit) | YES | NO | scoped roles |
| `role-slot-fill` Bindings | YES (one per filled slot) | NO | per rotated slot |
| `context/team/roster.md` | YES | NO | YES (in-place) |
| DecisionRecord | YES (new) | NO | amend notes |
| Diff report | NO | YES (stdout) | NO |

## Gotchas

- **Missing landscape-summary artifact.** This skill ingests a
  pre-structured markdown artifact tagged `landscape-summary`, NOT
  raw HTML. If none exists, error: "No landscape-summary artifact
  found. Run the Haiku landscape-ingest task to produce
  ART-*-LandscapeSnapshot before pk-team-create." Do not parse HTML.

- **Entity deactivation sequence on re-create.** When `pk-team-create`
  is re-run: (a) resolve prior team from roster.md; (b) for each
  prior `role-slot-fill` Binding call `binding-management.end_binding`
  with `reason="superseded by pk-team-create run <timestamp>"`;
  (c) close the prior RoleSlots via `team-manager.close_role_slot`
  (the slot state machine forbids reopening — re-charters always
  emit fresh SLOT-* IDs under the new Scope); (d) open new RoleSlots
  via `team-manager.create_role_slot` and fill them with
  `team-manager.fill_role_slot`. v1 `role-assignment` Bindings
  observed during a re-charter remain readable but are not migrated
  by `pk-team-create` — the Phase A apply script (see
  `team-manager/scripts/apply_migration_2139.py`) handles that
  one-shot back-fill.

- **Formula weight persistence.** Weights live in the chartering
  DecisionRecord's `spec.inputs_snapshot` block. `pk-team-rebalance`
  reads them via `decision-record.get_decision`. No skill-local
  config file for weights.

- **Tier-collapse (< 3 tiers accessible).** Promote the two highest-
  scoring light models to medium. Never fail; degrade gracefully.

- **PM is always rank=1, single slot.** Parallelism cap never applies
  to project-manager; the project-manager archetype always opens
  exactly one RoleSlot at `rank=1` (per DEC-20260414_0900). The
  `primary_contact: true` annotation on the project-manager mapping
  entry is retained as a convention marker — the actual semantics
  are now expressed by `RoleSlot.rank=1`.

- **Snapshot staleness.** Artifact older than 90 days → warn and
  proceed. Surface the artifact date in the DecisionRecord.

- **Provider-neutrality.** Never hardcode any model name, provider
  name, or tier label anywhere in this skill. All identifiers flow
  in from `model-recommender`.

- **Override audit trails (override layers 1–4).** Each override
  layer produces a distinct audit entry in the chartering team
  DecisionRecord's `inputs_snapshot`:
  - Layer 1 (landscape): `landscape_artifact_source` records
    `"explicit"` | `"project-tag"` | `"kit-default"` and the
    resolved ART-id. The project-tagged artifact (ART-*) is itself
    the audit record for who created the custom landscape.
  - Layer 2 (weights): `weights_source` + `weights` block records
    which DEC-*-TeamWeights (if any) was applied, or `"cli"` /
    `"skill-default"`. The DEC-*-TeamWeights record carries its own
    rationale and deciders.
  - Layer 3 (thresholds): `tier_thresholds_source` + `tier_thresholds`
    block; co-located with Layer 2 in the same DEC-*-TeamWeights
    record (causally coupled — cannot drift).
  - Layer 4 (role pins): `archetype_override_file`, `archetype_override_semantics`,
    and `archetype_overrides` list each overridden role with its new
    pin. The `context/team/role-archetypes.yaml` file itself is
    the persistent record.
  Any run with overrides: query the single chartering team
  DecisionRecord to fully reconstruct the run's configuration.

- **v0.16.0 capacity fields are gone.** v1 emitted five fields on Role
  / Actor entities (`primary_contact`, `clone_cap`, `cap_escalation`,
  `is_template`, `templated_from`). v2 stores capacity as the count of
  RoleSlots opened under a chartering Scope — there is no
  `clone_cap` field. Re-tiering replaces the matching RoleSlot's
  fill rather than spawning a clone Actor; the seed/clone distinction
  is therefore obsolete. v0.19.0 removed the fields from the live
  `role.yaml` and `team-member.yaml` schemas; older entity files that
  still carry them are tolerated as historical residue but are not
  produced by this skill.

## Agent-driven discovery

Agents can resolve user intent into the correct override layer using
the trigger phrases below. These are additive to the existing
`team-creator` triggers above — they extend the skill-finder entries,
not replace them.

| Layer | Trigger phrases | Routed action |
|---|---|---|
| Layer 1 — landscape | "use our own model list", "we have a custom provider set", "this project uses different models", "update the landscape for this project" | Create project-tagged landscape artifact (`landscape-summary-project` tag + `project_id`); pass `--landscape-artifact` to `pk-team-create` |
| Layer 2 — weights | "we value latency more", "cost matters more here", "prioritise governance", "adjust the scoring weights", "latency is critical for this project" | Write a `DEC-*-TeamWeights` record (tag: `team-weights-override`) via `decision-record-write`; re-run `pk-team-create` to pick it up |
| Layer 3 — thresholds | "the tier cutoffs don't fit our model set", "too many models landing in medium", "adjust the heavy threshold", "nothing is reaching heavy tier" | Amend or create `DEC-*-TeamWeights` with a `tier_thresholds` block; validate against rules in `references/team-weights-decision-schema.md` |
| Layer 4 — pins | "pin senior-architect to medium for this project", "we want all researchers on heavy", "remap role classes", "change the role tier assignments" | Create or update `context/team/role-archetypes.yaml`; re-run `pk-team-create` (eager validation fires on startup) |

Agents MUST consult skill-finder before routing any of these requests.
The trigger phrases are designed to match natural-language owner requests
without the owner naming the override layer explicitly.

## No-skill-inflation rationale

Option C chosen over extending `agent-management` (heaviest skill;
scope bleed) or `model-recommender` (individual model profiling vs.
team orchestration). Pure orchestration consumer: 5 existing skills
composed, 3 commands added, 0 new primitives or MCP tools.

## Full reference

### CLI contract — `pk-team-create`

```
pk-team-create
  --subscription <provider>:<tier>     # e.g. anthropic:max-5x
  --providers <list|"any">             # comma-separated; "any" = all accessible
  --parallelism-cap <int>              # max clones per role, default 5
  --governance-floor <0-5>             # G-score floor, default 3
  [--weight-overrides <json>]          # CLI > DEC-*-TeamWeights > defaults
  [--threshold-overrides <json>]       # CLI > DEC-*-TeamWeights > defaults
  [--landscape-artifact <ART-id>]      # explicit landscape; skips discovery
  [--landscape <ART-id>]               # alias for --landscape-artifact
  [--allow-degraded]                   # include models whose availability
                                       # is not "operational"
  [--security-critical]                # promotes developer archetype to heavy
  [--dry-run]                          # print plan; write nothing
```

Full step-by-step process (8 steps: resolve landscape → query models →
score+classify → load archetype-catalog mapping + map archetypes →
end prior `role-slot-fill` Bindings + close prior RoleSlots → open
new RoleSlots and fill them → write roster → write chartering
DecisionRecord) lives in `commands/pk-team-create.md`. Read that file
before changing the sequence; the order of (a) eager mapping-file
validation before archetype mapping, (b)
`binding-management.end_binding` before
`team-manager.close_role_slot`, and (c) DecisionRecord written
LAST so its ID can be embedded in roster.md is load-bearing.

### CLI contract — `pk-team-review`

```
pk-team-review
  [--landscape-artifact <ART-id>]      # default: same 3-level resolution
                                       # as pk-team-create
  [--threshold <float>]                # tier-shift sensitivity, default 0.05
```

Read-only. Re-scores the current team's models against the latest
landscape snapshot, diffs each TierScore against the value stored in
the governing chartering DecisionRecord's
`spec.inputs_snapshot.tier_scores` block, and prints a tier-shift
table to stdout. No entities written; no DecisionRecord amended.

### CLI contract — `pk-team-rebalance`

```
pk-team-rebalance
  --roles <list|"all">                 # comma-separated archetype names
  --confirm                            # required; no-op without it
  --reason <string>                    # free-text rationale; persisted
  [--landscape-artifact <ART-id>]
  [--weight-overrides <json>]
  [--threshold-overrides <json>]
```

For `--roles all`, full `pk-team-create` logic re-runs and a new
chartering DecisionRecord supersedes the current one. For named
archetypes, the matching RoleSlot's fill is rotated (end old
`role-slot-fill` Binding; fill the slot with the new TeamMember via
`team-manager.fill_role_slot`) and the governing DecisionRecord's
`progress_notes` are amended with the `--reason` string and the new
tier-score for each rotated archetype.

### Skill composition map

| Phase | MCP / skill call | Source skill |
|---|---|---|
| Step 2 | `check_availability`, `query_models`, `get_pricing` | model-recommender |
| Step 5 (a) | `end_binding` (per prior `role-slot-fill` Binding) | binding-management |
| Step 5 (b) | `close_role_slot` (per prior RoleSlot in the rotating archetype) | team-manager |
| Step 6 (RoleSlot) | `create_role_slot` (one per parallelism unit; rank 1..N) | team-manager |
| Step 6 (Fill) | `fill_role_slot` (places a TeamMember into the open slot) | team-manager |
| Step 8 | `record_decision` (chartering DEC) | decision-record |
| Rebalance read | `get_decision` (governing DEC for stored weights) | decision-record |

`team-creator` itself ships **no MCP server**; every write goes via the
upstream skills above. This is what keeps `provides.primitives: []`
and `provides.mcp_tools: []` in the frontmatter honest.

### 4-layer override model (data sources)

| Layer | What | Where it lives | Audit field in chartering DEC |
|---|---|---|---|
| 1 — landscape | The candidate model set | ART-*-LandscapeSnapshot artifact (tagged `landscape-summary` or `landscape-summary-project`) | `landscape_artifact`, `landscape_artifact_source`, `landscape_artifact_date` |
| 2 — weights | `{C, K, L, G}` for the TierScore formula | DEC-*-TeamWeights (tag `team-weights-override`) `spec.weight_overrides` | `weights`, `weights_source` |
| 3 — thresholds | `{heavy_min, medium_min}` | Same DEC-*-TeamWeights `spec.tier_thresholds` (causally coupled to layer 2) | `tier_thresholds`, `tier_thresholds_source` |
| 4 — archetype pins | Role → tier mapping overrides | `context/team/role-archetypes.yaml` (delta or replace mode) | `archetype_override_file`, `archetype_override_semantics`, `archetype_overrides` |

CLI flags ALWAYS win over DEC-stored values, which always win over
skill defaults. Eager validation for layer 4 fires BEFORE archetype
mapping; layers 2/3 validation is invoked from
`references/team-weights-decision-schema.md`. Validation failures at
any layer are hard errors — the run aborts before any entity write.

### Tiering formula — canonical definition

```
norm(x)        = clamp((x - min) / (max - min), 0.01, 1.00)
TierScore(m)   = C·norm(C_raw(m))
               + K·norm(K_raw(m))
               + L·norm(L_raw(m))
               + G·norm(G_raw(m))

C_raw(m)       = (swe_bench_verified + swe_bench_pro + community_rating) / 3
K_raw(m)       = 1 / (output_price_per_1M × quota_burn_vs_flagship)
L_raw(m)       = output_tokens_per_sec
G_raw(m)       = G_score / 5             # normalise 0-5 → 0-1

Defaults       C=0.60  K=0.20  L=0.10  G=0.10   (sum = 1.0 ± 0.001)
Tier cuts      heavy ≥ 0.70   medium ≥ 0.40   light < 0.40
```

Worked example and edge cases in `references/tiering-formula.md`.

### Role archetype pin table (kit defaults)

| Archetype | Catalog Role | Seniority | Tier pin | Slots opened | Override-when |
|---|---|---|---|---|---|
| project-manager | ROLE-product-manager | senior | heavy | 1 (rank=1, primary contact) | Never (PM is immutable; always exactly one slot) |
| senior-architect | ROLE-solutions-architect | senior | heavy | up to `--parallelism-cap` | Medium only if no heavy clears G-floor + owner approval |
| senior-researcher | ROLE-research-scientist | senior | heavy | up to `--parallelism-cap` | Same as senior-architect |
| junior-architect | ROLE-solutions-architect | specialist | medium | up to `--parallelism-cap` | Heavy if capability gap > 15pp on SWE-bench |
| developer | ROLE-software-engineer | senior | medium | up to `--parallelism-cap` | Heavy if `--security-critical` flag set |
| junior-researcher | ROLE-research-scientist | specialist | medium | up to `--parallelism-cap` | No override |
| junior-developer | ROLE-software-engineer | junior | light | up to `--parallelism-cap` | Medium if no light model accessible |
| assistant | ROLE-assistant | specialist | light | up to `--parallelism-cap` | No override; shares junior-developer model if no light available |

The `(role, seniority)` pairs above come from
`assets/archetype-catalog-mapping.yaml` (the kit default) and may be
overridden per-project at `context/team/archetype-catalog-mapping.yaml`.
The "Slots opened" column is the v2 replacement for v1's `clone_cap`
field — v0.19.0 removed `clone_cap`/`cap_escalation`/`primary_contact`
from the Role schema and `is_template`/`templated_from` from the
TeamMember schema; the count of RoleSlots under the chartering Scope
is the canonical capacity record. See
`references/role-archetypes.md` for the full responsibilities lists.

### chartering DecisionRecord — `inputs_snapshot` schema

The DecisionRecord schema (`SCHEMA-decisionrecord` v1.0.0) declares
`inputs_snapshot` with `additionalProperties: true`, so v2 augments
the block with two catalog-mapping audit fields without a schema bump:

```yaml
spec:
  inputs_snapshot:
    subscription: <provider>:<tier>
    governance_floor: <0-5>
    parallelism_cap: <int>
    weights:                  {C: <float>, K: <float>, L: <float>, G: <float>}
    weights_source:           cli | dec-team-weights | skill-default
    tier_thresholds:          {heavy_min: <float>, medium_min: <float>}
    tier_thresholds_source:   cli | dec-team-weights | skill-default
    landscape_artifact:       ART-<id>
    landscape_artifact_date:  <ISO date>
    landscape_artifact_source: explicit | project-tag | kit-default
    tier_scores:              {<model-id>: <float>, ...}
    weight_overrides_applied: <bool>
    archetype_catalog_mapping_file: kit-default | project | cli   # v2
    archetype_catalog_overrides:                                   # v2
      - {archetype, field, kit_default, project_value}
    archetype_override_file:  present | absent
    archetype_override_semantics: delta | replace | null
    archetype_overrides:      [{role, kit_default_pin, override_pin, rationale}]
    chartering_scope:         SCOPE-<id>     # v2 — required for RoleSlot writes
    role_slots:                              # v2 — provenance back-pointer
      - {archetype, slot_id, role, seniority, rank}
```

`archetype_catalog_mapping_file` records which layer of the
mapping-file precedence chain was applied
(`cli` > `project` > `kit-default`).
`archetype_catalog_overrides` lists each per-archetype-per-field
delta when the project file modifies the kit default; an empty list
means the kit default was used verbatim.

`pk-team-rebalance` and `pk-team-review` both read this block via
`decision-record.get_decision`. It is the single source of truth for a
team's configuration — there is no skill-local config file for
weights, thresholds, or pins. `inputs_snapshot.tier_scores` is what
`pk-team-review`'s diff is computed against.

### Referenced source files

| Path | Purpose |
|---|---|
| `commands/pk-team-create.md` | Step-by-step command process (8 steps) |
| `commands/pk-team-review.md` | Read-only diff process |
| `commands/pk-team-rebalance.md` | Targeted rotation process |
| `references/landscape-resolution.md` | 3-level landscape discovery rules |
| `references/tiering-formula.md` | Normalisation, thresholds, worked example |
| `references/role-archetypes.md` | Kit-default pins + responsibilities |
| `references/role-archetypes-override.md` | YAML schema + validation invariants |
| `references/team-weights-decision-schema.md` | DEC-*-TeamWeights schema + threshold validation rules |

### Extension points

- **New role archetype.** Add an entry to
  `assets/archetype-catalog-mapping.yaml` (or a project override at
  `context/team/archetype-catalog-mapping.yaml`) keyed by archetype
  name with `role: ROLE-<id>` + `seniority: <enum>`. Update
  `references/role-archetypes.md` with the responsibilities one-liner
  and add a row to the pin table above. The PM-immutability invariant
  remains in force (`project-manager.role` must remain
  `ROLE-product-manager` and the slot count must remain 1). v2
  archetypes are mapping keys, not Role entities — no schema change
  is required.
- **New scoring dimension.** Extend the weight set (currently
  `{C, K, L, G}`); update `weights` schema in `inputs_snapshot`,
  the worked example in `references/tiering-formula.md`, and the
  validation rule that weights sum to 1.0 ± 0.001.
- **New override layer.** Add a layer-N row to the team-creator override layers table,
  define an audit field in `inputs_snapshot`, and document the
  precedence rule (CLI > DEC > defaults) for the new layer.

### Corner cases

- **Tier collapse (< 3 distinct tiers).** Promote the two
  highest-scoring light models to medium. Never abort — degrade
  gracefully. Recorded in DEC `inputs_snapshot.notes`.
- **Snapshot staleness > 90 days.** Warn and continue; surface the
  artifact date in the DecisionRecord rather than hiding it.
- **PM single-slot rule.** `--parallelism-cap` is silently overridden
  to 1 for `project-manager` regardless of CLI / archetype overrides
  (DEC-20260414_0900). Layer-4 overrides cannot raise it; the
  project-manager archetype always opens exactly one RoleSlot at
  rank=1.
- **Slot continuity across rebalances.** A targeted rebalance
  (`pk-team-rebalance --roles <list>`) re-fills the existing RoleSlot
  rather than closing and re-opening it; SLOT-* IDs are stable
  across model rotations and only change on `--roles all`
  (full re-charter).
- **Empty preferred-providers tie-break.** Two models within 0.05
  TierScore and no preferred provider supplied: pick the higher raw
  Capability score, then alphabetical model-id as final tie-break.
- **Provider neutrality.** No model name, provider name, or tier
  label may be hardcoded anywhere in this skill — all identifiers
  flow in from `model-recommender`. Hardcoding is caught by
  release-audit's `skill_structure` check on the next release.
