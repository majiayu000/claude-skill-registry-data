---
name: records-request
description: Get a specific record out of a US government office by public-records request — "request the assessor's model", "file a data practices request", "FOIA this", "open records request", "can we just ask the county for it", "who do I write to at <county>", "chase that request", "did they ever answer". Covers checking the website first, finding the right office and statute, the carve-out paragraph that makes a request answerable instead of refused, web-form traps (hidden character caps, WAFs that reject apostrophes), chasing (there is usually no deadline), whether what comes back may be republished, and parsing multi-year tables without silent errors.
---

# Records requests

**Goal:** a named document in hand, cheaply, without annoying an office you want more from
later. **Done** = the file is on disk, cached, with its provenance and its rights position
recorded — or a written "we don't have that", which closes the file and is also a win.

**The gate: a human sends.** Draft it, verify the recipient, put it in a file, say it's a
draft, stop. A portal with a CAPTCHA and a signature checkbox can only ever be the human.

---

## Step 0 — read the website first. The cheapest rule here.

Before drafting anything, look for the document on the office's own site.

**A published fee schedule is evidence the office gets asked, not evidence the answer costs
money.** One county was reported as *selling* its capitalization-rate study for $34.50 a
year, and published four years of the same thing free on its statistics page. One page fetch
saved the money and three weeks of waiting.

Then check the neighbours: a state agency may publish an aggregate the county won't (but read
what it actually covers — a state "cap rate study" may cover only state-assessed utility and
railroad property). And confirm the negative properly: search the office's published reports
for your terms. That negative is what makes the request the only route in.

## Step 1 — find the office, and get its name right

**The office is not called the same thing in two states.** Writing to the wrong body gets
nothing back. For commercial property valuation, for example:

| state | who values commercial property |
|---|---|
| MN, IA, NE | County **Assessor** |
| KS | County **Appraiser** |
| ND | County **Director of Tax Equalization** |
| SD | County **Director of Equalization** |
| **WI** | **no county assessors** — assessment is municipal, so write to the **city** |

Also: some states fold the big city into the county's assessor (Iowa: Polk covers Des
Moines); others don't (ND: Fargo and Cass are separate).

**Route priority: email, portal, post.**
- **Email** wherever an address exists. Verify it on the office's own page.
- **Portal** (GovQA, NextRequest) only when no address is published. Portals need a human
  for the account, the CAPTCHA and the binding signature checkbox.
- **Post** last; note it in the draft header as the fallback.

Some pages render by script and `curl` returns nothing useful. Strip tags in Python and
search for `@`; if there is genuinely no address, say so rather than guessing one.

## Step 2 — the carve-out paragraph is the whole request

**Name the confidentiality statute yourself and disclaim it, in the letter.** Without that
paragraph the request gets refused wholesale, because the confidentiality provision is what
the office reaches for by reflex. With it, the question stops being "can we release this" and
becomes "which of our own tables did you mean."

Ask only for the office's **own derived, countywide schedules and studies**, carrying no
parcel-level or owner-identifiable data, and offer to take a mixed document with the
owner-submitted parts redacted.

Provisions used successfully for assessor requests (verify against current statute):

| state | request under | disclaim |
|---|---|---|
| MN | Minn. Stat. 13.03 subd. 3 | **13.51 subd. 2** — owner-submitted income/expense, vacancy factors, rentable areas, leases |
| KS | K.S.A. 45-215 et seq. (custodian: 45-218) | 45-221(b) — taxpayer financial info furnished to the appraiser |
| IA | Iowa Code ch. 22 | 22.7 trade secret — *and cite 441.21(3)(a), which affirmatively requires disclosure of the formula or method*, plus 441.19(1)(a) |
| NE | Neb. Rev. Stat. 84-712 | 84-712.05(3) trade secret / proprietary |
| ND | N.D.C.C. 44-04-18 | 44-04-18.4 trade secret / commercial |
| SD | SDCL 1-27-1 | that state's assessor-confidentiality equivalent |

**Where a statute compels disclosure, cite it** (Iowa above): it pre-empts the
confidentiality reflex entirely.

**Do not reword a body that has been accepted.** Once one office accepts your wording, reuse
it verbatim for its peers, swapping only the name; a reworded version invites a second round
of scoping questions. Verify the paragraph survived any bulk edit by hashing it against the
accepted original.

## Step 3 — three things to put in the first letter, always

1. **Ask for five years, not one.** *"Assessment years 2022 through 2026 inclusive."* Same
   search for the office, five times the data — and the series is often the product (it shows
   how the office moved its own rates). Add: *"Send whichever years you hold; a partial answer
   is a useful answer,"* so a missing year doesn't stall the reply.
2. **Give them a cheap exit.** *"If the Office does not maintain schedules of this kind, a
   one-line answer saying so closes this out and I will not follow up."* A written no is a
   closed file, and costs them thirty seconds instead of a refusal letter.
3. **Ask for the fee estimate first.** *"If filling this would incur a fee, tell me the
   estimate first and I will narrow the request."* Some offices bill hourly to locate **and**
   hourly to redact — two meters at once.

