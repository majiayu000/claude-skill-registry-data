---
name: create-wildtrace-atlas
description: "Plan, compile, generate, audit, and repair sparse data-driven editorial visualization art in the Wildtrace Atlas language. Use when an agent must turn data or named chart methods into handmade cut-paper visualization images; create one-panel art, asymmetric multi-panel boards, or large batches; preserve outliers, reversals, clusters, skew, unequal gaps, and flow widths; avoid dashboard-like or icon-like results; or reproduce consistent results across Claude, Codex, and image-generation tools. Includes an executable 120-method catalog, versioned board specification, prompt compiler, deterministic preflight audit, and targeted repair workflow."
---

# Create Wildtrace Atlas

Treat this skill as a data-to-image compiler, not a style prompt.

## Required resources

- Read [references/style-language.md](references/style-language.md) before art direction.
- Read [references/specification.md](references/specification.md) before changing a board spec or accepting user data.
- Read [references/composition-system.md](references/composition-system.md) when planning panel geometry.
- Read [references/quality-system.md](references/quality-system.md) before approving or repairing generated images.
- Read [references/model-adapters.md](references/model-adapters.md) for the active image tool.
- Query the 120-method catalog with `scripts/wildtrace.py catalog`; do not load the entire JSON unless bulk catalog work requires it.
- Use [assets/reference-board.png](assets/reference-board.png) only as a visual-language reference. Never copy its layout or data.

## Compiler workflow

Follow this sequence. Do not skip directly from a user request to an image prompt.

1. **Resolve methods.** Normalize chart names through the catalog.
2. **Write data contracts.** Use user data when supplied. Otherwise use catalog defaults and state that they are illustrative.
3. **Plan the artifact.** Produce a versioned JSON board spec.
4. **Audit the spec.** Fix deterministic errors before image generation.
5. **Compile prompts.** Generate one prompt per complete board from the audited spec.
6. **Generate boards.** Use one image-generation call per board. Never generate panels separately unless the user explicitly requests separate assets.
7. **Audit pixels.** Inspect the image with the quality rubric. Confirm method identity, data character, density, material language, and absence of unwanted UI or text.
8. **Repair narrowly.** Keep valid panels invariant. Change only the failed geometry or density, then inspect again.
9. **Persist deliverables.** Save every requested final board, its spec, compiled prompt, and audit report together.

## Commands

Set `SKILL_DIR` to this skill folder, then use the standard-library CLI.

```bash
python "$SKILL_DIR/scripts/wildtrace.py" catalog --search sankey
```

Plan a board:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" plan \
  --methods lollipop-chart,streamgraph,sankey-diagram \
  --seed 42 \
  --out work/board.json
```

Override catalog data:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" plan \
  --methods lollipop-chart,sankey-diagram \
  --data work/data-overrides.json \
  --out work/board.json
```

Audit and compile:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" audit --spec work/board.json --strict --out work/audit.json
python "$SKILL_DIR/scripts/wildtrace.py" compile --spec work/board.json --out work/prompts.txt
```

Or build the complete pre-generation evidence bundle in one command:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" bundle \
  --methods lollipop-chart,streamgraph,sankey-diagram \
  --provider your-provider \
  --model your-model \
  --dir work/wildtrace-run
```

This writes the spec, deterministic audit, compiled prompts, method-to-board index, hashed run manifest, and a visual-audit skeleton. Fill the visual audit only after inspecting the generated pixels.

Plan all 120 methods as twenty six-panel boards:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" batch --all --panels-per-board 6 --seed 42 --out work/all-120.json
```

Compile a targeted repair prompt:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" repair \
  --spec work/board.json \
  --report work/audit.json \
  --out work/repair.txt
```

Run the built-in integrity check when the skill changes:

```bash
python "$SKILL_DIR/scripts/wildtrace.py" doctor
```

## Non-negotiable invariants

- Encode data before choosing decorative geometry.
- Use exactly one visualization grammar per panel.
- Keep unsorted order unless ranking is intrinsic to the method.
- Preserve at least one meaningful irregularity per panel.
- Keep marks near 30–48% of the panel and preserve a calm field.
- Use two or more panel-background colors on multi-panel boards.
- Vary panel dimensions, anchors, and edges; do not use an equal card grid.
- Use color only for series, categories, direction, hierarchy, or emphasis.
- Omit titles, labels, numbers, legends, logos, watermarks, and UI chrome unless glyphs are intrinsic to the selected method.
- Reject icon-like symmetry, wallpaper density, glossy gradients, unrelated decoration, and stock-dashboard polish.

## User data rules

- Never silently replace supplied values with prettier values.
- Never sort, normalize, aggregate, or smooth supplied data without stating the transformation and obtaining approval when it changes meaning.
- Preserve signs, order, missing values, units, hierarchy, source/target direction, and flow conservation when applicable.
- If the user supplies only method names, use catalog defaults and label the result as illustrative.
- If the user supplies more methods than fit one board, create a series of complete boards; keep a stable seed and shared material language.

## Image-generation rules

- Treat user images as references unless the user explicitly requests an edit.
- State each input image's role in the prompt.
- For bitmap art, use the active image-generation tool rather than substituting SVG or UI code.
- Feed the complete compiled board prompt in one call.
- Do not add a brand name, logo, signature, or in-image title.
- Save the generated result outside temporary storage when it belongs to a project.

## Pixel audit

After generation, inspect every panel and record pass/fail for:

1. method identity;
2. data-order and anomaly preservation;
3. one-grammar-only compliance;
4. sparse mark count and negative space;
5. unequal board geometry and multiple backgrounds;
6. tactile paper/ink material;
7. unwanted text, UI, decoration, logo, or watermark.

Use [references/quality-system.md](references/quality-system.md) to score the result. Do not approve a board with a method-identity error. Repair that board only.

## Deliverables

For a project-bound result, deliver:

- generated image files;
- `board-spec.json` containing actual methods and data;
- `prompts.txt` containing the compiled prompt set;
- `audit.json` containing deterministic and visual findings;
- `run-manifest.json` binding the run to a content hash, provider, model, and file set;
- `visual-audit.json` containing the completed 28-point pixel review;
- a concise method-to-board index for multi-board series.

The images are examples. The spec, catalog, compiler, and audit trail are the reproducible system.
