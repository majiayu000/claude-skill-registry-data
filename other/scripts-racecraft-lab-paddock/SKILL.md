---
name: scripts
description: "Skill for the Scripts area of paddock. 486 symbols across 34 files."
---

# Scripts

486 symbols | 34 files | Cohesion: 80%

## When to Use

- Working with code in `scripts/`
- Understanding how githubApiHeaders, normalizeSourcePullRequest, pullRequestNumberFromText work
- Modifying scripts-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `scripts/visual-review-app.js` | githubTokenCreationUrl, itemSearchText, itemTitle, itemSubtitle, humanizeSnapshotName (+83) |
| `scripts/mc-tui.cjs` | clear, moveTo, bold, cyan, inverse (+47) |
| `scripts/mc-cli.cjs` | required, get, delete, wake, diagnostics (+41) |
| `scripts/publish-visual-pr-pages.mjs` | readJsonIfPresent, readGitHubEvent, repoParts, pageBaseUrl, githubServerUrl (+40) |
| `scripts/seed-spec-007.ts` | getE2EDbPath, placeholders, deleteWhereIn, selectIdsWhereIn, mergeFeatureFlags (+26) |
| `scripts/seed-e2e-spec-007.cjs` | entries, insertRow, slugify, createWorkspace, createProject (+16) |
| `scripts/visual-review-producer.mjs` | githubApiHeaders, normalizeSourcePullRequest, pullRequestNumberFromText, titleFromCommitMessage, sourcePullRequestFromEvent (+14) |
| `scripts/seed-e2e-spec-008.cjs` | entries, columnsFor, insertRow, mergeFeatureFlags, createWorkspace (+14) |
| `scripts/verify-visual-manifest.mjs` | pathExists, collectManifestFiles, readManifest, resolveScreenshotPath, verifyScreenshotHash (+12) |
| `scripts/visual-review-state.mjs` | parseReviewCommentBody, findReviewComment, renderReviewComment, validateVisualApproval, normalizeRequiredSurfaces (+10) |

## Entry Points

Start here when exploring this area:

- **`githubApiHeaders`** (Function) — `scripts/visual-review-producer.mjs:8`
- **`normalizeSourcePullRequest`** (Function) — `scripts/visual-review-producer.mjs:17`
- **`pullRequestNumberFromText`** (Function) — `scripts/visual-review-producer.mjs:37`
- **`titleFromCommitMessage`** (Function) — `scripts/visual-review-producer.mjs:53`
- **`sourcePullRequestFromEvent`** (Function) — `scripts/visual-review-producer.mjs:66`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `githubApiHeaders` | Function | `scripts/visual-review-producer.mjs` | 8 |
| `normalizeSourcePullRequest` | Function | `scripts/visual-review-producer.mjs` | 17 |
| `pullRequestNumberFromText` | Function | `scripts/visual-review-producer.mjs` | 37 |
| `titleFromCommitMessage` | Function | `scripts/visual-review-producer.mjs` | 53 |
| `sourcePullRequestFromEvent` | Function | `scripts/visual-review-producer.mjs` | 66 |
| `sourcePullRequestFromCommit` | Function | `scripts/visual-review-producer.mjs` | 96 |
| `commitHistoryShasFromGitHub` | Function | `scripts/visual-review-producer.mjs` | 127 |
| `initialReviewStateFromPullRequest` | Function | `scripts/visual-review-producer.mjs` | 155 |
| `reviewItemId` | Function | `scripts/visual-review-producer.mjs` | 196 |
| `reviewableReportItemIds` | Function | `scripts/visual-review-producer.mjs` | 201 |
| `reviewStateCoversReport` | Function | `scripts/visual-review-producer.mjs` | 209 |
| `coveredInitialReviewState` | Function | `scripts/visual-review-producer.mjs` | 225 |
| `resolveInitialReviewStateSource` | Function | `scripts/visual-review-producer.mjs` | 248 |
| `resetSpec007Fixtures` | Function | `scripts/seed-spec-007.ts` | 242 |
| `seedSpec007E2E` | Function | `scripts/seed-spec-007.ts` | 891 |
| `parseReviewCommentBody` | Function | `scripts/visual-review-state.mjs` | 188 |
| `findReviewComment` | Function | `scripts/visual-review-state.mjs` | 201 |
| `renderReviewComment` | Function | `scripts/visual-review-state.mjs` | 155 |
| `validateVisualApproval` | Function | `scripts/visual-review-state.mjs` | 208 |
| `normalizeRequiredSurfaces` | Function | `scripts/visual-review-state.mjs` | 260 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Tasks | 1 calls |

## How to Explore

1. `gitnexus_context({name: "githubApiHeaders"})` — see callers and callees
2. `gitnexus_query({query: "scripts"})` — find related execution flows
3. Read key files listed above for implementation details
