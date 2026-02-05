---
name: uimatch-suite
description: >
  Run a batch of visual comparisons defined in a uiMatch suite JSON file using @uimatch/cli,
  then read each report to summarize which components passed or failed their quality gates.
  Use this skill when the user wants to run many Figma-vs-implementation checks at once,
  such as CI-style validation for a component library or flow.
---

# uiMatch Suite Skill

## Purpose

Run a **batch of visual comparisons** defined in a JSON suite file and summarize overall results.

Use this skill to:

- execute multiple uiMatch comparisons in one go
- support CI-style checks locally
- see which components fail their quality gates across a suite

---

## Environment / assumptions

- Run commands from the repository root.
- `@uimatch/cli` is installed as a devDependency.
- Playwright and Chromium are already installed:
  - `npx playwright install chromium` has been run previously.
- Node.js 20+ is available.

### Figma token (IMPORTANT)

The uiMatch CLI does **not** load `.env` files automatically.  
Before running any `uimatch suite` command:

```bash
export FIGMA_ACCESS_TOKEN="figd_..."
```

Suite items that rely on Figma API will fail if this is missing.

### Figma references and quoting

Inside the suite JSON:

- Prefer `FILE_KEY:NODE_ID` format for `figma` fields:

  ```json
  {
    "figma": "AbCdEf123:1-2"
  }
  ```

- If a full Figma URL is used, it is stored in JSON and not parsed by the shell directly,
  so shell escaping is less of a problem. Still, keep URLs valid and unbroken.

For more shared environment notes, see:

- `../_shared/uimatch-common-env.md`

For advanced tuning (viewport, size, contentBasis, dpr) on suite items, see:

- `../_shared/uimatch-advanced-settings.md`

---

## Suite command usage

### Basic command

```bash
npx uimatch suite \
  path=<PATH_TO_SUITE_JSON> \
  outDir=<OUTPUT_DIR> \
  concurrency=<NUMBER>
```

Recommended:

- `outDir=.uimatch-suite`
- `concurrency=4`

Example:

```bash
npx uimatch suite \
  path=.github/uimatch-suite.json \
  outDir=.uimatch-suite \
  concurrency=4
```

---

## Suite file shape (high level)

A typical suite JSON looks like:

```json
{
  "name": "Component Suite",
  "defaults": {
    "profile": "component/dev",
    "story": "http://localhost:6006"
  },
  "items": [
    {
      "name": "Button Primary",
      "figma": "AbCdEf123:1-2",
      "story": "http://localhost:6006/iframe.html?id=button--primary",
      "selector": "#storybook-root button"
    },
    {
      "name": "Card Component",
      "figma": "AbCdEf123:3-4",
      "story": "http://localhost:6006/iframe.html?id=card--default",
      "selector": "#storybook-root .card"
    }
  ]
}
```

For full schema details, see `docs/docs/cli-reference.md` (suite section).

---

## Interpreting suite results

For each item, uiMatch will create a subdirectory under `outDir`:

- `<outDir>/<item-slug>/figma.png`
- `<outDir>/<item-slug>/impl.png`
- `<outDir>/<item-slug>/diff.png`
- `<outDir>/<item-slug>/report.json`

Claude Code should:

1. Enumerate all item directories under `outDir`.
2. For each `report.json`, read:
   - `metrics.dfs`
   - `qualityGate.pass`
   - `qualityGate.reasons`

3. Build a summary:
   - Which items passed
   - Which items failed (with reasons)
   - Any patterns across failures (e.g. all failing on color or spacing)

If CI-like behavior is desired, note that:

- `uimatch suite` will exit with:
  - `0` when all items pass
  - `1` when one or more items fail
  - `2` for configuration errors

---

## When to use this skill

Use this skill when:

- The user already has (or is willing to create) a suite JSON file.
- They want to run **multiple comparisons** consistently (e.g. on every PR).
- They care about overall health of a component library or flow, not just one component.

For one-off comparisons, prefer the `uimatch-compare` skill.
For text-only checks, prefer the `uimatch-text-diff` skill.
