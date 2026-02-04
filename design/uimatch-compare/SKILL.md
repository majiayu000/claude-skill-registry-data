---
name: uimatch-compare
description: >
  Run a single-shot visual comparison between a Figma design node and an implementation URL
  (local app, Storybook iframe, or deployed page) using @uimatch/cli, then read the generated
  report to explain design fidelity and quality gate status. Use this skill when the user wants
  to check whether one specific UI component or page matches its Figma design or debug a
  particular mismatch.
---

# uiMatch Visual Compare Skill

## Purpose

Run a **single visual comparison** between a Figma design node and an implementation URL  
(local app, Storybook iframe, or deployed page), then interpret the result.

Use this skill to:

- check how closely one component/page matches a Figma design
- get a Design Fidelity Score (DFS) and visual diff images
- enforce quality gates in local workflows before CI

---

## Environment / assumptions

- Run commands from the repository root.
- `@uimatch/cli` is installed as a devDependency.
- Playwright is installed and Chromium is available:
  - `npx playwright install chromium` has already been run.
- Node.js 20+ is available.

### Figma token (IMPORTANT)

The uiMatch CLI does **not** load `.env` files automatically.  
Before running any `uimatch compare` command, ensure:

```bash
export FIGMA_ACCESS_TOKEN="figd_..."
```

If the user mentions Figma API errors, check this first.

### Figma reference and shell quoting (IMPORTANT)

- Prefer `FILE_KEY:NODE_ID` format to avoid shell escaping issues:

  ```bash
  figma=AbCdEf123:1-2
  ```

- If you must use a full Figma URL, **always quote it**:

  ```bash
  figma='https://www.figma.com/file/AbCdEf123/MyDesign?type=design&node-id=1-2&mode=design'
  ```

Unquoted `?`, `&`, `=` may cause the shell to split the URL into multiple arguments and fail.

For more shared environment notes, see:

- `../_shared/uimatch-common-env.md`

For advanced tuning (viewport, dpr, size, contentBasis), see:

- `../_shared/uimatch-advanced-settings.md`

---

## How to run a comparison

### Recommended basic command

```bash
npx uimatch compare \
  figma=<FILE_KEY>:<NODE_ID> \
  story=<URL> \
  selector=<CSS_SELECTOR> \
  profile=component/dev \
  size=pad contentBasis=intersection \
  outDir=./uimatch-reports/<short-name>
```

Required parameters:

- `figma`: Figma file reference (`FILE_KEY:NODE_ID` or quoted full URL)
- `story`: implementation URL
  - Local app: `http://localhost:3000/your-page`
  - Storybook: `http://localhost:6006/iframe.html?id=button--primary`

- `selector`: CSS selector or data-testid for the element to capture

Recommended defaults:

- `profile=component/dev` – good balance for daily development
- `size=pad contentBasis=intersection` – handles page-vs-component cases well
- `outDir=./uimatch-reports/<short-name>` – per-comparison output folder

Examples:

```bash
# Storybook component vs Figma
npx uimatch compare \
  figma=AbCdEf123:1-2 \
  story=http://localhost:6006/iframe.html?id=button--primary \
  selector="#storybook-root button" \
  profile=component/dev \
  size=pad contentBasis=intersection \
  outDir=./uimatch-reports/button-primary
```

If layout depends on viewport or HiDPI, and you need to tweak them explicitly, add `viewport=` and/or `dpr=` as described in `../_shared/uimatch-advanced-settings.md`.

---

## Interpreting results

After `compare` finishes, open `<outDir>/report.json`.
Claude Code should:

1. Read `metrics.dfs` (Design Fidelity Score, 0–100).
2. Check `qualityGate.pass` (true/false).
3. If `pass` is false, inspect:
   - `qualityGate.reasons`
   - other metrics or style diffs if present.

Then:

- Summarize DFS and pass/fail status.
- Explain the main reasons in plain language (colors, spacing, layout, etc.).
- Suggest concrete changes (e.g. update CSS to match Figma, adjust padding, fix font size).

---

## When to use this skill

Use this skill when:

- The user is focusing on a **single component or page**.
- They want a detailed visual diff and numeric score.
- They are debugging one specific Figma node vs one URL.

If they want to run many comparisons at once, prefer the `uimatch-suite` skill.
If they only care about text/copy differences, prefer the `uimatch-text-diff` skill.
