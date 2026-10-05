---
name: opensrc
description: Give coding agents the actual source code of any dependency. `opensrc path <pkg>` shallow-clones a package at the right version and caches it locally, printing a path you can grep/read — for npm, PyPI, crates.io, and GitHub/GitLab/Bitbucket repos. Use when you need to read a library's real implementation (not just docs) to understand internals, verify behavior, find an undocumented API, debug a dependency, or check what changed between versions. Compose with ripgrep/cat/find.
---

# opensrc — read any package's real source

## Overview

`opensrc` resolves a package to its git repo, **shallow-clones it at the matching version
tag**, and caches it under `~/.opensrc/`. `opensrc path <pkg>` prints the absolute path
(fetching on first use, instant cache hit after), so you compose it directly with your
normal search tools. It turns "I wish I could read how this library actually works" into a
one-liner — grounding answers in the **real implementation** instead of guessing or relying
on docs.

Use it when documentation is thin/stale, when you need to trace a bug into a dependency,
confirm a function's real signature/behavior, or diff two versions. For library *docs/API
reference* the context7 MCP is often faster; reach for opensrc when you need the **code
itself**.

## Install

```bash
npm install -g opensrc      # installs the native Rust binary (no Node overhead per run)
opensrc --version           # v0.7.2 at time of writing
```

## Core pattern: `path` + your tools

`opensrc path` emits a directory path; wrap it in `$(...)`:

```bash
rg "parse" $(opensrc path zod)                       # search a package's source
cat $(opensrc path zod)/src/types.ts                 # read one file
find $(opensrc path pypi:requests) -name "*.py"      # explore a PyPI package
ls $(opensrc path crates:serde)/src/                 # browse a crate
grep -r "Router" $(opensrc path vercel/next.js)/packages/next/src/   # a GitHub repo

rg "parse" $(opensrc path zod react next)            # several packages at once
```

This is the idiomatic agent workflow: **resolve a path, then ripgrep into it.** No manual
`git clone`, no version guessing, no polluting the working project.

## Registries & prefixes

| Registry  | Prefix                       | Example                          |
|-----------|------------------------------|----------------------------------|
| npm       | _(default)_ or `npm:`        | `opensrc path zod`               |
| PyPI      | `pypi:` / `pip:` / `python:` | `opensrc path pypi:requests`     |
| crates.io | `crates:` / `cargo:` / `rust:` | `opensrc path crates:serde`    |
| GitHub    | `owner/repo` or full URL     | `opensrc path vercel/next.js`    |
| GitLab    | `gitlab:` or URL             | `opensrc path gitlab:owner/repo` |
| Bitbucket | `bitbucket:` or URL          | `opensrc path bitbucket:owner/repo` |

## Pin a version

```bash
rg "ZodError" $(opensrc path zod@3.22.0)
cat $(opensrc path pypi:flask@3.0.0)/src/flask/app.py
```

Without `@version`, opensrc detects the version from your **lockfile (npm only)** or falls
back to the latest tag. Pass `--cwd <path>` to point lockfile resolution at a specific
project so the source you read matches what's actually installed.

## Other subcommands

```bash
opensrc fetch zod pypi:requests crates:serde vercel/next.js   # pre-warm cache, no path output
opensrc list                # what's cached (human-readable)
opensrc list --json         # machine-readable (parse this in scripts)
opensrc remove zod          # drop one package (alias: rm)
opensrc clean               # wipe cache  (--packages | --repos | --npm | --pypi | --crates)
```

Flags worth knowing: `--verbose` (progress during `path` fetch), `--quiet`/`-q` (silence
`fetch`), `--cwd` (lockfile-aware version resolution).

## When to use vs alternatives

- **vs reading docs / context7 MCP** — opensrc gives you the *code*; use it when behavior is
  undocumented, docs are wrong/stale, or you must see the actual implementation.
- **vs `git clone` by hand** — opensrc auto-resolves the registry → repo → correct version
  tag, shallow-clones, and caches globally so repeated lookups are free and don't clutter
  your project tree.
- **vs your installed `node_modules`/site-packages** — those may be built/minified or lack
  tests; opensrc fetches the real source repo at that version (with tests, comments, history
  context).
- **For your own project's code** use normal search; for *understanding a dependency* use
  opensrc.

## How it works / gotchas

- Cache lives at `~/.opensrc/repos/<host>/<owner>/<repo>/<version>/`; metadata in
  `~/.opensrc/sources.json`. Override the location with `OPENSRC_HOME`.
- **Shallow clone at a tag:** great for reading a release, but full git history isn't
  present — don't rely on `git log`/`git blame` inside the cache.
- **Version detection from lockfiles is npm-only.** For PyPI/crates, pin `@version`
  explicitly (or with `--cwd`) when you need an exact match to what's installed.
- **First fetch needs network** (and may be slow for large monorepos like `next.js`); cache
  hits are instant. Pre-warm with `opensrc fetch` if you're about to do many lookups.
- Resolution depends on the package advertising a source repo and using sane version tags;
  packages without a public repo or with nonstandard tags may not resolve.
- Requires `git` on PATH.

## Related

Pairs with [[gh-cli]] (authenticated GitHub access for private/raw files) and the dev
primitives [[pytest]]/[[docker]] when you're tracing behavior into a dependency.
Apache-2.0 · github.com/vercel-labs/opensrc
