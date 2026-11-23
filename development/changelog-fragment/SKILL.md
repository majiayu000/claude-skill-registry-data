---
name: changelog-fragment
description: Add a changelog fragment (one-line YAML file under .changelog/unreleased/) for a user-visible change, or merge it into an existing unreleased one when appropriate, using Changie (changie.dev). Use when the user asks to add a changelog entry, add a changelog fragment, document a change for the release notes, or run `changie new` — and proactively before opening a PR that changes user-visible behavior, so the Changelog Fragment Check doesn't block it.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: documentation
  since: "2026-11-10"
---

# Changelog Fragment

Record a change for the release notes as a small YAML file instead of hand-editing a shared `CHANGELOG.md`. Each PR that changes user-visible behavior drops its own fragment under `.changelog/unreleased/`; each release batches them into `.changelog/<version>.md`. This avoids merge conflicts on a single changelog file and keeps the changelog entry in the same PR (and review) as the code change it describes.

Config lives at repo root: [`.changie.yaml`](../../.changie.yaml). Fragments are checked by `.github/scripts/changelog-check.sh` (workflow `changelog-check.yaml`) on every PR that touches package source code, and batched into `.changelog/<version>.md` by `changelog-batch.yaml` when `cd-release.yaml` publishes a release. These release notes complement, not replace, the per-package `CHANGELOG.md` files that release-please generates from commit subjects (see "When a fragment is not needed" below).

## Check unreleased fragments first

Before creating a fragment, read every `*.yaml` file under `.changelog/unreleased/`. A fragment matches the change being documented now only when it describes the same user-visible change — not merely the same `component`. Valid match signals: a shared feature flag name, config key, API field, or the same behavior being corrected. A shared `UN-*` ticket is supporting evidence only, never proof by itself; same `component` alone is never a match.

Never match `Security` fragments or dependency-bump fragments — those always stay separate, standalone fragments.

If nothing matches, skip ahead to "Create a fragment" below, unchanged. A fix to behavior that already shipped in a previous release, with no unreleased fragment currently describing it, is still a new `Fixed` fragment, not a merge.

## Merge matched fragments into a new one

When one or more existing fragments do match, run `./.github/scripts/changelog-fragment-guard.sh <every-matched-fragment-path>` before deleting anything — pass every matched path in one call, since the script fetches release refs once for the whole batch rather than once per file. Called bare, with no `--base-ref`, the script assumes the change targets `main` (the normal case). Pass `--base-ref <ref>` explicitly only when that assumption is wrong — e.g. a PR already exists targeting something else, or you're backporting on a `release/*` branch.

If it exits non-zero, don't touch any of the matched fragments. Fall back to creating a plain new fragment for just this PR's change via `changie new`, same as the "nothing matches" case above — the reason is already in the script's stderr output if a human needs an explanation.

If it exits `0`, work out the net-correct `body`/`kind`/`custom.Ticket` across all matched fragments plus this new change — absorb every correction into one client-facing sentence, don't concatenate multiple sentences describing bugs a customer never actually saw in a release.

If that net-correct body would say exactly what one of the matched fragments already says, with nothing new to add (no behavior change, no new ticket), skip the whole merge — leave that fragment alone and don't create or delete anything. There's no release-note effect to record.

Otherwise, decide first whether the net change's category genuinely changed — e.g. the addition was fully reverted before release — or whether it's still the same kind of change as before (e.g. an `Added` feature whose behavior got tweaked before release is still `Added` overall).

If it's a full revert: don't create a replacement fragment at all. Delete the old fragment(s) and apply the `no-changelog` label if the PR then has no remaining user-visible effect. Stop here — nothing below in this section applies.

Otherwise, create exactly one new fragment via `changie new` with the net-correct content, then delete every matched fragment file — never rename one, and never treat this as an edit to an existing file; the operation is always "delete these, add that one." Set `kind` to the net category decided above: the earliest matched fragment's `kind` when that category is unchanged, or the new category when it genuinely changed. Union every `UN-*` ticket id from all matched fragments into the new one's `custom.Ticket`, deduplicated, comma-separated (e.g. `UN-12345, UN-6789`).

## Create a fragment

