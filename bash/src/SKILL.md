---
name: src
description: Reads a library's or repository's real source and docs at an exact version, tag, branch, or commit, fetched with the `ask` CLI, which finds a dependency's installed version in the project lockfile itself. Use when a question is settled by upstream code rather than recall, or when the user pastes a repository URL.
allowed-tools: Bash(ask:*)
---

# Read upstream source

Fetch the code the question depends on, at the ref it depends on, then read it
with `rg`, `sed`, and `fd`. Finish by naming the spec and ref you read.

## 1. Write the spec

- **Repository:** `github:owner/repo`, adding `@ref` when the version matters.
- **Package:** `npm:name`, `pypi:name`, `pub:name`, or `maven:group:artifact`,
  with `@version` to pin it. A bare name is npm, versioned from the project
  lockfile. A bare `owner/repo` is read as an npm name too:
  `ask src stablyai/orca` fails with `npm registry returned 404`, and
  `ask src github:stablyai/orca` works.
- **URL:** `https://github.com/<o>/<r>` becomes `github:<o>/<r>`. In
  `…/tree/<rest>` or `…/blob/<rest>`, the ref is the longest leading part of
  `<rest>` that names a commit, since branch names can contain slashes. Try
  candidates longest first; the first that prints a SHA is the ref:

  ```bash
  gh api 'repos/<o>/<r>/commits/<candidate>' --jq .sha
  ```

- **Ref:** a tag for questions about a version, matching the project's
  installed version when it has one. Trunk otherwise. Omitting the ref reads
  trunk when it is `main` or `master`; for any other default branch, pass the
  name from `gh api repos/<o>/<r> --jq .default_branch`.

A commit SHA, or a repository off GitHub, goes to [Without ask](#without-ask).

## 2. Fetch

Read trunk or any branch through the freshness helper. It prints the checkout
path and refetches when the cached copy is over a day old and upstream has
moved. Tags and packages never change, so they go to `ask src` directly.

```bash
src=$(~/.agents/plugins/plugins/utils-agent/skills/src/scripts/fresh github:owner/repo) || exit 1
src=$(ask src github:owner/repo@v1.2.3) || exit 1
[ -n "$src" ] || { echo "no checkout path" >&2; exit 1; }
```

Keep stderr visible: it carries the reason a fetch failed. The step is done
when you hold a non-empty path at the ref you meant to read.

`ask docs <spec>` prints the same checkout's documentation directories, one
per line. `ask <command> --help` covers everything else.

## Without ask

`ask` reads GitHub over git only. On the work laptop, TLS interception also
breaks its tarball fallback, SHA refs, and `maven:` and `pub:` lookups; the
signal is `invalid peer certificate: UnknownIssuer` in stderr. Go straight to
these recipes:

```bash
# A few files at any ref, SHA included
gh api -H 'Accept: application/vnd.github.raw+json' \
  'repos/<o>/<r>/contents/<path>?ref=<ref>'

# A whole tree at a branch or tag, from any git forge
dir=$(mktemp -d)
git clone --depth 1 --branch <ref> <url> "$dir"

# A whole tree at a commit SHA
dir=$(mktemp -d)
git -C "$dir" init -q && git -C "$dir" remote add origin <url> &&
  git -C "$dir" fetch -q --depth 1 origin <sha> &&
  git -C "$dir" checkout -q FETCH_HEAD
```

Use the SSH URL (`git@github.com:<o>/<r>.git`) on the work laptop. Mercurial
repositories use `hg clone -r <ref> <url> "$dir"`.
