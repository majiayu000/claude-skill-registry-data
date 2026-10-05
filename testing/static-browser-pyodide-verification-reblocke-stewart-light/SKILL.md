---
name: static-browser-pyodide-verification
description: Use when changing the static web app, Pyodide loading, staged Python files, browser contracts, or GitHub Pages deployment.
---

# Static Browser Pyodide Verification

- Keep Python package code as the source of truth; stage it into the static app with the documented script.
- Verify the browser imports the staged package, executes the contract, and renders expected outputs.
- Check both local unit/contract tests and browser smoke or Playwright tests when available.
- Confirm CDN, local asset paths, `.nojekyll`, and worker paths are valid for GitHub Pages.
- Do not add persistence, telemetry, external APIs, or PHI-bearing URLs unless explicitly approved.
- Document deployment or browser-runtime decisions in `docs/DECISIONS.md`.
