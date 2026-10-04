---
name: rank-recommendations
description: Rank /next's derived candidate set into one next-best-action plus a ranked list (≤11 entries total), each with the exact command and a plain-language explanation of why it is recommended and what it unblocks — weighing structural priority (repair first, roadmap order, unblock count) and operator fit per the work-intelligence shelf's rules, skipping fit entirely when history is thin. Ranking and explanation ONLY — the candidate set is authoritative and this skill may never add, remove, or re-derive a candidate, never read the product model directly, and never write anything but the two recommendation artifacts. Use only from the /next play via product-os-keeper.
---

# rank-recommendations

Turn /next's mechanically derived candidate set into the recommendation the
operator reads: one **next-best-action (NBA)** plus a ranked list, capped at
**11 entries total including the NBA**, every entry carrying the exact command
and a plain-language explanation.

This skill is the ONLY judgment step in /next. Everything upstream is
deterministic (scan → derive → classify); everything here is ordering and
explaining what those scripts found. The boundary is hard: **the candidate set
is authoritative** — this skill never invents, drops, or re-derives a
candidate, and never reads the product model itself.

## Inputs (JSON contract)

| Field | What it is |
|-------|-----------|
| `candidates` | path to `candidates.json` from `derive_candidates.py` — the authoritative set: runnable + blocked candidates, gates, unblocks, lanes, and the inconsistency report |
| `operator_profile` | path to `operator-profile.json` from `classify_work.py` — author, work-type/stack distributions, `thin_history` flag |
| `fit_rules` | path to the work-intelligence shelf's `operator-fit.md` — the judgment rules for fit boosts |
| `model_state` | path to `model-state.json` — read-only context for writing grounded explanations (names, outcomes, orders); NEVER for adding candidates |
| `out_yaml` | path to write `recommendations.yaml` (machine) |
| `out_md` | path to write `recommendations.md` (human) |

## Ranking procedure

1. **Repair first (C5).** If the inconsistency report is non-empty, the
   highest-priority repair-lane candidate IS the NBA. No exceptions — a broken
   model poisons every downstream recommendation on that path.
2. **Structural order.** Then rank runnable candidates by: lane urgency
   (execute work already in flight, then grill, then foundation, then lens,
   then strategy, then learning/refresh), how much each unblocks (more
   downstream work first), and roadmap order (lower `order_hint` first).
   Blocked entries that the operator should *see* (the queue behind a
   blocker) rank below runnable ones and always name their blocker.
3. **Operator fit — only when trusted (C7/F4).** If `thin_history` is false,
   apply the shelf's fit rules: boost candidates matching the dominant work
   types/stacks **within their lane** (fit never overrides repair or
   structural order), and record a `fit_reason` on every boosted entry. If
   `thin_history` is true: apply NO fit adjustment, set NO `fit_reason`
   anywhere, and write a `fit_notice` stating fit was skipped and why.
4. **Cap to 11 (C4).** NBA + at most 10 more. Every runnable candidate that
   does not make the cut goes into `cut_for_cap` (its candidate id) — nothing
   is silently dropped (F6).
5. **Explain (C3).** Every entry gets a `why` in plain language — why now,
   citing its gates — and an `unblocks` line saying what it opens up. The NBA
   additionally gets a short paragraph in the markdown: what it is, why it
   beats everything else, what happens after it lands.

## Outputs

`recommendations.yaml`:

```yaml
generated_for: <author>
basis:
  model_hash: <from candidates.derived_from_model_hash>
  derivation_hash: <from candidates.derivation_hash>
nba:
  candidate_id: <id>            # MUST be an id from candidates.json
  command: </play args>
  why: <plain-language explanation, full sentences>
  unblocks: <what it opens>
  fit_reason: <only when fit applied; absent otherwise>
entries:                        # ranked, ≤10
  - candidate_id: ...
    command: ...
    why: ...
    unblocks: ...
    blocker: <verbatim from the candidate, when status is blocked>
    fit_reason: <optional>
fit_notice: <required when thin_history; absent otherwise>
cut_for_cap: [<candidate ids>]  # runnable candidates that didn't fit the cap
```

`recommendations.md`: the human report — the NBA as a lead paragraph, the
ranked list with one short explanation each, the inconsistency report (when
non-empty) as a "model needs repair" section, and the fit notice or fit
summary at the end. Plain language throughout; no field-name soup.

## Boundaries

### NEVER
- Add, remove, merge, or re-derive a candidate — `candidates.json` is the
  single source of what is possible.
- Read the product model tree, run git, or invoke another play or skill.
- Apply fit weighting (or emit any `fit_reason`) when `thin_history` is true.
- Exceed 11 entries including the NBA, or drop a runnable candidate without
  listing it in `cut_for_cap`.
- Write anywhere except `out_yaml` and `out_md`.

### ALWAYS
- Put a repair-lane candidate in the NBA slot when inconsistencies exist.
- Name the blocker on every blocked entry, verbatim from the candidate.
- Write explanations a person can act on without opening any yaml file.
- Carry `basis` (model_hash + derivation_hash) so the enforcer can pin the
  artifact to the exact state it was ranked from.
