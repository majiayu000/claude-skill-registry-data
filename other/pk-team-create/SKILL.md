---
name: pk-team-create
description: "Command: pk-team-create"
---

# Command: pk-team-create

Full team derivation from scratch (v2 / catalog-driven). Selects
catalog Roles via the archetype-catalog mapping, opens RoleSlots
under the chartering Scope, fills them with TeamMembers, rewrites
`context/team/roster.md`, and emits a chartering DecisionRecord that
supersedes the prior team DecisionRecord. **No archetype Role
entities are written.**

## Syntax

```
pk-team-create
  --chartering-scope <SCOPE-id>      # required — Scope that owns the team's RoleSlots
  --subscription <provider>:<tier>   # e.g. anthropic:max-5x
  --providers <list|"any">           # comma-separated; "any" = all accessible
  --parallelism-cap <int>            # max RoleSlots opened per archetype, default 5
  --governance-floor <0-5>           # G-score floor, default 3
  [--weight-overrides <json>]        # {"C":0.60,"K":0.20,"L":0.10,"G":0.10}
                                     # CLI > DEC-*-TeamWeights > skill defaults
  [--threshold-overrides <json>]     # {"heavy_min":0.70,"medium_min":0.40}
                                     # CLI > DEC-*-TeamWeights > skill defaults
  [--landscape-artifact <ART-id>]    # explicit landscape override; skips discovery
  [--landscape <artifact-id>]        # alias for --landscape-artifact (kept for compat)
  [--archetype-catalog-mapping <path>]
                                     # CLI override of the archetype→catalog
                                     # mapping (replace mode). Project override
                                     # at context/team/archetype-catalog-mapping.yaml
                                     # is auto-detected; this flag wins over both.
  [--budget-drift-threshold <float>] # drift alert threshold %, default 20
  [--projection-method <method>]     # heuristic | model-recommender-quote | manual
                                     # default: heuristic
  [--dry-run]                        # print plan; write nothing
```

## Process (sequential)

### Step 1 — Resolve landscape snapshot

Three-level precedence (see `references/landscape-resolution.md`):

1. If `--landscape-artifact <ART-id>` (or alias `--landscape`) is
   supplied, load that artifact directly. Record
   `inputs_snapshot.landscape_artifact_source: "explicit"`.
2. Else query artifact index for the most-recently-created artifact
   tagged both `landscape-summary` **and** `landscape-summary-project`
   whose `spec.project_id` matches the current project context.
   Record `inputs_snapshot.landscape_artifact_source: "project-tag"`.
3. Else fall back to the most-recently-created artifact tagged
   `landscape-summary` (kit default). Record
   `inputs_snapshot.landscape_artifact_source: "kit-default"`.

If no artifact is found at any level, **abort** with:
> "No landscape-summary artifact found. Run the Haiku landscape-ingest
> task to produce an ART-*-LandscapeSnapshot artifact before running
> pk-team-create."

If the resolved artifact is older than 90 days, emit a warning but
continue. Record the artifact ID and its `created` date in the
DecisionRecord `inputs_snapshot`.

### Step 2 — Query accessible models

```
model-recommender.check_availability()
model-recommender.query_models(
  providers=<--providers>,
  G_floor=<--governance-floor>,
  apply_user_filter=true
)
model-recommender.get_pricing(sort_by="value_score")
```

Filter out any model with availability != "operational" unless the
owner explicitly passes `--allow-degraded`.

### Step 3 — Resolve weights + thresholds, then apply tiering formula

**Weight resolution (before scoring):**

```
CLI --weight-overrides <json>
  > DEC-*-TeamWeights.weight_overrides (tag: team-weights-override,
      most recent accepted; see references/team-weights-decision-schema.md)
    > skill defaults: {C:0.60, K:0.20, L:0.10, G:0.10}
```

**Threshold resolution (before classification):**

```
CLI --threshold-overrides <json>
  > DEC-*-TeamWeights.tier_thresholds (same DEC; validated on load)
    > skill defaults: {heavy_min:0.70, medium_min:0.40}
```

Validate any threshold override against the rules in
`references/team-weights-decision-schema.md` (§Threshold validation
rules). Violations are hard errors — abort before scoring.

