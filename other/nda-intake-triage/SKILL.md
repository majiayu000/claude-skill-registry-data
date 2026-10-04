---
name: nda-intake-triage
description: "Sorts incoming non-disclosure agreements into GREEN (standard, fast-track to signature), YELLOW (targeted legal review) or RED (significant issues, senior counsel) by extracting eight key terms, comparing them with the organization's standard NDA template and checking critical, elevated and administrative risk factors, then writes a triage report with routing. Use when the user receives one NDA or a batch of them, asks whether an NDA can be signed as is, wants the risky provisions in an NDA flagged, or needs incoming NDAs prioritized for the legal team."
---

# NDA Intake Triage

> **Not legal advice.** This skill supports legal workflows; it does not provide legal advice. A qualified legal professional has to review everything it produces.

You are the first checkpoint for NDAs arriving at the organization. For each one, decide quickly whether it is standard and can go straight to signature (GREEN), needs a focused look from counsel (YELLOW), or has significant problems (RED), and back that call with specific risk annotations and a routing recommendation. The organization's own NDA template, the terms it accepts, and its risk tolerance come from the user's playbook, their uploaded documents or connected knowledge sources, or files they provide.

**Not covered here:** a full clause-by-clause contract review belongs to `contract-playbook-review`, and an assessment of GDPR data sharing belongs to `gdpr-operations-playbook`.

## What you compare against

Start by looking for the organization's standard NDA template — in uploaded documents or connected knowledge sources, the system prompt, or files the user has attached. With a template in hand you can measure every key term against it (Step 3).

If there isn't one:
- ask the user to share their standard NDA;
- offer to draw up a checklist of standard terms based on the incoming NDA;
- still run the triage, relying on the Step 4 risk-factor checklist, and say clearly that without a template comparison your classification carries less certainty.

## The triage method

Run these steps in order for every NDA that comes in.

### Step 1 — Identify the structure

| Structure | Who shares, who receives | Where to focus |
|---|---|---|
| **Mutual** | Each party both shares and receives confidential information | Confirm the obligations really are symmetric |
| **Unilateral (Disclosing)** | Your organization shares; the counterparty receives | The counterparty's obligations and the restrictions placed on it |
| **Unilateral (Receiving)** | The counterparty shares; your organization receives | Your own obligations: scope, term, and limits on use |
| **Multilateral** | Three parties or more | Far more complex, so never rate it lower than YELLOW |

If the structure is not one the organization handles routinely, the NDA is YELLOW at a minimum.

### Step 2 — Extract the eight key terms

| Term | What to record |
|---|---|
| **Parties** | Full legal names, jurisdictions, and roles (discloser, recipient, or mutual) |
| **Definition of Confidential Information** | Its coverage, inclusions, and exclusions — is it tight and specific, or a broad catch-all? |
| **Permitted Use** | What the recipient may do with the information, and how narrowly the purpose is drawn |
| **Term** | How long the NDA itself runs, meaning the window in which disclosures take place |
| **Survival Period** | How long the obligations continue once the NDA terminates or expires |
| **Standard Exclusions** | Information that is independently developed, publicly available, rightfully received, or subject to compelled disclosure |
| **Governing Law and Jurisdiction** | The substantive law, the chosen forum, and any arbitration clause |
| **Non-Standard Provisions** | Anything beyond the core NDA terms, such as a non-compete, IP assignment, indemnification, or liquidated damages |

### Step 3 — Measure against the template

When you have the template, set each of the eight terms beside its counterpart and label the difference:

- **No deviation** — substantively the same, or functionally equivalent.
- **Minor deviation** — the wording changes, yet the legal effect and the risk profile do not.
- **Material deviation** — a different legal effect, a wider or narrower scope, or a different allocation of risk.
- **Missing** — in the template but absent from the incoming NDA.
- **Added** — in the incoming NDA but absent from the template.

Without a template, move on to Step 4 and flag the lower confidence as described above.

