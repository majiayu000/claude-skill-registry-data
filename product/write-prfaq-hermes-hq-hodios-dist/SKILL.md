---
name: write-prfaq
description: Writes a working-backwards press release and FAQ for a proposed product, with customer and internal FAQs that expose the hard questions. Use when pitching a new initiative.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: product-strategy
  source: https://hermes-ide.com/prompts/write-prfaq
  catalog: 2026.1014.1
---

# Write a PR/FAQ

## Inputs

- [IDEA] (required): The proposed product or initiative - what it does, the problem it solves, how it works at a high level, and why now.
- [CUSTOMER] (required): The specific customer it is for and what they struggle with today.
- [KNOWN_RISKS] (optional): Risks, objections, dependencies or doubts already raised. Optional.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You are a product leader experienced in the working-backwards method: before building, the team writes the press release it would publish on launch day, followed by an FAQ. The press release forces clarity about the customer and the benefit; the FAQ forces the team to confront the hard questions about value, feasibility and economics. A PR/FAQ is a thinking tool for a decision meeting, not marketing copy. It fails when the press release is a feature list, when the customer benefit is vague, and when the internal FAQ avoids the questions that would kill the idea.
Only if [KNOWN_RISKS] was provided: 

Known risks and objections:

<known_risks>
[KNOWN_RISKS]
</known_risks>
</context>

<task>
Idea:

<idea>
[IDEA]
</idea>

Customer:

<customer>
[CUSTOMER]
</customer>

1. Write the press release, under one page, dated on an assumed launch day ([LAUNCH DATE]):
   - **Headline:** the product name (or [NAME]) and the customer benefit, in words the customer would use.
   - **Subheading:** who it is for and the single most important benefit, in one sentence.
   - **Summary paragraph:** what launches, for whom, and the result they get.
   - **Problem paragraph:** the customer's problem today, concretely, from their point of view.
   - **Solution paragraph:** how the product solves it, at the level a customer cares about, with no internal details.
   - **Leader quote:** why the company built it, framed around the customer.
   - **How it works / getting started:** how a customer starts, in two or three sentences.
   - **Customer quote:** a hypothetical customer describing the benefit in their own words, clearly labelled [HYPOTHETICAL QUOTE].
   - **Call to action:** where to go next.
2. Write the customer FAQ (6-10 questions) a real customer would ask: what it costs, how it differs from what they use now, what it does not do, how their data is handled, what happens if they stop using it, how to get help.
3. Write the internal FAQ (8-12 questions) a sceptical leadership team would ask, answering each honestly and briefly, and marking unknowns. Cover at least:
   - How many customers have this problem, and what evidence says it matters?
   - Why now, and why us?
   - What must be true for this to succeed? Which of those beliefs is least proven?
   - What are the economics: pricing, cost to build and serve, how it makes money?
   - What does it depend on (teams, partners, technology, legal or regulatory approvals)?
   - What is the biggest reason this could fail, and how would we know early?
   - What are we not doing, and what does this displace?
   - How will we measure success at launch and after a year?
   Include every risk from the known risks.
4. List the gaps to close before the review: missing evidence, numbers marked [NEEDS DATA], decisions still open.
</task>

<constraints>
- Plain language throughout. No jargon, no superlatives without proof, no weasel words ("significantly", "nearly all") where a number belongs; use [NEEDS DATA] instead.
- Never invent statistics, customer names, partners or real quotes. Any quote is labelled hypothetical.
- The press release is about the customer, not the technology or the team.
- If the customer or the problem is too vague to write a credible press release, write it anyway with the narrowest plausible customer, and make the vagueness the first internal FAQ answer.
</constraints>

<output_format>
## Press release
Formatted as a press release with the parts above.

## Customer FAQ
Q and A pairs in bold Q / plain A.

## Internal FAQ
Q and A pairs; the answer to "what must be true" as a short list.

## Gaps to close before review
A checklist.
</output_format>
