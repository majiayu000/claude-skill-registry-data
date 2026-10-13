---
name: wu-community-publishing
description: Implement or review WU-COMMUNITY-001 Urdu Writers one slice at a time. Covers authenticated submission snapshots, editor publishing prompts, Product OS human moderation, immutable approved public SSR writing, reporting, My Publications, revisions, withdrawal, taxonomy, SEO, policy and launch closure while preserving local-first writing and private My Documents.
---

# WriteUrdu Community Publishing — implementation skill

Use this skill for any implementation/review task under `WU-COMMUNITY-001`.

The product is **Urdu Writers**: signed-in writers explicitly submit writing snapshots, Product OS moderators approve/reject them, and only approved immutable snapshots become durable public WriteUrdu pages.

---

## 1. Mandatory read order

Always read current `main` and these parent contracts first:

1. `specs/WU-COMMUNITY-001-moderated-urdu-writing-publishing.md`
2. `specs/WU-AUTH-001-social-authentication-foundation.md`
3. `specs/WU-DRAFT-001-cross-device-cloud-drafts.md`
4. `specs/WU-GROWTH-002-account-save-share-entry-points.md`
5. `specs/WU-SHARE-001-public-share-pages-viral-publishing-loop.md`
6. `specs/WU-PLAT-002-v2-product-journey-workspace-handoffs.md`
7. current `functions/lib/auth.mjs`
8. current `/api/documents*` implementation
9. current Product OS `/api/internal/*` security/host patterns
10. current `functions/s/[id].js` + share report patterns
11. current migrations, route registry, sitemap, SEO, AdSense, telemetry and service-worker owners.

Then read the **exact slice file** being implemented:

```text
COMMUNITY-A → specs/WU-COMMUNITY-001A-submission-data-api.md
COMMUNITY-B → specs/WU-COMMUNITY-001B-editor-prompt-submission-ux.md
COMMUNITY-C → specs/WU-COMMUNITY-001C-os-moderation-publishing.md
COMMUNITY-D → specs/WU-COMMUNITY-001D-public-reader-seo-reporting.md
COMMUNITY-E → specs/WU-COMMUNITY-001E-my-publications-revisions-withdrawal.md
COMMUNITY-F → specs/WU-COMMUNITY-001F-taxonomy-guidelines-launch-closure.md
```

Do not implement from this skill alone. The slice spec owns detailed acceptance criteria.

---

## 2. Core invariant

**Private writing is never the public object.**

The only valid path to public content is:

```text
editor / My Documents
  → explicit authenticated snapshot
  → community_writing_submissions
  → Product OS human approval
  → community_writing_publications
  → /urdu-writers/:slug
```

Never point a public page/API at `writing_documents`.

Never let a private edit mutate an approved publication.

Never let writer/public APIs set approval state.

---

## 3. Existing platform decisions to preserve

### Database

Use:

```text
env.METRICS_DB
```

Do not create `COMMUNITY_DB`, `WRITE_URDU_DB`, `ACCOUNT_DB` or another D1 database.

Before migration work:

- inspect current migration sequence;
- reconcile next migration number;
- capture current table inventory;
- add community tables additively;
- prove telemetry/share/Auth.js/`writing_documents` tables remain unchanged.

Never edit an already-applied migration.

### Identity

Authorization subject is always:

```text
session.user.id
```

obtained through the project auth wrapper.

Never authorize by email.

Provider name/email/image are not public author identity.

### Local-first writing

Normal writing remains anonymous/local-first.

Publishing may require sign-in only **after explicit publish intent**.

Auth/publish failure must never disable:

```text
transliteration
Basic Writer
Rich Editor
Urdu Keyboard
Voice input
local autosave/history
My Documents
copy/export/share-link flows
```

---

## 4. Slice boundaries

### COMMUNITY-A — submission data + API

Build only the private submission foundation:

```text
community_writing_submissions
community_writing_publications schema
community_writing_reports schema
controlled taxonomy
server content validation/sanitization
owner-only submission CRUD/pending update
quota/rate/duplicate guards
```

No public reader route. No approval endpoint.

### COMMUNITY-B — editor prompt + submission UX

Build shared publishing discovery across:

```text
Basic Writer
Rich Editor
Urdu Keyboard
Voice transcript
```

Automatic prompt heuristic:

```text
>= 600 non-whitespace characters
OR
>= 90 whitespace-delimited words
```

Also ship manual `Publish to Urdu Writers` so short poetry can submit.

Signed-out publish intent uses existing safe short-lived same-origin auth continuity. Never put writing in URL/OAuth state.

### COMMUNITY-C — Product OS moderation

Build the **only approval boundary**.

Expected internal operations:

```text
queue/detail
approve exact revision
reject exact revision
approved-revision replacement
emergency unpublish
```

Moderation writes must fail closed behind current Product OS + Cloudflare Access boundary.

