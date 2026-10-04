---
name: chrome-web-store-release
description: "Chrome Web Store release process for Matrx Extend. Use when checking release readiness, submitting a Store update, running `pnpm zip:store` or its risk gate, judging whether a change is Store-material, picking the version, editing listing, privacy, or reviewer copy, or tracking a review. NOT for local unpacked builds (use pnpm dev)."
---

# Chrome Web Store release ownership

Own the Matrx Extend Store release through approval or a genuine human-only
blocker. Arman does not want routine questions, dashboard chores, packaging, or
status checks handed back to him.

## Standing authorization and account access

Starting or assigning a Store release is blanket authorization to finish it.
Do not ask Arman to approve packaging, versioning, login, dashboard edits,
upload, submission, automatic publication, monitoring, or routine corrections.
Discuss product bugs and improvement ideas when useful, but never turn that
discussion into a request to approve the release work already assigned.

Agents already have the Google-account access needed for this work. First use
the available authenticated browser state, AI Matrx Vault, personal Vault, and
stored credentials or verification codes. Never ask Arman for a password, a
stored code, permission to use an account, a screenshot, or a dashboard status
that the agent can obtain through those sources.

The sole normal handoff is a live Google 2FA challenge that cannot be completed
with the access or codes already in either Vault. Enter all available account
details, reach the exact challenge screen, and only then ask Arman to complete
that one challenge. Resume immediately afterward and finish the release. A
login page, expired session, missing tab, or unfamiliar browser is not a
blocker; recover access using the available browser and Vault tools.

Read these before acting:

- `/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHROME-WEB-STORE.md` — published version, candidate, evidence,
  item ID, and past rejection.
- `/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHROME-WEB-STORE.md` — canonical dashboard copy.
- `config/chrome-web-store-approved-baseline.json` — the exact policy surface
  Google most recently published.
- `src/config/sidepanel-visibility.ts` — the single public/member/admin feature
  switchboard for the candidate.

## Decide whether the update is routine or Store-material

Compare the candidate with the `publishedSourceCommit` in the approved
baseline. Run `pnpm zip:store`; its blocking risk gate compares the emitted
manifest with Google's published surface and scans emitted JavaScript for
forbidden runtime-code paths.

A change is **routine** when the approved manifest surface is identical and the
diff only fixes bugs, improves performance or UI, refactors internals, or
extends behavior already truthfully covered by the listing and disclosures.
Submit routine updates with concise release notes. Google still reviews the
package; no separate email is necessary.

Before packaging, inspect `SIDEPANEL_TAB_AUDIENCE`. Features marked `admin`
may remain available for internal testing but must not appear in public Store
copy, screenshots, or reviewer steps. Do not scatter one-off visibility checks
through components; change the typed switchboard so navigation and content are
gated together. An audience is a product decision, never a way to hide a defect:
never change a feature's audience because it is broken — fix the defect (on
2026-09-27 Chat was hidden from guests instead of fixing a server bug).

A change is **Store-material** when it changes or introduces any of these:

- required or optional permissions, host access, content-script reach,
  externally connectable origins, CSP, or web-accessible resources;
- collection, handling, retention, sale, or third-party transfer of a new user
  data category, including authentication information;
- remote code, downloaded executable logic, `eval`, `new Function`, or Chrome
  DevTools Runtime execution;
- a new primary purpose, a feature the listing does not truthfully describe,
  or behavior that makes existing screenshots/test instructions misleading;
- a new privileged browser capability, background/automatic behavior, payment,
  or account requirement;
- removal or breakage of the public no-login reviewer path.

Do not merely stop at the label. Reconcile every affected Store field: single
purpose, description, permission justifications, privacy-policy behavior, data
disclosures, Limited Use certifications, screenshots, and reviewer steps.
Create focused reviewer evidence when the change cannot be reproduced from the
existing public test path. The normal way to communicate a material update is
the Store submission and its notes; contact Google separately only when the
dashboard or an existing reviewer thread asks for it.

Never weaken the automated baseline to make a candidate pass. Update the
baseline only after Google publishes that changed surface.

## Versioning

Use three-part SemVer, which is valid for Chrome manifests:

- `PATCH` (`0.2.1`) — fixes and small compatible improvements.
- `MINOR` (`0.3.0`) — a meaningful compatible feature batch.
- `MAJOR` (`1.0.0`) — the public product promise is stable and the team is
  intentionally declaring general availability.

Store approval alone does not require `1.0.0`. For this product, `0.2.0` is the
first post-approval live-testing line. Use `1.0.0` after the short public
testing window passes, the primary workflows are stable, and the Store listing
and screenshots represent the product we want broadly marketed.

Never reuse or decrease a version. Do not write `0.2.00`; canonical SemVer is
`0.2.0`.

## Release and publish

1. Sync `main` with `origin/main`; preserve unrelated concurrent work.
2. Inspect changes since the baseline's published commit and classify them.
3. Run the full relevant tests. A Store release must include TypeScript, unit
   tests, strict schema routing, tool-registry drift, migration ledger, Store
   package validation, and the Chrome Web Store risk gate.
   Test the visible `everyone` surface signed out and the `signed-in` surface
   with a non-admin account. An admin session is never acceptable screenshot
   or reviewer-path evidence.
4. Use `./release.sh --patch|--minor|--major` when a new package is needed.
   Upload only `.output/matrx-extend-<version>-store.zip`; never the local zip.
5. In the existing publisher **Matrx**, update only the primary item
   `hnfolienncfklkgmdjjmhhegglimlamg`. Never use the duplicate draft item.
6. Reconcile listing fields only where the candidate requires it, save, upload,
   and submit for review. Keep automatic publishing enabled unless Arman asks
   for a staged release.
7. Verify the dashboard reaches **Pending review**. Record exact version,
   artifact SHA-256, classification, changed Store fields, submission time, and
   auto-publish state in `/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHROME-WEB-STORE.md`; commit and push it.
8. Monitor the dashboard and Google email until approved, rejected, or action
   is requested. On publication, verify **Published - public**, update the
   approved baseline version/commit/policy surface, and close the record.

Do not stop for an approval. Stop only after reaching a live Google 2FA
challenge that cannot be satisfied from either Vault. Ask Arman to complete
that exact challenge, then resume and finish. Resolve Store-policy questions
from the code, Google's requirements, and the canonical record; correct routine
submission issues autonomously.

## Store marketing

Treat conversion work as a truthful presentation pass, not a reason to inflate
the feature story. Keep the single-purpose description direct. Refresh
screenshots whenever the visible UI materially changes; show the strongest
four user outcomes, not internal architecture. Add promo tiles only when there
is polished campaign artwork worth using. Before `1.0.0`, complete one focused
marketing pass covering icon, title/summary, first screenshot, screenshot
captions/composition, support/homepage pages, and the public reviewer/demo path.
