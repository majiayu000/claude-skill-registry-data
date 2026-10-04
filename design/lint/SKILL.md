---
name: lint
description: Runs linting, formatting, and type checks for react-basics-ui. Triggers on "lint", "pre-commit", "format", "eslint", "prettier", "tsc", "type check", "code quality".
---

# Lint

Run all code quality checks. Report output as-is.

## Commands

Run these in order:

1. `npx tsc -p tsconfig.json --noEmit`
2. `npm run lint` — `eslint src --ext .ts,.tsx`
3. `npx prettier --check "src/**/*.{ts,tsx,css,md}"`

Notes:

- `tsconfig.json` covers the whole of `src/` — components, tests, and stories — so one type-check pass is enough. `tsconfig.test.json` exists for the test runner and is not a separate check target.
- ESLint uses **flat config** (`eslint.config.js`). There is no `.eslintrc.*`; ESLint 9 would ignore it.
- Stories relax several rules by design (`react-hooks/rules-of-hooks`, `no-console`, `react/no-unescaped-entities`) because CSF3 `render` functions are not components. Don't "fix" those by rewriting stories.

## Expected baseline

A clean run is **0 errors**. A handful of warnings (`no-non-null-assertion`, `no-explicit-any`) are known and tolerated — treat a *new* warning as worth a look, not a blocker.

## If there are failures

Ask the user if they want auto-fix. If yes, run:

- `npx eslint --fix src --ext .ts,.tsx`
- `npm run format` — `prettier --write "src/**/*.{ts,tsx}"`

Then re-run the check commands to show anything that remains.

Type errors are never auto-fixable — read them and fix the source.

---

## Optional: Accessibility check

ESLint cannot evaluate keyboard reachability, focus management, ARIA name/role/value correctness, contrast against semantic intent, hit-target size, or live-region behaviour. Those require the dedicated audit — and for a component library they matter more than usual, since every consumer inherits whatever the primitives do.

**When this prompt fires:**

- Lint ran and had no failures (or failures were fixed)
- The changes touch rendering components under `src/components/**/*.tsx` — not pure types, hooks, styles, or tests

**Prompt:**

```
Lint passed. The changes touch UI components ([list]).
Run /a11y to audit keyboard, focus, ARIA, contrast, and hit targets against WCAG 2.2 AA?

- Yes — invoke /a11y on the changed components
- Skip — defer accessibility review
```

Do not invoke `/a11y` automatically — accessibility findings can be substantial and the user should opt in. Skip the prompt entirely when:

- No component files changed
- Only non-rendering files changed (types, hooks, utils, tests, stories)
- Lint had unresolved failures (fix lint first)

---

## Boundary with Other Skills

| Skill | Relationship |
|-------|-------------|
| `/commit` | If a pre-commit hook runs `/lint`-style checks, `/commit` will surface their failures. `/lint` is the place to fix them. |
| `/a11y` | `/a11y` covers WCAG 2.2 AA (keyboard, focus, ARIA semantics, contrast, hit targets) — things lint cannot evaluate. See the optional prompt above. |
| `/test` | Type errors often surface first as test failures. Run `/lint` before chasing a confusing test failure. |
