---
name: photoshop-playbooks
description: "\"Use when the user asks what Manus can do with Photoshop or needs workflows for image batches, cutouts, retouching, composites, data-driven variants, reusable Actions, delivery exports, or Photoshop guidance. Routes each workflow by requested client and retained output state among Manus image tools, deterministic file processing, Photoshop Web in My Browser, and Photoshop Desktop through Computer Use.\""
compatibility: opencode
---

# Photoshop Playbooks (Manus for Photoshop)

Route by the state the user needs to keep, not by the word “Photoshop” alone. A good-looking image, an editable PSD, a clipping path, and a reusable Action are different products with different verification oracles.

## Step 0: Classify the retained output

```text
F1 STANDALONE IMAGE
   A new or semantically changed PNG/JPG is sufficient.
   Use Manus image generation or refinement when the current session exposes it.

F2 DETERMINISTIC FILE SET
   The job is measurable crop, resize, conversion, naming, compression, or exact
   template rendering. Use deterministic file processing after runtime preflight.

W1 WEB-EDITABLE PSD STATE
   The exact requested objects are supported in Photoshop Web and must remain
   editable. Use the authenticated Photoshop Web client through My Browser only
   after a representative PSD round trip proves the required state survives.

D1 DESKTOP-SPECIFIC PHOTOSHOP STATE
   A named desktop-only or web-limited object or behavior must remain: for example
   an Action, Variables setup, Pen/clipping path, installed plugin, or an explicit
   Photoshop Desktop lesson. Use Photoshop Desktop through Computer Use only after
   app/version availability and an observable saved postcondition are established.

A1 REUSABLE PHOTOSHOP AUTOMATION
   The retained product is an Action, Batch configuration, Variables template,
   droplet, or an approved Photoshop-hosted script. Name and test that asset; a
   Manus skill and a Photoshop Action are separate reusable artifacts.
```

“Editable,” “PSD,” “precise,” and “use Photoshop” do not by themselves prove that Desktop CU is required. If the user says Photoshop Desktop or asks to see the desktop app, preserve that client choice. If the user says only Photoshop, resolve Web versus Desktop from the required object and available client.

Read `formats/route-contract.md` before selecting a route and `formats/desktop_runtime.md` before My Browser or Computer Use.

## Step 0.5: Hard boundaries

- Use only assets the user owns or is authorized to modify.
- Do not forge records, identity documents, seals, evidence, or identity traits. ID-photo work is limited to specification-safe crop, size, background, dust, and conservative tonal cleanup.
- Preserve sources. Use a separate destination or copied project. Never choose a source-overwrite batch mode without separate explicit authorization.
- Local files are directly available only when attached, retrieved through a storage route, or inside a folder explicitly shared with Manus Desktop.
- Run Photoshop Desktop CU work serially. Another CU session may own the single desktop-control lease.

## Step 1: Routing map

| User outcome | Card | Read | Default route |
|---|---|---|---|
| Standardize a product or specification-safe ID-photo batch | 1 Product batch | `references/batch-production.md` | F2 geometry/naming; F1 semantic change; W1/D1/A1 only for a named retained object |
| Remove or replace a background | 2 Cutout | `references/retouch-cutout.md` | F1 standalone result; W1 ordinary editable mask; D1 clipping path or named desktop requirement |
| Retouch portraits against an approved reference | 3 Portrait retouch | `references/retouch-cutout.md` | F1 conservative result; W1/D1 only for required retained retouch state |
| Produce exact variants from structured data | 4 Data-driven variants | `references/batch-production.md` | F2 exact flat rendering; A1 Photoshop Variables when the reusable PSD system is required |
| Turn repeatable Photoshop steps into automation | 5 Action and Batch | `references/batch-production.md` | A1 through Photoshop Desktop; hold autonomous execution until the exact procedure passes live replay |
| Remove authorized objects or clutter | 6 Cleanup | `references/retouch-cutout.md` | F1 standalone repair; W1 supported retained repair; D1 named desktop-only state |
| Create text effects, posters, or composites | 7 Design and composite | `references/creative-guidance.md` | F1 visual concept; F2 exact flat text; W1/D1 for the required editable object graph |
| Create delivery variants | 8 Export pipeline | `references/batch-production.md` | F2 measurable exports; W1/D1/A1 only for a named app-specific requirement |
| Teach a Photoshop procedure | 9 In-app lesson | `references/creative-guidance.md` | Requested client; release one lesson only after its own fixture and live replay pass |

Read `formats/verification-manifest.md` before reporting completion.

## Step 2: Universal completion gates

1. State the requested client, selected route, and retained output before mutation.
2. Record source count and hashes where practical; use a separate destination or copied PSD.
3. For semantic or taste-sensitive work, approve a representative sample before scaling.
4. Verify with the oracle for the promised product. A good PNG does not prove a PSD, path, Action, or Variables deliverable.
5. Quarantine uncertain images and reconcile interrupted batches by manifest; do not silently accept partial output.
6. For My Browser or CU, re-observe the saved state after each meaningful transition. Input dispatch is not semantic success.
7. Report the exact retained artifact, unsupported state, skipped items, and remaining human review.
