---
name: lucy-image-production
description: One-shot Lucy asset generation and deterministic export for Skill Heaven.
---

# Lucy Image Production

This is the Skill Heaven specialization of Gaia Image Production. It governs
every generated Lucy raster, background removal, upscale, crop, filter, and
WebP export in this repository.

## Authority

Read these before production, in this order:

1. `packages/site/src/assets/lucy/authority/lucy-character-sheet-master.png`
2. `docs/lucy/authority/LUCY_CANONICAL_CHARACTER_SHEET.md`
3. `docs/lucy/authority/lucy-canon.json`
4. `packages/site/src/assets/lucy/authority/lucy-original-reference.jpg`
5. The assigned job in `docs/lucy/production/ASSET_PRODUCTION_PLAN.md`

The final sheet and written canon win over every earlier iteration. Lucy is one
character. Her anatomy and outfit do not transform between states.

## Paid generation contract

- Use `gpt-image-2` only.
- Make exactly one generation call for each assigned `GEN-*` job.
- Do not request alternates, variations, or a second attempt.
- Include the authority images in the generation context.
- Preserve the first result even when it fails a gate; mark the job blocked.
- Self-review the result once. Continue only with deterministic local
  processing: crop, resize, alpha extraction, cleanup, compositing, inversion,
  color filtering, and WebP export.
- An owner-authorized candidate brief may define multiple named candidates.
  Treat each named candidate or bounded edit as its own one-call job. Never add
  replacements beyond the explicit candidate count, and never promote a
  candidate before the brief's human selection gate.

## Storage contract

- Raw/master/intermediate PNGs:
  `packages/site/assets/workbench/lucy/<job-id>/` (gitignored).
- As-is backup: run `scripts/assets/backup-lucy-pngs.sh` after any PNG lands.
- Production deliverables:
  `packages/site/src/assets/lucy/` as WebP.
- The canonical sheet and owner-approved source masters already retained under
  `src/assets/lucy/*/masters/` may stay in Git for authority and provenance,
  but frontend code must never import those PNGs directly; browsers load
  delivery WebPs only.
- Write a receipt to `docs/lucy/production/runs/<job-id>.md` with model,
  prompt path or full prompt, input authorities, raw path, outputs, dimensions,
  alpha result, self-review results, and any blocked item.

## Transparency and chroma fallback

When a brief says transparent, the final production WebP must contain real
alpha. No white, black, gray, or colored matte may remain in translucent edges.

1. Request a transparent background in generation.
2. Inspect the PNG alpha channel itself. A painted checkerboard is opaque art,
   not transparency, even when the RGB preview looks correct.
3. If the generator returns an opaque background, accept that one result and
   use deterministic removal. Prefer a flat `#00FF00` chroma field requested in
   the original brief; chroma green is deliberately distant from Lucy's cyan,
   blue, gold, red, silver, and skin palette.
4. Reject opaque white, gray, scene, simulated transparency, and baked-checker
   sources at the matte gate. Do not reconstruct a checker into speculative
   alpha. Never use purple or magenta as a Lucy chroma field.
5. Run `scripts/assets/lucy-matte-guard.py` for native-alpha validation or
   verified flat-green extraction. Supply a semantic-region JSON for character
   masters so face core, head, hair, torso, both arms/hands, both legs/feet,
   wings, and weapons must each pass alpha-density gates. The face-core region
   must have at least 70 percent of pixels at alpha 192 or higher and median
   nonzero alpha of at least 224. Head and hair must also meet the tool's
   median-alpha floors; nonzero ghost pixels do not count as completeness.
6. Inspect the generated white, black, mid-gray, light-checker, dark-checker,
   inverted-RGB checker, and raw-alpha audits for halos, holes, ghost pixels,
   missing pale features, and contaminated glass edges.
7. Require zero strong-green and zero strong-magenta pixels in the
   exterior-connected partial-alpha band for chroma-key work. An approved
   native-alpha prismatic source may use the guard's explicit
   `--source-native-prism` exception only when the receipt records the source
   provenance and edge counts and browser QA confirms the inherited hues are
   art, not matte contamination. Do not infer completeness from RGB; the alpha
   silhouette is the authority.
8. Export a lossless-alpha WebP and re-open it to verify alpha survived.

Chroma is a workbench surface, never a brand color. Do not regenerate because
alpha removal is inconvenient.

Example fail-closed matte invocation:

```bash
python3 scripts/assets/lucy-matte-guard.py \
  --input packages/site/assets/workbench/lucy/JOB/raw.png \
  --output packages/site/assets/workbench/lucy/JOB/intermediate/alpha.png \
  --audit-dir packages/site/assets/workbench/lucy/JOB/audit \
  --report packages/site/assets/workbench/lucy/JOB/matte-report.json \
  --regions packages/site/assets/workbench/lucy/JOB/semantic-regions.json \
  --candidate JOB
```

## Deterministic processing

Use free local processing wherever possible. The preferred portable runtime is:

```bash
npx -y --package=tsx --package=sharp --package=@img/sharp-wasm32 tsx <script>
```

Keep reusable processing logic in `scripts/assets/`; do not hide the workflow
inside an untracked one-off command. Derivatives from the same generation—wide
composites, state cards, portraits, social crops, filtered plates, and mobile
crops—are not new image-generation jobs.

## Supersampling modes

