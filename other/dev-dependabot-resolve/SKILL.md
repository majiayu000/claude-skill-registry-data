---
name: dev-dependabot-resolve
description: "Comprehensive dependency update workflow for resolving Dependabot alerts and PRs. Use when: (1) User wants to update dependencies, (2) User mentions 'dependabot', 'security vulnerabilities', or 'dependency updates', (3) User asks to run security audit, (4) User wants to create a deps-update PR. Analyzes Dependabot issues, runs pnpm audit, applies updates, runs quality checks (typecheck, lint, test, build), handles Playwright Docker image sync, creates PR with changelog."
---

# Dependabot Resolution Workflow

Execute a comprehensive dependency update workflow:

## Step 1: Analyze Dependabot Issues

- Use `gh issue list --label "dependencies" --state open --json number,title,url,body` to list all open Dependabot issues
- For each issue, carefully analyze:
  - What dependency is being updated
  - What version change is proposed (patch/minor/major)
  - Any breaking changes mentioned
  - Security vulnerabilities fixed
- Determine which updates should be applied based on:
  - Security fixes (high priority)
  - Patch updates (generally safe)
  - Minor updates (review carefully)
  - Major updates (review very carefully for breaking changes)

## Step 2: Run Security Audit

- Run `pnpm audit` to check for security vulnerabilities
- Identify any critical or high-severity issues
- Note any recommended updates from the audit

## Step 3: Create Update Branch

If there are updates to apply:

- Get current date in MMDD format (e.g., "1220" for December 20th)
- Get the current branch name to use as base
- Create new branch: `deps-update-MMDD` from the current branch
- Switch to the new branch

## Step 4: Apply Updates

- For each dependency to update:
  - Use `pnpm update <package-name>` or `pnpm add <package-name>@<version>` as appropriate
  - If it's a major version update, check for breaking changes in the changelog first
- After all updates, run `pnpm install` to ensure lockfile is updated

## Step 4.5: Handle Related Updates (Package + Infrastructure Sync)

Some packages require coordinated updates across multiple files. Check for these patterns:

### Playwright Package + Docker Image

When updating `@playwright/test` or `playwright` in package.json:

1. **Check current versions**:
- `package.json`: Look for `@playwright/test` and `playwright` versions
- `.github/workflows/*.yml`: Search for `mcr.microsoft.com/playwright:v` Docker image tags

2. **Update Docker image tag** to match the npm package version:

   ```yaml
   # In workflow files using Playwright Docker container
   container:
     image: mcr.microsoft.com/playwright:v<NEW_VERSION>-noble
   ```

3. **Verify image exists** at https://mcr.microsoft.com/v2/playwright/tags/list or check Microsoft's Playwright Docker documentation

4. **Example**: If updating `@playwright/test` from `1.57.0` to `1.58.0`:
- Update package.json: `"@playwright/test": "^1.58.0"`
- Update workflow: `image: mcr.microsoft.com/playwright:v1.58.0-noble`

### Other Common Pairs to Watch

- **TypeScript + @types packages**: May need coordinated updates
- **ESLint + plugins**: Plugin versions often need to match ESLint major version
- **Next.js + related packages**: `next`, `eslint-config-next`, etc.

## Step 5: Quality Checks

Run all quality checks in sequence:

1. **Type checking**: `pnpm typecheck`
2. **Linting**: `pnpm lint` (or `pnpm lint:fix` if auto-fixable)
3. **Formatting**: `pnpm format` (or `pnpm format:fix` if needed)
4. **Unit tests**: `pnpm test:unit`
5. **Build**: `pnpm build` (to ensure the project builds successfully)
6. **E2E tests**: `pnpm test:e2e:critical` or `pnpm test:e2e:full-prod` for comprehensive testing

## Step 6: Review Results

- If all checks pass:
  - Proceed to Step 7
- If any checks fail:
  - Investigate the failure
  - Determine if it's a breaking change or test needs updating
  - Fix issues or revert problematic updates
  - Re-run quality checks

## Step 7: Push and Create PR

Once all checks pass:

- Stage all changes: `git add .`
- Commit with descriptive message: `git commit -m "chore: Update dependencies (MMDD)"`
- Push to remote: `git push -u origin deps-update-MMDD`
- Create PR using `gh pr create` with:
  - Title: "chore: Update dependencies (MMDD)"
  - Body including:
    - List of updated packages and versions
    - Summary of security fixes (if any)
    - Links to Dependabot issues being resolved using list format:

      ```
      - 関連Issue
          - https://github.com/<owner>/<repo>/issues/<issue-1>
          - https://github.com/<owner>/<repo>/issues/<issue-2>
      ```

    - Note that all quality checks passed
  - **Use full URLs** (not #<number>) so GitHub auto-expands them to show issue titles

## Important Notes

- Never auto-merge - always create PR for manual review
- For major version updates, mention breaking changes in PR description
- If updating critical dependencies (Gatsby, React, etc.), note that extra testing may be needed
- Close related Dependabot issues after PR is merged
- Follow the project's dependency management guidelines from CLAUDE.md

## Safety Checks

- Never use `--force` flags
- Always run full test suite before pushing
- Check for deprecation warnings during build
- Verify the build output works correctly (`pnpm serve` and manual testing if needed)
