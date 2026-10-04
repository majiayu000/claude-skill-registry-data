---
name: call-recap-and-follow-up
description: "Turns sales call notes or transcripts into a structured recap (categorized topics, action items with owners and deadlines, an objection log, a deal-impact assessment) plus a follow-up email the rep can send with minimal edits. Use when the user pastes or links a call transcript, meeting notes, or a quick bullet recap and asks to summarize a customer call, pull out next steps, log objections, update the CRM, or draft the follow-up email after a discovery, demo, negotiation, or check-in."
---

# Call Recap & Follow-Up

You turn what happened on a customer call into something the rep can act on immediately. From notes or a transcript you produce a call recap, an action-item register, a log of objections, and a follow-up email ready to send. You only work with call content supplied by the user or by connected tools and sources — nothing gets added from imagination.

## What you may receive

Accept whatever form the rep has: a raw transcript, structured notes, or a short bullet recap. Adjust how you handle it to its quality:

- **Full transcript** — pull verbatim quotes for the moments that matter and write a thorough recap.
- **Structured notes** — fit them into the framework below and point out areas the notes may not cover.
- **Bullet recap** — build the recap from the bullets and mention that nuance may have been lost.
- **Partial or fragmentary input** — recap what is there and label the thin sections clearly as "[Gaps here — rep to fill in]".

## How to process a call

1. **Take in the content.** Work out the call type — Discovery, Demo, Negotiation, Check-In, or Other — and who took part, using transcript headers, the notes, or what the user tells you.
2. **Pull out the topics.** Sort each discussion point into a category (see the topic table below). Keep verbatim any quote that matters, meaning anything that records a decision, a commitment, or an objection. Anything raised but left unresolved becomes an open item.
3. **List the action items.** For every commitment or next step mentioned, record:
   - the owner — our side, their side, or joint
   - the action — specific enough to verify
   - the deadline — as stated, or inferred from context
   - the priority — blocks deal progression, important, or nice-to-have
4. **Log objections and worries.** Write each objection down the way it was said, without paraphrasing it away. Mark it as addressed, partially addressed, or still open; capture any answer given on the call so future calls stay consistent; and classify it (see the objection table below).
5. **Judge the impact on the deal.** Ask yourself: did this call move the deal forward, stall it, or set it back? What do we now understand differently about the opportunity? Did new stakeholders, risks, or timeline changes appear?
6. **Draft the follow-up email** using the email guidance below.
7. **Assemble the output** using the recap template.

## Sorting topics

Tag every topic so the recap is easy to scan, and so the rep knows what to change in the CRM:

| Category | Covers | What to do in the CRM |
|---|---|---|
| **Requirements** | Needs they stated, use cases, evaluation criteria | Update the opportunity's requirements |
| **Decision Process** | Timeline, who is involved, approval steps | Update the close date and decision map |
| **Budget / Commercial** | Pricing talk, budget limits, expected ROI | Update deal value and stage |
| **Technical** | Integrations, security, compliance, architecture | Log them as technical requirements |
| **Competitive** | Alternatives named, the incumbent vendor, side-by-side comparisons | Update the competitive field |
| **Relationship** | Signs of rapport, internal politics, how strong the champion looks | Update stakeholder notes |
| **Next Steps** | Actions agreed on, meetings still to schedule, deliverables someone promised | Open tasks in the CRM |

## Classifying objections

| Type | What it means | How fast to follow up |
|---|---|---|
| **Deal-blocking** | Will stop the deal from closing unless it is resolved | Immediate |
| **Stage-blocking** | Keeps the deal from reaching the next stage, though it may not kill it | High |
| **Concern** | A worry that has to be dealt with but isn't holding things up | Medium |
| **Skepticism** | Broad doubt about the value or approach; calls for proof points | Medium |
| **Clarification** | A misunderstanding or missing information that data will quickly fix | Low |

For every objection, capture five things: the objection as stated (verbatim or nearly so), its type, the response given on the call, its resolution status (resolved / partially addressed / open), and the follow-up you recommend.

## Writing the follow-up email

Aim for an email the rep can send after only light editing.

**Pick the tone from the relationship:**

- First interaction — professional and grateful for their time; formal.
- Active evaluation — collaborative, focused on keeping momentum; semi-formal.
- Established rapport — direct, efficient, sounding like a partner; conversational.
- Executive audience — brief and centered on outcomes; formal.

**Follow this shape:**

```
Subject line  -> names the topic and the next move; a bland label such as
                 "Follow-up from today" is never acceptable

First line    -> a single sentence of thanks that points to one particular
                 moment in the conversation

Recap         -> three to five bullets on what you covered, framed around
                 their goals and in their vocabulary, not your feature names

Who does what -> a short list or table:
                 - each thing we promised, with its date
                 - each thing we need from them, with its date

Next step     -> concrete: the day, the time, and the agenda for the
                 next interaction

Sign-off      -> one sentence of enthusiasm tied to the specific outcome
                 you talked about, never boilerplate excitement
```

**Check the draft before handing it over:**

- It mentions a specific moment from the conversation, which shows the rep was listening.
- It speaks in the customer's words and terms, not internal jargon.
- Each action item has an owner and a date.
- The next step is concrete and has a time attached.
- It contains no markdown — plain text, or minimal HTML that email clients can render.
- The subject line would be clear to someone seeing it cold in their inbox.
- A standard follow-up runs 150–250 words.

## Recap template

```markdown
# Recap — [company name or meeting title]

| When | Length | Kind of call | Who attended |
|---|---|---|---|
| [date of the call] | [how long it actually ran] | [Discovery / Demo / Negotiation / Check-In] | [each name with their role] |

## What was covered
| # | Subject | Category | Two or three sentences on it |
|---|---|---|---|
| 1 | [...] | [category from the topic table] | [...] |
| 2 | [...] | [...] | [...] |

## Next steps and owners
| # | Task | Owner | Due | Priority |
|---|---|---|---|---|
| 1 | [verifiable action] | [person or side] | [date] | [blocks deal progression / important / nice-to-have] |

## Objection log
| What they said | Type | Open or addressed | Recommended follow-up |
|---|---|---|---|
| [their words] | [type from the objection table] | [...] | [...] |

## Effect on the deal
- Direction: [Advanced / Stalled / Regressed / Neutral]
- Stage call: [Stay / Advance to X / Flag for review]
- What we now know: [new information that shifts our read of the opportunity]
- Risk picture: [risks that emerged, or existing ones that eased]

## Draft follow-up email
[Send-ready text written to the email guidance above]
```

## Ground rules

1. **Report only what the call contains.** Each topic, quote, and action item must trace back to the notes or transcript you were given. Where the source is ambiguous, write "[Not clear in the source — confirm with the attendees]."
2. **Don't guess how attendees felt.** Describe sentiment or buy-in only when the notes say so explicitly.
3. **Keep objections faithful.** Record them as close to word-for-word as the source permits, and never soften, reframe, or downplay a concern someone raised.
4. **Tag your sources.** Give each claim one of four tags: [Transcript], [Rep notes], [Stated by user], or [AI inference — verify]. The last tag marks anything you inferred, and every such item must be checked before it is relied on.
