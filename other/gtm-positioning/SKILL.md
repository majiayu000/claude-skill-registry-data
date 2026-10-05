---
name: gtm-positioning
version: 1.0.0
description: Framework-based skill for B2B product positioning, GTM strategy selection, and website messaging. Use when someone asks for help positioning their product, choosing a GTM strategy, writing homepage or website copy, messaging for different buyer personas, content strategy by awareness stage, or ad and landing page copy. Based on the Fletch framework by Anthony Pierri.
---

# GTM Positioning Skill

A framework-based skill for B2B product positioning, GTM strategy selection, and website messaging. Based on the Fletch framework by Anthony Pierri.

-----

## When to use which framework

|User need                             |Go to section                         |
|--------------------------------------|--------------------------------------|
|"Help me position my product"         |1. Positioning Strategy               |
|"What's my GTM?"                      |2. GTM Strategy Types                 |
|"Write my homepage / website copy"    |3. Website Messaging Guide            |
|"Write messaging for different buyers"|4. Persona-Based Messaging            |
|"What content should I create?"       |5. Marketing Assets by Awareness Stage|
|"Write ads / landing page copy"       |6. Value Prop by Awareness Stage      |

-----

## 1. Positioning Strategy

Pick one of three before writing any copy.

### Strategy 1: Position in a mature category

- **Use when**: The category already exists and has mind share (CRM, project management, video conferencing)
- **Reference point**: The category name itself
- **Competitive alternative**: Other vendors in the category
- **Target customer**: People already shopping for the category
- **Advantage**: No education needed; budget already exists
- **Risk**: You're fighting established players directly
- **Examples**: Figma, Zoom, Salesforce, Workday, Snowflake

### Strategy 2: Position in an immature/emerging category

- **Use when**: The category is forming but not dominant yet
- **Reference point**: The job-to-be-done of the emerging category
- **Competitive alternative**: The status quo way people do the JTBD — not a named vendor
- **Target customer**: People doing the JTBD who don't know a category exists yet
- **Advantage**: Less direct vendor competition; growing categories attract VC/press attention
- **Risk**: You inherit the market's opinion of the category; categories can fizzle
- **Examples**: DocuSign, Dropbox, Google, Uber, Tesla, Slack, 1Password

### Strategy 3: Create a new category

- **Use when**: You're solving a JTBD no one has named yet, or existing categories would limit your story
- **Reference point**: The JTBD of your choosing — you design it
- **Competitive alternative**: The status quo way people do your chosen JTBD
- **Target customer**: People doing the JTBD you selected
- **Advantage**: Design the category from scratch; distribution headstart before others join
- **Risk**: Picking the right JTBD is hard; first mover rarely wins the category long-term
- **Examples**: eBay, VMware, Red Bull, Xerox, Brex, Clay

**Decision rule**: Pick Strategy 1 if you have resources to compete head-to-head. Pick Strategy 2 if the category will grow and you can become a leader as it solidifies. Pick Strategy 3 only if you're willing to play the long game and believe categorizing yourself in an existing bucket hurts more than it helps.

-----

## 2. GTM Strategy Types

Driven by how specific you're willing to be on use case. This determines everything about your messaging and channel strategy.

|Type                 |Definition                                  |Examples                                  |
|---------------------|--------------------------------------------|------------------------------------------|
|**Vertical**         |Single use case, single segment             |Fletch ("re-write SaaS founder homepages")|
|**Horizontal**       |Single use case, multiple segments          |Calendly, Loom, Asana                     |
|**Vertical Solution**|Multiple use cases, single industry         |Epic, Procore, Guidewire                  |
|**Horizontal Suite** |Multiple use cases, multiple segments       |Google Workspace                          |
|**Platform**         |Many use cases, many segments (configurable)|Airtable, Notion, Miro                    |

**Recommendation**: Most early-stage startups should start Vertical. Nail one use case for one segment before expanding. The others are valid but require more GTM complexity and usually come after finding initial traction.

