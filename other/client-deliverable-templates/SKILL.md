---
name: client-deliverable-templates
description: Fill-in templates for client-facing programmatic deliverables, with the honesty rules baked in. Use when the user asks for a "media plan template", a "QBR deck" or "business review", a "client proposal", how to "explain this to a client" or put it in "plain English", a "client glossary", how to "deliver bad news to a client", or a "client report template". Provides a media plan, a QBR slide spine, a proposal outline, a plain-language glossary, and a bad-news framing pattern.
---

# Client deliverable templates

Repeatable, fill-in templates for the things a client-facing programmatic team writes again
and again: the media plan, the quarterly business review, the proposal, the glossary that
translates jargon, and the message that delivers bad news. The templates carry the structure
and the honesty rules so every deliverable is clear, sourced, and trustworthy by default,
whatever DSP the work ran on.

Use these when the deliverable goes to a client. For the analysis that produces the numbers,
see the `reporting-by-campaign-goal` skill and hand off to the `reporting-analyst` agent. To
shape the narrative voice, use the `client-communications-lead` agent. Before anything ships,
route it through the `qa-scrutinizer` agent, which checks for exactly the failures this skill
is built to prevent.

## When to use this skill

- "Give me a media plan template" or "build a media plan for this campaign."
- "I need a QBR deck" or "structure a quarterly business review."
- "Write a client proposal" or "put together a pitch for this account."
- "Explain this to a client" or "say this in plain English" or "drop the jargon."
- "I need a client glossary" or "what does [term] mean for a client."
- "How do I deliver bad news to a client" or "the campaign missed, how do I tell them."
- "Give me a client report template."

Boundary: this skill provides the deliverable shell and the honesty bar. It does not decide
which KPI belongs to which goal (that is `reporting-by-campaign-goal`), compute the metrics
(that is `programmatic-foundations`), or produce the verified numbers and analysis (that is
the `reporting-analyst` agent). Fill these templates with numbers that came from those, never
with numbers invented to fit the template.

## Quick reference

| The user needs | Use this template | What it gives them |
| --- | --- | --- |
| A plan before a campaign runs | `assets/media-plan-template.md` | Objective, KPI and targets, audience, channel mix, flighting, budget by funnel stage, measurement, assumptions, and a labeled forecast |
| To present a quarter to a client | `assets/qbr-deck-outline.md` | A fixed slide spine: cover, three-number summary, performance vs goals, what worked, what did not and what changed, market context, learnings, next-quarter plan and budget, appendix |
| To win new work | `assets/proposal-outline.md` | Problem, approach, why us, scope, investment, outcomes as ranges, next steps |
| To translate a term for a client | `assets/client-glossary.md` | Each common term mapped to one plain client sentence |
| To deliver a miss or a problem | `assets/bad-news-framing.md` | The situation, what we saw, what we are doing, what we need from you, with a worked example |

Pick the template by the deliverable, fill every bracket, and apply the honesty rules below
to every line before it leaves the building.

## Core process

1. **Confirm the numbers are real and sourced before you touch a template.** Pull verified
   figures and the analysis from the `reporting-analyst` agent and the
   `reporting-by-campaign-goal` skill. A template makes a story look finished, which is
   exactly why it must never be filled with a number you cannot trace to a report.
2. **Pick the template that matches the deliverable** from the quick-reference table, and keep
   its structure. The order is the value: a QBR always leads with the result, a bad-news note
   always leads with the situation and ends with the ask. Do not reorder the spine.
3. **Fill every bracket in plain language.** Replace each placeholder with the client's actual
   objective, audience, and numbers. Swap any jargon for the plain sentence in
   `assets/client-glossary.md`, or paste those rows into an appendix. A blank field reads as an
   oversight, so write "to be confirmed" rather than leaving it empty.
4. **Apply the honesty rules to every line** (see the next section). This is the step the
   `qa-scrutinizer` agent will check, so do it before, not after.
5. **State any forward-looking number as a range and label it an estimate.** Forecasts and
   expected outcomes go in the clearly marked sections of the media plan and the proposal,
   given as conservative, expected, and stretch, with the assumptions shown. Never present a
   forecast as a commitment.
6. **Route the draft through review.** Shape the voice with the `client-communications-lead`
   agent and send it to the `qa-scrutinizer` agent as the gate before it reaches the client.

## The honesty rules (what qa-scrutinizer checks)

