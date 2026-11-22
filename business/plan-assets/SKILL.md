---
name: plan-assets
description: "Resolve and produce every production asset required by an approved storefront page plan. Searches real media first, manages user choices and uploads, discovers generation capabilities dynamically, persists outputs, and returns verified slot bindings."
---

# Resolve Page Assets

Turn the approved plan's `## Asset requirements` into permanent, verified
production bindings. This skill owns asset inventory, selection, import,
upload, permitted generation/editing, provenance, and final slot status. It
does not change page strategy, final copy, or section order.

Read:

- the exact `PLAN_APPROVED` page plan;
- optional `VISUAL_DIRECTION_APPROVED` frames and decisions;
- the selected store context and theme;
- `references/asset-prep.md`.

If an asset decision requires changing a section, claim, offer, or copy,
return that decision to `/plan-page`.

Use exact Lexsis actions:

- `lexsis_catalog.get`;
- `lexsis_asset_library.search`;
- `lexsis_asset_select.select`;
- `lexsis_assets.view` and `lexsis_assets.capabilities`;
- `lexsis_asset_import.import`;
- `lexsis_asset_import.discover`, `lexsis_asset_import.import_batch`,
`lexsis_asset_import.import_status`: when the user points at a website, scan it,
let them pick, queue the batch, and poll until it finishes;
- `lexsis_asset_upload.upload`;
- `lexsis_workspace.credits`;
- `lexsis_drafts.asset_generate`.

Resolve unfamiliar schemas through exact router/action discovery.

## 1. Discover Available Capabilities

Inspect image-generation and image-editing tools available in the current
client. Do not assume a particular external tool exists and do not hardcode
provider names.

Build an internal capability matrix for:

- generation from text and reference images;
- background removal and transparent output;
- inpainting, outpainting, cleanup, and upscaling;
- identity-preserving compositing;
- aspect ratios and output resolution;
- cost, approval model, and output persistence.

Honor a user-selected available capability. Otherwise choose by the asset job
and production requirements. Use Lexsis capabilities as the fallback.

Before a paid batch, state the slots, operations, count, and known cost or
credit impact, then obtain explicit approval. If cost cannot be determined,
ask before execution.

## 2. Resolve Mobile Before Larger Screens

For every visual slot, establish the mobile output first:

1. Confirm the 390 layout, rendered size, aspect ratio, focal point, crop,
   quiet zone, and interaction overlays.
2. Record an explicit mobile pixel target. Full-width mobile imagery should
   normally be at least 1080px wide; other slots should target roughly 2x
   their maximum rendered CSS dimensions.
3. Select, edit, or generate the mobile asset first.
4. Derive the 768/1280 treatment from that approved mobile direction.
5. Reuse one master source with art-directed crops when it has enough image
   area. Produce a separate larger-screen output when portrait-to-landscape
   conversion needs extension, recomposition, or a genuinely different crop.

The larger-screen output preserves the mobile-approved subject, identity,
scene, lighting, palette, focal intent, and consumer job. For full-width
desktop imagery, target at least 1600px wide and prefer 1920px when the source
and capability support it.

## 3. Resolve Slots in Order

For every asset requirement:

1. Refresh the exact product and variant media through
   `lexsis_catalog.get`.
2. Search the Lexsis library by theme, role, tags, semantics, filename, OCR,
   or similarity as relevant.
3. View each meaningful candidate in the mobile crop first, then the
   larger-screen crop.
4. Check identity, job fit, resolution, quiet zone, palette, neighbouring
   slots, rights, watermarks, and baked-in text.
5. Bind one clear fit.
6. When several candidates materially change the direction:
   - call `lexsis_asset_select.select` with the relevant search terms and
     filters, then wait for the user's selection message;
   - when the user wants to choose in the Lexsis dashboard, construct:
     `https://app.trylexsis.com/workspaces/<workspace-id>/storefront/design-library?theme=<theme-id>&tab=assets`
     using the exact bound workspace and theme ids, present it as a clickable
     Design Library link, and wait for the selected asset ids or URLs;
   - otherwise present only the fit-reviewed candidates;
   - choose directly only when the user delegated the choice.
7. For a missing slot, offer the valid routes: merchant upload, supplied URL
   or attachment import, permitted generation/editing, or a plan revision.

Search and visual inspection always precede generation.

Never reuse example ids in the dashboard URL. URL-encode the bound ids, and
do not treat opening the dashboard as a completed selection.

## 4. Import and Upload

- Use `lexsis_asset_import.import` for exactly one supplied URL, image data
  with MIME type, or conversation-attachment collection.
- Use `lexsis_asset_upload.upload` only for the local-file upload UI, scoped
  to the selected workspace and theme. Opening the panel is not completion;
  wait for the user's uploaded-asset response.
- Without upload UI, request a URL or attachment and import it.
- View every imported or uploaded asset before binding it.

## 5. Produce Missing Assets

Follow `references/asset-prep.md` for:

- transparent product cutouts from real product media;
- quiet-zone backgrounds and responsive crops;
- real-product composites with identity-bearing pixels unchanged;
- decorative transparent elements, textures, and patterns;
- permitted campaign or editorial imagery;
- extension, cleanup, background replacement, and upscaling.

Official press, payment, certification, trust, or media marks require a
verified official source or merchant upload. Customer proof, results,
founders, staff, product identity, packaging, labels, shades, fit, and
included-items evidence remain tied to real authorized media.

Persist every external output in the Lexsis library through
`lexsis_asset_import.import` before it can become a page binding. Transient
external URLs never enter the final table.

After production, view the output beside its source references. Allow one
bounded repair when the issue is clear. After that, use another valid source
route, request user input, or mark the slot blocked.

Produce or prepare the mobile output first. Then derive or produce the
larger-screen output from the approved mobile direction. Verify both sizes
before binding the slot.

## 6. Final Binding Record

Return:

```markdown
## Asset bindings

| Slot | Section | Source type | Product/media or asset id | Mobile URL / crop / pixels | Larger-screen URL / crop / pixels | Derivation | Rights/provenance | Generated/edited | Status |
|---|---|---|---|---|---|---|---|---|---|
```

Source type is `shopify`, `lexsis-library`, `merchant`, `supplier`,
`licensed-stock`, or `generated-and-imported`. Record the original source and
licence/approval basis even when the final file lives in Lexsis.

```markdown
## Asset production record

| Slot | Operation | Capability used | Source references | Cost approval | Output asset id | Verification |
|---|---|---|---|---|---|---|
```

Use generic capability descriptions in user-facing records unless the user
needs the installed tool name for reproducibility.

## Status

- `ASSETS_READY`: every required production slot has a permanent verified
  binding;
- `ASSETS_PENDING_USER`: at least one slot needs a user choice, upload,
  approval, or merchant source;
- `ASSETS_BLOCKED`: a required right, evidence source, identity image,
  product media item, or suitable capability is unavailable.

Report each unresolved slot with one next action. `/design-page` may begin
only with `PLAN_APPROVED` and `ASSETS_READY`; optional visual concepts remain
design evidence, never production assets.
