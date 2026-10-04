---
name: cgagentharness-release
description: Build, verify and prepare CG-agent-harness macOS desktop release artifacts, including universal Apple Silicon and Intel binaries and GitHub Bundle workflow provenance.
---

# Release the macOS desktop

Read `AGENTS.md`, `docs/DESKTOP.md`, `scripts/package-desktop.sh`,
`scripts/verify-desktop-bundle.sh`, `docs/RELEASING.md` and current workflows.
Refresh main; preserve existing work in another checkout.
Use a `codex/` branch; package committed source so `Resources/COMMIT` is meaningful.
`CGAH_ALLOW_DIRTY=1` is only for marked development artifacts.

Build on Apple Silicon macOS with installed Xcode CLT and rustup toolchains from
both toolchain files. Install `aarch64-apple-darwin` and `x86_64-apple-darwin`
standard libraries for both toolchains before a universal build. Use rustup Cargo
on PATH. Run `scripts/package-desktop.sh --universal` (optional `--dmg`).

The critical order is backend slices -> lipo -> sign universal backend -> compile
both desktop slices embedding that exact whole-file SHA256 -> lipo desktop -> sign
shell/bundle. Never re-sign the sidecar after its digest is embedded. The backend
remains a separate child; native commands must not become browser capabilities.

Verify the ZIP checksum, extract to a fresh directory with spaces, and run
`scripts/verify-desktop-bundle.sh '<extracted app>' universal`. Verify both executables
contain arm64 and x86_64, nested signatures, resources and system-only linkage.
Run `scripts/test-desktop-backend.py` with `CGAH_TEST_BINARY` set to the packaged
backend. Run desktop policy tests and both dependency policies.

Launch the actual app with a disposable `CGAGENTHARNESS_HOME`, distinct from any
operator home. Record app PID, owned sidecar/listener, local model chat and shutdown.
Do not treat a shared listener as this bundle's process. GUI acceptance requires
actual WKWebView evidence; HTTP tests do not prove pixels, focus or native dialogs.
Intel cross-compilation, Rosetta execution and native Intel testing are different
claims. Do not silently install Rosetta or change TCC settings to fill an evidence gap.

Before publication, complete local acceptance and inspect tracked files for
secrets or machine-specific data. Use the PR template.
Bundle calls reusable desktop CI; tagged releases reuse it too. Match remote SHA,
workflow run, artifact COMMIT and checksums. For unmerged candidates, use PR
Bundle artifacts. Scheduled/manual publication
requires main and a successful Bundle run at that SHA. The release planner
rejects prerelease tags. Check existing runs, tags and releases before dispatch.
Publication follows explicit user authorization. Never overwrite release assets
or tags after an ambiguous result.
Ad-hoc signing is not Developer ID signing or notarization; state that limitation.
