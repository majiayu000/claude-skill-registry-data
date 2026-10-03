---
name: add-tool
description: Add a new document tool (tab) to the ReVision single-page UI. Use when asked to add a feature/tool/tab alongside Fine Print Analyzer, Enhance, Translate, or Jargonary, or to wire a new Claude-powered action into the frontend.
---

# Add a new ReVision tool

The four tools (Analyzer, Enhance, Translate, Jargonary) all live in
`src/revision/static/index.html`. Adding a tool is almost entirely a frontend
change — the backend `/api/messages` proxy is generic and usually needs no edits.

## Anatomy of a tool

Each tool is a tab wired through three parts of `index.html`:

1. **Tab button** — in the tab bar (`~line 481`):
   ```html
   <button class="tab-btn" data-tab="mytool">🛠️ My Tool</button>
   ```
2. **Tab panel** — a matching content section (`~line 488+`):
   ```html
   <div id="mytool" class="tab-content">
       <textarea id="mytoolInput" placeholder="..."></textarea>
       <button id="mytoolBtn">Run</button>
       <div id="mytoolResults"></div>
   </div>
   ```
   The tab switcher (`~line 714`) toggles `.active` by matching `data-tab` to the
   panel `id`, so the button's `data-tab` must equal the panel's `id`.
3. **Behavior** — a click handler that builds a prompt and calls the shared
   helper `callClaude(prompt, maxTokens = 3000)` (`~line 727`), which POSTs to
   `/api/messages` and returns the model's text (reads `data.error.message` on
   failure).

## Steps

1. Add the tab button (step 1) and panel (step 2), keeping ids consistent.
2. Add a handler modeled on an existing one (e.g. the Enhance handler,
   `~line 900`): read inputs, build the prompt, `await callClaude(...)`, render
   into the results div. **Escape untrusted model/user text with `escapeHtml`**
   before injecting into HTML; use `storeForClipboard` + `copyStored` for copy
   buttons, following existing tools.
3. If the tool needs structured output, prompt for JSON only and strip code
   fences before `JSON.parse`, as the Analyzer does (`~line 837`).

## Guardrails

- Do **not** call `api.anthropic.com` from the browser or embed the key — always
  go through same-origin `/api/messages`. The key and model stay server-side.
- Only change the backend if the tool needs a genuinely new capability (e.g. a
  new endpoint). If you do, add a test in `tests/test_server.py` using the
  injected-client seam, and keep the backend stdlib-only.
- Update the tool list in `README.md` and `CLAUDE.md` (project overview) so docs
  don't drift.

After changes, verify with the `run-app` skill and run the `test-and-lint` skill.
