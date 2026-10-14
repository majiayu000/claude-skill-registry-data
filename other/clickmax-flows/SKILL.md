---
name: clickmax-flows
description: Use when the user wants to create, inspect, change, validate, test, debug (executions, failures, retry), run for a list/tag/segment (manual runs), or activate/archive a Clickmax automation flow and its step graph, or asks which automation message a contact is on — including any request to send/create an email (or SMS/WhatsApp) message to leads, even one mentioning a checkout button or a custom visual/dark style (the flow email step's own template options, never a page).
---

## When this applies

Use this skill when the user wants to operate a Clickmax automation flow: list/find one, inspect its graph, create/edit/connect/delete steps, configure entry events, validate, test it with a real contact, investigate its executions (who is stuck/failed and why), retry or stop runs, run a published flow for a list/tag/segment/contacts now or on a date (manual run) and follow or cancel that run, answer which message of which automation a contact is on and what comes next, see which other automations are linked to a tag/stage/message, or change lifecycle mode. A one-off "create/send an email to my leads" request is this skill too — build a minimal flow with a `trigger` + `flows_send_email` step. Do NOT reinterpret it as a landing page: a checkout button, dark theme, or urgency tone the user asks for are the email template's CTA/colors/font (`flows_send_email`'s style params), never page markup.

Not this skill:

- Funnel page graph, offers, pages, traffic routing -> `clickmax-funnels`
- A page — even one the user calls "email" — that isn't sent as a message (a landing/sales page, a page to share a link to) -> `clickmax-page-editing`
- Building the cohort that will feed the flow -> resolve that with the relevant CRM/sales skill first, then come back to wire the automation
- Channel copy authoring in isolation -> create the message content first, then reference real ids here

## Key assumptions