Do not enable public corpus before this slice’s security/state tests are green.

### COMMUNITY-D — public reader + SEO/reporting

Only read:

```text
community_writing_publications WHERE status='published'
```

Build:

```text
/urdu-writers
/urdu-writers/:slug
/urdu-writers/category/:category
/sitemap-community.xml
public read API
report API
```

Pending/rejected/private content must be impossible to retrieve anonymously.

### COMMUNITY-E — My Publications lifecycle

Build authenticated private writer status/control:

```text
/my-publications
pending update
revision submission
rejection state
withdrawal
source-document return
```

Current public version remains live while a revision is pending/rejected.

Writer withdrawal removes public visibility but never deletes private source writing.

### COMMUNITY-F — launch closure

Close:

```text
taxonomy/indexing quality
Community Guidelines
Privacy/Terms reconciliation
navigation/route/sitemap registries
AdSense boundaries
telemetry schema
Product OS operational metrics
moderation capacity/pause controls
feature-flag rollout/rollback
production launch proof
```

No comments/likes/follows/profiles/social feed/AI auto-approval in this epic.

---

## 5. Community state model

### Submission

Expected states:

```text
pending
approved
rejected
withdrawn
```

Writer can replace only an owned `pending` submission with optimistic revision safety.

### Publication

Expected states:

```text
published
unpublished
```

Public routes always require `published`.

### Revision rule

After first approval:

```text
current publication stays live
→ writer submits a new pending revision
→ moderator reviews exact revision
→ approval atomically replaces public snapshot
```

A rejected revision never changes current public version.

### Withdrawal

Owner withdrawal:

```text
publication → unpublished
hub/category/API/sitemap remove it
public detail → 410 + noindex
private source document untouched
```

Republishing always requires moderation again.

---

## 6. Public author identity

Submission asks for:

```text
public author name / pen name
```

Rules:

- account name may be prefilled only as convenience;
- writer explicitly confirms/edits it;
- never prefill/show provider email as public name;
- provider image is not part of v1;
- public name is snapshotted into submission/publication;
- later account profile changes do not silently alter public writing.

No public author profile pages in v1.

---

## 7. Controlled taxonomy

Initial primary categories:

```text
poetry
essay
prose
thought
story
```

Initial curated tags:

```text
ghazal
nazm
shayari
essay
prose
critical-thinking
personal-reflection
society
culture
education
story
other
```

Enforce:

```text
exactly 1 category
1–5 unique curated tags
```

No free-form public tags.

Moderator may correct category/tags before approval.

Moderator may not silently rewrite title/body/public name.

---

## 8. Content safety

Server owns validation.

Initial common guards from the feature family:

```text
title <= 180 chars
public author name <= 80 chars
manual body >= 80 chars
body bounded well below platform maximums
max 5 pending submissions/user
bounded rolling submission rate
```

### Rich HTML

If rich community publishing is retained:

- use a proven server-side allowlist sanitizer compatible with Cloudflare runtime;
- derive plain text after sanitization;
- strip unsafe tags/attributes/URLs.

If a proven sanitizer is unavailable, publish plain text in v1.

**Never hand-roll regex HTML sanitization.**

---

## 9. Moderation security

Product OS approval/rejection/unpublish mutations must require the current verified OS/Cloudflare Access boundary.

At minimum:

```text
correct PRODUCT_OS_HOST
Cloudflare Access protected hostname
verified authenticated Access identity/current project pattern
optional configured moderator allowlist
```

Never authorize from:

```text
query flag
localStorage
client role string
hidden form field
unverified arbitrary email header
```

Never persist Access tokens/assertion bodies.

Approval/rejection requires the moderator’s expected `submission_revision`.

Stale review => conflict and reload.

---

## 10. Approval atomicity

First approval must atomically:

1. verify exact pending revision;
2. generate publication ID + stable server slug;
3. copy approved snapshot to publication table;
4. mark submission approved/reviewed;
5. link publication/submission.

Use a current supported D1 atomic transaction/batch pattern after verifying platform semantics at implementation time.

Duplicate exact approval must be idempotent.

Revision approval atomically replaces approved publication fields while keeping stable canonical slug and original `published_at`.

---

## 11. Public SSR/SEO rules

Public detail must be server-rendered/crawler-readable and include:

```text
approved title
approved public author name
category/tags
published date
full approved safe writing
lang=ur / dir=rtl
canonical
OG/Twitter metadata
truthful Article/CreativeWork JSON-LD
report action
Write your own Urdu CTA
```

Never expose:

```text
user ID
email
provider/account data
source document ID
submission ID
moderation identity/rejection data
```

Community sitemap contains published canonical URLs only.

Category pages remain conservative/noindex until corpus quality threshold + manual SEO review are met.

`/s/:id` remains the separate noindex direct-share surface.

---

## 12. Public reporting

Controlled reasons:

