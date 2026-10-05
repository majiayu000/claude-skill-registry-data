---
name: opc-carousel-creator
description: Create an on-brand Oak Park Construction Instagram post/carousel (before-after, project progress, product tip) from photos or a topic. Use whenever Priscila asks to make/create an OPC post, carousel, or before/after. Loads the OPC design system FIRST — never improvises design.
---

# OPC Carousel Creator

**Trigger:** "make/create a post/carousel/before-after" for Oak Park Construction, with photos or a topic.
**Never** start designing from imagination. This skill exists because a session once invented a navy/orange "brand" — that must never happen again.

## Reference-loading order (MANDATORY, in this order, before any design work)
1. `docs/OPC_DESIGN_SYSTEM.md` in `priihigashi/oak-park-ai-hub` (fetch via `~/bin/gh api` if repo not local) — tokens, fonts, layout rules, template list, folder routing
2. `scripts/content_creator/opc_template_catalog.json` — pick the template by purpose/good_for (progress/proof → `opc_progress.html`; tips → `opc_tip.html`; never invent a layout)
3. CONTENT_FORMATS Drive doc `1XqXSyJC_iHMTrmMxpM5ZR7S-WQxz19HhDJO1HomdncM` — check if a registered FORMAT applies
4. The target Drive folder — in the **Marketing SHARED drive** (`0AIPzwsJD_qqzUk9PVA`) → Content → (Proof Posts `1R4p51rUyGSfgf5VMgFKjQVXl5A399_QI` / Carousel `16P2JN74JAAW3HKnmNqPGPrAq7N5jDNii` / Manual Posts `1NoWWdL9s9mIoevloioCceUKFnW6ncRFa`); never My Drive, always supportsAllDrives=true — prior builds for version numbering (`vN_proof-<slug>`)

## Workflow
1. **Intake**: photos (which is before/after?) + one-line description. Category: Talking Head (→ video pipeline, not this skill) / Progress-Before-After / Product Tip.
2. **Clean photos**: PIL re-save strips EXIF/GPS (`Image.open → exif_transpose → resize ≤1440w → save JPEG q90`). Never send GPS-tagged originals anywhere.
3. **Adapt the real template** (fetch `docs/templates/opc_<x>.html` + CSS + fonts from the repo): fill the slide spine with real copy — plain contractor voice, no promises/fake stats, NO invented names/addresses/dates/crew/project-IDs, hook <10 words. Fill or remove every image slot — no dashed placeholders in a real post.
4. **Review gate BEFORE rendering**: run `/opc-carousel-reviewer` checklist against the HTML drafts.
5. **Render 3 variants** (the template's own v1 dark / v2 cream / v3 lime-on-dark) via Playwright/headless Chromium at 1080×1350, screenshot each `.slide` element. NEVER text-to-image AI.
6. **Open renders for Priscila** (`open` folder) → she picks a version → finalize caption (150-200 chars + hashtags ≤30).
7. **Archive to Drive** (needs her permission-prompt approval for file transfer on this Mac): `Proof Posts/vN_proof-<slug>/` with `png/`, `html/`, `originals_used/` subfolders per convention. Update Library Index/Sheet row if a new folder was created.
8. **Deliver Buffer package**: file list in slide order + approved caption. Never publish/schedule without her explicit approval.

## Done check
- 3 variants rendered from an approved template, reviewer checklist passed
- She compared and picked; caption approved
- Package delivered (local paths + caption); Drive archived (or her-action noted)
- No step skipped silently — report anything blocked, honestly

## Working reference implementation
First build (2026-07-16 addition post): `build_post.py` pattern — fetch template/CSS/fonts via `gh api`, string-fill v1 slide block, clone for v2/v3, `playwright.sync_api` element screenshots. Reuse it.