These are non-negotiable and apply to every template in this skill. The `qa-scrutinizer` agent
checks client communication for precisely these, so build them in from the start.

- **No overpromising.** State targets as targets and forecasts as estimates with ranges and
  assumptions, never as guarantees. Do not commit to a number the evidence does not support.
- **No assist presented as a conversion.** Keep post-click and post-view separate. A
  view-through assist is not a conversion, and last-click credit is not proof of incremental
  impact. When a budget decision rides on it, lead with incrementality, not last-click. See
  `reporting-by-campaign-goal` and the platform measurement skill.
- **No correlation stated as a cause.** If two things moved together, say so. Do not claim one
  caused the other unless an experiment or a clean attribution path supports it. If the cause
  is uncertain, say it is uncertain and say what you are doing to find it.
- **Every number is sourced.** Each figure in a deliverable traces to a named report or study.
  If you cannot source it, it does not go in. This includes the numbers in a forecast, which
  trace to the stated assumptions.
- **Plain language.** Write for a non-technical reader. Translate every term with
  `assets/client-glossary.md`. No internal jargon without a plain-language gloss.
- **No em dashes in client text.** Use periods, commas, parentheses, or "and" and "but". This
  holds across every template and every filled-in deliverable.

## Reference material

The five templates live in `assets/` and are meant to be copied and filled, not read as
theory:

- `assets/media-plan-template.md`: the pre-flight plan. Objective, KPI and targets, audience
  strategy, channel and platform mix, flight and flighting calendar, budget split by funnel
  stage, measurement plan, assumptions, and a forecast section that is explicitly labeled an
  estimate. Use it when planning a campaign for a client.
- `assets/qbr-deck-outline.md`: the quarterly business review slide spine. A fixed order from
  cover through executive summary (three numbers), performance versus goals, what worked, what
  did not and what we changed, market and competitive context, learnings, next-quarter plan and
  budget, and an appendix. Use it to present a quarter.
- `assets/proposal-outline.md`: the new-business proposal. Problem, approach, why us, scope,
  investment, expected outcomes stated as ranges, and next steps. Use it to pitch or scope an
  engagement.
- `assets/client-glossary.md`: the two-column plain-language glossary, each jargon term mapped
  to one client sentence. The client-facing counterpart to the practitioner glossary in
  `programmatic-foundations`. Use it to translate any term in any deliverable.
- `assets/bad-news-framing.md`: the situation, what we saw, what we are doing, and what we need
  from you pattern, with a worked example. Use it for any miss, risk, or breakage.

## Templates and examples

A worked example ships inside `assets/bad-news-framing.md`: a retargeting campaign whose
recorded cost per order blew past target because a site change broke conversion tracking for
several days. It shows the four-part pattern in full, leads with the miss in the first
sentence, sources every number, separates the tracking break from the real performance, states
the expected recovery as a range, and ends with a concrete ask, without apologizing three
times or blaming the client.

For a media plan, the forecast table is filled as conservative, expected, and stretch columns
for each outcome (reach, primary KPI, and efficiency), under a heading that says in plain words
that these are estimates, not guarantees. For a QBR, the executive summary is exactly three
numbers, each shown against its target with one sentence of so-what.

## Common pitfalls

- **Filling a template with numbers that are not sourced.** The polish of a template hides the
  gap. Pull every figure from the `reporting-analyst` agent and name its source.
- **Presenting a forecast as a promise.** A forecast is an estimate on stated assumptions.
  Give it as a range and label it, or a client will hold you to the midpoint.
- **Calling an assist a conversion.** Keep post-click and post-view separate, and lead with
  incrementality when a budget decision is at stake.
- **Stating a correlation as a cause.** Two metrics moving together is not proof. Say "we saw"
  unless an experiment supports "we caused".
- **Leaving jargon in client text.** Translate it with `assets/client-glossary.md`. If the
  client has to ask what a word means, the deliverable failed at its one job.
- **Reordering the QBR spine or the bad-news pattern.** The order is the message. Result first
  in a QBR, situation first and ask last in bad news.
- **Skipping the review gate.** Shape the voice with the `client-communications-lead` agent and
  pass every client-facing draft through the `qa-scrutinizer` agent before it ships.

## Sources

- Attention Measurement framework (IAB and MRC), Interactive Advertising Bureau: https://www.iab.com/guidelines/attention/ (as of June 2026)
