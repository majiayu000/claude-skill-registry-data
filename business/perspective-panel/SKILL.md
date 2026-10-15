---
name: perspective-panel
description: "Looks at a topic, plan, decision, or draft from three to five genuinely different viewpoints (stakeholder roles, disciplines, or critical lenses such as skeptic, customer, regulator, or competitor), gives each viewpoint its strongest case with concrete concerns and questions, then maps where they agree and clash and closes with the decision-relevant takeaways. Use when the user wants balanced viewpoints, a devil's advocate, a pre-mortem, a red-team review, pros and cons from several sides, or wants to stress-test an idea before presenting or deciding."
---

# Perspective Panel

You assemble a small panel of distinct viewpoints and let each one look hard at the user's topic. The point is not to be balanced for its own sake, but to surface the concerns, opportunities, and questions the user would otherwise miss, and then to show clearly where the viewpoints agree, where they clash, and what that means for the decision.

## When to use which panel

Choose the lenses to fit the topic. Use **three to five** viewpoints: fewer misses angles, more becomes noise.

| Topic type | Suggested panel |
|---|---|
| Business decision or plan | Customer, Finance, Operations, Skeptic, Competitor |
| Product or feature idea | User, Engineering, Sales, Support, Skeptic |
| Policy or process change | Affected employee, Manager, Legal/Compliance, Works council or HR, Skeptic |
| Strategy or investment | Board member, Customer, Competitor, Risk officer, Long-term optimist |
| Public communication or draft | Target reader, Critical journalist, Legal, Internal employee |
| Personal decision or career choice | Future self in 5 years, Pragmatist, Risk-averse friend, Ambitious mentor |
| Contested topic or debate | The strongest positions actually held in the debate, each argued in good faith |

The user can name the panel instead ("look at this as our CFO, our biggest customer, and the works council"). Use their panel if they give one.

Every panel includes **at least one critical voice** (Skeptic, Risk officer, Critical journalist, or similar). A panel that only agrees is not doing its job.

## Step 1 — Frame the question

Restate what is being examined in one or two sentences:

- **The subject:** the plan, decision, idea, or draft.
- **The decision or use:** what the user will do with the result (decide, revise, present, prepare).
- **The context that matters:** constraints, deadlines, numbers, and stakeholders the user has shared or that come from uploaded documents or connected sources.

If the subject is too vague to critique ("our strategy"), ask one clarifying question before you start.

## Step 2 — Introduce the panel

List the viewpoints with one line each on what that viewpoint cares about most:

```
Panel
1. [Viewpoint] — cares most about [priority]
2. ...
```

Make the viewpoints genuinely different. Two lenses that would raise the same points (for example "Finance" and "Controller") should be merged and replaced by something new.

## Step 3 — Let each viewpoint speak

For each viewpoint, write a section in this format:

```
### [Viewpoint]
Overall: [supports / supports with conditions / skeptical / opposed] — [one sentence why]

What looks good from here
- [specific strength, tied to the subject]

What worries me
- [specific concern, as concrete as possible: which part, what could happen, how likely, how bad]
- [...]

What I'd ask before agreeing
- [question the user should be ready to answer]

What would change my mind
- [the evidence, change, or safeguard that would win this viewpoint over]
```

Rules:

- **Steelman, don't strawman.** Give each viewpoint the strongest, most intelligent version of its case.
- **Be specific to the subject.** "Costs might be high" is useless; "The rollout needs two FTEs for six months, which the plan doesn't budget for" is useful. If the material lacks the facts, phrase it as a question.
- **Stay in role, but stay factual.** Viewpoints may disagree on values and priorities, never on facts. Do not invent facts, figures, or quotes to strengthen a viewpoint.
- **Keep each section tight:** two or three points per heading.

## Step 4 — Map agreement and conflict

After the panel has spoken, step out of the roles and summarize:

```
## Where the panel agrees
- [point most viewpoints share — usually the safest conclusion]

## Where the panel clashes
| Issue | Side A (who) | Side B (who) | What the clash is really about |
|---|---|---|---|
| [issue] | [position] | [position] | [trade-off, e.g. speed vs. risk, cost vs. quality] |

## Blind spots
- [what none of the viewpoints could judge, and who should be asked]
```

## Step 5 — Close with takeaways

End with what the user can act on:

```
## Takeaways
1. [The biggest risk or open question, and how to address it]
2. [The change to the plan/draft that would win over the most critical viewpoint]
3. [The question to be ready for when presenting or deciding]

## Suggested next step
[one concrete action: get a number, talk to a stakeholder, run a small test, revise a section]
```

Do not pick the winner for the user unless they ask for a recommendation. If they do, give it, label it `[My recommendation]`, and say which viewpoint it favors and why.

## Variants

| Request | Adjustment |
|---|---|
| **Pre-mortem** | Every viewpoint starts from "It's a year later and this failed. Why?" and lists the most likely causes. |
| **Red team** | Only critical viewpoints; each tries to find the weakest point, then you rank the weaknesses by severity. |
| **Quick take** | Three viewpoints, one short paragraph each, then the agreement/clash summary in three bullets. |
| **Debate prep** | Two to three opposing positions, each with its best arguments and its best rebuttal of the others. |
| **Always-on** | If the user asks for this on every answer in the chat, add a compact three-viewpoint "Other angles" section to each answer until they say stop. |

## Combining with other skills

- Before **Presentation Prep** Step 5, run a panel to find the tough questions.
- With **Product Thinking Partner**, use a panel to stress-test the preferred option.
- With **Legal Risk Matrix** or **Operational Risk Register**, turn the panel's concerns into tracked risks.

## Ground rules

- Viewpoints represent roles and lenses, not real named people. Do not put words in the mouth of a real person ("what our CEO Anna would say") unless the user supplies that person's documented positions, and label them as such.
- On contested political, social, or ethical topics, present the positions that are actually held, fairly and in good faith, and do not declare one of them correct.
- Never invent data, studies, quotes, or precedents to support a viewpoint. Use `[Input required]` or phrase it as a question.
- Mark what comes from where: `[From your material]` for facts the user provided, `[Viewpoint]` for in-role arguments, and `[My recommendation]` for your own judgment.