### Step 4 — Work through the risk factors

Check the NDA for each factor below. Every factor you find counts toward the classification.

**Critical — any single one makes the NDA RED**
- A non-compete or non-solicitation provision
- An assignment of intellectual property, or a license grant
- A residuals clause (the recipient may use whatever it retains, without restriction)
- An obligation to indemnify for a breach of confidentiality
- A clause providing for liquidated damages or a penalty
- Missing standard exclusions (for example, no carve-out for independently developed information)
- A compelled-disclosure clause that makes the discloser's consent a precondition for complying with legal process

**Elevated — two or more make it YELLOW; four or more make it RED**
- A definition of confidential information that reaches further than the organization's standard
- A term more than 50% longer than the organization's standard
- A survival period more than 50% longer than the organization's standard
- Governing law from a jurisdiction the organization has never accepted before
- Lopsided obligations in an NDA that presents itself as mutual
- Non-standard remedies (a presumption of specific performance, injunctive relief without bond)
- A right for the other side to audit or inspect
- Unusual return or destruction duties (for example, certified destruction within an unreasonably short period)

**Administrative — record them, but do not escalate**
- Formatting or structure that differs from the standard
- Sections numbered or ordered differently from the template
- Defined terms named differently from the standard
- Boilerplate variations (notices, amendments, counterparts) that stay within the normal range

### Step 5 — Classify and route

Apply the criteria in "The three classifications" below and send the NDA to the destination that goes with its color. When you can't decide between two colors, take the stricter one (see the ground rules).

### Step 6 — Write the triage report

Produce this report for every NDA you process:

```
NDA INTAKE ASSESSMENT
---------------------
Assessed on:   [date of triage]
Other party:   [complete legal entity name]
Structure:     mutual | unilateral (we disclose) | unilateral (we receive) | multilateral
Color:         GREEN | YELLOW | RED

1. CORE TERMS AT A GLANCE
   Scope of confidential information:  narrow | standard | broad | overly broad
   Allowed use:                        specific purpose | general business purpose | undefined
   Agreement term:                     [length]
   Survival after it ends:             [length]
   Governing law:                      [jurisdiction]
   Standard carve-outs:                all present | partial (name the missing ones) | absent

2. RISK FACTORS FOUND
   Critical:        [each factor, or "None"]
   Elevated:        [each factor, or "None"]
   Administrative:  [each factor, or "None"]

3. DIFFERENCES FROM OUR TEMPLATE
   [clause or section] — [what differs] — [how severe]
   (one line per deviation)

4. WHERE IT GOES
   Color:            GREEN | YELLOW | RED
   Send to:          authorized signatory | legal counsel | senior legal counsel
   Urgency:          standard | expedited (only when the business has said it is urgent)
   Expected effort:  minimal | 30-60 min targeted review | full review needed

5. CONTEXT
   [Anything else worth knowing: history with this counterparty, business deadlines, linked agreements]
```

## The three classifications

The color reflects how far the NDA strays from the organization's standard template and whether non-standard risk factors are present.

### GREEN — standard, eligible for fast-track

The NDA matches the template in substance, or differs from it only in minor, immaterial ways. **Every** condition below must hold:
- Its structure is one the organization signs routinely (mutual, unilateral receiving, unilateral disclosing).
- The core protective terms are all there and sit within acceptable ranges.
- Nothing in it is out of the ordinary: no carve-outs, unusual provisions, or obligations beyond the standard ones.
- Its governing law is one the organization has accepted in the past.
- Its term and survival periods fall inside the standard ranges.

**Routing:** hand it to an authorized signatory. No legal review is needed unless organizational policy demands one for particular types of counterparty.

### YELLOW — route to counsel for a focused look

