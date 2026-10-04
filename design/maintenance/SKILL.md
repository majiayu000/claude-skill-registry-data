---
name: maintenance
description: Periodic repository health check — install, full validation, unused-code scan, outdated/vulnerable dependencies, and docs drift — ending in a concise report and, when there are safe fixes, a single PR. Designed to run unattended from a scheduled routine; also usable on demand.
argument-hint: "[--report-only]"
---

# Repository maintenance

Run unattended-safe: never push to `master`, never merge, never force-push. Mode: `$ARGUMENTS` (`--report-only` = no branch, no PR).

## 1. Health

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm format:check
pnpm typecheck
pnpm test
pnpm knip --include-entry-exports --no-exit-code
```

Record pass/fail and the first actionable error for each.

## 2. Dependencies

- `pnpm outdated`: group into patch/minor vs major. Note majors for Nuxt, Nuxt UI, Tailwind, AI SDK, and Vitest/Playwright, with a one-line migration risk each.
- `pnpm audit`: list high/critical advisories with the dependency path, marking dev-only ones. Include dev dependencies: `--prod` hid two high-severity `sharp` advisories. Note that 0.x packages (like `sharp`) never get minor bumps from `pnpm update` within a caret range.
- GitHub Actions: for each `uses:` in `.github/workflows/`, find the latest major (`git ls-remote --tags --refs https://github.com/<owner>/<action>.git`; some actions keep majors as branches). Flag actions whose current tag runs on a deprecated Node runtime, and follow the bump procedure in `.claude/rules/github-ci.md`.
- Don't upgrade majors here. Patch/minor bumps are Dependabot's job unless a security advisory needs a targeted fix.

## 3. Drift

Run the `docs-sync` checks in report-only mode and include the findings.

## 4. Stale product data

- AI model IDs in `app/types/ai.ts`: flag models the providers have deprecated or retired (check provider docs if network allows; otherwise list them as "verify").
- Tailwind palettes: compare `shared/constants/theme.ts` palettes with the installed `tailwindcss/theme.css`.
- `public/.well-known/security.txt`: `Expires` must be in the future. Flag it when it's within 60 days, and renew it to under a year ahead (RFC 9116). An expired file tells researchers the contact is stale.

## 5. Act

- Nothing actionable → report only. Don't open a PR or issue.
- Safe, mechanical fixes (lint auto-fix, doc drift, dead config, failing test caused by drift) → branch `chore/maintenance-YYYY-MM-DD`, commit with Conventional Commits, push, open **one** PR whose description is the report.
- Anything needing judgment (major upgrades, behavior changes, security advisories without an obvious patch) → include in the report as a recommendation and don't change code.

## Report format

`## Health` (table), `## Dependencies`, `## Drift`, `## Recommendations`. Keep it under ~60 lines.
