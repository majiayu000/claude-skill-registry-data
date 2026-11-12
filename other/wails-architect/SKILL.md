---
name: wails-architect
version: 1.0.2
description: Wails v3.1 shell around an existing web app — embedded SPA build, same-origin API proxy with server-held session cookies (WebKit drops Set-Cookie on custom schemes), per-OS window chrome, Android fetch shim and insets, packaging and Play signing. Use when scaffolding or reviewing a Wails desktop/mobile shell, or when sign-in fails inside the webview.
---

# Wails Architecture

Targets **Wails v3.1.0** on **Go 1.27.x**. Companion to [go-architect](../../languages/go-architect/SKILL.md), [react-architect](../react-architect/SKILL.md), [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md) and [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md). Full skeletons in [RECIPES.md](RECIPES.md); pinned versions in [STACK.md](STACK.md).

## 1. Decide whether a shell is justified

A Wails shell is a **thin client** around a web app that already talks to a remote API: it embeds the build, forwards API calls and holds no data. The server, the database and the SPA stay unchanged.

- **Never embed the server.** A desktop binary cannot run Postgres and the identity service, and doing so creates a second deployment.
- **Mobile is experimental.** Wails v3 marks iOS/Android experimental; keep the PWA or a native wrapper as the fallback and keep the shell thin enough to swap.
- **A shell must earn its place.** Ship the PWA unless you need something a browser tab cannot do (native notifications, badge, tray/menus, autostart, file association, keychain, updater). Add those after the shell works, in value order.
- **Alternatives:** Tauri 2 has stable mobile but adds Rust for what is mostly configuration; Capacitor covers phones only; a PWA covers the browser.

## 2. Project layout

Give the shell **its own `go.mod`**, outside the application module, with its own lint and archtest. It sits beside the SPA so the embed path is local and explicit.

- **No frontend of its own.** `frontend/package.json`'s build copies the SPA's `dist`, or `//go:embed` a relative directory. Commit neither `frontend/dist` nor `bin/`.
- **`main.go` wires, nothing else.** Asset handler + `application.New` + one window. Platform behavior goes in build-tagged files (`api_android.go`), not `runtime.GOOS` branches where the *contract* differs.
- **Taskfiles per target.** Keep the scaffold's `build/<os>/Taskfile.yml` includes and add your own `build`, `package` and `release:*` tasks at the shell root. Tree in [RECIPES.md](RECIPES.md#project-layout).

## 3. One origin: assets and API

Register a single `http.Handler` in `application.AssetOptions.Handler` and route inside it. Keeping the API on the webview's origin removes CORS and any base-URL configuration from the SPA.

- **SPA fallback:** a client route (`/settings`) serves `index.html`; a missing path **with an extension** returns 404, or a broken asset is served as HTML and the browser reports a misleading MIME error.
- **Proxy only the API patterns** (`/v1/`, exact `/health`); everything else is a static asset. Never proxy `/`.
- **Rewrite the request host** to the API's host, and drop `Origin` — the browser origin is meaningless to a shell.
- **Answer 502 when the API is unreachable**, not an empty 200. The page then shows a real error instead of corrupt JSON.
- **An origin-checking API needs a rewrite, not deletion.** Deleting `Origin` is enough for a permissive API; an API that validates the origin must receive a configured allowed value.

## 4. Session cookies: the custom-scheme trap

The webview loads the page from a custom scheme. **WebKit ignores `Set-Cookie` on responses from a custom-scheme handler.** Login returns 200 with both cookies and every later request carries none, so the user is signed out immediately.

- **Do not rewrite the cookie attributes** (`Secure`, `Domain`, `SameSite`). The cookie is never stored, so no attribute can save it.
- **Hold the session in Go:** a jar keyed by name + path with expiry (RFC 6265 path match) attaches `Cookie` on outgoing requests and removes `Set-Cookie` from responses. The page never holds a token.
- **In memory means logout on restart.** That is acceptable for a first release; persist to the OS keychain when a restart should keep the session. Wails v3 has no keychain API.
- **If the API supports it, prefer OIDC with a loopback redirect:** the shell holds tokens instead of proxying someone else's cookies.
- **Verify with a wrong password:** the page must show the API's own `401` message ("invalid credentials"), not "Network error." That single test proves the response path and the proxy.

## 5. Window chrome per OS

Return `application.WebviewWindowOptions` from one function that switches on `runtime.GOOS`. The shell owns the chrome; the SPA never learns which OS it runs on.

- **Linux:** frameless window plus a small minimise/maximise/close cluster injected with the window's `JS` option; the app's own `<header>` becomes the drag area. The `CSS` option did not apply under GTK 4 — inject a `<style>` from the script. Keep native chrome behind a config flag.
- **Drag regions** use `--wails-draggable: drag` / `no-drag`; interactive children must opt out or they stop receiving clicks.
- **Windows:** Mica backdrop + system theme. **macOS:** transparent native title bar, or the hidden-inset preset (`application.MacTitleBarHiddenInset`) when the page extends under it and the app header pads for the traffic lights.
- **Android/iOS:** plain options; the system draws the bars and the page fills the rest.
- **Never claim a platform works because it compiles.** Record which branches have been run.

