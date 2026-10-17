---
type: Skill
name: mcp-ai-wpoos-dictation-app
description: Operational guide for the NV oOS Dictation desktop companion app (Tauri v2 + Rust, examples/nvoos-dictate) — build/run on Windows/MSVC, the local-first engine track (parakeet/whisper/moonshine/silero-vad, all API-verified against pinned crate versions), the embedded remote-STT fallback against the Embedded addon's transcribe route, model registry + verification harnesses, the plugins.updater boot-crash config rule, and the full test/clippy gate matrix. Use when building, extending, or debugging the dictation app, adding an engine or model, touching the cleanup pipeline golden tests, or continuing the P2/P4/P5/distribution follow-up work.
license: Proprietary. See LICENSE.txt
metadata:
  app: nvoos-dictate
  app-version: "0.1.0"
  proposal: "067"
  pr: "7011"
  last-updated: "2026-10-11"
---
# NV oOS Dictation App — Build, Engines, and Verification Guide

Operational guide for `examples/nvoos-dictate` (Proposal 067, PR #7011):
a local-first push-to-talk dictation + meeting transcription desktop app
with the NV oOS plugin as the optional AI-enrichment backend.

## When to use this skill

- Building/running the app on Windows, or debugging a boot failure
- Adding or swapping an STT engine, a model catalog entry, or VAD behavior
- Changing the deterministic cleanup pipeline (golden fixtures are the backstop)
- Wiring the Embedded addon remote-STT fallback or its auth
- Running the benchmark harness (`transcribe_file`) or the model downloader
- Continuing P2 (loopback + PTT matrix), P4/P5 ports, or distribution

## Layout

```
examples/nvoos-dictate/
├── src/                  # React webview (Settings/History/Meetings/Overlay)
├── src-tauri/            # the Rust crate (manifest lives HERE, not at app root)
│   ├── src/{audio,stt,cleanup,nvoos,hotkey,paste,meetings,mcp,storage}
│   ├── tests/            # integration tests (must stay under src-tauri/tests!)
│   ├── examples/         # transcribe_file.rs (WER/e2e_ms) + download_model.rs
│   └── capabilities/ + icons/
├── docs/decisions/       # ADRs 0001 (paste strategy), 0002 (MCP transport), 0003 (engines)
└── e2e/                  # Playwright (webview UI)
```

## Build & run on Windows/MSVC

- Prerequisites: Rust + MSVC (VS 2022), Node 20+, WebView2 runtime
  (Win11 ships it), tauri-cli via npm (`npm run tauri`) — no cargo install needed.
- **MSYS shells**: every cargo command needs
  `export PATH="/c/Users/rasta/.cargo/bin:$PATH"` first; tauri-cli also needs
  cargo on PATH (`npm run tauri` fails with "cargo metadata: program not found"
  otherwise).
- Dev: `npm run tauri dev` (vite :1420). Debug exe:
  `npm run tauri -- build --debug --no-bundle` → `src-tauri/target/debug/nvoos-dictate.exe`.
- `generate_context!` embeds the frontend `dist` at compile time — run
  `npm run build` before any cargo step in CI.
- Boot smoke test: `cmd //c start "" <exe>` → `tasklist //FI "IMAGENAME eq
  nvoos-dictate.exe"` after ~10 s (process alive = boot OK); kill with
  `taskkill //IM nvoos-dictate.exe //F`. A running app locks the exe — kill
  it before `cargo build`/`test` or you get "failed to remove file" errors.
- **Stale-checkout artifact illusion**: the sources merged in #7011 live on
  `alpha-working`. On any branch older than that merge, `git status` shows the
  folder as untracked build leftovers (`?? examples/nvoos-dictate/` with only
  `target/`, `dist/`, `node_modules/` on disk) and the sources look deleted.
  They aren't — sync to `origin/alpha-working` (fetch + rebase/checkout)
  before assuming data loss or starting a rebuild.

## Critical config rule: `plugins.updater` block

`tauri.conf.json` MUST contain a `plugins.updater` block (endpoints +
pubkey). Without it the app panics at boot:

```
error while running NV oOS Dictation: PluginInitialization("updater",
"Error deserializing 'plugins.updater' within your Tauri configuration:
invalid type: null, expected struct Config")
```

The endpoint uses the runtime placeholder `{{current_version}}` matching the
`nvoos-dictate-v*` tag convention; `pubkey: ""` = unsigned dev builds.

## Gate matrix (all verified green on the reference PC)

```bash
cd src-tauri
cargo fmt --check
cargo clippy --all-targets -- -D warnings                          # default
cargo clippy --all-targets --features mcp -- -D warnings
cargo test            # 69 tests (41 lib + 17 golden + 6 history + 5 validation)
cargo test --features mcp       # +4 toolbox tests
cargo test --features parakeet  # +1 tar.bz2 extraction test (42 lib)
```

Native feature compile checks: `parakeet`, `whisper`, `moonshine`,
`silero-vad`, and the combined `--features parakeet,silero-vad,moonshine`.
**whisper needs extra env** (below). CI (`build-nvoos-dictate.yml`) runs
fmt/clippy/test default + `mcp` only; the native engines are local gates.

## Engine track (ADR 0003: local-first, embedded as fallback)

Ordering: mock → parakeet → whisper → moonshine → embedded. The factory is
`stt::create_engine(&EngineConfig, &EngineResources)` — `EngineResources`
carries `models_dir` plus nvoos secrets (`nvoos_site_url`,
`nvoos_credential`, `wp_username`, `wp_app_password`) so the `embedded`
engine can build auth without touching the keychain itself. Call sites:
`state.rs ensure_engine` (fetches secrets), `main.rs` headless +
`examples/*` use `EngineResources::local_only`.

### parakeet (sherpa-onnx, feature `parakeet`) — API VERIFIED 1.13.8

Use the crate's own doc example shape (the old stub had drift everywhere):

```rust
let mut config = OfflineRecognizerConfig::default();
config.model_config.transducer = OfflineTransducerModelConfig {
    encoder: Some(".../encoder.int8.onnx".into()),
    decoder: Some(".../decoder.int8.onnx".into()),
    joiner:  Some(".../joiner.int8.onnx".into()),
};
config.model_config.tokens     = Some(".../tokens.txt".into());
config.model_config.model_type = Some("nemo_transducer".into());
config.model_config.num_threads = n as i32;
config.model_config.provider   = Some("cpu".into());
config.decoding_method         = Some("greedy_search".into());
let recognizer = OfflineRecognizer::create(&config).ok_or(...)?;  // -> Option
let stream = recognizer.create_stream();               // infallible
stream.accept_waveform(sample_rate as i32, samples);   // &self, infallible
recognizer.decode(&stream);                            // infallible
stream.get_result().map(|r| r.text)                    // -> Option
```

Model archive: `sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2` extracts
a top-level dir named after the model id — **unpack into `models_dir` (the
parent)**, not `models_dir/{id}`. Files: `encoder.int8.onnx`,
`decoder.int8.onnx`, `joiner.int8.onnx`, `tokens.txt` (v2 int8 = feature_dim
80 default; v3 uses 128). TDT limit ≈ 4–5 min → meetings must be chunked
(`meetings/chunker.rs`).

### whisper (whisper-rs 0.16, feature `whisper`) — API VERIFIED

- `full_n_segments() -> c_int` (NOT a Result); segments via
  `state.get_segment(i) -> Option<WhisperSegment>` +
  `seg.to_str() -> Result<&str>` (the old `full_get_segment_text` is gone).
- Windows build prerequisites: **CMake on PATH** (VS-bundled CMake at
  `C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin`
  works) + **libclang** (`winget install LLVM.LLVM` → set
  `LIBCLANG_PATH=/c/Program Files/LLVM/bin`).
- `WHISPER_DONT_GENERATE_BINDINGS=1` is **Linux-only** — the checked-in
  bindings are glibc-specific and fail to compile on MSVC (`_IO_FILE` size
  errors). Always use real bindgen on Windows.

### ort / moonshine / silero-vad (features `moonshine`, `silero-vad`)

- **ort pin**: `ort = "=2.0.0-rc.9"` + `ort-sys = "=2.0.0-rc.9"` (direct).
  Without the ort-sys pin, the caret range drifts to rc.13 whose bindings
  break the rc.9 high-level API (233 errors), and rc.13's `download-binaries`
  build script demands a TLS feature rc.9 doesn't expose. Add `dep:ort-sys`
  to both `moonshine` and `silero-vad` features.
- Moonshine engine is a documented spike (`Unsupported` error) — the
  streaming ONNX loop is intentionally unimplemented.
- **silero-vad-rs 0.1.2 real API**: `SileroVAD::new(path)` +
  `model.process_chunk(&arr.view(), 16000) -> Result<Array1<f32>>` with
  exactly **512-sample chunks @ 16 kHz** (32 ms). The adapter in
  `audio/vad.rs` buffers partial input and mirrors the EnergyVad hangover
  semantics. Model: `silero_vad.onnx` from sherpa-onnx releases, catalogued
  as engine `vad` (UI shows `vad` entries alongside the selected engine).

### embedded (remote fallback, always compiled — no feature flag)

Contract: `POST {site}/wp-json/mcp-ai/v1/embedded/transcribe` with
`{"audio": "<base64 16-bit PCM WAV>", "language": "en"}`; server limit
10 MB, 30 req/min, 60 s timeout (Embedded addon → Gemma 4 audio endpoint).
Auth: **WP application password → Basic** (satisfies the route's
`is_user_logged_in()`; stored in keychain via `set_wp_app_password` IPC);
assistant credential → Bearer requires the addon `permission_callback`
tweak (follow-up PR). WAV encoder: `audio/wav.rs::encode_f32_to_wav`.
Contract tests in `stt/embedded.rs` (endpoint/body/parse/auth) — no network.

## Model registry conventions

`stt/model_registry.rs`: pinned `ModelSpec` catalogue (`engine`, `id`, url,
optional sha256, `archive`, `file_name` override for non-`.bin` files).
Rules: streaming SHA-256 (never read models into memory), atomic rename,
measured-hash logging when unpinned, tar.bz2 extraction behind the
`parakeet` feature. Downloads live in
`%APPDATA%/nvoos-dictate/models/` (GUI: Settings → Engine & Models).

## Verification harnesses

```bash
# Registry-driven download (same path the GUI uses)
cargo run --features parakeet --example download_model -- parakeet sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
cargo run --example download_model -- whisper tiny.en

# WER + e2e_ms + RTF against a speech file (sidecar .txt = reference)
cargo run --features parakeet --example transcribe_file -- ../speech.wav --engine parakeet --model sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8
```

- Speech samples without a mic: PowerShell SAPI TTS —
  `Add-Type -AssemblyName System.Speech; $s.Speak(...)` →
  `SetOutputToWaveFile(...)`.
- Reference-PC numbers (debug build, 4.27 s sample): parakeet 1187 ms
  (RTF 0.28), whisper tiny.en 1095 ms (WER 7.7%). Both beat the 1.5 s
  key-up→paste budget; release is faster.

## Known Rust pitfalls (this codebase)

- `cpal::Stream` is `!Send + !Sync` on WASAPI — streams must live on
  detached worker threads; only Send handles (ring buffer Arcs, channels,
  atomics) may enter `AppState`. Do not regress this.
- **Bare expression paths do not resolve sibling modules declared in a
  parent module** (proven with a minimal repro): inside
  `stt/engine.rs`, `parakeet::X` fails while `crate::stt::parakeet::X`
  works — always use crate-qualified paths for cfg-gated siblings.

## Cleanup pipeline (golden backstop)

Order matters: whitespace → vocabulary → numbers → fillers → capitalize →
punctuate → per_app. Any rule change must keep `src-tauri/tests/cleanup_golden.rs`
(17 cases + `meeting1` fixture) green or be an intentional, reviewed change.
The fixture previously said "So we need…" but the leading-marker rule strips
`so` after filler removal — "We need…" is the correct expectation.

## Status & follow-ups (2026-10-11)

Done: P0 core, P1 (nvoos client/archive), P3 (MCP stdio), engine track live-
verified, embedded fallback implemented, PR #7011 → `alpha-working`.
Remaining: PTT manual matrix + loopback meeting verification (P2 real-call),
embedded live test (needs a Gemma 4 audio endpoint), Embedded addon
permission tweak for `cred_x.SECRET`, P4/P5 ports, release signing/updater
feed. See the implementation plan (`docs/project/proposals/067-…-plan.md`)
for the full item list.

## Related skills

- `mcp-ai-wpoos-plugin` — plugin-side setup (assistant credentials, Docker)
- `mcp-ai-wpoos-spa-ui` — React/Vite conventions shared with the SPA addons
- `mcp-ai-wpoos-test-suite` — PHPUnit side; this skill covers the Rust gates
