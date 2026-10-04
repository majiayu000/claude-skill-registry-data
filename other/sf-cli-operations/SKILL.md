---
name: sf-cli-operations
description: Operating Salesforce CLI v2 (`sf`) as the deterministic execution layer for a Salesforce project — the `sf org`, `sf project`, `sf apex`, `sf data`, `sf package`, `sf schema`, `sf sobject`, `sf config`, `sf alias`, `sf plugins` and `sf code-analyzer` topics, global flags (`--json`, `--target-org`, `--target-dev-hub`, `--api-version`, `--flags-dir`), non-interactive authorization (`sf org login web|jwt|sfdx-url|access-token`, connected app plus JWT for CI), config variables and aliases, `--json` result shapes with jq extraction recipes, `SF_*` environment variables, plugin and JIT-plugin management, retired `sfdx force:*` to `sf` migration, and the failure modes that break CI pipelines. Use this skill whenever a command line is being written or debugged, whenever an org must be authorized from a pipeline, whenever `--json` output must be parsed, whenever the API version or default org resolution looks wrong, or whenever a `sf` command fails with an auth, plugin, or version error.
---

# Salesforce CLI Operations (`sf` v2)

Salesforce CLI v2 ships as `@salesforce/cli`; the `sfdx` executable is an alias of `sf`, and every
`sfdx` invocation resolves to the same v2 command with the same flags. `sfdx (v7)` must be
uninstalled before installing v2 or npm fails with `EEXIST`.

## When to use

| Situation | Action |
| --- | --- |
| Writing any shell/hook/check invocation of Salesforce tooling | Use the topic map below; always pass `--target-org` explicitly |
| Authorizing an org from CI (no browser) | `sf org login jwt` or `sf org login sfdx-url` — see `references/auth-and-ci.md` |
| Parsing command output in a script | `--json` plus the shapes in `references/json-automation.md` |
| Default org / API version behaving unexpectedly | Precedence tables below and in `references/env-vars.md` |
| A command is missing (`sf code-analyzer`, `sf lightning dev`) | JIT plugin — see pattern 5 |
| Migrating legacy scripts off `sfdx force:*` | Migration table in `references/command-matrix.md` |

Deployment mechanics live in skill `sf-deployment-strategies`; org creation and sandbox lifecycle in
skill `sf-scratch-orgs-sandboxes`; data commands in skill `sf-data-management`; static analysis in
skill `sf-code-analyzer-quality`.

## Topic map

| Topic | Representative commands | Use for |
| --- | --- | --- |
| `sf org` | `login web`, `login jwt`, `login sfdx-url`, `login access-token`, `logout`, `display`, `display user`, `list`, `list auth`, `list limits`, `list metadata`, `list metadata-types`, `list sobject record-counts`, `open`, `create scratch`, `create sandbox`, `refresh sandbox`, `delete scratch`, `delete sandbox`, `enable tracking`, `disable tracking`, `assign permset`, `generate password`, `auth show-access-token`, `auth show-sfdx-auth-url`, `auth show-user-password` | Authorization, org inventory, org-level introspection |
| `sf project` | `deploy start`, `deploy validate`, `deploy quick`, `deploy report`, `deploy resume`, `deploy cancel`, `deploy preview`, `retrieve start`, `retrieve preview`, `delete source`, `generate manifest`, `list ignored`, `reset tracking`, `delete tracking`, `convert source`, `convert mdapi`, `convert source-behavior` | Metadata movement, manifests, source tracking |
| `sf apex` | `run`, `run test`, `get test`, `get log`, `list log`, `tail log` | Anonymous Apex, Apex tests, debug logs |
| `sf data` | `query`, `search`, `get/create/update/delete record`, `import/export tree`, `import/export/upsert/update/delete bulk`, `*/resume`, `bulk results`, `create file` | Records and datasets |
| `sf package` | `create`, `version create`, `version promote`, `install`, `installed list`, `version list`, `uninstall` | 2GP/unlocked packaging (skill `sf-packaging-release`) |
| `sf sobject` / `sf schema` | `sobject describe`, `sobject list`, `schema generate field/sobject/platformevent/tab` | Schema introspection and scaffolding |
| `sf template generate` | `apex class`, `apex trigger`, `lightning component`, `project`, `static-resource`, `visualforce page` | Scaffolding. Aliases `sf lightning generate component` and `sf force apex class create` still resolve |
| `sf agent` | `create`, `generate agent-spec`, `test run`, `preview` | Agentforce artifacts |
| `sf code-analyzer` | `run`, `config`, `rules` (JIT plugin `@salesforce/plugin-code-analyzer`) | Static analysis gate — `vf-check analyzer` |
| `sf plugins` | `install`, `link`, `uninstall`, `update`, `inspect`, `trust verify`, `reset` | Plugin lifecycle |
| `sf config` | `set`, `get`, `list`, `unset` | `target-org`, `target-dev-hub`, `org-api-version`, `org-max-query-limit` |
| `sf alias` | `set`, `list`, `unset` | Human-readable org names used by every `--target-org` |
| `sf autocomplete` | `sf autocomplete zsh`, `--refresh-cache` | Shell completion (regenerate after a CLI upgrade) |
| `sf doctor`, `sf which`, `sf version`, `sf update` | diagnostics and version management | Triage — pattern 6 |
| `sf force data bulk upsert|delete|status` | legacy Bulk API 1.0 wrappers that still exist in v2 | Only when serial batch mode is required; prefer `sf data * bulk` |

