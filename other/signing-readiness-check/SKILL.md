---
name: signing-readiness-check
description: "Gets a negotiated legal document ready for execution: runs a pre-signature checklist covering document integrity, legal completeness and compliance, verifies that each signatory has authority to bind their organization, plans the signing order and e-signature setup, and lays out post-signing filing, key dates and reminders. Use when a contract is agreed and about to go out for signature, when the user asks who needs to sign or in what order, how to configure an e-signature envelope, or what to do once an agreement has been fully executed."
---

# Signing Readiness Check

> **Not legal advice.** This skill supports legal workflows; it does not provide legal advice. A qualified legal professional has to review everything it produces.

You take over once the negotiating is done and make sure an agreement is truly ready to be signed. Check that the execution copy is complete and clean, confirm that the people signing can actually bind their organizations, plan who signs when and how, and set up the administration that follows execution. Signing policies and authority levels specific to the organization come from the user's own policies or from their uploaded documents and connected knowledge sources.

**Not covered here:** substantive review of contract terms belongs to `contract-playbook-review`.

## Stage 1 — Readiness checklist

Nothing goes out for signature until you have worked through this list. Each item ends up in one of three states:
- **Confirmed** — checked and in order;
- **Waived** — an authorized person has explicitly waived it;
- **Unverified** — you could not check it. Mark it this way instead of leaving it out; no item may be dropped.

### Is the document itself right?

- [ ] **Version confirmation** — This is the final agreed version, and it carries no leftover tracked changes, comments, or hidden revisions.
- [ ] **Redline reconciliation** — Every change negotiated in the last round has made it in. Check the execution version against the final redline.
- [ ] **Exhibit and schedule completeness** — Every exhibit, schedule, appendix, and attachment the agreement refers to is present and complete. Use the agreement's own definition of "Agreement" or "Contract" to confirm that no component is missing.
- [ ] **Cross-reference accuracy** — After all the edits, internal references (section numbers, exhibit letters, defined terms) still point to the right place.
- [ ] **Defined terms consistency** — Defined terms are applied consistently, with no orphaned definitions (defined but never used) and no undefined terms (used but never defined).
- [ ] **Blank fields completed** — Every fill-in field (dates, names, addresses, amounts) has a value; no "[TBD]", "[●]", or other placeholder text is left.
- [ ] **Headers and footers** — Headers, footers, and watermarks show the right status; strip "DRAFT", "CONFIDENTIAL DRAFT" and the like unless they are meant to appear on the execution copy.
- [ ] **Page numbering** — Pages are numbered in an unbroken sequence across the whole document, exhibits included.

### Is it legally complete?

- [ ] **Governing law and jurisdiction** — A governing law clause exists and names the jurisdiction the parties intended.
- [ ] **Effective date** — It is clear how the effective date is fixed: by the last signature, by a stated date, or by a triggering condition.
- [ ] **Term and termination** — The start date, the initial term, any renewal mechanism, and the termination rights leave no room for doubt.
- [ ] **Counterparts clause** — If the parties will sign in counterparts (on separate signature pages), the agreement contains a clause allowing that.
- [ ] **Electronic signature clause** — If execution will be electronic, the agreement contains language accepting electronic signatures as valid.
- [ ] **Conditions precedent** — If the agreement only takes effect once conditions are met (board approval, regulatory clearance, and so on), confirm those conditions are either satisfied or being tracked.
- [ ] **Related agreements** — If the agreement refers to or depends on other agreements (a parent agreement, side letter, or DPA), confirm they are in the right state too: already executed, or ready to be signed at the same time.

### Are the compliance boxes ticked?

- [ ] **Internal approvals obtained** — Every approval the organization's approval matrix requires (legal, finance, business owner, procurement) is on record.
- [ ] **Regulatory filings** — If the agreement means something must be filed with, or notified to, a regulator (merger control, sector-specific rules), there is a confirmed plan for it.
- [ ] **Sanctions screening** — The counterparty has been checked against the applicable sanctions lists (EU, OFAC, UN) as organizational policy requires.
- [ ] **Anti-bribery check** — Where relevant, the anti-bribery and anti-corruption due diligence covering the counterparty is finished.
- [ ] **Data processing** — If personal data will be processed under the agreement, a DPA is already in place or forms part of the agreement.

## Stage 2 — Confirm signing authority

Every signatory needs the legal power to bind the organization they sign for. A job title alone never proves that; verify it against the authority matrix, and flag anyone you cannot confirm as unverified on the checklist. Record the result for each party:

**Authority check — [agreement title and ref.] — checked on [date]**

| Item | Party 1: [organization] | Party 2: [organization] |
|---|---|---|
| Person signing | [full name] | [full name] |
| Position held | [job title] | [job title] |
| Source of the power | board resolution / delegation of authority / articles of association / power of attorney | [source] |
| Reach of the power | unlimited / capped at agreements up to EUR X / only certain agreement types | [reach] |
| Evidence relied on | [how it was checked, e.g. certificate of incumbency, board minutes, delegation matrix] | [evidence] |
| Outcome | confirmed / pending / further documentation needed | [outcome] |

Where authority usually comes from, and what proves it:

| Kind of entity | Source of authority | Evidence to ask for |
|---|---|---|
| **Corporation (AG/GmbH/SA/Ltd)** | Managing directors (Geschäftsführer), a board resolution, or a power of attorney | An extract from the commercial register (Handelsregister), board minutes, proxy documentation |
| **Partnership** | The general partners, under the partnership agreement | The partnership deed and its registration |
| **Sole proprietorship** | The owner personally | The business registration |
| **Government entity** | Delegated authority or a statutory mandate | The delegation instrument or the enabling statute |
| **Special purpose vehicle** | Whatever its constitutional documents provide | Its articles and a shareholder resolution |

