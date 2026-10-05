---
name: renovate-setup
description: >-
  Add or extend Renovate with a seven-day minimum release age and immutable
  updates: lock files and integrity hashes, GitHub Action SHAs, and container
  digests. Use when adopting Renovate, replacing another update bot, covering
  missing manifests, or updating tools, images, actions, or custom files.
version: 0.2.0
---

# Renovate Setup

A Renovate config is complete only when its **update inventory** accounts for
every dependency declaration and its immutable artifact. Every setup must:

- apply `minimumReleaseAge: "7 days"` to every update type and data source that
  supports it, while preserving any longer existing minimum;
- update committed lock files and their tool-generated integrity
  hashes/checksums, including periodic lockfile maintenance where supported;
- pin GitHub Actions to full commit SHAs and container images to digests where
  Renovate supports them, retaining a readable version comment or tag; and
- record an explicit unsupported reason where Renovate or the package manager
  cannot produce an immutable or locked artifact.

These baseline requirements are mandatory. Start with a short config. Renovate
enables most built-in managers by default. A long
`enabledManagers` list or a custom regex for a supported format makes future
manifests easier to miss.

Keep three forms distinct. An exact dependency version in a manifest is
**version pinning**. A lockfile resolves manifest
ranges and can contain package-manager integrity data. A commit SHA or image
digest makes the referenced action or image content immutable. Renovate cannot
create hashes for every ecosystem or make a custom-manager match update a
related checksum automatically.

