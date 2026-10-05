---
name: comfyui-workflow-ui-policy
description: ComfyUI workflow visual layout, subgraph nesting, proxyWidgets exposure, and group organization policy. Use this skill EVERY TIME you create, edit, or save.
---

# ComfyUI Workflow UI Policy

## When to Apply

**EVERY TIME** a ComfyUI workflow JSON is created or modified, run the UI policy pass before save. This is a non-negotiable consistency layer — the workflow's structural visuals must match the project standard regardless of who/what made the change.

Trigger phrases that activate this skill:
- "workflow düzenle / edit"
- "node ekle / remove"
- "rebuild workflow"
- "yeni workflow"
- "v4 / v5 / new version"
- Any JSON write into the verified `<COMFYUI_ROOT>/user/default/workflows/` directory

## Core Policy

### 1. Subgraph Nest Pattern (from 08 - Pixaroma Subgraph Compact)

**Tech goes inside subgraph. Knobs stay outside.**

#### Inside subgraph (definition):
- UNETLoader, CLIPLoader, VAELoader
- Power Lora Loader (LoRA chain)
- ApplyPuLIDFlux2 + PuLID loaders (if used)
- IdentityFeatureTransferV3 (if used)
- CLIPTextEncode (pos + neg)
- ImageScaleToTotalPixels (ref scale)
- VAEEncode (ref → latent)
- ReferenceLatent / Flux2KleinMultiReferenceLatent
- GetImageSize, ComfySwitch (manual size logic)
- RandomNoise, KSamplerSelect, Flux2Scheduler, EmptyFlux2LatentImage
- CFGGuider, SamplerCustomAdvanced
- VAEDecode
- StringConcatenate (prompt 1+2 merge)
- PrimitiveStringMultiline guide notes

#### Outside (main workflow):
- LoadImage (user upload)
- PrimitiveStringMultiline (Prompt 1 — kimlik/fizik)
- PrimitiveStringMultiline (Prompt 2 — sahne)
- PrimitiveStringMultiline (Negatif)
- Power Primitive (CFG) — user knob
- PrimitiveInt (Steps) — user knob
- PrimitiveBoolean (Manuel boyut) — user knob
- PrimitiveInt (Width, Height) — user knobs
- PrimitiveBoolean (PuLID on/off toggle)
- PrimitiveBoolean (BFS toggle)
- Subgraph instance node (for example, "Model Engine")
- PreviewImage, SaveImage, Image Comparer (rgthree)
- MarkdownNote (Kontrol Paneli)
- Fast Groups Bypasser (rgthree) — optional group toggle

### 2. proxyWidgets (Exposed Controls on Subgraph Node)

The subgraph instance node should expose these widgets to the outer panel (no need to enter subgraph):

```json
"proxyWidgets": [
  ["<UNETLoader_id>", "unet_name"],
  ["<UNETLoader_id>", "weight_dtype"],
  ["<CLIPLoader_id>", "clip_name"],
  ["<CLIPLoader_id>", "type"],
  ["<PowerLoRA_id>", "lora_1"],  // BFS Head
  ["<PowerLoRA_id>", "lora_2"],  // anatomy
  ["<PowerLoRA_id>", "lora_3"],  // snofs
  ["<ApplyPuLID_id>", "strength"],
  ["<IdentityFeatureTransferV3_id>", "preset"],
  ["<KSamplerSelect_id>", "sampler_name"]
]
```

### 3. Group Standards (TR-titled, semantic colors)

| Group | Title | Color | Contents |
|---|---|---|---|
| 1 | 1. Kullanıcı Girdileri | `#6d5aa3` (purple) | LoadImage, prompts, knobs |
| 2 | 2. Model Yükleme | `#2f6f89` (blue) | (inside subgraph) UNET/CLIP/VAE loaders |
| 3 | 3. Referans İşleme | `#2f6f89` (blue) | (inside subgraph) scale, VAEEncode, GetImageSize |
| 4 | 4. Conditioning | `#4f7a45` (green) | (inside subgraph) CLIPTextEncode, RefLatent, StringConcat |
| 5 | 5. Sampling | `#6a54a3` (dark purple) | (inside subgraph) Noise, Sampler, Scheduler, CFGGuider |
| 6 | 6. Çıktı | `#3d7e86` (cyan) | Preview, Save, Comparer |
| 7 | 7. Yüz Kimliği | `#7a2a6a` (magenta) | PuLID chain or face-related |
| 8 | 🎛️ KONTROL PANELİ | `#2a2a5a` (deep blue) | MarkdownNote + Fast Groups Bypasser |

### 4. Node Collapse Rules

`flags.collapsed: true` for ALL tech nodes that are not knobs. Show only titlebar. User clicks to expand.

NEVER collapse:
- LoadImage (must show image preview)
- PrimitiveStringMultiline (text editing)
- Power Lora Loader (LoRA list interaction)
- PreviewImage, Image Comparer (display)
- MarkdownNote (info display)
- Bool/Int primitive knobs (single-click toggle)
- **Adjustable-tech (exception):** keep EXPANDED so the control is visible — `KSamplerSelect` (sampler_name), `IdentityFeatureTransferV3` (preset). See `validate_ui.py` ALLOW_EXPANDED.

### 5. Naming Convention (TR)

- Localized node titles (for example, `Modeli Yükle`, `Referansı Latent'e Çevir`)
- Group titles numbered + TR (`1. Kullanıcı Girdileri`)
- MarkdownNote titles with emoji prefix (`🎛️ KONTROL PANELİ`)
- LoRA filenames, model filenames, prompt content NEVER translated

