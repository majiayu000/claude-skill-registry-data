---
name: local-browser-live-preview
description: >
  See a local page in the browser while editing files in Cursor: run the right
  dev server (Vite HMR or static live-reload), dock Simple Browser beside the
  editor, and keep URL + port in sync so saves reflect almost instantly. Use when
  the user wants to watch a local browser tab, live preview, instant refresh
  while coding, or edit HTML/CSS/JS here and see changes immediately.
---

# Local browser live preview (edit here, see it now)

Cursor cannot literally “stream” an external Chrome tab into the chat. The reliable pattern is: **files in this workspace** → **local dev server** → **browser pointed at `localhost`** → **auto reload or HMR on save**. This skill tells the agent how to set that up and how you can **see the tab inside Cursor**.

## 1. Pick the stack

| What you are editing | Command (from project or folder root) | Instant updates |
|----------------------|----------------------------------------|-----------------|
| **Vite app** (`src/`, `vite.config.*`) | `npm run dev` | HMR — no full refresh |
| **Static HTML/JS** (e.g. `docs/.../logistica-carga-prototype/`) | `npx --yes live-server . --port=5174` *or* `npx --yes serve . -l 5174` | **Manual refresh** with `serve`; use `live-server` for **auto-reload on save** |
| **API + static** | API in one terminal; static server in another | Same as static |

\*Use a free port if `5174` is taken (`5175`, `8080`, etc.).

## 2. See the page **inside Cursor** (recommended)

1. Start the server (step 1).
2. Command Palette: **“Simple Browser: Show”** (or **View → Simple Browser**).
3. Open: `http://localhost:<PORT>/` (adjust path, e.g. `/index.html`).
4. **Dock** the Simple Browser panel **beside** the editor so edits and the page are visible together.

The agent edits files in the repo; **Vite** updates the DOM via HMR; **live-server** reloads the whole page when you save.

## 3. Agent workflow (when the user asks for live preview)

1. **Identify** the folder and entry (`index.html`, `main.jsx`, etc.).
2. **Start** the appropriate server (background if long-running), and tell the user the **exact URL**.
3. **Prefer** `live-server` for plain static prototypes so “save file → browser updates” without pressing refresh.
4. **Edit** only the files that back that URL (HTML, CSS, JS modules).
5. **Do not** claim the chat shows a live video of the tab; point to Simple Browser or an external browser on `localhost`.

## 4. Optional: one-liner for a specific prototype folder

From the prototype directory (example path — adjust to the real folder):

```bash
cd "docs/bmc-dashboard-modernization/logistica-carga-prototype" && npx --yes live-server . --port=5174 --open=/index.html
```

`--open` may vary by OS; if it fails, open `http://localhost:5174/index.html` manually in Simple Browser.

## 5. Related repo tools (do not duplicate)

- **Panelin Evolution viewer** (`~/.panelin-evolution/viewer/`, port **3847**): use skill **`panelin-live-editor`** — different app, same “edit files + refresh” idea.
- **Isolated JSX playground**: subagent **`live-jsx-dev`** (Vite + HMR for a single component file).
- **Automated checks / screenshots**: **`browser-agent-orchestration`** or Playwright — for verification, not primary “instant mirror while typing.”

## 6. Troubleshooting

| Symptom | Check |
|---------|--------|
| Blank or 404 | Correct **path** after port (`/`, `/viewer/`, `/index.html`). |
| No auto-reload | Switch from `serve` to **`live-server`**, or use **`npm run dev`** for Vite. |
| CORS / module errors | Serve over **http** (`live-server`/`serve`/`vite`), not `file://`. |
| Stale bundle | Hard refresh; for Vite, restart dev server after config changes. |

---

**Summary for the user:** Run **`live-server`** or **`npm run dev`**, open **Simple Browser** to that `localhost` URL, dock it next to the editor — then changes made here show up immediately (reload or HMR).
