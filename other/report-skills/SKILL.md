---
name: report-skills
description: Shared setup and rules for the report-skills bundle (report-publisher, client-reporter, proposal-tracker, deck-publisher, report-designer). Loaded by the individual skills for the common ReportRoom MCP publish flow, account bootstrap, and safety gates. Not invoked directly — pick the specific skill for the job.
---

# Report Skills — shared flow and rules

All five skills publish through the **ReportRoom MCP server**. This file holds what they share; each skill's SKILL.md holds only what differs.

## The publish flow (every skill follows this)

1. **Check access.** Call `account_status`. If no account/API key exists, call `create_account` — it issues a key in-flow; never ask the user to leave the conversation to sign up. Note: publishing is blocked until the user clicks the email-verification link (`create_account` sends it), and unverified accounts serve from a preview/noindex domain — tell the user this upfront so the first publish isn't a surprise.
2. **Fetch the design language.** Call `get_design_system` and follow it exactly when authoring. The design system supplies the taste; you supply content and assembly. Do not improvise your own CSS framework.
3. **Author a self-contained HTML document.** Semantic HTML, responsive, dark-mode aware, no external dependencies beyond what the design system allows.
4. **Lint before publish.** Call `lint_document` and fix every issue it reports. Never skip this step.
5. **Approval gate.** Show the user: title, a one-paragraph summary of what the page contains, section list, and who it's for. **Wait for explicit approval before calling `publish` on anything client-facing.** For personal/internal shares the user may pre-approve ("just publish it"). Also tell them every published page carries a small "Published with ReportRoom" footer credit (see below) — clients and prospects will see it.
6. **Publish.** Call `publish`. Return the live URL prominently. Handle the two common failure modes instead of retrying blind:
   - **`cap_reached`** — the account is at its live-document limit (free = 10, pro = 100; Team/Business = unlimited). The error carries the live-doc list. Offer the user a choice: retire an old document to make room (`publish` with `replace_slug: "<old-slug>"` in the same call, or `unpublish` it first), or upgrade the plan. Never silently drop the new page.
   - **Not verified / `FORBIDDEN`** — publishing is blocked until email verification (see step 1). A `FORBIDDEN` also means a team **viewer** role can't publish (see workspaces below) — surface it, don't loop.
7. **Close the loop.** Tell the user view analytics are attached: they can ask any time "how is my report doing?" (→ `get_analytics`, which returns 7-day views by day plus a summary). For tracked deliverables, offer to check back. Do not promise per-viewer or per-section detail — current analytics are aggregate view counts.

## Other tools you have

Beyond the core flow, the ReportRoom MCP exposes:

- **`list_documents`** — the account's live documents, most recent first. Use to keep recurring reports consistent, find a slug to update, or show what's using up the plan's slots.
- **`unpublish` / `republish`** — retire a live document (its URL returns 410 Gone, the plan slot frees up) or bring it back. Both idempotent. Use for expired proposals, superseded client reports, or freeing a slot at the cap.
- **`set_handle`** — rename the publishing subdomain (`<handle>.reportroom.io/<slug>`); existing docs move and old links redirect. This is the lightweight branding lever for everyone.
- **`attach_domain`** — attach a custom domain (Team/Business). Returns the DNS records the human must create at their registrar (a CNAME plus ownership/certificate TXT records) and streams progress as provisioning advances. Certificate issuance only completes *after* they add the records, so hand the records over and tell them to come back — don't wait on it. `account_status` and `list_documents` report the active custom domain once live. This is the real "branded page" lever for agencies.
- **Team workspaces** — `account_status` returns `org_kind` (`personal`/`team`) and the caller's `role`. In a team workspace, `visibility: "team"` on `publish` makes a document viewable only by signed-in org members (Team/Business plans); **viewers cannot publish** and will get a `FORBIDDEN`.

## Data rooms (Business plan only)

When the user needs **access control and per-person tracking** — a fundraise, a diligence process, a gated proposal — a data room beats a published document. A room is a named, access-controlled bundle of documents at one URL, shared with *identified* viewers.

**Gate:** Business plan only (not Free/Pro/Team) **and** the caller must be the org owner or an admin. Anything else returns a clear error — relay it and offer the plain-document path instead of retrying. Limits: **10 live rooms per org, 200 viewers per room.**

**The flow, in order:**
1. `create_data_room` — name it, pick `access_mode` (`public` | `email` (magic-link, the default) | `passcode` | `allowlist`), and optionally `settings`: `nda_text`, `expires_at`, `allow_download`, `watermark`. **`allow_download` and `watermark` are accepted and stored but not yet enforced at serve time (Phase 2) — never tell the user a room is watermarked or download-locked. `nda_text` and `expires_at` are fully enforced.**
2. `add_documents_to_room` — pass `document_ids` **in display order**. This *replaces* the whole set, so send the full ordered list every time. Documents stay first-class and standalone; adding one never unpublishes or moves it.
3. `set_room_access` — change access mode, rotate the passcode (string sets, `null` clears), or update NDA/expiry/download/watermark later.
4. `grant_room_access` — per viewer, by email. **Returns a single-use invite link once and does not email it.** Hand it to the user to send; it is never retrievable again (only a hash is stored), so if it's lost, re-grant to reissue. Never send it to the recipient yourself without the user's explicit go-ahead.
5. `list_room_viewers` — the roster with verification/NDA/revocation state. Never exposes invite tokens.
6. `revoke_room_access` — instantly ends that viewer's sessions.

**`get_room_analytics` is different from `get_analytics`.** It returns **per-viewer, per-document** opens, total events, and dwell — so you can say "the lead spent time on pricing and skipped the deck" and suggest a follow-up. Published documents outside a room remain **aggregate** view counts only. Don't mix the two up when telling the user what you can see.

## Safety rules (all skills, non-negotiable)

- **Published pages are public, search-indexable URLs.** A normal published report/deck is world-readable and can be indexed by search engines — the slug is obfuscation, not protection. Before publishing, scan the content for secrets, API keys, internal hostnames, personal data of third parties, or anything marked confidential. If found, stop and ask. For genuinely internal material in a team workspace, `visibility: "team"` restricts viewing to signed-in org members (and serves `noindex`); for gating to *named outside people*, only a **data room** does that — a normal link cannot.
- **Every page shows a "Published with ReportRoom" footer credit.** It's discreet but always present on both reports and decks, on every plan. Disclose it before publishing anything client-facing so it isn't a surprise on the recipient's screen.
- Never fabricate data, metrics, or client results in a report. If a number is estimated, label it.
- Never publish without the approval gate for client-facing content, even if the user seems in a hurry.
- If `lint_document` or `publish` fails, show the actual error and fix the document — do not silently retry with degraded content.

## Which skill for which job

| The user wants | Use |
|---|---|
| Share research/analysis they just produced | `report-publisher` |
| A recurring, branded deliverable for a client | `client-reporter` |
| A proposal/offer where knowing "did they open it" matters | `proposal-tracker` |
| Slides, not a document | `deck-publisher` |
| An existing page made better-looking | `report-designer` |
