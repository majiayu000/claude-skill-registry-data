---
name: demos
description: Use when creating demos or POCs
---

Scaffold files from ./assets/:

- index.html: For all static content
- script.js: For all dynamic content
- config.json: optional configs for demos, dataset, prompt, model, schema, ...
  - Use config.js instead when template literals and minimal JS expressions are needed
- README.md: Explains what the app does (functionally), how to run locally/deploy
- LICENSE: MIT

Guidelines:

- Prefer pure-front-end apps that can be deployed on GitHub pages.
- Make it easy to demo.
  - Begin with a 1-3 para functional description of what the app does and how to use it. Include lightweight `.webp` screenshot
  - Include cards from config.json to run a demo with one click
  - Include synthetic sample datasets as CSV/JSON each <= 1MB, total <= 5MB
  - Support deep-linkable demo state via URL params / hash
  - Provide one-click downloads for generated artifacts / outputs
- Make it self-serve
  - Allow users to upload their own data
  - Include a collapsible settings form to edit prompts, models, schema, ... with defaults from config.json.
  - Persist settings with https://www.npmjs.com/package/saveform allowing reset
- Provide a responsive UX
  - Use lit-html for DOM updates
  - Always show a spinner while awaiting network call. Show progress bars for batch/iterative work
    - Disable primary buttons while running; re-enable on completion/failure.
  - Always stream LLM responses. Stream JSON with partial-json. Render LLM output with marked. Highlight code blocks
  - Use modals for drill-down without cluttering the main UI
  - Support keyboard navigation, e.g. arrow keys, tab, for fast review
  - #TODO Output style, readability, etc.

Code style:

- Prefer CDNs over `npm install` (less build steps).
- Lint with dprint and oxlint
  - dprint fmt -c https://raw.githubusercontent.com/sanand0/scripts/refs/heads/main/dprint.jsonc
  - npx -y oxlint --fix
- If using pyodide to run Python code, use ./assets/pyworker.js as follows:
  ```js
  const pyodideWorker = new Worker("./pyworker.js", { type: "module" });
  pyodideWorker.addEventListener("message", listener);
  pyodideWorker.postMessage({ id, code, data, context: { } });
  pyodideWorker.removeEventListener("message", listener);
  ```
- If running DuckDB WASM for SQL, use ./assets/duckdb.js.

GitHub:

- Add a brief description. Tags: optional
- Deploy on GitHub Pages: `gh api repos/:owner/:repo/pages -F 'source[branch]=main' -F 'source[path]=/'`
- Ensure that the "About" section is linked to the GitHub Pages URL
