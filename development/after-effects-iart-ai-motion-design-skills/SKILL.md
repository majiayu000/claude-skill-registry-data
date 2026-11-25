---
name: after-effects
description: This skill should be used when the user asks anything about Adobe After Effects — to "write an After Effects expression", "make a wiggle / loopOut / inertial bounce", "rig a control with a slider / null", "build a MOGRT / Essential Graphics template", "export AE to Lottie or Media Encoder"; OR to "export from After Effects", "export with transparency / an alpha channel", "fix a black background on export", "choose ProRes vs H.264", "which codec / what bitrate for 1080p / 4K", "stop H.264 disappearing from the Render Queue"; OR when "After Effects is slow / laggy / crashing / froze", "RAM preview won't play in real time", "AE is using all my memory / render takes forever", "how do I speed up After Effects"; OR to "organize my After Effects project", "relink missing footage", "fix broken links after moving files", "set a folder structure / naming conventions", "batch rename layers", or "write an ExtendScript / .jsx script". Covers expressions & rigging, export recipes, performance triage, and project hygiene.
version: 0.1.0
---

# After Effects

After Effects is GUI software, so this skill delivers knowledge and ready-to-paste assets — expressions, rig setups, export checklists, diagnostic flows, naming schemes, and ExtendScript — rather than a rendered file. It is a hub covering four domains; route to the matching reference for depth and complete recipes.

## Routing

| If the user wants to… | Go to |
|---|---|
| Write/debug an expression, rig sliders & nulls, build a MOGRT, export to Lottie | `references/expressions.md` (deep cookbook in `references/expression-library.md`) |
| Choose a codec/container, export with alpha, fix a black background, set bitrate, recover H.264 | `references/export-recipes.md` |
| Fix slow/laggy previews, slow renders, crashes, freezes, out-of-memory | `references/performance-triage.md` |
| Organize the project, relink missing footage, set naming/folders, batch-automate with .jsx | `references/project-hygiene.md` |

The `.jsx` automation scripts live in `scripts/`.

## Expressions & rigging

Expressions are JavaScript evaluated on the property they are pasted on; `value` is that property's value, `time` is comp time in seconds, and `index`, `thisLayer`, `thisComp` are in scope. An expression overrides keyframes unless it incorporates `value`.

```js
wiggle(2, 30);            // 2 wiggles/sec, amplitude 30 (property units)
loopOut("cycle");         // repeat keyframed range forever; "pingpong" / "offset" / "continue"
seedRandom(index, true);  // stable-but-unique per layer (timeless) before random()/wiggle()
thisComp.layer("Lead").transform.position.valueAtTime(time - 0.2 * index);  // staggered echo
```

Inertial bounce (overshoot/settle after the last keyframe) and the full loop/wiggle/rigging set are in `references/expressions.md`.

Rig controllable motion: add a null with **Slider / Checkbox / Color / Angle / Point** control effects, then reference them and parent transforms to drive many layers from one.

```js
ctrl = thisComp.layer("Controls");
amt  = ctrl.effect("Intensity")("Slider");   // Checkbox → 1/0, Color → [r,g,b,a]
value * amt;
```

Expose those controls via **Window → Essential Graphics** and **Export Motion Graphics Template** (.mogrt) for Premiere/AE editors.

## Export recipes

Two engines, and choosing wrong is the root of most export confusion:
- **Render Queue (RQ)** — masters/intermediates: ProRes, image sequences, lossless, alpha.
- **Adobe Media Encoder (AME)** — delivery: H.264 MP4, H.265, social presets.

Since AE CC 2014/2015 the native **H.264 output module was removed from the RQ** — make MP4s in AME, not the RQ. **H.264/MP4 cannot store alpha**, so a transparent comp exported to H.264 always fills with black; that is the classic "black background" complaint and not a bug. For transparency use **ProRes 4444**, a **PNG/TIFF sequence**, or **HEVC-alpha (Safari) + VP9/WebM-alpha (Chrome)**, with Output Module **Channels: RGB + Alpha**.

Quick targets: editor handoff → **ProRes 422 HQ**; master/grade or alpha → **ProRes 4444**; web/social/client → **H.264 via AME**, VBR 2-pass (~10–16 Mbps 1080p, ~35–45 Mbps 4K). Full matrix, social specs, and step-by-step alpha exports in `references/export-recipes.md`.

## Performance triage

Work top-down by symptom, cheapest fix first, and stop when it clears. Most settings are in `Edit > Preferences` (Win) / `After Effects > Settings` (Mac).

- **Slow previews:** Half/Third resolution → enable **Multi-Frame Rendering** → raise RAM allocation (leave ~6 GB for OS) → Adaptive fast previews → purge cache → Disk Cache on SSD/NVMe → solo heavy layers/effects → HW-accelerated decode → proxy heavy comps.
- **Slow renders:** confirm MFR on → RQ for masters / AME for delivery → HW decode H.264 → pre-render slow precomps → cheaper effects → transcode long-GOP to ProRes.
- **Crashes/freezes:** purge + empty disk cache → update **NVIDIA Studio** (not Game-Ready) drivers → reset prefs (`Ctrl/Cmd+Alt+Shift` on launch) → pull third-party plugins → free disk space → disable MFR if MFR-specific → roll back AE after a bad update.

MFR needs several GB RAM per active core. Ordered flows, exact preference paths, and the proxy workflow are in `references/performance-triage.md`.

## Project hygiene

Keep projects organized, portable, and automatable.

- **Folders:** numeric-prefixed bins (`01_Comps`, `02_Precomps`, `03_Footage`, …, `99_Old`) for stable sort order.
- **Naming:** `PROJECT_section_descriptor_v01`; precomps `PRE_`; rename solids/nulls to their role (`CTRL_master`); no spaces/special chars for farm/cross-OS safety.
- **Broken links:** AE references footage by path, so moving files breaks links. Double-click a missing item → **Replace Footage > File** and AE relinks the whole folder at once; enumerate with `File > Dependencies > Find Missing Footage`. **Always hand off projects via `File > Dependencies > Collect Files`**, never a bare `.aep`.
- **ExtendScript (.jsx):** wrap batches in `app.beginUndoGroup(...) / app.endUndoGroup()`; apply effects by **matchName** (e.g. `"ADBE Gaussian Blur 2"`), not the display name. Ready scripts: `scripts/batch-rename.jsx`, `scripts/sequential-offset.jsx`, `scripts/apply-effect-to-layers.jsx`.

Full naming scheme, label-color system, relink/Collect-Files/Reduce workflows, and scripting setup in `references/project-hygiene.md`.

## Reference files

- `references/expressions.md` — expressions, rigging, MOGRT, Lottie/Media Encoder basics.
- `references/expression-library.md` — deeper expression cookbook: tuned inertial bounce, all loop variants, advanced wiggle, valueAtTime echoes, seedRandom grids, full rigging + coordinate spaces, MOGRT and Lottie/Bodymovin steps, Media Encoder presets.
- `references/export-recipes.md` — full codec/alpha/bitrate matrix, per-platform social specs, step-by-step transparency exports, AME preset cautions.
- `references/performance-triage.md` — ordered preview/render/crash flows, preference paths and values, MFR/GPU/disk-cache tuning, pre-render & proxy workflow.
- `references/project-hygiene.md` — folder template, naming and label systems, relink/Collect Files/Reduce details, scripting setup.
- `scripts/batch-rename.jsx`, `scripts/sequential-offset.jsx`, `scripts/apply-effect-to-layers.jsx` — ExtendScript automations.
</content>
