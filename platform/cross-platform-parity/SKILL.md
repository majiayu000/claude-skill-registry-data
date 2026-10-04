---
name: cross-platform-parity
description: Use when a kasane change touches networking, storage, navigation, fonts, safe areas, window chrome, or anything else that behaves differently on iOS, Android, web, or the Tauri desktop build — or when asked whether something works on native, on desktop, or in the browser.
---

# Cross-Platform Parity

One codebase, five targets: iOS, Android, web (Netlify), and macOS/Windows/Linux (Tauri 2 wrapping the web export). The repo has only **two** `Platform.OS` branches, yet several behaviours already differ by target. The risk is not too much branching, it is a change that is silently correct on web and broken on native.

## Where the targets already diverge

| Concern                    | Web (Netlify)                                                                     | Native (iOS/Android)                                | Tauri desktop                                                                                                        |
| -------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **MangaDex API**           | `/_mdx/*` proxy, because `api.mangadex.org` only sends CORS headers for localhost | direct to `api.mangadex.org`                        | serves `dist/` from a custom scheme, so `window.location.hostname` is **not** a Netlify host and **not** `localhost` |
| **Cover images**           | need `Referrer-Policy: no-referrer` or the CDN swaps in a placeholder             | no Referer sent                                     | inherits the web build's behaviour without Netlify's headers                                                         |
| **Supabase token refresh** | SDK handles visibility itself                                                     | `AppState` listener starts/stops `autoRefreshToken` | web path                                                                                                             |
| **Storage**                | AsyncStorage → localStorage                                                       | AsyncStorage → native                               | localStorage in the webview                                                                                          |
| **Safe areas**             | no-op                                                                             | notches and gesture bars                            | window chrome                                                                                                        |

`resolveBase()` in `src/api/mangadex.ts` decides the API base from `window.location.hostname`. **Verify this on desktop when touching it**: Tauri serves from `tauri://localhost` or a custom protocol, so the localhost branch may or may not be taken, and the fallback is a `/_mdx` path that has no proxy behind it.

## Checklist for a platform-sensitive change

Ask these before assuming a change is done:

- **Network** — does the URL depend on origin? Web proxies, native does not, desktop is neither.
- **Storage** — is the key namespaced? Web and desktop share an origin-scoped store; a collision between `kasane-progress`, `kasane-preferences`, and `kasane-query-cache` would be silent.
- **Navigation** — does the deep link work from cold start? Web needs the SPA fallback, native needs the `kasane` scheme from `app.json`, desktop needs both.
- **Input** — is there a hover or keyboard affordance? Web and desktop have pointers and tab focus; native does not. `hovered` on the Pressable style-callback state is web-only (declared in `src/types/react-native-augment.d.ts`).
- **Layout** — does it assume a viewport? Desktop windows resize freely, phones do not.
- **Fonts** — `expo-font` loads before `SplashScreen.hideAsync()`; a new font must be added to the `useFonts` call in `app/_layout.tsx` or text renders invisible on native.

## Branching

Use `Platform.OS` / `Platform.select` only when behaviour genuinely differs, and comment **why**, as `src/api/supabase.ts` and `src/api/mangadex.ts` both do. An uncommented branch is unmaintainable because the next reader cannot tell whether the constraint still holds.

Prefer `.web.ts` / `.native.ts` file extensions over an inline branch when an entire module differs.

## Verifying

```bash
bun run web                              # browser
bun run ios                              # simulator (Mac + Xcode)
bun run android                          # emulator
bun run build:web && bun run desktop:dev # Tauri window
```

Web-only verification is not verification. At minimum, run the target whose behaviour you branched on.

## Common mistakes

| Mistake                                             | Consequence                                                             |
| --------------------------------------------------- | ----------------------------------------------------------------------- |
| Testing a network change only in the browser        | The Netlify proxy hides that the native path is broken, or the reverse. |
| Assuming the Tauri build behaves like the web build | It ships the web bundle without Netlify's headers or redirects.         |
| Adding a font without updating `useFonts`           | Text is invisible on native; web falls back silently.                   |
| Using `hovered` for essential state                 | There is no hover on touch devices.                                     |
| Branching without a comment                         | Nobody can tell later whether the workaround is still needed.           |
