---
name: codex-desktop-pet-builder
description: Design, generate, repair, validate, package, install-test, and privacy-audit V2 animated pets for Codex Desktop from text, character art, images, or video references. Use when Codex needs to create or refine a custom desktop pet, define its nine standard animation states, build an 8x9 V2 spritesheet without mouse-follow views, preserve character identity across animation rows, diagnose atlas or motion defects, make a portable two-file pet package, or sanitize a pet project for public release.
---

# Codex Desktop Pet Builder

Build a Codex-compatible animated pet through explicit contracts, row-level quality gates, deterministic atlas assembly, and privacy-safe release. Treat generated art as source material and deterministic tooling as the owner of final geometry.

## Start with the contract

Read [references/animation-contract.md](references/animation-contract.md) before defining poses, frame counts, atlas dimensions, or manifest metadata.

This Skill publishes only the V2 contract:

- Use 8 columns by 9 rows for the nine standard animation states.
- Do not generate mouse-follow, gaze-direction, or other extra view rows.
- Set `spriteVersionNumber` to `2` in every release manifest.
- Never pad the atlas with unused extra rows or omit the V2 manifest declaration.

Record the pet id, display name, one-sentence description, style, chroma key, cell size, contract version, source roles, stable identity traits, prohibited elements, and approval mode before generation.

## Protect source privacy

Copy only necessary source assets into an isolated working directory. Rename them with generic roles such as `identity-front`, `motion-reference`, and `palette-reference`. Do not carry chat transcripts, conversation identifiers, messaging-app paths, user-profile paths, account names, temporary generation paths, or original media filenames into manifests, prompts, QA reports, documentation, or Git.

Keep raw images, video frames, rejected candidates, contact sheets, GIFs, and installer sandboxes outside the public release tree unless the user explicitly wants safe synthetic examples published and their rights are clear.

## Use a gated workflow

1. Define the visual identity.
   - Separate immutable identity from animation-specific motion.
   - Lock silhouette, proportions, face, palette, material, markings, costume, props, and handedness.
   - Exclude scenery, captions, UI, playback controls, lighting effects, and incidental objects from references.

2. Create and approve a canonical base.
   - Generate one centered, complete, readable full-body pet on a removable flat chroma background.
   - Verify identity, pet-size readability, connected components, safe margins, and background separability.
   - Use the approved base as the source of truth for every row.

3. Build standard rows in dependency order.
   - Use `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, then `review`.
   - Generate one coherent strip per state. Do not create unrelated cells and tile them together.
   - Attach the canonical base and every reference that defines identity or the current motion.
   - Keep later rows blocked until their dependency gate passes when the user requests per-state approval.

4. Gate every row immediately.
   - Run deterministic checks for exact frame count, separable poses, complete components, margins, clipping, baseline, scale, and extraction stability.
   - Render a motion preview and inspect identity, state semantics, cadence, first-to-last loop closure, and distinction from other states.
   - Do not mark a row complete merely because structural validation passes.

5. Assemble deterministically.
   - Extract approved rows into fixed cells with shared scale and stable anchors.
   - Compose the atlas from approved files only.
   - Apply exactly one deterministic edge-local chroma spill cleanup to the completed release atlas.
   - Validate dimensions, transparency, used and unused cells, manifest version, and file identity after encoding.

6. Run final visual QA.
   - Inspect the contact sheet and every row preview.
   - Confirm the atlas contains exactly the nine standard action rows and no mouse-follow views.
   - Block release for identity drift, missing frames, wrong travel direction, inert or reversed motion, size popping, clipping, detached effects, or transparent interior seams.

7. Package and install-test.
   - Put only `pet.json` and `spritesheet.webp` in the pet payload directory.
   - Make installer paths relative to the installer location or Codex environment variables.
   - Test first install and replacement install in an isolated Codex home; verify backup, rollback, staging cleanup, package hashes, and post-install manifest/atlas validity.

8. Sanitize public output.
   - Read [references/release-and-privacy.md](references/release-and-privacy.md).
   - Run `scripts/audit-pet-release.ps1` before staging and again with history scanning before pushing.
   - Review the staged diff and every binary by purpose. Publish only reusable instructions, deterministic scripts, generic examples, and intentionally distributable pet assets.

## Choose the approval mode

Use per-state approval when the user wants creative control. Present only the canonical base or current row, record approved/rejected status, and do not generate the next state early.

Use autonomous gated progress when the user asks Codex to finish independently. Keep the same row order and quality gates, but continue after each row passes. Stop only for a subjective decision that materially changes the character, an external blocker, or a contract change.

User feedback overrides the default motion concept for that state, but not geometry, package, privacy, or version integrity.

## Repair the smallest valid scope

Read [references/qa-and-repair.md](references/qa-and-repair.md) before diagnosing or repairing rows.

- Preserve accepted candidates and record a new revision for every retry.
- Regenerate the smallest coherent unit: one complete standard action row.
- Do not patch a failed cell into a newly generated coherent strip.
- Prefer deterministic corrections for extraction, registration, transparency, and packaging failures.
- Regenerate only when the source visual or motion semantics are wrong.
- If the same root cause repeats twice, change strategy instead of rephrasing the same prompt.
- Re-run every downstream check affected by the repair.

## Keep generation and geometry separate

Use the installed image-generation capability for base art and coherent row strips. Use deterministic scripts for chroma removal, extraction, shared-scale registration, atlas composition, WebP encoding, validation, preview rendering, and package auditing.

Never use code-drawn placeholders, affine whole-sprite rotation, copied guide pixels, or tiled duplicate cells as substitutes for missing generated art. Mirroring `running-right` into `running-left` is allowed only when markings, prop handedness, lighting, identity, direction, and frame timing remain correct; mirror cells without reversing temporal order.

## Deliverables

Keep production and release outputs separate:

- canonical identity reference and source-role manifest;
- approved row strips and revision decisions;
- extracted frames, contact sheet, previews, validation, and repair records;
- final atlas and matching manifest;
- minimal two-file pet payload;
- optional portable installer outside the payload;
- privacy audit and concise validation summary.

Do not include a README inside the Skill itself. Repository-level documentation may describe installation and invocation.