**Important**: The same product can have a completely different GTM. Positioning is not about changing the roadmap — it's about choosing which segment and use case to lead with. Slack, Discord, and Teams have nearly identical features but completely different positioning (target ICP, alternatives, problem framing, benefit).

-----

## 3. Website Messaging Guide

> **Fitting the words into the page.** This section decides what to say. Once you know, `righter` (`references/marketing-copy.md`) sets how much fits in each slot (hero h1 7 words, hero sub 12, section head 5, card title 4, card description 20), `vois-patterns` (`references/marketing-pages.md`) sets page structure, and `vois-tokens` sets type and spacing.

Each page has one job. Get the front-door pages right first — they determine whether anyone ever sees the rest.

### Front door pages — get these right first

|Page             |Role                |Lead with                                 |Goal                                     |Good model                                                                 |
|-----------------|--------------------|------------------------------------------|-----------------------------------------|---------------------------------------------------------------------------|
|**Home Page**    |The Front Door      |Capability + Use Case                     |Get the ideal user to take the first step|Calendly — super clear on the problem and what the product is              |
|**Persona Page** |The Personal Welcome|Capability + Use Case for that ICP        |Get the ideal user to take the first step|Asana — very clear who the page is for                                     |
|**Use Case Page**|VIP Entrance        |The capability that addresses the use case|Get the ideal user to take the first step|Zapier — thousands of use case pages, each highly specific, high converting|

### Exploration pages — prospects go here after the front door works

|Page              |Role              |Lead with               |Goal                                                    |Good model                                                   |
|------------------|------------------|------------------------|--------------------------------------------------------|-------------------------------------------------------------|
|**Product Page**  |The Feature Index |How it works            |Get users to see all the features                       |Slack — navigational dropdown, each feature gets its own page|
|**Pricing Page**  |The Value Exchange|Target Customer per tier|Convince buyers they're on the right package            |Airtable — clean with personalization by user type           |
|**About Page**    |The Big Vision    |Your Vision             |Convince investors and employees you're on something big|Canva — clear mission with highlights, key stats, ambitions  |
|**Resource Pages**|The Owner's Manual|High Value Guides       |Get users to value faster                               |Notion — incredible onboarding content depth                 |

-----

## 4. Persona-Based Messaging

In B2B, multiple people touch a buying decision. Each needs their own message.

For each persona, map: **Context → Problem → Capability → Benefit**

|Buyer Role                                              |What they care about                |Frame your message around                        |
|--------------------------------------------------------|------------------------------------|-------------------------------------------------|
|**User** (e.g., Sales Rep, PM, Designer)                |Their daily workflow                |How it removes friction from their actual job    |
|**Champion** (e.g., Dir. Sales Enablement, Product Lead)|Making the team work better         |Visibility, performance tracking, optimization   |
|**Decision Maker** (e.g., CRO, VP Product)              |Revenue, pipeline velocity, outcomes|Enabling the team to move faster and show results|
|**Financial Buyer** (e.g., CFO)                         |ROI, cost justification             |Defending spend to the board                     |
|**Technical Influencer** (e.g., Head of IT/Security)    |Risk, compliance, stability         |Security, encryption, reliability                |

### How to fill in the matrix

For each persona:

1. **Context**: What is their daily reality? What are they always trying to do?
1. **Problem**: What specific friction or failure does your product address for them?
1. **Capability**: What can they now do that they couldn't before?
1. **Benefit**: What outcome does that capability deliver that they actually care about?

This matrix powers your persona pages, sales decks, outbound sequences, and ad copy.

### Bottom-up vs top-down motion

**Bottom-up (PLG)**: Lead with the User persona. Win the person doing the work first. They pull the product up to their lead. Your homepage hero talks to the daily pain, your CTA is low-commitment (try free, not book a demo).

**Top-down (enterprise sales)**: Lead with the Decision Maker. Win the person who controls budget. Your homepage hero talks to org-level outcomes, your CTA is a conversation (book a demo, talk to us).