## Global flags

| Flag | Scope | Notes |
| --- | --- | --- |
| `--json` | every command that declares it under `GLOBAL FLAGS` | Prints `{status, result, warnings}`; overrides `--result-format` |
| `--flags-dir <dir>` | global | Reads flag values from files in a directory — one file per flag name |
| `-o, --target-org <alias\|username\|accessToken>` | org commands | Required unless `target-org` config or `SF_TARGET_ORG` is set. Accepts a raw access token (all commands except `sf org display user`) |
| `-v, --target-dev-hub <alias>` | `org create scratch`, `package*` | Dev Hub selector |
| `--api-version <n>` | most org commands | Overrides `apiVersion` — shape of the HTTP request, not of the metadata |
| `-w, --wait <minutes>` | async commands | `0` returns immediately with a job id |
| `-r, --result-format` | `apex run test`, `data query`, `data search`, `data export bulk` | `human\|csv\|json`, plus `tap\|junit` for Apex tests |

There is no `--loglevel` flag in v2. Set `SF_LOG_LEVEL=error|warn|info|debug|trace|fatal`; logs go to
`~/.sf/sf-<YYYY-MM-DD>.log`, rotate daily, and are deleted after seven days.

### apiVersion vs sourceApiVersion precedence

| `apiVersion` (request shape) | `sourceApiVersion` (metadata shape) |
| --- | --- |
| 1. `--api-version` flag | 1. `<version>` in the manifest |
| 2. `SF_ORG_API_VERSION` | 2. `sourceApiVersion` in `sfdx-project.json` |
| 3. `org-api-version` local config | 3. `--api-version` flag |
| 4. `org-api-version` global config | 4. `SF_ORG_API_VERSION` |
| 5. highest version the target org supports | 5. `org-api-version` local, then global, then org max |

vibe-force pins one value: `apiVersion` in `config/vibe-force.defaults.json` (`67.0`). Project setup
writes the same value to `sourceApiVersion` in `sfdx-project.json`, so `sf doctor`'s
`sourceApiVersion matches apiVersion` test passes.

## Core patterns

### 1. Authorize non-interactively, then alias everything

```bash
# CI: JWT bearer flow. Requires a connected app / external client app with the cert uploaded.
sf org login jwt \
  --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file "$PWD/server.key" \
  --username "$SF_USERNAME" \
  --instance-url https://mydomain.my.salesforce.com \
  --alias vf-int --set-default

# CI alternative: reuse an authorization captured on a workstation.
sf org auth show-sfdx-auth-url --target-org vf-int --no-prompt --json > auth.json
sf org login sfdx-url --sfdx-url-file auth.json --alias vf-int --set-default
```

