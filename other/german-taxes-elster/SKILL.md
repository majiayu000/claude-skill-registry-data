---
name: german-taxes-elster
description: "Prepare German taxes with an AI agent for founders and solopreneurs: personal Einkommensteuer and small-company (UG/GmbH) Umsatzsteuer-Voranmeldung, annual USt, Koerperschaftsteuer, Gewerbesteuer, E-Bilanz, Einspruch, Aussetzung der Vollziehung, Vorauszahlungen-Herabsetzung and Fristen, filed through Mein ELSTER with certificate login. Carries the traps that cost real money: section 13b reverse charge on EU and US SaaS (Anthropic Ireland, Cursor, Supabase), vendors billing the placeholder VAT ID DE000000000, invoices addressed to the founder privately, the 4-day Bekanntgabe rule since 2025, Verboeserung, Fuenftelregelung only via the ESt return since 2025. Use for ELSTER, UStVA, Steuerbescheid, Einspruch, Finanzamt letters, German VAT on software subscriptions, UG/GmbH annual filings, Taxfix-style self-filing. The agent prepares; a human approves every submission."
---

# German taxes and ELSTER, done by an agent

Built from a real filing season: one founder, one small UG, a personal return, every 2025 return and
2026 Voranmeldung filed through Mein ELSTER by an agent with certificate login, plus the Bescheide,
Schaetzungsbescheide and Einsprueche that followed. Every trap below cost money or a correction in
that run. Personal data has been removed; amounts in examples are illustrative.

**This is not tax advice.** German tax law changes every year. Every claim tagged *(verify)* must be
checked against the current law (gesetze-im-internet.de, BMF-Schreiben, the current ELSTER form)
before it is relied on. When a case involves a foreign entity, a shareholder dispute, a possible
Steuerstraftat (any letter that mentions § 371 AO) or real money at stake, recommend a Steuerberater
and say why.

## Safety rules (non-negotiable)

1. **The agent prepares, a human submits or explicitly approves each submission.** Pressing
   "Absenden"/"Übermitteln" is a legally binding declaration in the taxpayer's name (§ 150 AO).
   Get an explicit go for *that* form and *those* numbers, in this session. A general "do my taxes"
   is not approval to transmit. Approval to send form A is not approval to send form B.
2. **Never invent a deduction, a number or a fact.** Every line that reduces tax needs a piece of
   evidence: invoice, bank debit, contract, Eigenbeleg with the debit attached. No evidence, no
   line. Write `[FEHLT: ...]` instead of a plausible guess. Bank statements are not invoices.
3. **Evidence table per item.** For every amount you put in a form: source file, date, counterparty,
   who the invoice is addressed to, net/VAT/gross, VAT treatment, form line (Kz). Keep it next to
   the draft. If two sources disagree, stop and report the conflict.
4. **Positive proof for assets, not absence of counter-proof.** A Vorsteuer claim or a receivable is
   booked only when it is evidenced (invoice in hand, § 15 Abs. 1 Satz 1 Nr. 1 Satz 2 UStG), not
   because nothing contradicts it.
5. **Secrets never touch logs.** Certificate password, PIN, ELSTER login: never in a command-line
   argument, a log, a prompt, a commit, a chat reply. See `references/elster-access.md`.
6. **Disclose, don't hide.** If you know a filed return is wrong, § 153 AO requires correcting it
   without delay. Use the free-text field (§ 150 Abs. 7 AO, "Ergänzende Angaben") to state what is
   incomplete and why. A disclosed gap is a correction; an undisclosed one can become a problem.
7. **Re-verify state before claiming it.** "Filed" means you have a Transferticket and the
   Übertragungsprotokoll, and "Übermittelte Formulare" went up by exactly one. Not "the button
   was clicked."
8. **Retract loudly.** When a later document overturns an earlier conclusion, mark the old file
   ÜBERHOLT at the top with the reason and point to the current one.

## Step 0: triage before any form

Ask or find out, in this order. Most expensive mistakes come from skipping this.

| Question | Why it matters |
|---|---|
| Which taxpayer? Person (Steuer-ID) or company (Steuernummer), and which Finanzamt? | Companies and their founder are different taxpayers. A cost paid privately for the company is not automatically the company's Vorsteuer. |
| All Steuernummern on file? | A company can show one number on Bescheide/refunds and another on its ELSTER submissions. Read the Ordnungskriterium on each Bescheid and Kontoauszug. Filing under the wrong one has produced Schätzungsbescheide. |
| Kleinunternehmer (§ 19 UStG) or Regelbesteuerung? Waiver on file? | Decides whether any Vorsteuer is deductible. Find the "Fragebogen zur steuerlichen Erfassung" in ELSTER (Übermittelte Formulare) and read the waiver line itself. The waiver binds for 5 calendar years *(verify)*. |
| Ist- or Sollversteuerung? | Decides in which quarter revenue lands. Read the selected radio control, not its label. |
| Voranmeldung rhythm: monthly or quarterly? Dauerfristverlängerung? | Derive it from evidence: quarterly Bescheide mean quarterly filer; a Q1 due date of 10.04. means no Dauerfristverlängerung. |
| USt-IdNr? | Without one, EU vendors bill German VAT on DE000000000 and the reverse charge breaks. See `references/vat.md`. |
| What is overdue, what has a clock? | List every open Bescheid with its date and the Einspruch deadline computed per `references/notices-and-appeals.md`. Deadlines first, amounts second. |
| Dormant company? | For a near-dormant company the risk is non-filing, not tax: Verspätungszuschlag, Schätzung, Zwangsgeld, Ordnungsgeld. File zeros on time. |

