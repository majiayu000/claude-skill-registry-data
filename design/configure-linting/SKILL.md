---
name: configure-linting
description: Use when setting up lint and format in a frontend project - installs Biome as the only linter, formatter, import sorter and Tailwind class sorter (replacing ESLint/Prettier), with Vue SFC support, a lefthook pre-commit hook and a CI check.
---

# Configure Linting

## 1. Audit current state

Read `.claude/stack-profile.md` if present: `lint_format.ts` is `biome` by default. Any other value (an ESLint/Prettier or Oxlint setup the team chose) means follow it: say so, add nothing from this skill, and stop. `package_manager` replaces `pnpm` below (`../_shared/stack-versions.md`, "Stack profile").

Detect what's already present:
```bash
ls biome.json biome.jsonc .prettierrc* prettier.config.* .prettierignore eslint.config.* .eslintrc* lefthook.yml .husky 2>/dev/null
grep -E '"(@biomejs/biome|prettier|prettier-plugin-tailwindcss|eslint|oxlint|lefthook)"' package.json 2>/dev/null
grep -E '"(recommended)"\s*:' biome.json 2>/dev/null   # pre-2.5 config — run `biome migrate`
```

- **Prettier present?** Port its options with `pnpm biome migrate prettier --write`, then delete the Prettier config, `.prettierignore`, `prettier` and `prettier-plugin-tailwindcss`. See `lint-and-format.md`.
- **ESLint present?** Port the rules with `pnpm biome migrate eslint --write`, review the diff, then delete the ESLint config + deps. Don't silently delete a config someone tuned — say what moved and what Biome can't cover.
- **`oxlint` from the Vite 8 React template?** Remove `oxlint`, `.oxlintrc.json` and the `"lint": "oxlint"` script — Biome owns lint.

## 2. Decide what to do

- Nothing → full setup (steps 3–7).
- Biome + Prettier (or ESLint) → migrate (step 1), then apply step 4.
- Biome with `formatter.enabled: false` (the pre-0.6 split) → turn the formatter on, remove Prettier.
- Biome-only and current → confirm lefthook + CI script, then exit "Linting already in place."

## 3. Install (only what's missing)

```bash
pnpm add -D -E @biomejs/biome
pnpm add -D lefthook
```

`-E` pins Biome to an exact version: a linter minor bump can add rules that fail CI, so reproducibility beats auto-upgrade here.

## 4. One tool — Biome lints, formats, sorts imports and classes

**Biome is the only linter and formatter.** One binary, one config, one pass. The Prettier options this plugin used (single quotes, 2-space indent, 80 columns) map 1:1 onto Biome's formatter, so the output keeps its shape.

### `biome.json` (React)
```json
{
  "$schema": "https://biomejs.dev/schemas/2.5.15/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "files": { "ignoreUnknown": true },
  "formatter": { "enabled": true, "indentStyle": "space" },
  "javascript": { "formatter": { "quoteStyle": "single" } },
  "css": { "parser": { "tailwindDirectives": true } },
  "linter": {
    "enabled": true,
    "rules": {
      "preset": "recommended",
      "style": { "useImportType": "error" },
      "nursery": {
        "useSortedClasses": {
          "level": "warn",
          "fix": "safe",
          "options": { "functions": ["cn", "clsx", "cva"] }
        }
      }
    },
    "domains": { "react": "recommended" }
  },
  "assist": { "enabled": true, "actions": { "source": { "organizeImports": "on" } } }
}
```

### Vue — swap the domain, turn on full SFC support
```json
{
  "html": {
    "experimentalFullSupportEnabled": true,
    "formatter": { "enabled": true, "selfCloseVoidElements": "always" }
  },
  "linter": {
    "rules": {
      "style": { "useVueMultiWordComponentNames": "off" }
    },
    "domains": { "vue": "recommended" }
  }
}
```
Add `html` to the React file, **add** `useVueMultiWordComponentNames` to the existing `rules.style` (keep `preset`, `useImportType` and `useSortedClasses`), and replace the `react` domain with `vue`. Full support makes Biome read the `<template>`: Vue rules (`useVueVForKey`, `noVueVIfWithVFor`, …), a11y rules (`useAltText`, `useButtonType`, …) and formatting all apply, and template usage no longer looks like unused variables. `vue-tsc` stays the type check for templates. Single-word names (`Button.vue`) stay allowed so components map 1:1 to React.

- `preset` replaces the deprecated `"recommended": true` (Biome 2.5). Match the `$schema` version to the Biome you installed.
- `style.useImportType` mirrors `verbatimModuleSyntax` from `configure-typescript`.
- `useSortedClasses` is a nursery rule with an unsafe fix by default; `"fix": "safe"` lets `biome check --write` sort classes like `prettier-plugin-tailwindcss` did. It sorts `class`/`className` and the strings passed to `cn()`/`clsx()`/`cva()`.
- `css.parser.tailwindDirectives` lets Biome parse `@theme`, `@custom-variant` and `@apply`.

## 5. package.json scripts

```json
{
  "scripts": {
    "lint": "biome check",
    "lint:fix": "biome check --write",
    "format": "biome format --write",
    "check": "biome ci",
    "prepare": "lefthook install"
  }
}
```

Local + pre-commit use `--write` (autofix); CI uses `biome ci` (report, never fix). Type errors are `pnpm typecheck` (`configure-typescript`), a separate CI step: Biome does not type-check, and Vue templates need `vue-tsc`. `prepare` installs the git hooks on every `pnpm install` (pnpm blocks dependency install scripts by default, so the lefthook package cannot do it).

## 6. Pre-commit with lefthook

lefthook (one Go binary, one YAML file) over husky. Keep the hook fast — fix staged files only.

### `lefthook.yml`
```yaml
pre-commit:
  commands:
    biome:
      glob: "*.{js,jsx,ts,tsx,vue,json,jsonc,css,html}"
      run: pnpm biome check --write --no-errors-on-unmatched {staged_files}
      stage_fixed: true
```

Biome does not format Markdown or YAML; leave them to the editor (the old Prettier hook did format them).

Install the git hooks now (later clones get them through the `prepare` script):
```bash
pnpm lefthook install
```

## 7. Verify

```bash
pnpm biome ci
```

Expected: passes (or reports fixable issues — run `pnpm lint:fix`, then re-check). `pnpm lefthook run pre-commit` exercises the hook. The same `check` runs in CI, so the hook is a convenience, not the gate.

## References
- ./lint-and-format.md — why Biome alone, the Prettier/ESLint migration, the `useImportType` ↔ `verbatimModuleSyntax` link, Vue full support and its limits, Tailwind class sorting, CI wiring.
- ../_shared/stack-versions.md — Biome / tooling version policy.
- ../_shared/conventions.md — `@/` alias, file naming, `stores/` rule.
