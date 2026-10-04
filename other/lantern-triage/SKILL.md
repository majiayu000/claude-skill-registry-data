---
name: lantern-triage
description: Triage a crash/bug in the Lantern React Native (Expo) app.
---
# Lantern crash/bug triage

Lantern is a React Native / Expo couples app (repo: C:\Users\share\OneDrive\Documents\Projects\Lantern\native).

Steps:
1. Read the log/stacktrace with `read_file`.
2. Classify the failure:
   - **Native crash** (signal 11 / SIGSEGV / "Fatal signal") -> the JS ErrorBoundary CANNOT catch it; look at native modules, Google Maps engine, GPU.
   - **OOM** -> known hot spot: base64 media encrypt/decrypt holds whole files in JS heap (~4x size) in `src/lib/mediaCrypto.ts`.
   - **JS error** -> read the component/stack frames.
3. Known device note: vivo 1901 (4GB, Funtouch OS) needs battery whitelisting for background location; the native Maps engine OOM-crashes it (low-RAM tier shows a map-free SVG view).
4. Propose the most likely root cause + a concrete, minimal fix. Cite file:line where possible.

Do NOT suggest adding a WebView/WebGL globe to Beacon (reintroduces the memory pressure).
