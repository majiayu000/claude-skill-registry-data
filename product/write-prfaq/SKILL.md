---
name: write-prfaq
description: Use when defining a new product, feature, or service before committing resources to build it — especially for initiatives with unclear customer value, competing solution approaches, or significant investment required. Trigger before writing a PRD or technical spec for any initiative above a certain size threshold.
source: Amazon Working Backwards process (Ian McAllister, former Amazon PM Director), "Working Backwards" by Colin Bryar and Bill Carr (2021), AWS product development culture
related: [apply-narrative-memo-discipline]
tags: [product, amazon, working-backwards, press-release, customer-value, ideation, alignment, strategy]
verified: true
---

# Write PR/FAQ

Write an Amazon-style Press Release and Frequently Asked Questions document to define a product by working backwards from the customer — before any design or engineering begins.

## Why This Is Best Practice

**Adopted by:** Amazon (mandatory for all new products and major features since the early 2000s), AWS (every service launch begins with a PR/FAQ), and companies that have adopted the working-backwards method including Stripe, Shopify, and teams at Google and Meta.

**Impact:** Amazon's PR/FAQ process is credited with producing products that customers actually want versus products that engineers find interesting. Colin Bryar and Bill Carr's 2021 book "Working Backwards" documents how this process drove products like Kindle, Prime, AWS, and Alexa. Ian McAllister (former Amazon PM Director) reports that the process surfaces fatal flaws in about 30% of proposed features before any engineering investment is made.

**Why best:** Most product development starts with a solution and works forwards to rationalize it. PR/FAQ forces the reverse: start with the customer experience at launch and work backwards to what must be true for that to exist. This eliminates solutions looking for problems. Writing a compelling press release is a forcing function — if you cannot write one sentence that a customer would find exciting, the product likely isn't worth building.

Sources: Ian McAllister, "Amazon's approach to product development" (Quora, 2012, widely cited); Colin Bryar & Bill Carr, "Working Backwards" (St. Martin's Press, 2021); Werner Vogels, "Working Backwards" (All Things Distributed blog).

## Steps

1. **Write the press release first** (1 page maximum). Structure it as if the product has already launched and a reporter is covering it. Include:
   - Headline: the product name and its one-sentence value proposition
   - Subheadline: who it is for and the primary benefit
   - Problem paragraph: the customer problem in the customer's voice (not internal jargon)
   - Solution paragraph: how the product solves it, written in plain language
   - Customer quote: a specific, believable quote from a target customer describing their experience
   - Call to action: how to get started

2. **Write the internal FAQ** (2–5 pages). Answer the hard questions a skeptical executive would ask:
   - What customer problem does this solve, and what is the evidence it is a real problem?
   - Who is the target customer? How many of them exist?
   - Why will customers choose this over alternatives (including doing nothing)?
   - What does success look like in 1 year? 3 years?
   - What are the biggest risks and how will you mitigate them?
   - What does this cost to build and operate?
   - What is out of scope for the first version?

3. **Share with stakeholders for written feedback** — not a verbal discussion. Amazon's culture requires written feedback in the same document. This prevents the loudest voice in the room from dominating.

4. **Iterate the PR/FAQ** based on feedback, typically 2–4 revision cycles. The PR/FAQ is done when reviewers have no more hard questions that the document doesn't answer.

5. **Use the approved PR/FAQ as the north star** for the PRD, technical spec, and design brief that follow. Any proposed feature that doesn't appear in the press release is a candidate for descoping.

## Rules

- The press release must be written in the voice of a real journalist writing about a launched product — not in corporate marketing language. Avoid: "leverage," "synergy," "paradigm-shifting," "best-in-class."
- The customer quote must be specific and believable. Bad: "This product is amazing!" Good: "I used to spend two hours every Monday pulling reports from three different tools. Now I get everything in one place before my first coffee."
- Internal FAQ answers must be honest about risks and weaknesses. A FAQ that only promotes the idea is a red flag.
- The press release must be readable by someone outside your company. If you need to explain internal terminology to understand the headline, rewrite the headline.
- Length limit on the press release is enforced: one page, no exceptions. This constraint forces clarity.
- Do not include timelines, engineering estimates, or technical architecture in the PR/FAQ. Those belong in downstream documents.

## Examples

**Headline (bad):** "Introducing Project Horizon: A Next-Generation Data Orchestration Platform for Enterprise Stakeholders"

**Headline (good):** "Acme Analytics Launches One-Click Reports: Finance Teams Get Weekly Summaries Without Writing SQL"

**Customer quote (bad):** "This solution dramatically improves our operational efficiency and enables data-driven decision-making at scale."

**Customer quote (good):** "Before this, I'd spend my Friday afternoon manually pulling numbers from Salesforce, Stripe, and our data warehouse. Now it's there every Monday morning. I actually left work on time last Friday for the first time in six months." — Sarah T., Finance Manager at a Series B SaaS company

**FAQ answer (bad):** "We will build a robust and scalable infrastructure to support millions of users."

**FAQ answer (good):** "Year 1 success: 500 active teams with a 60-day retention rate above 70%. We believe this is achievable because we have 80 design partners who have confirmed they will use the product if we ship the core reporting feature by Q2."

## Common Mistakes

- **Investor pitch tone:** PR/FAQs written to impress executives instead of describe customer experience. The press release must be written as if it is already real, not aspirational.
- **Skipping the customer quote:** This is the hardest section to write and the most valuable. If you cannot write a specific, believable customer quote, you do not yet understand your customer.
- **FAQ answers that are too short:** "What are the risks?" answered with "We will mitigate risks appropriately" is not an answer. Name the specific risks and specific mitigations.
- **Using the PR/FAQ as a PowerPoint substitute:** PR/FAQs are read silently at the start of a meeting, not presented slide by slide. Format for silent reading: full paragraphs, no bullet points in the press release section.
- **Treating it as a one-time artifact:** The PR/FAQ should be revisited at major milestones (beta, launch, post-launch) to check whether the product you built matches the product you promised customers.
