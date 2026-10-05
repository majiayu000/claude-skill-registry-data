---
name: events
description: 'Run the Markster OS events playbook. CHECK prerequisites (ICP, offer, specific event), DO pre-event targeting + during-event conversation system + post-event follow-up, VERIFY before leaving the event pipeline empty. Routes through ScaleOS G2 Warm.'
---

# Events Operator

---

## CHECK

Do not proceed past any failed check.

**1. F1 complete?**

Read `company-context/audience.md`.

Required before this skill runs:
- ICP defined with company type and buying trigger
- Decision-maker title named
- At least one pain stated in the buyer's words

If missing: "The events playbook requires a clear ICP to identify which events your buyers actually attend and what qualifying signals to listen for. Open `methodology/foundation/F1-positioning.md` and complete it first."

**2. Offer can be stated in the room?**

Read `company-context/offer.md`.

Required:
- One-sentence outcome statement (what the client achieves)
- One proof point (specific result, company type, timeframe)

If missing: "You need to be able to name what you do and show one real result before walking into a room with prospects. Open `methodology/foundation/F2-business-model.md` and fill in the offer first."

**3. Specific event context**

Ask the user:
- Do they have an upcoming event in mind, or are they identifying which events to attend?
- If attending: event name, date, expected ICP presence?
- If evaluating: what do they know about where their ICP actually goes?

If they do not know which events their ICP attends, prompt them: "Ask your three best current clients: what conferences, associations, or communities do they stay active in?"

**4. Your archetype**

Before running this playbook, confirm the business type.

| Your type | Read this first |
|-----------|----------------|
| B2B SaaS, devtools, marketplace | `playbooks/segments/startup-archetypes/` |
| Agency, consulting, IT/MSP, advisory | `playbooks/segments/service-firms/` |
| Residential or commercial services | `playbooks/segments/trade-businesses/` |

The conversation approach, qualifying signals, and follow-up sequences differ by archetype. Read before building templates.

---

## DO

Run these three phases in order. Phase 1 must be done before the event. Phase 2 is a briefing, not a live exercise. Phase 3 triggers within 48 hours of the event ending.

### Phase 1: Before the event

**Step 1: Identify target contacts**

Build a list of 10-20 specific people to meet at the event. Use LinkedIn to identify likely attendees:
- Search by company + job title
- Filter by location (event city) + activity (posted in last 30 days = higher engagement)
- Cross-reference speaker lists and sponsor booths

If `EVENT_SCOUT_KEY` is set: the Event Scout add-on can pull attendee intelligence before committing. Run it now.

**Step 2: Send pre-event outreach**

Use `playbooks/warm/events/templates/pre-event.md`.

Timing: send 5-7 days before the event.

Message goal: not a pitch. A warm introduction + a specific reason to connect at the event. Reference:
- The event name
- A shared interest or mutual connection if one exists
- One specific thing you want to discuss (not "would love to connect")

**Step 3: Prepare conversation setup**

Before walking in, have these three ready:
- One-sentence company description (not a pitch -- what you do in their terms)
- One qualifying question to identify if they match the ICP
- One agreed next step to offer when the conversation goes well (not "let's stay in touch" -- a specific proposal: "I'll send you a one-pager" / "Can I show you what we did for [similar company]?")

### Phase 2: During the event

Brief the user on the conversation framework:

1. Open by asking about them -- their role, their current focus, what brought them to this event
2. Listen for ICP signals -- the buying trigger, the pain you solve, the company characteristics
3. When the signal appears, name it back -- "That's exactly what we work on with [company type]"
4. Offer the specific next step before ending the conversation
5. Capture notes on your phone immediately after each conversation -- what they said, what was agreed, the follow-up action

**What not to do:**
- Do not lead with a pitch
- Do not hand the card before the conversation
- Do not say "let's stay in touch" without a defined next action
- Do not sell in the first conversation -- set the next meeting

### Phase 3: After the event

**Timing:** Follow-ups must go within 48 hours. After that, the conversation cools and the reply rate drops sharply.

Use `playbooks/warm/events/templates/post-event.md` as the starting point.

Each follow-up must include:
- Reference to the specific conversation (what they said, not a generic "great meeting you")
- Something useful if applicable (resource, intro, observation relevant to what they mentioned)
- Confirmation of the next step agreed in the conversation

For contacts who did not confirm a next step in the conversation: offer one specific, low-friction action (read this, reply yes, 15 minutes next week).

---

## VERIFY

Before this session ends:

**1. Target contact list built?**

Confirm 10-20 specific people are identified with names, titles, companies, and the qualifying signal to listen for with each.

**2. Pre-event outreach sent or scheduled?**

If the event is more than 5 days out: confirm outreach is written and scheduled.
If the event is under 5 days: send today.

**3. Conversation opening prepared?**

Confirm they can state:
- What they do (one sentence, no jargon)
- The qualifying question they will ask
- The next step they will offer when the conversation qualifies

**4. Follow-up plan set?**

Confirm they know exactly what happens within 48 hours of the event. Who sends? What template? What tracking?

**5. Metrics tracking set?**

For every event, record:
- Event name, date, cost to attend
- Target conversations planned
- Conversations had
- Follow-ups sent within 48 hours
- Meetings booked from the event
- Deals opened (tracked at 90 days post-event)

Review after each event to decide whether to return.

---

## Reference files

- Full playbook: `playbooks/warm/events/README.md`
- Pre-event template: `playbooks/warm/events/templates/pre-event.md`
- Post-event template: `playbooks/warm/events/templates/post-event.md`
- Event Scout add-on: `addons/event-scout/README.md`
