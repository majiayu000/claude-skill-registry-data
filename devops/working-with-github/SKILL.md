---
name: working-with-github
description: "Use when working with GitHub itself (not Git, not GitHub Actions) — the gh CLI, the REST API, the GraphQL API, tokens and authentication, pull requests, code review, issues, releases (including uploading assets/binaries and changelogs), branch protection and rulesets, GitHub flow, multi-branch release with environments, and Dependabot + CodeQL security configuration. Invoke for any gh command/flag lookup, REST-vs-GraphQL decision, rate-limit/efficiency question, or 'how do I do X on GitHub' that isn't a raw git operation or a CI workflow. The gh CLI reference is generated verbatim from a pinned gh binary; the guides are fetched from docs.github.com. For raw git, use working-with-git; for CI/workflow YAML (incl. the Dependabot/CodeQL Actions cookbooks), use working-with-github-actions; for building Apps/SDKs, use developing-for-github."
metadata:
  last_updated: "2026-08-23"
---

# Working with GitHub

Reference for using **GitHub the platform** — the `gh` CLI, the REST and GraphQL APIs, and the web/repo features (PRs, review, issues, releases, branch protection, security config). The CLI pages in [`references/cli/`](references/cli/) are generated verbatim from a **pinned `gh`** binary (see [`PINNED_VERSION`](PINNED_VERSION) and [`references/VERSIONS.md`](references/VERSIONS.md)); the topic guides in `references/` are fetched from the `github/docs` repo. Every fetched/generated file carries `source`/`fetched_at`/`sha256` frontmatter.

## Scope / where to go instead

| You need… | Skill |
|---|---|
| Raw git (commits, rebase, bisect, conflicts, history) | `working-with-git` |
| CI/CD workflow YAML, Actions, OIDC deploys, the Dependabot/CodeQL **Actions cookbooks** | `working-with-github-actions` |
| Build a GitHub App / OAuth app / webhook consumer / Octokit bot | `developing-for-github` |
| Pick which downstream skill/command to run for a task | `git-github-workflows` (router) |
| **Everything else GitHub** (this skill) | continue below |

## Quick reference

| Task | Read |
|---|---|
| Exact `gh` command/flag | `references/cli/gh__<command>.md` (e.g. `gh__pr__create.md`); start at `references/cli/gh.md` |
| REST vs GraphQL — which to use | `references/howto/rest-vs-graphql.md`, `references/rest-graphql-comparison.md` |
| Don't burn your rate limit | `references/howto/api-efficiency.md`, `references/rest-rate-limits.md`, `references/graphql-rate-limits.md` |
| REST basics / auth / pagination | `references/rest-getting-started.md`, `references/rest-authentication.md`, `references/rest-pagination.md` |
| GraphQL basics / forming calls | `references/graphql-intro.md`, `references/graphql-forming-calls.md` |
| Tokens (classic vs fine-grained PAT) | `references/tokens-personal-access.md`, `references/rest-credentials-secure.md` |
| Open / review / merge a PR (human/UI) | `references/pr-*.md`, `references/review-*.md` |
| **Review a PR programmatically** (post reviews, inline comments, suggestions, check annotations, statuses) | `references/howto/code-review-via-api.md`; API ref: `references/api-pr-reviews.md`, `api-pr-review-comments.md`, `api-checks-runs.md`, `api-commit-statuses.md` |
| **Agent runbook: drive a PR branch → PR → review loop → all-approved** | `references/howto/driving-a-pr-to-approval.md` |
| **Rate a first-party AI reviewer's findings** (👍/👎/😕, why 😕 needs a reply) | `references/howto/giving-feedback-on-ai-reviews.md` |
| **Read that feedback and act on it** (trends, thresholds, fix surfaces) | `references/howto/tuning-the-ai-reviewer.md` |
| Resolve review threads / read `reviewDecision` (GraphQL-only) | `references/howto/code-review-via-api.md`, `references/graphql-forming-calls.md` |
| Cut a release + upload assets/changelog | `references/howto/releases-and-assets.md`, `references/releases-*.md` |
| Drive a PR → review → merge → release | `references/howto/pr-to-release.md` |
| Multi-branch release with environments | `references/howto/multi-branch-release.md` |
| Branch protection / rulesets / merge methods | `references/protected-branches.md`, `references/rulesets-*.md`, `references/merge-methods.md` |
| Issues (create, link, sub-issues, assign) | `references/issues-*.md` |
| Dependabot config (`.github/dependabot.yml`) | `references/dependabot-*.md` |
| CodeQL / code scanning setup | `references/code-scanning-*.md`, `references/codeql-*.md` |

## How to use this skill

1. **Exact CLI usage** — read `references/cli/gh.md` for the command tree, then the specific `gh__<command>__<subcommand>.md` page. These are the literal `gh <cmd> --help` output at the pinned version; trust the live binary if it disagrees and surface the drift.
2. **A "how do I" question** — start with the matching `references/howto/*.md` (hand-written, opinionated), then drill into the fetched `references/*.md` for the official detail.
3. **Uncertain topic** — `grep -ri <term> references/` to locate the right page.

## Behavioral guidance

- **Be rate-limit aware.** Authenticated REST is 5,000 req/hr (15,000 for GitHub Apps on an org); GraphQL is a separate point-budget. Prefer one GraphQL query over N REST calls when fetching nested data; use conditional requests (ETags) for polling. See `references/howto/api-efficiency.md`.
- **Prefer `gh` for one-offs**, the API for automation. `gh api` is the escape hatch for any REST/GraphQL endpoint with auth handled for you.
- **Dependabot/CodeQL split:** this skill owns the repo-settings/security-config side (`.github/dependabot.yml`, version updates, alerts, code-scanning setup). The advanced *workflow YAML* lives in `working-with-github-actions`.

## Keeping this current

Regenerated by [`scripts/update_docs.js`](scripts/update_docs.js): generates the `gh` CLI reference from the local pinned binary and fetches the curated docs.github.com guides. Refresh locally with `make update-working-with-github`. Bump the CLI pin via `brew upgrade gh`, update [`PINNED_VERSION`](PINNED_VERSION), then rerun. The weekly CI workflow auto-discovers the script, refreshes the fetched guides, and skips CLI generation when `gh` is absent or mismatched (no churn).
