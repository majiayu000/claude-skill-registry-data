---
name: design-page
description: "Implement an approved storefront page plan with verified production assets. Authors canonical Lexsis source, creates or edits one unpublished hosted draft, performs hosted responsive and commerce QA, and returns DESIGN_APPROVED. Never plans, produces assets, or publishes."
---

# Design an Approved Page

Turn the approved specification into one verified unpublished Lexsis draft.
This skill owns implementation schemas, source, CSS, compilation, draft
creation or version-safe editing, hosted QA, and design approval.

## Required Inputs

Read:

- `work/storefront/setup.md`;
- the selected store's `brand.md`, `design.md`, `products.md`, `persona.md`,
  `rules.md`, and default theme CSS;
- the exact page plan with `PLAN_APPROVED <who> <date>`;
- the asset handoff with `ASSETS_READY`;
- optional `VISUAL_DIRECTION_APPROVED` frames and visual decisions;
- `references/design-authoring.md`;
- `references/hosted-design-review.md`.

Use exact Lexsis actions:

- `lexsis_brand.context`, `lexsis_brand.get_theme`, and
  `lexsis_brand.navigation` when the plan requires full navigation;
- `lexsis_catalog.get`, `lexsis_catalog.reviews`, and
  `lexsis_catalog.review_collection_items`;
- `lexsis_template_library.get_kit` and
  `lexsis_template_library.get_mine` only for directions selected upstream;
- `lexsis_design.get_section`, `lexsis_design.islands`, and
  `lexsis_design.island_schema`;
- `lexsis_build.push_token` plus `npx @lexsis/cli new` / `pull` / `diff` /
  `push` in CLI mode (the default, see `lexsis-mcp-contract.md` Write Path);
- inline mode only: `lexsis_build.commit` with `create` to make the draft,
  then `lexsis_build.get`, `patch`, `commit` and `diff` for every edit
  (last-resort fallback: `lexsis_pages.compile` then `lexsis_page_create.create`);
- `lexsis_pages.integrity` and `lexsis_pages.qa`;
- `lexsis_drafts.page_update_head` (page `theme_css`) and
  `lexsis_drafts.page_record_qa`.

Resolve unfamiliar schemas through exact router/action discovery.

## 1. Enforce the Handoff

Stop before implementation when:

- setup context or the selected binding is missing;
- the plan is blocked, awaits approval, or lacks final section copy;
- the asset status is `ASSETS_PENDING_USER` or `ASSETS_BLOCKED`;
- any required slot lacks a permanent verified binding;
- supplied concepts remain `VISUAL_DIRECTION_IN_REVIEW`;
- plan, asset, concept, store, or theme bindings disagree.

Return strategy, copy, offer, proof, claim, section, or template changes to
`/plan-page`. Return missing, unsuitable, inaccessible, or unverified media
to `/plan-assets`. The visual stage is optional; continue when it was never
used or was explicitly skipped.

Preserve the approved value argument, component explanations, mechanism
evidence, proof placement, and offer terms through copy, imagery, and section
order. Previously approved plans remain usable without the newer value-strategy
fields; do not require retroactive replanning for unrelated scoped edits.
Changing the argument or commercial terms returns to `/plan-page`.

An explicit `/design-page` request authorizes one unpublished page-creation
credit for the named page. It does not authorize another page, paid asset
work, publication, or live operations.

## 2. Refresh Implementation Facts

Confirm the live store and selected theme. Refresh every bound product and
variant used by commerce controls. Read live review data only for review
components already specified by the approved plan.

Stop and return to the owning stage when live data invalidates approved copy,
offer terms, claims, product availability, variant defaults, proof totals, or
asset identity. Do not silently rewrite the plan.

## 3. Resolve the Implementation

Follow `references/design-authoring.md`.

1. Apply the plan's design direction, selected theme, and optional approved
   visual decisions.
2. Resolve the selected page kit, section source, or saved merchant section.
   For a custom direction, author the source directly.
3. For each planned interaction, inspect the compact island catalogue and
   fetch the exact current schema only for the chosen island.
4. Bind only production assets listed in the `ASSETS_READY` table. Use their
   permanent URLs, crops, alt intent, and provenance decisions.
5. Place final plan copy verbatim. A wording change returns to `/plan-page`;
   responsive line breaks are implementation.
6. Render proof, claims, offers, urgency, inventory, prices, reviews, and
   policies only from their approved rows and refreshed live facts.
7. Author semantic source, scoped section styles, page-wide `theme_css`,
   required scripts, head data, and schema-valid islands.

When the plan's scope is a product or collection template, follow
`references/resource-templates.md`: pass `resource_type` at compile and
create, bind islands and text to the resource instead of one product or
collection, and review the hosted preview at the plan's sample handles.
Routing live URLs to the template is a separate approved live operation.

On a PDP or product template, bind reviews with `productIds` and never
hardcode a fallback collection in props. Apply the plan's review fallback by
passing `review_fallback` to `lexsis_page_create.create`, or
`lexsis_drafts.set_review_fallback` on an existing page; unset means store
reviews. Write the product and fallback headings as page HTML toggled by CSS
on `data-reviews-source` (snippet in `references/resource-templates.md`);
the island renders no fallback labels.

