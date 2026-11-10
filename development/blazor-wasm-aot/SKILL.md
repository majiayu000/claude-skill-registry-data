---
name: blazor-wasm-aot
description: Build and publish Blazor WebAssembly apps with Mono AOT compilation on .NET 7 (net7.0), including toggling AOT on or off and explaining in plain English what the toggle changes (startup speed, publish time, download size, debugging, trimming risk). Use when asked to (1) build, publish or enable AOT / RunAOTCompilation for a Blazor WASM client, (2) turn AOT off or on for a fast vs release build, (3) fix AOT or publish failures such as NETSDK1147 missing wasm-tools workload, emcc/python3 errors, or unexpectedly long publishes, (4) verify an AOT publish really produced native output, or (5) tune Blazor WASM startup performance. Also use when a Blazor WASM build asks for wasm-tools-net7. Not for plain dotnet run dev-loop work, non-Blazor WebAssembly, or .NET 8+ server/MAUI AOT.
metadata:
  version: 0.1.0
---

# Blazor WASM AOT (.NET 7)

Repo-agnostic recipe for producing an AOT-compiled Blazor WebAssembly build, proven against a
`net7.0` Blazor WASM client served by an ASP.NET Core host. Replace project names, paths and
output locations with the target repo's.

## 1. Detect the target

1. Find the Blazor WASM project: `rg -l "Microsoft.NET.Sdk.BlazorWebAssembly" -g "*.csproj"`.
2. Read its `TargetFramework` and the repo's `global.json` — the SDK band decides the workload
   name and manifest feeds (step 2).
3. Find the project that actually emits the WASM assets: a server host that pulls in the client's
   static web assets (publish the host), or the client itself (static hosting).
4. Check whether AOT is already wired (`RunAOTCompilation` in the csproj, a Dockerfile or a
   publish profile) before changing anything.

## 2. Install prerequisites

| App TFM | Workload to install |
| --- | --- |
| `net7.0` | `wasm-tools-net7` |
| `net8.0` / `net9.0` / `net10.0` | `wasm-tools` (band matches the SDK) |

- Newer SDKs do **not** restore workload manifests for an older TFM band, so a net7 app under an
  SDK 8+ install needs the explicit, pinned install:
  `dotnet workload install wasm-tools-net7 --skip-manifest-update`.
- Install `python3` as well: the workload's `emcc` wrapper is a Python script and minimal/CI
  images ship without it.
- Verify: `dotnet workload list`, `python3 --version`. From the repo root `dotnet workload restore`
  restores whatever the project graph declares.
- Build with the `dotnet` on PATH that matches `global.json` (`which dotnet`, `dotnet --info`);
  mixing SDKs is the usual cause of restore/manifest weirdness.

## 3. Set the repo default

- Set `<RunAOTCompilation>true</RunAOTCompilation>` in the Blazor WASM csproj when AOT builds are
  the repo's default. This is only the default — section 4 shows how to flip any single build.
- Set it only on the Blazor WASM project — never on class libraries, tests or the server host.
- Keep `<CopyOutputSymbolsToPublishDirectory>true</CopyOutputSymbolsToPublishDirectory>` (plus
  `DebuggerSupport`) so the published, optimized output stays debuggable in the browser.
- Decide the globalization trade-off: `BlazorWebAssemblyLoadAllGlobalizationData=true` keeps
  every locale working but inflates the AOT payload; drop it and rely on invariant/small ICU if
  size matters more.
- Preserve reflection-heavy libraries through the trimmer with
  `<TrimmerRootAssembly Include="..." />`. Symptom of skipping it: works in dev, then after
  publish the app silently degrades (proven case: MSAL trimmed to a bare
  `authentication/login-failed` redirect with no error).

## 4. Toggle AOT on or off

Three levers, most specific wins:

| Lever | Where it lives | Use for |
| --- | --- | --- |
| `<RunAOTCompilation>` | committed csproj | the default every clone builds with |
| `-p:RunAOTCompilation=true\|false` | the publish command | one-off builds; **overrides the csproj** |
| `-p:RunAOTCompilation=${ENABLE_AOT}` | Docker `ARG` / CI variable | flipping in CI without editing source |

