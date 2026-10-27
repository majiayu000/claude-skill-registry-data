---
name: sweep-labs
description: >
  Find orphaned connect-labs workflows, pipelines, synthetic data, and solicitations and clean
  them up. Needs a live-set from sweep-live-set.
disable-model-invocation: false
---

# sweep-labs

Find connect-labs artifacts (workflows, pipelines, synthetic opportunities, solicitations, funds, reviews, responses) that no current opp references. Workflows, pipelines, synthetic opps, and **solicitations** have first-class delete/disable atoms in the labs MCP — deletable in the execute pass, **after the orchestrator's per-system human-confirmation gate** (see `agents/sweep.md § Human-confirmation gate`). The remaining LabsRecord-backed types (funds + standalone reviews/responses) are report-only by design until per-type atoms exist upstream. Reviews and responses cascade-delete with their parent solicitation, so they generally don't need standalone cleanup.

## Inputs

- Live-set file path from `sweep-live-set`.
- `LABS_MCP_TOKEN` and labs base URL (loaded via `connect-labs` MCP).
- Labs admin base URL: `https://labs.connect.dimagi.com`.
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is **report-only**: diff/score/render + return the recommended-action list; **no mutations** (no delete/disable). In `execute` it mutates only `approvedIds`. The human-confirmation gate between the two is the orchestrator's job — see `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact workflow/pipeline/synthetic/solicitation/update-link/quote ids the human approved in chat. Mutate nothing outside this set. A `force: true` delete of a solicitation with seeded responses is approved per solicitation, by name, never by a blanket approval.
- `programIds` (optional explicit argument) — labs program ids to audit for supply-chain records. Default: every `program_id` on a solicitation ACE's orgs own (Step 2), plus every `phases.execution-management.products.supply_chain.program_id` the live-set's runs carry.

## Products

