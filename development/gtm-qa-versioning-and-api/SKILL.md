---
name: gtm-qa-versioning-and-api
description: Version, preview, debug, and programmatically manage a Google Tag Manager container through workspaces, versions, environments, and the Tag Manager API v2. Use when the user asks about GTM workspaces, the 3-workspace limit, workspace sync and conflict resolution, container versions, publishing, the Live and Latest environments, custom environments, quick preview and share preview, preview and debug mode tabs, promoting changes dev to QA to prod, the Tag Manager API v2, tagmanager scopes, API quotas or 403 rate-limit errors, bulk_update, create_version, or automating container edits and audits in code.
---

# GTM QA, versioning, and API

Govern how changes move through a Google Tag Manager (GTM) container: build in a workspace, verify in preview and debug, cut a version, publish through environments, and do all of it in bulk through the Tag Manager API v2 when the container is too large or too numerous to click through. This is the change-management and automation layer that sits on top of the tags themselves. Get it right and every publish is reviewable, reversible, and reproducible. Get it wrong and someone overwrites a colleague's work, ships an unverified tag to production, or burns the daily API quota on the first sync.

This skill assumes you know what a container, tag, trigger, and variable are. For building the GA4, Google Ads, and Floodlight tags inside the workspace, see the `gtm-tags-triggers-variables` skill. For the dataLayer contract those tags read, see `gtm-web-container-and-datalayer`. For standing up and previewing a server-side (tagging server) container, see `gtm-server-side-tagging`. For consent signals and the June 2026 ads-data gating, see `gtm-consent-mode-v2`.

## When to use this skill

- "Set up workspaces for our team." / "Why can I only make 3 workspaces?" / "We need more than 3."
- "My workspace is out of date / has a conflict after someone published. How do I sync?"
- "Create a version and publish it." / "Roll back to a previous version." / "What is set as latest vs publish?"
- "Set up Dev, QA, and Live environments." / "Promote this version from staging to production."
- "Preview a change / share a preview link with a colleague or client."
- "Walk me through the preview and debug tabs. Why did a tag not fire?"
- "Automate GTM: create or update tags in bulk, audit every container, export the whole config."
- "How do I authenticate to the Tag Manager API?" / "Which OAuth scope do I need?"
- "I am getting HTTP 403 from the API." / "What are the API quotas / rate limits?"

Boundaries with sibling skills:
- Building the actual tags, triggers, and variables: `gtm-tags-triggers-variables`.
- Container snippet install and the dataLayer schema: `gtm-web-container-and-datalayer`.
- Server container infrastructure, clients, and transport: `gtm-server-side-tagging`.
- Consent Mode v2 signals and jurisdiction defaults: `gtm-consent-mode-v2`.
- Broader legal picture of consent and data rights: `privacy-and-consent`.

## Quick reference

| You want to | Do this | Why |
| --- | --- | --- |
| Let two people edit safely at once | Give each their own workspace | Edits stay isolated until versioned |
| More than 3 concurrent workspaces | Upgrade to Tag Manager 360 | Standard caps at 3 (1 default + 2 custom) |
| Your workspace is behind after a publish | Sync the workspace, resolve conflicts | Rebases your edits on the new base version |
| Snapshot the current edits | Create a version | A version is an immutable, publishable snapshot |
| Go live | Publish the version to the Live environment | Live always points at the currently published version |
| Test on a staging site | Publish the version to a custom environment | Custom environments get their own snippet and URL |
| Prepare a version without going live | Set version as latest | Sets the base for workspace sync without publishing |
| Show a colleague or client a change | Share preview link (no snippet needed) | Preview without touching any environment |
| Diagnose why a tag did or did not fire | Enter preview, read Tags and Console tabs | Shows fired vs not-fired and the error text |
| Edit or audit at scale, or in CI | Tag Manager API v2 | Bulk read/write, no clicking |

Golden order for any change: **workspace, preview, version, publish**. Never skip preview, and never publish straight from an unverified workspace.

## Core process

### A. Move a change through the container (UI or API, same model)

1. Open or create a workspace, because isolated edits keep one person's work-in-progress from landing in someone else's version. Standard containers allow at most 3 concurrent workspaces (one auto-created default plus two custom); Tag Manager 360 allows an unlimited number.
2. Make the tag, trigger, and variable changes in that workspace (hand off the actual tag build to `gtm-tags-triggers-variables`). Nothing you do is live yet; the workspace is a private set of changes on top of a base container version.
3. Preview the workspace before anything else, because preview is the only place you confirm a tag fires on the right event with the right values before it reaches a user. Use quick preview for a fast look or share preview to send a link to a reviewer.
4. If someone else published while you were working, your workspace base is now stale. Sync the workspace to the latest version, then resolve any conflict entity by entity (see Decision rules) so you rebase your edits instead of clobbering theirs.
5. Create a version from the workspace once preview is clean. A version is an immutable, numbered snapshot of the whole container (tags, triggers, variables, folders, built-in variables, templates, clients, Google tag configs, transformations, zones). Creating a version deletes the workspace and sets the new version as the base for other workspaces to sync against.
6. Publish the version to the target environment. Publish to Live to go to production; publish to a custom environment (Dev, QA, staging) to test on a non-production site first. Publishing is a human-gated action: confirm the diff and the environment before you click or call the API.
7. To roll back, publish an earlier version to the affected environment. Versions are immutable and retained, so rollback is a re-publish, not an edit.

