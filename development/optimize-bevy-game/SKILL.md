---
name: optimize-bevy-game
description: Use when a Bevy game stutters, drops frames, loads slowly, or ships a large binary or wasm — measure with diagnostics and Tracy/Chrome traces first, then fix change detection, system parallelism, batching, per-frame allocations, and release/wasm profiles.
---

# Optimize Bevy Game

Bevy 0.20. Rationale per rule: [optimization-patterns.md](optimization-patterns.md). Versions: [stack-versions](../_shared/stack-versions.md). Principle: [measure before optimizing](../../core/_shared/engineering-principles.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null                  # hosting/web target, task_runner
grep -nE '^\[profile|opt-level|lto|codegen-units|strip|panic' Cargo.toml
grep -nE 'trace|tracing|dynamic_linking|"debug"' Cargo.toml
grep -rnE 'FrameTimeDiagnosticsPlugin|LogDiagnosticsPlugin|FpsOverlay' src/
grep -rnE 'Vec::new\(\)|collect::<Vec|format!\(|\.clone\(\)' src/ | head -20     # per-frame allocation suspects
grep -rnE 'iter_mut\(\)|&mut [A-Z]' src/ | head                                   # mutable access that marks change
ls -l target/release/* 2>/dev/null | head -3; ls -l dist/*.wasm 2>/dev/null
```

State the symptom as a number before touching code: frame time in ms (not FPS), load time in s, binary or wasm size in MB. "It feels slow" is not a symptom.

## 2. Decide what to do
- **No measurement yet** → step 5 (measure). Stop there until the numbers exist.
- **Measured, a system or plugin dominates** → fix that one; re-measure.
- **Size or startup problem only** → release/wasm profile rules, no code changes.
- Numbers already meet the target (say a 16.6 ms frame, a wasm under budget) → "already in place", stop.

## 3. Detect track
- **CPU-bound** (a system tops the trace): change detection, parallel iteration, allocation, scheduling.
- **GPU-bound** (frame time tracks resolution or sprite/mesh count, systems are short): batching, atlases, fewer materials, lower resolution.
- **Load / size:** asset processing ([manage-bevy-assets](../manage-bevy-assets/SKILL.md)), release profile, wasm size.

## 4. Install only what's missing
Profiling needs a Tracy viewer matched to the client library version, or nothing (Chrome traces open in `ui.perfetto.dev`):

```bash
cargo tree --features bevy/trace_tracy | grep tracy      # read the tracy-client version, then match the Tracy UI to it
```
Tracy UI: official Windows binaries, third-party macOS/Linux builds (`tracy-builds`), or a package manager. wasm size tools: `wasm-bindgen-cli` (same version as the crate) and optionally Binaryen `wasm-opt`.

## 5. Measure first

```bash
cargo run --release --features bevy/trace_chrome              # writes trace-*.json; open in https://ui.perfetto.dev
cargo run --release --features bevy/trace_tracy,bevy/debug    # live in Tracy; `debug` gives Bevy systems readable names
```
Quick numbers without a profiler: add `FrameTimeDiagnosticsPlugin::default()` and `LogDiagnosticsPlugin::default()` to the app (dev builds only). Always profile `--release`; dev builds mislead.
Read the trace: find the longest system span per frame and what it waits on. Write down: system name, ms per frame, the target.

## 6. Fix, one change at a time
Apply the first matching rule from [optimization-patterns.md](optimization-patterns.md), in this order:
1. Skip work: `Changed<T>`/`Added<T>`, run conditions, `set_if_neq`.
2. Parallelism: disjoint queries so the scheduler can overlap systems; `par_iter_mut` for large heavy loops.
3. Allocation: reuse `Local<Vec<_>>`, `spawn_batch`, no `format!` or `collect` per frame.
4. Rendering: texture atlases, shared materials, fewer unique handles; see GPU rule.
5. Build profile: `lto`, `codegen-units`, `panic = "abort"` only when measured.
6. Web size: `wasm-release` profile, `wasm-bindgen`, optional `wasm-opt`.

Canonical release profile (desktop):

```toml
[profile.release]
codegen-units = 1
lto = "thin"
```
Web:

```toml
[profile.wasm-release]
inherits = "release"
opt-level = "s"
strip = "symbols"
```

## 7. Verify
Repeat the exact measurement from step 5 and compare:

```bash
cargo run --release --features bevy/trace_chrome        # same scene, same machine, same duration
cargo build --profile wasm-release --target wasm32-unknown-unknown && ls -l target/wasm32-unknown-unknown/wasm-release/*.wasm
```
Expected: the target number is met, or the change is reverted. Keep a one-line before/after in the PR description. Run `cargo nextest run` to confirm behavior did not change.

Related: [structure-bevy-app](../structure-bevy-app/SKILL.md) (sets and ordering), [test-bevy-systems](../test-bevy-systems/SKILL.md) (ambiguity check).
