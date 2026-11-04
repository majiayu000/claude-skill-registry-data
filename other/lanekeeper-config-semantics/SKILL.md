---
name: lanekeeper-config-semantics
description: Domain rules for how Lanekeeper models config files. It covers the two repos, how files are named on NFS, how the Spring Cloud config-server resolves property sources and resource files (tenant suffixes, channel folders, search locations, ${KEY} rendering), drift states, when changes take effect, and checks C1–C11. Use this skill whenever you touch the engine, registry, write paths, MCP tools, docs feature status, fixtures or tests that involve effective config, rendering, drift, adoption, path mapping, the comparison grid, tenants or channels. Use it even if the task names only one of these concepts, because they interact, and getting one wrong silently corrupts every view built on top of it.
---

# Lanekeeper config semantics

Every view in Lanekeeper, whether a diff, the grid, drift, findings or an MCP answer, comes from the rules below. A small mistake here produces confident wrong answers, and nobody notices because the UI still looks fine. Read the whole file before you change anything in `crates/engine`, `crates/hub-registry` or a fixture.

The authoritative sources are `docs/domain-model.md` and decisions D11–D20, D72–D88 in `docs/decisions.md`. This skill is the working summary. Where they disagree, those documents win, so flag the gap.

## 1. Where files come from

- `configuration-base-saas`: config under `config/`. It has one branch, and tags mark versions.
- `csp-tenant-data`: config under `data/config/`. Its branches fall into three groups:
  - `sit1` … `sitN` are tenants;
  - `templates/*` are Core templates, which are never deployed;
  - `templates/common-docs` holds the docs.
- **In Git, a tenant file has the same relative path as its base file.**
- **On NFS, a tenant file sits beside the base file with the tenant id as a suffix.** For example, `tx-infinity-api/tx-infinity-core-sit1.yml` sits next to `tx-infinity-api/tx-infinity-core.yml`.
- **The tenant id equals the tenant branch name.** The tenant data deploys as the Helm chart `csp-tenant-data-<branch>`.
- **A swimlane has a set of tenants, not exactly one** (Q34). Never assume a single tenant.

### Path mapping

Implement this mapping with `PathMappingRule`.

- **Forward:** `data/config/<rel>/<name>.<ext>` on branch B maps to `<nfs_root>/<rel>/<name>-B.<ext>`.
- **Reverse:** strip an exact `-<tenant>` immediately before the extension, where `<tenant>` is a known tenant. Names like `tx-infinity-core` contain hyphens of their own, so never split on the first hyphen.
- **Extension-less files:** the suffix goes at the end of the name.

## 2. How the config-server resolves a request (D82–D83)

A service requests `(application, profile = "<tenant>,default", label = master, [channel], file)`. There are two kinds of file, and they follow different rules.

**Property sources** are `application.*`, `<app>.*`, `application-<tenant>.*` and `<app>-<tenant>.*`, in `.properties`, `.yml` or `.yaml`. Together they form the *property view*, merged setting by setting. Highest precedence first:

1. `<app>-<tenant>.*`
2. `application-<tenant>.*`
3. `<app>.*`
4. `application.*`

At equal rank, `.properties` beats `.yml`, and a later search location beats an earlier one.

**Resource files** are everything else, including XSL, images, and YAML that isn't a property source. For each request:

1. Choose the whole file: `<name>-<tenant>.<ext>` if it exists, otherwise `<name>.<ext>`. Tenant files are full documents, never merged with base.
2. If the request names a channel, the copy in `<folder>/<channel>/` wins.
3. Replace each `${KEY}` whose key exists in the property view with that value. Leave any other `${...}` exactly as written; the service resolves it later from its own environment.

**Search locations** are `<root>/{application}`, `<root>/{application}/{profile}`, and every directory except channel directories (those named in `channels.yml`). The config-server computes them once, at startup. Two consequences:

- A new folder, or a change to `channels.yml`, isn't served until the config-server restarts. That's check C11.
- File names effectively share one namespace, so the same name in two non-channel folders is ambiguous. That's check C9.

See `references/worked-examples.md` for the config-server's own fixture (`CORE_ROUTING`) and real repo examples. Port them into golden tests.