Concept images guide composition only. Their URLs never enter source or asset
bindings.

## 4. Compile Early

Compile the complete rough source before polishing isolated sections.

1. Treat `validation_errors` as the work list.
2. Resolve only the schemas implicated by planned behaviour or compiler
   findings.
3. Repair editable source and CSS, preserving section ids and approved copy.
4. Recompile until blocking errors are clear.
5. Retain the clean compile id, input hashes, and bundle hash.

The compiler is the compatibility authority. Do not patch compiled output or
replace unsupported interactions with unverified custom behaviour.

## 5. Create or Update One Draft

For a new page in CLI mode, write the files into a folder and run
`npx @lexsis/cli new ./page --slug <slug> --theme <theme_id> --dry-run`, then
again without `--dry-run`, with a create-only token from `lexsis_build`
`push_token` (no `page_id`). Pass the store header and footer ids as
`--shared <id,id>` and a similar page as `--from <page_id>`. Inline (no
shell), call `lexsis_build.commit` once with no `page_id`, a
`create` object (`slug`, `title`, `theme_id`, plus `archetype`,
`product_binding` or `resource_type` when needed) and the page as files
(`lexsis.json`, `sections/<id>.html`, `styles/*.css`). Run it with
`dry_run: true` first: one call returns every diagnostic with file and line
and creates nothing. Pass the store header and footer ids from `setup.md` in
`shared_sections` so they are linked at creation. When a similar page or kit
page exists, pass it as `from` and send only the new or changed files. See
`page-editing.md`, New Page.

Fallback when `lexsis_build` is unavailable: `lexsis_page_create.create` once
with the clean `compile_id`, creation metadata and `publish:false`. Do not
combine `compile_id` with source, CSS, head, scripts or runtime dependencies.

Record the returned page id, version, hosted preview, compile evidence,
`DRAFT_CREATED`, `design.status: pending-approval`, and
`qa.status: pending`. Return the hosted preview immediately.

If the page already has an id, read its edit context and current source.
Reconcile unexpected version drift, compile the updated complete source, and
write the smallest source-based change with `expected_version`. Never spend a
second creation credit to fix or revise the same page.

## 6. Run Hosted Review

Follow `references/hosted-design-review.md` against the hosted draft at 390,
768, and 1280. Verify:

- fidelity to the approved plan, asset bindings, and optional visual
  decisions;
- responsive hierarchy, typography, spacing, media crops, accessibility,
  motion, and absence of generic design clutter;
- exact copy, proof, offer, claim, policy, and product treatment;
- island hydration and expected interaction;
- real variant, cart, quantity, subtotal, sold-out, navigation, header, and
  footer behaviour;
- no overflow, broken media, duplicated chrome, console errors, or unexpected
  layout shifts.

Save supported evidence through `lexsis_drafts.page_record_qa`. Fix findings
in the existing draft with version-safe source edits, then rerun the affected
checks. If browser evidence is unavailable, keep QA pending and return
`DRAFT_CREATED`.

## 7. Approve the Design

Show:

```text
Hosted preview: [url]
Draft: [page id] version [version]
Plan: PLAN_APPROVED [who, date]
Assets: ASSETS_READY [binding count]
Visual direction: [approved | skipped | not used]
Sections: [ordered ids]
Interactive components: [islands]
Hosted review: 390/768/1280 [passed | findings]
Commerce: [passed | findings]
Source and bundle hashes: [values]
```

After hosted QA passes and the user explicitly approves that reviewed version,
record `DESIGN_APPROVED <who> <date>` for the page id and version.

Any later visible source, CSS, copy, layout, island, or asset change returns
the design to `changes-pending-approval`. `/publish` must gate on the same
`DESIGN_APPROVED` version.

## Shared Sections

Read the `Shared sections` table in `work/storefront/setup.md`. Never rebuild a
header, footer, or entry pop-up that already exists as a shared section. On a
new page, pass the shared section ids as `lexsis new --shared`
(inline: `lexsis_build.commit` `shared_sections`); they are added and linked with no extra version. On an
existing page, link one with `lexsis_drafts.shared_section_sync` and
`page_ids`.

To change a shared section, edit it once with
`lexsis_drafts.shared_section_update`, or change only island props or one
exact CSS/JS snippet with `lexsis_drafts.shared_section_patch`; both reject a
source no page could compile. Then run
`lexsis_drafts.shared_section_sync` without `page_ids`. Sync writes drafts, so
live pages change only after `/publish`. Pages in a running experiment are
skipped with `reason: "running_experiment"`; report them. Use
`lexsis_drafts.shared_section_detach` only when one page must diverge.

## Return

Return the page id, version, hosted preview, compile evidence, QA evidence,
sections, islands, and status:

- `DRAFT_CREATED` while hosted QA or user approval is pending;
- `DESIGN_APPROVED` only after hosted QA and explicit approval.

Never publish.
