---
name: unity-optimize-web
description: Measure and optimize Unity web builds for transfer size, startup, memory and browser execution without changing engines.
engines: [UNITY]
---

# Unity Optimize Web

## When to use

Improve a selected Unity project's web-player startup, delivery size, memory or runtime performance. This skill retains Unity as the engine; it does not replace the game with a browser-engine implementation.

## Activation and inputs

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-optimize-web`; require effective `UNITY` compatibility before edits, builds or browser launches. Honor permitted output scope. Inspect actual Editor version, web build module, selected packages, build configuration, hosting control and supported browser/device matrix. Keep observations and reports in the resolved `.hephaera/.cache/`.

## Workflow

1. Establish comparable development and release baselines with source/package identities, scenes, stripping settings, compression, cache state and representative devices. Set project budgets for transferred bytes, first interaction, steady/peak memory and frame-time percentiles.
2. Use BuildReport and browser network traces to attribute cost before changes. Separate download bytes, decompressed files, WebAssembly memory, browser resources and Unity allocations; a smaller file does not prove lower peak runtime memory.
3. Remove measured unused content through owned scene/asset and stripping decisions. Verify reflection, serialization, fonts, variants and dynamically loaded content survive release stripping. Do not enable aggressive stripping without runtime coverage.
4. Match build compression to server `Content-Encoding`, MIME and cache behavior. Test an actual HTTP-served player, cold/warm loads, content-hash upgrades and cache invalidation. Use a decompression fallback only as an explicit hosting tradeoff.
5. Bound initial content and concurrent downloads/decode work. Review texture/audio import, allocation hot paths and memory growth on target browsers. Gate threading and platform features against the installed Editor and deployment isolation requirements.
6. Validate focus, resizing, pointer lock/fullscreen, input, user-gesture audio, lost context, suspension and offline/error UI in real browsers. Browser evidence covers this web player; native player UI/audio still requires native testing.

Read [web build measurement and delivery](references/web-delivery.md) for report scope, compression and acceptance evidence.

## Output and verification

Deliver measured before/after builds, the change attribution, HTTP/browser evidence and remaining budgets/limitations. Keep build output outside runtime source assets and do not deploy or publish automatically. Missing platform modules, host control or representative devices block the affected claims; an Editor build receipt does not certify startup or browser gameplay.