Then size the problems by money at risk and deadline, and work in that order. The late return a
founder asks about is often the cheapest item on the list.

## Workflow

1. **Collect** (read-only): ELSTER "Übermittelte Formulare" and Posteingang, bank export *with
   Verwendungszweck per booking* (summarised exports merge counterparties and hide what happened),
   payment-processor export (Stripe balance transactions, not only payouts), vendor invoices
   downloaded from each vendor portal, contracts, prior Bescheide.
2. **Reconcile**: bank vs processor vs declared figures, per quarter, to the cent. Reverse-engineer
   how earlier filings were computed before trusting or "correcting" them.
3. **Classify** each item (`references/vat.md` decision table). Mark confidence high/medium/low.
4. **Draft** the form values with the evidence table. Write the draft to a file.
5. **Adversarial review**: have a second model or a fresh agent attack the draft ("find every
   reason not to submit this"). Fix or disclose each finding. In the source run every review round
   found real defects, including a wrong form line and an invented field value.
6. **Fill the form** in ELSTER with "Datenübernahme" where offered, run "Alles prüfen", read every
   error and Hinweis, read back every field from the control state.
7. **Human approval** of the final numbers and text, explicitly for this form.
8. **Submit**, then verify (Transferticket, Protokoll PDF saved immediately, counter +1, draft
   folder empty). Record ticket and timestamp in the working file.
9. **Calendar** every follow-up: next Voranmeldung, Einspruch deadlines, Vorauszahlungen,
   Offenlegung, certificate expiry.

## Reference files (load only what the task needs)

| File | Load when |
|---|---|
| `references/elster-access.md` | Logging in as an agent, certificate handling, submitting, E-Bilanz via myebilanz, form quirks |
| `references/vat.md` | UStVA, annual USt, § 13b reverse charge, DE000000000, founder-billed vendors, Dauerfristverlängerung, USt-IdNr |
| `references/company-annual.md` | UG/GmbH Jahresabschluss, E-Bilanz, KSt, GewSt, Rückstellungen, § 7g, losses, Offenlegung |
| `references/notices-and-appeals.md` | A Bescheid arrived: Fristen, Einspruch, AdV, Verböserung, Herabsetzung, Schätzung, Zuschläge, paying |
| `references/personal-income-tax.md` | Founder's own ESt: Pflicht vs Antrag, Abfindung/Fünftelregelung, employer + company in one year |
| `references/templates.md` | Wording for Einspruch, AdV, Herabsetzung, § 153 Anzeige, Eigenbeleg, Steuernummer clarification |

## Ten traps, one line each

1. Anthropic, Cursor and others bill a company without USt-IdNr as a consumer (`DE000000000`,
   "VAT Germany 19 %"). That VAT is not deductible Vorsteuer; the reverse charge still applies.
2. EU supplier (Anthropic Ireland, Meta Ireland, Lovable Sweden) → Kz 46/47; third-country
   supplier (Cursor US, Supabase Singapore, Vercel US) → Kz 84/85. Not interchangeable.
3. Invoice addressed to the founder privately → no Vorsteuer for the company; deduct the gross
   amount via Auslagenersatz or Einlage with an Eigenbeleg.
4. Einspruch against a Bescheid: 1 month from Bekanntgabe, and Bekanntgabe is the **4th** day
   after posting since 2025 (not the 3rd), rolled to the next working day. Against your own
   Steueranmeldung the month runs from its receipt (§ 355 Abs. 1 Satz 2 AO).
5. An Einspruch reopens the whole assessment: Verböserung is possible after a warning (§ 367
   Abs. 2 AO); withdraw if warned and the downside is bigger.
6. An Einspruch does not stop payment. Apply for Aussetzung der Vollziehung separately.
7. Missing Voranmeldung → Schätzungsbescheid under Vorbehalt; the real filing replaces it.
   Dauerfristverlängerung is free for quarterly filers and prevents the next one.
8. GewSt for a corporation has no 24,500 EUR Freibetrag; Gewerbeertrag rounds down to 100 EUR.
9. Since 2025 the employer may not apply the Fünftelregelung; it only comes through the ESt return.
10. KSt 1 and GewSt 1 A have no "berichtigte Erklärung" checkbox; mark a correction in free text.
