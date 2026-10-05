---
name: sales
description: 'Run the Markster OS sales playbook. CHECK deal context, DO discovery/proposal/close, VERIFY before moving stages. Includes 9 Kill Skills audit for conversion problems.'
---

# Sales Operator

---

## CHECK

**1. Foundation ready?**

Read `company-context/offer.md` and `company-context/audience.md`.

Required before running this skill:
- F1: ICP defined with buying trigger
- F2: Offer stated as an outcome, not a deliverable. Pricing documented.
- Proof: at least one specific result (company type + number + timeframe)

If any of these are missing: "The sales process runs on Foundation. Without a defined ICP, outcome statement, and proof point, your sales calls will produce inconsistent results because you are improvising instead of executing a system. Complete F1 and F2 first."

**2. Which stage?**

Ask: "Which of these describes where you need help right now?"

```
1. Preparing for a discovery call (upcoming call)
2. Writing a proposal after a discovery call
3. Handling a stall or objection
4. Auditing why deals aren't closing (conversion problem)
5. Reviewing the pipeline
```

Route to the corresponding DO section below.

**3. Archetype**

The sales motion differs by business type. Confirm the type before starting.

| Type | Key difference |
|------|---------------|
| B2B SaaS | Demo-led, shorter cycle, trial or POC as close mechanism |
| Consulting / Advisory | Longer cycle, relationship-driven, proposal is the close mechanism |
| Agency | Scoped project or retainer, value tied to outcomes not hours |
| Trades | Phone + in-person, speed of response is often the competitive moat |

Read the relevant segment file before running any stage: `playbooks/segments/`

---

## DO

### Stage 1: Discovery call prep

**Pre-call research (10 minutes max):**
- Company: what do they do, how big, what changed recently
- Contact: role, tenure, what they have said publicly
- Trigger: what happened that made them take this meeting

**Qualification threshold:**
Before the call, define what must be true for you to want this client:
- Company type match
- Budget range
- Problem severity
- Decision-making authority

If they do not meet the threshold on the call, do not propose. Qualify out cleanly.

**Call structure (45 minutes):**

| Minutes | Phase | Purpose |
|---------|-------|---------|
| 0-5 | Open | Set agenda. Ask why they agreed to the call. |
| 5-25 | Situation questions | Current state, history, what they have tried |
| 25-35 | Implication questions | Cost of the problem continuing. Their words, not yours. |
| 35-40 | Solution framing | 2-3 sentences. Tailored to what they described. |
| 40-45 | Next steps | One specific action with a date. |

**Key questions to ask (pull from `playbooks/biz-dev/sales/templates/discovery-call.md`):**
- "What does solving this mean for you personally?"
- "What have you already tried?"
- "If we do nothing, what happens to this problem in 6 months?"
- "What would need to be true for you to move forward on this?"

**After the call (within 30 minutes):**
Capture: their exact language, the cost they named, qualifying signals, confirmed next step.
Use this to write the proposal.

### Stage 2: Proposal writing

Use `playbooks/biz-dev/sales/templates/proposal.md`.

Build each section with the discovery notes in front of you:

| Section | Rule |
|---------|------|
| Situation summary | Use their words. Quote what they said. Do not rephrase. |
| Outcome | F2 outcome statement tailored to their specific situation. |
| Approach | 3-6 steps. Enough for confidence. Not enough to DIY. |
| Timeline | First visible result in 14 days. Full outcome by [specific date]. |
| Investment | Outcome-based price from F2. State confidently, no apology. |
| Risk reversal | From F2. One clear statement of what happens if it does not work. |
| Next steps | One action to say yes. Not two. One. |

**If a discovery notes section is missing:** Do not improvise or fill it with assumptions. Stop and ask the user: "What did the prospect say about [the missing section]?" If the information was not captured on the discovery call, schedule a 10-minute follow-up call before sending the proposal. A proposal missing the prospect's own words will not close.

**Delivery rule:** Walk through the proposal on a call. Do not just email a PDF and wait. Send it 2 hours before the call so they can review. Walk through it live. Close on the call.

### Stage 3: Objection handling

**"I need to think about it"**
Ask: "Of course -- what specifically would make you more confident moving forward?"
Do not accept the vague response. Get the specific concern. Address that, not the general objection.

**"Too expensive"**
Ask: "What are you comparing it to?"
Reframe against: cost of the problem continuing, cost of hiring internally, or the value of the outcome.
Never lower the price without removing scope. If they need a lower entry point, propose the Downsell: a smaller first engagement, not a discount.

**"We need internal approval"**
Offer to create a one-pager they can share internally. Write it for them. Use their language. Make their internal sell easy.

**"We already have someone for this"**
Ask: "Is there still an area where the problem persists?"
Do not pitch against the incumbent directly. Find the gap the incumbent is not solving.

**"Not the right time"**
Ask: "When would be the right time, and what needs to happen between now and then?"
Their answer is your follow-up roadmap. Set a reminder. Come back when the condition is met.

Full objection scripts: `playbooks/biz-dev/sales/templates/objections.md`

### Stage 4: Conversion audit (9 Kill Skills)

Use this when close rate is below target or declining.

Pull the last 5 recorded calls. Score each Kill Skill 1-3.

| Kill Skill | What to listen for |
|-----------|-------------------|
| 1 Breathe the Script | Is the script running word for word, or improvised? |
| 2 Tone | 150-170 wpm? Loud enough? Every word clear? |
| 3 Introduction | Call framed in first 60 seconds? Agenda set? |
| 4 Discovery | At least 20 minutes of questions before offering anything? |
| 5 Offer | Is the offer presented using their own words from discovery? |
| 6 Objections | Are objections addressed without losing momentum? |
| 7 Looping | After a failed close, does the rep return to discovery? |
| 8 BAMFAM | Does every call end with a next meeting booked? |
| 9 Referrals | Is every closed customer asked for names on the close call? |

The lowest-scoring Kill Skill is the training drill.

**Pause rule:** After asking for the business, pause for at least 8 seconds. Do not fill the silence. The person who speaks first loses. Most closers answer their own question within 3 seconds.

### Stage 5: Pipeline review

Walk through every active deal. For each one, answer:

```
Deal: [Company name]
Stage: intro / discovery / proposal / negotiation / stalled
Last contact: [date]
Next action: [specific action]
Next action date: [date]
Blocker: [if any]
```

Flag: any deal without a next action date. It will die.

Flag: any deal with no contact in 14+ days. Send a re-engagement email today.

Flag: any deal sitting at "proposal sent" for more than 7 days. Follow up with a specific question, not "just checking in."

---

## VERIFY

Before ending this session:

**1. Next step defined?**

Every active deal must have one next action with a date. No exceptions.

**2. Objection unblocked?**

If a deal was stuck on an objection, confirm the response was sent or scheduled.

**3. Conversion metric set?**

State the baseline: "Current close rate is [X]%. Target this month is [Y]%."

If close rate is below target: confirm which Kill Skill was identified as the gap and what the drill is.

**4. Pipeline health?**

Confirm no deal is sitting without a next action date.

**5. BAMFAM confirmed?**

If a discovery call was prepared this session: confirm a follow-up call or proposal delivery date is already on the calendar.

---

## Reference files

- Full playbook: `playbooks/biz-dev/sales/README.md`
- Discovery call guide: `playbooks/biz-dev/sales/templates/discovery-call.md`
- Proposal template: `playbooks/biz-dev/sales/templates/proposal.md`
- Objection scripts: `playbooks/biz-dev/sales/templates/objections.md`
- Segment archetypes: `playbooks/segments/`