Record `inputs_snapshot.weights_source` and
`inputs_snapshot.tier_thresholds_source` with the resolution level
used (`"cli"`, `"dec-team-weights"`, or `"skill-default"`), and
store the actual values in `inputs_snapshot.weights` and
`inputs_snapshot.tier_thresholds`.

**Scoring:**

For each accessible candidate model `m`:

1. Compute raw dimension values:
   - `C_raw(m)` = (swe_bench_verified + swe_bench_pro +
                   community_rating) / 3
   - `K_raw(m)` = 1 / (output_price_per_1M × quota_burn_vs_flagship)
   - `L_raw(m)` = output_tokens_per_sec
   - `G_raw(m)` = G-score from model-recommender (0–5 scale,
                  normalise to 0–1 by dividing by 5)

2. Min-max normalise each dimension across the full candidate set:
   `norm(x) = clamp((x - min) / (max - min), 0.01, 1.00)`

3. Compute TierScore using resolved weights `{C, K, L, G}`:
   `TierScore(m) = C×norm(C) + K×norm(K) + L×norm(L) + G×norm(G)`

4. Classify using resolved thresholds:
   - TierScore ≥ `heavy_min` → **heavy**
   - TierScore ≥ `medium_min` and < `heavy_min` → **medium**
   - TierScore < `medium_min` → **light**

5. Tier-collapse rule: if fewer than 3 distinct tiers result, promote
   the two highest-scoring light models to medium.

See `references/tiering-formula.md` for the full formula and worked
example.

### Step 4 — Load archetype-catalog mapping + role-archetypes override, then map archetypes

**Layer A — archetype-catalog mapping (eager validation — before archetype mapping):**

Resolve the archetype → catalog `(ROLE-id, seniority)` mapping with
three-level precedence:

1. `--archetype-catalog-mapping <path>` flag (CLI; replace semantics).
2. `context/team/archetype-catalog-mapping.yaml` (project; delta
   semantics by default — top-level `override_semantics: replace`
   switches to replace).
3. Kit default: `assets/archetype-catalog-mapping.yaml` shipped with
   the team-creator skill.

Validate eagerly: every archetype entry must declare a `role` that
starts with `ROLE-` and a non-empty `seniority`. Replace-mode
overrides must list all 8 archetypes (missing archetypes are a hard
error).

Record:
- `inputs_snapshot.archetype_catalog_mapping_file`: `"kit-default"`,
  `"project"`, or `"cli"` — which layer was applied.
- `inputs_snapshot.archetype_catalog_overrides`: per-archetype
  per-field deltas relative to the kit default. Empty list when the
  kit default was used verbatim.

**Layer B — role-archetypes override (eager validation — before archetype mapping):**

If `context/team/role-archetypes.yaml` exists, load it now and
validate it immediately against the rules in
`references/role-archetypes-override.md` (§Validation invariants).
Validation failures are hard errors — abort before any mapping begins.
This includes: PM pin must remain heavy, all rationales non-empty,
all 8 archetypes present in `replace` mode. (The legacy
`clone_cap_override` field is no longer accepted — capacity is the
count of RoleSlots opened in step 6 below.)

Record `inputs_snapshot.archetype_override_file: "present"` (or
`"absent"`) and list each overridden role with its new pin and
rationale summary in `inputs_snapshot.archetype_overrides`.

**Archetype mapping:**

For each of the 8 role archetypes:

1. Select the archetype's pinned tier — from the (possibly-overridden)
   archetype table. Kit defaults (`references/role-archetypes.md`)
   apply for any archetype not listed in a delta override, or when no
   override file is present.
2. From the models classified into that tier, pick the highest TierScore.
3. If preferred_providers are supplied and two models score within 0.05
   of each other, prefer the model from the preferred provider.
4. If the pinned tier has no candidates: apply the override-when rule
   from the active archetype table; if no override applies, fail
   with a clear message.
5. Resolve the archetype's `(role, seniority)` pair via the mapping
   from Layer A. Verify `role` is present in `context/roles/`; fail
   with a clear message if the catalog Role file is missing.

### Step 5 — Deactivate prior team (if re-running)

If `context/team/roster.md` already exists:

1. Parse the prior team's RoleSlot and Binding IDs from roster.md.
2. For each prior `role-slot-fill` Binding:
   `binding-management.end_binding(id, reason=
     "superseded by pk-team-create run <ISO-timestamp>")`
