---
name: cx-subject-access-request
description: Use to fulfil a subject access request from support data — finding everything about the person, and deciding what must be redacted before disclosure. Trigger for "handle this SAR", "subject access request", "customer wants all their data", DSAR fulfilment from support systems, "a customer asked for their call recordings", or an employee requesting their own QA records.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Subject access requests against support data

A subject access request against a support operation is harder than against most systems,
for one reason: **support data is full of other people's personal data, mixed into the
same records.** A conversation is about the requester, and it also contains the agent, the
third party they mentioned, and sometimes another customer entirely.

So there are two failure directions and both are real:

- **Under-disclosure** — withholding what the person is entitled to. The failure that
  generates complaints and regulatory attention.
- **Over-disclosure** — releasing a third party's personal data. A breach in itself, and
  unrecoverable once sent.

This produces the material and the redaction proposal. **The response, the legal
determination, and the sending are not yours** — they belong to whoever owns data
protection.

## Find everything, which is the hard part

Support data about one person is scattered, and the parts people forget are usually the
ones that matter most to the requester.

Search every store, on every identifier:

- **Conversations across every channel**, including ones under a different email or phone
  number. This needs identity resolution, and a SAR is one of the few places where
  under-matching is a compliance failure rather than a conservative choice.
- **Internal notes.** Frequently the part the requester most wants and the part most often
  omitted. Notes are personal data about them if they are about them, and agents write
  differently in notes than in replies.
- **Call recordings and transcripts.**
- **QA evaluations and their reasoning text**, where the conversation concerns them. For an
  employee SAR, this is the core of the request.
- **Complaint files**, including investigation notes and internal correspondence.
- **CRM and account records** linked from support.
- **Tags, custom fields, dispositions and risk flags** applied to them — including anything
  inferred, like a sentiment score, a churn-risk flag, or a vulnerability marker. Inferred
  data about a person is still their personal data.
- **The analytics warehouse**, exports, and any vector or search index built from their
  conversations.
- **Third-party systems** — BPO tools, transcription vendors, survey platforms.
- **Email**, and chat channels where staff discussed them by name.

Record what you searched and what you found nothing in. **A SAR response has to be able to
show the search was reasonable**, and the negative results are part of that.

## Employee SARs are the sharper case

An employee — or a former one — requesting their own data will typically want QA
evaluations, coaching records, performance documentation and any internal discussion about
them. This lands differently from a customer SAR:

- **QA reasoning text is their personal data**, including the parts that are unflattering.
- **The conversation content is largely the customer's** personal data, so a transcript
  cannot usually be released wholesale to the agent.
- **Internal discussion about their performance** is likely in scope, including messages
  between managers.
- **Expect it in the context of a dispute.** Handle it to the standard that assumes it will
  be scrutinised, and involve HR and legal from the start.

## Third-party data: the redaction decision

The general position is that the requester is entitled to their own personal data, not to
someone else's. In a support transcript these are interleaved line by line, so:

- **Agent identity.** Whether agent names are disclosed is a judgement that balances the
  requester's rights against the agent's, and it varies by jurisdiction and by the
  circumstances — including whether the agent has been threatened. **Do not decide this;
  flag it as a decision needed.** Agent first names are often already known to the
  requester from the conversation itself, which is relevant to the balance.
- **Other customers' data.** Redact. If a conversation contains another customer's details,
  that is also a finding about how it got there.
- **Third parties the requester named** — a family member, an employer, a business contact.
  Redact their data even though the requester mentioned them, unless legal advises
  otherwise.
- **Joint accounts and authorised representatives** need an explicit position on who is
  entitled to what.
- **Voice recordings** cannot be partially redacted as easily as text, and another person's
  voice is their personal data. A transcript with redactions may be the practical answer;
  that is a decision, not a workaround to apply silently.

Produce a **redaction proposal with reasons**, item by item, for legal to approve. Do not
redact silently, and do not release unredacted.

## The exemptions are not yours to apply

Most regimes have exemptions — legal privilege, ongoing investigations, crime prevention,
management forecasting, others — and some allow refusal of manifestly excessive requests.

**Identify candidates and route them.** Flag material that looks privileged, that concerns
an open investigation, or that would reveal a fraud control, and let legal decide. Applying
an exemption yourself is one of the higher-risk errors available here, in both directions.

## Practicalities that determine whether it goes well

- **The clock starts on receipt, by anyone.** A SAR arriving as a sentence in an ordinary
  support ticket is a SAR, and the clock started then. **Identification lag is the most
  common cause of a missed deadline** — search for SAR-shaped language across support
  contacts, not just in the inbox the policy names.
- **Verify identity proportionately**, and do not use verification to run the clock down.
- **Clarify scope where genuinely unclear**, but do not use clarification as a delay tactic;
  in some regimes it pauses the clock and in others it does not.
- **Deliver in a usable form.** A thousand-page PDF of raw ticket exports is technically
  compliant and reads as obstruction. Structure it.
- **Log everything** — receipt, searches run, decisions made, redactions applied and why,
  the response sent. The log is what defends the response later.

## Guardrails

- **Do not send the response.** This prepares material and a redaction proposal.
- **Do not decide the legal questions** — scope, exemptions, agent identity, joint accounts,
  refusal. Route them, clearly labelled, with the material attached.
- **Do not delete or alter anything** in scope of a request. Once a SAR is received,
  destroying data in scope is a serious matter, and it may also breach a litigation hold.
  If scheduled retention deletion would remove in-scope data, flag it immediately so it can
  be suspended.
- **Assemble in a restricted location.** A SAR bundle is a concentrated pile of one
  person's personal data and its own security exposure. Delete the working copies once the
  response is sent, on a schedule.
- **Do not paste content into chat or a ticket** while preparing it.
- **If preparing the bundle reveals something else** — data held that should not be, another
  customer's data in a record, a possible breach — raise it separately. It is a finding in
  its own right and it does not belong buried in the SAR response.

## Present results to the user

1. **Receipt date and how the request arrived**, with the identification lag if it came in
   through support rather than the named route.
2. **Search coverage** — every store searched, the identifiers used, and where nothing was
   found. This is what makes the search defensible.
3. **The material found**, itemised by source and type, with counts.
4. **The redaction proposal**, item by item with reasons, for approval.
5. **Decisions required from legal** — agent identity, exemption candidates, joint accounts,
   voice recordings, scope questions.
6. **Retention conflicts** — in-scope data due for deletion, flagged for suspension.
7. **Anything discovered in passing** that is a separate finding.
8. **The log**, and where the bundle is held.