**Two signatures needed?** Certain jurisdictions and entity types insist on two authorized signatories — a German GmbH under Gesamtvertretung, for example — and some organizations require dual sign-off once an agreement passes a value threshold. Establish:
- whether the law requires two signatures for this entity;
- whether organizational policy requires them for an agreement of this value or type;
- that both signatories have been named and will be available.

## Stage 3 — Plan the signing order

Decide the sequence by weighing:

- **Legal requirement** — the agreement itself may fix the order (licensor before licensee, say, or employer before employee).
- **Organizational preference** — plenty of organizations prefer the counterparty to sign first, so they are not left bound while the other side stalls or reopens terms.
- **Practical logistics** — if one party's signatory is hard to get hold of, build the sequence around them.
- **Conditions precedent** — if one party's signature depends on the other's (for instance a DPA that has to be signed before the MSA), order things so the condition is met.
- **Simultaneous execution** — for high-stakes or time-critical agreements, arrange for everyone to sign at the same time, or use escrow.

Lay the plan out like this:

```
EXECUTION PLAN — [agreement title]
Aim to be fully signed by: [target date]

1) Internal sign-off
   Reviewed by [name] → approved / pending
   Conditions attached to the approval: [list, or "none"]

2) Execution copy goes out
   Direction: they send it to us  OR  we send it to them
   From [name] to [recipient's name, email address], on [date]
   Delivered as: PDF / via the e-signature platform / wet-ink original

3) Signature one
   [signer's name, organization] signs via [e-signature / wet ink], no later than [date]

4) Signature two
   [signer's name, organization] signs via [e-signature / wet ink], no later than [date]

5) Closing out
   Fully signed copy sent to: [recipients]
   Stored in: [contract management system / connected knowledge source / matter file]
   CLM entry updated? yes / no / N/A
```

## Stage 4 — Electronic execution

The rules on electronic signatures differ from one legal system to the next, and your preparation has to reflect the regime that applies:

| Jurisdiction | Main legislation | What to keep in mind |
|---|---|---|
| **EU** | eIDAS Regulation (EU 910/2014) | There are three levels: simple, advanced, and qualified. Only a qualified e-signature carries the same legal effect as a handwritten one (Article 25(2)). |
| **Germany** | eIDAS plus BGB §126a for qualified form | Where BGB §126 demands written form (Schriftform), a qualified electronic signature under §126a may be needed. Check whether this particular type of agreement requires Schriftform. |
| **United States** | ESIGN Act and state UETA | Broadly accepting of e-signatures, with some categories carved out (court orders, family law, wills). |
| **United Kingdom** | Electronic Communications Act 2000, plus Law Commission guidance | E-signatures are generally valid; deeds may need attestation. |

Whether a specific agreement in a specific jurisdiction may be signed electronically is a question for counsel — never give that answer yourself.

When the agreement is going onto an e-signature platform, configure:

- **Signers** — full names, email addresses, and the role each person signs in.
- **Signing order** — sequential (state the order) or parallel.
- **Signature fields** — on the correct signature block for each party.
- **Date fields** — filled automatically or entered by hand.
- **Initial fields** — only where needed (for example initials on every page, which not every jurisdiction treats as standard).
- **Attachments** — every exhibit and schedule is inside the envelope.
- **Expiration** — an envelope expiry that fits the signing deadline.
- **Reminders** — automatic nudges to anyone who hasn't signed yet.
- **Completion routing** — the executed copy goes out automatically to all parties and is filed.

## Stage 5 — After execution

Once everything is signed, work through the administrative follow-up, grouped here by deadline:

**Within 24 hours of execution**
- Legal operations sends out the executed copies.
- Legal operations files the agreement in the contract management system.

**Within 48 hours of execution**
- Legal operations pulls out the key dates (see the table below).
- The assigned contract owner puts calendar reminders in place.
- Legal operations lets the relevant teams know.
- The assigned lawyer brings the matter file up to date.

The dates to pull out and put in the calendar, and how far ahead to be reminded:

| Date | What it marks | When the reminder fires |
|---|---|---|
| **Effective date** | The point at which obligations begin | N/A (for information only) |
| **Term expiration** | The end of the agreement | 90 days before, to leave time to assess renewal |
| **Auto-renewal deadline** | The last day a non-renewal notice can be given | Notice period + 14 days buffer |
| **Termination notice period** | How much advance notice termination requires | Notice period + 14 days buffer |
| **Milestone dates** | Delivery dates, payment dates, performance milestones | 14-30 days before each one |
| **Regulatory filing deadlines** | Any filings that must follow execution | As the regulatory timeline dictates |

## Ground rules

1. **Authority is verified, never assumed.** A person's title does not by itself give them signing authority; check it against the authority matrix and flag any signatory you cannot confirm as unverified on the checklist.
2. **No verdicts on e-signature validity.** Do not advise whether a particular agreement can be validly signed electronically; that needs verification by counsel.
3. **Every checklist item stays.** If you cannot verify something, label it "unverified" rather than removing it.
4. **Execution formalities depend on jurisdiction.** Never say a given form of execution is sufficient without noting that the answer turns on the jurisdiction.

If the user wants a formatted Word document ready to distribute, tell them they can ask for DOCX output.
