---
name: integrations
description: This skill should be used when the product talks to a platform you do not control — receiving webhooks, syncing with a CRM, ERP, e-commerce or calendar API, connecting a user's Google or Meta account over OAuth, sending through WhatsApp or another messaging API, or sending transactional email. Trigger phrases (English) include "integrate with", "connect to the X API", "receive a webhook", "the webhook isn't firing", "sync with", "import from their API", "OAuth with Google", "refresh token", "send transactional email", "their API returns", "pagination". Trigger phrases (Spanish) include "integrar con", "conectar con la API de", "recibir un webhook", "el webhook no llega", "sincronizar con", "importar desde su API", "conectar la cuenta de Google", "mandar mails transaccionales". It designs the integration so that a third party being late, wrong, duplicated or down does not corrupt your data or fail silently. For Stripe and payment webhooks specifically, use `payments`.
---

# Integrations

Your own code does what you wrote. A third party does what it does today, which may differ from its documentation, from yesterday, and from its sandbox. This skill designs for that.

Analogy: an integration is a business partner in another time zone who answers by post. Letters arrive twice, out of order, or not at all, and sometimes the letter says "done" when nothing was done. You don't run the business on the letters — you keep your own books and reconcile.

## Discovery (max 3 questions, only if unknown)

1. Direction — do you **read** from them, **write** to them, or both?
2. Do they push events (webhooks), or do you pull?
3. Is the connection per-product (one key of yours) or per-customer (each user connects their own account)?

## Step 1 — Inbound: treat the webhook as a doorbell

**Take only the id from the webhook, then fetch the object from their API with your own credentials.** Never write the webhook body into your tables.

This one decision removes a family of problems: forged payloads, bodies re-serialized by a gateway (which breaks signature checks), events arriving out of order, and fields that are empty in the event but present in the API.

Around it:
- **Verify the signature — and reject when it is missing.** A handler that skips verification if no signature header arrives has no verification.
- **Deduplicate by their event or message id**, stored with a unique constraint. Deliveries repeat.
- **Batched webhooks: one bad item must not stop the rest.** `try/catch` per item, persist before you enqueue, and never `return` out of the loop when one entry belongs to an unknown account — the other tenants in the same request go silent.
- **Expect your own writes to come back.** Change something through their API and the webhook reports it to you; without a guard it overwrites the state you just set.
- **Never depend on the webhook alone.** Build the pull path too — a "sync now" action that rings the same doorbell by hand, or a reconciliation job. Webhooks get registered and then never fire, and you find out from a customer.

## Step 2 — Outbound: "they said no" is not "I don't know"

Classify every response from a write:

| What came back | Meaning | Tell the user |
| --- | --- | --- |
| 2xx | Done | Done |
| 4xx | **They refused.** Nothing changed | Their reason |
| 5xx, timeout, connection dropped | **Unknown.** It may have gone through | "We couldn't confirm — check before trying again" |

Showing "nothing was changed" on a gateway error invites a retry, and the end customer receives the notification twice.

- **The user's main action never waits on the third party.** Save first, sync after; a failed sync is a visible state on the record, not a failed save.
- **Send dates as ISO-8601 with an explicit offset.** A timestamp without a zone moved a real appointment by three hours — and notified the customer.
- **Find out in the sandbox what each omitted field does.** Leaving a field out of an update is not always "keep it": one provider re-ran its own assignment logic and gave the appointment to a different person.
- **Trust the response you receive, not the one documented.** Field names differ.

## Step 3 — Reading: don't believe the pagination

- **Stop on an empty page, not on `has_more: false`.** One API reported no more pages with 33 customers still pending.
- **Reconcile against an independent total** — a report, an invoice sum, a count from their UI. Coming up short is otherwise invisible.
- **Compare ids, not counts.** A date-range filter that returns the right number of the wrong records looks fine.
- **Batch id lists.** A hundred ids in a query string produced a gateway error; so did sixty parallel requests. Chunk both.
- **Paginate your own reads too**: auto-generated APIs cap rows per request (commonly 1000) and return a truncated list without an error.

## Step 4 — Credentials that expire

- **Long-lived tokens still expire.** Schedule the renewal and alert when it fails; the alternative is discovering it when the integration stops.
- **Single-use refresh tokens need a lock.** Two processes refreshing at once invalidate each other; take a database lock so only one renews.
- **Adding a scope does not update existing installations.** They fail with 401 until each customer reconnects — plan the migration.
- **Per-user OAuth (Google and similar):**
  - Validate the **scopes actually granted** in the token response. Consent screens let the user untick one; the integration then shows "connected" and fails later.
  - To request an extra scope from a signed-in user, **link the identity** rather than starting a new sign-in — a new sign-in with a different account switches users and their data "disappears".
  - "Disconnect" must **revoke at the provider**, not just delete your row — especially if your privacy policy says so.
  - The provider validates the **full redirect URL**, not the origin.
  - Sign-up metadata (a chosen role, a plan) does not survive the OAuth round trip; carry it in the return URL.

## Step 5 — Test what you think you are testing

- **A 403 alone proves nothing. Test both ends**: rejected without the secret *and* accepted with it. A misspelled header name returns the same 403 as a working guard.
- **A 200 is not success** until you have read the body. A wrong path can return an HTML page with status 200.
- **Simulated events answer simulated questions.** "Does the real event carry the email?" is answered only by a real event.
- **Never test against contacts that might be real people.** Sandbox data with a plausible email address is someone's inbox. Use addresses you own, and put guards in test tooling so a missing argument cannot write to a live record.
- **Check the credential's prefix before storing it.** A live key saved under a variable named "test" charges real money.
- **Write down what you could not measure**, as "no evidence", instead of assuming.

## Step 6 — When a hop is added, the failure mode is added too

Moving logic to another service inserts a network hop. Each hop needs: a retry, an emergency branch that still records that the user wrote, and an alert that is separate from the run status — because a handled failure finishes green.

## Step 7 — Transactional email

- **Best-effort, but logged.** A failed email must not break the action that triggered it; a rejected one must be distinguishable from a sent one. Check the SDK's returned error.
- **One-click unsubscribe is a POST.** Link scanners follow every GET in a message; a GET that unsubscribes will be triggered by security software. Link to a page with a button and set the `List-Unsubscribe` and `List-Unsubscribe-Post` headers.
- **Verify your sending domain** before you need to email anyone but yourself.
- **Escape user-supplied values** in HTML bodies, and restrict what a visitor's name can contain when it ends up in an invitation sent to a third party.
- **Provider templates default to English** — translate them before launch.
- **Respect the provider's rate limit** in loops; add a delay.

## Output

Deliver: the direction and trust model, the webhook handler (signature, dedupe, doorbell fetch, per-item isolation), the reconciliation path, the response classification for writes with the user-facing message for each, the credential-renewal plan, and the both-ends test. List anything the sandbox could not confirm.

## Field notes

`references/field-notes.md` — what each rule cost before it was a rule.

## Reference

The provider's own API reference and changelog (read the current version, then verify against real responses), RFC 8058 (one-click unsubscribe), Stripe's webhook best practices (general guidance that applies to any provider). Pairs with `payments`, `api-design` (idempotency), `secure-coding` (secrets, signatures) and `ai-features` (chat platforms).
