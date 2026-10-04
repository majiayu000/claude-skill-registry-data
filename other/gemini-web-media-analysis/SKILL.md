---
name: gemini-web-media-analysis
description: Attach a local image or video to gemini.google.com through Chrome automation and get an analysis, without opening a native file dialog. Use when a second opinion on a screenshot, render, contact sheet, frame grid, or gameplay capture is wanted and the user is already signed in to Gemini in Chrome. Both images and video work; the two paths differ and both are documented here.
---

# Gemini web media analysis

Attaches a **local image or video** to the Gemini web composer and reads the reply. Verified working on `gemini.google.com/app`, Chrome, signed-in account, 2026-08-15.

Needs the **claude-in-chrome** MCP server — `navigate`, `find`, `file_upload`, `computer`, `javascript_tool`, `get_page_text` — and a Chrome profile already signed in to Gemini. No API key.

**Two different paths. Use the right one:**

| Media | Path |
|---|---|
| **Video** | `find` Gemini's own hidden input → `file_upload` into it → real click on the composer. See [Video path](#video-path) |
| **Image** | Helper input → synthetic `paste` event. See [Image path](#image-path) |

> **Never click "Dateien hochladen" / "Upload files" in the uploads menu.** It opens the **native OS file dialog**, which blocks the whole automation session — no further tool call reaches the browser until a human dismisses it by hand.

## Video path

1. **Navigate** to `https://gemini.google.com/app`, wait for load.
2. **Real click** the `+` / "Uploads & Tools" button in the composer. A JS `.click()` does not open the menu — it needs real pointer events. The hidden input only exists while this menu is open.
3. **`find("hidden file input element")`** → returns Gemini's own input ref.
   **Make sure no helper input of yours is in the page** — it shadows this search and `find` returns yours instead. Remove it first.
   The `uploader` component does not mount on every menu open. If `find` comes back empty, close and re-open the menu and retry.
4. **`file_upload`** with the absolute video path and that ref.
5. **Real click into the composer text area.** This is the trigger — Angular picks the file up on the next tick.
6. **Wait, and be patient.** The thumbnail appears **later than you expect** — well beyond 8 s for a small clip. It renders as a still frame with a duration badge like `▶ 0:06`.
   **Do not conclude failure early.** That mistake cost a whole session once: the upload had in fact worked and was reported as impossible.
7. **Type the prompt and send**, then poll `get_page_text` for the reply. Video analysis takes 30–60 s.

## Image path

Gemini's own input rejects images — its `accept` list is documents and code only — so images go in through a synthetic `paste` instead. Build **your own** file input in the page, let the browser tool fill it with the real file, then hand that `File` object to the composer as paste data. Paste is the one mechanism Gemini's composer honours for images.

1. **Navigate** to `https://gemini.google.com/app` and wait for load.

2. **Inject a helper input** via the JavaScript tool:

```js
let el = document.getElementById('__cin_up');
if (!el) {
  el = document.createElement('input');
  el.type = 'file';
  el.id = '__cin_up';
  el.setAttribute('accept', '*/*');
  el.setAttribute('aria-label', 'claude helper upload');
  el.style.cssText = 'position:fixed;top:8px;left:8px;z-index:2147483647;width:240px;height:30px;';
  document.body.appendChild(el);
}
({ ready: true });
```

3. **Find it and fill it.** `find("claude helper upload file input")` → ref, then `file_upload` with the absolute path and that ref. Confirm it landed:

```js
const f = document.getElementById('__cin_up').files[0];
f ? ({ name: f.name, size: f.size, type: f.type }) : ({ error: 'no file' });
```

4. **Paste it into the composer.** This is the step that actually attaches:

```js
const f = document.getElementById('__cin_up').files[0];
const dt = new DataTransfer();
dt.items.add(f);
const ce = document.querySelector('[contenteditable="true"]');
ce.focus();
const pe = new ClipboardEvent('paste', {
  bubbles: true, cancelable: true, composed: true, clipboardData: dt
});
const notCancelled = ce.dispatchEvent(pe);
await new Promise(r => setTimeout(r, 2500));
({ notCancelled });                     // false means Gemini consumed it — that is success
```

5. **Confirm visually before typing.** Screenshot and check a thumbnail appears in the composer. The composer grows taller and the send button becomes enabled. If no thumbnail, stop — do not send a prompt that references an image Gemini never received.

6. **Remove the helper input** so it does not pollute later `find` calls — it will otherwise be returned instead of Gemini's own input:

```js
const e = document.getElementById('__cin_up'); if (e) e.remove(); ({ removed: true });
```

7. **Type the prompt and send.** Click the composer text area, type, click the send arrow. Poll with `get_page_text` for the reply; generation takes 20–40 s for an image.

## What does not work — measured, so nobody retries it

| Attempt | Result |
|---|---|
| Click "Dateien hochladen" / "Upload files" in the uploads menu | Opens the **native OS file dialog**, which blocks the whole automation session. Never click it |
| `file_upload` into Gemini's hidden input, then fire `input` + `change` from JS | The file genuinely lands in `input.files` — verified by reading name, size and type back — but nothing attaches. The synthetic events are not the trigger; a **real click into the composer** is, which is why the video path works |
| `paste` event carrying a `video/mp4` file | Handler fires and calls `preventDefault`, but nothing attaches. Images attach immediately by the exact same mechanics |
| `drop` event on the composer | Handler fires and calls `preventDefault`, nothing attaches — images and video alike |
| Assign a `DataTransfer` to Gemini's input from page JS | Gemini's input sits in a **closed shadow root**. `find` reaches it over CDP; `document.querySelectorAll` and a recursive open-shadow walk do **not** |
| `Set-Clipboard -Path <file>` then a synthetic Ctrl+V | Synthetic key events do not read the OS clipboard |
| Google Drive as a staging area | Drive has **no** `input[type=file]` in its DOM and drives uploads through the native dialog, so it cannot be automated either |

## Verified limits

- **`accept` is not a filter for programmatic setting.** Gemini's own input advertises a ~1006-character `accept` list of document and code extensions with no video type at all — yet `file_upload` into it works for `video/mp4`. `accept` only constrains the native dialog. Do not conclude a file type is unsupported from the `accept` attribute.
- **10 MB per `file_upload` call.** An 18.9 MB file returns "total upload size would exceed 10 MB". Splitting does not help for a single media file. Re-encode smaller instead: `-c:v libx264 -crf 22 -vf scale=1280:-2` put a 6 s 1280-wide capture at 0.17 MB.
- **Path must be inside a session folder.** The session scratchpad works; arbitrary paths are rejected.
- **A local HTTP server as a byte source does not work.** Gemini's CSP is `connect-src 'self' https://*.google.com … data:` — `localhost` is not allowed, and HTTPS→HTTP is mixed content regardless.
- **Base64 into the JS call is CSP-legal** (`data:` is present) but costs far too many tokens at video sizes. Viable for a small image if the helper-input path ever breaks.

## Practical guidance

For video, converting to a **frame grid** and sending that instead is often better than the video path — a labelled contact sheet lets the model compare poses directly, and it sidesteps the 10 MB cap:

```powershell
ffmpeg -y -i in.avi -vf "select='not(mod(n\,60))',scale=640:-1,tile=3x2" -frames:v 1 grid.png
```

Before sending anything the user has not published, say plainly that the upload goes to Google and get a yes. Unreleased game footage, internal documents and customer material are not yours to hand over.