`sf org login web` is for humans only; it opens `http://localhost:1717/OauthRedirect`. High-assurance
(stepped-up) authentication makes the JWT flow unusable for that org. Dev Hub orgs that must run
`sf org create scratch|sandbox` need a **connected app**, not an external client app.

### 2. Make the org selection explicit and reviewable

```bash
sf alias set vf-dev=test-3k9x@example.com vf-prod=release@acme.com
sf config set target-org vf-dev                  # project-local (.sf/config.json)
sf config set --global org-api-version 67.0
sf config list
```

Resolution order for any config-backed value: command-line flag, then local project config, then
global config. vibe-force commands and checks always pass `--target-org` so no run depends on the
ambient default; `productionAliases` in `.vibeforce/config.json` is matched against that value by the
vibe-force hooks before a deploy or destructive data command is allowed.

### 3. Script against `--json`, never against human output

```bash
# Which API version does the org actually run?
sf org display --target-org vf-dev --json | jq -r '.result.apiVersion'

# Fail the job when the org is not connected.
status=$(sf org display --target-org vf-dev --json | jq -r '.result.connectedStatus')
[ "$status" = "Connected" ] || { echo "org not connected: $status"; exit 3; }

# Row count guard after a data load.
sf data query --target-org vf-dev --json \
  --query "SELECT COUNT() FROM Account WHERE Industry='Energy'" \
  | jq -e '.result.totalSize >= 100' >/dev/null
```

Salesforce guarantees only additive changes to `--json` shapes; breaking changes go through a
deprecation period behind an environment variable. Human-readable output carries no such guarantee,
so `grep` on tables is not a contract. Per-command schemas live in each plugin repo under
`schemas/<command-with-hyphens>.json`; `sf which <command>` names the owning plugin.

### 4. Treat exit codes as the gate signal

| Exit code | Meaning in `sf` | vibe-force mapping |
| --- | --- | --- |
| `0` | command succeeded | check passes |
| `1` | command failed (validation error, deploy failure, test failure, org error) | `vf-check` returns `1` for gate failures, `3` when the failure is org/network |
| `2` | usage error raised by the oclif parser, such as an unknown or missing required flag `[unverified]` — the CLI docs state no exit-code contract beyond zero/non-zero | `vf-check` returns `2` (misconfiguration) |

With `--json`, a failure still prints JSON on stderr with `status` non-zero plus `name`, `message`,
and often `data`; `SF_JSON_TO_STDOUT=true` moves it to stdout, which is what a wrapper that pipes
into `jq` needs.

### 5. Install plugins explicitly; understand JIT

```bash
sf plugins                                   # installed (and JIT-installed) plugins with versions
sf plugins install @salesforce/plugin-code-analyzer
sf plugins install @salesforce/plugin-lightning-dev
sf plugins link ./my-local-plugin            # dev only: linked plugins are never auto-updated
sf plugins inspect @salesforce/plugin-data
sf plugins update
```

These plugins ship as just-in-time (JIT) entries in the CLI manifest and install on first use of one
of their commands: `@salesforce/plugin-code-analyzer`, `@salesforce/plugin-community`,
`@salesforce/plugin-custom-metadata`, `@salesforce/plugin-dev`, `@salesforce/plugin-devops-center`,
`@salesforce/plugin-flow`, `@salesforce/plugin-lightning-dev`, `@salesforce/plugin-signups`,
`@salesforce/plugin-ui-bundle-dev`, `@salesforce/sfdx-plugin-lwc-test`. A CI container should install
them up front — the first-use install writes to the CLI cache and adds latency (and a network
dependency) to the job that needs the command. `sf update` does not update JIT or user-installed
plugins.

### 6. Diagnose with `doctor`, logs, and `which`

```bash
sf doctor --output-dir .vibeforce/reports/doctor
sf doctor --command "org list --all"          # runs it in debug mode, writes stdout+stderr logs
sf doctor --plugin @salesforce/plugin-deploy-retrieve
SF_LOG_LEVEL=debug sf project deploy start --target-org vf-dev --dry-run
```

