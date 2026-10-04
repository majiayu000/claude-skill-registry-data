---
name: renovate
description: Audit, write, or revise renovate.json. Use when adding Renovate, troubleshooting unexpected (or missing) update PRs, hardening against supply-chain attacks, or evolving an existing config.
---

A **silent stall** is a dependency that can never update yet looks current: no PR, no error, no `[Updates: ...]` on the dashboard.

## Defaults

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:best-practices",
    "security:openssf-scorecard",
    "customManagers:githubActionsVersions"
  ],
  "timezone": "Europe/London",
  "reviewers": ["alunduil"],
  "labels": ["dependencies"],
  "pre-commit": { "enabled": true }
}
```

- This block is identical in every repo and is a standing candidate for a shared preset (`github>alunduil/renovate-config`, a `default.json`); Renovate also checks `<owner>/renovate-config` when onboarding a new repo. Until that repo exists, keep the block inline and change it everywhere at once.
- Omit `baseBranchPatterns`. It is auto-detected, and hard-coding it is the one field that differs per repo (`main` vs `master`) — the thing that would block sharing.
- Omit `schedule` unless a repo wants batching. With a bake period the PR is already delayed, and Renovate's default `prHourlyLimit` of 2 rate-limits the rest.
- `packageRules` and `customManagers` are `mergeable: true`, so preset arrays concatenate with a repo's own rather than replacing them. `labels` and `reviewers` are not mergeable — setting them in a repo replaces the inherited value. `addLabels` merges and appends; `labels` in a shared preset is dropped wholesale by the first repo setting its own.
- `labels` — default `[]`, so Renovate labels nothing without this. A stale sweep exempting Renovate PRs by label depends on it: closing a Renovate PR tells Renovate the version is unwanted and it will not re-offer it. `vulnerabilityAlerts` takes no `labels`.
- `reviewers` — without it, Renovate PRs land silent. Use `assignees` instead for a creation-time ping with no rebase notifications.
- `pre-commit: { enabled: true }` — opt-in manager; enable unconditionally. No-op without `.pre-commit-config.yaml`; replaces pre-commit.ci where the file exists.
- `config:best-practices` = `config:recommended` + `docker:pinDigests` + `helpers:pinGitHubActionDigests` + `:configMigration` + `:pinDevDependencies` + `abandonments:recommended` + `security:minimumReleaseAgeNpm` + `:maintainLockFilesWeekly`. It does *not* include OpenSSF scorecard; that is `security:openssf-scorecard`, which adds a badge column to PR bodies.

## Supply-chain hardening

`config:best-practices` bakes npm releases for 3 days (`security:minimumReleaseAgeNpm`) but nothing else. Widen it to every datasource:

```json
{
  "minimumReleaseAge": "3 days",
  "minimumReleaseAgeBehaviour": "timestamp-optional",
  "osvVulnerabilityAlerts": true,
  "packageRules": [
    {
      "matchUpdateTypes": ["pin", "pinDigest", "digest", "lockFileMaintenance",
                           "lockfileUpdate", "rollback", "bump", "replacement"],
      "minimumReleaseAge": null
    }
  ]
}
```

- `minimumReleaseAge` — 3-7 days catches the common attack shape (publish → community flags → upstream yanks within a day or two).
- A release with no timestamp is a silent stall. The default `timestamp-required` treats it as never stable, and the default `internalChecksFilter: "strict"` cuts no branch while `renovate/stability-days` pends. Two causes, one fix each:
  - **Update type** — the eight types in the carve-out never carry a timestamp. `config:best-practices` pulls in `:maintainLockFilesWeekly` and both digest-pinning presets, so `lockFileMaintenance`, `digest`, and `pinDigest` are always in scope.
  - **Datasource** — some datasources return no timestamp for any release; with `hackage`, every cabal dependency stalls. These are ordinary major/minor/patch updates the carve-out cannot reach. `timestamp-optional` lets a timestamp-less release through with a Dependency Dashboard warning; releases that carry a timestamp still bake.
  - Keep both. The carve-out removes the age check from the eight types, so the dashboard warning names only datasources that lack timestamps.
- `osvVulnerabilityAlerts: true` — widens alerts beyond GitHub's advisory database to OSV. Defaults to `false`. Haskell repos are the exception: OSV fixes arrive as an open range (`>= <fixed>`), `pvp` accepts only two-bound ranges, and the generated rule aborts every run. Treat a `false` there as deliberate and look for its tracking issue.
- Do *not* write `internalChecksFilter: "strict"` or `vulnerabilityAlerts: { "minimumReleaseAge": "0 days" }`. Both are already the defaults (`lib/config/options/index.ts`: `internalChecksFilter` default `strict`; the `vulnerabilityAlerts` default object contains `minimumReleaseAge: null`, force-applied over the top-level bake).
- `minimumReleaseAge: "0 days"` is identical to `null` as of Renovate 42.19.5. Prefer `null`.

## Version pins in scripts

Annotate the pin; do not write a manager per pin. One generic manager reads them all, and a new pin needs no config change:

```bash
# renovate: datasource=github-releases depName=mikefarah/yq
YQ_VERSION="v4.53.2"
```

```json
{
  "customType": "regex",
  "managerFilePatterns": ["script/install/*", ".chezmoiscripts/*.tmpl"],
  "matchStrings": [
    "# renovate: datasource=(?<datasource>[a-zA-Z0-9-._]+?) depName=(?<depName>[^\\s]+?)(?: packageName=(?<packageName>[^\\s]+?))?(?: versioning=(?<versioning>[^\\s]+?))?(?: extractVersion=(?<extractVersion>[^\\s]+?))?\\s+[A-Za-z0-9_]+?_VERSION=\"(?<currentValue>.+?)\""
  ]
}
```

- Annotation field order is fixed by the regex: datasource, depName, packageName, versioning, extractVersion, registryUrl. `datasource`, `versioning`, `extractVersion` and `registryUrl` are recognised capture-group names — no `*Template` fields needed. An out-of-order annotation does not match — a silent stall.
- Set `versioning=loose` on every plain pin whose upstream is not semver. The default, `semver-coerced`, reads a four-component version (Haskell PVP, some .NET and Java tools) as unstable, and `ignoreUnstable` drops every release — a silent stall. Two-component versions work by accident: `3.10` coerces to `3.10.0`.
- `pvp` updates only two-bound cabal ranges under `rangeStrategy: "widen"`; a plain pin never updates. `datasource=hackage` defaults to `pvp`, so write `versioning=loose` on a hackage pin.
- For workflow YAML (`X_VERSION: "v1"` under `env:`) extend `customManagers:githubActionsVersions` instead of writing this yourself; add `extractVersion=^v(?<version>.+)$` when the consumer wants the tag without its leading `v`.
- Hoist a `with:` version input to `env:` only when its action is missing from the [known-actions table](https://docs.renovatebot.com/modules/manager/github-actions/#updating-with-values-in-github-actions). Renovate reads a listed action's input natively, `actions/setup-*` included; hoisting it removes a working dependency.
- Upstream ships equivalents for Dockerfiles, Makefiles, `*.tfvars`, `pom.xml`, and several CI formats — check `customManagers:*` before writing a regex.
- Keep a bespoke manager only where an annotation cannot go: a version embedded in a URL (capture `depName` and `currentValue` from the URL itself), or a snippet in user-facing docs where a `# renovate:` line would be copy-pasted by a reader.
- `managerFilePatterns` (renamed from `fileMatch`): bare strings are globs; wrap in `/.../` for a regex. Prefer the glob.
- Validate `matchStrings` against the real files after adding a manager or editing an annotation — the regex is ECMAScript/RE2 (no lookahead, no backreferences), and a non-matching manager is a silent stall.

