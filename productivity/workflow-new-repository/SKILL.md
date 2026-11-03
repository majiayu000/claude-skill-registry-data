---
name: workflow-new-repository
description: Bootstrap a new bitwise-media-group repository for a given archetype (go, node, python, swift, terraform, or common-only Markdown/YAML) — git init on main, baseline files (README, MIT LICENSE, AGENTS.md with a CLAUDE.md symlink, .gitignore, release-please config), the shared mise toolchain submodule, the language scaffold, and the SHA-pinned reusable GitHub workflow callers — then verify the lint gate and hand off the commit and the GitHub-side setup. Asks for the archetype when the request does not name one. Use when creating, starting, bootstrapping, initialising, or scaffolding a new repository, repo, or project for the org, or setting up a fresh repo with the standard toolchain, CI, release, and merge automation. Not for adding the toolchain or workflows to an existing repo (the workflow-toolchain and actions-reusable-workflows skills), scaffolding a module or package inside an existing repo, or creating the GitHub remote without a local scaffold.
license: MIT
---

# Bootstrap a new repository

A new org repository is the same three layers every time: the shared **toolchain** (mise tasks, pinned tools, lint
policy), a **language scaffold** for its archetype, and the **reusable workflow callers** (CI, security, release,
merge, Renovate). This skill sequences them; the `workflow-toolchain` and `actions-reusable-workflows` skills own the
details of their layers, so apply them rather than restating them.

## 1. Settle the inputs before writing anything

- **Archetype** — exactly one of `go`, `node`, `python`, `swift`, `terraform`, or `common` (Markdown/YAML with nothing
  to build or test). If the request does not name one, **ask** — offer the six with a one-line description each. Never
  infer it from the repo name.
- **Name and directory** — the repo name (kebab-case) and where to create it; default to `./<name>`. If the directory
  exists and is non-empty, or is already a git repository, stop: that is an adoption, handled by `workflow-toolchain`
  and `actions-reusable-workflows` directly.
- **One-line description** — for the README and, later, the GitHub repo.
- **Releases** — whether the repo cuts versioned releases (default yes) and, for `go`/`swift`, whether it ships
  binaries via GoReleaser.

## 2. Initialise and write the baseline files

```sh
git init --quiet --initial-branch=main "<dir>" && cd "<dir>"
```

- **`README.md`** — the name, the description, and a short "Development" section (`mise trust --all`, `make help`,
  `make pr`).
- **`LICENSE`** — MIT, copyright `<year> BitWise Media Group Ltd` (the toolchain's default license holder).
- **`AGENTS.md`** + **`CLAUDE.md`** — repo conventions for agents in `AGENTS.md`, and `ln -s AGENTS.md CLAUDE.md` so
  Claude Code reads the same file.
- **`.gitignore`** — the archetype's outputs from the toolchain's adoption guide (`coverage/`, and `node_modules/`,
  `.venv/`, `site/`, `.build/`, `.swiftpm/`, `dist/` as applicable).
- **Release config** (skip if the repo will not release) — `.release-please-manifest.json` as `{".": "0.0.0"}` and:

  ```json
  {
    "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
    "always-update": true,
    "include-component-in-tag": false,
    "packages": { ".": { "release-type": "<release-type>" } }
  }
  ```

  `release-type` is `go`, `node`, `python`, or `terraform-module` for those archetypes, and `simple` for `swift` and
  `common`.

SPDX license headers are not hand-written: `make fmt` stamps them once the toolchain is in place.

## 3. Add the toolchain

Apply the `workflow-toolchain` skill for the chosen archetype: submodule at `.mise/` pinned to the latest tag, root
`mise.toml` (runtime pin, `common` + the archetype, knobs), and the one-line `Makefile`.

## 4. Scaffold the language layer

| Archetype   | Scaffold                                                                                                         |
| ----------- | ---------------------------------------------------------------------------------------------------------------- |
| `go`        | `go mod init`, then the `go-project` skill's tree (`cmd/`, `internal/`, thin `main`); `go-release` for binaries. |
| `node`      | `package.json` on the archetype's script contract (`typecheck` and `build` required).                            |
| `python`    | the `python-project` skill (`uv init`, `src/` layout, dev dependency group).                                     |
| `swift`     | `swift package init`, with `swift_product` set when only one product ships.                                      |
| `terraform` | the `terraform-module` skill's five files.                                                                       |
| `common`    | nothing beyond the baseline.                                                                                     |

The toolchain owns the build surface, so **skip the language skills' own Makefile, tools-module, and CI/release-workflow
steps** — `go-project`'s `tools/go.mod` and Makefile `pr` gate, `python-project`'s Makefile, and `go-release` /
`python-release`'s hand-written workflows are all replaced by the toolchain and the reusable callers. Keep their source
layout, `.goreleaser.yaml`, and version-package guidance; point the go archetype's `version_pkg` knob at that package.
Read `docs/archetypes/<archetype>.md` in the toolchain clone for the archetype's knobs and contract.

## 5. Wire the workflow callers

Apply the `actions-reusable-workflows` skill: copy `ci`, `security`, `release` (if releasing), `merge`,
`merge-review-ack`, `merge-notice`, and `renovate` from the library's examples at its latest release, pin them to its
commit SHA, and set `merge.yaml`'s `workflow_run.workflows` to the CI caller's real `name:` plus `"Merge Review Ack"`.
Skip `add-to-project` — the org settings sync adds it. A `common` repo still gets `security` (it scans `actions`).

## 6. Verify locally

```sh
mise trust --all
make fmt    # stamps SPDX headers and formats prose
make lint   # license, prose, workflows (actionlint + zizmor), and the archetype's linters
make test   # and make build, where the archetype defines them
```

Fix every finding before handing off; the `actions-validate` skill covers workflow lint failures.

## 7. Hand off the commit and the GitHub side

Commit with the `workflow-commit` skill — in a fresh main checkout that means a `commit.sh` for the user to run, with an
initial `chore: bootstrap <archetype> repository` commit (or a few commits split by layer).

Everything below changes shared org state, so **list it for the user and do none of it without their explicit go-ahead
for that step**:

1. Create the remote and push — `gh repo create bitwise-media-group/<name> --private --source . --push` (or
   `--public`), after `commit.sh` has run.
2. Apply the org's repository template — rulesets (with the FF Merge bypass), labels, and merge settings — with
   `./repo-config.sh import <name>` from
   [`github-settings`](https://github.com/bitwise-media-group/github-settings).
3. Confirm the FF Merge, Renovate, and Project Sync GitHub Apps cover the repo. They are normally installed on all
   repositories; a selected-repositories install needs the new repo added.
4. With a `zensical.toml`, set **Settings → Pages → Source** to **GitHub Actions**.