```text
spam
abuse
privacy
copyright
other
```

Report records are community-owned and do not store reporter identity in v1.

Reports raise moderator visibility but do not auto-unpublish by count.

Do not write community reports into share-artifact tables.

---

## 13. Guidelines/legal product boundary

Before broad launch:

- `/community-guidelines` exists;
- Privacy distinguishes local/private/submitted/public writing;
- publishing consent/Terms match actual license/withdrawal behavior;
- report/takedown path works;
- account deletion interaction is documented.

Core rights principle:

**Writer keeps copyright they own; WriteUrdu receives the permission needed to display/distribute the approved version under the publishing terms.**

Do not claim ownership of writer copyright.

---

## 14. Ads

Do not place ads on:

```text
submission flow
/my-publications
Product OS moderation
```

Do not insert ads inside writer body.

Any public-reading monetization uses existing safe post-content/reading boundaries and current `WU-GROWTH-001` operating contract.

Do not use this feature as an excuse to increase site-wide Auto ads.

---

## 15. Telemetry privacy

Allowed event family is defined in Slice F.

Telemetry can contain only bounded product-state metadata such as:

```text
workspace/route type
entry point
category
size bucket
state bucket
outcome/error category
```

Never include:

```text
title
body/excerpt
public author name
email
user ID
document ID
submission ID
publication ID/slug
content signature
moderator identity
```

Focused tests must enforce forbidden fields.

---

## 16. Feature flags and rollback

Use at least:

```text
COMMUNITY_SUBMISSIONS_ENABLED
COMMUNITY_PUBLIC_ENABLED
```

Rollback never drops shared D1 tables.

Disabling submissions must not break writing/My Documents/current public reading.

Disabling public corpus must fail public community routes closed/noindex while retaining private/moderation data.

---

## 17. Implementation workflow for an agent

For each requested slice:

1. read parent + exact slice spec;
2. inspect current `main` owners/dependencies;
3. reconcile any spec drift explicitly;
4. record baseline tests before code changes;
5. implement the smallest shared owner set that satisfies the slice;
6. add focused contract/unit/browser tests from that slice;
7. run existing auth/documents/share/editor/SEO regressions affected by touched files;
8. run full repository gate;
9. verify no writing/private identity appears in logs/telemetry/public HTML;
10. update parent/child status and `specs/README.md`/`specs/BACKLOG.md` only if implementation state actually changed;
11. provide production/preview verification notes and unresolved gates.

Do not combine multiple slices in one implementation PR unless explicitly requested and the earlier slice acceptance gates are already green.

---

## 18. Suggested test families

Names can follow repository conventions, but coverage must include:

```text
community-submission-api-contract
community-publishing-editor-contract
community-moderation-security-contract
community-public-reader-contract
community-publications-lifecycle-contract
community-launch-governance-contract
```

Also retain/re-run relevant existing contracts for:

```text
auth foundation
My Documents basic/editors
Voice typing/input
share loop
product telemetry
SEO authority/sitemap
AdSense route governance
service worker/application shell
```

---

## 19. Slice exit gates

### A exit

- owner-only pending submission API green;
- migration safe;
- controlled taxonomy/content guard green;
- no public publishing capability.

### B exit

- automatic prompt + manual short-poetry path green on all eligible editors;
- auth continuity preserves writing;
- successful submit says `In review`, not published.

### C exit

- OS/Access security green;
- exact-revision approval/rejection green;
- atomic/idempotent publication creation green;
- stale review cannot publish.

### D exit

- published-only SSR corpus green;
- pending/rejected/private leakage impossible;
- report + sitemap + withdrawal/unpublish public behavior green.

### E exit

- My Publications state model green;
- pending revisions preserve current public version;
- owner withdrawal green;
- no direct republish bypass.

### F exit

- guidelines/privacy/terms + taxonomy/indexing + ads + telemetry + OS metrics + rollout/rollback production checklist closed.

---

## 20. Global stop conditions

Stop and fix immediately if any implementation does any of the following:

- introduces another D1 database;
- makes sign-in required for normal writing;
- points public pages at `writing_documents`/submission rows;
- lets writer/public API approve content;
- lets private edits mutate approved publication;
- exposes provider email/name automatically as public identity;
- makes arbitrary user tags into public crawlable URLs;
- authorizes moderator writes from public origin/client flag;
- approves a stale unseen revision;
- accepts rich HTML without a proven server sanitizer;
- logs/telemeters writing or private identifiers;
- allows pending/rejected content into public API/HTML/sitemap;
- lets CDN caching keep withdrawn writing publicly readable;
- deletes private My Documents content when publication is withdrawn;
- inserts ads inside writer content/private/moderation surfaces;
- claims WriteUrdu owns writer copyright;
- enables AI automatic approval to compensate for moderation volume;
- builds comments/likes/follows/profiles/social feed inside this epic.
