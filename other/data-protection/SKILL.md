---
name: data-protection
description: Use when a feature collects, stores, exports or shares personal data, or when a new third party will receive it. Structured checklist, not legal advice.
---

# data-protection

Business layer (`business/README.md`), touching step 3 and step 6 of the dev pipeline. GDPR is where
an engineering decision quietly becomes a legal exposure, usually at the moment someone adds a field
"we might need later" or wires in a convenient third-party API.

**This is not legal advice.** It's the set of questions that, unasked, turn into a problem nobody can
fix cheaply afterwards. Where a question has a legal answer, the answer comes from a lawyer or the DPO,
not from here.

## When
As soon as a feature: adds a field holding personal data, exports or displays it in a new place, sends
it to a third party, or changes how long it's kept. Also when a new dependency or SaaS will process
it.

## Steps

### 1. Name the data and why you have it
1. **List the personal data this feature touches**, field by field. "Personal data" is wider than most
   engineers assume: a name, an email, an IP address, a device id, a photo, free-text notes that
   mention someone, and anything that identifies a person once combined with something else.
2. **Flag the special categories separately** — health, biometrics, union membership, religion, sexual
   orientation, criminal records. These carry much stricter obligations, and a "just a comment field"
   that ends up holding health information is the standard way of acquiring them by accident.
3. **State why each field exists**, in one sentence tied to the feature. A field nobody can justify is
   a field to remove: that's not a legal nicety, it's the cheapest way to shrink the problem.
4. **Collect the minimum.** "We might need it later" is not a purpose. Later, with a purpose, is when
   to add it.

**To keep this field list as a versioned file next to the code** that feeds the DPO's record of
processing activities, with a category on each field and a check in CI, read
[`references/05-processing-record.md`](./references/05-processing-record.md).

### 2. Settle the questions an engineer can't answer alone
Take these to the DPO/legal rather than guessing:
- **On what basis are we allowed to hold this?** (consent, contract, legal obligation, legitimate
  interest — they are not interchangeable and they have different consequences in the code)
- **If it's consent**: it has to be freely given and withdrawable. Withdrawable means there's a code
  path for withdrawal, which is a feature someone has to build.
- **How long do we keep it, and what happens at the end?** Deletion or anonymisation, and a mechanism
  that actually runs. A retention rule with no job behind it is a sentence in a document.
- **Does this need a formal impact assessment?** Large-scale, sensitive or systematic-monitoring
  processing may. That call isn't ours.

**For a French project, or a French DPO/legal team**, GDPR's open wording above ("appropriate",
"high risk") has a published, concrete answer from CNIL: the AIPD trigger grid, retention-period
figures by data category, the cookie-consent regime and the DPO-designation criteria are in
[`references/01-cnil-france.md`](./references/01-cnil-france.md). Read it before taking a retention
period or an AIPD call to the DPO, so the question arrives with CNIL's own figure attached rather
than "how long is normal?"

### 3. What the code has to provide
1. **Access and portability**: a person can ask what you hold about them. If satisfying that request
   means a developer writing a bespoke query each time, it will be slow and eventually wrong.
2. **Deletion**: an actual mechanism, and know what it does about backups, logs, analytics and search
   indexes. Deleting the row while the record survives in a search index and three log lines is the
   normal outcome of not asking.
3. **Correction**: editable, or a route to get it corrected.
4. **Never personal data in logs or URLs.** Same reasoning as credentials
   (`skills/auth-session-conventions` §2.1 and §2.4): logs have wider read access and longer retention
   than the system that produced them, and URLs travel into history, `Referer` and every proxy.
5. **Non-production environments.** A production dump in a dev database is a real disclosure with real
   consequences. Anonymise or generate; if you must copy, that's a decision someone senior takes
   knowingly.
6. **Access is scoped**: the same discipline as any authorisation
   (`skills/security-hardening` §3), applied to the data most likely to be requested.

**For a concrete Laravel/Nuxt shape of items 2, 4 and 5 above** — anonymising a record instead of a
hard delete, a scheduled purge job tied to a named retention figure, a cookie-consent integration,
and keeping personal data out of logs and exception reporters — see
[`references/02-code-patterns.md`](./references/02-code-patterns.md). Illustrative patterns to adapt,
not a certified implementation.

### 4. Third parties
1. **A new service that receives personal data is a decision, not a dependency choice.** It needs a
   data processing agreement, and where the data is hosted matters. Both are legal questions.
2. **Analytics, error reporting and session replay are the common unnoticed cases**: an exception
   reporter that serialises request bodies is exporting personal data to a third party, whatever the
   feature intended.
3. **Write down what leaves the system, to whom, and why** — you will be asked, and reconstructing it
   later from the code is much harder than noting it now.
4. **The broader security/compliance review of the vendor itself — not just the data-processing
   question — is `business/vendor-management`'s process.** This section covers what to ask about a
   vendor that will hold personal data specifically; that block covers assessing and tracking the
   vendor relationship generally.

