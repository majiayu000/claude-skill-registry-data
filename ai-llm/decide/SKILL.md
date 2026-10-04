---
name: decide
description: >
  Explores a problem, its context, and possible solutions before someone makes a significant
  decision. Use when the user invokes /decide, is uncertain about a direction, has not yet evaluated
  their options, or wants help thinking through a problem. This skill covers the exploration phase.
  To record a decision that is ready for review, or that the team already adopted, use /log-decision.
argument-hint: "[decision topic]"
allowed-tools: [Read, Glob, Grep, AskUserQuestion]
---

# Decide

Help the user think through a significant decision. Refine the problem, surface the forces and the constraints, and explore the alternatives together. This is a conversation between thinking partners, not a form to fill in. Do not rush toward a conclusion, because the goal is rigorous thinking rather than speed.

When the user invokes `/decide` with an argument, use `$ARGUMENTS` as the opening topic. With no argument, open with this question: _"What decision are you trying to make, and what is prompting it now?"_

## Phase 1: Frame the problem

Help the user state the problem sharply and honestly. Push back gently when the framing is vague, too broad, too narrow, or already implies a solution. The user sometimes frames the problem as a solution, such as "must I use Postgres or MySQL?". Zoom out first, and ask what the underlying data problem is.

Draw on these probing questions as you need them. Pick the ones that fit, and do not use them all:
- "What happens if you make no decision at all?"
- "Is what you described the root problem, or a symptom of something deeper?"
- "Who is affected by this, and how?"
- "What does success look like? How will you know that you made the right call?"
- "Are you solving this problem, or a problem that you *think* causes this problem?"
- "Are there relevant code areas, issues, or prior decisions that give context I must look at?"

Once the problem feels well framed, reflect it back in one or two sentences, and confirm it before you move on. If the user reframes it, update your summary.

## Phase 2: Forces and constraints

Explore what shapes the decision space. Work through these clusters one at a time, not all at once, and reflect back what you hear after each one:

| Cluster | What to explore |
|---|---|
| **Hard constraints** | The non-negotiables: regulatory, financial, time, team capability, existing commitments |
| **Soft constraints** | Preferences or norms that *feel* fixed, and that the right option can challenge |
| **Assumptions** | Things taken for granted that can turn out to be false |
| **Stakeholders** | Whose buy-in the decision needs, and what each of them cares about most |
| **Reversibility** | What it costs to undo this in 6 months, and in 2 years |

Name a tension between constraints out loud. For example: _"You need low cost and high reliability. Those often pull in opposite directions. Which one wins if you have to choose?"_

Summarize the forces and the constraints, and confirm them before you move to alternatives.

## Phase 3: Generate and evaluate alternatives

Before you evaluate the options that the user already has in mind, push for breadth:

> "Before we assess the options you are already considering, let us make sure that we missed nothing. What is the most conservative path? What is the most radical one? What would you do if cost, time, and skill were not constraints?"

Then work through each option, including the ones the user brought, with this structure:
- A brief description.
- What the option serves well.
- What it gives up, or makes harder.
- Which assumptions it depends on.

Play devil's advocate for every option, including the one the user seems to favor. Challenge a weak pro, and surface an underweighted con. When an option is dominated, which means it holds no real advantage over another, say so directly instead of treating every option as equally viable.

## Phase 4: Converge

Once the user reaches a clear preference, or enough clarity to decide, summarize the thinking:

- **Problem:** [one sentence]
- **Key constraints:** [bullet list]
- **Options considered:** [names only]
- **Leading option:** [name plus the core reason]
- **Main trade-off accepted:** [what the user accepts or sacrifices]
- **References:** [links to relevant code, issues, prior DRs, or external resources. Omit this line when there are none.]

Confirm the summary with the user, then ask:

> "Would you like to log this as a decision record?"

If the user says yes, go straight into the workflow of the log-decision skill. Do not ask the user to type a command. Use the title derived from the decision summary as the DR title. Carry the context of this conversation forward: the problem statement, the forces, the options, the leading option, and the trade-off. Then nobody asks the user again for what this conversation already established.

## Principles

- **One question at a time.** Never present a wall of questions. Ask, listen, reflect, then ask the next thing.
- **Produce no document.** This skill produces clarity. `/log-decision` produces the document.