- `ACE/_sweep/<timestamp>/labs-orphans.md` — human-readable triage report.
- `ACE/_sweep/<timestamp>/labs-orphans.yaml` — machine-readable `OrphanReport`.
- For approved orphan workflows: `workflow_delete` calls.
- For approved orphan pipelines: `pipeline_delete` calls.
- For approved orphan synthetic opps: `synthetic_disable` calls.
- For approved orphan solicitations: `delete_solicitation` calls (cascade-deletes reviews + responses; gated on cascade emptiness — connect-labs PR #197).
- For approved supply-chain items: `supply_chain_update_link_revoke` and `supply_chain_quote_void` calls.
- An **irreversible-records** section in `labs-orphans.md`: the supply-chain records labs keeps no delete for, listed for audit (§ "Optional labs track" below).

## Process

1. **Read the live-set** via `drive_read_file`.
2. **List labs inventory** using existing atoms:
   - `workflow_list`
   - `pipeline_list`
   - `list_solicitations` (each entry includes `program_id`, `status` and `is_public`). It returns every call ACE's organisations own, **unlisted (`is_public: false`) ones included**, plus every public call. No `program_id` is needed to see an unlisted call you own — that was a stale claim, refuted against the live schema in #3166. Pass `organization_id` per ACE org (`pm_org`, `nm_org`, `llo_org`) to scope the listing to ACE's own calls.
   - `list_funds`
   - `list_reviews`
   - `list_responses`
3. **Diff** against the live-set's labs buckets:
   - workflows → `liveSet.identifiers.labsWorkflowIds`
   - pipelines → `liveSet.identifiers.labsPipelineIds`
   - synthetic opps → `liveSet.identifiers.labsSyntheticIds`
   - solicitations/funds/reviews/responses → `liveSet.identifiers.labsRecordIds`
4. **Score** each orphan via `scoreLabsItem(item, liveSet)` from `lib/sweep-fingerprint.ts`. Pass each item's `name` AND its `description` (workflows, registries, cohorts) / `notes` (synthetic opps): a Phase 7 object carries its sweep handle `(synthetic, ace <opp>/<run-id>)` in whichever field no frame renders — a rendered object (programme report, opp report, synthetic opportunity) has it in `description` / `notes`, never its name (`demo-data-setup` § C7 "Sweep handles", ace#2733). `sweepHandleField` checks all three and the score names the field and the run it came from. The scorer defensively downgrades to `low` when an item references a Connect opportunity that's still in `liveSet.identifiers.connectOpportunityIds` — that's a sign the caller mis-flagged the item.
5. **Build the `OrphanReport`** with `system: 'labs'`. Partition into:
   - **Actionable (deleted in the execute pass, after human approval):** workflows, pipelines, synthetic opps, orphan solicitations. Solicitation deletion is gated on `responses + reviews == 0` (cascade emptiness), not on lifecycle status — every ACE dogfood solicitation passes that gate cleanly because no real LLO ever engaged. See connect-labs PR #197.
   - **Informational only:** funds, standalone reviews/responses (reviews+responses that were already cascade-deleted with a parent solicitation don't appear here). Funds may need their own per-type atom in a future labs MCP release; reviews/responses generally cascade with their parent solicitation.
   - **Supply-chain items (optional labs track):** active update links, and quotes that are neither awarded nor voided, in a program that is orphaned or whose run has closed — see § Optional labs track.
6. **Render** + write `labs-orphans.md` and `.yaml` to the sweep folder, including the irreversible-records section.
7. **Recommend — stop here in `mode: recommend`.** Return the structured recommended-action list (orphan workflows/pipelines/synthetic to delete-or-disable; orphan solicitations to delete with their cascade preview — each with id, confidence) plus the informational-only items (funds, standalone reviews/responses) and the report Drive link, to the orchestrator. **Perform no mutations.** Do not try to prompt the human from this skill — a dispatched subagent can't reach them; the orchestrator runs the confirmation gate (see `agents/sweep.md § Human-confirmation gate`).

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` + `approvedIds` (the ids the human approved in chat). Mutate **only** those ids:

- Orphan workflows → `workflow_delete({ workflow_id })`
- Orphan pipelines → `pipeline_delete({ pipeline_id })`
- Orphan synthetic opps → `synthetic_disable({ synthetic_opp_id })`
- Orphan solicitations → `delete_solicitation({ solicitation_id })` (`program_id` is "accepted for compatibility; not needed" in the live schema). The atom cascade-deletes the solicitation's reviews and responses in one call and returns the count of records deleted at each level — surface that in the result so the human sees the cascade impact. Pass `force: true` only for the rare legitimate destroy-with-engagement-data case (test fixtures that intentionally include responses) — and only if the human explicitly approved that override.

- Approved update links → `supply_chain_update_link_revoke({ program_id, link_id, source: { ref: "ace:sweep:<timestamp>:update-link:<link_id>" } })`. It stops working at once and cannot be re-enabled; what was recorded through it stays.
- Approved quotes → `supply_chain_quote_void({ program_id, quote_id, reason: "ACE sweep <timestamp>: simulated run <run-id> closed", source: { ref: "ace:sweep:<timestamp>:quote:<quote_id>" } })`. The quote stays readable and drops out of comparisons.

Funds, standalone reviews/responses and every irreversible supply-chain record are never mutated (report-only). Return the per-item result.

## Optional labs track (`--with labs_e2e` runs)

A run with the optional steps on (spec `docs/superpowers/specs/2026-10-18-optional-labs-e2e-steps.md`) leaves three kinds of labs objects behind, each with a different cleanup:

1. **Private solicitations with seeded responses.** `solicitation-seed-responses` files fictional respondents (names end `[Synthetic]`, the run's roster lists them). Because the call then HAS responses, `delete_solicitation` refuses it without `force: true`. Recommend it as a per-solicitation `force` delete, with the cascade preview, and say the responses are ACE-seeded fixtures. The human approves the override for that solicitation by name. A solicitation with any response NOT on the run's seeded roster is real engagement data: report it, never recommend `force`.
2. **Removable supply-chain items.** For each program in `programIds`: `supply_chain_update_link_list({ program_id, include_inactive: false })` → recommend revoking every active link of an orphaned or closed run; `supply_chain_quote_list({ program_id })` → recommend voiding every quote that is neither awarded nor already voided, on a tender no live run still has open. These are the only supply-chain removals labs offers.
3. **Irreversible records — report, never act.** Labs keeps no delete for tenders, quotes, awards, contracts, shipments, consignments, receipts, invoices, payments, stock counts or distributions (spec § F6), and a declared **programme runner** can only be changed by that runner's admins or support, never removed. For each program, list counts from the matching `supply_chain_*_list` reads and `supply_chain_programme_runner_get`, each with the run that wrote it. The isolation for these is the program itself: they are scoped to ACE's own program, named "simulated", and stay there for audit.

**Known ACE-made items as of 2026-10-18**, so the first sweep after them reads them right rather than flagging them as strays:
- Private call **1000003** on program 308 (owned by `connect_orgs.pm_org`), closed, with seeded responses **1000046–1000049**: the PR4 live probe (#3176). Deletable: recommend `force: true` with the cascade preview.
- Program **308**'s runner declaration (`connect_orgs.pm_org`'s labs org, 352): the live check of connect-labs #2605. Irreversible from ACE; report it. Nothing else was written to program 308's supply chain.

## Failure modes

- **Live-set path doesn't resolve:** abort with "Run `sweep-live-set` first."
- **Labs MCP returns 401:** `LABS_MCP_TOKEN` is expired; recommend `/ace:labs-token-mint` to rotate, then retry.
- **`workflow_delete` fails because the workflow has running tasks:** report the item as "in-use — needs manual review"; don't retry, don't abort the batch.
- **`delete_solicitation` refused (`FAILED_PRECONDITION` with response/review counts):** the solicitation has real engagement data — a real LLO filed a response or a review was created. Surface the counts in the chat output; do NOT pass `force: true` automatically. The operator decides whether to override.

## Why funds + standalone reviews/responses remain report-only

The labs MCP exposes per-type delete for solicitations because solicitations are the **lifecycle unit** for the audit-data ecosystem (reviews and responses are children that cascade-delete with their parent). The other LabsRecord types intentionally don't have per-type delete atoms because:

- **Funds** may have allocations + downstream allocation refs from responses. A future `delete_fund` atom would need similar lifecycle guards (and the labs team hasn't surfaced demand for one yet — funds tend to be reused across solicitations rather than created per-opp).
- **Standalone reviews/responses** (not cascade-deleted with a parent solicitation) are uncommon — if they exist as true orphans, they were probably created by a buggy producer and should be investigated rather than auto-deleted. Surface them for visibility.

If the labs team adds `delete_fund` upstream, this skill's coverage matrix entry flips automatically — the proxy is a pure forwarder so no ACE-side wiring is needed beyond updating Step 5/6/9 and `agents/sweep.md`.

## Related skills

- `sweep-live-set` produces the live-set this skill diffs against.
