---
name: kdp-operations
description: Operate an Amazon KDP publishing catalog safely — the three irreversible upload decisions (DRM, KDP Select, ISBN), format asset checklists, metadata audit/maintenance loops, royalty report analysis, and browser-automation doctrine for KDP's API-less dashboard. Use when uploading books, auditing catalog metadata, parsing royalty reports, or automating repetitive KDP dashboard work.
triggers:
  - kdp upload
  - kdp select
  - kdp metadata
  - royalty report
  - kdp automation
  - bookshelf audit
personas:
  - FREELANCE
  - MARKETING
  - DEV
tech_stack: []
derived_from: original — methodology facts synthesized from public KDP practitioner frameworks
---

# KDP Operations

[OBJ] Most KDP dashboard fields are editable after publishing. Three are not. Operations excellence = never getting the irreversible ones wrong + keeping metadata compounding.

## The three irreversible decisions (decide BEFORE upload)

### 1. DRM — recommended: decline
Once enabled it can never be removed without unpublishing and losing the listing's reviews/rank. DRM does not stop pirates (they were never customers) and does punish real buyers (no lending, device-transfer friction). Consensus practice: decline.

### 2. KDP Select / Kindle Unlimited — 90-day exclusivity lock
Enrollment means the ebook cannot be sold or given away anywhere else for 90-day rolling windows.
- **Fiction:** generally yes — KU page-reads are a major revenue stream in most fiction genres.
- **Non-fiction:** generally no — nonfiction buyers spread across platforms; wide distribution usually wins.
- Print editions are NOT affected by Select — exclusivity covers the ebook only.

### 3. ISBN
- Free KDP ISBN: Amazon listed as publisher-of-record imprint; fine for most indie work.
- Own ISBN (Bowker etc.): required if you want your own imprint name or use the same ISBN across other print distributors.
- Ebooks need no ISBN. You cannot swap the ISBN decision on a published print edition.

## Format asset checklists

| Format | Required assets |
|--------|-----------------|
| Ebook | EPUB/DOCX interior validated in Kindle Previewer, 1600×2560-ish cover JPG, description HTML ready |
| Paperback | print-ready interior PDF (embedded fonts, correct trim+margins), full-wrap cover PDF with spine math from FINAL page count, bleed verified |
| Hardcover | same as paperback with hardcover-specific wrap template |

Post-upload verification: check the live listing within 72h — description rendering, look-inside sample, category placement, price. Fix fast; the new-release clock is running.

## Metadata maintenance loop

Quarterly per title:
1. Audit keywords — are all 7 boxes filled with non-redundant phrases still matching demand?
2. Audit categories — did Amazon add new relevant subcategories? Are you shelved correctly?
3. Description refresh — does the hook still match top-of-niche conversion patterns?
4. Series linkage — series pages correct, read-through ordering intact?
Small metadata wins compound: better keywords = free organic discovery forever.

## Royalty report analysis

- Download reports monthly (KDP dashboard → reports). Parse into a simple ledger: per-title royalties, units, KENP pages, per-format split.
- Watch ratios, not just totals: KENP-to-unit ratio shows KU vs sale mix; ad-spend-to-royalty ratio shows true profitability per title.
- Kill or revive: titles with zero movement for 2+ quarters get one structured revival attempt (new keywords, cover refresh, Countdown deal) or are deprioritized.

## Browser automation doctrine (no public API exists)

Amazon exposes **no official KDP metadata/royalty API**. Automation is possible but rule-bound:

1. Session-based browser automation (Playwright-style) with saved login state — the user completes sign-in + MFA in a visible window; automation continues the session.
2. **Sequential operations only** — one book, one write operation at a time, fully completed before the next. Never parallel batches against a session-driven dashboard: rate limits, session corruption, account flags.
3. Local-first: session files stay local and gitignored; never commit cookies/session state.
4. Fail-closed: any structural change in the dashboard (selectors drift) must stop automation, not guess. Log and escalate.
5. Read operations (reports, metadata sync) before write operations in any automation rollout — prove reads for weeks before trusting writes.

## Rules

1. [REQ] DRM/Select/ISBN decided and documented before the upload session starts.
2. [REQ] Full-wrap covers built only from final page counts — a page-count change invalidates the spine.
3. [REQ] Quarterly metadata audit per title; log before/after values.
4. [REQ] Automation is sequential, local-first, fail-closed.
5. [PROHIBIT] Sharing accounts/session cookies across machines or committing them to version control.
