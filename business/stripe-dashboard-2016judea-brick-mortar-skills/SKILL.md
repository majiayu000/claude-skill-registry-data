---
name: stripe-dashboard
description: Operate your own Stripe account(s) — via the API where it works and a logged-in browser where it does not. Use for "mint a Stripe key", "update the branding/logo/icon on Stripe", "change the statement descriptor", "turn on receipts", "create a payment link", "spot-check our Stripe links", "make the checkout look like the site", "invoice a customer". Carries the one fact that costs a cycle every time — your own account's settings cannot be written through the API — and the exact dashboard mechanics that do work.
---

# Stripe: API first, dashboard for the rest

## Rule 1 — split the work by what the API can touch

**The API can:** products, prices, payment links (create/update/deactivate, incl.
`invoice_creation`, `payment_method_types`, custom fields, `submit_type=donate`), checkout
sessions, customers, invoices, files (`files.stripe.com/v1/files`, purpose
`business_logo` / `business_icon`), reading `/v1/account`.

**The API cannot:** write your own account. `POST /v1/account` returns 403 *"you may only
use it on connected accounts"* even with a full key. That covers branding (logo, icon,
colours), public details (name, support email/URL, website), statement descriptor,
dashboard timezone, and the customer-email toggles. All of that is the dashboard, in a
browser session. Do every API step first, then one browser pass per page.

**Verify every dashboard write by reading `/v1/account` back** — the page says "saved" for
things it did not save (e.g. a Save click that landed after a fullPage screenshot resized
the viewport).

## Rule 2 — the verification step is passable, but it is the owner's

Creating a secret key, or changing identity-class fields, opens **"Verification
required"**. A passkey prompt is the owner's to complete. The email route is: Stripe mails
"Your Stripe verification link" — open it **in the same browser instance** that holds the
session (a second launch with the same `--user-data-dir` hands the URL to the running
instance; `curl` proves nothing) — then Stripe texts a 6-digit code to the account phone.
In an OTP widget, click the first box and `keyboard.press("Digit<n>")` per digit; setting
`.value` fails.

If you script it, run the whole wizard as one browser-automation script (one connect per
launch) and have it poll a `code.txt` so a human or another tool can supply the code.
Restricted key of choice: **"Full access — except sensitive operations"** (no payouts or
transfers).

## Rule 3 — dashboard mechanics that actually work

- Modals are `role="alertdialog"`, and the Setup-guide widget is a visible `role="dialog"`
  that will be the `.pop()` of any dialog query. Scope to the alertdialog, or search the
  whole document for a visible button by text.
- Buttons are often `<a>` or a `Pressable` div. Find by trimmed innerText across
  `button,a,[role=button]`, `scrollIntoView`, then `mouse.click` at the centre.
- The one `input[type=text]` you find may be the global Search box. Scope by `name`
  (`business_profile[support_email]`, `settings[payments][statement_descriptor]`) and set
  via the native value setter + `input` + `change` + `blur`.
- **Branding page** (`/acct_.../settings/branding`): `[data-testid="branding-icon-upload"]`
  and `branding-logo-upload`. An empty slot is a hidden `input[type=file]` -> `uploadFile`.
  A filled slot has no chooser: click the slot, then its **top-right corner (x+w-2, y+2)** —
  the × — and a fresh file input appears. Colour inputs are the text inputs whose value
  equals the current hex without `#`. Then the visible "Save changes" button.
- **Public details** (`/settings/business-details` -> "Customer-facing information" ->
  Edit): fields by `name`; the Save is a hidden submit — `requestSubmit()` on the form of any
  field saves it. Same page, "Statement descriptor" -> Edit.
- **Timezone** (`/settings/account`): a `button[role=combobox]` under "Time zone"; click,
  type the city, click the `[role=option]`, Save.
- **Customer emails** (`/settings/emails`): "Successful payments" and "Refunds" toggles
  auto-save on click and are often OFF by default — check them. Re-read on a fresh launch,
  not `page.reload` (networkidle never settles on the dashboard).
- Take viewport screenshots only. `fullPage:true` changes the layout and every coordinate
  after it.

## Rule 4 — link hygiene

- A payment link printed on paper (a mailer QR code) is **never deactivated**. Grep your
  print assets for `https://buy\.stripe\.com/\w+` before any cleanup.
- A link whose after-payment page now redirects somewhere unrelated **is** deactivated: a
  paid purchase that lands on a homepage is a broken promise.
- Every live link gets `invoice_creation[enabled]=true` with a description and a footer
  carrying the support address, `customer_creation=always`, and
  `payment_method_types[]=card,link` — buy-now-pay-later on a small digital product is
  noise the buyer pays for in attention.
- Checkout Sessions carry the same flags; test a change by creating a live session with the
  new params and expiring it (`/v1/checkout/sessions/{id}/expire`) — no charge, real
  validation.
- **Register every checkout host as a payment method domain**, or embedded Checkout silently
  hides Apple Pay and Google Pay: `GET /v1/payment_method_domains`, and `POST` with
  `domain_name=<host>` if missing (free, instant).

## Rule 5 — leave the machine clean

Kill any automated browser and delete the copied profile (it holds live session cookies);
delete any scratch file holding a key. A key's only homes are your `.env` and your host's
environment variables (to rotate on Vercel: delete the old env id, add the new one, then
redeploy).
