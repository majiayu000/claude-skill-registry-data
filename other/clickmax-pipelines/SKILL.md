---
name: clickmax-pipelines
description: Use when the user wants to operate CRM pipelines, stages, opportunity cards, attendants, or pipeline analytics in Clickmax.
---

## When this applies

Use this skill for pipeline/stage/card operations: create or change pipelines and stages, move cards, assign attendants, inspect history/risk, import leads into pipelines, or read pipeline analytics/settings.

Not this skill:

- lead search and identity -> `clickmax-leads`
- manual tagging or segment/list membership -> `clickmax-tags` / `clickmax-list-segments`
- building or reading a saved Insights dashboard (opportunities, sales, messaging…) -> `clickmax-insights-dashboards`
- follow-up tasks and multi-step follow-up cadences on a card -> `clickmax-activities`

## Key assumptions

- stage/pipeline ids must be resolved before mutation
- stages have NO type: won/lost lives on the CARD `status` (`cards_update`; `lost` needs a reason), never on a stage, and moving a card never changes its status
- auto-assignment strategy changes who owns new/changed cards and should be treated as operational policy, not cosmetic text
- settings can include idle SLA threshold, lost reasons, default priority, temperature, currency, and card display fields
- some move paths may be blocked by stage passage rules
- delete semantics are soft-hide/remove-from-board at the backend level, but still user-visible destructive actions
- attendant assignment/settings writes replace current structures, not patch arbitrary fragments
- Every money amount here is an INTEGER IN CENTS — `cards_create`/`cards_update`'s `value`, `opportunities_bulk_set_value`'s `value`, `cards_list`/`opportunities_query`'s `valueMin`/`valueMax`, and `commissionFixedCents`. `19990` = R$ 199,90. Neither side divides or multiplies: a decimal like `199.90` is not "reais", it is a fifth of a cent. Commission PERCENTAGES are basis points instead (`525` = 5,25%).
- `cards_*` and `opportunities_bulk_*` act on the SAME thing — an opportunity card. The bulk family is not "the lead version" of the single-card tools; `opportunities_bulk_apply_tags` writes the exact same card↔tag link as `cards_apply_tags`, just over a whole selection. Tagging the CONTACT is a different domain entirely (`crm_tags_apply_to_leads`, see `clickmax-tags`).
- Bulk targeting is `cardIds` (an explicit non-empty list of CARD ids, max 200) OR `allMatching: true` with a `scope` `{ pipelineId, stageId?, filters? }` — mutually exclusive, one required, and never `opportunityIds`/`leadIds`. Sending both or neither is a 400; above 200 cards only `allMatching` works (async).
- `scope.filters` = the board filters of `cards_list` (search, attendants, products, funnels, status + temperatures, priorities, tags, contacts, companies, offers, origins, value range, closing-date range) plus the advanced `conditions` tree. A "select the whole column" request carries the filters the user has ON SCREEN, or the action hits more cards than they see. Sort order is irrelevant. Forecast cut, `cardIds` and `viewAsAttendantId` inside `filters` are a 400, not dropped.
- Four different "assign" verbs, do not mix them: `cards_update.responsibleAttendantId` / `opportunities_bulk_set_responsible` = who owes the NEXT ACTION (fixed | multiple rotation | team round-robin; management only); `cards_assign_attendants` / `opportunities_bulk_assign_attendants` = commission ROLES (replace, wipes the cards' previous roles and commissions; the bulk one writes NO commission); `opportunities_bulk_transfer` re-evaluates both against another pipeline.
- Bulk move/transfer skip the stage passage rules (WIP, required fields, direction) that `cards_move` obeys, and append cards at the end of the target stage. `opportunities_bulk_transfer` is management-only, needs a target stage of the target pipeline, and keeps responsible/roles only where the destination supports them (`keepResponsible`/`keepRoles`, default true); commissions are rewritten from the destination pipeline and are not restored by transferring back.
- Contacts (not cards) enter a pipeline through `cards_add_leads_to_pipeline` (selection of contacts; `mode: "new"` builds a 4-stage pipeline first) or `cards_import_from_lists` (lists/segments). Neither moves an existing card unless `moveExistingCards: true` (add-to-pipeline only): then a contact's OPEN card in that pipeline is dragged to the chosen stage, never backwards unless `allowMoveToPreviousStage`, and won/lost cards stay put. Segments always run async.
- The contacts of a card selection become a manual list with `opportunities_bulk_create_list` (ALL contacts of each card, deduplicated; the list exists at once, its `listId` comes back even when the fill is async).
- Flow triggers on cards: "entered a stage" also fires when a card is CREATED in the stage (not only on a move) and "left a stage" on a move out; build them as flow triggers or as a stage `managed_flows_upsert` (see `clickmax-flows`), not as `stage_automations_*`.
- Contact-level filtering of cards (name, city, e-mail, Temperature, Score, custom fields of the CONTACT…) goes in `conditions` through the `lead` node — a JSON string of contact filter items in `valueString`, described on `opportunities_query`. `cards_list` rows carry the primary contact Temperature/Score (`leadTemperatureScore`, `leadScore`).

- `id` means a DIFFERENT thing depending on the tool — same param name, no `pipelineId`/`stageId` alias to disambiguate. On `stages_list`, `stages_create`, and `stages_reorder`, `id` is the PIPELINE id (the stage itself is created/reordered by name/list, not addressed). On `stages_update` and `stages_delete`, `id` is the STAGE id. Do not assume it means the same thing across sibling tools — check which one before calling.

## Thought process

1. Resolve the exact pipeline/stage/card first.
2. Distinguish card mutation from pipeline metadata/settings mutation.
3. When moving or reordering, preserve board semantics and current anchors.
4. Confirm destructive changes when intent is not already explicit.

## Execute guide

- Resolve the board before writes: use `mcp__plugin_clickmax_clickmax__pipelines_list` to find the pipeline, `mcp__plugin_clickmax_clickmax__stages_list` with `id` (the pipeline id, not `pipelineId`) to map stage ids, and `mcp__plugin_clickmax_clickmax__cards_list` with `pipelineId`, `stageId`, pagination, and optional filters such as `search` or `tagIds` when the target card still needs disambiguation.

- Creating a NEW pipeline with its stages already defined (the common "create a pipeline with stages X, Y, Z" ask): pass the stages inline in `mcp__plugin_clickmax_clickmax__pipelines_create`'s optional `stages` array (`{name, color?, metaPixelEvent?}` per stage; there is no stage type — win/loss is the card status) instead of one pipeline call plus N separate `stages_create` calls. One call creates the whole board.

- Create cards with `mcp__plugin_clickmax_clickmax__cards_create`, passing the target `leadIds`, `pipelineId`, and `stageId`; include `value` and `attendantIds` only when the user wants those set at creation time. Do not guess a card-creation tool name outside pipelines — `cards_create` is the only one; there is no `pipelines_create_card`.
  - Brand-new/fictional contacts: create each one first via `clickmax-leads`'s `leads_create` (one call per contact, returns the new lead id), THEN batch them into `cards_create` calls using that pipeline's `pipelineId`/`stageId` and `leadIds: [<the returned id>]`.
  - EXISTING contacts (e.g. "pegue os últimos N leads e adicione na pipeline X"): this is a TWO-DOMAIN task — resolve the leads first via `clickmax-leads`'s `leads_search` (no special sort needed for "last N", see that skill), resolve the pipeline/stage via `pipelines_list`/`stages_list` here, THEN call `cards_create` once per resolved lead id with that `pipelineId`/`stageId`. Load both skills' guidance for this request — do not treat it as pipelines-only just because a pipeline is named.

- Change many cards at once with the `mcp__plugin_clickmax_clickmax__opportunities_bulk_*` family instead of looping the single-card tools: `opportunities_bulk_move`, `_apply_tags`, `_assign_attendants`, `_set_value`, `_set_priority`, `_set_temperature`, `_set_closing_date`, `_set_custom_field`, `_create_next_action`, `_delete`. Resolve the selection first (`mcp__plugin_clickmax_clickmax__cards_list` or `mcp__plugin_clickmax_clickmax__opportunities_query`), then send it as `cardIds`, or describe it once as `allMatching: true` + `scope`. Each call answers `{ mode: "sync", affected }` up to 200 cards, or `{ mode: "async", jobId }` above that — an async answer means NOTHING has happened yet; poll `mcp__plugin_clickmax_clickmax__opportunities_bulk_job_status` with that `jobId` before reporting the change as done.

- Write an opportunity custom field with `mcp__plugin_clickmax_clickmax__opportunities_bulk_set_custom_field` — `customFieldId` from `mcp__plugin_clickmax_clickmax__custom_fields_list` with `entityType: "opportunities"`, and `value` raw for the field type (string for text/select, number for number, ISO string for date, boolean for boolean, string array for multi_select; `null` clears it). Only `text`, `number`, `date`, `boolean`, `select` and `multi_select` can be written in bulk — every other type (`currency`, `textarea`, `link`, `percentage`, `radio`, `rating`, `file`, `formula`, `json`) is refused with a 400 `Custom field type "<x>" is not supported in bulk update`. For those, write per card via `mcp__plugin_clickmax_clickmax__cards_update`'s `customFieldValues`, or pick a supported type when creating the field.

- Move cards with `mcp__plugin_clickmax_clickmax__cards_move`, passing the card `id`, the destination `stageId`, and the current relative anchor (`beforeCardId` or `afterCardId`) so the board order stays intentional; include `lossReason` only when the move path requires or justifies it.

- Assign attendants in 2 steps: first read `mcp__plugin_clickmax_clickmax__pipelines_attendant_types_get` for the pipeline's valid attendant type ids, then write `mcp__plugin_clickmax_clickmax__cards_assign_attendants` with explicit `assignments` entries containing `attendantId`, `attendantTypeId`, and `isPrimary`.

- Import leads into a pipeline with `mcp__plugin_clickmax_clickmax__cards_import_from_lists` only when the user wants board population from list/segment cohorts rather than one-off card creation; use `mcp__plugin_clickmax_clickmax__cards_add_leads_to_pipeline` when the audience is a contact selection or filter (and when already-present contacts should be moved). Both answer async above 200 contacts (always for segments): poll `mcp__plugin_clickmax_clickmax__cards_import_job_status`, nothing is created before it finishes.

- Mass reassignment: read who is eligible with `mcp__plugin_clickmax_clickmax__attendants_list` (must be linked to the pipeline) and `mcp__plugin_clickmax_clickmax__teams_list`, then `mcp__plugin_clickmax_clickmax__opportunities_bulk_set_responsible` with `assignment` `{ mode: "fixed", attendantId }` | `{ mode: "multiple", attendantIds }` | `{ mode: "round_robin", teamId }`. The selection must sit in ONE pipeline. Report `affected` (round-robin leaves cards nobody can take unassigned and uncounted).

- Cross-pipeline mass move: `mcp__plugin_clickmax_clickmax__opportunities_bulk_transfer` with `targetPipelineId` + `targetStageId`; say beforehand what happens to roles and commissions, it is not undoable by transferring back.

- Brief an attendant before a call ("Raio-X da oportunidade") with `mcp__plugin_clickmax_clickmax__cards_insights`: deal snapshot, linked contacts with Temperature/Score, last 8 timeline entries (+ total). Its purchase numbers are the PRIMARY contact's only (zeros without sales permission); purchases list, funnels, messaging and members area are not there — use `leads_context` / `leads_xray` on the contact (`clickmax-leads`).

- Inspect card behavior with `mcp__plugin_clickmax_clickmax__cards_get` for one card, `mcp__plugin_clickmax_clickmax__cards_list_by_lead` for a lead's pipeline presence, `mcp__plugin_clickmax_clickmax__cards_history` for move/change history, and `mcp__plugin_clickmax_clickmax__cards_at_risk` for cards currently flagged as operational risk.

- Update structure only after resolving the exact target object: to add a stage to an EXISTING pipeline, use `mcp__plugin_clickmax_clickmax__stages_create` with `id` = that pipeline's id (not a `pipelineId` field, and not the new stage's id — the stage has no id yet); `mcp__plugin_clickmax_clickmax__stages_update`/`mcp__plugin_clickmax_clickmax__stages_delete` instead take `id` = the STAGE's own id, since those two target one stage directly. Use `mcp__plugin_clickmax_clickmax__stages_reorder` (`id` = pipeline id) to resequence. Use `mcp__plugin_clickmax_clickmax__pipelines_create`, `mcp__plugin_clickmax_clickmax__pipelines_update`, or `mcp__plugin_clickmax_clickmax__pipelines_delete` for pipeline changes.

