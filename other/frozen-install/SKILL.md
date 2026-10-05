---
name: frozen-install
description:
  "Replace resolving install commands with frozen ones - `npm ci`, `uv sync
  --locked` - at every site meant to reproduce a lockfile: CI workflows, image
  builds, task runners, deploy scripts, and docs. Use when the user wants
  reproducible installs, or mentions `npm install` in CI, `npm ci`,
  clean-install, `--frozen-lockfile`, or lockfile drift. Covers `npm` and `uv`."
version: 0.1.0
---

# Frozen Install

An install command either **resolves** - reads the ranges in the manifest, picks
versions, and writes the lockfile - or is **frozen**: it installs the lockfile
exactly and fails when it cannot. `npm install` resolves even with a lockfile
sitting beside it. `npm ci` is frozen.

Sort every install site by intent. A site that reproduces an environment - CI,
an image build, a deploy, a contributor's first setup - belongs on the frozen
side. Anything that moves the lockfile forward is a **resolving site**, run
deliberately by a person who wants exactly that.

A complete fix pairs a frozen command with a committed lockfile. Either half
alone gives a broken build or silent drift.

**Loud is the point.** A frozen install that fails because the lockfile
disagrees with the manifest has done its job. Regenerate the lockfile and commit
it. Unfreezing the command deletes the only check that the two ever agree.

Read the flags off the installed tool, not from memory: `npm help ci`,
`uv sync --help`.

## Procedure

### 1. Inventory the install sites

```bash
git grep -nE '\b(npm (i|install|add|ci|clean-install|update)|uv (sync|add|run|export|lock|pip [a-z]+))\b'
```

The hits appear in more files than CI. Check `Dockerfile` and `Containerfile`,
`Makefile`, `justfile`, `Taskfile.yml`, `mise.toml` tasks, shell scripts,
`package.json` scripts such as `postinstall` and `prepare`, `devcontainer.json`,
platform config such as `netlify.toml`, `vercel.json`, and `Procfile`, plus code
blocks in `README.md` and the docs.

Give each hit a row with its file, line, and command. Add the site's purpose and
a reproducing-or-resolving verdict.

Done when every hit has a row with a verdict, docs and image builds included,
and each row names the lockfile it depends on.

### 2. Check the lockfile

Settle this per manager before touching any command:

```bash
git ls-files package-lock.json uv.lock           # committed?
git check-ignore -v package-lock.json uv.lock    # ignored anywhere?
uv lock --check                                  # current with pyproject.toml?
npm install --package-lock-only && git diff --exit-code package-lock.json
```

A missing or stale lockfile turns step 3 into a build failure. Regenerate and
commit it first, in its own commit, so the rewrite starts from a passing build.
Read `.dockerignore` too: a lockfile that never reaches the build context is the
same problem one layer down.

Done when each manager has a committed lockfile its own tool reports as current,
or a recorded plan to commit one first.

### 3. Rewrite the reproducing sites

| Resolving                                   | Frozen                                          | Fails when                                                       |
| ------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| `npm install`, `npm i`, `npm add`           | `npm ci`                                        | `package-lock.json` is missing, or disagrees with `package.json` |
| `npm install --no-save`                     | `npm ci`                                        | as above - `--no-save` protects the file, not the versions       |
| `npm install --production`                  | `npm ci --omit=dev`                             | as above                                                         |
| `uv sync`                                   | `uv sync --locked`                              | `uv.lock` is missing or out of date with `pyproject.toml`        |
| `uv run <cmd>`                              | `uv run --locked <cmd>`                         | as above                                                         |
| `uv pip install -r requirements.txt`        | `uv pip sync --require-hashes requirements.txt` | a requirement lacks a matching hash                              |
| `npm update`, `uv add`, `uv lock --upgrade` | keep - this is a resolving site                 | -                                                                |

`npm ci` deletes `node_modules` before installing, so it costs a full install.
That cost is what makes it reproducible.

uv gives two words and they differ. `--locked` asserts the lockfile is current
and errors if resolution would change it; `--frozen` skips that check and
installs what the lockfile already says. Use `--locked` wherever the manifest is
present, which is nearly everywhere. Reach for `--frozen` only where the layer
cannot support the check - a Docker build that copies `uv.lock` and
`pyproject.toml` without the project source - and put a `uv lock --check` step
in CI to cover what it skips. `UV_LOCKED=1` freezes every uv command in a job at
once. `npm` carries it on each command.

For a manager this table omits, get its word from `<tool> install --help`. The
vocabulary is `--frozen-lockfile` (`pnpm`, Yarn 1, `bun`), `--immutable` (Yarn
2+), `--locked` (Cargo), `--deployment` (Bundler), `--enforce-lockfile`
(`dart pub`), `--locked-mode` (`dotnet restore`), and `-lockfile=readonly`
(Terraform).

Done when every reproducing row runs a frozen command, and every resolving row
carries a comment naming it as one.

### 4. Close the ways back in

A frozen step still drifts when something downstream resolves:

- a later `npm install <pkg>`, `uv add`, or `uv pip install` in the same job
- a `package.json` script the frozen step triggers - `postinstall`, `prepare` -
  running its own install
- a `Makefile` target CI calls: the workflow step reads as frozen, the target
  inside it is not
- a `Dockerfile` that copies the source before the lockfile, or a
  `.dockerignore` that keeps the lockfile out of the build context

Done when nothing after a frozen install writes a lockfile or installs a
package, and the lockfile reaches every image build.

### 5. Make the drift loud once

Prove the check fails instead of trusting the flag. Widen a dependency range in
`package.json` or `pyproject.toml`, leave the lockfile alone, run the rewritten
command, and confirm it exits non-zero. Then revert and confirm it exits zero.

```bash
npm ci; echo $?
uv sync --locked; echo $?
```

Done when each rewritten command has been observed failing on a manufactured
mismatch and passing on the committed state, or carries a stated reason it could
not run here.

Report the rewritten sites, the resolving sites left deliberate, and the
documented way the lockfile now moves forward - a person running `npm update` or
`uv lock --upgrade`, or an update bot's pull requests. Pair a bot with the
`dependency-cooldown` skill so the versions it resolves have aged first.