## Validation

Wire `renovate-config-validator` as a pre-commit hook so schema typos, deprecated fields, and malformed custom-manager regex fail at commit time instead of surfacing as Repository Problems on the next Renovate run.

```yaml
- repo: https://github.com/renovatebot/pre-commit-hooks
  rev: <latest>
  hooks:
    - id: renovate-config-validator
      args: [--strict, --no-global]
```

- `--strict` — fail on configs that need migration (e.g. `fileMatch` → `managerFilePatterns`), not only on outright errors. Neither flag is upstream default; both go in `args`.
- `--no-global` — treat the file as repo-level config. Without it the validator interprets it as global self-hosted config and misreports repo-only fields.
- The validator does not resolve remote presets, so it cannot tell you an `extends` target is missing or that a shared preset changed under you.
- Upstream docs: <https://docs.renovatebot.com/config-validation/>.

## Liveness

A hosted Renovate job that dies is never retried and reports nowhere, so a repo with a valid `renovate.json` can stop getting updates unnoticed. Self-hosted Renovate reports its failures in the repo's Actions log and needs no check.

Renovate edits the open Dependency Dashboard issue as updates come and go, so a dashboard left untouched means Renovate has stopped. Add this job, taken from [genshin.dungeon.studio `daily.yml`](https://github.com/dungeon-studio/genshin.dungeon.studio/blob/main/.github/workflows/daily.yml), to the repo's `daily.yml`; create that workflow if the repo has none.

```yaml
renovate-liveness:
  name: Check Renovate liveness
  runs-on: ubuntu-latest
  timeout-minutes: 5
  permissions:
    issues: read
  steps:
    - uses: actions/github-script@<sha> # <version>
      with:
        script: |
          const STALE_DAYS = 10;
          const MS_PER_DAY = 86_400_000;
          const query = `repo:${context.repo.owner}/${context.repo.repo} is:issue is:open in:title "Dependency Dashboard" author:app/renovate`;
          const { data } = await github.rest.search.issuesAndPullRequests({ q: query });
          const dashboard = data.items[0];
          if (!dashboard) {
            core.setFailed('No open Dependency Dashboard: Renovate is uninstalled or disabled on this repository. Reinstall the app or re-enable the repository.');
            return;
          }
          const ageDays = (Date.now() - new Date(dashboard.updated_at)) / MS_PER_DAY;
          if (ageDays > STALE_DAYS) {
            core.setFailed(`Dependency Dashboard #${dashboard.number} last updated ${ageDays.toFixed(1)} days ago: Renovate runs are dying. Read the Mend job log, then trigger a run by hand.`);
          }
