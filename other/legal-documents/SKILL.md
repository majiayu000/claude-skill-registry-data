---
name: legal-documents
description: "Use when a product needs its public legal set (terms, legal notice, privacy policy, cookie notice, DPA, SLA, EULA): which apply, who owns each, what engineering must supply."
---

# legal-documents

Business layer (`business/README.md`), legal. These documents are drafted by a lawyer and signed off by
a lawyer. What repeatedly goes wrong is upstream of that: **the drafting stalls because nobody can say
what the software actually does**, so it gets filled with a template, and the template then describes a
product that doesn't exist.

That gap is engineering's, and it's the only part this block owns. The copy-paste failure is the
expensive one: a document promising a 30-day deletion nobody implemented is a commitment, and it will be
read back to you.

## When
Before a first launch or a public beta; when a product starts charging, opens self-service signup,
enters a new country, or adds a subprocessor; when a lawyer asks for input on any of these documents.

## Steps

### 1. Identify which documents apply, don't assume the set
The set depends on what the product does and who it sells to — not on what a competitor publishes.
Candidates, and the question that decides each:

| Document | Applies when |
|---|---|
| Legal notice / publisher identification | there's a public site at all |
| Terms of use (usage rules) | users have accounts or can post content |
| Terms of sale / subscription terms | money changes hands, and B2B ≠ B2C |
| Privacy policy | any personal data is processed |
| Cookie / tracker notice | anything non-essential is set client-side |
| Data processing agreement (DPA) | we process personal data on a customer's behalf |
| Subprocessor list | third parties touch that data |
| SLA | availability or support is promised |
| Licence / EULA | software is delivered rather than hosted |
| Accessibility statement | required in some jurisdictions and sectors |

**Which of these are mandatory, and in what form, is a legal answer, per country.** Sector rules
(public procurement, finance, health) add more. Don't settle it from a blog post — see
`business/regulatory-watch` §1.

### 2. Supply the facts before the drafting starts
This is the deliverable. For each item, the true answer, not the intended one:
1. **What the service does**, in plain sentences, including what it deliberately doesn't do.
2. **Who the customer is** — business or consumer, which countries. Consumer rules are stricter and
   mostly non-waivable.
3. **What data is collected, why, and for how long** — reuse the field list from
   `business/data-protection` §1 rather than producing a second, divergent one.
4. **Where it's hosted and where it's processed**, including backups, and every third party that
   receives it, with what each does.
5. **Deletion and export: what actually happens**, mechanism by mechanism, including what survives in
   backups, logs and search indexes.
6. **Availability figures only if measured.** An uptime number in an SLA is a contractual commitment,
   and it needs a measurement definition behind it (`business/product-marketing` §2.2).
7. **Security measures actually in place**, present tense reserved for what's deployed.
8. **Licences of what we ship** — from `business/licence-compliance`, since attribution and copyleft
   obligations surface in the EULA.

### 2b. What official pages say about content (read 2026-10-20, facts only, not advice)
1. **Privacy notice contents.** The French data-protection regulator's page on informing people lists: who the
   controller is, purposes, legal basis, whether providing the data is mandatory, recipients, retention period
   or criteria, rights, a contact for data questions and the right to complain; and, depending on the case,
   transfers outside the EU with safeguards, automated decisions, and the right to withdraw consent. For
   indirect collection also the categories and the source. It asks for a layered approach with the essentials
   first, given at collection time, or within one month for indirect collection. Check each item against the
   field list of step 2.3: an item the product cannot answer is a gap, not a line to fill with a template.
2. **Consent is provable.** The same regulator says the controller must be able to show valid consent at any
   time, that withdrawal must be as simple as giving it, and that bundled consent for several purposes is not
   valid. This is the basis of step 4.3 and 4.2.