```bash
# fast build while iterating (seconds)
dotnet publish <proj>.csproj -c Release -o out -p:RunAOTCompilation=false
# release build with AOT (minutes)
dotnet publish <proj>.csproj -c Release -o out -p:RunAOTCompilation=true
```

**Plain English — what the toggle actually changes:**

| | AOT on | AOT off |
| --- | --- | --- |
| What happens | C# is compiled to WebAssembly on your machine during publish | the browser downloads ordinary IL and works it out while the app loads |
| First load | noticeably faster startup — the biggest win on phones and low-end hardware | slower cold start; nobody notices during development |
| Publish time | minutes | seconds |
| Download size | larger (native `dotnet.wasm` grows by several MB) | smaller |
| Debugging | needs symbols; stack traces point into native code | matches the dev build, easiest to step through |
| What can go wrong | trimming can strip reflection-heavy libraries — usually only shows up after publish | far fewer moving parts |
| Ship it? | yes — releases and perf-sensitive demos | no — dev loop, CI smoke checks, PR builds |

Rule of thumb: AOT trades publish time and download size for faster first load. Turn it off while
iterating, on for anything you ship; the app behaves identically either way.

**Tell which mode a build used:** seconds + small `dotnet.wasm` = off; minutes + a grown
`dotnet.wasm` + native-compilation lines in the log = on. A fast build when you asked for AOT
means the flag never reached the published project (see troubleshooting).

## 5. Publish

```bash
dotnet publish <HostOrClient>.csproj -c Release -o artifacts/publish -p:RunAOTCompilation=true
```

- If the repo defines publish profiles (container/self-contained), neutralise them with
  `-p:PublishProfile=` so output lands where you expect.
- Pick the mode per section 4; everything else about the publish is identical between modes.
- For a local debugging loop, the build output already contains the client at
  `bin/<Config>/<tfm>/wwwroot/_framework/`; publish only when producing the shippable bundle.

## 6. Verify the AOT build

1. Confirm the boot manifest is published: `_framework/blazor.boot.json` on net7/net8-style
   output (on .NET 10+ the manifest is merged into `_framework/dotnet.js` — probe that instead).
2. Confirm the mode actually ran — the tell-tales are in section 4. A publish that finished in
   seconds with an unchanged `dotnet.wasm` never compiled AOT, regardless of what you asked for.
3. Serve the publish output and load it in a browser: framework assets must fetch 200, the app
   must reach first render, and cold-load time should beat the non-AOT build.
4. If it ships in a container, probe the boot manifest and asset paths over HTTP from inside the
   container (runtime images often lack curl — use bash `/dev/tcp`).

## 7. Troubleshoot

| Symptom | Fix |
| --- | --- |
| `NETSDK1147: ... workloads must be installed: wasm-tools-net7` | `dotnet workload install wasm-tools-net7 --skip-manifest-update` (or `dotnet workload restore` from the repo root) |
| `emcc: not found` / python errors during publish | Install `python3`; the workload's emcc wrapper is a Python script |
| Workload install/restore fails right after an SDK upgrade | Confirm `which dotnet` is the SDK pinned by `global.json`; manifests are per SDK band |
| Publish finishes in seconds, output identical to before | `RunAOTCompilation` was not applied to the published project — pass `-p:RunAOTCompilation=true` on the publish command and check no publish profile overrides it |
| App works in dev, breaks only after publish | Trimming: root the affected assembly with `TrimmerRootAssembly` |
| Publish runs out of memory / very slow in CI | Allocate more memory or split the job; AOT is inherently minutes-long — use `-p:RunAOTCompilation=false` for non-release builds |
| Need to debug the published AOT bundle | Keep `DebuggerSupport` + `CopyOutputSymbolsToPublishDirectory`, then attach the browser devtools via the WASM debug proxy |

## Notes

- AOT is a ship-time decision, not a code change: nothing in the app behaves differently, only
  how it was compiled. Judge it with cold-load measurements, not build-time intuition.
- Keep both modes on one switchable flag so the fast and AOT paths cannot drift apart.
