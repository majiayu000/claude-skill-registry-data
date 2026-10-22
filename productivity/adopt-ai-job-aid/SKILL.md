---
name: adopt-ai-job-aid
description: Builds one card for one AI task with five fixed fields (when to use AI, what to give it, what to check, what never goes in, who to ask), in a format picked by task shape, with its place in the workflow, an owner and a review date. Use for "run adopt-ai-job-aid", "AI job aid", "AI cheat sheet for this task", "quick reference card for using AI", "one-pager for using AI on this task", "AI checklist instead of a course", "people need the answer mid-task", part of the Claude Guide for AI Adoption Pack by Polar Bear.
---

# AI Job Aid
## When To Use
People need the answer in the middle of the task, not a module, and the rules changed last month. Use this to build the one card a person looks at while doing one task with AI, and to decide where it sits so they can reach it without leaving the work. It answers: for this task, when do I use AI, what do I give it, what do I check, what never goes in, and who do I ask?

## When Not To Use
If you need the full check for a type of work, with its passes and stop condition, use AI Output Check: the card carries only its two or three key lines. If you want a collection of prompts with owners and test dates, use Shared Prompt Library. A card holds one task.

## Inputs
- The task: its steps, choices and exceptions, in the words of someone who does it.
- Where the task happens: the system, screen or document people already have open.
- The rule that applies to this task, the never-put-in list, who answers questions, and who owns the process.
If you have none of this, I start from the task described in a few lines and mark the output as a first draft.

## Approach
This is performance support at the moment of need: help that sits inside the work and is used while doing it. It starts with action mapping's job aid check (from the originator's public page), which asks, before any course, whether a card alone would do. The judgement is in what you leave off. The failure this prevents: a twelve-page "AI quick guide" on the intranet that nobody opens mid-task, so the person about to paste a customer email decides from memory.

## Workflow
1. Ask at most three questions: what the person is doing when they need this, what they have open at that moment, and how often the tool or the rules for this task change.
2. Run the job aid check first. A card fits where the task is done rarely, changes often, carries many details, or is costly to get wrong; you confirm which applies. If none does, say so and stop: the person may need practice, or nothing at all.
3. Pick the format by task shape: a checklist for fixed steps in order, a decision table for if-then choices, a one-page flow for branching paths. A task with one real decision in it is a decision table, however many steps surround it.
4. Fill the five fixed fields: when to use AI for it (and when not), what to give it, what to check, what never goes in, who to ask. "What to check" carries two or three lines only. The card carries the one rule for this task, not the policy.
5. Draft the aid with only what is needed during the task: action verbs, one step per line, the common mistake beside the step where it happens. Reasons and background go elsewhere.
6. Decide placement: the exact point in the workflow, reachable without leaving the task. Walk through the task once with the card and note where the person would stop.
7. Set the owner, the review date and the trigger for an early update (the tool or the rules changed).

## Output Format
```markdown
# AI Job Aid
Task: [task] | Role: [role] | Format: [checklist, decision table or flow] | Why a card fits: [rare, changes often, many details, costly to get wrong]
## The five fields
| Field | For this task |
|---|---|
| When to use AI for it | [use it when] / [do not use it when] |
| What to give it | [the source material, the context, what good looks like] |
| What to check | [two or three lines from the output check for this work] |
| What never goes in | [items from the never-put-in list that apply here] |
| Who to ask | [role or channel, for a rule in doubt or a blocked step] |

## The aid
| Step or condition | Action | Watch out for |
|---|---|---|
| [step or "if X"] | [verb-led action] | [the common mistake at this step] |

## Placement
[The exact point in the workflow, the channel, how the person reaches it without leaving the task]
## Upkeep
Owner: [role] | Review date: [date] | Early-update trigger: [the tool changed, the rules changed] | Last checked: [date]
## Decision
[Process owner] signs the content and the placement by [date]. [Rules owner] confirms the "what never goes in" and "who to ask" lines by [date]. A person who does the task tests the card on real work before it is published.
```

## Done When
- The job aid check names which of the four reasons applies, or says a card does not fit.
- The format matches the task shape, and the card fits on one page or one screen.
- All five fields are filled, with a named role under "who to ask", and placement, owner, review date and early-update trigger are set.

## Quality Bar
- Every line starts with an action; no paragraphs of background.
- The common mistake sits beside the step where it happens.
- One task per card. A second task gets a second card.
- No prompt collection and no restated policy on the card.
- A card nobody can reach mid-task has failed, however well it reads.
- Claude drafts the card; the process owner signs it and a person does the task and the check.

## Next
Run adopt-ai-train-the-trainer (AI Train-the-Trainer Kit) to prepare the people who will teach with these materials.

## About the makers
This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
