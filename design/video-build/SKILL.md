---
name: video-build
description: Transform an approved video script into a Remotion build specification with scaffolded project directory, compositions, scene components, and render config
type: planning
version: v0.2
required_conventions: [alignment-page]
argument-hint: "<script-path-or-slug> [--style minimal|motion-heavy|kinetic-text] [--fps 30|60] [--resolution 1080p|4k]"
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Video Build

Invoke as `$video-build`.

Take an approved video script and produce a build specification document and a scaffolded Remotion project directory with compositions, scene components, asset manifest, and render config.

## Prerequisites

- `specs/youtube/video-script-<slug>.md` must exist.
- Remotion availability is checked (`npx remotion --help`). If not installed, produce the spec and scaffold but defer render commands to `tasks/manual-todo.md`.

## Inputs

- `specs/youtube/video-script-<slug>.md`
- `specs/youtube/series-<slug>.md` (visual identity)
- `research/youtube/product-led-media-map-<slug>.md` (proof assets)
- Codebase scan for design tokens, logos, and fonts.

## Process

0. Resolve arguments: script path or slug, style (`minimal`, `motion-heavy`, `kinetic-text`), fps (`30`, `60`), resolution (`1080p`, `4k`).
1. Load script, series spec (visual identity), product-led-media-map (proof assets), and scan codebase for design tokens, logos, and fonts.
2. Text-based checkpoint: confirm visual identity (colors, fonts, logo), asset sourcing per asset requirement, technical config (platform, fps, resolution, existing Remotion project?) with the user before proceeding.
3. Design component tree: map script scenes to Remotion components with durations in frames, visual elements, animation timing, and audio references.
4. Text-based checkpoint: present build specification — component tree diagram, per-scene build plan, asset manifest, render config. Validate with user.
5. Write output only after user confirmation.

## Output

Create the `specs/youtube/` and `src/videos/<slug>/` directories if they do not exist.

Write `specs/youtube/video-build-<slug>.md` with:

- **Build Brief:** script reference, style, fps, resolution, target platform.
- **Component Tree:** diagram and component descriptions.
- **Scene-by-Scene Build Plan:** table — component, duration (frames/seconds), visual elements, animation type, assets.
- **Asset Manifest:** table — name, type, status (`available`/`placeholder`/`needs-creation`), path, notes.
- **Audio Plan:** narration, music, SFX, sync points.
- **Render Configuration:** composition ID, fps, width, height, codec, output format.
- **Typography & Color Tokens:** fonts, sizes, colors from brand/series.
- **Transition Library:** which transitions between which scenes.
- **Next Steps.**

Write `specs/youtube/video-build-<slug>-interview.md` with the interview log.

Scaffold `src/videos/<slug>/`:

```
composition.tsx        // Root composition with Sequence timing
scenes/               // One component per script scene
transitions/          // Reusable transition components
components/           // Shared UI (LowerThird, BrowserFrame, etc.)
assets/
  manifest.json       // Asset paths and statuses
config/
  render.ts           // Render configuration
  theme.ts            // Colors, fonts, spacing tokens
```

### Task Classification

After writing output:

- `tasks/todo.md`: render commands, asset sourcing automation, subtitle generation.
- `tasks/manual-todo.md`: record footage, source music, record voiceover, YouTube upload, metadata, thumbnail, scheduling.
- `tasks/recurring-todo.md`: review performance at 7-day and 30-day marks.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default `## Next-Skill Routing` sequence, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/video-build-{topic}.html`.

## Constraints

- Every scene component must match the approved script timing — do not add or remove scenes.
- Do not generate AI voiceover without explicit user approval.
- Do not embed copyrighted assets without the user confirming licensing.
- Asset manifest must clearly distinguish `available` vs `placeholder` vs `needs-creation`.
- Respect series visual identity when a series spec exists.
- Present the build specification before writing — never write until the user confirms.
- Keep components composable — series should reuse intro/outro/transition/lower-third across episodes.
- Do not expose secrets, private customer data, or unreleased commitments.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

