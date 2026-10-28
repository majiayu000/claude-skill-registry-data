---
name: lab-ordering
description: "Place lab supply orders from member requests — route by request header to Amazon Business, the Pritzker Lab Google Form, or a direct vendor; stage the cart/form and stop for human review before any purchase. Use when the user pastes an order request or asks to order supplies, place an order, or fill the Pritzker form."
---

# Lab Ordering Skill

Use this skill when the user pastes a lab order request (a field table of
Requested by / Item / Link / Part # / Quantity / Project-grant / Urgency /
Notes) or asks to place/stage a supply order.

Keywords: order, ordering, purchase, supplies, Amazon Business, Pritzker, cart,
catalog number, restock, requisition.

## Golden rules (never violate)

1. **Never complete a purchase or final form submission.** Always stage the
   order and STOP for the user's review.
2. **Confirm the funding source with the user before staging any order.**
3. **Flag every discrepancy** (price vs. quote, out of stock, ambiguous item,
   login required, more items than a form holds).
4. If the request is for the **CLEAN LAB**, emit a CAPITAL-LETTERS alert once
   the order is staged (see Clean Lab Alert below).

## Step 0 — Load config (bootstrap if missing)

Read `~/.config/lab_ordering/config.yaml`.

- If it exists, load `identity`, `pritzker_form_url`, `amazon_business_url`,
  and `funding_sources`.
- If it is missing, tell the user and walk them through creating it: copy the
  layout from `references/config.example.yaml`, ask for each value, and write
  the completed file to `~/.config/lab_ordering/config.yaml`. Never store these
  values in the skill repo.

## Step 1 — Parse the request

Extract, per item: item description, vendor/company, catalog/part #, quantity,
product URL, plus request-level: requester name, urgency, notes/flags, and the
stated project/grant. Field names are fuzzy — map synonyms (Part # = Catalog #,
Project/grant = Account, etc.). A request may list **multiple items**.

## Step 2 — Determine the route (decision tree)

Read the request **header / first line**:

- Contains "Amazon" -> **Amazon Business** (see `references/amazon_business.md`)
- Contains "Pritzker" -> **Pritzker Google Form** (see `references/pritzker_form.md`)
- Otherwise -> **Direct from vendor** (see `references/direct_vendor.md`)

Note any flags in the header (e.g. "Clean Lab").

## Step 3 — Confirm funding source

Before touching a browser:

- If the request's project/grant is "To be determined by Bruno", blank, or
  unclear, ask the user.
- Otherwise propose the best match from `funding_sources` and ask the user to
  confirm.
- Carry the confirmed `detail` string forward:
  - Amazon -> PO field at checkout review.
  - Pritzker -> "Account to be charged".
  - Direct vendor -> PO/notes field if present, else the review summary.

## Step 4 — Pick the browser method (environment-agnostic)

1. If a Claude-for-Chrome / computer-use browser tool is available, use the
   user's real (already-authenticated) Chrome. Preferred.
2. Else if in Claude Code, use the webapp-testing (Playwright) skill, and warn
   the user that logins will be required in the fresh browser.
3. If no browser control is available, fill in every value as text and give the
   user a ready-to-paste summary to drive the browser themselves.

Always begin the route by **checking login state**; pause if not authenticated.

## Step 5 — Execute the route

Follow the matching reference file. Default to the **cheapest shipping** unless
the request notes ask for faster. Check availability/in-stock before staging.

## Step 6 — Stop and report

Present a review summary table for each item: item, catalog #, quantity, price
seen vs. quoted, link, funding account, shipping. List all flags. Then STOP and
wait for the user — do not purchase or submit.

## Clean Lab Alert

If the request header/flags indicate the CLEAN LAB, after staging output a
prominent capital-letters alert, e.g.:

```
*** CLEAN LAB ORDER — THIS ORDER IS FOR THE CLEAN LAB. HANDLE / STORE ACCORDINGLY. ***
```

## Available resources

- `references/pritzker_form.md` — Pritzker form field mapping and fill steps.
- `references/amazon_business.md` — Amazon Business cart + PO-field review.
- `references/direct_vendor.md` — generic vendor cart-and-review.
- `references/config.example.yaml` — placeholder config layout.
