---
name: viewport-perf
description: >-
  Investigate and optimize Blunder editor viewport performance: Skia present,
  CPU readback, zero-copy path, partial repaint, and frame pacing. Use when
  editor FPS is low or viewport rendering is slow.
---

# Viewport performance

## Symptom pattern

Low editor FPS often comes from **full-window Skia composite + CPU pixel readback** every frame, not only 3D draw cost.

## Per-frame data flow

```
RenderSystem::tick
  → ForwardRenderPath (offscreen Vulkan RT)
  → copyColorToBuffer (staging) OR zero-copy VkImage
  → pollAndPresent / pollZeroCopyAndPresent

SlintSystem::update
  → SkiaRenderer.render() (composite + Present on HWND)
  → Image control samples viewport pixels (readback or borrowed texture)
```

Read `docs/agents/render-pipeline.md` before changing code.

## Key files

| File | Role |
|------|------|
| `engine/src/runtime/function/render/render_system.cpp` | Offscreen pass, readback, present pacing |
| `engine/src/runtime/function/ui/viewport/slint_viewport_sink.cpp` | Viewport image into Slint |
| `engine/src/runtime/function/slint/slint_system.*` | Skia composite, dirty regions, tiered pacing |
| `docs/agents/render-pipeline.md` | Authoritative flow + env toggles |

## Investigation checklist

1. **Confirm bottleneck** — Skia `render()` vs Vulkan scene vs readback (`copyColorToBuffer`).
2. **Readback path** — default CPU staging; check if zero-copy is available (`viewportUsesSharedDevice()`).
3. **Partial Skia repaint** — viewport-only dirty rect vs full-window refresh (resize/invalidate forces full).
4. **Present pacing** — tiered interactive/idle floors plus `BLUNDER_EDITOR_VIEWPORT_PRESENT_MS`.
5. **Editor toggles** — shadows, overlay AA, render scale (see render-pipeline doc).
6. **Validation layer** — blocks shared-device zero-copy in debug; try `BLUNDER_VK_VALIDATION=0` to test zero-copy.

## Environment toggles

| Variable | Effect |
|----------|--------|
| `BLUNDER_VIEWPORT_ZERO_COPY=1` | Opt in to GPU texture path (no CPU readback) when shared device works |
| `BLUNDER_VK_VALIDATION=0` | Enable zero-copy testing in debug builds |
| `BLUNDER_SLINT_PARTIAL=0` | Disable partial Skia viewport repaint |
| `BLUNDER_EDITOR_VIEWPORT_PRESENT_MS=50` | Min ms between Skia composites while viewport updating (default 50) |
| `BLUNDER_EDITOR_VIEWPORT_INTERACTIVE_MS=33` | Composite request/present floor while interacting (~30 Hz) |
| `BLUNDER_EDITOR_VIEWPORT_IDLE_MS=100` | Composite request/present floor when idle (~10 Hz) |
| `BLUNDER_EDITOR_VIEWPORT_INTERACTIVE_HOLD_MS=150` | Ms to stay interactive after input stops |
| `BLUNDER_EDITOR_RENDER_SCALE=0.75` | Render 3D at reduced resolution |
| `BLUNDER_EDITOR_SHADOWS=1` | Enable shadow pass (expensive) |
| `BLUNDER_EDITOR_OVERLAY_AA=1` | Full-scene overlay AA (expensive) |

## Optimization priorities (typical)

1. Avoid full-window Skia composite when only viewport changed.
2. Eliminate or reduce CPU readback (zero-copy when validation off).
3. Throttle present rate during continuous camera motion.
4. Reduce offscreen resolution via render scale.
5. Disable expensive editor-only passes unless needed.

## Validation

1. `cmake --build build/vs2026-debug --config Debug --target engine_editor`
2. Run `engine_editor`; orbit/pan in viewport; compare FPS with toggles.
3. Confirm viewport still displays correctly (no black/corrupt regions).

Use `/validate` or `/render-change` for full workflow.