Pick one motion and commit. Trying to do both on one homepage dilutes both messages.

-----

## 5. Marketing Assets by Awareness Stage

Match the content to where the buyer actually is. The wrong content at the wrong stage gets ignored.

|Awareness Stage                    |Who they are                           |Content approach                            |Asset types                                   |
|-----------------------------------|---------------------------------------|--------------------------------------------|----------------------------------------------|
|**Problem Unaware** (Out of Market)|Don't know they have the problem yet   |Educate on trends and the problem           |White papers, industry reports, trend analysis|
|**Problem Aware** (Actual TAM)     |Know the problem, not shopping yet     |Educate on how to approach the problem      |Frameworks, guides, breakdowns                |
|**Solution Aware**                 |Know solutions exist, comparing options|Show success stories, highlight capabilities|Case studies, ROI calculators, buying guides  |
|**Product Aware**                  |Know your product, considering it      |Pull them into value-creating steps         |Free trials, consults, value adds             |

**Key insight**: Your actual TAM is only the Problem Aware layer — not everyone with the problem. The Problem Unaware layer is much larger but they're not in market. You're playing a long game with them through content, not ads.

-----

## 6. Value Prop Variations by Awareness Stage

The same product needs different messaging depending on where the buyer is. One homepage is a trap.

|Awareness Stage    |Mode            |Lead with                             |Earn trust by                                  |To convince them                  |
|-------------------|----------------|--------------------------------------|-----------------------------------------------|----------------------------------|
|**Problem Unaware**|Creating demand |The alternative — how they do it today|Showing you understand their situation         |They have a problem               |
|**Problem Aware**  |Creating demand |The problem                           |Showing you understand their problem           |They're missing a key capability  |
|**Solution Aware** |Capturing demand|The capability                        |Showing you understand their desired capability|Your feature unlocks it           |
|**Product Aware**  |Capturing demand|The feature                           |Connecting the feature to an outcome           |Your solution delivers the benefit|

### How to use this in practice

**For ads and cold outbound**: Lead with the alternative or the problem. Don't open with your product name.

**For landing pages from branded search**: Lead with capability or feature. They already know you.

**For persona pages**: Match the awareness stage of that segment. Enterprise buyers are often more problem aware; power users are often product aware.

-----

## Output format

When applying this skill:

1. **Identify first**: What's the product? Which positioning strategy? Which GTM type? Bottom-up or top-down?
1. **Map the ICP**: Who is the primary buyer? What awareness stage are they likely at?
1. **Draft the message**: Use the right framework for the channel or page type
1. **Check the copy**: Does it lead with the right thing for the awareness stage? Does each persona get their own message?

Produce output as structured copy blocks with clear labels, not paragraphs of prose. Make it easy to drop into a page or doc.

### Homepage copy block structure

```
HERO
Headline: [Capability + Use Case — short, punchy, no product name required]
Subhead: [Who it's for + the problem it solves — 1 sentence]
CTA primary: [Action verb + specific outcome — not "Learn More"]
CTA secondary: [Low-friction alternative — "See how it works"]
Note: [Remove friction — "No credit card needed", "Takes 15 minutes"]

PROBLEM SECTION
[Name the daily pain in the customer's language — validate before selling]
[2-3 specific scenarios that make them feel seen]
[End with empathy, not blame]

CAPABILITY SECTION
[What they can now do — one block per capability, short]
[Input → Action → Output for each]

BENEFIT SECTION
[Emotional payoff — what this actually means for their work and career]
[2-3 specific outcomes they care about]

SOCIAL PROOF
[Peer quotes from the same role, not executives]
[One stat if you have a real one]
[Format: quote + role + company stage]

FINAL CTA
[Urgency from a real scenario, not artificial pressure]
[Repeat primary CTA + friction remover]
```

Once you have the copy structure, run it through the **Righter skill** to tighten the writing — active voice, grade 5 reading level, no weakeners, no em dashes.
