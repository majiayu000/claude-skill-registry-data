---
name: mav-bp-linting
description: Linting conventions for applications. Covers linter selection, rule configuration, auto-formatting, CI integration, and project linting guidance. Applied when writing or reviewing code, or configuring developer tooling.
user-invocable: false
disable-model-invocation: true
---

# Linting Standards

Code quality is enforced automatically through static analysis and formatting — style decisions are made once in config, then enforced by tooling, never debated in review.

## Maverick's Rules

- **Error-only policy** — every enabled rule is `error`, never `warn`. Warnings are noise: if a rule matters, it's an error; if it doesn't, disable it; if it has too many false positives, disable it and find an alternative. "Too many existing violations" is not a reason to downgrade — fix incrementally or baseline.
- **Linting and formatting are separate tools** — disable all style/formatting rules in the linter and delegate to the formatter (ESLint + Prettier; Ruff + Ruff format for Python — Ruff replaces flake8/pylint and Black; gofmt is non-negotiable in Go).
- **ESLint flat config is mandatory** — `eslint.config.js`, not legacy `.eslintrc`. Ignore patterns live in the flat config's `ignores` field. Ignore generated/vendor code; never ignore source code to dodge lint errors.
- **One config per project**, at the root — no per-directory overrides unless structurally necessary (e.g., test files).
- **Start from recommended presets** (`@eslint/js` + `typescript-eslint` recommended, `eslint-plugin-react-hooks` for React, Ruff defaults) and override selectively — never build a ruleset from scratch.
- **Inline disables**: require an explanatory comment, scope to one line (not a file), and treat them as technical debt in review. Never use them to silence an issue instead of fixing the root cause.
- **Pre-commit hooks format only** (`lint-staged` / `pre-commit` on staged files) — linting runs in CI. Never skip hooks with `--no-verify`; if a hook is too slow, fix the hook.
- **CI is the final gate** — run the linter (fail on any error) and the formatter in check mode, on **all** files, not just changed ones.

## Project Implementation Lookup

Check for `docs/maverick/skills/linting/SKILL.md`. If present, read it and follow it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting Linting Issues in Code Review

| Pattern | Issue | Fix |
| ------- | ----- | --- |
| No linter config in project | No automated quality checks | Add linter + formatter with recommended presets |
| Warnings in linter config | Warnings are ignored | Change to errors or disable |
| Formatting rules in linter | Conflicts with formatter | Disable formatting rules, use a dedicated formatter |
| Many inline disables without comments | Suppressed issues without justification | Require explanation or fix the violations |
| No CI lint step | Lint issues merge to main | Add lint + format check to CI pipeline |
| Lint config uses legacy format | Maintenance burden | Migrate to current format (e.g., ESLint flat config) |
| No pre-commit formatting | Style inconsistency across commits | Add lint-staged or equivalent |
| Linter running on generated/vendor code | False positives, slow runs | Update ignore patterns |

<!-- maverick-plugin-version: 4.0.2-dev -->
