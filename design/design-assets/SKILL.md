---
name: design-assets
description: Use whenever a task needs a visual asset — logo, icon, illustration, hero/OG/web-page graphic, empty-state art, favicon/app icon, or converting a raster reference to vector. Recraft (a generative asset tool reached through its MCP server) is called FIRST for all visual assets; Claude hand-authors only as fallback or for surgical cleanup. Covers the art-direction brief format, curation/render workflow, integration conventions, and billing/availability caveats. For visual JUDGMENT (colors, spacing, hierarchy) pair with design-guide; for Tabler component markup use tabler-ui.
---

# Design assets (Recraft)

Goal: produce production-quality visual assets through **Recraft** — a generative
asset tool reached through its MCP server — with Claude doing all art direction,
curation, and integration. (This install's tool roster and setup: `LOCAL.md` beside
this skill, when your copy keeps one — *Tool roster*.)

## The standing rule: Recraft-first (user decision, 2026-07-13)

**Every visual-asset request goes to Recraft first.** Logos, icons, illustrations,
web-page graphics, hero/OG images, empty-state art, texture/background art,
raster→vector conversion. Claude hand-authors an asset itself only when:

1. **Recraft is unavailable** — MCP unreachable or credits exhausted. Claude does
   it at the identical bar and **flags it inline**.
   🔑 An unattended (scheduled/headless) run can still reach an OAuth MCP server once
   its tool use has been approved once — the approval is stored with the task, after
   which it proceeds unattended. Check before assuming otherwise: run it and look.
   (How this was verified here: `LOCAL.md` beside this skill, when your copy keeps
   one — *Unattended runs*.)
2. **Surgical cleanup or derivation** — adapting an existing asset (theme recolor,
   `currentColor`/CSS-var conversion, svgo cleanup, geometry fix, favicon
   derivation from an approved mark). Don't regenerate what only needs editing.

Recraft never decides direction. Claude briefs; the user picks from rendered
candidates; Claude integrates.

## Workflow

1. **Read the design context first.** design-guide (LEARNINGS + standing
   decisions), the app's existing visual language, and any brand story/palette on
   record. An asset that contradicts a recorded preference is rework.
2. **Write the art brief before generating.** Decision-complete, like an
   implementation brief: subject/concept (one per generation — don't mush
   concepts), style (e.g. `vector_illustration` substyle for marks/icons), exact
   palette hexes, background (transparent unless told otherwise), output type
   (**vector/SVG for logos and icons — always**; raster only for
   photographic/painterly work), size, and N variants.
   Record the brief — it gets committed with the asset.
3. **Check the balance when planning a large batch** — `get_user` is free. Single
   images cost ~$0.04–0.08; a 6–8 concept exploration is cents, a 100-asset sweep
   is real money — ask before those. The balance lives behind the MCP server, and
   Recraft's REST API bills separately from the subscription it uses, so read it with
   `get_user` rather than the REST API. (If your install tracks the balance somewhere
   else, pass the number on whenever you call `get_user`; this install's courier step:
   `LOCAL.md` beside this skill, when your copy keeps one — *Balance reporting*.)
4. **Generate, then curate.** Pull the results, drop weak ones, and render the
   survivors into a labeled comparison (montage on light AND dark backgrounds —
   design-guide's render-candidates rule). The user picks; Claude never ships an
   asset the user hasn't seen rendered in context.
5. **Integrate like an engineer.** svgo-clean the SVG; convert fixed colors to
   `currentColor`/CSS vars where the asset must follow theme; derive
   favicon/app-icon sizes from the approved mark; verify at target sizes (16/32px
   for favicons) and in both themes with inline screenshots.
6. **Commit the asset with its provenance.** The prompt/brief that produced it
   goes in the plan file or a sibling `*.brief.md` — regenerating or extending a
   family of assets later requires knowing exactly what produced the originals.

## Tool surface (hosted MCP: `mcp.recraft.ai/mcp`)

`generate_image` (text→raster or **true-SVG vector**) · `vectorize_image`
(raster→SVG) · `image_to_image` (variation from reference + prompt) ·
`remove_background` / `replace_background` · `crisp_upscale` /
`creative_upscale` · `create_style` (custom style from reference images — use
one per project for a consistent asset family) · `get_user` (free; balance).

In Claude Code the tools may need loading via ToolSearch (`recraft`). In a
session started before the server was registered, spawn a fresh sub-agent to
carry the generation calls — new agent processes pick up the current MCP config.

## Division of labor

- **Claude**: art direction, briefs, curation, montage/rendering, integration
  edits to SVG, verification, commits. Claude's SVG-authoring skill is the
  fallback lane, not the default lane.
- **Other implementers** (a coding agent or teammate the code is delegated to):
  never call Recraft. They consume committed asset paths in the code they write.
  If an implementer needs an asset that doesn't exist yet, generating it is its
  own first step, done before the implementation is handed over. (This install's
  split: `LOCAL.md` beside this skill, when your copy keeps one — *Division of
  labor*.)
- **Ideogram (manual, user-driven)**: for typography-accurate lettering
  explorations, suggest the user run them in Ideogram and bring results back;
  no API integration for it. Arabic script from ANY image model needs letterform
  verification by someone who reads it.

## Common failure modes

- **Hand-authoring by default out of habit** — the standing decision is
  Recraft-first; hand-authoring without an unavailability/cleanup reason
  violates it. Flag fallbacks inline every time.
- **Generating raster for a logo/icon** — marks and icons are vector output,
  always; raster gets blurry favicons and unusable scaling.
- **Skipping the montage** — handing the user raw generation dumps (or worse,
  integrating a self-picked winner) instead of a curated, labeled, both-themes
  comparison.
- **Losing provenance** — an asset in the repo whose generating prompt is
  nowhere on record.
- **Icon-set mismatch** — a generated icon dropped next to an existing set
  (e.g. Tabler's 24×24 stroke-2 grid) without matching its design language;
  those cases usually end in the cleanup lane (redraw to grid) — check
  design-guide's custom-icon standing decision before integrating.

## Before you call this done

- [ ] Asset went through Recraft (or the fallback/cleanup exception is flagged inline).
- [ ] Brief recorded and committed alongside the asset.
- [ ] User picked from a rendered light+dark comparison, not a description.
- [ ] SVG cleaned, theme-adapted, verified at target sizes, both themes, screenshots shown.

## Capturing learnings (session-handoff protocol)

Append to `LEARNINGS.md` beside this skill, when your copy keeps one: prompt
patterns that worked per asset type, style ids created per project
(`create_style` results), credit costs observed, MCP quirks. Dedupe; promote settled
patterns into this file.