Generation/master authority, enhancement workbench, delivery master, web
encoding, and verification are separate stages. The approved source always
owns Lucy's pose, identity, composition, and silhouette. An enhancer may
recover bounded image detail; it never owns alpha geometry.

- **standard:** direct deterministic resampling for ordinary derivatives.
- **high:** a 4x enhancement workspace collapsed to the requested delivery
  dimensions.
- **overkill:** offline hero/key-art production. Separate luma, chroma, and
  canonical alpha; use a neural detail oracle only on luma with
  `face_enhance=false`; keep conservative resampling as the structural owner;
  then use a tiled 16x numerical workspace and staged Lanczos
  `16x -> 4x -> 2x` collapse. Never commit or ship the 4x/8x/16x workspace.

The v5 reference implementation is
`scripts/assets/lucy-v5-overkill-export.py`. Reproduce it from a clean checkout
with Python 3.11 and the pinned
`scripts/assets/requirements-lucy-overkill.txt`; the script downloads the
checksum-pinned MIT-licensed ArtCNN R16F96 ONNX model into the ignored
workbench. Its hybrid path bounds the ArtCNN luma residual, reconstructs BT.709
Cb/Cr independently, resamples the source alpha independently, produces exact
2x delivery dimensions, encodes lossy RGB with lossless/high-fidelity alpha,
reopens the WebP, and refuses any encoded alpha change.

```bash
python3.11 -m venv packages/site/assets/workbench/lucy/ISSUE-73-OVERKILL/.venv
packages/site/assets/workbench/lucy/ISSUE-73-OVERKILL/.venv/bin/pip install -r scripts/assets/requirements-lucy-overkill.txt
packages/site/assets/workbench/lucy/ISSUE-73-OVERKILL/.venv/bin/python scripts/assets/lucy-v5-overkill-export.py --provider coreml --force
python3 scripts/assets/validate-lucy-v5-delivery.py
```

Use `--provider cpu` when Core ML is unavailable. Provider choice is recorded
in the manifest and may alter RGB bytes; dimensions, bounded-detail policy, and
decoded-alpha verification remain identical.

Every supersampled run must record:

- source and model provenance plus SHA-256;
- exact source, theoretical workspace, and delivery dimensions;
- model/runtime/provider versions and `face_enhance=false`;
- luma residual bounds, chroma method, and alpha method;
- encoded dimensions, byte count, alpha counts/hash, and output hash;
- white, black, gray, light/dark checker, inverted-RGB, and raw-alpha audits;
- real browser verification on every consuming route at desktop and mobile.

The delivery size and byte budget are quality targets, not permission to
damage the approved art. Report misses honestly. A delivery must still be a
smaller modern-format browser asset than its retained source PNG.

## State gates

- **Zero:** seated zen, closed eyes, normal gravity, one katana, no wings and
  absolutely no shards.
- **Heaven:** unique falling pose, both diamond eyes open, one katana, ordered
  saturated cyan-blue glass-shard wings.
- **Hell:** generate a complete Heaven-palette source with both eyes naturally
  closed and one continuous tear from the eyelid down the full face, then apply
  one exact full-foreground RGB inversion. The source tear must be the cyan
  complement that becomes the final vivid red tear. Use one katana and
  fragmented shards. Never patch eyelids or recolor the tear after inversion;
  all Hell-related derivatives descend from the untouched inverted master.
- **Ultra:** unique decisive falling pose, one gold diamond eye open, the other
  closed with a red tear, two matching katanas, gold shards, never inverted.

All states retain shoulder-length silver-white hair, dark sailor uniform,
prismatic ribbon, barefoot anatomy, real steel katana construction, and glass
shards with no feathers or membranes.

## One-pass self-review checklist

- [ ] Same canonical Lucy, proportions, uniform, hair length, ribbon, bare feet.
- [ ] Assigned pose, gravity, eye state, tear, weapon count, and shard language.
- [ ] No text, labels, signature, watermark, frame, or accidental UI.
- [ ] Full silhouette and required effects are not clipped.
- [ ] Transparent deliverables have real alpha and no matte/halo.
- [ ] Head, face, hair, torso, limbs, wings, and weapons have nonzero alpha in
      their declared semantic regions.
- [ ] White, black, gray, normal-checker, dark-checker, and inverted previews
      preserve hair, skin, glass, and steel edges.
- [ ] Exterior partial-alpha edges contain no strong green or magenta pixels.
- [ ] The two-pixel interior foreground boundary contains no strong green key
      spill. This includes opaque hair/glass edge pixels: exact Hell inversion
      would turn missed green spill into a magenta rim.
- [ ] For Hell, enforce that green-boundary rule on the pre-inversion source.
      The final exact-inverted Hell may use the guard's explicit
      `--exact-inverted-hell` mode only after the source report passes and the
      inversion report proves full-foreground RGB inversion plus byte-identical
      alpha. This avoids misclassifying legitimate green produced by inverting
      canonical source magenta.
- [ ] Hell inversion receipts must verify the source tear contains vivid cyan
      pixels in the declared face-core, the exact inversion contains the same
      number of vivid-red pixels, and the red pixels span at least 35 percent
      of the face-core height. Human composite review still decides eyelid
      contact and unbroken eyelid-to-jaw continuity.
- [ ] Output dimensions and file paths match the production plan.
- [ ] Production WebP re-opens successfully and stays within its target size.
- [ ] Raw PNG was backed up as-is.
- [ ] Receipt records pass/fail honestly; failed gates are not silently hidden.