## 3. Drift (D19–D20)

Each NFS path has three hashes:

- **B:** the baseline hash.
- **N:** the current NFS hash.
- **G:** the current Git hash, found through reverse mapping. Base files come from the base default branch head; tenant files come from that tenant's branch head.

Normalise line endings before comparing `structured` and `text` files. Treat a missing file as the hash `∅`. Check for `untracked` first: if N is present, G is `∅` and there's no baseline, the file is untracked. Otherwise:

| Condition | State |
|---|---|
| No baseline, N = G | `in_sync` (set B = N) |
| No baseline, N ≠ G | `unknown` |
| N = B, G = B | `in_sync` |
| N = B, G ≠ B | `git_ahead` |
| N ≠ B, G = B | `nfs_ahead` |
| N ≠ B, G ≠ B, N = G | `in_sync` (set B = N) |
| N ≠ B, G ≠ B, N ≠ G | `conflict` |

`intentional_divergence` overrides the non-sync states only while both N and G still equal the hashes recorded when someone marked it.

## 4. When a change takes effect (D85)

Compute this per change and per consuming service. Each Deployment's settings come from its environment: `CONFIG_CLIENT_CACHE_TTL` (default 20 minutes) and `CONFIG_CLIENT_MONITOR_ACTIVEMQ_ENABLED`.

| Change | State |
|---|---|
| Resource file | `live_within_ttl` until the client cache expires or a notification arrives |
| Property source, client with notifications enabled | `needs_notify_or_restart`; a notification refreshes the Spring context |
| Property source, client without notifications | `needs_notify_or_restart`, where only a restart helps |
| New folder or `channels.yml` change | `needs_config_server_restart` |

Never show a bare "pending restart". It was the old model, and it was wrong.

## 5. Checks quick reference

| Id | What it flags | Real example |
|---|---|---|
| C1 | A tenant copy is missing base changes made since the copy (whole-file resources). For property sources, a tenant setting overriding something base no longer has. | sit1 `entryGroupConfig.yml` has no `atm` entry |
| C2 | A tenant file identical to base (semantically for structured files, byte-equal otherwise) | `account-sorting-config.yml`, `miniStatementConfig.yml`, `receipt-ci_1.bmp` |
| C3 | Tenant files exist for some tenants but not others | — |
| C4 | Orphans: a suffix that isn't in the swimlane's tenant set, or an untracked file | — |
| C5 | Drift: any state other than in sync or intentional | — |
| C6 | An external host from the wrong environment tier. Cluster-local single-label names are excluded. | sit1 points at a dev video host |
| C7 | A sync overwrote an NFS change (`nfs_ahead` or `conflict`) | — |
| C8 | Duplicate YAML keys; the last one wins | `security-roles.yml`: 3 keys |
| C9 | The same file name in more than one non-channel folder | `authentication-config.yaml` in 12 core-adapter folders |
| C10 | A placeholder that's neither in the property view nor an environment variable name on any consumer | — |
| C11 | Config-server restart needed: a folder created after it started, a `channels.yml` change, or a channel folder and channel list that disagree | — |

## 6. Mistakes that have bitten this design before

- **Treating tenant resource files as key-merged.** Only property sources merge setting by setting.
- **Treating property sources as whole-file.** They merge setting by setting.
- **Resolving every `${...}`.** Only keys present in the property view are substituted. Never use environment values for this.
- **Assuming the suffix is "the deployed branch".** It's the tenant id, and a swimlane has a set of tenants.
- **Forgetting that channel folders aren't search locations.** They're reached only through a channel request.
- **Comparing files without normalising line endings,** or writing them back without restoring the original style. Real files are CRLF.
- **Equating `yes`/`on` with `true`.** Flag them, because YAML 1.1 and 1.2 disagree.
- **Inventing facts in an AI layer.** Every fact comes from the engine (D33).

## 7. Testing expectations

- **Golden fixtures** ported from the config-server repo must match byte for byte, after line-ending normalisation.
- **Synthetic fixtures** come from `cargo xtask gen-fixtures`. Never commit real tenant config.
- **The opt-in real-snapshot test** reads repo paths from environment variables. It must reproduce the examples in the table above, plus the 13 ambiguous names for C9.
