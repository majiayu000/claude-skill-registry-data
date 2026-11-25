---
name: rust-command
description: Recipe to add a Rust command to EasyTask (src-tauri) - the command and its registration, heavy work off the UI thread, path checks, a new crate with cargo deny / cargo audit, caches in the data folder, unit tests with generated files, and the TypeScript side. Use when adding or changing a #[tauri::command], adding a Cargo dependency, or moving work from the frontend to Rust.
---

# Add a Rust command (EasyTask)

Rust lives in `src-tauri/src/`, one module per area: `audio.rs` (metadata with lofty), `files.rs` (path checks, asset scope), `paths.rs` (data folder), `transfer_zip.rs`, `db.rs`, `media_session.rs`, `settings.rs`, `window.rs`. The database is NOT here: tables and queries are TypeScript (`src/db/`). Model a new command on `audio::audio_metadata`.

## 1. The command

```rust
#[tauri::command]
pub(crate) async fn audio_metadata(path: String) -> Result<AudioMetadata, String> {
    if !is_audio_file(&path) {
        return Err("audio file not found".to_string());
    }
    tauri::async_runtime::spawn_blocking(move || read_audio_metadata(Path::new(&path)))
        .await
        .map_err(|error| error.to_string())?
}
```

- `pub(crate) async fn`, errors as `Result<_, String>`; the result type derives `serde::Serialize` with `#[serde(rename_all = "camelCase")]` if the TS side expects camelCase (check the existing struct).
- **Check every path from the frontend** before touching it: `files::is_audio_file` / the media check (allowed extension + regular file). Never read or write a path the user did not pick.
- **Heavy work** (decoding, hashing, zip) goes in `spawn_blocking`. `Cargo.toml` has no `panic = "abort"` on purpose: a panic while parsing a user file must come back as a `JoinError`, not kill the app.
- Long work that the UI can abandon (another file chosen): make it cancellable or make the frontend ignore stale answers (a sequence number, as `playSeq` in `audio-context.tsx`).
- The data folder is `paths::DataDirInfo` (managed state: `info: tauri::State<'_, DataDirInfo>`). Caches go in a subfolder of it, keyed by something that changes with the file (path + size + mtime), written atomically (temp file + rename) and safe to delete.

## 2. Registration and permissions

- Add it to `tauri::generate_handler![...]` in `lib.rs`.
- App commands need no capability entry; plugin commands and window APIs do (skill **tauri-permission**). If the frontend then loads the file with `convertFileSrc`, the path must be in the asset scope (`files::allow_audio_file`).

## 3. A new crate

- `src-tauri/Cargo.toml` `[dependencies]`, with only the features needed (`default-features = false` when the defaults pull a lot). Keep `Cargo.lock` in the commit.
- CI runs `cargo deny check` and `cargo audit` in `src-tauri` (job "audit"). `deny.toml` allows only permissive licenses (MIT, Apache-2.0, BSD, ISC, MPL-2.0, Zlib...): a crate outside the list fails CI and needs the user's OK, never a silent `allow`. Do not add an `ignore` to advisories without a written reason and a date, like the existing ones.
- The release profile is `lto = true`, `opt-level = "s"`: check the effect on the size of the installer for big crates and say it in the PR.
- The app ships on Windows and Linux (`[graph] targets` in `deny.toml`): no crate that needs a system library not installed by `.github/actions/linux-tauri-deps`.

## 4. Tests

- `#[cfg(test)] mod tests` at the bottom of the module; `crate::test_support::temp_dir(name)` for a fresh folder, removed at the end.
- Generate the files in the test instead of committing binaries: `audio.rs` has `write_test_wav` (a WAV header + samples), extend it with a known signal (for example a 1 kHz sine at a known level) to assert values with a tolerance.
- Cover: a valid file, a wrong extension, a missing file, a corrupt file (must be an `Err`, not a panic).
- Run in `src-tauri`: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test` (skill **pre-push**). CI runs them on Windows and Ubuntu.

## 5. The TypeScript side

- `invoke<Type>("command_name", { path })` from `@tauri-apps/api/core`, wrapped in a function of a `src/lib/` or `src/contexts/` module (not called from components).
- Model: `src/lib/audio-metadata.ts` with its test `src/lib/audio-metadata.test.ts` (vitest mocks `invoke`, error case included) and `rightbar/DetailsPanel.audio.test.tsx` for the panel.
- Show progress with `LoadingDots` and errors with the existing toasts; texts in en + it (skill **i18n-keys**).