3. **Consumer information is regulated beyond the privacy notice.** The Commission's page on the consumer rights
   directive says it sets the information traders give before consumer contracts, a withdrawal right with a
   standard withdrawal form, and rules for digital content, with member states allowed to add requirements;
   the length of the withdrawal period was not on the page read. Whether it applies is a per-country, per-customer
   question for counsel.
4. **A national example of the legal notice.** The French business-service page lists, for a company website:
   company name, legal form, capital, registered office, contact details, registration number, VAT number where
   applicable, the host's name, address and phone, and the publication director; and states fines for missing
   identity mentions, missing data-protection information, missing sales terms for consumers and for a missing
   online cancellation function. Example of the shape of a rule, not a rule for any other country.

### 3. Keep the document and the code in step
1. **Every promise in a published document is a requirement with no ticket.** Retention periods,
   deletion deadlines, export formats, response times, notification windows: each needs something that
   runs, and it usually doesn't exist yet.
2. **List them explicitly when the document is signed off**, and turn them into work. This is the single
   highest-value thing engineering does here.
3. **A change in behaviour can require a change in the document**, and sometimes prior notice to users.
   Adding a subprocessor is the standard example.
4. **Versions and dates matter.** Users accepted a specific version; keep the history and the record of
   who accepted what and when. Reconstructing consent later is not possible.

### 4. Publishing and accepting
1. **Reachable without an account**, and stable URLs — they get cited in contracts.
2. **Acceptance is recorded**, with the version, if acceptance is being relied on.
3. **Never a pre-ticked box, never bundled consent** where consent is the basis
   (`business/data-protection` §2).
4. **Nothing is published until the owner has approved that version.** Not a draft, not "temporarily".

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the applicable-document list with its owner, the
factual input pack of §2, the list of commitments the signed documents impose on the code, and the
version/acceptance record. Anything unanswered is stated as unanswered.

## Guardrails
- **Never publish a legal document not approved by whoever owns legal.** A template found online is
  drafted for another product, another country and another customer type.
- **Never write a commitment nobody implemented** — a retention period, an SLA figure, a deletion
  deadline, a support response time.
- **Never assume France, or any single country.** A group operating across several countries has a
  different set per country, and consumer rules in particular don't travel.
- **Never state a legal obligation from a secondary source.** Blogs summarising the law are how a wrong
  article number ends up in a document.
- This block produces **input for a lawyer**, never the document itself, and never an opinion on whether
  a clause is enforceable.

## Origin
**Sourcing pass 2026-10-20 (status stays 🟡, nothing was run).** Read for facts, own words, no text copied: the
French data-protection regulator's pages on informing people and on consent, the French business-service pages
on website mentions and on invoicing, and the European Commission's consumer rights directive page. Confirmed:
the factual-input approach (a privacy notice cannot be written without the field list, retention and recipients
that step 2 asks for) and the consent-record and version-record points (step 3.4, 4.2). Added: point 2b. Not
verified: the document table's "applies when" column (it is our inventory; the pages read cover only the notice,
consent, consumer information and French legal notice), the accessibility statement row (the Commission page read
did not mention a statement and gave no application date), the DPA content (the regulator's processor-contract
page returned not found; the EDPB guideline page gave no text), and the service-level and EULA rows.

Structure taken from Anthropic's `claude-for-legal` plugin suite, which is explicit that every output is
a draft for attorney review and that jurisdiction assumptions must be surfaced rather than left
implicit — both adopted here. The document inventory reflects the set of public documents a hosted
software product is commonly asked for; **which are mandatory is deliberately left as a question for
counsel**, because the accessible sources on it are commercial content marketing rather than the law.
Also informed by a survey of community legal skills for Claude (contract review, policy generation, GRC
framework packs): they generate the documents, which is exactly the step we refuse to take.

Written **without internal legal expertise**. What's ours: the framing that the real engineering
deliverable is the factual input pack, and §3 — every published promise is an unticketed requirement,
which is the failure this block exists to prevent. Verified 2026-08-06.