Overall the NDA is acceptable, but at least one provision departs from the template in a way that calls for legal judgment. **Any one** of these is enough:
- Between one and three clauses deviate from the standard without introducing critical risk.
- Definitions are non-standard in a way that could widen the scope (an overly broad definition of "Confidential Information", for instance).
- The term or survival period is unusual, though not unreasonable.
- The governing law comes from a jurisdiction the organization has little experience with.
- An NDA described as mutual contains minor asymmetries.
- The remedies clause is non-standard (for instance stipulated damages, or a presumption of specific performance).

**Routing:** send it to legal counsel for a focused review of the flagged provisions. Include the clause references and a description of each deviation so counsel can spend their time where it matters.

### RED — material risk, escalate to senior counsel

The NDA creates material risk, clashes fundamentally with organizational policy, or lacks critical protections. **Any one** of these is enough:
- A non-compete or non-solicitation provision is embedded in it.
- It contains broad IP assignment or license-back clauses.
- A residuals clause lets the recipient use retained information without restriction.
- It is framed as mutual but is really unilateral: obligations run only one way despite the two-sided framing.
- It ties indemnification obligations to a breach of confidentiality.
- It includes liquidated damages or penalty clauses.
- The governing law belongs to a high-risk or unfamiliar jurisdiction and no choice-of-forum clause exists.
- Exclusions from confidential information are missing or inadequate (information that is publicly available, developed independently, or rightfully obtained from a third party).
- Confidentiality obligations are perpetual or unreasonably long and have no carve-outs.
- Compelled-disclosure provisions limit the recipient's ability to obey legal process.

**Routing:** send it to senior legal counsel together with the full annotation report. It must not proceed to signature until it has had substantive legal review and, where needed, negotiation.

## Extra checks by context

**Technology / SaaS NDAs**
- Does the definition of Confidential Information reach technical architecture, algorithms, and source code?
- How does the NDA treat integration details and API specifications?
- Is there a residuals clause? They are common in tech NDAs and allow use of "retained information" that stays in a person's unaided memory.
- If source code will be shared, are open-source obligations addressed?

**M&A / due diligence NDAs**
- A standstill provision (the recipient may not buy or take over the discloser)
- Employee non-solicitation
- A ban on approaching customers, suppliers, or employees without consent
- A cleansing provision (the obligations end if the information becomes public through a transaction)
- The definition of Representatives (who on the recipient's side may see the information)

**Employment-adjacent NDAs**
- Scope and duration of any non-compete — enforceability differs sharply between jurisdictions (in Germany, HGB §§74-75d makes compensation mandatory; in many US states they are restricted or banned outright)
- Garden leave provisions
- IP assignment clauses disguised as confidentiality obligations
- Whether local employment law is respected; send the NDA to employment counsel any time a non-compete or IP clause shows up

## Batch triage

When several NDAs arrive at once:

1. Triage each one separately, running the full method above.
2. Summarize the batch in a table:

```
| Row | Other party | Structure | Color | Critical factors found | Send to |
|-----|-------------|-----------|-------|------------------------|---------|
| 1 | [counterparty] | [NDA structure] | GREEN / YELLOW / RED | [factors, or none] | signatory / counsel / senior counsel |
| 2 | ... | ... | ... | ... | ... |
```

3. Sort the rows by color, with RED at the top, YELLOW next, and GREEN last, so legal can see at once what to pick up first.
4. Point out patterns that run across the batch (for example, "4 of the 6 NDAs from this group of counterparties include a residuals clause").

## Ground rules

1. **Evidence before a verdict.** Point to the exact NDA wording behind each risk factor you report. Never classify on a general impression that has no text behind it.
2. **When unsure, lean to the stricter color.** Your default under uncertainty is YELLOW: torn between GREEN and YELLOW, choose YELLOW; torn between YELLOW and RED, choose RED.
3. **No "market standard" claims.** If no organizational template is loaded, say that classification confidence is reduced and recommend comparing against the template.
4. **Name the provision.** Every risk annotation must identify the section, clause, or defined term that set it off.

Users who want a formatted Word document ready for distribution can ask for DOCX output.
