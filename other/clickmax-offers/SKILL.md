---
name: clickmax-offers
description: Use when the user wants to inspect, create, clone, update, approve, archive, unarchive, or delete product offers and checkout variants in Clickmax, or make a product sellable (deliverable, support contact, invoice name, approval).
---

## When this applies

Use this skill for offer-level commercial control: pricing/currency/checkout variants, cloning the main offer, readiness diagnostics, approval submission, archive/unarchive, and destructive delete.

Not this skill:

- product catalog identity/archive/delete -> use the direct product tools
- "checkout" through the user's own Whop, Hotmart, Stripe or Pagar.me account (embedded on a page or as a funnel step) -> `clickmax-pages` external checkout: it starts with `mcp__plugin_clickmax_clickmax__external_checkout_accounts_list` and, with no integration, instructs the user to connect it. Do NOT create a Clickmax product/offer or an `externalUrl` offer as a substitute.

## Key assumptions

- the offer is the sellable variant; one main offer is created with the product
- lifecycle is `draft -> pending_approval -> active`
- `offers_get_incomplete_reason` is the preflight diagnostic before approval
- **Sellability gate (internal checkout).** An internal-checkout offer becomes approvable only when `offers_get_incomplete_reason` returns empty. For a fresh offer it typically flags: `softDescriptor` (the ≤15-char name shown on the buyer's card/invoice statement; some gateways trim it further, to ~13 alphanumeric chars), `supportPhone`, `deliverables` (what the buyer receives — required for `community|course|ebook|physical|other|software|mentorship`; NOT for `event|services|consultancy`), and `description`. `supportEmail` defaults to the account owner's email, so it rarely blocks. External-checkout offers (any `externalUrl`) skip all of these.
- **Two blockers Max cannot fix:** `sellerStatus` and `bankAccountStatus` come from the seller's own payout onboarding (identity + bank account); no offer edit clears them. Surface them as "finish your seller/payout registration" and stop.
- **Custom support email = verified flow.** The default support email is the account owner's, so `supportEmail` rarely blocks. A DIFFERENT address must be registered (`offers_create_support_email`) and then verified by the user clicking a link sent to that inbox (out-of-band). Only after `verifiedAt` is set (check via `offers_list_support_emails`) can it be attached with `offers_update` (`offerSupportEmailId`); attaching an unverified one fails. Do not register a custom email unless the user explicitly wants one.
- **Product image ≠ checkout banner — never confuse them.** `bannerDesktop`/`bannerMobile` (settable via `offers_update`) are the checkout's promotional banner art. The product's OWN image (the photo/thumbnail that represents the product) is a SEPARATE slot: it is set by uploading a file to the offer's product-image slot, and NO offer field turns an arbitrary image URL into it — `offers_update` cannot set the product image. Never drop a product image into `bannerDesktop`/`bannerMobile` as a stand-in; that is a different thing (checkout background art).
- **Approval is moderated, not automatic.** `offers_send_to_approval` moves a cleared offer to review (`pending_approval`); a human moderator turns it `active`. Max can complete fields and submit, never self-approve. Checkout sells only an `active` offer; before that it renders as preview only.
- `offers_create` creates secondary offers only; clone-main is the safer variant path
- `offers_update` preserves the same offer id and existing checkout identity
- Offer type matters: internal offers sell through Clickmax checkout; external offers redirect/use `externalUrl`
- Public checkout identity is exposed as `hash`; keep it stable unless the user intentionally creates/clones a different offer
- Prices use the smallest currency unit; recurring behavior is controlled by `isRecurrent` and payment configuration, not product identity alone
- `quantityItems` controls delivered/sold quantity semantics for the offer variant
- `type` (offer nature) is a full enum, not a physical/other binary: `community | course | ebook | event | physical | other | services | software | consultancy | mentorship`. Pick the specific value that matches the product (e.g. a course product's offers use `course`, not `other`) — never default non-physical offers to `other`.

## Thought process

1. Distinguish read/diagnose from variant creation from lifecycle activation.
2. Prefer cloning the main offer when the user wants a close derivative.
3. Run incomplete-reason diagnostics before approval submission.
4. Confirm destructive delete when intent is not already explicit.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__offers_get` to inspect one offer by id.
- Use `mcp__plugin_clickmax_clickmax__offers_get_incomplete_reason` before approval to identify every blocking item for that offer id.
- Use `mcp__plugin_clickmax_clickmax__offers_create` to create a secondary offer under the same product, passing the product id, offer name, price fields in cents, currency, and the intended `paymentConfig`.
- Use `mcp__plugin_clickmax_clickmax__offers_clone_main_offer` when the user wants a new variant that inherits the current main-offer setup for the product id. It does NOT auto-inherit everything: `name`, `originalPrice`, and `paymentConfig` are required inputs even though other offer fields are copied — supply them explicitly (reuse the main offer's own values from `offers_get` when the user just wants a near-identical clone).
- Use `mcp__plugin_clickmax_clickmax__offers_update` when the user wants to keep the same offer id and checkout identity while changing commercial fields such as name, price, default installment, currency, or `paymentConfig`. This is a FULL REPLACE, not a patch — `name`, `type`, `productType`, `currency`, `originalPrice`, `defaultInstallment`, and `supportPhone` are all required on every call. Call `offers_get` first and resend the complete set with only the intended field changed; sending just the changed field(s) fails validation on the rest.
- Use `mcp__plugin_clickmax_clickmax__offers_send_to_approval` only after blockers are cleared for that offer id.
- Use `mcp__plugin_clickmax_clickmax__offers_archive` or `mcp__plugin_clickmax_clickmax__offers_unarchive` for lifecycle visibility changes without deleting the offer.
- Use `mcp__plugin_clickmax_clickmax__offers_delete` only for explicit permanent removal and expect failure when transaction history prevents deletion.
- Use `mcp__plugin_clickmax_clickmax__offers_add_membership_delivery` to make an offer deliver a Clickmax members-area classroom (`offerId` + `portalId` + `classroomId`); it adds an `internal_membership` deliverable so buyers get classroom access. Build the members area first (`clickmax-members-area`) to get the portal/classroom ids. Adds a deliverable, does not replace existing ones.
- Use `mcp__plugin_clickmax_clickmax__offers_add_link_delivery` to deliver external link(s) the user already has (a hosted PDF, a Drive/Notion page, a third-party course area): pass `offerId` + `links` (`[{ title, url }]`, http(s)). Prefer this over `offers_add_membership_delivery` when the deliverable is NOT a Clickmax classroom. Never fabricate the URL — ask the user for it, or offer to build a members area when they have no destination yet.
- Use `mcp__plugin_clickmax_clickmax__offers_add_file_delivery` to deliver a file the user uploads (e.g. a PDF). When `deliverables` is a blocker and the user has the material as a file, OFFER a direct file upload first — let them attach it in the chat and use the public `url` you get back, plus a `title` (optional `description`). Don't force them to find or host a link for something they can simply upload. Reserve `offers_add_link_delivery` for a deliverable that already lives at an external URL, and `offers_add_membership_delivery` for a Clickmax members-area classroom.
- **Readiness wizard (make an offer sellable). ASK FIRST, ACT SECOND — never auto-fill or auto-decide.** The FIRST step of completing an offer is a single `question` batch collecting the checklist below (deliverable type + support phone + support email + product image); you MUST NOT call `offers_update` / `offers_add_*` / `offers_set_product_image` / `offers_send_to_approval` before you have the user's answers. NEVER guess the deliverable (e.g. silently assume a members area), never auto-fill the phone/email, never skip the image — executing without asking is the WORST failure of this flow, and it keeps happening in long conversations, so treat "I already have enough to just run the tools" as a red flag: ask. `mcp__plugin_clickmax_clickmax__offers_get_incomplete_reason` is ONLY a preflight check — do NOT use it as the question list. ALWAYS walk the user through this FIXED checklist; some items are NOT in `incompleteReason` yet MUST still be asked (support email has a default, product image is a frontend-only pendency). Ask them (batch the simple ones), then fill each:
  - **invoice name** (`softDescriptor`) — pre-fill a ≤15-char suggestion for the user to confirm/edit → `mcp__plugin_clickmax_clickmax__offers_update`;
  - **support phone** (`supportPhone`) → `mcp__plugin_clickmax_clickmax__offers_update`;
  - **support email** — ALWAYS ask, even though it is NOT a blocker. Read the offer's current `supportEmail` via `mcp__plugin_clickmax_clickmax__offers_get` and SHOW it as the default (e.g. "e-mail de suporte atual: `user@conta.com` — manter ou trocar?"); keep it, or if the user gives a different address run the verified-email flow below;
  - **description** (min 50 chars — `incompleteReason` only checks presence, not length, so expand a too-short one before saving) → `mcp__plugin_clickmax_clickmax__offers_update`;
  - **deliverable** — ONLY when the offer `type` requires one (`community|course|ebook|physical|other|software|mentorship`; NOT `event|services|consultancy`). FIRST ask how the buyer receives it (one select: upload a file/PDF · an external link · a Clickmax members area); do NOT assume the type. THEN branch: file → upload → `mcp__plugin_clickmax_clickmax__offers_add_file_delivery`; link → ask URL (+ title) → `mcp__plugin_clickmax_clickmax__offers_add_link_delivery`; members area → get/create portal+classroom (`clickmax-members-area`) → `mcp__plugin_clickmax_clickmax__offers_add_membership_delivery`;
  - **product image** — ALWAYS offer it. It is NEVER in `incompleteReason` (frontend-only pendency), so you MUST ask proactively: have the user upload an image, then `mcp__plugin_clickmax_clickmax__offers_set_product_image` (offer id + uploaded URL). Never route it to the banner.
    Then re-run `mcp__plugin_clickmax_clickmax__offers_get_incomplete_reason` until empty and `mcp__plugin_clickmax_clickmax__offers_send_to_approval`. If it returns `sellerStatus`/`bankAccountStatus`, stop and route the user to the Carteira Clickmax to finish payout registration — not fixable here. Offer it with a navigation CTA `action="open-page" path="/sales/wallet"` (the wallet lives at `/sales/wallet`, NEVER `/wallet`).
- Custom support email (only if the user wants one different from the account's): `mcp__plugin_clickmax_clickmax__offers_create_support_email` → user clicks the link sent to that inbox → confirm via `mcp__plugin_clickmax_clickmax__offers_list_support_emails` (`verifiedAt` set) → attach the id via `mcp__plugin_clickmax_clickmax__offers_update` (`offerSupportEmailId`). `mcp__plugin_clickmax_clickmax__offers_resend_support_email_validation` re-sends the link. The account email already satisfies the gate, so this is optional polish.
- **Product image:** to set or replace the product's main image, collect the image (ask the user to upload it) and then call `mcp__plugin_clickmax_clickmax__offers_set_product_image` with the offer id + the uploaded image URL. Do NOT use `offers_update` for this, and NEVER `bannerDesktop`/`bannerMobile` (separate checkout banner art). It is a common product pendency worth offering during product creation/completion.
- **Exact param names for the delivery/image tools (call them directly — no need to inspect the schema first):** `offers_set_product_image` takes `offerId` + `imageUrl` (the param is `imageUrl`, not `image`); `offers_add_file_delivery` takes `offerId` + `url` + `title` (+ optional `description`) for a SINGLE file — it is NOT an array and NOT a `files` field; `offers_add_link_delivery` takes `offerId` + `links`, where `links` IS an array of `{ title, url }`; `offers_add_membership_delivery` takes `offerId` + `portalId` + `classroomId`.

## Report

- Start with the offer identity and whether it is main or secondary.
- Then report lifecycle state, commercial settings changed or inspected, and any remaining blockers.
- For approval requests, say clearly `ready for approval` or list each blocking item.
- For create/clone/update/archive/unarchive/delete actions, state the action result first and keep follow-up actions opt-in.
- After a create/publish that finishes the requested work, follow `clickmax-getting-started` to close with at most one opt-in offer of the next setup task.

## Warnings

- Do not create a new secondary offer when the user really wants to modify the existing offer.
- Approval is not automatic; diagnostics matter. It is moderated by a human — never report an offer as approved/live just because it was submitted.
- `sellerStatus`/`bankAccountStatus` blockers are the seller's payout onboarding; no offer edit clears them.
- Never fabricate deliverable content — ask the user for the link, or build a members area; do not invent a URL or auto-generate files.
- Route images by intent: an image FOR the product ("add an image to product X", "imagem do produto") → `offers_set_product_image`, NEVER the banner. Only use `bannerDesktop`/`bannerMobile` (via `offers_update`) when the user explicitly asks for checkout banner art. A "product image" request must never end up in `offers_update`.
- Delete can be blocked by transaction history.

## Anti-patterns

- Treating product and offer as the same object.
- Sending to approval without checking blockers.
- Treating `externalUrl` or checkout `hash` as cosmetic fields.

---

Clickmax skill revision: `b8294822a4d6`
