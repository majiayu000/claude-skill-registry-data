---
name: ls-github-starredrepos
description: "Manage a GitHub starred repositories archive named starredrepos with authenticated context checks, dry-run synchronization, repo scouting, metadata snapshots, and guarded publish workflows."
metadata:
  version: "1.0"
compatibility:
  notes:
    - "Uses Node.js >=22 ESM helper scripts as a task-driven exception to the framework Python-first tooling default."
---

# GitHub Starred Repositories Archive

**Purpose:** Build and maintain a `starredrepos` archive of the authenticated user's GitHub starred repositories, with read-only discovery first, explicit mutation gates, schema-backed manifests, and optional repo scouting.

Use this skill when the user asks to inventory GitHub stars, sync starred repositories into a `starredrepos` repository, generate docs for starred projects, scout repository metadata, or automate a personal starred-repo archive.

## Operating Model

1. **Authenticate first:** Run `node scripts/verify-github-auth.mjs` before any GitHub API or repository work. Prefer the active `gh` login and record host, viewer, REST API versions, and rate-limit context.
2. **Read-only by default:** Start with `node scripts/list-starred-repos.mjs --limit 100 --json` and `node scripts/sync-starredrepos.mjs --dry-run`.
3. **Use the `starredrepos` contract:** Store publishable metadata, manifests, diffs, and generated docs in the archive repository. Keep local checkout caches, bare mirrors, and scout caches outside committed history.
4. **Use metadata storage:** Current helper apply mode is metadata-only. Submodule, checkout-cache, bare-mirror-cache, and vendor strategies are roadmap concepts until guarded implementations and tests exist.
5. **Scout conservatively:** Static metadata scouting is deterministic and default. Only run a configured model or command when `STARREDREPOS_SCOUT_MODE=command` or a matching CLI flag is explicit.
6. **Guard mutations:** Creating remotes, committing, pushing, deleting submodules, and vendoring content require separate explicit flags and should be previewed in a dry run first.

## Common Commands

```bash
node scripts/verify-github-auth.mjs --help
node scripts/verify-github-auth.mjs
node scripts/list-starred-repos.mjs --limit 100 --json
node scripts/sync-starredrepos.mjs --dry-run
node scripts/scout-repo-metadata.mjs --input data/examples/repo-metadata.example.json
node scripts/generate-starredrepos-docs.mjs --manifest data/examples/manifest.example.json --dry-run
node scripts/verify-starredrepos-state.mjs --examples
```

Run commands from this skill directory unless a script option names another path. Scripts are read-only unless the option name says otherwise, such as `--apply`, `--create-remote`, `--commit`, or `--push`.

## Environment

- `STARREDREPOS_GITHUB_HOST`: GitHub host, default `github.com`.
- `STARREDREPOS_REPO_NAME`: archive repository, default `starredrepos`.
- `STARREDREPOS_WORKTREE`: local archive worktree path.
- `STARREDREPOS_STORAGE_MODE`: `metadata` only. Other storage strategies are rejected by the helper until implemented.
- `STARREDREPOS_CACHE_DIR`: local cache directory for non-committed clones or mirrors.
- `STARREDREPOS_REST_API_VERSION`: REST version header, default `2026-03-10`.
- `STARREDREPOS_SCOUT_MODEL`: optional model label passed to external scout tooling.
- `STARREDREPOS_SCOUT_CONCURRENCY`: maximum concurrent scout jobs, default `2`.
- `STARREDREPOS_SCOUT_MAX_INPUT_TOKENS`: input budget hint for scout tools.
- `STARREDREPOS_SCOUT_TIMEOUT_MS`: command timeout, default `30000`.
- `STARREDREPOS_SCOUT_MODE`: `static` or `command`, default `static`.
- `STARREDREPOS_SCOUT_COMMAND`: external command invoked only in command scout mode.

## Mutation Guardrails

- `sync-starredrepos.mjs --dry-run` plans archive changes without writing files, creating remotes, committing, or pushing.
- `--apply` allows local archive file updates only.
- `--create-remote` may create `OWNER/starredrepos` only when combined with `--apply`; the helper initializes a new archive Git repository or verifies that the requested worktree is its root before remote creation.
- `--commit` may create a local commit only when combined with `--apply`; the helper initializes a new archive Git repository or verifies that the requested worktree is its root before committing.
- `--push` may push only when combined with `--apply --commit`.
- Do not delete, deinitialize, or rewrite existing submodules unless the user explicitly asks for that cleanup; this helper does not create submodules yet.
- Never print GitHub tokens, authorization headers, or full `gh auth token` output.

## Reference Map

- [Source ledger](references/source-ledger.md)
- [Architecture](references/architecture.md)
- [Authenticated GitHub context](references/authenticated-github-context.md)
- [Starred repo sync runbook](references/starred-repo-sync-runbook.md)
- [Starredrepos repository contract](references/starredrepos-repository-contract.md)
- [Storage strategies](references/storage-strategies.md)
- [Scout modes](references/scout-modes.md)
- [Release intelligence](references/release-intelligence.md)
- [Documentation archive](references/docs-archive.md)
- [API and CLI references](references/api-cli-references.md)
- [Node runtime](references/node-runtime.md)
- [Actions automation](references/actions-automation.md)
- [Security and privacy](references/security-privacy.md)
- [Rate limits and resilience](references/rate-limits-resilience.md)
- [Troubleshooting](references/troubleshooting.md)
- [Update procedure](references/update-procedure.md)

## Contracts

- [Manifest schema](data/schema/manifest.schema.json)
- [Snapshot diff schema](data/schema/snapshot-diff.schema.json)
- [Repo metadata schema](data/schema/repo-metadata.schema.json)
- [Scout report schema](data/schema/scout-report.schema.json)
- [Examples](data/examples/)
- [Templates](templates/)

The schemas are the public contract. The scripts use standard-library shape validation so no npm install is required.
