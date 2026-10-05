---
name: rust-windows-native-dev
description: "Windows Rust: windows crate COM, winreg, cross-compile."
---

# Rust Windows Native Development

Windows system programming in Rust. Hard-won knowledge from BootKeeper (windows crate 0.62.2).

## Cross-platform strategy (the big one)

Structure crates so **pure logic compiles on Linux** and Windows API code is cfg-gated:

```toml
# Cargo.toml — platform deps MUST be target-gated or Linux build dies
[dependencies]                    # cross-platform: serde, chrono, thiserror, uuid
[target.'cfg(windows)'.dependencies]
winreg = "0.56"
windows = { version = "0.62", features = [...] }
```

```rust
// lib.rs — Windows-only modules behind cfg
pub mod windows;                  // mod.rs gates submodules #[cfg(windows)]
```

- **Linux host** (`cargo test`): runs pure-logic tests (rule engines, storage, models) — fast feedback without Windows.
- **Cross-compile** (`cargo build --target x86_64-pc-windows-msvc`, needs `rustup target add x86_64-pc-windows-msvc`): validates API usage/features compile. **Lib crates compile; bin crates fail at link** — no MSVC link.exe on Linux. So a CLI/Tauri bin can't be cross-verified locally; let CI do it.
- **Real Windows CI** (`windows-latest` runner in GitHub Actions): the ONLY place Windows-only code actually runs. **Cross-compiling proves it compiles; CI proves it runs.** A null-pointer deref in WinVerifyTrust passed cross-compile and crashed on the real runner (`STATUS_STACK_BUFFER_OVERRUN`). Always add a `test-windows` job with integration tests hitting real registry/Task Scheduler.

## windows crate — the traps

Full API notes in `references/windows-crate-com.md`. Summary:

1. **Feature gates are mandatory.** Every API family needs its feature: TaskScheduler → `Win32_System_TaskScheduler` + `Win32_System_Com` + `Win32_System_Variant` + `Win32_System_Ole`; `WINTRUST_DATA` → `Win32_Security_Cryptography` (not just WinTrust!). Missing feature = "cannot find" errors.
2. **COM interfaces are HIGH-LEVEL wrappers, not raw bindings.** Methods differ from C API: `Connect(&VARIANT, ...)` not `Connect(NULL)`; collections use `Count()` + `get_Item(&VARIANT)` — **not iterators**; out-params like `IExecAction::Path(&mut BSTR)`; `IActionCollection::Count(&mut i32)` returns `Result<()>`.
3. **`let-else` + `unsafe` needs parens**: `let Ok(x) = (unsafe { f() }) else { ... };`
4. **Unions**: assign the pointer (`data.Anonymous.pFile = &mut file_info;`), never deref-and-assign (`*data.Anonymous.pFile = ...` → null deref). Union field is `Anonymous`, not `u`.
5. **Class IDs**: Task Scheduler class is `CLSID_CTaskScheduler`, not `TaskSchedulerClass`.
6. **HRESULT comparisons**: `0x800B0100` (TRUST_E_NOSIGNATURE) exceeds i32 → compare as `0x800B0100u32 as i32`.

## Dependencies (checked, current)

- `winreg` 0.56 — alive, 196M downloads. Registry Run keys.
- `windows` 0.62 — official, 283M downloads.
- `taskschd` crate — **DEAD** (2023, 3.9k downloads). Do not use; use windows crate TaskScheduler COM.
- `schtasks` CLI wrapping — fragile, localized output. Avoid.

## Verify patterns

- Rule engine / risk logic: pure functions + unit tests on Linux.
- Windows integration tests: `#![cfg(windows)]` in `tests/`, run on CI windows-latest; assert "no panic" + non-empty names for registry/tasks/folders.
- clippy gate: `cargo clippy --workspace --all-targets -- -D warnings` on both platforms in CI.