## 6. Android specifics

A phone has no environment, and its webview is stricter than the desktop one. Handle both before testing the UI.

- **API address in code.** `os.Getenv` is always empty on a phone. Set the deployed URL in a constant and override per build with `-ldflags "-X main.defaultAPI=..."`; the emulator reaches the host at `10.0.2.2`.
- **Fetch shim.** The Android webview hands the asset handler every request as a **bodiless `GET`** and turns any status but 200 into "asset not found", so a sign-in `POST` never reaches the API. Inject a script that wraps `window.fetch` for the API routes and sends method, headers and body over the Wails bridge to a Go service that runs it through the same handler. Desktop does not use it.
- **Shim limits:** `fetch` only — no `XMLHttpRequest`, `EventSource`, streaming bodies, redirect following or abort propagation. Say so in the UI/docs.
- **System-bar insets.** Android 15+ draws edge-to-edge; pad the root view from `WindowInsetsCompat`. The scaffold's `MainActivity` can carry the patch, but `wails3 task common:update:build-assets` overwrites it — reapply after every scaffold update.
- **Full JDK 21**, not a runtime-only JRE: Gradle needs `javac`, and `jlink` fails on a newer JDK. Set `JAVA_HOME`. If the emulator dies with `SIGSEGV`, start it with `-gpu host`.
- **Verify with `adb logcat`** filtered to the app; the proxy log and the shim calls should show while signing in.

## 7. Build, package and release

- **Toolchain:** `wails3` ships with the Go toolchain pinned by mise. Run tasks from the repo so it is on `PATH`.
- **Rebuild the SPA in every build task.** The scaffold's frontend task is status-checked and can silently ship a stale `dist`; do the copy yourself.
- **Desktop:** `wails3 tool package` produces `.deb`, `.rpm` and `.pkg.tar.zst`; `generate appimage` embeds GTK/WebKit (roughly 100+ MB, the others ~7 MB). nfpm metadata lives in `build/linux/nfpm/`.
- **Android:** build a **signed AAB** with the upload key, passed through the scaffold's `ANDROID_KEYSTORE_*` variables from the secrets store — never into the repo. Derive `VERSION_NAME`/`VERSION_CODE` from the git tag (a final release must outrank its RCs). Use `bundle`, not `assemble:aab:release`: the latter skips the SPA copy and ships whatever `libwails.so` is in `jniLibs`.
- **Check the signature before uploading:** `keytool -printcert -jarfile app.aab` must show the upload key.
- **Play internal testing first.** The package ID locks at the first upload and a lost upload key needs a support reset — back it up.
- **Updater:** Wails v3 has `app.Updater` (download, SHA-256 or Ed25519/ECDSA check, atomic swap), desktop only. A private-repo GitHub provider needs a token in the binary; prefer an `endpoint` provider with a signed manifest.

## 8. What the webview cannot do

Do not design around browser features the shell lacks, and put the missing capability in Go:

- **No service worker** — the PWA's offline cache and Web Push do not run. Native notifications and a badge are the shell's job.
- **No keychain** — persist tokens yourself.
- **No passkeys inside the webview** as of 3.1.0; use OIDC with a loopback redirect.
- **A webview app is not "lighter than Electron" by default** — measure PSS and CPU before promising it.

## 9. Testing and debugging

- **Unit-test the pieces that hide bugs:** jar (path scope, expiry, removal), proxy (cookies kept from the page, `Set-Cookie` stripped, `Origin` dropped, 502 on failure), SPA fallback (route → `index.html`, missing asset → 404).
- **Hand-check what only a webview shows** per OS: cookie kept across a reload, window drag and controls, theme, insets, sign-in failure text. Keep a per-OS matrix in the shell README.
- **Common failures:** signed in then out → cookies never reached the jar; `403` on a private module → `GOPRIVATE` and the module proxy; Java capability / `jlink` error → wrong JDK; `wails3: not found` → mise toolchain not active; Play rejects the bundle → debug key; page under the status bar → insets patch lost.

## 10. Review checklist

- Shell has its own module; no server, database or identity embedded.
- One asset handler: SPA fallback + API proxy on the same origin; 502 on failure.
- Session held in Go, `Set-Cookie` stripped, `Origin` handled; wrong-password test passes.
- Per-OS window options exist and each platform is marked run or compile-only.
- Android: URL in code, fetch shim on, insets patch present, JDK 21, signed release task.
- Version derived from the tag; upload key read from secrets; signature checked.
- No reliance on service workers, Web Push, WebAuthn or a keychain.
- Only the native features the shell actually needs are wired in.
