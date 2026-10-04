---
name: oxc-toolchain-setup
description: |
  Set up Oxlint + Oxfmt + Lefthook for React/Vite/Tailwind projects. Use when:
  (1) user asks to add oxlint, oxfmt, or oxc tooling, (2) setting up linting and
  formatting for a new React project, (3) migrating from ESLint/Prettier to oxc tools.
  Covers verified gotchas: lefthook npx requirement, sortTailwindcss object type,
  sortImports group format, React Router component mappings, config file naming.
author: Claude Code
version: 1.0.0
date: 2026-03-21
---

# Oxc Toolchain Setup (Oxlint + Oxfmt + Lefthook)

## Problem
Setting up Oxlint and Oxfmt has several non-obvious configuration requirements that differ
from what documentation examples suggest, leading to failed commits and silent config issues.

## Context / Trigger Conditions
- User asks to add oxlint and/or oxfmt to a project
- New React/Vite/Tailwind project needs linting and formatting
- Migrating from ESLint/Prettier to oxc tools
- Setting up pre-commit hooks with lefthook for oxc tools

## Verified Gotchas (as of oxlint 1.56, oxfmt 0.41, lefthook 2.1)

### 1. Lefthook needs `npx` prefix
`node_modules/.bin` is NOT in PATH during git hooks. Commands like `oxfmt {staged_files}`
fail with `command not found`. Always use `npx oxfmt` and `npx oxlint` in `lefthook.yml`.

### 2. `sortTailwindcss` is an object, not a boolean
`"sortTailwindcss": true` is INVALID. Use `"sortTailwindcss": {}` to enable with defaults.
It auto-detects Tailwind v4's stylesheet from the installed package.

### 3. `sortImports` groups use arrays for combining
Groups support array nesting: `["parent", "sibling", "index"]` sorts them together.
Default: `["builtin", "external", ["internal", "subpath"], ["parent", "sibling", "index"], "style", "unknown"]`
The key is `newlinesBetween` (boolean), not `newlinesBetweenGroups`.

### 4. `--write` is oxfmt's default
Unlike Prettier (stdout by default), oxfmt writes in-place by default. No `--write` flag
needed in hooks or scripts. Use `--check` for CI.

### 5. Config file is `.oxfmtrc.json`
Not `.oxfmt.json`. Supports JSONC (comments and trailing commas). Run `oxfmt --init` to
generate with `$schema` for IDE autocomplete.

### 6. `internalPattern` defaults include `~/` and `@/`
Projects using these path aliases don't strictly need to configure this.

### 7. React Router v7 template triggers lint error
Default scaffold generates `export function meta({}: Route.MetaArgs)` which oxlint flags
as `no-empty-pattern`. Fix: change to `_args: Route.MetaArgs`.

### 8. Lefthook `stage_fixed: true` for auto-fix hooks
Use `stage_fixed: true` instead of manual `git add {staged_files}` — it handles partially
staged files correctly.

### 9. Use `prepare` not `postinstall` for lefthook install
`"prepare": "lefthook install"` is skipped in CI/Docker production builds where `.git`
doesn't exist. `postinstall` would fail in those environments.

### 10. Oxfmt respects `.gitignore` automatically
No need to add ignore patterns for `node_modules/`, `build/`, etc.

## React Router v7 Component Mappings
When using React Router v7, map `Link`, `NavLink`, and `Form` in oxlint settings:
```json
{
  "settings": {
    "react": {
      "linkComponents": [
        { "name": "Link", "linkAttribute": "to" },
        { "name": "NavLink", "linkAttribute": "to" }
      ],
      "formComponents": [{ "name": "Form", "formAttribute": "action" }]
    },
    "jsx-a11y": {
      "components": { "Link": "a", "NavLink": "a", "Form": "form" }
    }
  }
}
```

## Verification
After setup, verify with:
1. `npx oxlint` — should show 0 errors
2. `npx oxfmt --check .` — should show 0 formatting issues (after initial format)
3. Make a trivial change, stage, commit — lefthook should run both tools
4. `bun run check` — should pass all three checks (format + lint + types)

## Notes
- Oxfmt is pre-1.0 (v0.41) — config schema may change between versions
- Always check `node_modules/oxfmt/configuration_schema.json` for current schema
- Lefthook sorts commands alphabetically by key name when `parallel: false`
- Both tools share one VS Code extension: `oxc.oxc-vscode`
