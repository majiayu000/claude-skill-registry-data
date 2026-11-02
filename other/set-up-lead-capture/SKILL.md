---
name: set-up-lead-capture
description: Use when adding or hardening a signup, contact, newsletter, or waitlist form on a public page — form contract, one destination seam, layered spam defense (honeypot, time-trap, Turnstile), GDPR/TDDDG-aware consent, double opt-in.
---

# Set Up Lead Capture

A landing page exists to convert; this form is the conversion. The skill wires it with
one destination seam, invisible-first spam defenses, and consent that would survive an
audit.

## 1. Gate — is this a public page?

Run the gate from `../_shared/page-types.md`. Authenticated app forms (settings,
checkout, CRUD) are the other catalogue's job: `skills/frontend/set-up-forms`
(schema-first, mutation-wired). This skill owns the *public, anonymous* form.

## 2. Audit current state

```bash
curl -s "$URL" -o /tmp/page.html
grep -oiE "<form[^>]*" /tmp/page.html              # how many forms, where do they post?
grep -ciE "<label" /tmp/page.html                   # labels present?
grep -ciE "autocomplete=" /tmp/page.html
grep -ciE "type=\"checkbox\"[^>]*consent|consent[^>]*checkbox" /tmp/page.html
```

Findings to look for: forms posting directly to a vendor URL scattered per page (no
seam), missing labels, no spam defense, no consent checkbox, success state that dumps
PII into the URL. (As in `../set-up-seo/SKILL.md`: the greps are coarse presence checks on double-quoted
attributes — the consent pattern will also match prose mentioning consent and checkbox;
read the page, don't trust the counts.)

## 3. The form contract

```html
<form method="post" action="/api/leads">
  <label for="lead-email">Work email</label>
  <input id="lead-email" name="email" type="email" autocomplete="email"
         required aria-describedby="lead-email-err">
  <p id="lead-email-err" class="field-error" hidden></p>

  <!-- honeypot: bots autofill it; humans never see it. No aria-hidden — it would
       strand a focusable input in a hidden subtree; the label warns anyone who lands here -->
  <div class="hp">
    <label for="lead-company2">Leave this field empty</label>
    <input id="lead-company2" name="company2" type="text" tabindex="-1" autocomplete="off">
  </div>
  <!-- time-trap: must be stamped per page LOAD (SSR per request, or inline JS) —
       a build-time value on a static page never trips the check -->
  <input type="hidden" name="form_ts" value="{{render_timestamp}}">

  <!-- newsletter/marketing forms only. A contact form that just answers the request
       needs no marketing checkbox — a privacy notice link beside the button instead. -->
  <label class="consent">
    <input type="checkbox" name="consent" required>
    I'd like to receive the newsletter — see the <a href="/privacy">privacy policy</a>.
  </label>

  <button type="submit">Get the guide</button>
  <p role="status" class="form-feedback"></p>
</form>
```

```css
.hp { position: absolute; left: -9999px; }   /* off-screen: the laziest bots skip display:none; the field existing is the real trap */
```

- Minimal fields — each extra field costs conversions and widens PII. Often email alone.
- Real `<label>`s; `autocomplete` for WCAG 1.3.5 input purpose, `type="email"` for the
  right mobile keyboard.
- Error state: inline, per field, announced (`aria-describedby` — the field-level
  channel). Success state: the `role="status"` element — the form-level channel —
  with visible confirmation **that says what happens next** ("Check your inbox to
  confirm"). One message per channel; don't announce the same thing twice.

## 4. The destination seam

All forms post to **one** endpoint/handler; the vendor (CRM, list provider, webhook)
lives behind it, named in one place. Shapes and trade-offs: `./capture-patterns.md`.
The handler's contract — whatever implements it:

1. Reject silently (normal success response, record dropped) if `company2` is non-empty,
   or if `form_ts` is present and `now − form_ts < 3 s`. A missing `form_ts` (JS off on
   a static page) degrades gracefully — the honeypot still guards. A bot can forge a
   plain timestamp; if the time-trap matters, issue it server-side signed (HMAC), and
   verify the signature.
2. Validate the email server-side; honest inline error for real mistakes.
3. Rate-limit by IP.
4. Store: `{ email, consent: true, consent_text_version, submitted_at, source_page }`.
5. Trigger the double-opt-in confirmation; the address is *used* only after the click.

## 5. Spam defenses — escalate, invisible first

The honeypot is free, invisible, and static-safe — it goes in always. The time-trap
needs a **per-load** `form_ts` (SSR per request, or a one-line inline script setting
`Date.now()` on load); on a fully static page a build-time timestamp never trips the
check, so treat the time-trap as an upgrade where rendering allows, not a given.
Escalate to Cloudflare Turnstile (managed mode) only when measured spam pressure
demands; an interactive challenge is the last resort, because every challenge costs
real conversions. Turnstile is a third-party script and has privacy consequences in the
EU (`./capture-patterns.md`) — one more reason it is the escalation, not the default.
Server-side `siteverify` is mandatory; the widget alone protects nothing. Snippets and
rejection etiquette: `./capture-patterns.md`.

## 6. Consent + double opt-in

- Checkbox **unticked** by default; specific text; policy linked. Pre-ticked or bundled
  consent isn't consent (GDPR recital 32; CJEU *Planet49*, C-673/17).
- Record consent (timestamp + text version) with the lead. The advertiser must be able
  to prove consent (GDPR Art. 7(1)); a bare "ticked" boolean proves little.
- Double opt-in: store unconfirmed → confirmation email → only confirmed addresses enter
  the list. Not required by statute, but in Germany it is the accepted way to prove
  consent for marketing email (UWG §7(2) no. 3 needs prior express consent). Keep the
  confirmation email free of promotion — German courts have treated promotional
  confirmation mails as unsolicited advertising — and log the confirmation click.
- Engineering guidance, not legal advice. A regulated project encodes its counsel's
  rules via `../audit-copy-compliance/SKILL.md`.

## 7. Verify

- Valid submit → success state, record stored with consent fields, confirmation mail
  flow triggers.
- Fill the hidden `company2` field → normal success response, **no** record.
- Submit within 3 s of load → no record (on per-load `form_ts` setups).
- Bad email → inline error names the field.
- View the page with JS disabled: the form is present and labeled (it's in the HTML).

## References
- ./capture-patterns.md — destination shapes, spam escalation, silent rejection, consent recording, PII minimization, when to deviate.
- ../_shared/page-types.md — the gate.
- ../../frontend/set-up-forms/SKILL.md — authenticated in-app forms (schema-first, mutation-wired); use that skill there.
