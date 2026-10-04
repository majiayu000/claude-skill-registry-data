---
name: agent-foundry-app-icon
description: "Design, generate, integrate, build, and verify a production iOS App Icon for an AgentFoundry product. Use when creating or replacing an app logo/icon, when a product brief needs a detailed English image-generation prompt, or as the mandatory brand-icon contour inside agent-foundry-proof. Produces an opaque 1024x1024 master, validates 40x40 readability, installs an AppIcon asset catalog, and verifies the compiled icon on the selected Simulator or iPhone."
---

# AgentFoundry App Icon

## Outcome

Ship one distinctive production App Icon, not merely an image concept:

- one simple product-specific visual metaphor;
- a reusable detailed English generation prompt;
- an opaque full-bleed 1024x1024 PNG without pre-rounded corners;
- a 40x40 readability check and visual inspection;
- a correctly wired `AppIcon.appiconset`;
- build evidence that `actool` emitted the icon into the app bundle;
- install and launch on the selected runtime target when available.

## Required Companions

Always read and apply:

1. `references/prompt-template.md` before writing the generation prompt.
2. `../imagegen/SKILL.md` for generation, output conventions, inspection, and targeted iteration.

When invoked outside `agent-foundry-proof`, also read `../agent-foundry-design/SKILL.md` if the product has no established design concept or color story. Inside Proof, inherit the design concept already selected by `agent-foundry-design`.

## Workflow

### 1. Resolve The Brand Brief

Determine from the user request and product sources:

- product display name;
- one-sentence purpose;
- primary audience;
- brand character and established palette;
- optional symbol preference;
- iOS project root and runtime target.

Infer these from an active Proof instead of asking again. Ask only when a missing choice would materially change the brand.

### 2. Choose One Metaphor

Choose one bold central symbol that communicates the product at 40x40. Prefer an ownable metaphor tied to the durable product object or primary workflow. Avoid combining icons, drawing a scene, encoding UI, or defaulting to category clichés.

Do not use letters, product initials, words, a medical cross, generic heart, shield, sparkles, chatbot bubble, or infinity mark unless the user explicitly requires that symbol. Record the selected metaphor and a one-sentence rationale in the proof report, but keep explanations out of the final generation prompt when the user asks for prompt-only output.

### 3. Write And Generate

Fill `references/prompt-template.md` in English. Preserve all hard constraints and customize only the product, metaphor, palette, material, and mood.

Use `gpt-image-1.5` with high quality and `1024x1024`. Generate one candidate first. Save stable outputs under:

```text
<PROJECT>/output/imagegen/<Product>-AppIcon-1024.png
<PROJECT>/output/imagegen/<Product>-AppIcon-prompt.txt
```

Use an existing process-scoped `OPENAI_API_KEY`. Inside an authorized AgentFoundry Proof, if the key has already been promoted to the product-scoped Secret Manager resource, expose it only to the image-generation process without printing, logging, or persisting plaintext. Do not start a second credential decision flow. The Proof upfront ledger must cover Image API use and its cost.

### 4. Inspect At Full And Small Size

Inspect the 1024 master. Create a 40x40 preview with a standard image-resize tool and inspect it too.

Reject or target-iterate when any of these are true:

- the silhouette is unclear at 40x40;
- the generator produced text, initials, watermark, frame, mockup, or rounded corners;
- the symbol is a prohibited cliché or no longer matches the selected metaphor;
- the background is transparent or does not fill the canvas;
- the composition contains multiple competing objects or thin detail.

Make one targeted prompt correction at a time. Do not batch-generate unrelated options unless the user asks for variants.

Verify the final master is exactly 1024x1024 and opaque.

### 5. Integrate The App Icon

Create or update:

```text
<PROJECT>/App/Resources/Assets.xcassets/Contents.json
<PROJECT>/App/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json
<PROJECT>/App/Resources/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png
```

Use the universal iOS 1024x1024 slot. Keep the source square and unmasked; iOS applies its own icon shape.

Persist resource inclusion and `ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon` in the source project graph. For Tuist projects, ensure the resource glob includes the asset catalog and regenerate the project. Do not rely on a generated `.xcodeproj`-only edit as the source of truth.

Before building, verify the PNG contains local data and is not a macOS/iCloud `dataless` placeholder. A placeholder can make `actool` succeed while emitting an empty icon set. If necessary, materialize or regenerate the master into a local non-cloud temporary path before copying it into the project.

### 6. Build, Package, And Run

Build for the runtime target selected by the parent Proof: prefer a connected usable iPhone, otherwise Simulator. Reuse the Proof authorization ledger for signing, install, and launch.

Do not accept `BUILD SUCCEEDED` alone. Verify all of the following:

- `actool` compiled `AppIcon` without an icon error;
- the built `.app` contains generated icon PNGs and/or `Assets.car`;
- the built `Info.plist` contains `CFBundleIconName = AppIcon` or equivalent primary-icon metadata;
- the final build installs and launches on the selected target.

If a device build requires a Development Team, follow the parent Proof signing workflow. If disk space blocks compilation, remove only task-created temporary DerivedData and retry.

## Completion Evidence

Return or record:

- selected metaphor;
- final prompt path;
- 1024 master path;
- asset catalog path;
- opaque/dimension validation;
- 40x40 inspection result;
- build/`actool` result;
- bundle icon metadata result;
- install/launch target and result;
- exact remaining blocker, if any.

Do not claim the icon shipped when the generated PNG exists but the app bundle lacks primary-icon metadata or icon renditions.
