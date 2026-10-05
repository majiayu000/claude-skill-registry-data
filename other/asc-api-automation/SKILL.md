---
name: asc-api-automation
description: 'Use when automating App Store Connect from a script or CI via the ASC REST API (`api.appstoreconnect.apple.com`) — ASC API `.p8` key / JWT auth, TestFlight `betaGroups` / `betaBuildLocalizations`, `appStoreVersions` / `releaseType`, `reviewSubmissions`, `salesReports`, `analyticsReportRequests` — or asked "automate TestFlight / submission / release notes", "should I use fastlane", or debugging 401 NOT_AUTHORIZED / 429 RATE_LIMIT_EXCEEDED, or asked which ASC steps have no API and must be clicked by hand. API side only: build & upload → xcode-cloud-single-track-ci / local-archive-export-upload; `.p8` storage → build-time-secret-injection.'
---

# App Store Connect API Automation

This catalog's default way to drive App Store Connect from scripts and CI: an Apple-native toolchain — a ~30-line Swift/CryptoKit script mints the JWT, plain curl calls the REST API. No fastlane/spaceship, no Ruby gems, no Homebrew, consistent with the catalog's mise + no-third-party baselines.

## When to invoke

- Writing release tooling: distribute a build to TestFlight groups, set what's-new, create the next App Store version, submit for review
- Pulling sales or App Store analytics reports on a schedule
- Debugging ASC API auth failures (401 `NOT_AUTHORIZED`) or rate limiting (429)
- Asked "should I use fastlane for this?"

## Scope

Owns: token minting, curl conventions, and the endpoint cookbook below. Does NOT own:

- **Building / uploading the binary** — builds arrive in ASC via Xcode Cloud (→ `xcode-cloud-single-track-ci`), a local `xcodebuild -exportArchive` / `xcrun altool` run (→ `local-archive-export-upload`), Xcode Organizer, Transporter, or the ASC API's Build Uploads resources (`POST /v1/buildUploads` + `buildUploadFiles` reserve / commit — not part of this cookbook). This skill picks up *after* the build exists in ASC.
- **`.p8` key storage & leak prevention** → `build-time-secret-injection` (Layer 2 `secrets/.env`) + `apple-public-repo-security` (rotate-first SOP).
- **What metadata will pass review** → `app-store-review-rejections`; this skill is *how* to submit, not *what*.

## Keys: create, scope, store

| Key kind | Where | JWT identity claim | Use for |
|---|---|---|---|
| **Team key** (default) | Users and Access → Integrations; role-scoped | `iss` = Issuer ID | CI and shared tooling — pick the least-privilege role that works (App Manager covers release ops; avoid Admin) |
| **Individual key** | Your user profile → Individual API Key | `sub: "user"` (no `iss`) | Personal one-off scripts; inherits *your* permissions |

Store per `build-time-secret-injection` Layer 2:

```bash
# secrets/.env (gitignored; .env.example committed)
ASC_KEY_ID=2X9R4HXF34
ASC_ISSUER_ID=57246542-96fe-1a63-e053-0824d011072a
ASC_KEY_PATH=secrets/AuthKey_2X9R4HXF34.p8
```

## Mint the token (CryptoKit, zero dependencies)

