---
name: workflow-toolchain
description: Set up, adopt, or update the bitwise-media-group/toolchain shared mise task library in a repository — mount it as a git submodule at .mise/ pinned to the latest release tag, write the root mise.toml (runtime pins, the common tasks plus exactly one archetype, [vars] knobs), reduce the Makefile to a single include, and trust the config. Use when adding the shared toolchain or mise tasks to a repo, choosing a toolchain archetype (go, node, python, swift, terraform, or common-only), migrating a repo from the v2 tasks/<archetype>.toml + mise.mk layout, bumping or repairing the .mise submodule, or asked how make lint / build / test / pr are wired. Not for writing GitHub Actions caller workflows (the actions-reusable-workflows skill), scaffolding a whole new repository (workflow-new-repository), or changing the toolchain library itself.
license: MIT
---

# Set up the bitwise toolchain

[`bitwise-media-group/toolchain`](https://github.com/bitwise-media-group/toolchain) is the org's shared build layer:
pinned developer tools, one mise task **archetype** per primary language, and the house lint/license policy. A repo
consumes it as a git submodule mounted at `.mise/`, pins its own language runtime in a root `mise.toml`, and keeps a
one-line `Makefile`. The reusable CI workflows run those mise tasks, so this is also the CI contract — wire the callers
with the `actions-reusable-workflows` skill.

This skill is the procedure. The library's own docs **at the release you pin** are the source of truth for archetype
details, knobs, and runtime versions — they move faster than this skill, so read them instead of recalling them.

## 1. Resolve the latest release and read its docs

```sh
url=https://github.com/bitwise-media-group/toolchain.git
tag=$(git ls-remote --tags --refs --sort=-v:refname "$url" 'v*.*.*' | head -n1 | sed 's|.*refs/tags/||')
src=$(mktemp -d "${TMPDIR:-/tmp}/toolchain.XXXXXX")
git clone --quiet --depth 1 --branch "$tag" "$url" "$src"
```

Read from `$src`, in this order: `docs/getting-started/adopt.md` (the three files and housekeeping),
`docs/archetypes/index.md` (which archetype), `docs/archetypes/<archetype>.md` (its knobs), and `README.md`. A repo on
the old layout also reads `docs/reference/migrating.md`. The same pages are published at
<https://oss.bitwisemedia.uk/toolchain/>, but that site tracks the newest release — the clone matches the tag you pin.

## 2. Pick exactly one archetype

| The repo is…                                   | Archetype   |
| ---------------------------------------------- | ----------- |
| a Go CLI or service                            | `go`        |
| a TypeScript library or GitHub Action          | `node`      |
| a Python package, or a Zensical docs-only site | `python`    |
| a SwiftPM package or CLI                       | `swift`     |
| a Terraform/OpenTofu module or environment     | `terraform` |
| Markdown/YAML with nothing to build or test    | common only |

Archetypes **do not stack**: mise merges included task files whole-task and the later include wins, so a second
archetype silently replaces the first's `fmt`/`lint`/`build`/`test`/`ci`/`pr`. A second language becomes repo-local
tasks inside the primary archetype. If the language is ambiguous, ask.

## 3. Mount the submodule at the tag

```sh
git submodule add --name toolchain "$url" .mise
git -C .mise -c advice.detachedHead=false checkout --quiet "$tag"
git config -f .gitmodules submodule.toolchain.branch "$tag"
git add .gitmodules .mise
```

The mount point is load-bearing: mise reads `.mise/config.toml` as its own config (shared `[settings]`, `[tools]`,
`[vars]`), and every task path assumes `.mise/`. Recording the tag as the submodule `branch` is what lets Renovate's
`git-submodules` manager propose each newer tag. `git submodule add -b <tag>` does **not** work — it only accepts
branches.

## 4. Write the root `mise.toml`

Take the archetype's block from `adopt.md` at the pinned tag. Its shape:

```toml
[tools]
# the repo's language runtime — the library never pins it. go also pins
# "go:golang.org/x/vuln/cmd/govulncheck"; python and terraform pin nothing.
go = "<version from adopt.md, or the latest stable>"

[vars]
# structural knobs from docs/archetypes/<archetype>.md, e.g. app / app_pkg for go

[task_config]
includes = [".mise/common/tasks.toml", ".mise/archetypes/go/tasks.toml"] # common first, then one archetype
```

A common-only repo includes just `.mise/common/tasks.toml`. Repo-local tasks go in `[tasks]`; to **redefine** an
archetype task, put it in a repo `tasks.toml` appended after the archetype in `includes`.

## 5. Reduce the `Makefile` to one include

```makefile
include .mise/archetypes/<archetype>/include.mk
```

(`include .mise/common/include.mk` for common only.) Every `make <target>` forwards to `mise run <target>`; make-side
prerequisites (`pr: docs`) go beneath the include. CI never calls make.

## 6. Housekeeping

- **`.gitignore`** — the outputs `adopt.md` lists for the archetype (`coverage/`, plus `node_modules/`, `.venv/`,
  `site/`, `.build/`, `.swiftpm/`, `dist/` as applicable).
- **`.licenseignore`** — only generated files the defaults don't already skip (a node action lists `dist/**`).
- **No prose or workflow-lint config** — prettier, markdownlint, actionlint and zizmor read the house defaults from
  `.mise/`. Commit your own `.prettierrc.yaml` etc. only to override one wholesale.
- **Remove what the toolchain replaces** — `tools/go.mod` tool modules, linter `devDependencies`, `.bin/`, hand-written
  Makefile targets, and no-op task stubs (CI skips tasks a repo doesn't define).

## 7. Verify

```sh
mise trust --all   # once per clone; CI trusts the workspace itself
mise tasks         # or: make help
make lint          # then build / test where the archetype defines them
```

## Updating and the never-re-lock rule

Renovate bumps `.mise` to each new tag. By hand: `git -C .mise fetch --tags`, check out the new tag, update
`submodule.toolchain.branch` in `.gitmodules`, and stage both. Shared tool pins live **inside** the library, so
**never run `mise lock` or `mise upgrade` in a consumer** — it writes into the submodule. Lock only the repo's own pins
(`mise lock <tool>`), and change shared pins upstream in the toolchain repo.