### 6. Position Layout

Standard layout grid (master + extensions):

```
y\x    -2700      -2200      -1750      -1300      -880       -450       -50
-300                                          KONTROL PANEL (MarkdownNote)
-100   PuLID                                         
       loaders
0      PuLID Apply  USER       MODEL      REF        COND       SAMP       OUTPUT
500    chain       INPUTS      LOADERS    PROCESS    chain      chain      chain
1000                Prompts     
1280                            (knobs row: CFG, Steps, Manual, W, H)
1450                            Face crop chain (if multi-ref)
2050                            Fast Groups Bypasser
```

### 7. File Naming Convention

- Protected master: `<PROJECT>-MASTER.json` or an explicit user-supplied allowlist
- Active workflow: `<PROJECT>-v{N}-{feature}.json`
- Reference workflows: `0{4-9} - {description}.json`
- Archive folder: `_archive/{timestamp}-{purpose}/`
- Analysis folder: `_analysis/{timestamp}-{purpose}.md`

### 8. Geometry & Spacing (overlap-free, symmetric) — enforced by validate_ui.py

- **No node-node overlap.** Rendered AABB must not intersect (collapse-aware: collapsed node ≈ 30px tall bar).
- **No group-group overlap** unless one fully contains another (intentional nesting).
- **Single-group membership.** A node's center lies inside exactly one group.
- **Title-band clearance.** A node's top edge ≥ its group's `y + 34`. Never let nodes sit under the group title band (the user's #1 complaint).
- **Column grid + symmetry.** Fixed x-column pitch (~360px), aligned rows. No flat single-row dumps.
- **Minimal-but-safe gaps.** ~16–40px between neighbours (<8 = cramped, >220 inside a group = wasteful).
- **Node sizing.** Min width ~140px, proportionate; collapse tech nodes so footprint ≈ titlebar.
- Group bounding wraps members + ~16px side/bottom margin + ~40px top (title band).
- Constants (frontend 1.44): node titlebar ≈30, group title band ≈34, collapsed node ≈30.

### 9. Module Toggles (rgthree bypass / mute) — OFF = zero compute

- **Fast Groups Muter** — group nodes ALWAYS↔NEVER (mute = skipped). Use when output not needed downstream.
- **Fast Groups Bypasser** — BYPASS (input passes through). Use to neutralize an inline MODEL/COND patch (e.g. IFT V3) while keeping the chain connected.
- **Mute/Bypass Repeater** — one node dispatches mode to many → feed a Fast Muter/Bypasser for a single dashboard toggle.
- Put toggles in `🎛️ KONTROL PANELİ`. TR titles. Bypass safer for inline patches; mute for whole branches.

### 10. Classic LiteGraph vs Nodes 2.0

- Author/ship in **classic LiteGraph** (stable; all custom nodes work).
- **Nodes 2.0** = Vue render (BETA, logo menu → "Nodes 2.0"). Can BREAK custom-node mappings (frontend #10988). Experimental preview only — never author assuming 2.0.
- Subgraph + parameters-panel widget editing OK in classic on frontend ≥1.24.3 / ≥v0.3.66 (user 1.44.19 → fine).

## Workflow Edit Checklist (mandatory)

Run these checks AT THE END of every workflow JSON modification:

1. [ ] Tech nodes have `flags.collapsed: true`
2. [ ] Knobs (LoadImage, prompts, primitives, Power LoRA) are NOT collapsed
3. [ ] All groups have TR titles + correct color
4. [ ] MarkdownNote control panel exists at top with current version info
5. [ ] No duplicate links (link IDs unique)
6. [ ] No dangling links (all link endpoints exist in nodes)
7. [ ] `last_node_id` and `last_link_id` match actual max
8. [ ] Prompt fields NOT translated
9. [ ] LoRA/model filenames NOT translated
10. [ ] BFS Head LoRA: if `on: true`, MarkdownNote MUST mention `head_swap:` prompt prefix requirement
11. [ ] PuLID strength: if used, must be 0.85-1.05 (never 1.4 — burns at 4-step distilled)
12. [ ] Backup the workflow file to `_archive/` before destructive edits

## Validator Script

Use `scripts/validate_ui.py` to automatically check policy compliance:

```bash
python "<SKILL_ROOT>/scripts/validate_ui.py" \
    "<COMFYUI_ROOT>/user/default/workflows/your-workflow.json"
```

## Subgraph Programmatic Build Helper

See `scripts/build_subgraph.py` for the helper that converts a flat workflow to the nest pattern. It:
1. Identifies tech vs knob nodes by type
2. Generates subgraph UUID
3. Moves tech nodes into `definitions.subgraphs[0].nodes`
4. Creates internal links + IO ports
5. Generates subgraph instance node with proxyWidgets
6. Rewires main workflow

## References

- `references/subgraph-pattern.md` — Deep dive on the 08 Pixaroma subgraph format
- `references/identity-mechanisms.md` — Face transfer mechanisms (PuLID Klein V2, BFS Head, IFT V3, MultiReferenceLatent)
- `references/research-2026.md` — Late 2025/early 2026 research findings on Klein 9B identity preservation

## Hard Rules

- **NEVER** translate prompts, LoRA names, or model filenames.
- **NEVER** modify a verified protected master in place; edit a copy or named version and hash-check the protected source.
- **ALWAYS** backup before destructive edits.
- **ALWAYS** validate after edit (0 missing links, 0 dangling refs).
- **ALWAYS** update MarkdownNote control panel with the new version's behavior.
- **ALWAYS** apply this skill at the END of every workflow change. No exceptions.