Claims (verified against Apple's *Generating tokens for API requests*, 2026-07): header `alg: ES256` (the only accepted algorithm), `kid`, `typ: JWT`; payload `iss` (**Issuer ID**, the UUID from Users and Access → Integrations — not your Team ID), `iat`, `exp` (invalid if more than 20 minutes ahead — **exception**: a token carrying `scope` and restricted to GET requests on allow-listed resources can live up to 6 months, per Apple's *Determine the Appropriate Token Lifetime* — but that allow-list is Xcode Cloud / Power-and-Performance resources only (Build Actions, Build Runs, Git References, Issues, macOS Versions, Products, Providers, Power and Performance Metrics and Logs, Pull Requests, Repositories, Test Results, Workflows, Xcode Versions); none of this cookbook's endpoints qualify, so release tooling always mints ≤ 20-minute tokens), `aud: "appstoreconnect-v1"`, optional `scope` (array of allowed requests like `"GET /v1/apps"` — pin single-purpose tokens to single endpoints).

The script is bundled at `${CLAUDE_SKILL_DIR}/scripts/mint-asc-token.swift` (the `scripts/` folder next to this SKILL.md; CryptoKit, zero dependencies) — run it by that path, or copy it into your repo's `scripts/` first, which the example below assumes.

```bash
source secrets/.env
ASC_TOKEN=$(swift scripts/mint-asc-token.swift)
curl -sf -H "Authorization: Bearer $ASC_TOKEN" "https://api.appstoreconnect.apple.com/v1/apps?limit=200"
```

Mint fresh per run; a job that outlives the token re-mints instead of extending `exp`.

## curl conventions

- **JSON:API shape** — write calls send `Content-Type: application/json` with the body wrapped as `{"data": {"type": ..., "id": ..., "attributes": {...}, "relationships": {...}}}`.
- **Pagination** — pass `limit=200` (the max) and follow `links.next` until absent; the small default page size silently truncates lists otherwise.
- **Rate limit** — every response carries `X-Rate-Limit: user-hour-lim:3500; user-hour-rem:…` (rolling hour, per key; Apple says actual limits vary). Exceeding returns 429 `RATE_LIMIT_EXCEEDED` — back off and re-queue; a 429 lockout hits *everything* sharing that key, including CI.
- **Errors are structured** — read `.errors[].detail`. Triage: 401 = token/claims problem, 403 = key role or `scope` problem, 409 = resource state problem (e.g. version not in a submittable state).

## Endpoint cookbook

| Goal | Call |
|---|---|
| App's ASC id | `GET /v1/apps?filter[bundleId]=<bundle-id>` |
| Latest processed builds | `GET /v1/builds?filter[app]=<appId>&sort=-uploadedDate&limit=5` |
| TestFlight what's-new | `GET /v1/builds/<id>/betaBuildLocalizations` → `PATCH /v1/betaBuildLocalizations/<locId>` with `attributes.whatsNew` |
| Add build to a beta group | `POST /v1/betaGroups/<groupId>/relationships/builds` with `{"data":[{"type":"builds","id":"<buildId>"}]}` |
| Create next App Store version | `POST /v1/appStoreVersions` — relationship `app`, attributes `platform: "IOS"`, `versionString`, `releaseType` (see Release automation below — don't omit) |
| Set description / what's-new | `GET /v1/appStoreVersions/<id>/appStoreVersionLocalizations` → `PATCH /v1/appStoreVersionLocalizations/<locId>` |
| Attach build to version | `PATCH /v1/appStoreVersions/<id>/relationships/build` |
| Set release behavior | `PATCH /v1/appStoreVersions/<id>` with `attributes.releaseType` — `MANUAL` (release yourself), `AFTER_APPROVAL` (auto-release the instant Apple approves), or `SCHEDULED` (auto-release at `attributes.earliestReleaseDate`, ISO 8601) |
| Submit for review | `POST /v1/reviewSubmissions` (app + platform) → `POST /v1/reviewSubmissionItems` (reviewSubmission + appStoreVersion) → `PATCH /v1/reviewSubmissions/<id>` with `attributes.submitted: true` |
| Daily sales report | `GET /v1/salesReports?filter[frequency]=DAILY&filter[reportType]=SALES&filter[reportSubType]=SUMMARY&filter[vendorNumber]=<n>` (+ `filter[reportDate]=YYYY-MM-DD` for a specific day) — response is a **gzipped TSV**, not JSON: `curl -o report.gz` then `gunzip` |
| App Store analytics | `POST /v1/analyticsReportRequests` (`accessType: "ONGOING"`) once per app, then poll its `reports` → instances → segments for download URLs |

The review-submission flow is the `reviewSubmissions` model introduced in App Store Connect API 1.7, which replaced the deprecated one-shot `appStoreVersionSubmissions`.

## Pre-submission prerequisites the three-call flow doesn't mention

The `POST reviewSubmissions` → `POST reviewSubmissionItems` → `PATCH submitted: true` sequence above assumes the app is already submittable; in practice three preconditions block it and have no REST fix:

| Blocker | Symptom | Fix | Where |
|---|---|---|---|
| App pricing not set | `POST reviewSubmissions` fails with a pricing-state error (exact error-code string not found in Apple's published API reference — observed in practice) | Set the price once, via the API (`POST /v1/appPriceSchedules`, "Add a Scheduled Price Change to an App") or the web UI | Needs the Paid Apps Agreement accepted first — web-UI-only (see "Steps with no ASC API at all" below) |
| Empty `copyright` attribute | An `ENTITY_ERROR.ATTRIBUTE.REQUIRED`-shaped error — documented for other required fields (e.g. `companyName`); the same shape is observed in practice for a blank `copyright`, not confirmed against Apple's official attribute reference | Always send a non-empty `copyright` string | API |
| Leftover non-`COMPLETE` `reviewSubmissions` | A new `POST /v1/reviewSubmissions` is refused; the resource has no DELETE (unlike the deprecated pre-2022 `appStoreVersionSubmissions`, which did) | `PATCH /v1/reviewSubmissions/<id>` with `{"data":{"type":"reviewSubmissions","id":"<id>","attributes":{"canceled":true}}}` — `state` is read-only and transitions to `CANCELING` in response; during `WAITING_FOR_REVIEW`, canceling returns the version to an editable state (observed as `DEVELOPER_REJECTED`) without leaving an Apple rejection record | API |

## Steps with no ASC API at all — must be clicked by a human

The three prerequisites above are gaps in an otherwise-scriptable flow. These are different:
Apple publishes no REST resource for them at all, so no amount of scripting closes the gap —
budget a manual, one-time (or rarely-repeated) click in the ASC web UI. For the two verified
cases (Agreements/Tax/Banking, and whole-app Promo Codes vs Subscription Offer Codes) and their
sourcing, read `references/no-api-steps.md`.

## Release automation: SemVer, changelog, and explicit releaseType

- **`versionString` = SemVer, sourced from the build, not reinvented in CI.** Set it to the same value as the archived build's `MARKETING_VERSION` (`CFBundleShortVersionString`) — bump that once at the Xcode-project level (→ `xcode-cloud-single-track-ci` build-number & version automation), then read it back for the `appStoreVersions` call instead of maintaining a second version counter in release tooling.
- **Changelog → `whatsNew`, generated once, written twice.** Build the "What's New" text from `git log <last-tag>..HEAD --oneline` (or your conventional-commit tooling) in the release job, then `PATCH` it into both `betaBuildLocalizations` (TestFlight) and `appStoreVersionLocalizations` (App Store) per locale — one generated string, two writes, so testers and reviewers see the same notes.
- **`releaseType` — set it explicitly, every time.** The attribute is optional and Apple's schema documents no default value. The ASC web UI backs the same behavior with an explicit 3-way choice (*Manually release this version* / *Automatically release this version* / *Automatically release this version after App Review, no earlier than*); skipping `releaseType` in a scripted create/update leaves the version's release behavior to an undocumented default — in practice new versions show up as auto-release — instead of a decision your pipeline made on purpose. Default to `MANUAL` in automation unless auto-release is the deliberate intent.

## Rationale

- **No fastlane by default**: spaceship drags a Ruby toolchain into a repo whose only Ruby consumer would be release tooling — against the catalog's mise/no-Homebrew baseline — and inserts a drift layer that breaks whenever ASC changes ahead of a spaceship release. Direct REST against Apple's own docs has zero intermediary.
- **CryptoKit mint script**: token minting is the only genuinely fiddly step (ES256, raw-signature format); everything after is plain curl. A 30-line Apple-native script beats installing PyJWT or hand-rolling openssl DER conversion.
- **Least privilege**: token-leak blast radius scales with the key's role; the `scope` claim can pin a single script to a single request.

## Deviation considerations

- **Already on fastlane** with maintained lanes and a Gemfile → keep it; this skill is the default for repos *without* a Ruby toolchain, not a migration mandate.
- **Heavy tooling** (dozens of endpoints, typed models, retries) → generate a client from Apple's published App Store Connect OpenAPI spec instead of hand-rolled curl; still no fastlane required.
- **One-off manual task** → the ASC web UI is faster; scripting has a floor cost.

## Common Mistakes

1. **`iss` set to Team ID** — ASC API wants the **Issuer ID** (UUID); Team ID belongs to other Apple JWTs (e.g. APNs). Symptom: 401 `NOT_AUTHORIZED` with a well-formed token.
2. **`exp` more than 20 minutes ahead** — token rejected outright (unless it's a `scope`d, GET-only token on allow-listed resources, which can live up to 6 months); also watch local clock skew on `iat`.
3. **openssl-signed tokens failing** — `openssl dgst` emits a DER-encoded signature; JWT ES256 requires the raw 64-byte r‖s form. CryptoKit's `rawRepresentation` is already correct.
4. **Uploading the binary via REST** — no such endpoint exists; route builds through Xcode Cloud, `local-archive-export-upload`, Organizer, or Transporter.
5. **Ignoring pagination** — the default page size silently truncates; always `limit=200` + follow `links.next`.
6. **Parsing `salesReports` as JSON** — it's a gzipped TSV file.
7. **Tight-polling build processing or analytics** without reading `X-Rate-Limit` — 429 locks out every consumer of the key.
8. **Admin-role key in CI** when App Manager or a `scope`d token suffices.
9. **`.p8` committed to the repo** — stop and run the rotate-first SOP in `apple-public-repo-security`; storage layout per `build-time-secret-injection`.
10. **Omitting `releaseType` on an `appStoreVersions` create/update** — the attribute has no documented default, so an unset value can leave a version on automatic release; it goes live the instant Apple approves it instead of waiting for a deliberate manual release. Set `releaseType: "MANUAL"` explicitly unless auto-release is intended.

## Review Checklist

- [ ] Team key with least-privilege role; `.p8` + IDs stored per build-time-secret-injection Layer 2, nothing tracked by git
- [ ] Token claims: ES256, `kid` header, `iss` = Issuer ID (or `sub: "user"` for individual keys), `exp` ≤ 20 min (or a `scope`d GET-only token, up to 6 months), `aud` `appstoreconnect-v1`
- [ ] Every collection call sets `limit` and follows `links.next`
- [ ] 429 handled with backoff; no tight polling loops
- [ ] Write calls use the JSON:API `{"data": {...}}` wrapper
- [ ] No REST binary-upload attempt; build side delegated to xcode-cloud-single-track-ci
- [ ] `releaseType` explicitly set on every `appStoreVersions` create/update (`MANUAL` unless auto-release is intended) — never left to ASC's undocumented default
- [ ] `grep` for key IDs / issuer ID / `.p8` contents across tracked files returns zero hits

## Related skills

- `xcode-cloud-single-track-ci` — build & upload side; this skill starts after the build exists in ASC
- `local-archive-export-upload` — the local `xcodebuild -exportArchive` / `altool` upload path; this skill starts after the build exists in ASC
- `build-time-secret-injection` — where `ASC_KEY_ID` / `ASC_ISSUER_ID` / the `.p8` live (Layer 2 `secrets/.env`)
- `apple-public-repo-security` — `.p8` leak prevention and the rotate-first SOP
- `app-store-review-rejections` — *what* to submit so review passes; this skill is *how* to submit
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
