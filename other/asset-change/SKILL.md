---
name: asset-change
description: Change agent-office's Blender-built 3D assets — the atrium, Main Street, wings and their themes, garden, cap, furniture kit, lighting/bake, the character mesh, rig or animation clips, the manifest or the graphics contract. Use for any edit under assets/ (assets/blender/**, assets/build.mjs, assets/validate*.ts), to docs/graphics-contract.md, or for anything in packages/web/public/assets/.
---

# Change the 3D assets

Rules: `SCENE.md` (budgets, animation rules, no logos), `TESTING.md` (asset validation), `docs/graphics-contract.md` (the contract both sides follow).

1. **Contract first.** If anchors, roles, clip names, coordinates or budgets change, edit `docs/graphics-contract.md` additively and plan the renderer side (`packages/web/src/app/manifest.ts` and friends) in the same change. Extend the fixture tests in `assets/validate.test.ts` red-first.
2. **Edit the scripts** in `assets/blender/**` (modules, furniture kit, materials, themes, character). Never edit a `.glb` by hand or export from the GUI: every shipped file comes from `make assets`.
3. **Iterate fast:** `make assets-draft` (low bake samples, small lightmaps, gitignored output).
4. **Look at it:**
   - With the Blender MCP connected (optional: `claude mcp add blender --scope user -- uvx blender-mcp`, then **Connect** in Blender's MCP sidebar), use `get_scene_info` and viewport screenshots to review proportions, materials and lighting. Use only the Poly Haven integration; leave Hyper3D and Sketchfab off.
   - `make asset-previews` renders Eevee stills of every module into `assets/previews/`. Read the images.
5. **Test:**
   - `make assets-test`: Blender-side checks (naming grammar, counts, loop pose continuity, ≤ 4 weights, applied transforms, no text objects except the runtime sign).
   - `pnpm vitest run --project unit assets/validate.test.ts`: `gltf-validator` 0 errors, budgets, anchors, nav connectivity, clips, ≤ 45 MB.
6. **Final build:** `make assets` (final bake). Then `/run-office` and `make screenshots` to check the assets in the app, and `make perf` if triangle counts or materials changed (≥ 55 fps at Medium with 150 agents).
7. **License and branding checklist** before handing off:
   - Every new texture or HDRI is CC0 (Poly Haven), pinned by asset id and SHA-256, and listed in `assets/LICENSES.md` with its URL.
   - No logos, trademarks or real company names anywhere (textures, decals, text objects, material names). Wing signs stay blank planes; the runtime draws the provider id.
   - No AI-generated or Sketchfab models.
8. **Git LFS:** `.glb`, lightmap `.png` and `.hdr` files under `packages/web/public/assets/`, plus `assets/out/**` and `assets/previews/**`, are LFS files (`.gitattributes`). Make sure `git lfs install` has run before the human commits. Prepare the commit commands; never commit yourself.

2D RPG mode: see `docs/2d-architecture.md`. The pure logic is in `web/src/app/pixel/*`, the Canvas2D drawing in `web/src/adapters/pixel/*`, the art in `assets/pixel/src` (`make pixel-assets`), and the floor plans come from `make assets-plan`. Check both modes with `pixel.spec.ts` and the existing 3D specs.
