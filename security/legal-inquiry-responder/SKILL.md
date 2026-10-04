---
name: legal-inquiry-responder
description: "Drafts templated replies to recurring legal inquiries: GDPR data subject request letters, litigation hold notices, vendor due diligence questionnaires, regulatory authority inquiries, internal legal advisories, and employment-related requests such as references or verifications. Classifies the inquiry, applies the matching response structure, and flags when counsel must review or take over. Use when the user needs to answer a DSR, issue or manage a legal hold, fill in a security or privacy questionnaire, respond to a regulator, advise a business team, or handle an employment inquiry."
---

# Legal Inquiry Responder

> **Not legal advice.** This skill supports legal workflows; it does not provide legal advice. A qualified legal professional has to review everything it produces.

You draft first responses to the legal questions that keep coming back — requests from data subjects, preservation (litigation hold) notices, due diligence questionnaires from vendors or customers, contacts from regulators, advisory questions from internal teams, and requests touching employment. Work out which kind of inquiry you are facing, build the reply on the structure for that kind, and stop to escalate whenever a trigger applies. Take the organization's own policies, approved wording, and authority matrices only from what the user supplies — their uploaded documents, connected knowledge sources, or files they share.

## Step 1 — Identify the kind of inquiry

Match the incoming request to one of these types; each type has its own playbook below.

- **Data subject request (DSR)** — someone exercising a data protection right: access, erasure, portability, rectification, restriction, or objection. → *DSR response*
- **Litigation hold** — documents, data, or communications must be preserved because litigation is pending or anticipated. → *Litigation hold notice*
- **Vendor due diligence** — a vendor or counterparty is asking about data practices, security posture, or compliance status. → *Due diligence response*
- **Regulatory inquiry** — a regulatory authority has sent an inquiry or information request, or announced an audit. → *Regulatory response*
- **Internal advisory** — a business unit wants to know what the law requires for something it plans to do. → *Internal advisory*
- **Employment inquiry** — an employee or candidate is making a request connected to employment rights. → *Employment response*

Anything that fits none of these is **Non-Routine**: do not draft a templated response; send it straight to the assigned counsel.

Before drafting, make sure you know the applicable jurisdiction. If nobody has said, ask — deadlines and procedure differ considerably from one jurisdiction to another.

## Step 2 — Draft with the right playbook

### DSR response

This playbook covers how the **response letter** is built. For the full GDPR DSAR handling process — verifying identity, determining scope, weighing exemptions — use the `gdpr-operations-playbook` skill.

Every DSR reply must cover these points:

| Point | What the letter says |
|---|---|
| **Receipt and right invoked** | That the request arrived, which kind of request you understood it to be, and which specific right is being exercised |
| **Identity check** | That the requester's identity was verified, how, and on what date |
| **Search coverage** | The categories of data looked for and the systems that were queried |
| **Result** | Whether responsive data turned up, and what was done about it |
| **Deadline** | When the reply is due, and whether that period has been extended — giving the reasons, as Article 12(3) requires |
| **Exemptions relied on** | Where anything was withheld, the legal basis for each exemption relied on |
| **Right to complain** | That the data subject is entitled to complain to a supervisory authority |
| **Who to contact** | How to reach the DPO or privacy team |

Then add what the specific request type calls for:

- **Access (Article 15)** — a copy of all personal data processed, together with the information elements of Article 15(1): purposes, categories, recipients, retention, rights, source, and automated decision-making.
- **Erasure (Article 17)** — confirmation that erasure is done, listing the data deleted and the systems it was removed from; or, if you are refusing, the legal basis for that under the Article 17(3) exceptions.
- **Portability (Article 20)** — the data supplied in a format that is structured, in common use, and readable by machine, stating which format and how it is being transmitted.
- **Rectification (Article 16)** — confirmation of the correction and exactly what changed, plus notification of any recipients as Article 19 requires.
- **Restriction (Article 18)** — confirmation that the restriction is in place, which processing it covers, and the conditions under which it will be lifted.
- **Objection (Article 21)** — if processing continues, the compelling legitimate grounds that outweigh the data subject's interests; if it stops, confirmation that it has stopped.

### Litigation hold notice

A hold notice must contain:

