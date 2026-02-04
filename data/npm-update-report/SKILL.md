---
name: npm-update-report
description: Check for outdated npm/pnpm/yarn packages, update them, and generate impact/risk assessment reports with changelog investigation and security audit. Use when asked to "check npm updates", "update dependencies", "review package updates", "update and report", or "check for breaking changes".
---

# Package Update Report

## Workflow

| Step | Action           | Details                                                            |
| ---- | ---------------- | ------------------------------------------------------------------ |
| 1    | Detect PM        | Check lock file to determine package manager                       |
| 2    | Check outdated   | List packages with available updates                               |
| 3    | Update packages  | Update according to strategy below                                 |
| 4    | Classify changes | Extract diff from `package.json`, classify as major/minor/patch    |
| 5    | Investigate      | Web search changelogs for major/minor bumps and key packages       |
| 6    | Assess impact    | Grep for package usage, evaluate breaking changes                  |
| 7    | Audit            | Run security audit, include advisory URLs for vulnerabilities      |
| 8    | Verify           | Run scripts from package.json (lint, typecheck, test, build)       |
| 9    | Output           | See [references/report-template.md](references/report-template.md) |

## Package Manager Detection

| Lock File           | PM   | Outdated        | Update                       | Audit        |
| ------------------- | ---- | --------------- | ---------------------------- | ------------ |
| `package-lock.json` | npm  | `npm outdated`  | `npm update` / `npm install` | `npm audit`  |
| `pnpm-lock.yaml`    | pnpm | `pnpm outdated` | `pnpm update` / `pnpm add`   | `pnpm audit` |
| `yarn.lock`         | yarn | `yarn outdated` | `yarn upgrade` / `yarn add`  | `yarn audit` |

For monorepos: `pnpm --filter {pkg}`, `npm -w {pkg}`, `yarn workspace {pkg}`

## Update Strategy

| Type  | Action                                |
| ----- | ------------------------------------- |
| Patch | Auto-update via `{pm} update`         |
| Minor | Auto-update, investigate key packages |
| Major | Confirm with user before update       |

## Investigation Criteria

**Sources:** GitHub Releases, CHANGELOG.md, official blogs only

**Always investigate:**

- Major version bumps (breaking changes likely)
- Minor bumps of: frameworks (React, Vue, Next.js), build tools (Vite, esbuild), test tools (Vitest, Jest)

**Investigate if verification fails:**

- Any package that may be related to the failure

**Skip:** Patch-only updates with passing verification

## Verification Failure Handling

If verification fails:

1. Identify failing script and error message
2. Search for related packages in the error
3. Investigate those packages' changelogs for breaking changes
4. Document findings in report under "Verification Results"
5. Set conclusion to "Needs attention" with specific action items