### B. Promote through environments (dev to QA to prod)

1. Keep Live for production only. The Live environment is built in and always points at the currently published version; you cannot repurpose it.
2. Use the Latest environment (also built in) as the preview target for workspace changes, and stand up custom environments (for example Dev and QA) for each non-production site, because each environment gets its own snippet or server URL and its own published version.
3. Install the correct environment snippet on each site (grab it from the container Admin, per environment) or, for a server container, point that environment at its own tagging server URL.
4. Promote by publishing the same version to the next environment up the chain. Verify in Dev, publish that exact version to QA, verify, then publish it to Live. Promoting the same version number (not re-cutting) is what makes staging a true rehearsal of production.
5. For a review-gated flow, use 360 workspace approvals or an out-of-band change ticket before the Live publish, because standard GTM has no built-in approval gate.

### C. Automate with the Tag Manager API v2

1. Authenticate with OAuth 2.0 (user or service account) and request the narrowest scope that covers the job (scope table below). Read audits need only `tagmanager.readonly`; publishing needs `tagmanager.publish`. Credentials come from an environment variable or a user-supplied key path, never hardcoded.
2. Walk the resource hierarchy top down: account, container, then either a version (read published or historical config) or a workspace (make changes). Editing always happens inside a workspace resource, exactly like the UI.
3. Read before you write. List and get the current entities so your automation diffs against real state instead of assuming it.
4. Batch writes with `bulk_update` (applies multiple entity changes to a workspace in one call) instead of one request per entity, because the project rate limit is low (see quotas) and per-entity calls will 403 fast.
5. Cut and publish through the API the same way the UI does: `create_version` on the workspace, then `publish` on the resulting version, then optionally point an environment at it. Keep publish behind a human gate in any pipeline.
6. Handle quota. The daily and per-second limits are per project. On HTTP 403, back off and retry inside a 100-second sliding window rather than hammering the endpoint.

## Decision rules and thresholds

### Workspace limits and when to upgrade

- Standard (free) GTM caps a container at 3 concurrent workspaces: the default workspace plus 2 custom. Hit that ceiling and you must version or discard a workspace before opening another, or move to Tag Manager 360 for unlimited workspaces. If a team of five keeps colliding on 3 workspaces, that friction is the buying signal for 360, not a reason to share one workspace.
- One change stream per workspace. Do not batch unrelated changes into a single workspace; it makes the version diff unreviewable and rollback coarse.

### Sync and conflict resolution

When another workspace publishes, your base version is stale and you must sync. GTM classifies each entity by how it differs from the new base, shown by color in the UI:

| Color | Meaning | Default action |
| --- | --- | --- |
| Blue | Modified in both your workspace and the synced version | You choose which to keep, entity by entity |
| Red | Changed in the synced version, not in your workspace | Take the synced change unless you have a reason not to |
| Green | Changed in your workspace, not in the synced version | Keep your change |

Rule: resolve blue conflicts deliberately, one entity at a time. On publish, any synced change you chose to ignore is overwritten by your workspace's version of that entity, so an ignored red conflict silently reverts someone else's fix. Read the diff before you publish.

### Version and publish semantics

- Create a version to snapshot; publish to make a version live. These are separate. You can create a version and not publish it.
- "Set as latest" sets the base version other workspaces sync against, without publishing. Use it to stage a known-good version as the sync target without pushing it to production.
- Publishing is the only action that changes what real users load. Treat every publish to Live as a production deploy: preview first, confirm the environment, keep the previous version for rollback.
- Rollback is re-publishing a prior version. Because versions are immutable snapshots, this is safe and does not lose the newer version's history.

### API scopes: least privilege

Grant only the scope the task needs.

| Task | Scope |
| --- | --- |
| Read-only audit / export | `https://www.googleapis.com/auth/tagmanager.readonly` |
| Edit tags, triggers, variables in a workspace | `https://www.googleapis.com/auth/tagmanager.edit.containers` |
| Create and manage container versions | `https://www.googleapis.com/auth/tagmanager.edit.containerversions` |
| Publish a version | `https://www.googleapis.com/auth/tagmanager.publish` |
| Manage accounts and containers | `https://www.googleapis.com/auth/tagmanager.manage.accounts` |
| Manage user permissions | `https://www.googleapis.com/auth/tagmanager.manage.users` |
| Delete containers | `https://www.googleapis.com/auth/tagmanager.delete.containers` |

A CI audit job should hold `tagmanager.readonly` only. A deploy job needs edit + containerversions + publish, and its publish step should be human-approved.

### API quotas and 403 handling

