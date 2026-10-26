---
name: chrome-extension-mv3
description: Use when building a Chrome extension with Manifest V3 in TypeScript and Vite — service-worker background, offscreen documents for audio and DOM work, capturing tab audio with tabCapture, AudioWorklet recording, heavy analysis in Web Workers, saving files with fallbacks, minimal permissions and privacy by design. Also use when an MV3 background script stops unexpectedly, tab capture fails, or saving files works in one browser context but not another.
---

# Chrome extensions (Manifest V3)

Default: TypeScript + Vite with one entry per extension context (service worker, popup, offscreen document, workers), the smallest permission set that works, all user data kept on the user's machine.

## Contexts and their limits

| Context | Can | Cannot |
|---|---|---|
| Service worker (background) | Events, messaging, `chrome.*` APIs | DOM, audio playback; it is stopped when idle |
| Popup / options page | DOM, user gestures | Live long — closes when focus leaves |
| Offscreen document | DOM, Web Audio, `getUserMedia` on a capture stream | UI visible to the user |
| Web Worker | CPU-heavy analysis | `chrome.*` APIs, DOM |

Keep state that must survive in `chrome.storage` or the offscreen document, not in service-worker globals.

## Capturing tab audio

1. The user clicks the action or popup button (a user gesture is required).
2. The service worker calls `chrome.tabCapture.getMediaStreamId({ targetTabId })`.
3. It creates an offscreen document (reason `USER_MEDIA`) and sends it the stream ID.
4. The offscreen document calls `getUserMedia` with `chromeMediaSource: "tab"` and that ID, routes the stream back to the speakers (otherwise the tab goes silent), and records with an `AudioWorklet` into chunks.
5. Cap recording length and memory; stop cleanly when the tab closes.

## Heavy processing

Send recorded samples to a Web Worker (transfer `ArrayBuffer`s, do not copy) for analysis or encoding; report progress back so the UI stays responsive.

## Saving files

- File System Access API (`showSaveFilePicker`) where available — it needs a user gesture in a document context.
- Fallback: `chrome.downloads.download` with a blob URL created in a document context.
- Bundling several outputs into one ZIP gives users a single file per save.
- Use neutral file names (date and time); do not put page titles or URLs into names or metadata if privacy matters.

## Permissions and privacy

- Request only what you use (`tabCapture`, `offscreen`, `downloads`, `storage`); avoid broad host permissions.
- Do not collect titles, URLs or content unless the feature needs it; never send captured data anywhere.
- Captured third-party audio is for private use; respect copyright and the site's terms.

## Verification loop

1. Unit-test analysis code in Node/Vitest with synthetic signals (known tones; measure SNR of the reproduction).
2. Load the unpacked extension (`chrome://extensions` → developer mode → load the build folder), record a short tab, save, inspect the files.
3. Reload the extension while recording to confirm it fails safely.

## Pitfalls

- **Service worker termination:** timers and in-memory state disappear; use `chrome.alarms` and storage.
- **One offscreen document at a time** per extension; check with `chrome.runtime.getContexts` before creating.
- **Firefox** differs in APIs (no offscreen documents in the same form, different capture APIs); treat it as a separate port.
- **Content Security Policy:** MV3 forbids remote code and `eval`; bundle everything.
