---
name: github-devops
description: GitHub Actions CI/CD workflows, automated testing gates, branch protection, and production release management for LKDV.
---

# GitHub DevOps & CI/CD for LKDV

This skill covers GitHub workflow management, repository automation, pull request verification, and production release pipelines for LKDV.

## 1. Quality Gates & Pre-Commit Verification

Before opening a pull request or pushing code:
1. `npm run type-check` (Strict TypeScript, 0 errors).
2. `npm run lint` (ESLint 9, 0 warnings/errors).
3. `npx vitest run src/features/compas` (or `npm run test:unit`).
4. Validate that no sensitive keys or `.env` files are tracked by Git.

## 2. GitHub Actions CI Pipeline

- Standard workflow file: `.github/workflows/ci.yml`.
- Jobs:
  - **Typecheck & Lint**: Runs Node.js 22 LTS, installs dependencies, verifies types and linting rules.
  - **Unit & Integration Tests**: Runs Vitest test suites.
  - **E2E Smoke Tests**: Playwright smoke verification against preview builds.
  - **Build Verification**: Ensures `next build` passes with zero errors and generates valid production bundles.

## 3. GitHub MCP & Automation

- **GitHub MCP Server**:
  - List and inspect issues, PRs, workflow run statuses, commit logs, and repository file trees.
  - Automate branch synchronization and release summaries.
- **Git Branch Conventions**:
  - Working branch for Compas: `claude/compas-p1-referentiel` (or dedicated feature worktree).
  - Main production branch: `main`. Never push directly to `main` without review and explicit confirmation.
