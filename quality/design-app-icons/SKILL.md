---
name: design-app-icons
description: Design, redesign, critique, generate, productionize, and validate distinctive app icons, with an iOS-first workflow using built-in Imagegen for whole-icon concept iteration and Apple Icon Composer for approved production delivery across iOS, iPadOS, macOS, and watchOS. Use for app-icon briefs, visual direction, targeted revisions, category differentiation, small-size and contextual audits, Liquid Glass migrations, deliberate SVG or PNG layer reconstruction, `.icon` and Xcode integration, alternate icons, tvOS or visionOS asset catalogs, and App Store icon experiments. Require explicit approval of a named whole-icon version before creating production layers or changing an app project.
---

# Design App Icons

Work like an icon designer first and a production engineer second. Keep exploration fast: create complete images, revise one variable at a time, and obtain explicit approval. For a shipping iPhone, iPad, Mac, or Apple Watch icon, translate the approved design into deliberate sources, finish it in Apple Icon Composer, and validate the compiled result. Never let production silently redesign the approved icon.

## Choose the route

- **Concept or redesign:** run the complete workflow below. Stop after the approved image only when the user explicitly requested concept art or a bitmap deliverable.
- **Production app icon:** treat Icon Composer as the final authoring route for iOS, iPadOS, macOS, and watchOS. Use asset catalogs for tvOS and visionOS.
- **Critique:** inspect the supplied artwork and contexts; return prioritized findings without changing files unless asked.
- **Existing approved artwork:** record it as the visual lock, run the Composer-feasibility gate, and continue to production.
- **Plan only:** describe artifacts and evidence as `Prepared (specification only)`; do not generate or claim files.
- **Experiment:** create meaningfully different hypotheses and read [app-store-experimentation.md](references/app-store-experimentation.md).

Read only the references needed for the task:

- Current canvases, masks, and platform routes: [platform-specifications.md](references/platform-specifications.md)
- Icon Composer controls and Xcode delivery: [liquid-glass-icon-composer.md](references/liquid-glass-icon-composer.md)
- Imagegen prompts, versioning, and revisions: [imagegen-workflow.md](references/imagegen-workflow.md)
- Direction quality and collision review: [visual-language.md](references/visual-language.md)
- Small-size, context, and evidence rules: [qa-and-evidence.md](references/qa-and-evidence.md)
- Production handoff: [delivery-and-handoff.md](references/delivery-and-handoff.md)
- Official sources and claim boundaries: [sources.md](references/sources.md)

## Default workflow

`Brief → category collision scan → 1–2 whole-icon directions → targeted revisions → explicit visual approval → Composer-feasibility gate → deliberate layers → Icon Composer → Xcode and context validation`

The two gates are mandatory. Do not merge visual approval with technical validation.

### 1. Establish the smallest useful brief

Collect only decisions that change the design:

- app name, category, and core promise in one phrase
- audience and desired emotional signal
- target Apple platforms and minimum releases
- owned recognition anchors and prohibited changes
- input-image roles: edit target, identity anchor, style reference, competitive reference, or context screenshot
- whether the request ends at concept art or requires a shipping app icon

State safe assumptions and continue. Ask only when a missing choice would materially change identity or delivery.

### 2. Check category collision

When web access is available and the task is not private/offline, inspect current category neighbors before generation. Record recurring metaphors, silhouettes, palettes, and compositions. Compare in monochrome as well as color. Do not copy or redistribute competitor art.

Define one recognition anchor and one collision to avoid. Reject a direction that is attractive but interchangeable with AI, photo, finance, chat, or utility icons in its category. Read [visual-language.md](references/visual-language.md).

### 3. Explore complete icons

Use built-in Imagegen and read [imagegen-workflow.md](references/imagegen-workflow.md).

Generate one complete square icon per call. Produce:

- **one direction** when the brief already specifies a strong metaphor;
- **two genuinely different directions** when the identity is unresolved.

Do not automatically generate three directions. Do not generate isolated components, exploded diagrams, SVGs, or `.icon` files during exploration. Favor bold, frontal, source-friendly compositions that can later become no more than four Composer depth groups, but judge the whole icon before its layer plan.

Present every retained candidate with the compact review contract in `assets/concept-review-template.md`:

- stable version ID
- one-line concept
- locked invariants
- the single changed variable
- full-size image and 32 px preview
- main collision or small-size risk
- one direct question: revise one element or explicitly approve this version

Do not overwrite versions. For revisions, edit the selected image and repeat its locked invariants. Change one dimension when practical: metaphor, silhouette, composition, palette, depth, or material. If the edit drifts, return to the last accepted version.

Keep status `Exploring — not approved` until the user explicitly approves a named version. Do not infer approval from silence, “better,” “interesting,” or another variation request.

### Gate A — Lock visual approval

Accept clear equivalents such as “I approve B3,” “this is the one,” or “proceed with this version.” Record the named artifact, approval date, SHA-256 when local, recognition anchor, silhouette, composition, palette, and protected invariants.

For project-bound production, copy `assets/design-approval-template.yaml` into the project and set production authorization only for the approved route. A request made before the concept loop may authorize production after approval; it never authorizes skipping approval.

Apply this same gate to the skill’s own icon, repository branding, examples, and social imagery. Never publish a generated identity in the same turn that first presents it unless the user explicitly approves that named version.