### 5. Email marketing: three questions, no default answer
A marketing list is personal data with a channel attached, and three questions recur in every conversation about
it. This block answers none of them; the person who owns data protection does, for the countries concerned,
from the regulator's current published guidance.
1. **What evidence of consent do we hold for each address?** Who gave it, when, in what words and for which
   purpose, and whether we can show it later. A list without that record is a list nobody can defend.
2. **How long may the suppression list be kept?** It exists so a person is never mailed again, which argues for
   keeping it; the same person's data should not outlive its purpose, which argues for a limit. The answer is
   a decision with a named owner, not "forever" and not "delete with the rest".
3. **What applies to business-to-business mail?** A work address belongs to a person; whether it changes what is
   required before mailing them is a question for legal, not an assumption.
What CNIL's published pages state on the first and third question is in
[`references/01-cnil-france.md`](./references/01-cnil-france.md) point 6; the suppression-list question has no
answer there. For the design of the flows themselves, see `business/lifecycle-email-program-design-pitfalls`.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: the field list with a
purpose each, the questions routed to the DPO/legal with their answers when they come back, the
retention mechanism named, and the list of third parties receiving data. If the answers aren't in yet,
that's a blocker to state, not a reason to guess.

## Guardrails
- **Never decide a lawful basis or a retention period yourself.** Wrong here is expensive and
  invisible for a long time.
- **Never widen collection because it's convenient.** Every extra field is an obligation you now carry.
- Never copy production personal data to a local or shared dev environment on your own initiative.
- **When in doubt about whether something is personal data, treat it as if it is** and ask. The cost of
  asking is a message; the cost of being wrong is a notification obligation.

## Origin
**Sourcing pass 2026-10-20 (status stays 🟡, nothing was run).** Read for facts, rewritten in our own words:
CNIL pages on the AIPD (trigger grid: two of nine criteria, or a listed processing), the AIPD lists page, the
retention page and the retention guide (PDF), the cookies FAQ and the cookies recommendation page, the
register page, DPO designation, email prospecting and consent; each is a regulator's public page, no licence
statement read, so no text is reproduced. Confirmed: the AIPD trigger, the presumption-of-conformity wording,
the prospect retention rule, billing data kept 10 years, refusal as easy as acceptance, consent proof, register
contents and the narrow small-organisation exemption, the three mandatory DPO cases. Corrected: CNIL
describes DPO designation outside the mandatory cases as encouraged by the EDPB, not recommended by CNIL itself.
Still unverified: the 13- and 25-month cookie figures, the client "3 years after the end" figure, the
connection-log range. `references/02-code-patterns.md` stays our own engineering guidance.

Assembled from public sources: the GDPR text itself (lawful bases, data-subject rights, special
categories, impact assessments) and published regulator guidance. Written **without internal legal
expertise**, deliberately shaped as "which questions must reach a lawyer" rather than as answers. The
engineering consequences — logs and URLs, search indexes and backups surviving a deletion, exception
reporters exporting data unnoticed, non-production copies — are ours, and are the part this block adds
that a legal summary wouldn't.

**Email-marketing questions added 2026-10-20** (§5): three questions named from an email-marketing review,
with no law restated and no source of ours for any answer.

**Sectioned 2026-09-29**, following the split already used by `business/interface-design`,
`business/product-ownership` and `business/data-analytics`: this file is now the router, and two
`references/` files carry what a single generic GDPR file couldn't hold without either bloating past
the router's own budget or staying vague. `references/01-cnil-france.md` is sourced from CNIL's own
published guidance — its AIPD pages, its retention-period guide, its cookies recommendation/FAQ, its
DPO-designation guidance and its register-of-processing guidance, all cited by URL inline and checked
2026-09-29 — **not itself CNIL-endorsed**: it's this block's reading of CNIL's public documents,
same non-authoritative register as the rest of `business/`. One figure is flagged unresolved rather
than asserted: connection-log retention, where CNIL's own published range spans roughly 6 months to
1 year (`references/01-cnil-france.md` §1.2 states the range and defers the exact figure within it to
the DPO/legal team).
`references/02-code-patterns.md` is original engineering translation — Laravel/Nuxt patterns for
anonymisation, consent, scheduled purges and log scrubbing — written by us, not sourced from CNIL or
any external catalogue, and stated as illustrative rather than certified in its own opening
paragraph and guardrails.
`references/05-processing-record.md` (added 2026-10-16, 🟡 never dogfooded) restates GDPR Article 30
as published in the Official Journal, read on EUR-Lex 2026-10-16 (not the consolidated text), and
takes the field-annotation pattern from the `ethyca/fides` example files (Apache-2.0); the file says
which sentences are ours.

Independent verification 2026-10-21: 19 checked, 14 matched, 1 corrected, 4 unverified