Install [changie](https://changie.dev/guide/installation/) (`brew install changie`, or prefix commands with `npx -y changie@1.26.0`; CI pins `v1.26.0`). Run non-interactively (this is the required mode for an agent — no TTY prompts):

```bash
changie new --interactive=false --kind Fixed --body "Short, client-facing description of the fix." --component Toolkit --custom Audience=developer --custom Ticket=UN-12345
```

- `--interactive=false` — always pass it; otherwise changie prompts for every unset optional field (e.g. `Ticket`).
- `--kind` — one value, see allowed kinds below.
- `--body` — the client-facing description (see wording rules below).
- `--component` — one value, see allowed components below.
- `--custom Key=Value` — repeat once per custom field; `Audience` is required, `Ticket` is optional.

Run `changie new` with no flags to be prompted interactively — that mode is for humans only.

This writes a new file to `.changelog/unreleased/`. Double-check the diff before finishing — the file should contain exactly `component`, `kind`, `body`, `time`, `custom.Audience`, and optionally `custom.Ticket`, matching the fields passed above.

## Allowed values (from `.changie.yaml`)

- `--kind`: `Added`, `Changed`, `Fixed`, `Removed`, `Security`
- `--component` (drives the `### {{.Component}}` heading): `Connectors` (`connectors/*`), `Deep Research` (`tool_packages/unique_deep_research`), `MCP` (`unique_mcp`), `Orchestrator` (`unique_orchestrator`), `Postprocessors` (`postprocessors/*`), `RAG` (`tool_packages/unique_internal_search` and retrieval changes in `unique_toolkit`), `SDK` (`unique_sdk`), `Tools` (other `tool_packages/*`, e.g. SWOT, skill tool), `Toolkit` (`unique_toolkit`, except retrieval), `uqadm` (`uqadm`), `Web Search` (`tool_packages/unique_web_search`). Component names match the monorepo's where the area is the same (`RAG`, `Web Search`, `MCP`, `Connectors`), so combined notes read consistently.
- `Audience`: `developer` (builds on the SDK, toolkit or packages), `user` (end-user visible behavior), `admin`, `operator` (deploys or runs a service, e.g. the search proxy Helm chart)
- `Ticket` (optional): related Jira ticket(s), each matching `UN-<number>` (e.g. `UN-12345`); comma-separate multiple, e.g. `UN-12345, UN-6789`. Omit entirely if there's no ticket — nothing changes in the rendered line. It is never rendered; it only stays in the archived `.changelog/<version>/*.yaml` files for internal traceability, and no tooling reads it.

## Body wording

Standalone Jira ticket references must never go in `body` or otherwise appear in the public release notes (`.changelog/<version>.md`). Jira IDs that are part of real feature flag or configuration names must remain intact because clients need the exact identifier. If useful for internal traceability, put standalone ticket references in `custom.Ticket`; this metadata is not rendered into release notes.

Write `--body` the way a release note reads: concise, present-tense, client-facing, no internal nomenclature. Never restate the `kind` or component inside the body. `changeFormat` in `.changie.yaml` renders `- AUDIENCE_{{.Custom.Audience | upper}}: {{.Body}}`, producing the double-click-selectable prefixes `AUDIENCE_DEVELOPER`, `AUDIENCE_USER`, `AUDIENCE_ADMIN`, and `AUDIENCE_OPERATOR`. The component and kind still show up once each as the `### {{.Component}}` and nested `#### {{.Kind}}` headings above every group of entries in `.changelog/<version>.md` — so a body starting with `FIXED: Chat: ...` would duplicate what's already shown by the surrounding headings.

Describe the observable result directly. Do not use generic phrases such as "the problem with ... now works as intended", "fixed an issue where", or "resolved a problem with". For a `Fixed` kind, state what users see or what the system does now:

```
Concurrent requests now display each citation only once.
```

For `Added`/`Changed`/`Removed`/`Security`, keep the same tone: short, present-tense, describing the user-visible effect only.

Vulnerability patches (`Security`, or dependency bumps that close advisories): never name the closed package versions, CVE/GHSA IDs, or the versions that were vulnerable. State that vulnerabilities were patched, or how many. Name the surface if it helps (image, service, dependency class) — not the advisory.

```
Sandbox egress gateway image patches two published container vulnerabilities.
```

```
Search proxy image patches published CRITICAL and HIGH container vulnerabilities.
```

## Operational details the body must capture

A client-friendly sentence alone is not enough — release notes readers need to know how to actually turn the change on. Before finalizing `--body`, check:

- Name any feature flag or env var that gates the change, preserving its exact identifier, and state whether it's on or off by default.
- Name any additional config required beyond the flag — a company config key, a per-space setting, an API-only field, a Helm value. Never say "opt-in" without saying how.
- Call out required manual activation steps explicitly (e.g. "must be requested", "API-only, not available in the UI").
- If the change silently alters behavior for users who didn't opt in, add an explicit `Behavior change:` callout as a new paragraph. Use `body: >-` and put a blank line before the callout so the rendered release note preserves the separation.
- For a large feature that needs more explanation than a body can hold, link out to a Confluence page instead of over-explaining inline.

## When a fragment is not needed

`.github/scripts/changelog-check.sh` skips PRs whose changed files only match `EXCLUDED_GLOBS` (Markdown, `.github/**`, `.claude/**`, `.cursor/**`, `docs/**`, `tutorials/**`, tests, `uv.lock`) and skips any PR carrying one of the `EXEMPTION_LABELS`: `no-changelog`, `autorelease: pending` (release-please Release PRs), `dev-version-bump` (dev-cut pin PRs) or `dependencies` (Dependabot). Apply `no-changelog` for docs-only changes or pure refactors with no user-visible effect — don't create a fragment just to satisfy the check. If a dependency bump closes a vulnerability that matters to consumers, add a `Security` fragment by hand.

Before pushing, verify locally:

```bash
./.github/scripts/changelog-check.sh
```

This diffs the current `HEAD` against the merge-base with `origin/main` and reports whether a fragment (or exemption) is present.

## Examples

`time` is omitted below for brevity — `changie new` generates it.

Plain fix, no flag involved:

```yaml
component: Toolkit
kind: Fixed
body: Concurrent requests now display each citation only once.
custom:
  Audience: user
```

With a single Jira ticket (`--custom Ticket=UN-12345`):

```yaml
component: Toolkit
kind: Fixed
body: Concurrent requests now display each citation only once.
custom:
  Audience: user
  Ticket: UN-12345
```

With multiple tickets — changie CSV-splits `--custom`, so wrap the whole `Key=Value` pair in double quotes inside single quotes (`--custom '"Ticket=UN-12345, UN-6789"'`):

```yaml
component: Toolkit
kind: Fixed
body: Concurrent requests now display each citation only once.
custom:
  Audience: user
  Ticket: UN-12345, UN-6789
```

Flag-gated addition, disabled by default, only the flag matters:

```yaml
component: Toolkit
kind: Added
body: >-
  Inline document previews in chat. Disabled by default; enable via
  `FEATURE_FLAG_ENABLE_INLINE_DOCUMENT_PREVIEW`.
custom:
  Audience: user
```

Flag-gated addition that also requires config beyond the flag:

```yaml
component: Toolkit
kind: Added
body: >-
  Cross-space search. Disabled by default. Enabling it requires both the
  feature flag `FEATURE_FLAG_ENABLE_CROSS_SPACE_SEARCH` and a company search
  scope set via the `searchScopePolicy` company configuration (`spaceMembers`
  or `allCompany`).
custom:
  Audience: admin
```

API-only config, no feature flag at all:

```yaml
component: Toolkit
kind: Added
body: >-
  Custom retention windows per Knowledge Base folder. Off by default and can
  only be enabled via API. Enable it with `retentionConfig.customWindowDays`
  in the folder ingestion config; not available in the UI.
custom:
  Audience: operator
```

Vulnerability patch — count only, no versions or advisory IDs:

```yaml
component: Connectors
kind: Security
body: Search proxy image patches two published container vulnerabilities.
custom:
  Audience: operator
  Ticket: UN-25502
```

A follow-up PR corrects a feature before release. Delete the existing fragment:

```yaml
component: Tools
kind: Added
body: >-
  Automatic meeting summaries. Disabled by default; enable via
  `FEATURE_FLAG_ENABLE_MEETING_SUMMARIES`.
custom:
  Audience: user
  Ticket: UN-30001
```

Add one merged fragment describing the net behavior instead, unioning both tickets:

```yaml
component: Tools
kind: Added
body: >-
  Automatic meeting summaries, generated in the meeting's original language
  instead of always English. Disabled by default; enable via
  `FEATURE_FLAG_ENABLE_MEETING_SUMMARIES`.
custom:
  Audience: user
  Ticket: UN-30001, UN-30045
```

Change with an explicit behavior-change callout:

```yaml
component: Orchestrator
kind: Changed
body: >-
  Agent response caching now respects per-space TTL overrides.

  Behavior change: Spaces without an explicit override now fall back to the
  shorter platform default TTL instead of caching indefinitely.
custom:
  Audience: user
```
