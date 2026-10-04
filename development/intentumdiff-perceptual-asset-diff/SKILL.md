---
name: intentumdiff-perceptual-asset-diff
description: >-
  The IntentumDiff perceptual image/asset diff — how binary assets are compared and visualised.
  Use this whenever you work on image diffing, the asset viewer, or the interactive comparison
  UX (side-by-side / onion / swipe / difference, marching-ants lasso, blink comparator,
  interactive hotspots, channel histograms), or when extending perceptual diff to new media
  (video / audio / other binary). It covers the strict split — ALL pixel work happens in the
  Rust engine (`crates/rust-core-host/src/asset_diff.rs`), the webview only renders artifacts
  and draws SVG overlays — plus the data shapes and the performance gotcha (release build).
  Read intentumdiff-architecture and intentumdiff-vscode first.
---

# IntentumDiff — Perceptual asset diff

For images (and, on the roadmap, other binary media), IntentumDiff shows a *perceptual*
comparison instead of a text diff. The hard architectural rule: **all decode/compute happens
in the Rust engine; the webview does no image processing** — it renders engine-produced PNG
artifacts and draws lightweight SVG/CSS overlays on top.

## Engine side (`crates/rust-core-host/src/asset_diff.rs`)

`diff_asset_image_value` (and the git-driven `diff_git_assets`) produce, for a before/after
pair, all of:
- **Metrics:** MAE, RMSE, pixels-changed.
- **Layers/artifacts (PNG):** `before`, `after`, `diff`, `mask`, `overlay`, `heatmap`.
- **`hotspots`:** changed regions with pixel `bbox`, normalized `centroid`, and `severity`;
  optional `hotspot_navigation.order`.
- **`histograms`:** 16-bin per-channel (R/G/B/brightness, +alpha) delta arrays.
- **`comparison_dimensions`:** `{ width, height }` — the reference frame for normalizing
  hotspot bboxes into the viewer.

Decode cost is bounded (`max_decoded_pixels`) so large/adversarial media fails fast. Never send
media to a cloud LLM — asset diff is fully on-device.

## Webview side (`plugins/vscode/src/reviewWebviewModel.ts`)

`assetModeViewer(...)` renders four modes and the overlays. All are pure DOM/CSS/SVG:
- **Side-by-side / Onion (opacity + blink) / Swipe (curtain) / Difference (heatmap).**
- **Lasso (marching ants):** an SVG `rect` per hotspot with animated `stroke-dashoffset`,
  drawn over **both** panes so the same change is locatable on LHS and RHS. Rectangles come
  from `hotspot.bbox` normalized by `comparison_dimensions` (left=`x/W`, top=`y/H`, …).
- **Blink comparator:** `setInterval` toggling the onion top layer opacity 0↔1.
- **Interactive hotspots:** list items + on-image markers are clickable; selection pulses the
  lasso, dims others; prev/next + arrow keys cycle; uses `hotspot_navigation.order` when present.
- **Histograms:** per-channel SVG bar charts from the delta arrays (theme-tinted).

Pure helpers to reuse: `assetLasso(hotspots, compDims, options)`, `assetHistogramBars(histograms)`,
`assetHotspot`, `assetMarker`. Client interactions follow the existing `setAssetMode` /
`setAssetOpacity` delegation pattern (no round-trip to the engine).

**Threading gotcha:** `comparison_dimensions` must be parsed in `assetDiffFromMetadata` and
threaded from the call site into `assetModeViewer` — the model historically dropped it, which
breaks overlay alignment. Wrap each `<img>` in an inline-block box sized to the image so
`inset:0` overlays align over `object-fit:contain`.

## Routing & lifecycle

Image-extension files route to asset review instead of the text semantic diff
(`isImageLikePath`, and the engine's `content_type` category). Clicking an image's Evidence
must open the asset viewer, not an `intentumdiff-base:` text diff.

## Performance

The perceptual pipeline is compute-heavy (PNG deflate encoding + per-pixel passes). It is
~20–50× slower on a **debug** core — always build with `maturin develop --release` (a 1050×700
image drops from ~6 s to ~0.3 s). The VS Code compare is also non-blocking: the preview shows
instantly and upgrades when the engine result is ready. See `intentumdiff-architecture` (build)
and `docs/PERCEPTUAL_ASSET_DIFF.md`.

## Roadmap: video / audio / other binary (`docs/BACKLOG.md`)

Extend the pattern by content-type routing, keeping all decode/compute in Rust and on-device:
- **Video:** sample keyframes, run the per-frame image pipeline, add a timeline scrubber with
  changed-frame markers (needs a vetted ffmpeg-backed decode dependency).
- **Audio:** waveform + spectrogram comparison (prefer pure-Rust `symphonia` + `rustfft`).
- **Other binary:** a routed fallback (size/format delta) for formats with no perceptual
  comparator. Bound decode cost like the image `max_decoded_pixels` cap.

## Tests / verify

`test/reviewWebviewModel.test.ts` asserts the Swipe tab, blink controls, lasso `<svg>` with
per-hotspot `data-asset-hotspot`, histogram `<svg>` bars, and that the panel script executes.
For interaction, use the panel-render harness (see `intentumdiff-vscode`) with a real image
injected as every artifact, served for the Claude Preview MCP; resize narrow (~760px) to
confirm no overflow regression. Rust side: `cargo test -p rust-core-host`.
