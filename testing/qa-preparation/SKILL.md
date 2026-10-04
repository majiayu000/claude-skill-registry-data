---
name: qa-preparation
description: Builds a management Q&A preparation pack of the hardest buyer and investor questions with crisp, evidence-backed answers, for use when management faces tough diligence or roadshow questioning.
---

# Q&A Preparation Agent

## When to use
Use this agent when management is about to face tough questions from a buyer, a sponsor, or an institutional investor: a management presentation, a diligence session, a roadshow, or an investor call. It is most valuable in the days before a live meeting when the team needs to be sharp under pressure and cannot afford a fumbled answer on a sensitive topic.

## What it does
It produces a Q&A prep pack: a structured set of the hardest anticipated questions, organized by theme, each paired with a crisp draft answer, the supporting proof points, and a bridging line to steer back to the equity story.

## Method
This agent runs a structured management Q&A preparation process.

1. Frame the audience and their agenda. Identify who is asking, what they are trying to disprove, and the two or three concerns most likely to move price or certainty of close.
   - A strategic buyer probes synergy and integration; a sponsor probes cash generation and the exit; a lender probes downside and covenants.
   - Good framing names the single question that, answered badly, kills the deal, and builds the pack backward from it.

2. Generate the hard questions by theme. Build a question bank across five themes so nothing is missed.
   - Financials: margin trend, quality of earnings, working capital swings, one-time items, revenue recognition.
   - Customers and management: concentration, churn, and pricing power; bench depth, key-person risk, and retention.
   - Risk and growth: litigation, regulation, competition, and supply; pipeline credibility, capacity, and the capital the plan actually needs.

3. Rank the questions by difficulty and likelihood. Score each on how likely it is to be asked and how much damage a weak answer does.
   - Flag the handful that are both very likely and potentially damaging; these earn the most rehearsal time.

4. Draft crisp answers. Write a lead sentence that answers directly, then two or three supporting sentences.
   - Avoid hedging and never volunteer a new problem the counterparty had not raised.
   - What good looks like: the answer survives one hostile follow-up without the story changing.

5. Attach proof points. Tie each answer to a specific, verifiable fact.
   - Use a cohort retention number, an audited margin, a signed contract, or a backlog figure; an answer without proof is only an opinion.

6. Prepare bridges. For each sensitive answer, draft one bridging line that acknowledges the concern and returns to the core thesis.
   - The bridge pattern: name the concern in one clause, then pivot to the strongest fact in the equity story.

7. Build the landmine list. Isolate the two or three questions the team most fears.
   - Script the exact wording, including what not to say, and assign one spokesperson per topic so answers never contradict.

8. Rehearse and pressure-test. Run a mock session and ask follow-ups until answers stop wobbling.
   - Note every place an answer shifted under pressure, tighten it, and run the drill again.

## Inputs
- The audience type and the meeting format (management presentation, diligence call, roadshow)
- The equity story or investment thesis being presented
- Recent financials and any known soft spots such as margin dips or customer losses
- Any prior questions raised by this counterparty or by comparable buyers
- Topics management wants to avoid or feels nervous about
- The named spokespeople and who owns which subject area
- The timing and sequence of upcoming meetings

## Output format
Claude returns a themed Q&A pack with these sections:
- An audience read: one paragraph on who is asking and their likely agenda.
- A themed question bank: for each of the five themes, the anticipated questions ranked by difficulty and likelihood, expressed in prose such as "high likelihood, high damage" rather than a table grid.
- Answer cards: under each question, a direct draft answer, the proof points to cite, and a bridging line.
- A landmine section: the two or three most dangerous questions with fully scripted responses and the assigned spokesperson.
- A rehearsal checklist: the mock-session drills and the hostile follow-ups to fire.

## Example
For Northwind Logistics, a regional freight operator preparing for a sponsor diligence session, the customer theme surfaces: "Your top three shippers are 41 percent of revenue. What happens if you lose one?" The drafted answer leads directly: contracts with all three run through 2028 with auto-renewal and volume minimums. Proof points are the signed master agreements, a 96 percent renewal rate over five years, and the fact that Northwind runs dedicated lanes that are costly for shippers to re-tender. The bridge: "Concentration reflects deep integration, which is exactly why net revenue retention has stayed above 105 percent." The landmine list flags a pending rate dispute with the second-largest shipper, assigns the CFO to answer it, and scripts a response that states the reserve already taken and avoids speculating on the outcome.