Use Renovate's current
[manager index](https://docs.renovatebot.com/modules/manager/) and the linked
manager pages as the source of truth. Manager names, default
`managerFilePatterns`, and capabilities change. Renovate has a built-in
[mise manager](https://docs.renovatebot.com/modules/manager/mise/), so mise does
not need a custom manager.

## Procedure

### 1. Establish the existing behavior

Find every repository-level config and every way Renovate runs:

```bash
git ls-files | grep -E '(^|/)(renovate\.json5?|\.renovaterc(\.json5?)?|package\.json|config\.(js|cjs|mjs)|renovate-config\.(js|cjs|mjs))$|(^|/)\.github/(renovate\.json5?|workflows/)|(^|/)\.gitlab-ci'
git grep -nEi 'renovate(bot)?|renovate-config-validator'
```

Read the complete local config, all `extends` presets, repository workflow, and
self-hosted global config that is available. Record:

- the canonical config file and its syntax;
- hosted app or self-hosted runner, platform, credentials boundary, and
  schedule;
- inherited and local presets, `enabledManagers`, manager disables,
  `ignorePaths`, `includePaths`, custom managers, package rules,
  `minimumReleaseAge`, `pinDigests`, and `lockFileMaintenance`;
- the current update bot and any policy that must survive a migration.

Keep one canonical config. Extend the existing file in its existing syntax
instead of creating a competing `renovate.json`. Treat inherited presets and
global configuration as active even when they are outside the repository.

Resolve preset contents and package-rule precedence instead of judging the
local file alone. Find every rule that lowers, nulls, or scopes
`minimumReleaseAge`, disables digest pinning or lockfile maintenance, or skips
artifact updates.

Done when every config layer and execution path is named, every existing rule
has a keep, change, or retire verdict, and the strongest existing cooldown is
known.

### 2. Inventory every dependency declaration

Start with all tracked files, not only root manifests:

```bash
git ls-files
git ls-files | grep -Ei '(^|/)(mise(\.[^.]+)?\.toml|\.mise(\.[^.]+)?\.toml|mise/config\.toml|mise\.lock|\.tool-versions|package\.json|.*lock.*|pyproject\.toml|requirements[^/]*|Pipfile|poetry\.lock|Cargo\.toml|go\.(mod|work)|Gemfile|composer\.json|pom\.xml|build\.(gradle|gradle\.kts|sbt|mill)|gradle-wrapper\.properties|mix\.exs|pubspec\.yaml|Package\.swift|.*\.(csproj|fsproj|vbproj)|global\.json|Dockerfile[^/]*|Containerfile[^/]*|compose[^/]*\.ya?ml|Chart\.yaml|Chart\.lock|values[^/]*\.ya?ml|kustomization\.ya?ml|terraform\.lock\.hcl|.*\.tf|\.pre-commit-config\.yaml|devcontainer\.json|flake\.lock|Brewfile)$|(^|/)\.(github|gitlab|circleci)/'
git grep -nEI 'uses:[[:space:]]*[^[:space:]]+@|(^|[[:space:]])FROM[[:space:]]+|image:[[:space:]]*[^[:space:]]+|release(s)?/download/|[A-Z0-9_]+_VERSION|(^|[[:space:]])version[[:space:]]*[:=]'
```

The filename search is a lead list, not an allowlist. Inspect task runners,
shell and PowerShell scripts, CI, container build arguments, deployment files,
docs that drive installs, generated examples, and nested workspaces. Find
versions hidden in download URLs, image tags, action references, and install
commands. Distinguish a dependency declaration from a project's own version.

Give every declaration a row:

| File and field | Dependency | Version form | Lock, hash, or immutable target | Owner or mirror | Intended scope |
| -------------- | ---------- | ------------ | ------------------------------- | --------------- | -------------- |

An **owner** is the source Renovate should update, while a **mirror** repeats a
version owned elsewhere and needs either synchronized updates or an explicit
reason to stay manual. Include lock files beside their manifests. Mark fixtures, examples,
third-party source copies, generated files, and local-only mise configs as in
scope or intentionally excluded. Presets can ignore these directories silently.

Pair each manifest with its committed lockfile, checksum file, or generated
artifact. For actions, include the full SHA and trailing version comment. For
images, include both the readable tag and digest.

Done when every tracked dependency declaration has a row, including every mise
tool in top-level `[tools]` and `tasks.*.tools`, and each row has an explicit
scope verdict and immutable target or candidate unsupported reason.

### 3. Map the inventory to built-in managers

For each in-scope row, consult the manager index and that manager's page. Record:

| Declaration | Manager | Pattern matches? | Extracts? | Artifact update | Timestamp available? |
| ----------- | ------- | ---------------- | --------- | --------------- | -------------------- |

Prefer a built-in manager whenever one understands the format. Common
non-package managers include `github-actions`, `dockerfile`, `docker-compose`,
`devcontainer`, `pre-commit`, and `mise`, but verify their current names and
patterns instead of copying this list into `enabledManagers`.

Manager `managerFilePatterns` are additive. Add a narrow pattern under that
manager only when the file uses a supported format under a nonstandard name.
Use `ignorePaths` or `includePaths` for path scope. Check preset-derived ignores:
`config:recommended` commonly excludes tests, examples, fixtures, and vendor
directories.

Leave `enabledManagers` absent for a new config so default managers can discover
future manifests. If the existing config intentionally uses it, either remove
the restriction with the user's agreement or add every discovered built-in and
`custom.*` manager. Preserve intentional manager disables.

For mise, verify each backend and version syntax against the mise manager page.
Its built-in manager recognizes standard and environment-specific config,
top-level and task tools, and `mise.lock`. Some backend forms have documented
limitations. A lockfile refresh executes `mise lock`. A self-hosted administrator
must decide whether to allow the `mise` unsafe execution globally. Record that
decision instead of hiding a blocked lock update.

For each built-in manager, verify both extraction and artifact support on its
current manager page. Normal version PRs should refresh the corresponding
lockfile and generated integrity fields. `lockFileMaintenance` also re-resolves
transitive versions without changing the manifest. It is not a
substitute for normal lockfile updates.

Done when every in-scope row maps to a matching built-in manager and an
immutable/artifact strategy, or names the exact unsupported capability.

### 4. Fill only unsupported declarations

First check Renovate's
[custom-manager presets](https://docs.renovatebot.com/presets-customManagers/)
and manager-specific configuration. Use `customManagers` only for a declaration
that no built-in manager extracts:

- use `jsonata` for structured JSON, JSON5, or YAML;
- use `regex` for stable line-oriented text and comment conventions;
- make `managerFilePatterns` as narrow as the real file set;
- extract or template the data source, dependency identity, and current value;
- set `versioningTemplate` explicitly unless the data source defines the right
  versioning;
- preserve surrounding text and constrain captures so one dependency cannot
  consume the next line.

Follow the current
[custom manager contract](https://docs.renovatebot.com/configuration-options/#custommanagers).
Test each matcher against representative matches, inputs that must not match,
indentation, and multiple declarations in one file. Prefer an adjacent
`renovate:` annotation when a generic assignment does not contain enough
identity to update safely.

A custom manager usually updates only the captured version text. If a download
also has a checksum, use a manager or artifact update that regenerates both in
one PR; otherwise keep the row unsupported instead of leaving a stale checksum
or inventing one.

Done when every unsupported declaration has a tested extractor, no custom
manager duplicates a built-in manager, and every associated checksum is updated
atomically or has an unsupported verdict.

### 5. Merge the minimum config

For a repository with no config, start with:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "docker:pinDigests",
    "helpers:pinGitHubActionDigests",
    ":maintainLockFilesWeekly"
  ],
  "minimumReleaseAge": "7 days"
}
```

The digest presets retain an image tag as `tag@sha256:...` and turn an action
tag into `owner/action@<full-sha> # <version>`. That metadata lets reviewers
read the version and lets Renovate update the immutable reference. Add a version
comment to an existing bare action SHA; Renovate disables updates for bare SHAs
whose source tag or branch it cannot determine.

Keep `minimumReleaseAge` at top level so it covers the supported data sources.
Inspect inherited and local package rules after merging. Remove a shorter or
`null` override, or replace it with an equally scoped value of `"7 days"`;
preserve values longer than seven days. Keep the default
`minimumReleaseAgeBehaviour: "timestamp-required"`: a data source without a
usable timestamp cannot prove a seven-day age and belongs in the report as a
cooldown limitation, not behind a global timestamp-optional escape.

`config:best-practices` currently includes both digest presets, weekly lockfile
maintenance, and an npm-specific three-day minimum. It can remain, but replace
the three-day value that wins after merging with seven days. Do not assume the
top-level value wins over an inherited package rule.

Enable `lockFileMaintenance` when supported lock files exist. Preserve an
existing maintenance schedule, or use `:maintainLockFilesWeekly`. Confirm that
the self-hosted runner allows each package manager or other artifact command.
Renovate must commit lock files, integrity hashes, checksums, and related
generated metadata exactly as the generating tools produce them; never hand-edit
those fields.

Then add only the manager patterns, custom managers, and policy the inventory
requires. Preserve existing `extends`, package rules, schedules, grouping,
labels, registry settings, and security policy unless a baseline above requires
strengthening. Merge arrays according to Renovate's option semantics; validate
the fully merged result instead of assuming ordinary JSON merge behavior.

Choose manifest `rangeStrategy` separately. Exact manifest pins can be useful
for applications and tools. Libraries can require ranges, and peer dependencies
must express compatibility. A committed, refreshed lockfile is the immutable
resolution strategy in those cases. `rangeStrategy: "pin"` does not replace it.

`minimumReleaseAge` cannot age `lockFileMaintenance` or `lockfileUpdate`
updates because Renovate delegates their resolution to the package manager.
Configure that manager's committed native cooldown when it supports one. Where
it does not, report the transitive lockfile-maintenance gap explicitly; the
seven-day Renovate gate still applies to supported direct version and digest
updates. Security updates bypass Renovate's minimum release age.

Keep credentials and self-hosted-only options in the runner's secret/global
configuration. Repository config can name a private registry, but tokens do not
belong in it.

If another bot updates the same dependency set, disable it only after Renovate
is activated; two bots create competing branches, while disabling first creates
an update gap.

Done when the canonical config has a minimum of at least seven days after all
presets and package rules merge, digest/SHA pinning, and supported lockfile
maintenance, and every inventory row has an immutable/artifact strategy or
exact unsupported reason.

### 6. Validate syntax and extraction

Run Renovate's validator with the same major version as the deployment when it
is pinned. Otherwise use current Renovate:

```bash
npx --yes --package renovate -- renovate-config-validator --strict
```

Pass a custom filename with `--no-global`. Without it, the validator treats
an explicit file as global configuration. Resolve warnings and migrations, not
only errors.

Then prove discovery locally:

```bash
LOG_LEVEL=debug npx --yes --package renovate -- renovate --platform=local --dry-run=extract
```

Compare the extracted package files and dependencies with the inventory row by
row. For behavior that requires the real platform, inherited config, private
registries, or lockfile execution, run the deployment in `dryRun=extract` or
`dryRun=lookup` and inspect its debug logs. Validate a config branch through the
hosted app when applicable.

Inspect the fully merged config, not only validator success. Prove for every
row that:

- the `minimumReleaseAge` that wins after all config merges is at least seven
  days, or the data source has a documented timestamp limitation;
- an action becomes a full SHA with a readable version comment and an image
  becomes a digest pin with its readable tag;
- a normal update refreshes its lockfile and integrity data; and
- lockfile maintenance runs where the manager supports it.

Review a real or dry-run update branch where artifact execution is available.
The generated lockfile/checksum diff must pass that package manager's frozen or
locked install/check command. A dry extraction alone cannot prove artifact
updates.

Done when strict validation passes, every in-scope row appears with the intended
manager, `datasource`, current version, cooldown verdict, and immutable/artifact
result, and each unavailable check has an owner and exact follow-up action.
Report managers and custom managers enabled after all config layers merge; the
`minimumReleaseAge` that wins after merging for every row, including each
preserved minimum longer than seven days; covered manifests, tool files, lock
files, integrity hashes/checksums, action SHAs, and image digests, including
mise; each row's immutable/lockfile strategy or explicit unsupported reason;
intentional exclusions and mirrors that remain manual; and validation and
extraction commands with outcomes. Note any administrator-only activation step
with an owner and exact follow-up action.
