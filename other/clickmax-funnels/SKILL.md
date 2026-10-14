---
name: clickmax-funnels
description: Use when the user wants to create, inspect, change, publish, deactivate, delete, or analyze a Clickmax funnel graph.
---

## When this applies

Use this skill when the user wants to operate a Clickmax funnel: inventory it, create/edit graph nodes, connect triggers/pages, validate, publish, deactivate, delete, or inspect analytics.

Not this skill:

- Funnel step backed by an EXTERNAL page (URL hosted outside Clickmax, e.g. the user's own site/domain) -> STAY here: compose the granular tools (see the external-page common flow below). Never use `pages_create` for an external URL — that makes an empty INTERNAL page.
- Script-install help for an EXISTING external page (no graph change) -> `clickmax-external-pages`
- Lead/payment cohort analysis inside a funnel -> solve that with the relevant sales/CRM skill first
- Full AI-authored funnel with responsive page copy/design -> stay here and follow [AI funnel creation](references/ai-funnel-creation.md); load `clickmax-pages` alongside it, because that skill owns everything that happens inside a single page.
- ONE page, with no funnel graph involved (create, restyle, rebuild, configure, publish a single page) -> `clickmax-pages`
- Fine-grained visual edits after creation (moving one block or changing one mounted element) -> page editor UI.

## Discovery before authoring

For AI-authored pages, read [AI funnel creation](references/ai-funnel-creation.md) and load `clickmax-pages` before mutation. Guided discovery is the default for missing proof, people/assets and delivery links; “use the platform default design” does not skip it. Reuse supplied facts, accept an explicit skip, and continue an already requested draft after answers without another assembly approval.

## Build completion rule (mandatory)

- ONE build = ONE funnel. Call `funnels_create` exactly once. If a later step fails, validation is dirty, or the graph looks wrong, FIX the existing `funnelId` in place — re-run only the specific failing `funnels_node_create`/connect/`funnels_abtest_variants_update` — NEVER call `funnels_create` again to "start over". Retrying by re-creating leaves duplicate funnels (and if you also publish each attempt, several live funnels with the same name). If a prior attempt already left a half-built funnel, delete it with `funnels_delete` (or reuse it) instead of stacking another.
- Do NOT publish until the build is complete and `funnels_validate` is clean and the user asked to go live — never publish an attempt you might abandon.
- Creating nodes is only half the job. A funnel build is incomplete until its nodes are routed.
- After creating page nodes you must connect them with `funnels_triggers_connect` and, for non-page node families, with the type-specific tool (`funnels_abtest_variants_update`, `funnels_conditional_branches_update`, `funnels_traffic_source_update`).
- Never end the turn with page nodes whose triggers still have no `target`: unrouted triggers show up as loose, disconnected nodes with no edges in the editor.
- Multi-node builds should do create + connect as one continuous workflow, not in stop-and-go calls that might stop before the connect step.
- Before reporting done: call `funnels_structure_get`, confirm every intended route has an edge, then call `funnels_validate`; if there are leftover `disconnectedTriggers` or `orphanNodeIds`, surface them instead of silently finishing.

## Key assumptions

- Scope = one workspace + one project; never ask for workspace id
- Funnel lifecycle = `draft` -> `published` -> `unpublished_changes` after graph edits -> republish, or `disabled` after deactivate
- Graph = nodes + embedded triggers/variants/branches/outputs depending on node type
- Trigger, branch, and variant ids are server-generated; always read them from create/structure output
- Manual node creation is not a stopping point by itself; after `funnels_node_create`, always finish the wiring step
- Funnel workflow nodes own the entry (page trigger feeding the flow) and exit (flow-membership end) of their linked flow — this is flow membership, not page routing; a workflow never forwards the visitor to a page. Do not also configure standalone flow triggers for that embedded automation
- `funnels_validate.valid` is not enough by itself; still inspect disconnected triggers, orphan nodes, and missing page links
- Delete tools are destructive and should be confirmed unless deletion was already explicit
- Connections define the visual flow: the builder arranges the funnel left-to-right by following routed edges. Disconnected nodes have no graph flow, so they tend to stack in the first column.
- One domain per funnel: the funnel serves every published node on its domain (`funnels_get.settings.domain`, else the project's public domain), and every next-step redirect opens there. A page with its own `domainId` inside a funnel on another domain → the visitor leaves the page's address on the next step. Page created for / linked to a funnel → same `domainId` as the funnel (`null` when the funnel has none)

- Read [lifecycle and safety](references/lifecycle-and-safety.md) when deciding between draft edits, publish, deactivate, or destructive delete.
- Read [node types and edges](references/node-types-and-edges.md) when choosing node types and the correct connection tool for each edge family.
- Read [templates and starters](references/templates-and-starters.md) when the user wants a standard funnel shape that maps to a sequence template.
- Read [AI funnel creation](references/ai-funnel-creation.md) when the user wants discovery, automatic decisions, or a full assembled funnel.
- Load the `clickmax-pages` skill whenever a build has to produce page content. It owns the page authoring pipeline, the visual system, the section spine and copy, and the form/checkout/CTA/motion contracts; nothing here restates them.

## Thought process

1. Classify the request: read/list/analytics vs create/build/connect vs AI-authored funnel vs publish/deactivate/delete.
2. Resolve `projectId` and `funnelId` first.
3. Prefer template scaffolds for common funnel families; prefer manual graph creation only when the user describes a custom route.
4. Use `funnels_structure_get` as the canonical graph view before connecting, publishing, deleting, or diagnosing.
5. Keep graph wiring separate from page authoring: page nodes can exist before page ids are connected.
6. Always finish the wiring after node creation. A build that created nodes but skipped connecting them is not done.
7. Publish only after validation is clean enough and the user explicitly wants the funnel live.

## Execute guide

Use the tools in dependency order when later ids come from earlier results.

- Resolve the target project with `mcp__plugin_clickmax_clickmax__projects_filters` or list funnels with `mcp__plugin_clickmax_clickmax__funnels_list` when the project or funnel is not yet known.
- Read one funnel with `mcp__plugin_clickmax_clickmax__funnels_get`, passing the `funnelId`.
- Use `mcp__plugin_clickmax_clickmax__funnels_structure_get`, passing the `funnelId`, as the canonical graph view before wiring, publishing, deleting, or diagnosing.
- For a standard starter, create the funnel with `mcp__plugin_clickmax_clickmax__funnels_create`, then scaffold the graph with `mcp__plugin_clickmax_clickmax__funnels_sequence_create`. Set `objective` on create to the funnel's obvious goal (`capture` | `sales` | `scheduling` | `diagnosis`); it pre-configures the Analytics metrics. When you scaffold from a template, the objective + metrics are auto-derived — don't re-set them.
- For a custom graph, create nodes with `mcp__plugin_clickmax_clickmax__funnels_node_create`, then read back the generated trigger, branch, variant, or output ids before routing them.
- For page nodes or other trigger-based draft nodes, connect outgoing edges with `mcp__plugin_clickmax_clickmax__funnels_triggers_connect`.
- For A/B test nodes, route each variant with `mcp__plugin_clickmax_clickmax__funnels_abtest_variants_update`, giving every variant its OWN distinct page node in `connectedTo` (clone the base page once per variant with `mcp__plugin_clickmax_clickmax__pages_clone` first); two variants sharing one page is not a test.
- For traffic source nodes, route the output with `mcp__plugin_clickmax_clickmax__funnels_traffic_source_update`.
- For conditional nodes, route each branch with `mcp__plugin_clickmax_clickmax__funnels_conditional_branches_update`.
- When real page ids already exist, attach them to the correct page nodes with `mcp__plugin_clickmax_clickmax__funnels_node_connect_page` before publishing.
- Validate with `mcp__plugin_clickmax_clickmax__funnels_validate`, passing the `funnelId`, then re-read structure if you need to confirm every intended edge is present.
- Publish only when the user wants the funnel live: use `mcp__plugin_clickmax_clickmax__funnels_publish` with the `funnelId` and the node ids that should go live.
- Page-level operations on a linked editor3 page: publish a single page on its own with `mcp__plugin_clickmax_clickmax__pages_publish`, adjust its checkout/settings with `mcp__plugin_clickmax_clickmax__pages_update_config`, or duplicate it with `mcp__plugin_clickmax_clickmax__pages_clone` (e.g. to seed A/B variations from one built page).

Common flows:

- AI-authored funnel = follow [AI funnel creation](references/ai-funnel-creation.md) for the funnel half and `clickmax-pages` for the page half: guided or automatic discovery -> one brief -> one design for the whole funnel -> one draft funnel -> authored draft pages with `mcp__plugin_clickmax_clickmax__pages_import_html_draft` -> graph connections -> structure check -> validation. Never publish as part of automatic creation.
- Template funnel = use `mcp__plugin_clickmax_clickmax__funnels_create`, then `mcp__plugin_clickmax_clickmax__funnels_sequence_create`, then `mcp__plugin_clickmax_clickmax__funnels_validate`, then publish only if the user asked for it.
- Custom funnel = use `mcp__plugin_clickmax_clickmax__funnels_node_create`, then the correct connection tool for that node family, then `mcp__plugin_clickmax_clickmax__funnels_structure_get`, then `mcp__plugin_clickmax_clickmax__funnels_validate`.
- Go live with existing pages = use `mcp__plugin_clickmax_clickmax__funnels_node_connect_page`, then `mcp__plugin_clickmax_clickmax__funnels_validate`, then `mcp__plugin_clickmax_clickmax__funnels_publish`.
- Page WITH a checkout = `mcp__plugin_clickmax_clickmax__pages_templates_list` (`type: ["checkout"]`, pick `canUse: true`), then `mcp__plugin_clickmax_clickmax__pages_create` (`type: "checkout"` + `templateId` + `offerId` + `funnelId`) so the offer is auto-bound to the checkout, then `mcp__plugin_clickmax_clickmax__funnels_node_connect_page` to link it. See [pages and checkout](references/pages-and-checkout.md).
- Step that sells through the workspace's Whop, Hotmart, Stripe or Pagar.me account = an `external_checkout` node (`config.provider` `whop`|`hotmart`|`stripe`|`pagarme`) + a page built with `externalCheckout` of the same provider, linked with `mcp__plugin_clickmax_clickmax__funnels_node_connect_page`. Start with `mcp__plugin_clickmax_clickmax__external_checkout_accounts_list`; its `setup` not null (not connected / incomplete) → relay the instructions and stop before creating the node. See [pages and checkout](references/pages-and-checkout.md#whop-or-hotmart-checkout-step).
- Funnel step is an EXTERNAL page (the user gives a URL hosted OUTSIDE Clickmax — their own site/domain/landing) = compose these granular tools in order (NEVER `pages_create` — that makes an empty INTERNAL page):
  1. `mcp__plugin_clickmax_clickmax__pages_create_external` (`projectId` + `externalUrl` + `name` + `type`) -> returns the `pageId`. `projectId` = the FUNNEL's project; a page from another project is refused at connect time.
  2. `mcp__plugin_clickmax_clickmax__funnels_node_create` (`funnelId`, `type: "page"`, a `slug`, `pageType`, and `triggers` = one `contact_captured` + one `undefined`) -> returns the page node id.
  3. `mcp__plugin_clickmax_clickmax__funnels_node_connect_page` (`funnelId` + `nodeId` + `pageId`) — linking an EXTERNAL page auto-wires `node.config.externalUrl`, so the funnel 302-redirects visitors to the URL and tracks them (no manual config needed). ONE page per node: repeat 2+3 per page (each page needs its OWN node).
  4. `mcp__plugin_clickmax_clickmax__funnels_triggers_connect` to route the `contact_captured` trigger to the next node (e.g. the thank-you page).
  5. `mcp__plugin_clickmax_clickmax__pages_get_external_script` (`pageId`) -> returns `headScript` (paste in `<head>`); for lead-capture + redirect snippets use the `clickmax-external-pages` skill references. The external page does NOT track or advance until `headScript` is installed.
- Checkout page WITH order bumps = set them after the checkout page exists and is linked to its node, with `mcp__plugin_clickmax_clickmax__checkouts_set_order_bump`. Bumps ARE offers, so create them first with `mcp__plugin_clickmax_clickmax__offers_create`/`mcp__plugin_clickmax_clickmax__products_create`. Full parameter semantics are in `clickmax-pages`.
- A/B test across pages = the split only tests something if each variant resolves to a DIFFERENT page. Build the base page once (`mcp__plugin_clickmax_clickmax__pages_create` from a template), then `mcp__plugin_clickmax_clickmax__pages_clone` it once PER additional variant (each clone is a separate editable page); connect each page to its own page node (`mcp__plugin_clickmax_clickmax__funnels_node_connect_page`), create the `ab_test` node (`mcp__plugin_clickmax_clickmax__funnels_node_create`), and call `mcp__plugin_clickmax_clickmax__funnels_abtest_variants_update` with EACH variant's `connectedTo` set to a DIFFERENT page node id and the `percentage` split across them. The variant pages may reconverge downstream (e.g. all route on to one checkout), but their `connectedTo` targets must be distinct — never point two variants at the same page.
- Funnel WITH an embedded automation (e.g. "on lead capture, run an email automation") = build the capture page AND its page route (e.g. to the thank-you page) first, then call `mcp__plugin_clickmax_clickmax__funnels_workflow_automation_create` with `funnelId` + `projectId` + the capture page node id (`capturePageNodeId`, from `mcp__plugin_clickmax_clickmax__funnels_structure_get`) + a `title` (those four ONLY — there is NO next-page/connect parameter). That ONE atomic call adds the workflow node, wires the capture lead trigger into it as a PARALLEL side-effect (the trigger KEEPS routing the visitor to its existing page — nothing is disconnected), creates the flow, and links them (funnel-managed, shown in the canvas as a `workflow_input` edge). The workflow is TERMINAL: it does NOT forward the visitor onward, so never try to give it an outgoing edge or exit to "reach" the thank-you page — the visitor path continues from the page trigger's own route, in parallel. Idempotent per capture trigger: do NOT re-call it to "start over" (that stacks duplicate automations) — fix the existing one in place, or `mcp__plugin_clickmax_clickmax__funnels_node_delete` a bad attempt. It returns `flowId` + `entryStepId`; then add the message AFTER the entry with `mcp__plugin_clickmax_clickmax__flows_graph_apply` `{op:'add', type:'send_message', input:{…}, after:{step: entryStepId}}` (or a `mcp__plugin_clickmax_clickmax__flows_send_*` tool with `after: {step: entryStepId}`) — the entry step is the SOURCE; never pass `entryStepId` as the message's `target` (that wires the message back into the entry), then `mcp__plugin_clickmax_clickmax__flows_validate`. Only fall back to building it by hand (`funnels_node_create` type=workflow → `funnels_workflow_flow_set` → `funnels_triggers_connect`, in that order so the flow is linked before the trigger is wired) for a non-standard shape; never hand-set the flow's `funnelId` or its start triggers for an embedded automation.

- Full "capture + thank-you (+ email on capture)" build: resolve the project with `mcp__plugin_clickmax_clickmax__projects_filters`, create one funnel with `mcp__plugin_clickmax_clickmax__funnels_create`, and scaffold its capture and thank-you nodes with `mcp__plugin_clickmax_clickmax__funnels_sequence_create` using the `lead-magnet` template. For authored content, create each page with `mcp__plugin_clickmax_clickmax__pages_import_html_draft`; for a ready-made template, use `mcp__plugin_clickmax_clickmax__pages_create`. Connect each returned page id to its matching node with `mcp__plugin_clickmax_clickmax__funnels_node_connect_page`. For email, follow the embedded-automation recipe above using the capture node id from `mcp__plugin_clickmax_clickmax__funnels_structure_get`, then validate with `mcp__plugin_clickmax_clickmax__funnels_validate`. Publish only if asked.
- Read [templates and starters](references/templates-and-starters.md) to choose between `sales`, `lead-magnet`, `webinar`, `tripwire`, `vsl-auto`, and `upsell-downsell`.
- Read [node types and edges](references/node-types-and-edges.md) when deciding which connection tool owns each edge.
- Read [lifecycle and safety](references/lifecycle-and-safety.md#publish-checklist) before publishing, deactivating, or deleting.

## Report

- For reads: `name | id | projectId | status | publishedAt | node count | key problems`
- For create/build: return funnel id, discovery mode, assumptions, visual direction, created page/node labels, validation summary, factual gaps, and next action
- For publish: report whether the funnel went live, how many nodes were published, and any remaining manual element wiring
- For deactivate: explain that the funnel is offline, not deleted
- For analytics: summarize the main period metrics instead of dumping raw payloads
- Cap long node/trigger lists and prefer graph summaries
- After a create/publish that finishes the requested work, follow `clickmax-getting-started` to close with at most one opt-in offer of the next setup task.

## Warnings

- Resolve real `projectId`, `funnelId`, `nodeId`, `triggerId`, and `pageId`; never invent them
- Publish from fresh structure data, not stale ids captured before later edits
- `valid=true` can still hide non-blocking but important issues like missing pages or disconnected triggers
- API-created graphs may need visual rearrangement in the builder; do not promise tidy coordinates
- Use the correct edge tool for the node family (`funnels_triggers_connect`, `funnels_abtest_variants_update`, `funnels_traffic_source_update`, `funnels_conditional_branches_update`)
- `funnels_node_connect_page` rules, all refused server-side: target = `page`/`draft` node ONLY (never `ab_test`/`conditional`/`workflow`/`traffic_source`/`quiz` — connect THOSE to a page node instead) | page and funnel in the SAME project | one page per node, so a second call REPLACES the first and returns the swapped-out page in `replacedPageId` — read it before reporting two pages as linked
- `funnels_validate.nodesWithUnusedPage` = node carrying a page its type never serves (legacy link); the visitor never reaches that page
- "Lead doesn't reach the next page" / next step on an unexpected address → compare `pages_get.domainName` of each funnel page with the funnel domain before touching triggers; fix = align the domain (`pages_update` `domainId` or the funnel's domain) + republish, only with user approval
- For a `workflow` node, link its flow (`funnels_workflow_flow_set`, resolving `flowId` via `flows_list`/`flows_create`) and set its exit event (`funnels_workflow_exit_trigger_set`); a workflow without a linked flow does not fire automation and is flagged by `funnels_validate.workflowsMissingFlow`
- For a `workflow` node, configure entry/exit from the funnel side; flow-level start events are for standalone automations, not funnel-embedded flows
- Creating nodes without connecting them leaves a broken-looking graph: no routed edges and stacked nodes
- When the target project, product, or offer is ambiguous, ask the user to choose an existing entity or explicitly request a new one before mutation.
- Never fabricate factual proof or commercial facts while filling skipped discovery answers. Explicitly requested fictional testimonial samples follow the draft-only labeling and publication rules in `clickmax-pages`.

## Anti-patterns

- Asking for workspace id
- Using raw `funnels_get` as the only planning source when `funnels_structure_get` gives the compact graph view
- Connecting nodes by slug/label instead of real ids
- Creating page nodes and stopping before `funnels_triggers_connect`, leaving loose unrouted nodes in the editor
- Splitting create and connect across separate incomplete steps so the build stops before routing is finished
- Deleting a funnel when the user only wants it offline or paused
- Creating a BLANK page when the user wanted a checkout/sales page — start from a template (`pages_templates_list`) and pass `offerId` so the checkout is bound, instead of leaving an empty page
- Building an `ab_test` and pointing every variant's `connectedTo` at the SAME page (all the percentages bound to one page) — that splits traffic to one destination and tests nothing; clone the base page (`pages_clone`) once per variant and give each variant a distinct page node
- Connecting two pages to the SAME node and reporting both as added — the second silently replaced the first (`replacedPageId` says which); one node per page
- Retrying a failed/imperfect build by calling `funnels_create` again — it leaves duplicate funnels (all published/live if you also publish each try). One build = one funnel: fix the existing `funnelId` in place, or `funnels_delete` the broken attempt before restarting; never stack a fresh funnel on top of a failed one
- Creating page nodes BOTH ways in one build — `funnels_node_create` by hand AND `funnels_sequence_create` — leaves the manually-created nodes orphaned and forces a messy delete/reconnect cleanup. Decide the skeleton ONCE up front: for a standard family (capture→thank-you, sales, webinar, …) use `funnels_sequence_create` alone and connect pages to ITS nodes; use `funnels_node_create` only for a custom graph the templates don't cover — never both
- Treating a `workflow` as a step BETWEEN pages — it is a parallel side-effect with no visitor output, so giving it a `flow_completed`/`page_viewed` exit to "reach" the next page does nothing. On lead capture the SAME trigger routes the visitor to the page AND feeds the automation in parallel (`funnels_workflow_automation_create` keeps the page route); never re-point the capture trigger onto the workflow to add an automation — that used to disconnect the page

---

Clickmax skill revision: `b8294822a4d6`