## Step 4 — before a batch send

- **MX-check every recipient domain:** `dig +short MX <domain>`. Catches a typo before
  nineteen bounces.
- **Read one full body end to end.** Not the diff, the letter.
- **Keep the requester identity consistent** across a campaign (same person or same company,
  same address) so replies thread and nobody re-asks who you are.
- Send as **plain text**. Hard-wrapped letters collapse in HTML.

## Step 4b — a web form is a hostile channel. Budget for two traps.

1. **A character cap you are not told about.** A message field can silently truncate a
   2,000-character body at 1,000. For any form, write a **short variant up front**: statute
   cite, the ask with its year range, the confidentiality disclaimer, the fee-estimate line,
   contact. The disclaimer is the last thing to cut.
2. **A Web Application Firewall that rejects the payload outright** (`Event Type: signature`).
   The cause is punctuation, not length: **a bare apostrophe is the standard SQL-injection
   signature.** Scrub the body **and the subject** of `'` `"` `(` `)` `&` `/` `;` `=` `<` `>`
   `--` and non-ASCII. Write "and" for "&", drop statute subsections rather than parenthesise
   them, say "your Office derived" instead of "the Office's". Audit it in code:

       python3 -c "s=open('body.txt').read(); print({c:s.count(c) for c in \"'\\\"()&/;=<>\" if c in s})"

**Know the fallback before you start:** offices that hide an email still publish a street
address. A form that fights you for three rounds is not worth a fourth; post it.

## Step 5 — record the send, or it never happened

**Keep the statutory subject line** — a records officer routes on it, and replies thread
under it. Flip each draft's header from `NOT SENT` to `SENT <date> from <address>, messageId
<id>`, keep the body verbatim beneath as the record, and update your tracker. **Re-read every
row a bulk edit touched**: a global find-and-replace on a status column will happily mark
unsent web-form rows as SENT.

## Step 5b — replies that need an attachment

Some mail MCPs (Zoho's, for one) have no attachment upload. Send that reply through a
transactional provider (e.g. Mailgun) from the same address, threaded onto the office's
message with `h:In-Reply-To` and `h:References` set to their `Message-ID`, keeping their
subject. With curl, use **`--form-string` for every header and body field** — `-F` treats a
value beginning with `<` (every Message-ID) or `@` as "read this file". Confirm delivery from
the provider's events API.

**An office's own form is usually on its website.** If it's a flat PDF, overlay text with
reportlab, put long specifications on a page 2, and **render the page to PNG and look at it**
before sending (text lands on top of labels more often than you'd think).

**Narrow when you return a form.** A fee warning is the moment to say what you already hold
and ask only for the rest, estimate first.

**A soft no that names the inputs is not a no on the derived tables.** "We use data from
rental surveys, which is confidential" answers one item by pointing at confidential inputs
and skips the derived study. Re-ask the skipped items as yes/no, thank them, and offer the
one-line exit again. Stay courteous: you want this office's next answer too.

## Step 6 — chase, because there is usually no deadline

**The short clock is often not yours.** A portal's "10 business days" may apply only to a
**data subject** asking about themselves. A general request for government data commonly gets
"a reasonable time" (e.g. Minn. Stat. 13.03 subd. 3), which sets no clock at all. **Follow-up
is the only pressure.** Queue a chase about two weeks out the day it goes (see the
`pending-queue` hook), with the reference number, portal path, named contact and "do not
reword the request" in it. A chase is a status check; never re-scope in a follow-up.

## Step 7 — may what came back be republished?

Answer this **before** building anything on it.

- **Minnesota: yes, including commercially.** An agency must permit "unrestricted use of that
  data, even for commercial purposes, absent specific statutory authority to the contrary" —
  MN Attorney General opinion 852 (1995).
- **Everywhere: facts carry no copyright** (*Feist*) — only a particular selection or
  arrangement can. **Republish the numbers, never their document layout.** Re-express into
  your own schema.
- **Elsewhere, the use half is unsettled.** Read that state's commercial-use clause before
  claiming it, and mark your own files honestly ("not yet cleared for republication" is your
  marker, not the office's restriction — don't cite it as one).

## Step 8 — parsing what arrives

Cache the original next to the parsed output with a sha256 and the canonical URL, and never
re-fetch.

**Labels drift between years.** One county's own row labels went 22, 22, 18, 18 across four
annual sheets, with property types vanishing. **Hand-write the crosswalk and keep the raw
label verbatim on every record. Never fuzzy-match** — that is how a wrong number ships
looking right. A type that disappears is *absent*, not zero.

**Don't trust a regex over `pdftotext` output to tell you the structure.** A character class
missing digits truncated `Warehouse <25% Office / >20K` at the `2` and silently merged four
rows into two. **Check the row count against the source before believing your extraction.**

**Prove a cross-source join on source #2 before selling breadth.** Two counties in the same
state, same document type, can share **zero** exact property-type names.
