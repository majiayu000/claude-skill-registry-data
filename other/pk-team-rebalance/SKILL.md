---
name: pk-team-rebalance
description: "Command: pk-team-rebalance"
---

# Command: pk-team-rebalance

Apply a `pk-team-review` recommendation. Targeted re-tiering of one or
more roles without full team recreation. Requires `--confirm` to
prevent accidental writes.

## Syntax

```
pk-team-rebalance
  --roles <list|"all">         # comma-separated role names, or "all"
  --confirm                    # required; prevents accidental writes
  --reason <string>            # recorded in the DecisionRecord amendment
  [--landscape-artifact <ART-id>]  # explicit landscape override
  [--landscape <artifact-id>]      # alias for --landscape-artifact
  [--weight-overrides <json>]      # override stored weights for this run
  [--threshold-overrides <json>]   # override stored thresholds for this run
```

## Process (sequential)

### Step 1 — Load governing DecisionRecord + DEC-*-TeamWeights check

```
decision-record.get_decision(<governing-DEC-id>)
```

Read `spec.inputs_snapshot` to retrieve:
- Stored formula weights (used unless `--weight-overrides` supplied)
- `governance_floor`
- `parallelism_cap`
- The landscape artifact ID from the prior run

**DEC-*-TeamWeights newer-than-governing-DEC check:**

Query the decision index for the most-recent accepted DecisionRecord
tagged `team-weights-override` (see
`references/team-weights-decision-schema.md`). If one exists and its
`metadata.created` is **newer** than the governing team
DecisionRecord's `metadata.created`, emit this warning and do NOT
silently apply the new weights:

```
WARNING: A newer DEC-*-TeamWeights record (created <ISO-date>)
post-dates the governing team DecisionRecord (created <ISO-date>).
Weight policy has changed since the last pk-team-create run. This
targeted rebalance uses stored weights from the governing DEC.
To apply the updated weights across all roles, run:
  pk-team-rebalance --roles all --confirm --reason "<reason>"
```

CLI `--weight-overrides` and `--threshold-overrides` always override
stored values regardless of DEC age.

If `--roles all` is specified, re-run the full `pk-team-create` logic
(steps 1–8 of `pk-team-create`) and write a new DecisionRecord instead
of amending. The remainder of this document covers the non-`all`
path.

### Step 2 — Resolve landscape snapshot

Same resolution logic as `pk-team-create` Step 1. If `--landscape` is
not supplied, use the latest `landscape-summary` artifact. Warn if
older than 90 days; do not block.

### Step 3 — Resolve archetype names → catalog (role, seniority) and re-score

`--roles` accepts archetype names (`developer`, `senior-architect`,
...). Resolve each name through the archetype-catalog mapping
(`assets/archetype-catalog-mapping.yaml`, layered with
`context/team/archetype-catalog-mapping.yaml` if present) into the
catalog `(ROLE-id, seniority)` pair. Operate on the matching
`RoleSlot(s)` in the active chartering Scope.

For each archetype in `--roles`:

1. Look up `(role, seniority)` via the mapping. Abort if the
   archetype is not present and no project override defines it.
2. Query accessible models scoped to that archetype's pinned tier:
   ```
   model-recommender.query_models(
     G_floor=<governance_floor>,
     apply_user_filter=true
   )
   ```
3. Apply the tiering formula with stored (or override) weights.
4. Select the best-scoring candidate for the tier.
5. If the best candidate is the same model currently filling the
   archetype's RoleSlot(s): report "no change needed"; skip writes.

### Step 4 — End old role-slot-fill Bindings

For each archetype where a model change is needed, list the
matching RoleSlots in the active chartering Scope via
`team-manager.list_role_slots(scope=<chartering-scope>, role=<ROLE-id>,
state="filled")`, then for each filled slot end its current fill
Binding:

```
binding-management.end_binding(
  id=<current-role-slot-fill-BIND-id>,
  reason="superseded by pk-team-rebalance: <--reason> (<ISO-timestamp>)"
)
```

### Step 5 — Re-fill the existing RoleSlots

A targeted rebalance does NOT close-and-reopen the slot — capacity
(slot count) hasn't changed; only the TeamMember and the model
underneath it have. For each affected RoleSlot:

```
team-manager.fill_role_slot(
  id=<SLOT-id>,
  team_member_slug=<new-team-member-slug>,
  rationale="rebalanced <ISO-timestamp>: <--reason> "
            "(model: <new-model-id>, score: <score>)",
  valid_from=<today>,
  valid_until=<chartering Scope's ends_at, if any>
)
```

(If the new TeamMember does not yet exist in `context/team-members/`,
provision it first via the team-member skill. Ephemeral
`(role, seniority)` dispatches that have no persistent TeamMember
re-attach to the slot's `default_model_profile` instead — no fill
write is needed.)

### Step 6 — _(folded into step 5)_

v1 split this into "create new role-assignment Binding"; v2's
`fill_role_slot` writes the `role-slot-fill` Binding inline, so a
separate step is no longer required.

### Step 7 — Update roster.md in-place

Rewrite the affected rows in `context/team/roster.md`'s routing table.
Update the "Last rebalanced" timestamp and append the reason to the
history section.

### Step 8 — Amend governing DecisionRecord

Append to the governing DecisionRecord's `progress_notes`:

```
Rebalanced on <ISO-timestamp> by <actor>:
  Roles changed: <list>
  Reason: <--reason>
  New assignments: <role> → <model-id> (score: <score>)
  Weights used: C=<C> K=<K> L=<L> G=<G>
  Landscape: <artifact-id> (<date>)
```

A new DecisionRecord is NOT written unless `--roles all` is used.

## The `--roles all` shortcut

`pk-team-rebalance --roles all --confirm --reason "<reason>"` is
equivalent to running `pk-team-create` with the stored weights and
subscription, except:
- A new DecisionRecord IS written (superseding the current one).
- The deactivation sequence from `pk-team-create` Step 5 applies in full.

Use this when the landscape has shifted so broadly that targeted
rebalancing would touch every role anyway.

## State side-effects

Ends N old `role-slot-fill` Bindings. Re-fills the affected RoleSlots
(no slot create/close — capacity is unchanged) and writes N new
`role-slot-fill` Bindings via `team-manager.fill_role_slot`. Amends
roster.md in-place. Appends to the governing DecisionRecord's
`progress_notes`. Does NOT write a new DecisionRecord (unless
`--roles all`).

## Safety

- `--confirm` is always required. The command prints the plan and
  exits if `--confirm` is absent.
- Dry-run preview is printed before writing, even with `--confirm`:
  show the plan and ask for explicit "proceed" confirmation in
  interactive mode; in non-interactive mode proceed immediately after
  showing the plan.
