---
name: package-web-games
description: Package static web-engine games in .NET MAUI for Windows, Mac Catalyst, Android and iOS, with explicit native prerequisites and release evidence.
engines: [AGNOSTIC]
---

## When to use

Use when a web game needs a native application build, platform package or release preparation. Resolve the effective engine first; registered web engines select MAUI automatically. Native engines keep their own exporters.

## Workflow

Read `docs/WEB_GAME_PACKAGING.md` and `.packaging/maui/PACKAGING.md` from the shared baseline root. Use `commands/web-game-package.sh` through the installed `.hephaera/` path.

1. Resolve packaging and run read-only `doctor` for the requested official target. Keep missing tools/signing/device access explicit. Automatic selection installs nothing.
2. Initialize a fresh host using the user's app identity. Compile the web distribution with its locked toolchain, then `sync` exact assets. Review stale source/native/configuration changes before resync. Use explicit `recover` for an interrupted journal; never overwrite changed or foreign state.
3. Inspect `plan`, then run the explicitly requested `build` or `package` on a compatible host. Keep private signing properties/credentials out of logs, source and artifacts.
4. Verify the actual artifact, signature, full game behavior and target performance. Browser evidence cannot certify native WebView behavior or a physical device.
5. Prepare the selected release channel and obtain any still-required external publication authorization. A local package does not grant store/GitHub upload or release permission.

## Output

Return the exact package/run receipt, source/configuration identity, checks performed and unavailable native/device/store evidence. Preserve the local durable state; do not call source fixtures a native release pass. Linux/TV are unsupported; Wine/Proton compatibility remains unverified.

For an explicitly configured Web3 game, use `integrate-game-wallets` and `verify-web3-game-lifecycle` for the selected native wallet transport and target evidence. Keep the existing popup/navigation restrictions; return-state validation is not an arbitrary JavaScript-to-native bridge or proof that external wallet launch works. Review actual NFT/payment distribution rules before promising a store release.
