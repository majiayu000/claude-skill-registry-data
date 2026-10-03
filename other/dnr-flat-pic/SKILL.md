---
name: dnr-flat-pic
description: >-
  Transform reference photographs and visually dense images into sparse, recognizable, high-saturation flat-vector-style illustrations through semantic compression rather than literal tracing. Use when the user asks for photo-to-flat illustration, photo-to-vector-style redraw, 照片转扁平插画, 无渐变高饱和插画, iconification, visual simplification, composition-preserving abstraction, a consistent minimal illustration set, or revisions that remove gradients, glow, texture, blur, clutter, text, logos, numbers, or UI. Default to human-perceived semantic complexity 6 out of 10 or lower, fixed-HSB solid fills, crisp boundaries, and no gradients or light-halo effects.
---

# DnR FlatPic v2.0

Transform a supplied image into a newly reconstructed, low-complexity, flat-vector-style illustration. Preserve the image's specific identity and spatial relationships while removing most nonessential meanings and all photographic surface detail.

Do not trace the photograph. Do not apply a generic cartoon filter. First compress the semantics; then rebuild the scene from large closed shapes and solid fills.

## Load the supporting instructions

- Read `references/generation-spec.md` before every generation or edit. It contains the canonical generation specification and hard flat-color constraints.
- Read `references/semantic-complexity.md` whenever estimating, reducing, or validating semantic complexity.
- Read `references/aspect-ratio-adaptation.md` whenever the user explicitly requests an output aspect ratio different from the reference.
- Read `references/examples-and-failures.md` only when the scene resembles an example or the result is drifting toward over-detail or generic symbolism.
- Read `references/square-source.md` only after an accepted FlatPic exists and the user explicitly requests `poster`, `icon_svg`, or `all`.
- Read `references/poster-output.md` only for the `poster` or `all` mode.
- Read `references/svg-output.md` only for the `icon_svg`, `source_svg`, or `all` mode.

## Workflow decision

1. **New transformation from a supplied reference image**: follow the full creation workflow.
2. **Revision of an illustration already present in the conversation**: preserve the existing composition and follow the revision workflow.
3. **No usable image is present**: ask the user to upload or identify the image. Do not invent a target.
4. **User requests a derived output after an accepted FlatPic**: route only through the explicit modes in `## Optional derived outputs`; never let a derived mode alter the base generation prompt, ratio, validation, or retry budget.
5. **User requests SVG without an explicit mode**: ask whether they want `生成 SVG 图标` (square, rounded) or `导出当前插画 SVG（原比例）` (native ratio, no rounded wrapper).

## Global conflict resolution

Resolve every generation and revision conflict in this order: the flat-color rendering contract first; identity anchors and spatial relationships second; semantic compression third; stylistic preferences last. Lower-priority requirements must not override higher-priority requirements.

## Full creation workflow

### 1. Inspect the reference

Read the whole image before generating. Determine:

- dominant subject or subject group;
- foreground, midground, and background ordering;
- dominant horizontal, vertical, or diagonal axes;
- major scale differences and overlaps;
- overall warm-cool tendency, discrete light-dark value tiers, and regional color roles;
- repeated elements that humans naturally perceive as one group;
- source text, watermarks, subtitles, counters, or interface overlays that should normally disappear.

Do not use resolution, pixel count, edge density, or texture entropy as the main complexity measure.

### 2. Build and compress the semantic brief

Use `references/semantic-complexity.md` to select the target complexity, identify the primary and supporting systems, choose three to six identity anchors, group repeated elements, compress nonessential meaning, and allocate visual fidelity. Use the HSB palette role assignment rules in `references/generation-spec.md` to assign palette colors based on semantic regions, value hierarchy, and warm-cool contrast. Do not reproduce the source photograph's native hues. Preserve relationships before surface detail.

Do not show this internal brief unless the user explicitly asks for analysis.

### 3. Reconstruct with the canonical rendering contract

Apply `references/generation-spec.md` as the canonical rendering contract. Do not override its flat-color, boundary, lighting, or texture constraints.

### 4. Generate the image

Use the available image-generation capability to reconstruct the image from the reference and the compressed brief.

Place the complete Hard Flat-Color Specification from `references/generation-spec.md` before the reference-specific semantic brief. This is an internal prompt-assembly step, not an additional semantic condition.

Preserve the reference aspect ratio unless another ratio is requested; for a changed ratio, follow `references/aspect-ratio-adaptation.md`. Apply Source Cleanup and the HSB palette role assignment rules from `references/generation-spec.md`, fill the canvas with solid palette fields using the assigned color roles, and output only the clean illustration.

#### Generation Call Protocol

For each requested output image, call the image-generation tool exactly once by default. Track the call state as `not_started -> generating -> artifact_received -> delivered`.

A generation call is deemed successful if the tool returns any valid image artifact, image content, image URL, or generated output path—even if the wrapper produces no textual stdout. Immediately forward the artifact to the user via the available media-forwarding mechanism.

##### Prohibited Retries

Never issue another generation call for the following reasons:

- missing textual stdout from the wrapper;
- failed media display in the assistant response;
- empty accompanying text;
- mishandled media forwarding.