- Scope = one workspace; never ask for workspace id
- Graph writes work while the flow is `draft`, `template`, or paused (`closed`); a paused flow stays paused after the edit. `active` → ask the user, pause with `flows_close`, then edit. Never edit `scheduled`/`archived`
- The graph is steps connected by each step output `target`; there is no separate edge object. Each visible step lists its `outputs[]` (`handle` + `target`) — handle vocabulary in [step types](references/step-types.md#output-handles)
- A message that waits for a reply (or a timeout) owns hidden helper steps; never target them — address the message's `invalid`/`timeout` handles instead
- The entry is a single `trigger` step; a flow has at most one trigger step
- Trigger start/exit events live at flow level (`triggerStart` / `triggerExit`), not inside arbitrary step fields
- Standalone flows use flow-level trigger events; funnel-embedded flows (`funnelId` set) are started/exited by funnel workflow nodes instead
- Two ways an automation relates to a funnel. (1) EMBEDDED — the funnel's `workflow` node owns it: link/create it from the funnel side with `funnels_workflow_flow_set`, which syncs the funnel's triggers onto the flow and makes it show in the funnel canvas. This is what "an automation linked to the funnel" means — build it from the funnels skill (create the funnel workflow node BEFORE the flow, then link). (2) STANDALONE SCOPED — an ordinary flow whose trigger is narrowed by a `funnelId`/`pageId` constraint; it reacts to that funnel's events but is NOT part of the funnel graph. Never hand-set a flow's `funnelId` or hand-craft funnel triggers — the funnel workflow node's link tool does that; setting `funnelId` alone leaves an orphan (list badge shows, funnel canvas empty)
- Step ids are server-generated; always read real ids from create output or `flows_structure_get`
- When the user is inside the flow builder, the currently-open flow (its `flowId` + every step with full content + the edges between them) is published to screen context under `flows3.builder`; read it before asking which flow/step the user means, and target edits at that `flowId`. If `selectedStepId` is set, that is the node the user has focused on the canvas — prefer it when they say "this step/node" or open the assistant from a node without naming one. The `labels` map resolves the entity UUIDs inside step inputs (tags, lists, products) to human names — read names from there so you never echo a raw UUID back to the user
- Destructive deletes require explicit confirmation unless the user already made deletion explicit

- Read [lifecycle and safety](references/lifecycle-and-safety.md) when deciding between draft edits, activation, closure, archive, or destructive delete.
- Read [step types](references/step-types.md) when choosing which step type/action/input shape fits the requested automation.
- Read [email authoring](references/email-authoring.md) before writing an email step's content — the default slot template only ever recolors, never truly restyles; a genuinely designed email needs `customHtml`.
- Read [WhatsApp templates](references/whatsapp-templates.md) before writing a WhatsApp step — free-form text only reaches contacts inside the 24h window, so every other trigger needs an approved template.
- Read [trigger events](references/trigger-events.md) when mapping user intent to flow entry events + constraints.
- Read [executions, testing and links](references/executions-and-testing.md) before running a test, retrying/stopping executions, diagnosing a failed or stuck run, or answering "which automations react to / feed this tag, stage or message".
- Read [manual runs and cadences](references/runs-and-cadences.md) before sending a published flow to a list/tag/segment/contacts, scheduling or cancelling that send, or answering where a contact is in an automation's messages.
- Read [examples](references/examples.md) when you need a concrete build/branch/inspect pattern.

## Thought process

1. Classify the request: read/list/inspect/validate vs create/edit/connect vs lifecycle/destructive.
2. Resolve `flowId` first. If `flows3.builder` screen context is present, use its `flowId` (the user is editing that flow); otherwise find an existing flow by name, or create one in `draft`.
3. Check whether the flow is editable before planning step writes.
4. Plan the whole change set (trigger → steps → wiring) and send it as ONE `flows_graph_apply` call; the next call only fixes what its result reports.
5. Prefer `flows_structure_get` (or `flows3.builder`) as the canonical graph view before editing, deleting, or diagnosing.
6. Activate only after validation passes and the user explicitly wants the flow running on real contacts.
7. To prove a draft works, run it once for the user's own contact (`flows_test_run_start`) instead of activating: a test is a REAL run for one contact, activation opens the flow to everyone.
8. To investigate what happened, go list (`flows_executions_list`) → one run (`flows_execution_get`) → fix the cause → only then retry.
9. "Send this automation to list/tag/segment X" on a published flow = a manual run: `flows_run_estimate` → confirm audience (and cooldown choice) with the user → `flows_run_start` → follow with `flows_runs_list`. Never activate a draft just to reach a list, and never build a new flow for a one-off send when a published one already does it.

## Execute guide

- Build AND every adjustment = `mcp__plugin_clickmax_clickmax__flows_graph_apply`: one call per change set, applied atomically with the canvas's own wiring rules. Read `mcp__plugin_clickmax_clickmax__flows_structure_get` (or `flows3.builder`) first and use each step's real `outputs[].handle`. Ops run in order:
  - `add` — new step with a `$ref` (e.g. `$welcome`) usable by later ops in the SAME call; `after: {step, handle}` inserts it on that output and the output's previous destination becomes the new step's main output (insert in the middle = one op, nothing drops); `capture: {timeoutMinutes?}` on a WhatsApp/Telegram/Instagram message makes it wait for the reply
  - `update` (input/action) | `connect` (`from` + `handle` → `to`) | `disconnect` | `remove` (`bridge` default true = predecessor reconnects to successor) | `move` | `setTriggers` (standalone flows only; same replace semantics as `flows_step_triggers_set`)
  - `layout`: default places new steps next to their predecessor; `'organize'` re-lays out the whole flow; `'none'` keeps positions
- Never create a step in one call and connect it in another — that leaves a loose step on the canvas the user is watching. Finish only when the result has `orphanStepIds = []` and `triggerWithoutOutput = false`; otherwise fix it in a follow-up `flows_graph_apply` before replying.
- New flow: `mcp__plugin_clickmax_clickmax__flows_create` → one `flows_graph_apply` (trigger + steps + wiring + `setTriggers`) → `mcp__plugin_clickmax_clickmax__flows_validate`.
- Messages inside `add` use the raw `send_message` input ([step types](references/step-types.md)). To insert ONE message alone, a `mcp__plugin_clickmax_clickmax__flows_send_*` tool with `after: {step, handle?}` is equivalent (per-channel schema). The other `flows_step_*` tools stay for isolated single-step edits.
- `category` (on `flows_create`/`flows_update`) is a FIXED ENUM, not free text — one of `atendimento`, `vendas`, `suporte`, `marketing`, `cobranca`, `onboarding`, `retencao`, `pesquisa`, `agendamento`, `qualificacao`, `feedback`, `notificacao`, `integracao`, `teste`, `outro`. Pick the closest match from this exact list; guessing a plausible-sounding word outside it (e.g. `recuperacao`) fails validation. It's optional — omit it entirely if none fit well.
- For an existing flow, check editability with `mcp__plugin_clickmax_clickmax__flows_get_mode`, inspect the current graph with `mcp__plugin_clickmax_clickmax__flows_structure_get`, apply only the needed ops in one `flows_graph_apply`, and validate again before any lifecycle change.
- Use `mcp__plugin_clickmax_clickmax__flows_update` only for flow metadata such as name/category; it does not edit the step graph.
- Read the valid `action` names and their `input` fields from `mcp__plugin_clickmax_clickmax__flows_actions_catalog`, and a `conditional`'s valid `statements[].type` and its fields from `mcp__plugin_clickmax_clickmax__flows_conditionals_catalog`, BEFORE writing any non-message step. These are the only authoritative sources for those shapes — the catalogs also mark `comingSoon` actions that cannot be used yet. Never guess an `action`, a `statement.type`, or an `input` key. An invented key inside an otherwise valid `input` is not rejected — it is simply never read by the engine (`removeFromOtherPipelines` on `assignOpportunity` is exactly this, written by the flows3 drawer and consumed by nobody), so the step reports created and configures nothing. The shapes worth memorizing (and the `assignOpportunity` `opportunityId` trap) are in [step types](references/step-types.md).

- Read the valid entry/exit events from `mcp__plugin_clickmax_clickmax__flows_triggers_catalog` before suggesting or setting a trigger — it returns each event's friendly `label`, `description`, and the `scopes` it can be narrowed by; pick the exact `eventName` and never invent one. See [trigger events](references/trigger-events.md).
- Change entry events with the `setTriggers` op (or `mcp__plugin_clickmax_clickmax__flows_step_triggers_set`), and send the complete `triggerStart` / `triggerExit` arrays that should remain on the flow.
- For a flow linked to a funnel workflow node, keep flow-level trigger arrays empty unless the user is intentionally converting it into a standalone automation; wire entry/exit from the funnel skill instead.
- Use `mcp__plugin_clickmax_clickmax__flows_list` to find candidate flows by name before asking for confirmation on ambiguous matches.
- Use `mcp__plugin_clickmax_clickmax__flows_structure_get` as the canonical graph view before connecting, deleting, or diagnosing steps — each step's `outputs[].handle` is the exact vocabulary `flows_graph_apply` accepts.
- Use `mcp__plugin_clickmax_clickmax__flows_validate` before activation and surface its `issues` (each has a `severity` and the `stepId` to fix — group errors before warnings; codes and meaning are in [executions, testing and links](references/executions-and-testing.md#validation-issues)) plus `hasEntryTrigger`, `danglingTargets`, `orphanStepIds`, `triggerWithoutOutput`, and `incompleteChannelSteps` (channel steps — email/telegram/WhatsApp — missing their sender id: `emailSenderSignatureId`, `telegramBotId`, or `gupshupAppId` under `numberStrategy: 'fixed'`), not just `valid`. Resolve any `incompleteChannelSteps` before activating — with `email_sender_signatures_list` / `channel_instances_list`, then `flows_step_update` — rather than retrying `flows_activate` unchanged: a channel step without a real sender id fails on every single send no matter what activation itself currently checks, so never treat a clean validation as a substitute for having resolved the sender at creation.
- For branching, connect each branch explicitly with the correct `handle` (`true` / `false` for conditionals); an unknown handle is rejected with the step's valid outputs — use one of those.

- WhatsApp steps are TEMPLATE-first. `mcp__plugin_clickmax_clickmax__flows_send_whatsapp` REJECTS `format: 'text'` unless `numberStrategy: 'context'`, because free-form text only delivers inside the 24h customer-care window and only a flow started by the contact's own inbound WhatsApp message guarantees that window is open. Every other trigger (funnel, tag, schedule, checkout) takes a template. Order to follow, cheapest first: 1) `mcp__plugin_clickmax_clickmax__gupshup_templates_list` for an existing `approved` template that already says what the user wants; 2) for a generic use case (OTP, order update, reminder), `mcp__plugin_clickmax_clickmax__gupshup_template_library_list` + `mcp__plugin_clickmax_clickmax__gupshup_template_library_create` — Meta pre-vetted, near-instant approval; 3) otherwise author one with `mcp__plugin_clickmax_clickmax__gupshup_templates_create`, show the exact copy to the user, and only then `mcp__plugin_clickmax_clickmax__gupshup_templates_submit`. See [WhatsApp templates](references/whatsapp-templates.md).
- Never stall the build waiting for Meta. A template still `pending` can already be wired into the step — create the automation, then tell the user plainly that WhatsApp starts sending once Meta approves the template (hours to days) and that everything else runs immediately.

- Minimal build pattern: [create -> trigger -> action](references/examples.md#create-trigger-action)
- Linear automation pattern: [trigger -> delay -> send_message](references/examples.md#trigger-delay-message)
- Branch pattern: [conditional -> true/false branch](references/examples.md#conditional-branch)
- Adjustments: [insert in the middle](references/examples.md#insert-in-the-middle) | [swap two steps](references/examples.md#swap-two-steps) | [message that waits for a reply](references/examples.md#message-that-waits-for-a-reply)
- Read-only diagnostics: [inspect -> validate](references/examples.md#inspect-and-validate)

## Report

- Write every user-facing reply in plain business language: use entity **names** (never UUIDs), never show code, tool names, or internal field names (`triggerStart`, `triggerExit`, `eventName`, `tagId`). Those are for your own reasoning, not the reply — e.g. say "this flow now starts when the **VIP** tag is applied", not the event name or id.
- For list/find: compact candidate table (`name`, `mode`, `category`), not full raw graph dumps
- For create/build/edit: confirm what changed in user terms (which trigger, which steps, what happens next) — not step ids or edge internals
- When summarizing one specific created/read automation in a visual card, use the automation/flow name as the large headline/value. Put node count, status, channel mix, and similar build metrics in pills, sub-metrics, or `value-suffix`, not as the main headline.
- For validate: always surface the `issues` list (errors first, then warnings, each pointing at the node in user terms), `hasEntryTrigger`, `danglingTargets`, `orphanStepIds`, `triggerWithoutOutput`, and `incompleteChannelSteps`, even when `valid=true` (warnings never flip it). When `incompleteChannelSteps` is non-empty, say plainly that the listed message step(s) have no real sender configured (which channel/step, in user terms — never the raw field name) and that the flow will not deliver until that's resolved, then offer to fix it (list the workspace's numbers/bots/sender signatures and set the one the user picks)
- For executions: lead with counts by status and the top failure reasons in plain words (never raw error JSON), name the affected contacts, cap the list (`+N more`), and offer retry/stop as an opt-in next step with the exact number of contacts it touches
- For lifecycle: explain the new mode in user terms (`active` = processing real contacts; `closed`/`archived` = stopped)
- Cap long step/edge lists; summarize rather than dumping giant payloads
- After a create/publish that finishes the requested work, follow `clickmax-getting-started` to close with at most one opt-in offer of the next setup task.

## Warnings

- `flows_create` needs a real `projectId`; resolve it, never invent it
- `flows_update` is metadata-only and does not edit the graph
- `flows_delete` removes the flow and all steps permanently
- `delay` / `timeout` numeric `when` values are hours, not minutes or days
- `flows_step_triggers_set` edits the entry/exit events independently: send only the side you are changing (`triggerStart` or `triggerExit`) and omit the other to keep it; an explicit `[]` clears a side, and the array you do send replaces that side. Use the exact `eventName` from the [trigger events](references/trigger-events.md) catalog — an unknown/guessed name silently never fires. Scope with the entity id the catalog lists for that event (e.g. `tagId`, `offerId`)
- Conditional, `collect`, and `timeout` branches depend on correct `handle` wiring; missing branch targets usually show up as dangling targets or orphaned paths
- Unknown `action` names or wrong `input` shapes are rejected; fix the payload, do not assume partial success
- `gupshup_templates_submit` sends the template to Meta for review — external and practically irreversible (a rejected or low-quality submission affects the number's quality rating). Confirm the exact final copy with the user before calling it; never submit content you authored on your own, and never submit "to see if it passes".
- `gupshup_templates_create` validates the template against Meta's rules before saving and returns EVERY violation at once. Fix them all in the next call instead of retrying the same payload — the error text says what to change.
- Message personalization uses single-brace lead tokens — `{name}`, `{email}`, `{telephone}` — never `{{name}}` or `{{lead.name}}`; an unknown/misformatted key is delivered to the lead literally. Use them as fact, do not ask the user which format applies (GupShup/WhatsApp templates are the only exception: positional `{{...}}` `paramMapping`). See [step types](references/step-types.md).
- Never echo a raw UUID to the user. Step inputs store tags/lists/products by id; resolve them to names via the `flows3.builder` `labels` map (or the matching `clickmax-tags`/list/product lookup tool when an id is absent from `labels`). A UUID in your reply is a bug — report "the tag **Black Friday**", not its id.
- `flows_test_run_start` is NOT a dry run: it sends real messages, applies tags, spends credits and counts in the flow's metrics. Only with the user's explicit go-ahead, naming the recipient; default to the user's own contact
- `flows_run_start` is a REAL mass send to the whole audience; cancelling the run (`flows_run_cancel`) only stops what has not gone out — contacts already reached keep going through the flow. Confirm the audience size before starting and never start a second run to "retry" a run that is still `running`
- `flows_execution_retry` / `flows_executions_retry_by_error` re-run the failed node INCLUDING its side effect (the message is sent again, possibly to many contacts); retrying without fixing the cause fails again. `flows_execution_cancel` is permanent for that run
- Never wire a step's output (a `connect` op, `flows_step_connect`, or an inline `target`) back to the flow's `trigger` step id. The trigger is the entry point only; any step pointing back at it makes the worker reprocess the automation from the start forever (infinite loop). The backend rejects this with a 400 — treat that error as confirmation the graph you were building was wrong, not something to retry.

## Anti-patterns

- Asking the user for workspace id or a hidden platform id
- Guessing `flowId` or step ids instead of resolving them
- Editing an `active` flow without asking + pausing it first (`flows_close`), or editing a `scheduled` one at all
- Creating a step and connecting it in a later call, or spreading one adjustment over several calls — use one `flows_graph_apply`
- Replying "done" while the last result still has `orphanStepIds` or `triggerWithoutOutput = true`
- Treating `valid=true` as publish-ready while ignoring dangling targets or orphan steps
- Activating a flow without explicit user intent to start real processing
- Creating a second flow to retry after a step/connect/trigger error — keep editing the same `flowId` and fix the failing call; recreating leaves duplicate half-built automations
- Guessing a trigger `eventName` (e.g. `contact_captured`) instead of reading the exact one from `flows_triggers_catalog` first
- Guessing an `action` name, a `conditional` `statements[].type`, or an action's `input` keys instead of reading `flows_actions_catalog` / `flows_conditionals_catalog` first
- Passing an opportunity/card id as `assignOpportunity`'s `opportunityId` — that field is the PIPELINE id
- Writing a `delay` with a unit field (`{ type: 'days', when: 3 }`); there is no unit, a numeric `when` is always HOURS
- Hand-setting a flow's `funnelId` (or hand-crafting funnel triggers) to "link" it to a funnel — an embedded automation is linked from the funnel's `workflow` node via `funnels_workflow_flow_set` (funnels skill); `funnelId` alone leaves an orphan (badge shows, funnel canvas empty)
- Connecting any step's output back to the `trigger` step id — infinite loop, always rejected by the backend
- Presenting a test run as a simulation, or retrying/stopping executions without saying how many contacts are affected
- Starting a manual run without first showing the user the audience size from `flows_run_estimate`, or quoting its cost as exact
- Retrying failures in bulk before reading the cause (`flows_execution_get`) and fixing it
- Answering "which automations use this tag" from memory instead of `flows_link_targets_list` / `flows_link_sources_list`

---

Clickmax skill revision: `b8294822a4d6`
