---
name: minecraft-skin-studio
description: Draft, clean, preview, register, or build a Minecraft Java skin workflow, including the bundled `apps/minecraft-skinbar` menu bar app. Use when Codex needs to turn a skin idea into launcher-ready files, wire the local Minecraft Launcher skin library, render previews, or refine the repo-native macOS skin workflow.
---

# Minecraft Skin Studio

Use this skill when the user wants a Minecraft Java skin workflow, not a server workflow. If the current repo contains `apps/minecraft-skinbar`, use that workspace by default when the request involves a menu bar app, app UI, or local macOS workflow changes.

## Quick Start

1. Treat the launcher-ready deliverable as a `64x64` skin PNG plus a preview image.
2. If the request touches the bundled app, run `bash scripts/run_minecraft_skinbar.sh doctor` first.
3. Run `bash scripts/run_minecraft_skinbar.sh inspect` before editing the app.
4. Use `bash scripts/run_minecraft_skinbar.sh generate` after changing `apps/minecraft-skinbar/project.yml`.
5. Use `bash scripts/run_minecraft_skinbar.sh typecheck` for a fast shell and Python syntax pass before the helper smoke test.
6. Use `bash scripts/run_minecraft_skinbar.sh test` after changing the Python helper, preview rendering, or launcher registration contract.
7. Use `bash scripts/run_minecraft_skinbar.sh build` after app UI, model, CLI wiring, or keychain changes.
8. Use `bash scripts/run_minecraft_skinbar.sh run` when you need the local menu bar app relaunched.
9. Prefer registering skins through the launcher's local custom-skins file instead of brittle UI clicking.
10. If the user has a prompt only, generate a draft skin sheet first, then clean it into a usable `64x64` skin.
11. Be honest that prompt-to-perfect skin generation is still draft-quality and may need a second pass.
12. If the user already has a PNG, skip generation and register it directly.

## Workflow

### Choose The Lane

- Use `minecraft-skinbar-workspace` when the user wants to build, troubleshoot, or refine the bundled macOS app in `apps/minecraft-skinbar`.
- Use `go` for the full flow: prompt draft, clean skin, preview, and launcher registration.
- Use `generate` when the user only wants files and iteration.
- Use `register` when they already have a valid skin PNG.
- Use `render-preview` when they want a quick visual check without touching the launcher.

### Work The Bundled App First

- Read `references/project-map.md` before editing the app workspace.
- Prefer the local runner before typing `xcodegen` or `xcodebuild` manually.
- Keep `Minecraft Skin Bar` compact and menu-bar-first.
- Preserve the current split:
  - `SkinBarModel` owns local state, launcher-facing actions, and keychain-backed API key handling
  - `SkinStudioCLI` shells out to `minecraft_skin_studio.py` through `uv`
  - `MenuBarView` stays focused on prompt, import, preview, and launcher handoff
- Keep OpenAI API keys in Keychain or environment variables only. Do not add plaintext config storage.
- Keep skin output local in `~/Pictures/Minecraft Skins` unless the user explicitly asks for another path.
- The current app project has no Xcode unit-test target, so use `typecheck` for the fastest helper sanity pass, `test` for the helper smoke path, and `build` as the strongest native validation.

### Skin Rules

- Java launcher skins should be treated as `64x64` PNG files.
- Keep the launcher-facing flow simple:
  - skin PNG
  - preview PNG
  - custom skin entry in `launcher_custom_skins.json`
- If the user asks for direct launcher automation, prefer the local JSON registration path first.
- Do not pretend generic image generation is guaranteed to produce a perfect UV layout on the first try.

### Required Deliverables

- A launcher-ready skin PNG path.
- A preview image path.
- A clear note on whether the skin was registered into the local launcher library.
- If generation was used, a short quality note about whether the result looks usable or needs another pass.

### Editing Guidance

- Keep prompts visual and specific: outfit, palette, theme, face detail, accessories.
- Use `wide` unless the user explicitly wants `slim`.
- Prefer simple names for launcher entries.
- Do not overwrite an existing launcher skin entry unless the user clearly wants a replace/update behavior.
- If you edit the bundled app, preserve the local-first workflow:
  - generate or import
  - preview locally
  - register into the launcher JSON
  - open the launcher or reveal the saved files
- Do not pretend the app can silently inject skins into Mojang services or change the active skin without the launcher's own local flow.

## Resources

- `scripts/minecraft_skin_studio.py`: generate, clean, preview, and register skins.
- `scripts/run_minecraft_skinbar.sh`: local doctor, inspect, generate, typecheck, test, open, build, and run helper for `apps/minecraft-skinbar`.
- `references/launcher-flow.md`: launcher storage path, workflow boundaries, and practical limits.
- `references/project-map.md`: bundled app target map, main files, and validation notes.
- `../../apps/minecraft-skinbar/`: the bundled macOS menu bar app workspace.
- `agents/openai.yaml`: UI metadata and default invocation prompt.
