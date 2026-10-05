---
name: research
description: 'Run structured B2B research prompts from the Markster OS library. CHECK what they are trying to learn and ICP context. DO one or more of 9 prompts (competitive intelligence, buyer JTBD, buying signals, pricing perception, GTM channels, objection research, market positioning, mental category positioning, first 60 seconds). VERIFY output is documented back into Foundation.'
---

# Research Operator

---

## CHECK

Do not proceed past any failed check.

**1. What are they trying to learn?**

Ask the user one question before running anything: "What specific decision or action does this research need to inform?"

If they cannot answer: "Research without a decision to feed is noise. Tell me what you are trying to do -- write a cold email, define your positioning, prepare for a sales call -- and I will route you to the right prompt."

**2. ICP context**

Ask: "Do you have an ICP defined, even partially? Prompts with more specific inputs produce more usable outputs."

- Full F1 complete: proceed directly to prompt selection
- Partial F1 (know company type + title but not buying trigger): proceed, prompt will surface buying trigger
- No F1 at all: run the Buyer JTBD prompt first -- it will define the language and signals needed for F1

**3. Existing knowledge**

Ask: "What do you already know about your buyer and market? Any verbatims from clients or prospects, any competitor claims you have seen, any objections that keep coming up?"

Existing knowledge prevents duplicate work and makes prompts more specific.

---

## DO

Present the menu and ask which the user wants to run. Multiple prompts can be run in one session if the decision being informed is broad enough.

### The 9 research prompts

| # | Prompt | When to run it |
|---|--------|----------------|
| 1 | **Competitive intelligence** | Before writing any cold email or content. Understand what the buyer is already seeing from competitors. |
| 2 | **Buyer JTBD** | When building F1 or the messaging guide. Surfaces the buyer's language, functional goals, emotional goals. |
| 3 | **Buying signals** | When defining the buying trigger for F1. What to look for when building a list. |
| 4 | **Pricing perception** | When building F2. How your ICP thinks about price, what they compare you against. |
| 5 | **GTM channels** | When choosing channels. Where your ICP trusts discovery and learns about vendors. |
| 6 | **Objection research** | Before writing cold email sequences. Surface what you will encounter in replies. |
| 7 | **Market positioning** | When defining your messaging. Find the white space. |
| 8 | **Mental category positioning** | When differentiating from alternatives. How buyers categorize solutions like yours. |
| 9 | **First 60 seconds** | Before events, sales calls, or any live conversation with an ICP. |

### Running a prompt

When the user selects a prompt:
1. Open the corresponding file in `research/prompts/`
2. Ask the user to provide the variables the prompt requires -- ICP description, company category, competitive names, whatever the prompt needs
3. Fill in the variables with their context and run the prompt
4. Produce specific, usable output -- not a summary, not a framework description, actual findings they can act on

Do not run a prompt with empty variables. Generic inputs produce generic outputs. Push back until the variables are specific.

### Prompt files

| Prompt | File |
|--------|------|
| Competitive intelligence | `research/prompts/competitive-intelligence-prompt.md` |
| Buyer JTBD | `research/prompts/buyer-jobs-to-be-done-prompt.md` |
| Buying signals | `research/prompts/buying-signals-trigger-events-prompt.md` |
| Pricing perception | `research/prompts/pricing-value-perception-prompt.md` |
| GTM channels | `research/prompts/gtm-channel-effectiveness-prompt.md` |
| Objection research | `research/prompts/ai-agency-objections-prompt.md` |
| Market positioning | `research/prompts/market-positioning.md` |
| Mental category positioning | `research/prompts/mental-category-positioning-prompt.md` |
| First 60 seconds | `research/prompts/first-60-seconds-messaging-prompt.md` |

---

## VERIFY

Before this session ends:

**1. Output is documented in the correct file?**

Route findings to the right destination -- do not leave research in the chat only.

| Finding type | Where it goes |
|-------------|--------------|
| Buyer verbatims (exact phrases buyers use) | `methodology/foundation/messaging-guide.md` -- problem statement section |
| Buying signals and trigger events | `company-context/audience.md` -- situational layer in F1 |
| Objections | `playbooks/biz-dev/sales/templates/objections.md` |
| Competitor claims and positioning | `company-context/messaging.md` -- differentiation section |
| Pricing perception patterns | `company-context/offer.md` -- pricing rationale in F2 |
| White space / positioning gaps | `methodology/foundation/messaging-guide.md` -- mechanism section |

**2. Buyer verbatims captured?**

If the prompt surfaces exact phrases buyers use to describe their problem -- capture them verbatim. These are the highest-value output from any research session. They belong in the messaging guide and should feed directly into cold email and content.

**3. Decision informed?**

Confirm the research answers the decision from CHECK step 1. If not, identify which prompt would close the gap and either run it now or schedule it.

**4. Next prompt recommended?**

Each research output typically reveals a second question. Name it: "Based on what we found, the next most useful research would be [prompt] because [reason]."

---

## Reference files

- Research library: `research/README.md`
- Messaging guide: `methodology/foundation/messaging-guide.md`
- F1 Positioning: `methodology/foundation/F1-positioning.md`
- Objection scripts: `playbooks/biz-dev/sales/templates/objections.md`