- Daily limit: 10,000 requests per project per day.
- Rate limit: 0.25 queries per second per project, enforced on a 100-second sliding window (25 requests per 100 seconds).
- Over quota returns HTTP 403 Forbidden. Do not retry immediately; back off and stay under 25 requests per 100 seconds.
- Because limits are per project (not per user or per container), a single noisy script starves every other job on the same Cloud project. Batch with `bulk_update`, cache reads, and give heavy automation its own project if you can apply for a higher quota.

## Reference material

- `references/workspaces-versions-environments.md`: the full change-management model. Workspace limits by tier, the default-workspace lifecycle, version immutability and retention, set-as-latest vs publish, the built-in Live and Latest environments vs custom environments, environment snippets and URLs, and a promotion runbook for dev to QA to prod. Read this when designing a team's GTM change process or setting up environments.
- `references/preview-and-debug-tabs.md`: what each preview and debug tab shows and how to read it. Quick preview vs share preview, the web Tag Assistant flow, and the server container debugger tabs (Request, Tags, Variables, Event Data, Console) with a decision tree for "why did this tag not fire". Read this when a tag misbehaves in preview or you are teaching someone to debug.
- `references/api-v2-resources-and-quotas.md`: the Tag Manager API v2 field map. Full resource hierarchy, every workspace and version method (including `bulk_update`, `getStatus`, `sync`, `resolve_conflict`, `create_version`, `set_latest`, `live`, `publish`), the OAuth scope table, exact quota numbers, and worked request sequences for audit-export and bulk-edit. Read this when writing code against the API.

## Templates and examples

- Two-person team, standard GTM: person A works in the default workspace, person B in a custom workspace. B previews, versions, publishes. A now sees a stale base, syncs, resolves one blue conflict on the GA4 config tag (keeps A's field change, takes B's trigger change), previews, versions, publishes. Three workspaces max is enough for two editors.
- Staging rehearsal: cut version 47 in a workspace, publish 47 to the QA environment (QA snippet on staging.example.com), verify GA4 purchase fires once and Google Ads conversion dedupes, then publish that same version 47 to Live. Same version, so production is exactly what QA saw.
- Rollback: a bad Floodlight tag ships in version 51 and doubles counts. Publish version 50 to Live to roll back immediately, then open a workspace to fix the tag properly and cut version 52. No edits to 51; it stays in history.
- Nightly audit job: a service account with `tagmanager.readonly` lists all containers, gets the live version of each, and flags any tag firing without a consent check or any container over 90% of an entity budget. Read-only scope, well under 10,000 requests, batched.
- Bulk rename in code: open a workspace, list all variables, build one `bulk_update` payload renaming the 40 legacy variables, apply it in a single call, `create_version`, then leave publish to a human-approved step. One write call instead of 40 keeps you off the 403 line.

## Common pitfalls

- Sharing one workspace across a team. Two people editing the same workspace overwrite each other with no diff. Give each editor their own workspace; that is the entire point of workspaces.
- Publishing straight from an unverified workspace. If you never previewed, you do not know the tag fires correctly. Preview is not optional; it is the gate before every version.
- Ignoring a red conflict on sync. On publish, ignored synced changes are overwritten, so ignoring a red conflict silently reverts a colleague's already-live fix. Read every conflict before publishing.
- Confusing set-as-latest with publish. Set-as-latest changes the sync base only; it does not change what users load. Only publish does. People assume "latest" means "live" and ship nothing.
- Re-cutting a version between environments. If you edit and re-version between QA and Live, QA never tested what production gets. Promote the same version number up the chain.
- Treating the API rate limit as per-user. It is per project. Fanning out per-entity writes across users still shares one 0.25 QPS budget and will 403. Use `bulk_update` and back off.
- Requesting `tagmanager.publish` for a read job. Over-scoped credentials are a security and blast-radius problem. A read audit needs `tagmanager.readonly` and nothing more.
- Hardcoding the service-account key. Load credentials from an environment variable or a path the user supplies. Never commit a key.

## Sources

- [Workspaces (GTM Help)](https://support.google.com/tagmanager/answer/7059647?hl=en) (as of July 2026)
- [Environments (GTM Help)](https://support.google.com/tagmanager/answer/6311518?hl=en) (as of July 2026)
- [Publish preview and debug a container version (GTM Help)](https://support.google.com/tagmanager/answer/4620708?hl=en) (as of July 2026)
- [Tag Manager API v2 overview](https://developers.google.com/tag-platform/tag-manager/api/v2) (as of July 2026)
- [Tag Manager API limits and quotas](https://developers.google.com/tag-platform/tag-manager/api/v2/limits-quotas) (as of July 2026)
- [accounts.containers.workspaces REST reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest/v2/accounts.containers.workspaces) (as of July 2026)
- [accounts.containers.versions REST reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest/v2/accounts.containers.versions) (as of July 2026)
- [Server-side preview and debug](https://developers.google.com/tag-platform/tag-manager/server-side/debug) (as of July 2026)
