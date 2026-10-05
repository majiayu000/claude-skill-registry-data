---
name: cx-ai-disclosure
description: Use to design and audit how customers are told they are interacting with AI, or that AI was involved in a decision about them, and to evidence that it happened. Trigger for "do we tell customers it's a bot", "AI disclosure requirements", "should the bot say it's not human", "customer asked if they were talking to a person", AI transparency obligations, or evidencing that an AI-assisted decision was explained.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Telling customers about AI

Three distinct obligations get collapsed into one conversation, and they have different
triggers, different audiences and different evidence:

1. **You are talking to a machine.** Transparency about the interaction itself.
2. **AI was involved in a decision about you.** Transparency about a process, which may
   carry a right to an explanation or to human review.
3. **Your conversation was processed by AI.** A data-processing question — QA scoring,
   sentiment analysis, summarisation — that the customer may never see any output from.

The third is the one most often missed, because nothing about it is visible to the customer.
A support operation running AI QA over every conversation is processing personal data with
AI, whether or not a bot ever replied.

**What is legally required varies by jurisdiction, sector and use, and it is changing.
Nothing here states an obligation.** This gives you the design and the evidence; the
determination is legal's.

## Design the interaction disclosure

**Up front, not on request.** A bot that identifies itself only when asked has left every
customer who did not think to ask uninformed. Disclose at the start of the interaction.

**In the conversation, not only in a policy.** A line in the privacy notice is not a
disclosure to someone in a chat window.

**Answer the direct question honestly, always.** "Am I talking to a human?" must get a
straight answer. A bot deflecting that question is the single worst failure available here,
it is trivially screenshotable, and it destroys trust in everything else you say about AI.
Test it explicitly — ask your own bot, in every language.

**Give a route to a human, and make it work.** Disclosure without an escape is worse than
none: the customer now knows they are stuck with a machine. Measure whether the route
completes, not whether it exists.

**Name it consistently.** A bot with a human-sounding name and no other signal is
misleading by design. If it has a persona, the disclosure has to be clearer to compensate.

**Handle the handover in both directions.** Tell the customer when they move from bot to
human, and when a human hands back to automation. Mid-conversation transitions are where
customers most often end up misled, because they reasonably assume continuity.

**Cover the channels people forget** — voice bots, proactive outbound messages, and
automated replies that look like a person wrote them. An automated acknowledgement in a
human agent's name is a disclosure failure hiding as a template.

## AI-assisted decisions

Where AI contributed to a decision affecting the person — a claim, a refusal, a redress
amount, an account action, or an agent's performance assessment:

- **Say that it was involved**, at the point the decision is communicated.
- **Explain the basis in terms the person can act on.** "The model scored it 62" is not an
  explanation. What factors mattered, and what would change the outcome.
- **Offer human review** where that applies, and make it real — a review that re-runs the
  same model is not human review, and a human who only sees the model's conclusion is
  rubber-stamping.
- **Record the provenance**: model, version, prompt, retrieved sources, raw output before
  post-processing. Without this the explanation cannot be reconstructed later, which is a
  separate problem when the person asks again in six months.

This applies internally too. An agent assessed with AI QA is a person subject to
AI-assisted decision-making about them, and the same transparency logic applies — plus
employment-law considerations that vary by jurisdiction.

## Auditing what actually happens

Design is the easy half. Test the operation:

- **Disclosure presence rate**, per channel, per path, per language. Automated paths built
  after the policy are the routine gap.
- **Position in the conversation** — was it first, or after several turns?
- **The direct-question test.** Sample conversations where the customer asked whether they
  were talking to a human, and check what happened. Report the honest-answer rate as its own
  number.
- **Handover disclosure**, both directions.
- **Human-route completion**, not availability.
- **Decision-explanation presence**, where AI-assisted decisions were communicated.
- **Consistency after a change.** A model or prompt change can alter behaviour without
  anyone updating the disclosure; re-test after every deployment.

## The failure modes worth naming

- **Disclosure on request only.** Covered above and worth repeating: it is the most common
  design.
- **A persona that undercuts the disclosure.** Disclosed once, then forty turns of
  human-styled conversation with a first name.
- **Disclosure in a language the customer is not using.**
- **A human-sounding automated reply** in a named agent's voice.
- **Silent escalation to AI.** A human conversation quietly continued by automation.
- **Invisible processing undisclosed.** QA scoring, sentiment analysis and summarisation of
  conversations, with nothing anywhere telling the customer.
- **Recording notification updated for AI and not the reverse** — a firm that discloses AI
  processing but has quietly started retaining transcripts longer to feed it.

## Guardrails

- **Do not state what the law requires.** Design and evidence; the obligation is legal's
  determination, and it differs by jurisdiction and is moving.
- **Never instruct a bot to deny being a bot**, or to deflect the question. If a system
  currently does either, that is an urgent finding, not an audit note.
- **Do not treat a disclosure as a licence.** Telling the customer it is AI does not make an
  otherwise-inappropriate automated interaction appropriate — a bot handling a
  vulnerability disclosure is a problem whether or not it introduced itself.
- **Do not remove a human route to improve containment.** If that has happened, report it as
  a conduct finding.
- **A disclosure failure affecting decisions already communicated** goes to compliance and
  legal, because the remedy may involve re-notifying customers.
- **Cite ids; quote only the disclosure line.**

## Present results to the user

1. **The three obligations, separated**, with which of them are in scope here and what is
   currently done for each — the invisible-processing one named explicitly.
2. **Design review** against the points above, per channel and per path.
3. **Presence and position rates**, per channel, path and language, in counts as well as
   rates.
4. **The direct-question test result**, as its own headline number.
5. **Handover disclosure**, both directions, and human-route completion rather than
   availability.
6. **AI-assisted decision explanations** — presence, and whether the explanation is actionable
   rather than a score.
7. **Provenance recording**, so an explanation can be reconstructed later.
8. **Internal application** — agents assessed by AI, and whether they were told.
9. **What needs a legal determination**, and anything requiring immediate change rather than
   a recommendation.