3. For each prior RoleSlot under the prior chartering Scope:
   `team-manager.close_role_slot(id, reason=
     "superseded by pk-team-create run <ISO-timestamp>")`.
   The slot state machine forbids reopening — re-charters always
   emit fresh `SLOT-*` IDs under the new chartering Scope. There is
   no Actor-template / Actor-clone distinction in v2; capacity is
   expressed by RoleSlot count, not by clone Actors.

If the prior team predates v2 (its roster references v1
`role-assignment` Bindings and archetype Roles), do NOT touch those
entities. The Phase A migration apply script
(`team-manager/scripts/apply_migration_2139.py`) is responsible for
back-filling the v1 surface; pk-team-create only operates on the v2
RoleSlot surface.

### Step 6 — Write entities

Skip if `--dry-run`.

For each of the 8 archetypes, look up `(role, seniority)` in the
mapping resolved in step 4. Open one RoleSlot per parallelism unit
(rank 1..N, where N is `--parallelism-cap`; `project-manager` is
always exactly 1 slot at rank=1):

```
team-manager.create_role_slot(
  scope=<--chartering-scope>,
  role=<ROLE-id from mapping>,
  seniority=<seniority from mapping>,
  rank=<int 1..N>,
  rationale="archetype=<archetype-name> tier=<tier> "
            "score=<tier-score> model=<model-id>",
  default_model_profile=<ART-*-ModelProfile-*>     # optional
)
```

Then, for each TeamMember selected to fill a slot:

```
team-manager.fill_role_slot(
  id=<SLOT-id>,
  team_member_slug=<team-member-slug>,
  rationale="<why this person for this slot>",
  valid_from=<today>,
  valid_until=<chartering Scope's ends_at, if any>
)
```

`fill_role_slot` writes the `role-slot-fill` Binding inline. No
archetype Role, Actor, or `role-assignment` Binding is written by
pk-team-create.

Ephemeral archetypes that have no persistent TeamMember to assign
(e.g. `assistant`, when handled by ad-hoc dispatch) leave the slot
in `state=open` with a `default_model_profile` set; the resolver
pre-step in `team-manager.get_interlocutor_runtime_binding` will
return the open slot's profile for ephemeral lookups.

### Step 7 — Write roster.md

Write `context/team/roster.md` with:
- Narrative preamble (team charter, subscription, governance floor)
- Routing table: role → actor → model-id → tier → tier-score
- Parallelism cap and PM clone-cap note
- Weights used (from inputs or defaults)
- Landscape artifact ID and date
- DecisionRecord ID (written in step 8)

### Step 7.5 — Compute budget projection

After step 6 writes all RoleSlots and before writing the chartering
DecisionRecord, iterate every created slot and compute a cost projection.

For each RoleSlot:

1. Call `model-recommender.get_pricing(<model_profile>)` to fetch the
   live unit cost.  Snapshot the returned `price_per_token_usd` into
   `unit_cost_usd` in the projection row.
2. Determine the effective time window for the slot:
   - If the slot is filled by a `type=consultant` TeamMember: intersect
     the consultant's `engagement_window` with the chartering Scope's
     `{starts_at, ends_at}`. Use the intersected window.
   - Otherwise: use the chartering Scope's full window.
3. Apply heuristic formula (when `--projection-method heuristic`):
   ```
   weeks = ceil(effective_window_days / 7)
   projected_total_usd = unit_cost_usd
                         × (avg_input_tokens + avg_output_tokens)
                         × expected_invocations_per_week
                         × weeks
   ```
   Defaults when not pinned by the landscape artifact:
   - `expected_invocations_per_week`: 50
   - `avg_tokens_per_invocation.input`: 8000
   - `avg_tokens_per_invocation.output`: 2000

4. Sum slot `projected_total_usd` values into `projected_total`.

5. Build the `budget_projection` block (see shape in step 8 below).
   Pass `drift_threshold_pct` from `--budget-drift-threshold` (default 20).

Skip budget projection if the chartering Scope has no `starts_at`/`ends_at`
dates; log a warning and set `budget_projection: null` in the snapshot.

### Step 8 — Write chartering DecisionRecord

