---
name: laravel-herd-worktrees
description: Create, list, or remove git worktrees for Laravel projects served by Laravel Herd on macOS. Use when the user needs a branch worktree, .test URL, or per-worktree PHP/composer isolation.
compatibility: "macOS with Laravel Herd installed"
---

# Laravel Herd + Git Worktrees

Run multiple branches of a Laravel project in parallel, each reachable at its own `*.test` URL through Laravel Herd, with isolated dependencies, env, database, and caches.

## Mental Model

- A **worktree** is a sibling directory of the main checkout with its own `HEAD`. Composer/Node deps, `vendor/`, `node_modules/`, `storage/`, and `bootstrap/cache/` are **per-worktree**: never share via symlink.
- Herd's **parked directory** auto-serves every immediate subdirectory as `<dir>.test`. Park the *parent* of all worktrees once and every new worktree gets a URL for free.
- `.env` is **untracked**, so it must be re-created in each worktree. `APP_URL`, `DB_DATABASE`, cache prefixes must differ per worktree to prevent cross-branch bleed.

## When to Use This Skill

- User asks to create a worktree for a Laravel app served by Herd.
- User reports `vendor/`, migrations, cache, or `.env` problems after switching worktrees.
- User wants per-branch URL like `myapp-feat.test` without manual Nginx/Valet config.
- User wants the same Laravel project on multiple PHP versions simultaneously.

## Workflow

### 1. One-time setup

Park the **parent** directory that holds the main checkout (worktrees become siblings of the main checkout, so they land in the same parked dir):

```bash
cd ~/Code           # parent of your laravel project
herd park
```

Verify:

```bash
herd parked
```

Each immediate subdir is now `<name>.test`. Adding a worktree at `~/Code/myapp-feat` makes `myapp-feat.test` resolve immediately.

If parking the parent is not desired (other non-Laravel dirs live there), use explicit `herd link` per worktree instead: see [references/herd-commands.md](./references/herd-commands.md).

### 2. Create a new worktree

Use the helper script. It creates the worktree, copies `.env`, rewrites `APP_URL` + `DB_DATABASE` + cache prefixes, installs deps, generates app key, and runs migrations (when Composer hooks require assets built before `composer install`, follow step 1 of [Bootstrap a bare worktree](#bootstrap-a-bare-worktree)):

```bash
bash scripts/worktree-new.sh <branch-suffix> <base-branch> [--driver sqlite|mysql|pgsql]
```

Example:

```bash
bash scripts/worktree-new.sh feat-billing main --driver sqlite
```

Result: `../myapp-feat-billing/` exists, `myapp-feat-billing.test` works, isolated DB.

See [scripts/worktree-new.sh](./scripts/worktree-new.sh) for the exact transformations applied to `.env`.

### 3. Remove a worktree

```bash
bash scripts/worktree-rm.sh <branch-suffix> [--drop-db]
```

Runs `git worktree remove`, optionally drops the per-worktree DB, and `herd unlink`s if a manual link exists.

### 4. Switch PHP version per worktree (optional)

```bash
cd ../myapp-legacy
herd isolate php@8.1
```

Site uses 8.1; sibling worktrees keep their isolated or default version. `herd isolated` lists all overrides. `herd unisolate` reverts.

## Bootstrap a bare worktree

A worktree made with plain `git worktree add` (the PR, issue, and CI recipes in other skills, at `.claude/worktrees/<name>`) has no `vendor/`, `node_modules/`, or `.env`; nor does one the harness made (`claude --worktree`, a subagent with `isolation: worktree`). With the leek-skills plugin in Claude Code, a session that opens in such a worktree is told so at start; elsewhere, check for `vendor/` yourself before running anything. Make it runnable from inside the worktree, with `main` set to the main checkout (`git worktree list --porcelain | sed -n '1s/^worktree //p'`):

1. **Dependencies and assets.** `cp -Rc "$main/vendor" vendor` (an APFS clone: instant, no extra disk), then `composer install` so it matches this branch's lock. Do the same for `node_modules` when the run builds assets. When Composer hooks require generated assets that do not exist yet (such as `@php artisan filament:assets` needing an editor bundle from `npm run build`), run `composer install --no-scripts`, build the assets, then run `composer install`. Each tree owns a real copy: Composer's autoloader resolves `app/` and `tests/` relative to `vendor/`, so a symlinked `vendor/` makes Pest run the main checkout's code.
2. **Environment.** Copy `.env` (and `.env.testing` when present) from `$main`. When the calling skill gives the run its own database, set `DB_DATABASE` to that name in both. When the worktree lives under `.claude/worktrees/<name>` (not an immediate subdirectory of Herd's parked parent) and the run needs a `.test` URL for HTTP verification, run `herd link <name>` (and `herd secure <name>` when `APP_URL` uses `https://`), then `herd unlink <name>` from inside the worktree before removing it (each skill's worktree removal step says so).
3. **Proof.** `git rev-parse HEAD` equals the commit the run means to test, and `test ! -L vendor` passes. Run nothing until both hold.

## Per-Worktree Isolation Rules

| Concern | Rule |
|---|---|
| `vendor/` | Always per-worktree. Never symlink. |
| `node_modules/` | Always per-worktree. Never symlink. Use `pnpm` for fastest installs (content-addressable store). |
| `.env` | Copy from main, rewrite `APP_URL`, `DB_DATABASE`, `CACHE_PREFIX`, `SESSION_COOKIE`, `REDIS_PREFIX`. |
| `APP_KEY` | Run `php artisan key:generate` in each worktree. |
| Database | SQLite: per-worktree file. MySQL/Postgres: per-worktree DB name `<app>_<suffix>`. |
| Redis | Set unique `REDIS_PREFIX` (or different `REDIS_DB` index). |
| `storage/`, `bootstrap/cache/` | Per-worktree. Run `php artisan optimize:clear` after install. |
| `storage/app/public` symlink | Re-run `php artisan storage:link` in the new worktree. |

Full rationale: [references/isolation.md](./references/isolation.md).
DB strategy details (sharing seeds, schema dumps, fresh vs. migrate): [references/db-strategies.md](./references/db-strategies.md).

## Common Pitfalls

- **Sharing `vendor/` via symlink**: breaks when branches have different package versions; autoload class maps drift.
- **Forgetting `php artisan key:generate`**: encrypted cookies/sessions fail silently across worktrees that share `APP_KEY`.
- **Same `SESSION_COOKIE` across `*.test` siblings**: cookies leak between branches because they share the `.test` parent domain. Set a unique `SESSION_COOKIE` per worktree.
- **Same Redis DB without prefix**: cache keys collide; one branch invalidates another's cache.
- **Running `composer install` against a stale `composer.lock`** after rebasing: always re-run install after switching base branches inside a worktree.
- **Herd not picking up new worktree**: happens if the parent isn't parked or if the worktree directory name contains characters Herd rejects (stick to `[a-z0-9-]`).

## Quick Diagnostics

```bash
herd parked              # confirm parent is parked
herd isolated            # list per-site PHP overrides
herd which-php           # PHP version Herd resolves for current dir
git worktree list        # all worktrees + branches
ls -1 ../ | grep <app>   # worktree dirs as Herd sees them
```

If a `.test` URL 404s: check `herd parked` includes the parent, dir name is lowercase, and `php artisan route:list` works inside the worktree.

## Out of Scope

- **Valet**: different tool. Herd-only here.
- **Linux Herd**: paths and CLI differ; this skill assumes macOS Herd.
- **Docker / Sail**: covered by other workflows. Worktrees still work but routing is via Docker, not Herd.
