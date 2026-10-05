---
name: mise-setup
description:
  Set up or extend a project's mise.toml by inventorying the tools the project
  already uses and pinning each one to a backend and a version. Use when the
  user wants to adopt mise, add tools to an existing mise.toml, or migrate off
  `asdf`, `nvm`, `pyenv`, or `tfenv`.
version: 0.1.0
---

# mise Setup

[mise](https://mise.jdx.dev/) declares a project's whole toolchain in one
committed `mise.toml`, so a laptop, a container, and CI run the same versions.
Writing the TOML takes minutes. Taking **inventory** is what takes time: the
toolchain already exists, spread across CI workflows, Dockerfiles, task
runners, READMEs, and one version file per language.

<!-- vale ai-tells.FigurativeOwns = NO -->
<!-- The second bullet defines "owns" as a term for the version this file is
     the source for, so the verb is the terminology, not a metaphor. -->

- A **backend** is the source mise downloads a tool from. The registry maps a
  bare name like `yq` to a backend for you, and that mapping changes between
  mise releases. Write the backend-qualified name so the tool cannot move under
  the project.
- A version in `mise.toml` either **owns** its constraint or **mirrors** one
  that lives in another file. A mirror drifts unless the comment beside it names
  its upstream.

<!-- vale ai-tells.FigurativeOwns = YES -->

Verify claims against the installed mise, not from memory:
`mise settings --all`, `mise registry <tool>`, `mise tool <tool>`, and
`<command> --help`. Settings and backends change monthly.

## Procedure

### 1. Inventory the toolchain

List the files that name a tool or a version:

```bash
git ls-files | grep -Ei '(^|/)(\.tool-versions|\.?mise\.toml|mise/config\.toml|\.nvmrc|\.node-version|\.python-version|\.ruby-version|\.terraform-version|\.java-version|\.sdkmanrc|\.go-version|package\.json|pyproject\.toml|go\.mod|Cargo\.toml|Gemfile|Brewfile|Dockerfile[^/]*|Containerfile|[Mm]akefile|[Mm]agefile\.go|justfile|Taskfile\.ya?ml|\.pre-commit-config\.yaml|lefthook\.ya?ml|devcontainer\.json|flake\.nix|shell\.nix)$|(^|/)(Formula|HomebrewFormula)/.*\.rb$|\.github/workflows/|\.gitlab-ci'
```

Then read the workflows and the task runner, which name tools no version file
does:

```bash
grep -rhoE 'uses: [^ ]*setup-[^@]+@[^ ]+|(brew install|apt-get install|go install|pipx install|npm i(nstall)? -g|cargo install|curl [^|]+\| (ba)?sh)[^\n]*' \
  .github .gitlab-ci.yml Makefile GNUmakefile justfile Taskfile.yml 2>/dev/null | sort -u
```

Give each tool a row. Record the tool, what needs it, and the file that already
states a version. Consumers include build commands and CI jobs. Also include
runtime dependencies of the distributed binary.
[discovery.md](references/discovery.md) maps each marker to the tools it implies
and to where its version is already declared.

Inventory tools that CI installs but the README omits. Include runtime
dependencies that the project invokes through the shell.

Done when every tool a contributor needs to run the project's own commands has a
row. Each row names its consumer and version source or states `none`. Include
tools only CI installs today.

### 2. Pick a backend for each tool

Ask mise for the candidates, best first:

```bash
mise registry yq          # aqua:mikefarah/yq asdf:sudermanjr/asdf-yq go:github.com/mikefarah/yq/v4
mise tool aqua:mikefarah/yq   # Backend, Security, Tool Options, Config Source
```

Take the leftmost backend that fits, and read the `Security` line from
`mise tool` to see what verification the choice buys. Preference order, with the
reason:

| Prefix                                   | Use for                                                                                          | Verification                                                                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `core:`                                  | Language runtimes mise builds in (`node`, `python`, `go`, `java`, `ruby`, `deno`, `bun`, `rust`) | Checksums, plus GPG for Node.js and Swift                                                                         |
| `aqua:`                                  | Any CLI published as a release binary - the default choice                                       | Checksums, and Cosign/Minisign signatures, SLSA provenance, and GitHub attestations where upstream publishes them |
| `github:`, `gitlab:`, `http:`            | Release assets no aqua package covers                                                            | Checksums when upstream publishes them                                                                            |
| `npm:`, `pipx:`, `cargo:`, `go:`, `gem:` | Tools without a standalone binary                                                                | Whatever that ecosystem gives; resolution pulls transitive dependencies                                           |
| `asdf:`, `vfox:`                         | The last resort                                                                                  | A plugin is a shell or Lua script mise runs on your machine                                                       |

[backends.md](references/backends.md) covers the full prefix list, forcing a
backend for a bare name, and testing an unfamiliar package with
`mise test-tool`.

Done when every inventory row holds a backend-qualified name or a recorded
reason mise will not manage it. Reasons include requiring root or getting the
tool from the OS. Record when no backend is available.

### 3. Decide owner or mirror for each version

Sort every version into one of two kinds:

- **Owner** - `mise.toml` is the only place the version appears. Pin an exact
  version.
- **Mirror** - the constraint is already declared in `go.mod`'s `go` directive,
  `engines.node`, `requires-python`, `.terraform-version`, a Homebrew formula,
  or a Dockerfile base image. mise repeats it, so the comment beside it names
  that file.

```toml
[tools]
# Keep in sync with the `go` directive in go.mod.
go = "1.25.3"
```

Resolve a conflict at the upstream, not in `mise.toml`: a mirror that disagrees
with its upstream means one of the two is wrong, and silently picking one hides
which.

Done when every version has an owner-or-mirror verdict, every mirror's comment
names the file it tracks, and no mirror contradicts its upstream.

### 4. Write mise.toml

Add tools with `mise use --pin aqua:mikefarah/yq@4.53.3` so mise resolves and
installs as it writes, then edit the file to group the tools and add the
comments from step 3. Group by the reason the tool exists - the build, the docs
pipeline, the distributed binary's runtime dependencies - because the grouping
is what tells the next reader whether a tool is still needed.

Consult [config.md](references/config.md) for the `[settings]` worth committing,
the accepted version syntax, tool options, and `[env]`. Set at least these
four:

```toml
[settings]
# Record exact versions and checksums in mise.lock.
lockfile = true

# Hold back releases published in the last 7 days.
minimum_release_age = "7d"

# Install Python tools with uv instead of pipx.
pipx.uvx = true

[tool_config]
# Require the tools declared here to install from mise.lock. Unlike
# `settings.locked`, this leaves tools from a contributor's global config alone.
locked = true
```

Match `minimum_release_age` to the cooldown the project's package managers
already use, and reach for the `dependency-cooldown` skill to set the duration
everywhere else it resolves.

Run `mise fmt` to normalize the file.

Keep personal preferences out: `mise.toml` is committed, `mise.local.toml` is
git-ignored.

Done when `mise.toml` covers the managed rows from step 1, `mise fmt` leaves it
unchanged, and each tool sits in a group.

### 5. Lock the resolution

`lockfile = true` alone records the platform you ran on. Resolve for every
platform the team and CI use, then commit `mise.lock`:

```bash
mise install
mise lock --platform macos-arm64,macos-x64,linux-x64,linux-arm64
```

With the lockfile committed, installs read pre-resolved URLs and checksums
instead of calling GitHub and the aqua registry. `[tool_config] locked = true`
makes plain `mise install` fail on a missing entry, locally and in CI, so no
`--locked` flag is needed. Prove the enforcement in both directions:

```bash
mise install                                   # succeeds from the lockfile
cp mise.lock /tmp/mise.lock.bak
# delete one tool's block from mise.lock, then:
mise install -f <tool>                         # expect: "<tool> is not in the lockfile"
mv /tmp/mise.lock.bak mise.lock
```

> [!WARNING]
> Verify with plain `mise install`, never `mise install --locked`. `--locked`,
> `MISE_LOCKED`, and `settings.locked` apply to every loaded config, so on a
> developer machine they fail for every tool in `~/.config/mise/config.toml`
> that the project never declared. CI passes only because runners have no
> global config. When `--locked` has to run locally, hide the global config:
> `MISE_IGNORED_CONFIG_PATHS=$HOME/.config/mise/config.toml mise install --locked`.
> Pointing `MISE_GLOBAL_CONFIG_FILE` at `/dev/null` errors, and an empty file
> does not stop the real global config from loading.

Done when `mise.lock` holds a checksum for each tool on each platform in use,
`mise install` succeeds, and the install of a tool removed from the lockfile
fails.

### 6. Verify the toolchain runs

Read the state back through mise instead of trusting the file:

```bash
mise doctor            # activation, shims, config problems
mise ls --current      # every requested tool, its version, and the config that set it
mise x -- go build ./...   # the real consumer, under mise
```

A tool that installs but never runs its consumer proves nothing. Run one command
per tool through `mise x`.

Done when `mise ls --current` shows a version for every tool in `mise.toml` and
each tool's consumer ran under `mise x`.

### 7. Report and offer optional cleanup

Report the managed tools with their backends, the platforms in the lockfile, and
what stayed outside mise.

The setup is finished at that point: `mise.toml` works with every discovery site
from step 1 still in place. Retiring those sites is a second change with
separate risks - a CI workflow that stops installing a tool the way the team
knows, or a version file another tool still reads. Offer a list for the user to
choose from, and change only their choices:

- Replace the `setup-*` steps in CI with `jdx/mise-action`, pinned to a release
  commit SHA. A `setup-node` left beside a `node` entry means two versions and
  one of them wins silently.
- Delete a per-language version file, or keep it as the owner and read it with
  `idiomatic_version_file_enable_tools`. mise reads `.tool-versions` with no
  setting.
- Point README install instructions at `mise install`.

[ci-and-migration.md](references/ci-and-migration.md) covers the CI wiring,
Docker, and migration from `asdf`, `nvm`, `pyenv`, `tfenv`, and Homebrew.

Done when the report names every managed tool, and each retirement the user
picked leaves its discovery site deleted or named as the upstream of a mirror.

## Tasks

Use `[tasks]` where a command is already written down elsewhere - a Makefile
target, a CI step, a README code block - because moving it there gives the
command one home and the tools it needs. Keep the name contributors already
type:

```toml
[tasks.build]
description = "Build the project"
run = "mage build"
```

mise runs a `run` script with `sh -c`, which is dash on Ubuntu runners and
bash on macOS. Write POSIX sh (no `<<<`, `[[ ]]`, arrays, or `pipefail`), or
set `shell = "bash -c"` on the task. Check with `sh -n` or `dash -c` before
pushing, because a bash-only construct passes on a Mac and exits 2 in CI.

A task that wraps nothing adds a layer to read through. Full reference:
<https://mise.jdx.dev/tasks/>
