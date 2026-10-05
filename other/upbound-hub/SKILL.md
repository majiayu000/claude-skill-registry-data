---
name: upbound-hub
description: Query and mutate Upbound Hub, the central API for an Upbound Platform deployment, which gives one cross-fleet view of control planes, spaces, realms, types, packages, resources, identity providers, and the image catalog. Use when asked about fleet-wide state ("how many resources are unhealthy", "list control planes", "what types are deployed across the fleet", "show resources in <control plane>"), or to create, update, or delete Hub objects. Not for a single control plane's own API server, and not for Crossplane resources managed inside one.
license: Apache-2.0
---

# Upbound Hub

Hub is the central cluster in an Upbound Platform deployment. It provides the
authentication, storage, and APIs that Upbound's fleet products build on, and it serves a
synthesized view assembled from every connected control plane.

Treat it as an aggregator, not as a cluster's own apiserver. It looks like Kubernetes and
mostly behaves like it, and the places it does not are where wrong answers come from.

**The API surface differs by Hub major, so do not pin a group.** Hub 1.0.x served
almost everything from `hub.upbound.io`. Hub 1.1.0 split it:

| Resources | 1.0.x | 1.1.0 |
|---|---|---|
| `resources`, `resourcestats`, `lenses`, `typedefinitions`, `crossplanepackages`, `resourcerelationships`, `resourcerelationshiptrees` | `hub.upbound.io` | `inventory.hub.upbound.io` |
| `controlplanes`, `spaces`, `controlplaneregistrations`, `spaceregistrations` | `hub.upbound.io` | `fleet.hub.upbound.io` |
| `realms` | `hub.upbound.io` | `hub.upbound.io` (unchanged) |
| `identityproviders`, `users`, `groups` | `authentication.hub.upbound.io` | `iam.hub.upbound.io` |
| `organizationrolebindings`, `realmrolebindings`, `selfsubjectaccessreviews` | `authorization.hub.upbound.io` | `iam.hub.upbound.io` |

`realms` is why this is not a rename: `hub.upbound.io` still exists on 1.1.0 and
still serves it, so a blanket find-and-replace breaks a working call.

`scripts/hub-list` and `scripts/hub-stats` resolve both group and version from
`/apis` at runtime and work against either major. When writing a path by hand,
check first:

```bash
scripts/hub-curl /apis | jq -r '.groups[].name'
```

Within a group, v1beta1 is served everywhere; the v1alpha1 `Resource` and
`ResourceStats` types are deprecated.

## Setup

Every script path in this skill is relative to **the directory containing this file**, not
to your working directory — your working directory is the user's project. Resolve each one
against this skill's own directory before running it.

**Do this yourself. Do not hand the user a list of commands to run.** Start every session
with:

```bash
scripts/hub-setup
```

That one call installs the credential helper, checks it against a published SHA-256, signs
in if needed, and reports what it did. Act on the exit code:

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Ready | Continue with the user's question. |
| 1 | Something went wrong | The message says what. Relay it. |
| 3 | No endpoint configured | Ask the user for their Hub API endpoint, then run `scripts/hub-setup --url <url>`. It is saved, so this happens once per machine. |

Asking for the endpoint is the only thing you need the user for, and only the first time.
If sign-in is required, `hub-setup` opens a browser — tell the user to complete it there,
then carry on. The credential lasts around 90 days.

The endpoint is stored in `${XDG_CONFIG_HOME:-~/.config}/upbound/hub.env`. Setting
`HUB_API_URL` in the environment overrides it for a one-off against another deployment.

On a Hub that serves multiple organizations, set `HUB_ORG` to the organization to
authenticate against. The credential helper reads it from the environment, so
`hub-setup` and every other script pick it up and scope the token to that
organization. Leave it unset for a single-organization Hub, which is the default.

`HUB_CA_FILE` points at a PEM bundle when the system trust store does not include Hub's CA.
Do not set `HUB_INSECURE=1`; it disables TLS verification. Set it only if the user asks for
it by name.

Confirm it works:

```bash
scripts/hub-curl /apis | jq '.groups[].name'
```

## Scripts

Prefer these over hand-rolled curl. They handle auth, pagination, and the quirks.