```
decision-record-write(
  title="Team composition — <subscription> — <date>",
  state="accepted",
  supersedes=[<prior-team-decisionrecord-id>],  # if re-running
  inputs_snapshot={
    subscription: ...,
    governance_floor: ...,
    parallelism_cap: ...,
    weights: {C, K, L, G},
    weights_source: "cli" | "dec-team-weights" | "skill-default",
    tier_thresholds: {heavy_min, medium_min},
    tier_thresholds_source: "cli" | "dec-team-weights" | "skill-default",
    landscape_artifact: <ART-id>,
    landscape_artifact_date: <date>,
    landscape_artifact_source: "explicit" | "project-tag" | "kit-default",
    tier_scores: {<model-id>: <score>, ...},
    weight_overrides_applied: <bool>,
    # v2 catalog-mapping audit (additionalProperties=true on inputs_snapshot)
    archetype_catalog_mapping_file:
      "kit-default" | "project" | "cli",
    archetype_catalog_overrides: [
      {archetype, field, kit_default, project_value}, ...
    ],
    archetype_override_file: "present" | "absent",
    archetype_override_semantics: "delta" | "replace" | null,
    archetype_overrides: [...],   # list of {role, kit_default_pin, override_pin}
    chartering_scope: <SCOPE-id>,
    role_slots: [
      {archetype, slot_id, role, seniority, rank}, ...
    ],
    # Gap 5 — budget projection (additionalProperties=true; additive)
    budget_projection: {
      currency: USD,
      window: {starts_at: <ISO>, ends_at: <ISO>},  # = chartering Scope window
      projected_total: <float>,
      projection_method: heuristic | model-recommender-quote | manual,
      slot_projections: [
        {
          slot: SLOT-<id>,
          role: ROLE-<id>,
          seniority: <enum>,
          model_profile: ART-*-ModelProfile-*,
          expected_invocations_per_week: <int>,
          avg_tokens_per_invocation: {input: <int>, output: <int>},
          unit_cost_usd: <float>,          # snapshotted from get_pricing at charter time
          projected_total_usd: <float>,
          effective_window: {starts_at: <ISO>, ends_at: <ISO>},
        }, ...
      ],
      drift_threshold_pct: 20,             # from --budget-drift-threshold, default 20
      notes: <free-text or null>,
    }
  }
)
```

The `inputs_snapshot.weights` block is the canonical weight store
that `pk-team-rebalance` will read on future runs. The
`chartering_scope` and `role_slots` blocks are the v2 provenance
back-pointer from the DEC to the RoleSlots opened in step 6.

The `budget_projection` block is Gap 5 (SUB-4 / SwiftReef). It is
additive (`additionalProperties: true` on the decision_record schema);
old DecisionRecords without this block validate cleanly. The block is
the source of truth that `pk-team-review` Step 5c reads for drift
detection.

## Dry-run output format

```
=== pk-team-create DRY RUN ===
Subscription: <value>   Governance floor: <value>
Chartering Scope: <SCOPE-id>
Landscape: <artifact-id> (<date>)
Weights: C=0.60 K=0.20 L=0.10 G=0.10
Mapping source: kit-default | project | cli   (overrides: <count>)

Candidate models scored:
  <model-id>  TierScore=0.92  → heavy
  <model-id>  TierScore=0.61  → medium
  ...

RoleSlot plan (per archetype):
  project-manager  → ROLE-product-manager / senior  (heavy, score=0.92)
    1 slot at rank=1, fill: TEAMMEMBER-<slug>, model=<model-id>
  senior-architect → ROLE-solutions-architect / senior  (heavy, score=0.87)
    N slots at rank=1..N, fill: TEAMMEMBER-<slug>, model=<model-id>
  ...

Entities to write (skipped in dry-run):
  <total RoleSlot count> RoleSlot entities
  <total fill count>     role-slot-fill Binding entities
  context/team/roster.md
  DecisionRecord superseding <DEC-id>
===========================
```

## State side-effects (non-dry-run)

Creates: one RoleSlot per parallelism unit (under the chartering
Scope), one `role-slot-fill` Binding per filled slot, roster.md,
1 DecisionRecord. Closes prior RoleSlots and ends prior
`role-slot-fill` Bindings on re-charter. Does NOT write archetype
Role entities, Actor entities, or `role-assignment` Bindings —
those v1 surfaces are read-only during the deprecation window.