`sf doctor` always runs three built-in tests: `salesforcedx plugin not installed` (uninstall it if it
fails), `no linked plugins`, and `sourceApiVersion matches apiVersion`.

## Anti-patterns

| Anti-pattern | Why it breaks | Fix |
| --- | --- | --- |
| `sf project deploy start` with no `--target-org` in a script | Deploys to whatever default the runner happens to have — including production | Always pass `--target-org "$ORG_ALIAS"`; vibe-force hooks reject ambient-default org commands in `standard`/`strict` mode |
| `sfdx force:source:deploy -p force-app` | Retired v7 syntax; the `force:source:*` topic no longer exists in v2 | `sf project deploy start --source-dir force-app --target-org <alias>` (full table in `references/command-matrix.md`) |
| Parsing `sf org display` table output with `awk` | Human output can change in any release; secrets are now redacted there | `sf org display --json \| jq`, and `sf org auth show-*` for secrets |
| Committing `server.key`, `auth.json`, or an `sfdxAuthUrl` | Full org access in version control | Keep them in CI secret storage; `rm server.key` after use; `.gitignore` `*.key`, `auth*.json` |
| `sf org auth show-access-token` in a pipeline without `--no-prompt` | The command blocks on an interactive confirmation and the job hangs | Add `--no-prompt` (or `--json`) |
| Setting `SFDX_*` variables in new pipelines | They are deprecated synonyms; when both are set with different values the `SF_*` value wins and the CLI warns | Use the `SF_*` names in `references/env-vars.md` |
| Running the CLI headless on Linux/macOS without keychain config | Auth file encryption tries to reach the OS keychain and fails with a secret-service error | Export `SF_USE_GENERIC_UNIX_KEYCHAIN=true` in the CI image |
| Relying on JIT install inside the gate job | First run pulls from npm; an npm outage fails an otherwise green build | Pre-install in the image (pattern 5) |

## Verification

```bash
sf version                                    # expect @salesforce/cli/2.x
sf config list                                # target-org, org-api-version resolved as intended
sf org list --all --json | jq -r '.result.nonScratchOrgs[]?.alias'
sf org display --target-org vf-dev --json | jq '{api:.result.apiVersion, status:.result.connectedStatus}'
sf org list limits --target-org vf-dev --json | jq '.result[] | select(.name|test("DailyApiRequests|DataStorageMB"))'

# vibe-force gates that exercise the CLI end to end
node "$VF_ROOT/scripts/checks/vf-check.mjs" local
node "$VF_ROOT/scripts/checks/vf-check.mjs" apex --target-org vf-dev
node "$VF_ROOT/scripts/checks/vf-check.mjs" deploy-validate --target-org vf-int
```

`vf-check analyzer` requires `@salesforce/plugin-code-analyzer`; `vf-check apex`, `deploy-validate`,
`deploy-quick`, `smoke`, and `verify` all require a working authorization for the alias they are
given, and exit `3` when the CLI reports an org or network failure rather than a gate failure.

## References

- [`references/command-matrix.md`](references/command-matrix.md) — topic → command → key flags → purpose, plus the retired `sfdx force:*` → `sf` migration table.
- [`references/auth-and-ci.md`](references/auth-and-ci.md) — JWT setup end to end, connected app configuration, sfdx-url files, GitHub Actions/Jenkins/CircleCI snippets.
- [`references/json-automation.md`](references/json-automation.md) — `--json` shapes for `org display`, `org list`, `project deploy start|validate`, `apex run test`, `data query`, `data import bulk`, with jq extraction recipes.
- [`references/env-vars.md`](references/env-vars.md) — `SF_*` environment variables, config variables, and their precedence.
- Salesforce CLI Command Reference (generated): <https://github.com/salesforcecli/cli/blob/main/README.md>
- Salesforce CLI Setup Guide: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_intro.htm>
- Salesforce DX Developer Guide, Authorization: <https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth.htm>
- Environment variable definitions (`@salesforce/core`): <https://github.com/forcedotcom/sfdx-core/blob/main/src/config/envVars.ts>
