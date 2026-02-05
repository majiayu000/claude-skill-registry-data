---
name: npm-update-report
description: Generate npm package update reports with changelog investigation and impact assessment.
---

# npm Package Update Report Generator

Generate investigation reports for npm dependency updates with changelog research and verification.

## Workflow

| Step | Action            | Details                                                         |
| ---- | ----------------- | --------------------------------------------------------------- |
| 1    | Sync package.json | Match versions to lock file, keep semver prefix (`^`, `~`)      |
| 2    | Identify changes  | Extract diff from `package.json`, classify as major/minor/patch |
| 3    | Investigate       | Web search changelogs for major/minor bumps and key packages    |
| 4    | Assess impact     | Grep for package usage, evaluate breaking changes               |
| 5    | Verify            | Run scripts from package.json (lint, typecheck, test, build)    |
| 6    | Output            | Write report to `./reports/{yyyyMMdd}-{branch-name}.md`         |

## Investigation Criteria

**Always investigate:**

- Major version bumps (breaking changes likely)
- Minor bumps of: frameworks (React, Vue, Next.js), build tools (Vite, esbuild), test tools (Vitest, Jest)

**Investigate if verification fails:**

- Any package that may be related to the failure

**Skip investigation:**

- Patch-only updates with passing verification

## Key Rules

- Reference primary sources only: GitHub Releases, CHANGELOG.md, official blogs
- Detect package manager from lock file: `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn)
- For monorepos, use workspace filters (`pnpm --filter`, `npm -w`)

## Verification Failure Handling

If verification fails:

1. Identify failing script and error message
2. Search for related packages in the error
3. Investigate those packages' changelogs for breaking changes
4. Document findings in report under "Verification Results"
5. Set conclusion to "Needs attention" with specific action items

## Report Template

```markdown
# Package Update Report: {branch-name}

## Summary

| Metric       | Value            |
| ------------ | ---------------- |
| Verification | PASSED / !FAILED |
| Major        | {count}          |
| Minor        | {count}          |
| Patch        | {count}          |

## Notable Changes

### {package-name} ({old-version} -> {new-version}) [major/minor]

**Changes:**

- !Breaking: {description}
- New: {description}
- Fix: {description}

**Project Impact:** Affected / Not affected

- {affected-files-or-features}

**Reference:** [CHANGELOG]({url})

## Other Updates

| Package | Change             | Type  | Notes |
| ------- | ------------------ | ----- | ----- |
| {name}  | {x.x.x} -> {y.y.y} | patch | -     |

## Verification Results

### {script-name}

\`\`\`
{output-summary}
\`\`\`

## Conclusion

- **Breaking Changes:** No action required / !Action required: {details}
- **Recommendation:** Ready to merge / !Needs attention: {details}
```

## Formatting Rules

| Rule                   | Example                  |
| ---------------------- | ------------------------ |
| Version transition     | `18.2.0 -> 18.3.1`       |
| Breaking change prefix | `!Breaking: API removed` |
| Placeholder format     | `{placeholder-name}`     |