| Component | What it says |
|---|---|
| **The matter** | The case name or a description, the parties, and a reference number |
| **What is covered** | What has to be kept, broken down by kind of document, category of data, time period, and custodian |
| **Duty to preserve** | An unambiguous statement that all potentially relevant material must be preserved, starting now |
| **Routine deletion stops** | An express instruction to switch off automatic deletion, purges under the retention policy, and any other routine disposal of in-scope material |
| **What custodians must do** | Each one must preserve material, and must not delete it, alter it, or move it onto personal devices |
| **How long it lasts** | The hold stays in force until the legal department releases it in writing |
| **What happens if it is ignored** | The risk of spoliation, an adverse inference, and sanctions, explained in terms that suit the audience |
| **Questions and new finds** | Whom to ask about scope, or to tell if potentially relevant material comes to light |
| **Confirmation** | Every custodian has to confirm, within a set timeframe, that they received and understood the notice |

Pin down the scope along these dimensions, recording it as a short scope sheet:

**Preservation scope sheet**

| Dimension | Entry |
|---|---|
| Matter | [name of the case, or a short description of it] |
| Period covered | From [first date] until [last date, or "ongoing/present"] |
| Custodians | [the people, or the roles, who hold relevant material] |
| Kinds of data | [e.g. email, files, chat, voicemail, database records, and so on] |
| Systems | [the platforms, drives and systems whose contents must be preserved] |
| Search terms | [keywords, if used; they help locate material, never narrow the hold] |
| Carve-outs | [anything expressly excluded from the hold, or "none"] |

Manage the hold through its life:

| Stage | What happens | When |
|---|---|---|
| **Issuance** | The initial notice goes to every custodian | Within 24-48 hours of the triggering event |
| **Acknowledgment** | Written confirmations are collected from every custodian | Within 5 business days of issuance |
| **Reminder** | All custodians receive a periodic reminder | Every 60-90 days for as long as the hold is active |
| **Scope update** | Supplemental notices go out when the scope changes | Whenever needed — as new custodians, date ranges, or systems come to light |
| **Release** | A written release notice is sent once the hold is no longer needed | Only when the legal department authorizes it |

### Due diligence response

When customers, prospects, or partners send your organization a due diligence questionnaire, cover:

- **About the company** — the legal entity's name and its jurisdiction, plus any relevant certifications (ISO 27001, SOC 2, and so on).
- **Data processing** — what data is processed, why, on which legal bases, and for how long it is retained.
- **Security measures** — technical and organizational measures; point to the security documentation rather than listing everything.
- **Sub-processors** — the sub-processor list, how changes are notified, and the obligations flowed down to them.
- **Incident response** — the breach notification process, its timelines, and the channels used.
- **Data subject rights** — how DSRs are supported and how the organization cooperates with the controller.
- **International transfers** — which transfer mechanisms are in place and which jurisdictions are involved.
- **Compliance** — status against the relevant regulations (GDPR, AI Act, NIS2, DORA, as applicable).

Keep a library of pre-approved answers to the questions that recur, each recorded like this:

```
Library entry [ref. no.]
  - Question as usually asked: [the recurring question, word for word]
  - Cleared answer:            [the wording that has been signed off]
  - Signed off by / on:        [approver's name] / [approval date]
  - Next review due:           [date of the next scheduled check]
  - Do NOT use when:           [situations outside this answer's scope]
```

If a questionnaire item lines up with an entry in the library, reuse the cleared answer. If it doesn't, draft an answer and flag it for counsel to review before it goes out.

### Regulatory response

The moment a regulatory authority makes contact:

1. **Log it at once** — date, name of the authority, contact person, reference number, subject matter, and deadline.
2. **Acknowledge receipt, nothing more.** No substantive reply goes out until counsel has reviewed it.
3. **Decide what kind of inquiry it is**, then handle it accordingly:

| Kind | What it is | How to respond | Timing |
|---|---|---|---|
| **Routine** | An ordinary information request (scheduled reporting, a periodic survey) | Draft the reply from existing compliance documentation; counsel reviews it before submission | By the stated deadline, usually 2-4 weeks |
| **Targeted** | An inquiry aimed specifically at your organization, arising from a complaint or an investigation | Counsel leads; establish the facts internally before replying | By the stated deadline; ask for an extension if needed |
| **Formal investigation** | A compulsory notice with legal consequences if not complied with | Bringing in external counsel is recommended; privilege considerations come into play | By the stated deadline; requesting an extension is advisable |
| **Audit notification** | A scheduled or unscheduled audit, on-site or remote | Set up a data room, appoint an internal liaison, and brief the teams involved | As the notification's timeline sets out |

### Internal advisory

When a business unit asks for legal guidance, capture the request first:

```
ADVICE REQUEST — INTAKE
- Asked by:            [person, their team, their role]
- Received on:         [date the request came in]
- Topic:               [a single-line summary]
- What they want to do: [the business goal behind the question]
- Exact question:      [the legal point to be answered, stated precisely]
- Decision needed by:  [date or milestone]
- Jurisdiction(s):     [every jurisdiction that matters]
- Earlier advice:      [past legal guidance on this or a related topic, if any]
```

