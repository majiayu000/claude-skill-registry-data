---
name: preferences
description: Use when aligning with Georgios’s default Git/GitHub conventions—cloning with gh, Conventional Commits, atomic staging, and guarded GitHub Actions for Rust/Python/TypeScript—so work matches his standard workflows.
---

# Preferences (Git & GitHub)

## Overview
Follow these defaults any time work touches git, GitHub, or CI to stay consistent with Georgios’s workflow and keep repos ready for automation.

## When to Use
- Cloning or checking out repos/PRs.
- Writing commits or preparing PRs.
- Adding or editing GitHub Actions (Rust, Python/uv, TypeScript, Vercel previews).
- Any task that might break established tooling if conventions drift.

## Core Preferences
- Use `gh` for auth, cloning, PRs, issues, and API calls (not raw curl).
- Standard clone path: `~/github/<owner>/<repo>`; ensure parent exists before cloning.
- Commit style must be Conventional Commits, one behavior per commit, staged atomically with `git add -p`.
- PR titles/bodies mirror main commit; keep history clean and reviewable.
- CI should be path-scoped: run only the stacks whose files changed; add a `changes` job with `dorny/paths-filter`.
- Language defaults: Rust uses rustfmt/clippy/nextest + sccache/mold; Python uses uv (ruff, mypy, pytest); TypeScript uses pnpm (format:check, lint, test) and caches Playwright when needed; Vercel previews gated on frontend paths.
- Use concurrency to cancel superseded PR runs; optional `alls-green` aggregator for a single required status.
- Avoid storing PATs; fetch tokens on demand via `gh auth token`.

## Git & GitHub Workflow
- Check auth first: `gh auth status`; log in if needed. Export tokens via `gh auth token` when tools expect `GITHUB_TOKEN`.
- Clone/checkout with `gh repo clone owner/repo ~/github/owner/repo` and `gh pr checkout <num>`.
- Prefer `gh pr create --fill` for new PRs; reviews via `gh pr review --approve|--request-changes -b "..."`
- For data/scripts, use `gh api ... --paginate` piped to `jq`; avoid unauthenticated curl to api.github.com.

## Commit Rules (Conventional Commits)
- Subject: `<type>[scope]: <imperative>` (e.g., `feat(auth): add magic link`), ≤72 chars, present/imperative.
- Types: feat, fix, refactor, chore, test, docs, perf, build, ci, revert.
- One behavior per commit: stage with `git add -p`; verify `git diff --cached` matches the subject.
- Body: what/why; footer for issues. No “update/misc” subjects.

## GitHub Actions Expectations
- Add a `changes` job with `dorny/paths-filter@v3`; gate downstream jobs with `needs: changes` + `if` outputs.
- Rust job: checkout, `dtolnay/rust-toolchain@stable` with fmt/clippy, `rui314/setup-mold`, `mozilla-actions/sccache-action`, `Swatinem/rust-cache`, `cargo fmt -- --check`, `cargo clippy -D warnings`, `taiki-e/install-action@nextest`, `cargo nextest run --no-fail-fast -j num-cpus`.
- Python job: checkout, `astral-sh/setup-uv@v3`, `uv venv && uv sync --frozen`, `uv run ruff check .`, `uv run mypy .`, `uv run pytest`.
- TypeScript job: checkout, `actions/setup-node@v4` (node 20, cache=pnpm), `pnpm/action-setup@v4 --run_install`, `pnpm lint`, `pnpm test -- --runInBand`, `pnpm format:check`, cache Playwright and install on cache miss.
- Vercel preview: only when frontend paths change; permissions `contents: read, deployments: write, id-token: write`; use project/org/token secrets.
- Add `concurrency` to cancel superseded runs; optional `re-actors/alls-green` to aggregate statuses.

## Quick Reference
- Clone: `dir=~/github/o/r; mkdir -p "$(dirname "$dir")"; gh repo clone o/r "$dir"`
- Checkout PR: `gh pr checkout <num>`
- Stage atomically: `git add -p`; verify: `git diff --cached`
- Commit: `fix(api): guard null author id`
- Paths-filter job: `uses: dorny/paths-filter@v3` → outputs gate jobs
- Rust CI trio: fmt + clippy + nextest; with sccache + mold
- Python CI: uv sync, ruff, mypy, pytest
- TS CI: pnpm format:check, lint, test; cache Playwright
- Vercel: gated on TS/frontend paths only

## Red Flags
- Using `git clone` or raw HTTPS without `gh` (breaks auth/layout).
- Commit mixes new feature + bugfix or has vague subject.
- CI runs every job on docs-only PRs (missing paths-filter).
- Python job uses `pip install` instead of `uv sync --frozen`.
- Vercel preview runs on every PR regardless of frontend changes.
