---
name: install-scripts
description:
  Stop dependency install scripts from executing - a committed `ignore-scripts`
  for `npm`, `--no-build` for `uv` - then allowlist by name the few packages
  that genuinely build something. Use when the user wants to block `postinstall`
  scripts, harden a project against a compromised release, or mentions
  `ignore-scripts`, lifecycle scripts, or `npm rebuild`. Covers `npm` and `uv`.
version: 0.1.0
---

# Install Scripts

Installing a package should copy files. A `preinstall`, `install`, or
`postinstall` script makes it run code instead - with your shell, your
environment, your CI token, and your `~/.ssh`, before anyone has read a line of
the package. The Shai-Hulud worm propagated exactly this way, out of a
transitive dependency nobody chose.

Almost no package needs it. In one 437-package tree, two do: `esbuild` and
`fsevents`, both distributing native binaries. That ratio is what makes the fix
cheap - **deny** every script by default, then **allowlist** the handful that
build something, each with its reason beside it.

Read the flags off the installed tool: `npm help config`, `uv sync --help`.

## Procedure

### 1. List the packages that run code today

Read it out of the lockfile, with nothing installed:

```bash
jq -r '.packages | to_entries[] | select(.value.hasInstallScript) | .key' package-lock.json
uv sync --no-build --no-install-project --dry-run
```

`hasInstallScript` flags `preinstall`, `install`, and `postinstall`. It does not
flag `prepare`, which runs for git and path dependencies - read the manifest of
each dependency pulled from a git URL.

uv has no `postinstall`. Python code runs at install time when a **source
distribution** builds, so the script surface is the set of dependencies with no
wheel, and the `--dry-run` above names one per run.

Do the same for the project's own scripts
(`grep -nE '"(pre|post)?[a-z]+"\s*:' package.json`), because the deny in step 2
catches those too.

Done when every package that executes code at install time is listed with what
it builds and whether the project needs it, and the project's own lifecycle
scripts sit beside that list.

### 2. Deny by default

For `npm`, commit it so CI, contributors, and image builds share one setting:

```ini
# .npmrc
ignore-scripts=true
```

For `uv`, put it on the install command - `UV_NO_BUILD=1` covers a whole job:

```bash
uv sync --locked --no-build --no-install-project
```

`--no-build` refuses to build any source distribution, including the project
itself. Put `--no-install-project` beside it, then install the project in a
second step without the flag: its build backend is code you wrote.

Cover every install site - CI, image builds, task runners, deploy scripts -
which the `frozen-install` skill's step 1 grep finds. In a `Dockerfile`, copy
`.npmrc` in before the install layer, or the deny does not apply.

For a manager this skill omits, the vocabulary is `onlyBuiltDependencies` with
`pnpm approve-builds` (`pnpm` 10 denies by default), `trustedDependencies`
(`bun`), and `enableScripts: false` with `dependenciesMeta.<pkg>.built` (Yarn
2+).

Done when every install site denies scripts through committed config or an
explicit flag, and the deny reaches the image build.

### 3. Allowlist what builds

Rebuild the needed packages by name, right after the install that skipped them:

```bash
npm ci
npm rebuild --ignore-scripts=false --foreground-scripts esbuild fsevents
```

A project-wide `ignore-scripts=true` applies to `npm rebuild` as well, so
without `--ignore-scripts=false` the rebuild reports success and runs nothing at
all. `--foreground-scripts` prints what each script did so you can confirm it
ran.

uv has no per-package allowlist: `--no-build-package` denies more, and nothing
permits less. A dependency with no wheel leaves three choices - replace it,
build and host a wheel yourself, or drop `--no-build` for the whole tree and
record which package forced that.

Keep the allowlist beside the install command it follows, with the reason per
package:

```yaml
# esbuild, fsevents: native binaries, no JavaScript fallback
run: npm rebuild --ignore-scripts=false esbuild fsevents
```

Done when every allowlisted package names its reason, and nothing sits in the
allowlist that step 1 did not flag.

### 4. Restore the project's own scripts explicitly

`ignore-scripts=true` silences the project's own lifecycle scripts too, and it
does it quietly: `npm run` and `npm test` still run the script named, while
their `pre` and `post` hooks stop firing, so `npm test` passes without its
`pretest` fixture step.

- Call the hook where it was implied: `npm run pretest && npm test`, or fold it
  into the main script.
- Run `prepare` work - `husky`, a build before publish - as its own command.

Done when every `pre` hook, `post` hook, and `prepare` from step 1 is either
called explicitly somewhere or recorded as deliberately dropped.

### 5. Prove nothing ran

```bash
rm -rf node_modules && npm ci --foreground-scripts
```

`--foreground-scripts` prints every script that executes, so a denied install
prints nothing for the step 1 packages. Output from any of them means the deny
is not in effect at that site. Then run the allowlist rebuild and confirm output
appears for exactly the allowlisted packages and no others.

For uv, `uv sync --no-build --no-install-project --dry-run` exiting zero is the
observation: no dependency needs a build.

Done when a fresh install at each site from step 2 produces script output from
the allowlist only.

Report the denied sites, the allowlist with reasons, and the hooks moved in
step 4. A package can still run its code once the project imports it. A deny
also says nothing about which version arrived. Pair this with
`dependency-cooldown` so a fresh release ages first, and `frozen-install` so
every site installs the same tree. Check the update bot as well: it installs on
its own infrastructure with its own token when it refreshes the lockfile.
