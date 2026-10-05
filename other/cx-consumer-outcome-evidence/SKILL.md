---
name: cx-consumer-outcome-evidence
description: Use to assemble evidence that customers are getting good outcomes from support, at the level a board or regulator expects, rather than reporting activity metrics. Trigger for "evidence our customers get good outcomes", "consumer duty evidence from support", "board report on customer outcomes", outcomes-based regulatory reporting, or a request to show harm is not occurring.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Evidencing customer outcomes

Outcomes-based regulation asks a question that ordinary CX reporting cannot answer.
Response time, CSAT and QA scores describe **activity and satisfaction**. The question is
whether customers ended up in the right place — and specifically whether any group of
them is systematically ending up in the wrong one.

The gap shows up sharply the first time someone asks "how do you know customers aren't
being harmed?" and the answer is a dashboard of averages.

## Averages hide the thing being asked about

The question is about distribution and about groups, not about the mean.

An operation with a 4.5 CSAT and a 92% QA score can be failing a specific group badly:
customers in one language, on one channel, with one product, or with a characteristic
that makes them less able to advocate for themselves. **The average is evidence that
most customers are fine, which was not the question.**

So the analytical shape is: **pick outcomes, define them observably, then look for
groups where they are worse — and specifically for groups whose worse outcome you could
not defend.**

## Define outcomes observably

An outcome has to be something you can see in data, not a sentiment. For support, the
defensible ones:

- **Did the customer get what they were entitled to?** Redress paid where owed, the
  entitlement granted, the cancellation completed.
- **Did they get it without disproportionate effort?** Contacts to resolution, channel
  switches, time from first contact, times they had to repeat themselves.
- **Did they understand it?** Repeat contact on the same issue after an explanation is
  the strongest available proxy for a communication that did not land.
- **Was the issue resolved, and did it stay resolved?** Reopen and repeat rate.
- **Were they able to exercise their rights?** Complain, cancel, switch, claim — measured
  as completion, not as availability.
- **Did anything go wrong that we caused and did not fix?** Unresolved failures, and how
  long they stayed unresolved.

Note that most of these are computable from data you already have. The barrier is
usually framing rather than instrumentation.

## Look for the groups, deliberately

Segment every outcome and go looking for gaps rather than waiting for one to surface:

- **Channel**, especially voice against digital.
- **Language and market.**
- **Customers with vulnerability signals**, handled at aggregate level only.
- **Digital capability proxies** — customers using assisted channels, needing repeat
  explanation, or acting through a third party.
- **Product and plan**, including legacy products, which are a recurring source of poor
  outcomes because nobody maintains them.
- **Tenure**, since long-standing customers on old terms are frequently worse off.
- **Anything you could not defend** — where an outcome gap correlates with a protected
  characteristic or a proxy for one, that is the headline finding and it changes the
  document from a report into an escalation.

Where a gap exists, the honest report says so. **A report that finds no gaps anywhere
will be read as a report that did not look**, and it is the least credible outcome
available. If genuinely nothing is found, say what you tested and what would have been
detectable at your sample sizes.

## Evidence, not assertion

The standard here is higher than internal reporting. Every claim needs the same four
things:

1. **The definition**, precisely, including the date field and the exclusions.
2. **The population**, and what it omits — channels not covered, records not synced.
3. **The number, with its interval**, and the absolute counts alongside any rate.
4. **The method**, reproducible by someone else from the description.

Then, distinctly:

- **What the evidence does not establish.** Say it explicitly. An assessment that claims
  more than its data supports is worse than one with acknowledged gaps, because the gap
  will be found by someone else.
- **What action followed.** Evidence of a gap with no action attached is a finding about
  governance, not just about outcomes. The question is always "and what did you do?"

## Negative assurance is the hard part

Showing good outcomes exist is easier than showing harm is absent, and the second is
what is really being asked.

Approach it as coverage rather than proof:

- **Enumerate the harms you looked for**, and for each, what you would have seen if it
  were occurring.
- **State the detection sensitivity** — a harm affecting 50 customers is invisible in a
  sample of 200, and saying so is the honest position.
- **Name what you cannot see at all**: customers who never contacted you, silent
  dissatisfaction, harms with no operational trace.
- **Say where you have no data**, rather than reporting the covered part as the whole.

"We tested for these six harms, at these sensitivities, and found evidence of two" is
credible. "No harm detected" is not.

## Make it repeatable

This gets asked for periodically, and the second edition is where the value is — because
comparison across periods is the actual evidence of whether things are improving.

Fix the definitions, version them, and treat a definition change as breaking the series
and requiring disclosure. Freeze the figures as published, and if restated later, label
the restatement. An outcome series whose definitions drift quietly is worse than no
series, because the trend is fictional and the document asserts otherwise.

## Guardrails

- **This assembles evidence; it does not conclude compliance.** Whether the evidence
  discharges an obligation is a determination for compliance, legal and the board.
- **Do not tune the analysis toward a reassuring conclusion.** If the brief arrives as
  "show that outcomes are good", say plainly that the assessment has to be able to find
  a problem to be worth anything, and run it that way.
- **Handle vulnerability data at aggregate level only.** No named lists, no disclosure
  text, restricted distribution.
- **Do not include protected characteristics you do not lawfully hold** in order to test
  for gaps. Where you cannot test for a disparity, say that you could not, rather than
  inferring the characteristic from a proxy.
- **Expect this document to be read externally.** Write it accordingly.
- **Cite ids and aggregates; never transcripts.**

## Present results to the user

1. **Scope and definitions**, versioned, with the population and its omissions.
2. **Outcome measures**, each with intervals and absolute counts.
3. **Group gaps found**, with the indefensible ones separated and escalated.
4. **What was tested and not found**, with detection sensitivity — the negative-assurance
   section, framed as coverage rather than proof.
5. **What cannot be seen at all**, including customers who never contacted you.
6. **Action taken against each gap**, with owners and dates — the governance half of the
   answer.
7. **Comparison to the previous period**, with any definition change disclosed as breaking
   the series.
8. **What requires a compliance or board determination** rather than an operational fix.