- Treat settings and analytics as separate from board CRUD: read current configuration with `mcp__plugin_clickmax_clickmax__pipelines_settings_get` before `mcp__plugin_clickmax_clickmax__pipelines_settings_update`, use `mcp__plugin_clickmax_clickmax__pipelines_attendant_types_set` only when changing the pipeline's attendant-role structure itself, and use `mcp__plugin_clickmax_clickmax__pipelines_analytics` for performance/throughput answers rather than card-by-card inspection.

## Report

- For structural changes: report what changed, where, and the resulting status.
- When summarizing one specific created/read pipeline in a visual card, use the pipeline name as the large headline/value. Put stage count, opportunity count, active status, and similar board metrics in pills/secondary metrics instead of replacing the headline with counts.
- For card moves: report origin -> destination and any relevant status/owner effect.
- For analytics/risk: summarize the operational takeaway, not raw board payloads.

## Warnings

- Do not guess stage ids from names when several stages are similar.
- A bulk write that comes back `mode: "async"` has NOT been applied yet. Reporting "done" off that response is how a mass update gets silently lost — poll `opportunities_bulk_job_status`, and use `opportunities_bulk_job_history` to audit or recover a `jobId` that was not kept.
- Treat a tool result flagged as an error as a FAILURE even though the transport answered 200. MCP reports a failed tool call in the result envelope (`isError: true`, the message as text), not as a JSON-RPC `error` — a caller that only inspects `error` reads "Provide non-empty cardIds OR allMatching=true with scope" as if it were a successful write. Never count rows as written on a result you did not actually read.
- `cards_create` creates ONE card per call, even when `leadIds` carries several contacts — that is the multi-contact card, not a shortcut for N cards. For one card per contact, call it once per lead id.
- Card order uses relative positioning semantics; stale anchors can misplace cards.
- Importing from lists/segments (and add-to-pipeline by default) skips contacts that already have a card in the pipeline, whatever its status.
- `opportunities_bulk_assign_attendants` REPLACES roles and drops their commissions; re-set commission per card with `cards_attendant_commission_update`.
- A sync/async bulk answer for `opportunities_bulk_create_list` still carries the `listId` of a list that may be only partly filled until the job ends.
- If `leads_create` (or any write here) returns an empty/unexpected result for a contact you need the id of, do not silently skip it or fabricate an id — call `leads_check_duplicates`/`leads_search` (see `clickmax-leads`) to recover the real id before using it in `cards_create`, or surface the failure instead of creating a card with no lead.

## Anti-patterns

- Treating pipeline settings as harmless cosmetic edits.
- Moving cards without checking destination stage semantics.
- Using card deletion when the user only wants to hide/archive operationally.

---

Clickmax skill revision: `b8294822a4d6`
