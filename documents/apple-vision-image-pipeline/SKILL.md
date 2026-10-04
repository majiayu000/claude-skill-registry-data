---
name: apple-vision-image-pipeline
description: Build safe Apple image pipelines with ImageIO, CoreGraphics, and Swift-native Vision. Use when decoding, OCR, classification, orientation, color, or encoding.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-31"
  last-reviewed: "2026-08-31"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Vision Image Pipeline

Build one bounded path from bytes to validated pixels and evidence. Treat input, metadata, OCR, and labels as untrusted.

## Decide the contract

Identify every ingress, accepted format, byte/pixel/frame limit, orientation/color convention, concurrency policy, retained evidence, metadata policy, and fallback. Files and clipboard data must share the decoder and validation policy.

## Preserve these invariants

1. Inspect type, count, dimensions, and overflow before full decode; verify decoded dimensions afterward.
2. Bound accumulated bytes, pixels, and concurrent memory; downsample when full resolution is unnecessary.
3. Apply orientation once: either pass source orientation to Vision or render upright pixels and use `.up`.
4. Preserve or deliberately convert color; successful encoding alone proves no fidelity.
5. Give one owner admission, cancellation, and stale-result rejection.
6. Keep OCR candidates/confidence/regions and classifier scores as evidence. Deterministic policy owns thresholds, unknowns, and actions.
7. Check ImageIO creation/finalization, then reopen and validate output.
8. Do not log pixels, OCR, clipboard contents, paths, or metadata. Copy only allowlisted metadata.

## Execute and prove

Read [pipeline-contracts.md](references/pipeline-contracts.md) before changing decode, normalization, Vision, encoding, or privacy behavior.

Prefer Swift-native `RecognizeTextRequest` and `ClassifyImageRequest` with async `perform(on:orientation:)` where the deployment target supports them. If supported OS versions predate those APIs, gate the modern path with availability checks and keep a tested `VNRecognizeTextRequest`/`VNClassifyImageRequest` path or raise the deployment floor deliberately. Keep coordinate transforms explicit and distinguish failure, cancellation, no result, low confidence, and unknown classification.

Read [testing.md](references/testing.md) for hostile-input, orientation/color, source-equivalence, Vision, concurrency, output, and privacy tests. Avoid exact Vision scores unless contractual.

A build or preview proves none of those properties. Stop on unvalidated types, limit/overflow failures, unknowable orientation/color intent, unavailable APIs, or output that cannot be reopened.

For API work, use Xcode `DocumentationSearch` and read [apple-documentation.md](references/apple-documentation.md). Advance review dates only after the corresponding review; Apple-doc review requires a fresh search.

## Review

- Last updated: 2026-08-31
- Last reviewed: 2026-08-31
- Apple documentation reviewed: 2026-08-30

ImageIO, CoreGraphics, and Vision pipeline guidance was reviewed with Xcode MCP `DocumentationSearch`; checked-arithmetic instruction behavior was re-reviewed with a live Codex evaluation. See [Apple documentation evidence](references/apple-documentation.md).