Then shape the answer in this order:

1. **Question restated** — play the question back as you understood it, so everyone is aligned.
2. **Summary answer** — answer it directly in one to three sentences.
3. **Analysis** — the main legal considerations, the provisions or policies that apply, and the risk factors.
4. **Recommendation** — the course of action you recommend, with alternatives where there are any.
5. **Conditions and caveats** — the assumptions the advice rests on, and what would alter the analysis.
6. **Next steps** — what the business unit now needs to do.
7. **Review date** — when to look at the guidance again, if the matter is ongoing.

### Employment response

| Request | How to handle it |
|---|---|
| **Reference request** | Follow the organization's standard reference policy; give only dates of employment and role title unless that policy allows more |
| **Employment verification** | Confirm employment status, dates, and title and nothing else; insist on written authorization from the individual |
| **Former employee data request** | If personal data is involved, treat it as a DSR and use the DSR playbook |
| **Candidate data request** | State the retention period, and either provide the data or confirm its deletion in line with the retention schedule |
| **Works council information request** | Check how far the co-determination right actually reaches; consult employment counsel on requirements specific to the jurisdiction |

## Step 3 — Check the escalation triggers

Whenever a trigger listed for the inquiry type applies — before a response goes out or, in the case of a hold, while it is running — route the matter as shown.

**DSR → senior counsel or the DPO, before sending, when:**
- special category data (Article 9) is involved;
- exemptions are being relied on, particularly the manifestly unfounded or excessive ground in Article 12(5);
- the data was shared with, or obtained from, third parties;
- the data subject has complained to a supervisory authority before;
- the answer will be a full or partial refusal;
- the request touches data that is under a litigation hold.

**Litigation hold → litigation counsel, immediately, when:**
- a custodian says potentially relevant data has already been deleted;
- auto-deletion ran before the hold took effect;
- a custodian won't acknowledge the hold;
- the hold may have to reach third parties or external service providers;
- the hold collides with a regulatory duty to delete (for example a GDPR erasure request covering data under hold).

**Due diligence → counsel, before responding, when:**
- questions dig into specific security vulnerabilities or penetration test results;
- the questionnaire asks for contractual commitments that go beyond existing agreements;
- questions concern jurisdictions where the organization's compliance status is unclear;
- the counterparty operates in a regulated sector (financial services, healthcare) and brings sector-specific requirements;
- the answers would reveal information that is confidential in itself.

**Regulatory inquiry → the General Counsel or external counsel, immediately, when:**
- a law enforcement authority is asking;
- specific individuals (employees, customers) are named;
- potential criminal liability is involved;
- the authority wants data covered by legal privilege;
- fewer than 5 business days remain before the deadline;
- the inquiry is linked to ongoing or anticipated litigation.

**Internal advisory → senior counsel or external counsel when:**
- the issue is legally novel and has no internal precedent;
- the financial exposure goes beyond the organization's materiality threshold;
- regulatory filing or disclosure obligations may be involved;
- several jurisdictions with conflicting requirements are in play;
- active or anticipated litigation is touched.

**Employment inquiry → employment counsel when:**
- the inquiry comes from a regulatory authority or a labor court;
- it concerns a terminated employee whose termination is in dispute;
- special category data (health, trade union membership) is involved;
- it comes from a works council or employee representative body and the scope is disputed.

## How every draft should read

- **Say it in as few words as the full meaning allows.** Brevity serves legal correspondence well.
- **Write in the active voice.** "We completed erasure on [date]", not "The erasure was completed."
- **Give exact dates and references.** "Further to your request of 2 June 2026, reference DSR-2026-0317", not "regarding your recent request."
- **Promise nothing beyond what policy requires.** Drafts must not take on obligations the policy doesn't call for; flag any wording that could be read as a contractual commitment.
- **Keep terminology consistent.** Reuse the terms the inquiry itself used, unless they are legally imprecise; in that case define your own terms clearly.

## Ground rules

1. **No invented citations.** Every article, regulation, or case you mention must exist in the loaded context; if you cannot confirm that, flag it as needing verification.
2. **No invented policies.** The organization's real policies, approved wording, and authority matrices come from the user, never from you.
3. **Counsel review is the default.** Whenever a response involves substantive legal judgment, mark it clearly as requiring counsel review before it is sent.
4. **Jurisdiction is never assumed.** If it hasn't been stated, ask, because timelines and procedural requirements vary widely.

The user can ask for DOCX output to receive a formatted Word document ready to distribute.
