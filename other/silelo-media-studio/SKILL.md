---
name: silelo-media-studio
description: Build and verify media tools for SILELO-style applications. Use when adding source-linked web search, bounded image batches, browser-side ONNX vision, or video scene manifests while keeping media limits and provider capabilities explicit.
---

# SILELO Media Studio

## Scope

Use this skill for media-tool features. Keep it alongside—not instead of—`silelo-ai-studio-workflow`. This package does not promise that a provider exists, that a long video is rendered, or that a large batch has completed.

## Source-linked Web Search

Call an approved server-side search source and normalize results to `{ title, url, snippet }`. Allow only `http`/`https` URLs, sanitize text, preserve the source domain, and render outbound links with `target="_blank"` and `rel="noopener noreferrer"`. Do not fabricate results or citations.

## Image Batches

Validate prompt and count, then apply a provider-specific upper bound per run. Return and display both `requested` and `completed`. For large workloads such as 100 images, create durable queued jobs with progress, cancellation, retries, and persisted status; do not fire all requests in parallel or describe a queue as completed before artifacts exist.

## Browser-side ONNX Vision

Verify model input shape, preprocessing, output labels, and class limitations from the actual model. Serve model and runtime assets from deployment-safe URLs, configure compatible WASM paths, and state whether images stay local or are uploaded. Test with a permitted sample image and report runtime failures honestly.

## Video Projects

Treat long-form video as `plan → render clips → review → merge`. A scene manifest may contain title, duration, scene index, start time, visual prompt, and narration, but it is not a rendered video. Require a connected video provider before offering render or merge controls. Report the maximum verified clip/project size rather than inventing an hour-long output.

## Proof Before Delivery

Test web search URL parsing, image batch bounds, ONNX model loading where feasible, video scene count/timeline generation, and success/error notifications. Verify the relevant tool in the browser and state the precise capability level: plan-only, queued, provider-connected, or rendered.
