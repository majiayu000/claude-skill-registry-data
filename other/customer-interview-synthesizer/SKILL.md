---
name: customer-interview-synthesizer
description: "Synthesizes raw customer interview transcripts into themes, quotes, Jobs-to-be-Done (JTBD) signals, force-of-progress diagrams, and actionable opportunity hypotheses with confidence levels. Use when synthesizing a round of discovery, switching, win-loss, or churn interviews; preparing a research readout; aligning a team on what the customer signal actually says; or feeding inputs into an Opportunity Solution Tree (OST)."
---

# Customer Interview Synthesizer

> Turns hours of qualitative interviews into a tight, evidence-anchored set of opportunities.

## What this skill is

A structured workflow for synthesizing interview transcripts: code utterances, theme them, score saturation, extract Jobs-to-be-Done (JTBD) signals and forces of progress, identify opportunity hypotheses, and produce a readout that distinguishes evidence from interpretation. Designed to remove the analyst's narrative-fitting bias and keep the customer's voice central.

## What it solves

- "What did we learn?" readouts that summarize whichever interview was freshest
- Cherry-picking quotes that support a pre-existing hypothesis
- No theme saturation check (claiming a theme on a sample size of one)
- Conflating what the customer said with what the analyst inferred
- Failure to translate findings into prioritized hypotheses with confidence levels

## When to invoke

- Concluding a discovery or generative interview round
- Synthesizing switching interviews after a churn wave
- Win-loss analysis from a sales cycle
- Sensemaking after a competitive deep-dive
- Feeding the Opportunity Solution Tree (OST) with fresh evidence

## Phase 1: Catalog the corpus

For each interview, log:
- Participant pseudonym, segment, role
- Date, duration, interviewer
- Recording or transcript location
- Recruitment source (and any selection bias)
- Whether incentives were offered
- Whether the participant is current, former, or prospective customer

Minimum saturation guideline: 5-8 interviews per segment for generative discovery; more for major decisions.

## Phase 2: Code the utterances

Read each transcript line by line. Tag passages with **codes** - short labels for the topic discussed.

Two-pass approach:
1. **Open coding** - generate codes inductively from the data
2. **Axial coding** - group related codes into categories

Each code must include:
- A verbatim quote from the transcript
- Interview Identifier (ID) and timestamp
- Whether it's a **report** (something they did or experienced) or **opinion** (something they said they'd do)

Reports far outweigh opinions in predictive value. Flag the distinction.

## Phase 3: Theme the codes

Group codes into themes. For each theme:
- Theme title in the customer's voice
- Definition
- Number of participants who mentioned it (saturation count)
- 3-5 representative verbatim quotes
- Segments where the theme is strongest
- Disconfirming evidence (interviews where the theme didn't appear)

**Saturation rule**: a theme appearing in less than 30% of interviews in a segment is a hypothesis, not a finding.

## Phase 4: Extract JTBD signals

For passages describing what the customer was trying to accomplish:
- Write the job statement: *When [situation], I want to [motivation], so I can [outcome].*
- Classify functional / emotional / social
- Identify the job stage (Define / Locate / Prepare / Confirm / Execute / Monitor / Modify / Conclude)

## Phase 5: Forces of progress

For switching, churn, and win-loss interviews, map the four forces per participant:

| Force | Evidence from interview |
|-------|------------------------|
| Push of current situation | What was broken or frustrating? |
| Pull of new solution | What did they hope for? |
| Anxiety of new solution | What worried them about switching? |
| Habit of old | What kept them on the old solution? |

Aggregate across interviews to identify which force dominates the decision.

## Phase 6: Generate opportunity hypotheses

Convert themes into opportunity hypotheses:

> We believe [customer segment] experiences [pain or unmet need] when [situation], because [evidence].
>
> Confidence: [High / Medium / Low] based on [number of interviews] and [type of evidence].
>
> If we solved this, we'd expect to see [observable outcome].

Each hypothesis links back to:
- The theme(s) it came from
- The verbatim quotes that support it
- The disconfirming evidence (where it didn't show up)

## Phase 7: Separate observation from interpretation

The synthesis output has two tiers, clearly labeled:
- **What we heard** (verbatim, quoted, sourced) - high confidence
- **What it might mean** (analyst interpretation) - explicitly labeled as inference

Never blur the line. Stakeholders will treat them as the same unless you separate them.

## Output

- Coded transcript library (referenceable for any future synthesis)
- Theme list with saturation counts and supporting verbatims
- JTBD inventory: functional, emotional, and social jobs by segment
- Forces-of-progress diagram for switching or churn signals
- Opportunity hypothesis register with confidence levels and source evidence
- 1-page readout with the 3 most decision-grade findings
- Explicit list of disconfirming evidence
- Recommended next-round research questions

## Operating rules

**Always**
- Quote verbatim before paraphrasing
- Distinguish reports from opinions
- Score theme saturation (count of interviews / total interviews per segment)
- Surface disconfirming evidence explicitly
- Label observation versus interpretation

**Never**
- Claim a theme from a single interview
- Cherry-pick quotes that confirm a hypothesis
- Use the analyst's words as if they were the customer's
- Skip the recruitment-bias note
- Merge wildly different segments into one theme
