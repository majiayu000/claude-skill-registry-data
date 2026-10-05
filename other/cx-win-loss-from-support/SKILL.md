---
name: cx-win-loss-from-support
description: Use to extract competitor mentions, switching language and feature-gap evidence from support conversations as an input to win/loss and product strategy. Trigger for "what competitors do customers mention", "why do customers switch away", "find feature gaps customers ask about", competitive intelligence from support, or win/loss analysis that only samples deals sales remembers.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Win/loss evidence in support conversations

Formal win/loss programmes interview a small, self-selected slice of deals, usually
months later, mediated by the account team's memory. Support conversations contain a
much larger, contemporaneous, unmediated record of the same subject — customers naming
competitors, describing what they cannot do, and explaining what they are switching to
and why.

It is a genuinely underused source. It is also a **badly biased sample**, and the
analysis is only worth anything if that is stated at the top.

## What the sample actually is

Three biases, all in the same direction:

- **It is post-purchase.** These are customers who already bought. Lost prospects never
  contacted your support, so this source is nearly blind to why you *lose deals* and
  reasonably good at why customers *leave*.
- **It is contact-conditioned.** You hear from customers engaged enough to ask. Silent
  switchers are absent.
- **It is topic-conditioned.** A competitor gets mentioned when it is relevant to the
  problem at hand, which over-weights integration and migration contexts and
  under-weights price.

So this is **input to** win/loss, never a substitute. Frame every finding as "among
customers who contacted support", and where you have a formal programme, use this to
generate hypotheses it can test on a proper sample.

## Four extractable signals

**1. Competitor mentions.** Who is named, in what context, and how the volume trends.
Context is the whole value — a competitor mentioned because the customer is migrating
*from* them means something opposite to one mentioned as an alternative they are
evaluating. Classify by context, not by count, or the analysis will report your
strongest migration source as your biggest threat.

**2. Switching language.** Data export requests, contract termination questions,
questions about running two systems in parallel, "our new provider needs…". These are
the clearest loss signals available and they arrive earlier than the churn event.

**3. Feature gaps, with evidence of consequence.** Support hears "I can't do X" with
the actual situation attached, which is more useful than a feature request in a portal.
Capture what the customer was trying to achieve and what they did instead — the
workaround is often the more important finding.

**4. Expectation mismatch at purchase.** Customers describing what they thought they
were buying. This is a sales and marketing finding, not a product one, and it is one of
the most valuable outputs because nobody else is looking for it. A rising rate is a
messaging problem with a measurable cost.

## Extract properly, or the numbers are noise

- **Search in every language you support.** Competitor names are stable across
  languages; the surrounding context is not.
- **Watch for name collisions.** Competitor names that are also ordinary words, product
  names, or your own integration partners will wreck a naive keyword count. Hand-label a
  sample and report the false-positive rate before quoting any volume.
- **Distinguish the competitor from the integration.** Many companies are simultaneously
  a competitor, a partner, and an integration target. A mention in an integration
  question is not competitive intelligence.
- **Exclude your own staff and automated content.** Internal notes discussing a
  competitor are not customer voice, and a macro or knowledge article mentioning one
  will match every conversation it was pasted into.
- **Count conversations, not mentions.** One long thread naming a competitor nine times
  is one data point.
- **Report a trend, not a level.** Absolute mention volume depends entirely on your
  extraction method; the change over time is comparable to itself and much more useful.

## The interpretation trap

**Competitor mention volume is not competitive threat.** It tracks the competitor's
marketing spend, their brand recognition, and how often their name comes up in normal
conversation — not how often they beat you.

What is informative:

- **Mention volume weighted by the revenue of the accounts mentioning them.**
- **The share of mentions in a switching context**, specifically.
- **Conversion of mention to actual departure** — for accounts that named a competitor,
  what happened next? This is the number that separates a competitor customers talk
  about from one that takes customers, and it is computable if you can join to churn
  outcomes.

Rank on the third. It reorders the list substantially in most businesses.

## Route the findings by owner

The output splits four ways, and pushing it all to product wastes most of it:

- **Product** — feature gaps with consequence and workaround evidence.
- **Sales and marketing** — expectation mismatch, competitor positioning that is landing,
  and the objections customers raise after buying.
- **Pricing** — where the gap is commercial rather than functional.
- **Support and knowledge** — where the capability exists and the customer could not find
  it, which shows up here disguised as a feature gap. **Check this before filing anything
  as a gap**; it is common and the fix is a paragraph, not a roadmap item.

## Guardrails

- **Do not use customer conversation content in competitive marketing.** Quoting a
  customer's private support conversation in a sales battlecard is a trust and
  potentially a legal problem.
- **Do not brief the account team to counter-sell inside an open support conversation.**
  Detection and commercial response stay separate.
- **Cite ids; do not paste transcripts** into a competitive intelligence deck. These
  circulate widely and outside the company more often than anyone plans.
- **Do not name individual customers** in a strategy document without a reason and a
  check on whether it is appropriate.
- **Say what the sample is** on every slide that shows a number, not once at the front.

## Present results to the user

1. **What the sample is and is not** — post-purchase, contact-conditioned, and therefore
   evidence about departure rather than about lost deals.
2. **Extraction quality** — how you searched, languages covered, and the hand-labelled
   false-positive rate.
3. **Competitor mentions by context**, with migration-from separated from
   evaluating-against, as a trend rather than a level.
4. **Mention-to-departure conversion**, if outcomes are joinable. The ranking that matters.
5. **Feature gaps with consequence and workaround**, after removing the ones that are
   really discoverability.
6. **Expectation mismatch**, routed to sales and marketing with volume attached.
7. **Hypotheses for the formal win/loss programme** to test on an unbiased sample.
