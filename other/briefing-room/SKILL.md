---
name: briefing-room
description: Use when the user brings messy, layered, scattered, overloaded, or ambiguous context and asks to organize it into a brief. Trigger on notes, transcripts, research dumps, meeting context, strategy thoughts, emails, Slack threads, customer feedback, planning fragments, personal context, or requests like "make sense of this," "structure this," "what matters here," "clean this up," "prepare this for Ground Truth," or "prepare this for The Quorum."
---

# The Briefing Room

The Briefing Room turns messy context into a brief a human can think with.

The goal is not to make the input short. The goal is to make it usable. A normal summary compresses. A briefing organizes: it separates what is known from what is inferred, makes unresolved tensions visible, and gives the person a cleaner surface for judgment, creativity, planning, critique, or deeper agent work.

Use this skill when the user is overloaded by context and needs help seeing the shape of the situation.

---

## When To Use

Use The Briefing Room when the user has enough material to organize, but the shape of the situation is not yet clear:

- scattered notes, transcripts, messages, research, or feedback
- competing interpretations of the same situation
- uncertainty about what is fact, claim, assumption, or open question
- personal or professional context that needs sensemaking before advice
- preparation for Ground Truth, The Quorum, drafting, research, planning, or human review

## When Not To Use

- Use a normal summary when the user only asks for compression and no deeper structure is needed.
- Use Ground Truth when the user already has a clear claim, plan, or thesis and wants it challenged.
- Use The Quorum when the user already has a meaningful decision, trade-off, or strategy question that would benefit from multiple expert lenses.
- Use direct drafting when the user already knows the message, audience, and goal.
- Ask clarifying questions first when the input is too thin to organize without inventing context.

---

## Core Principles

**1. Organize before advising.**
Do not jump straight to a recommendation. First make the context legible. The user may need clarity more than advice.

**2. Preserve useful complexity.**
Do not flatten nuance into a generic summary. Keep contradictions, minority signals, awkward details, and uncertainty if they matter.

**3. Separate evidence levels.**
Distinguish facts, claims, interpretations, assumptions, and unknowns. This is the difference between a brief and a polished blur.

**4. Name the implied task.**
Messy context often hides what the person is actually trying to do: decide, explain, plan, create, diagnose, align, or learn. Name that implied task when possible.

**5. Make it readable for a human first.**
The brief may later feed Ground Truth, The Quorum, research, drafting, or planning, but the primary reader is a human trying to regain agency.

**6. Do not invent missing context.**
If something is not provided, mark it as unknown. Do not fill gaps with plausible-sounding facts.

**7. Ask only when the input is too thin.**
If there is enough material to structure, produce the brief and list open questions. Ask clarifying questions first only when the request cannot be usefully organized from what was provided.

---

## Quick Reference

| Input Type | Briefing Focus |
| --- | --- |
| Messy notes | Themes, facts, assumptions, tensions, open questions |
| Meeting dump | Strategic question, perspectives, action owners, unresolved decisions |
| Research dump | Topic clusters, evidence quality, claims, contradictions, missing proof |
| Product or strategy thoughts | Objective, theory, user/customer signals, options, constraints, risks |
| Customer feedback | Raw observations, repeated pain points, outliers, validation needs |
| Personal context | Situation, practical constraints, emotional stakes, uncertainty, reflection paths |
| High-stakes or current-fact context | Evidence status, verification needs, expert-review needs, unsupported claims |
| Prep for Ground Truth | A clean claim/theory plus assumptions, evidence, risks, and unknowns |
| Prep for The Quorum | A structured decision context with options, trade-offs, stakes, and open questions |

---

## Default Output Format

Use this structure by default. Rename or omit sections only when the context clearly calls for it.

```markdown
# Brief

## Top Readout
The 2-4 most important things the reader should understand first.

## Situation
What is going on, in plain language.

## Core Objective
What the person appears to be trying to understand, decide, explain, create, or improve.

## Important Context
The details that matter, grouped by theme.

## Known Facts
What appears directly supported by the provided material.

## Claims And Interpretations
What is being asserted, inferred, framed, or believed, but not fully proven by the material.

## Assumptions
What has to be true for the current thinking, plan, or concern to hold.

## Tensions And Contradictions
Where the context conflicts, feels unresolved, points in multiple directions, or creates trade-offs.

## Open Questions
What is still unclear and would materially improve understanding.

## Emerging Decisions Or Next Moves
The choices, actions, drafts, investigations, or conversations implied by the context.

## Recommended Next Use
What this brief is now ready for: human review, Ground Truth, The Quorum, drafting, research, planning, or more context gathering.
```

---

## Scale The Brief To The Mess

Match the output size to the input's complexity:

- **Small messy input:** produce a compact brief. Keep each section short and combine sections when helpful.
- **Medium messy input:** use the full structure, but keep the total brief dense and skimmable.
- **Large or high-stakes input:** preserve more detail, group context by theme, and make open questions/action paths explicit.

Do not expand a short input into a bloated memo just because the template has many sections. The template is a thinking scaffold, not a word-count target.

When the user asks for something "brief," "quick," or "sendable," prioritize a concise Top Readout, grouped bullets, and only the sections that materially help.

---

## Example

Messy input:

```text
Sales says enterprise prospects love analytics, support says onboarding is the real problem,
product wants dashboards because they are half-built, and marketing has a campaign in three weeks.
The CEO asked whether to go upmarket or fix activation first.
```

Useful briefing move:

```markdown
## Top Readout
- The real question is not "analytics or onboarding"; it is whether the company is optimizing for enterprise expansion or activation repair.
- The current evidence is split by function: sales has prospect enthusiasm, support has churn/friction signals, product has build momentum, and marketing has campaign timing pressure.
- The situation is ready to pressure-test, but not ready for a confident decision until churn and onboarding evidence are reviewed.
```

This is better than a summary because it names the hidden decision, separates perspectives, and shows what evidence would change the next move.

---

## How To Handle Different Inputs

**Notes or personal context**
Organize into themes. Preserve emotional stakes when they matter, but do not over-psychologize. Separate what happened from what the user fears or hopes it means.

**Meeting transcripts**
Extract the situation, decisions discussed, action items, disagreements, unresolved questions, and follow-ups. Preserve who owns what if names are present.

**Research dumps**
Group by topic and evidence quality. Label source types when useful: internal incident, direct observation, user/customer quote, vendor claim, third-party commentary, unverified current-fact claim, or missing source. Pull out contradictions and what evidence would settle the issue.

**Strategy or product thinking**
Identify the goal, current theory, target user/customer, assumptions, constraints, options, risks, and decision readiness.

**Customer feedback**
Separate raw observations from interpretations. Cluster repeated pain points, outliers, feature requests, and signals that need validation.

**High-stakes or current-fact context**
Do not present the brief as verification, professional advice, or a substitute for current sources. Organize what the user provided, label unsupported claims, and make verification or expert review an explicit next use when accuracy, safety, legal, medical, financial, or reputational stakes matter.

---

## Briefing Stance

Write like a sharp operator preparing a principal for a thoughtful conversation:

- clear but not simplistic
- structured but not sterile
- concise but not reductive
- direct about uncertainty
- careful with unsupported claims
- useful for both human review and agent handoff

Avoid:

- generic executive-summary filler
- premature recommendation
- false certainty
- burying contradictions
- treating every situation as a decision
- over-formatting tiny inputs
- making the user feel their messy context was "cleaned" by deleting the hard parts

---

## Decision Readiness

When the context implies a decision, include a short readiness assessment inside **Recommended Next Use**:

- **Ready to decide:** enough facts, options, constraints, and stakes are visible.
- **Ready to pressure-test:** the core theory is visible but needs critique.
- **Ready for council:** meaningful options and trade-offs exist, with enough stakes for deliberation.
- **Needs more context:** decisive facts, options, constraints, or objectives are missing.
- **Exploratory:** the material is sensemaking, not yet a decision.

Do not force the context into a decision workflow if the user is still trying to understand what they think.

---

## Example Openers

Use plain, grounded openers:

- "Here is the brief I would work from."
- "I would structure the situation this way."
- "The useful shape of this context is..."

Avoid praise-first openers like "Great question" or "This is really interesting." The user brought messiness; give them structure.

---

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Turning the brief into advice | Organize first. Put recommendations only in next-use language unless the user asks for advice. |
| Using every template section for tiny inputs | Combine or omit sections so the brief stays proportional. |
| Hiding contradictions to sound polished | Preserve tensions explicitly; contradictions are often the point. |
| Treating personal context as life coaching | Structure the context without telling the user what to do. |
| Treating claims as facts | Label assertions, interpretations, assumptions, and unknowns separately. |
| Treating a brief as verification | Make evidence status and verification needs explicit. |
| Forcing every situation into a decision | Some briefs are for sensemaking, reflection, research, or communication. |
| Producing a generic executive summary | Show the shape of the mess, not just the cleanest-sounding version. |

---

## Final Check

Before answering, check:

1. Would a human understand the situation faster after reading this?
2. Is the Top Readout strong enough that the reader has an immediate handle?
3. Are facts separated from interpretations and assumptions?
4. Did you preserve meaningful uncertainty instead of smoothing it away?
5. Is the next use clear without forcing a decision?
6. Is the length proportional to the mess?
7. Could this brief be handed to Ground Truth, The Quorum, a writer, a researcher, or the user themselves?