### Gate B — Decide whether the design can become a faithful Composer icon

After approval, create a minimal layer plan. Classify every visible effect:

- **source geometry or intrinsic texture:** preserve in SVG or PNG;
- **alpha-edge translucency:** preserve only when the source boundary survives varied backgrounds;
- **platform material:** recreate in Icon Composer, including dynamic specular, blur, refraction, translucency, and inter-group shadow.

Composer-compatible designs normally have a frontal view, clearly defined edges, bold forms, simple fills, and one to four meaningful depth groups. Integrated painterly lighting, fur, complex 3D perspective, soft shared glow, or inseparable reflections are warning signs.

If a faithful translation is possible, continue. If it requires changing a protected invariant, create a clearly labeled `Composer-adapted production concept`, show it as a new version, and return to Gate A. If the user prefers exact pixels over adaptation, use the flattened asset-catalog fallback and report that Icon Composer was not used. Never call degraded decomposition progress.

### 4. Reconstruct deliberate sources

Prefer SVG for exact curves, symmetry, recoloring, and scaling. Use PNG for mesh gradients, raster texture, or unsupported SVG features. Do not auto-trace and ship noisy Imagegen geometry.

Use the fewest sources that preserve control:

1. redraw the recognition anchor and essential negative space;
2. keep every source on the complete Apple canvas;
3. use numbered names from back to front;
4. remove the platform mask, background fills, gradients, blur, shadow, bevel, specular, and refraction that Composer should own;
5. convert essential text to outlines, but prefer no text;
6. recompose the sources and compare them with the approved image at 1024 px and 32 px.

Use separate Imagegen calls for raster layers only as a rare post-approval route. Verify real alpha and shared alignment with `prepare_raster_layer.py` and `compose_raster_layers.py`. Reject checkerboards, halos, changed lighting, or detached glow.

### 5. Author in Icon Composer

Use the actual Apple app. Do not hand-author or rename a folder into a `.icon` file.

1. Select only the supported platforms in the Document inspector.
2. Set the canvas background in Composer when a solid color or gradient is sufficient.
3. Import SVG/PNG sources and organize them into a maximum of four depth groups, bottom to top.
4. Use **Individual** when layers in a group need separate material edges; use **Combined** when the group should behave as one glass object.
5. Tune Color, Liquid Glass, and Composition independently. Keep specular on unless it harms the design; adjust refraction, blur, translucency, and shadow with restraint. Disable Effects on layers that must remain opaque or flat.
6. Author and inspect Default, Dark, and Mono. From Mono, preview Clear light/dark and Tinted light/dark. Keep the recognition anchor consistent.
7. Preview supported platforms, current grid, small sizes, varied wallpapers, and multiple lighting angles. Use platform-specific position or scale only for optical consistency.
8. Export a flattened marketing image when needed, but preserve the `.icon` as the production source.

Read [liquid-glass-icon-composer.md](references/liquid-glass-icon-composer.md) for the control model, exact preparation rules, and evidence checklist.

### 6. Integrate and test

Before changing Xcode, inspect the current app-icon source, target settings, minimum releases, alternates, and existing asset catalogs. Preserve the previous source until the new result builds and is reviewed.

Add the Composer file to the target and ensure **App Icons and Launch Screen → App Icon** matches its filename without the extension. The current Xcode toolchain uses the matching `.icon` instead of the existing `AppIcon` asset catalog and generates earlier-release images from it. Keep asset catalogs when exact historical artwork must remain.

Validate separately:

1. static source and 16–256 px previews;
2. Composer platforms, appearances, wallpapers, lighting, and scale;
3. Xcode build and target selection;
4. Simulator surfaces: Home Screen, search, Settings, App Library, notifications, and Dock where applicable;
5. named physical devices and supported OS releases when available.

Run deterministic preflight:

```bash
python3 scripts/icon_qa.py path/to/icon.png \
  --platform ios \
  --role flattened \
  --preview-dir work/icon-previews \
  --report work/icon-audit.json
```

The generated appearance and context boards are heuristics, not Apple renders. Read [qa-and-evidence.md](references/qa-and-evidence.md).

## Acceptance rubric

Do not call a production icon complete unless:

- one dominant silhouette and recognition anchor survive at 32 px;
- no essential meaning depends on text, thin lines, or micro-detail;
- current category collision was considered;
- the approved image and reconstructed proof match at full size and 32 px;
- Composer Default, Dark, Mono, Clear, and Tinted previews remain recognizable;
- supported masks and platform variants preserve optical balance;
- Xcode builds the intended `.icon` and the result is observed in requested contexts;
- every untested surface is named honestly.

## Status language

Always separate:

- **Validated:** directly observed with named artifacts, commands, versions, or screenshots.
- **Prepared:** files exist but still require the named import, build, runtime, device, or store step.
- **Not tested:** Composer, Xcode, Simulator, device, older-release fallback, App Review, or conversion outcomes not actually observed.

Never promise App Review approval, ranking, or conversion lift.

## Platform boundaries

- Icon Composer: iOS, iPadOS, macOS, watchOS, and App Store representation.
- Asset catalogs: tvOS layered parallax and visionOS layered 3D icons.
- Alternate icons require their own appearance variants where Apple requires them and remain subject to review.
- A concept bitmap is not editable vector geometry, a valid `.icon`, or proof of runtime behavior.