| Script | What it does |
|---|---|
| `scripts/hub-setup [--url <url>]` | Saves the endpoint, installs the credential helper, signs in. Run first. |
| `scripts/hub-common.sh` | Shared helpers the others source. Not run directly. |
| `scripts/hub-curl <path>` | Authenticated curl. Path must start with `/`. |
| `scripts/hub-list <resource> [pageSize] [key=value...]` | Pages a resource into one JSON array. Exits **4** if the result was truncated. |
| `scripts/hub-stats [groupBy...] [-- filter...]` | Aggregate counts. **Use this for every "how many" question.** |
| `scripts/hub-types [group-suffix]` | The type catalog as a table. |
| `scripts/hub-health` | Fleet-wide rollup as JSON, with honest denominators. |
| `scripts/hub-resources-by-cp <cp> [realm] [--unhealthy]` | Resources in one control plane, with health and reason. |
| `scripts/hub-kubectl <args...>` | kubectl against Hub. The write path only — see below. |

## Reference

- [api-surface.md](references/api-surface.md) — read when you need the exact resource,
  group, version, scope, or verbs. Also has the error taxonomy.
- [querying.md](references/querying.md) — read before any query that filters, paginates, or
  counts. Has the CEL filter fields and what health actually means.
- [writing.md](references/writing.md) — read before creating, updating, or deleting
  anything. Has the permission check and the manifests.
- [recipes.md](references/recipes.md) — worked answers to the questions that come up most.

## Four things that cause wrong answers

**Counting by paging.** `metadata.total.count` saturates at 1000, and past that
`relation` is `gt` with no magnitude. A paged count is a lower bound. Use
`scripts/hub-stats`, which returns a real aggregate.

**Reporting health against the wrong denominator.** Most records carry no conditions at
all, and `Unknown` is not the same as failing. Give three numbers: assessable, explicitly
failing, and not reporting. Never divide by the total.

**Reading through kubectl.** Hub implements no `limit`/`continue`, so `hub-kubectl get` on
a collection silently returns one page as if it were the whole list. Read with
`scripts/hub-list`.

**Assuming the view is current.** Hub is eventually consistent. Something created or
deleted seconds ago may not be there yet. Only `resources` records carry `hub.lastSyncTime`;
check it against the clock before saying one does not exist. Do not derive freshness from
`hub.syncLagSeconds` instead — it has been seen reading 0 on every record of a live
deployment, including records months out of date, which is a reported defect. Comparing
`lastSyncTime` against the clock is correct either way. Freshness is per record, so one
timestamp says nothing about the fleet's. Control
planes, spaces and realms carry no freshness field at all, so for those say the view may be
stale instead of implying it is current.

## Anti-patterns

- **Do not discover permissions by attempting the operation.** Hub serves
  `selfsubjectaccessreviews` — ask it. Attempting a `delete` to see whether you may is
  destructive. See [writing.md](references/writing.md).
- **Do not use `kubectl apply` on an object that already exists.** There is no `patch`
  verb, so it returns 405. Use `replace`.
- **Do not treat `crossplanepackages` as installed packages.** It is Hub's catalog.
  Packages installed in a control plane live in that control plane's own apiserver.
- **Do not sum `summary.resourceCount` across `typedefinitions` for a fleet total.** It
  disagrees with `resourcestats`, partly because composition fans one logical resource out
  into several records. Report both rather than picking one.
- **Do not count `Unknown` as unhealthy.** `Ready=Unknown` is the normal state while a
  managed resource is being created, and `Synced=False` with reason `ReconcilePaused` means
  someone paused it deliberately.
- **Do not write to `ingest.hub.upbound.io/resourceevents` or `controlplanes/{name}/jwks`.**
  Both are the connector's paths. Writing to the second breaks a control plane's
  authentication to Hub.
- **Do not report realm or package health.** Hub exposes none. Say so rather than inferring.
- **Deleting a realm is not reversible and is not an editing technique.** A realm is a
  namespace containing control planes, and recreating it re-grants realm-admin to whoever
  ran the command. Enumerate what it holds, tell the user, and get agreement first.
- **Never echo a registration token.** Minting one returns a join credential. Extract the
  field; do not put the response in a transcript, a log, or a file the user did not ask for.