##### Allowed Retries

A second automatic generation call is permitted only as one of the following:

1. **Tool retry**: the tool explicitly reports an error, and the result contains no media artifact at all.
2. **Quality regeneration**: visual validation is enabled, and the image formally fails the Visual Validation Checklist.

> Quality regeneration triggered by formal validation is not counted as an erroneous duplicate call. Duplicate calls caused by misjudging tool success status are strictly prohibited.

`Tool retry` refers only to recovery from an explicit tool error with no artifact. `Quality regeneration` refers only to a new generation triggered by formal visual-validation failure. They share one allowance: each requested output may use at most one automatic follow-up call in total. If that follow-up also fails, stop without making a third call, do not present the result as compliant, briefly report the failed outcome, and wait for explicit user direction.

An explicit user request to regenerate or revise starts a new output request with a fresh call state and retry allowance.

After calling the image-generation tool, do not add a textual description unless the user asked for one. Once an accepted FlatPic has been delivered, the only optional follow-up prompt is: `继续：生成海报 / 生成 SVG 图标 / 导出当前插画 SVG（原比例）/ 都要`. Omit it when the user requested image-only output.

### 5. Visual Validation Checklist

Visual validation is enabled by default and may be disabled only when the user explicitly requests that it be skipped. Artifact delivery confirmation remains mandatory even when visual validation is disabled.

Run all checks internally before delivery. If any check fails, regenerate or revise the output; do not deliver a failing result with explanatory excuses.

#### 1. Recognition & Composition

- **Pass**: the primary subject is immediately recognizable.
- **Pass**: the result preserves the specific reference composition, not a generic category example.
- **Pass**: for custom aspect ratios, the result satisfies every validation condition in `references/aspect-ratio-adaptation.md`.
- **Fail**: generic composition that loses the reference's distinctive spatial arrangement.

#### 2. Semantic Complexity Budget

- **Pass**: perceived complexity meets or falls below the target level.
- **Pass**: repeated or subordinate elements read as grouped systems, not individual instances.
- **Pass**: no further semantic element can be removed without violating any condition in the Compression stopping rule in `references/semantic-complexity.md`.
- **Fail**: more competing focal centers than the semantic budget allows, or excessive ungrouped fine details.

#### 3. Flat-Color Compliance

- **Pass**: the result fully complies with the complete Hard Flat-Color Specification in `references/generation-spec.md`.
- **Fail**: any effect prohibited by that specification remains.

#### 4. Source Cleanliness

- **Pass**: the result fully complies with Source Cleanup in `references/generation-spec.md`.
- **Fail**: any content prohibited by Source Cleanup remains.

## Revision workflow

When the user asks to modify an existing generated illustration:

1. Treat each user-initiated revision as a new output request with a fresh Generation Call Protocol state and retry allowance.
2. Confirm that the target image is actually present in the conversation.
3. Preserve composition, crop, subject placement, and identity anchors unless the user requests structural change. When the target aspect ratio changes, aspect-ratio adaptation overrides crop and placement preservation only where necessary; identity anchors and primary-subject proportions remain invariant.
4. Change only the requested visual property where possible.
5. Reapply the full rendering contract after the edit.
6. Run the complete Visual Validation Checklist before delivery unless the user explicitly disabled visual validation.

For flatness revisions, replace continuous transitions with solid palette fills or discrete hard-edged steps; remove bloom, halo, glow, haze, light spill, and soft shadows; and convert lit windows or lamps into solid brightest-palette or permitted-variant shapes.

Do not describe these changes after generation unless requested; return the edited image.

## Multiple-reference sets

When several images are supplied:

- process each image independently;
- preserve each image's distinctive composition;
- use the same abstraction strength, boundary treatment, and rendering grammar across the set;
- use the same fixed HSB palette and independently assign palette roles to each source image; do not force identical local variants or compositions;
- do not combine unrelated references into one image unless explicitly requested;
- keep every image within the requested semantic-complexity ceiling.
- track the Generation Call Protocol state and shared one-call automatic retry allowance independently for each output image; one image's retry does not consume another image's allowance.

## Optional derived outputs

These are downstream actions, not alternative base-generation modes. Start them only after an accepted FlatPic artifact and an accessible original-photo/FlatPic pairing exist. Check the local Node.js environment only when one of these modes is explicitly requested; never check Node during ordinary FlatPic generation.

- `poster`: read `references/square-source.md` and `references/poster-output.md`.
- `icon_svg`: read `references/square-source.md` and `references/svg-output.md`.
- `source_svg`: read `references/svg-output.md`; do not generate a square source.
- `all`: read all three derived references, create at most one square source, and reuse it.

If the user says only “SVG”, ask the exact two-way question from Workflow decision. If a required artifact path cannot be recovered, ask the user to reattach the original photo or accepted PNG; never substitute a preview screenshot or invent a path. If Node is missing or too old, stop the derived mode and say: `此功能需要本机 Node.js LTS。当前未检测到可用版本。请从 https://nodejs.org/en/download 自行安装；完成后回复“已安装”，我会重新检测并继续。` Never download or install Node.