```

- Set `STALE_DAYS` to about twice the longest healthy quiet spell.
- The failed run is the alert: GitHub emails it to whoever created the workflow or last edited its cron. Passing runs are silent, so a daily check adds no noise.

## Dashboard reading

Renovate opens a "Dependency Dashboard" issue. Read it before assuming a bug:

- **Detected Dependencies** without `[Updates: ...]` = current or silently stalled; the dashboard cannot tell them apart.
- **Pending Status Checks** — the bake period holding an update back. A resident older than the bake points to a missing carve-out or a datasource with no timestamps.
- **Repository Problems** — investigate. "Base branch does not exist" usually means a stale config reference or a transient mid-run state.
- **Config Migration Needed** — Renovate offers an automated PR for field renames (e.g. `fileMatch` → `managerFilePatterns`, `baseBranches` → `baseBranchPatterns`). Tick the checkbox or hand-migrate.
- **Open** — pending PRs; the per-row checkboxes force a rebase/retry.

## Procedure

1. Confirm any field name, default, or preset body you plan to rely on against the source, not memory: defaults in `lib/config/options/index.ts`, preset bodies in `lib/config/presets/internal/*.preset.ts`. Docs summaries and prior commits drift — several fields once worth writing are now defaults.
2. Read `renovate.json` if present, and any preset it extends.
3. **Greenfield** — write the Defaults and Supply-chain hardening blocks. Add `customManagers` only for pins the annotation convention cannot reach. Add the `renovate-config-validator` pre-commit hook (see Validation).
4. **Audit existing** — flag drift:
   - Restated defaults: `internalChecksFilter`, `vulnerabilityAlerts.minimumReleaseAge`, `baseBranchPatterns`.
   - Silent-stall causes: a no-timestamp carve-out missing or narrower than the eight update types, missing `minimumReleaseAgeBehaviour: "timestamp-optional"`, a non-semver plain pin without `versioning=loose`, unannotated `*_VERSION=` pins, a literal `with:` version on an action missing from the known-actions table.
   - Structure: one manager per pin where an annotation would do, a listed action's `with:` input hoisted to `env:`, deprecated `fileMatch`/`baseBranches`, missing validator hook, missing `labels` where a workflow exempts Renovate PRs by label.
   - Liveness: a repo on hosted Renovate with no dashboard-staleness job in a daily workflow.
5. **Cross-check** — compare each detected dependency against its upstream latest release, each Pending Status Checks resident against its release date, and each tool's pins across workflows; diverging versions of one tool mean one pin is unmanaged. A config can pass step 4 and still hold a silent stall; only these comparisons show it.
6. Surface findings before editing. Apply only after scope is agreed.
