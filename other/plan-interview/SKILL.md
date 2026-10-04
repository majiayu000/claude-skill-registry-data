---
name: plan-interview
description: Interview a user with a vague or stalled goal, draft concrete next actions for approval, and create the approved project in Todoist when an authenticated integration is available. Use when the user wants to turn an unclear goal into a practical Todoist project or repair a project whose tasks are not getting started.
---

# Plan Interview

Turn a vague goal into a Todoist project the user can actually start on.

This skill treats procrastination as a task-initiation problem: people often stall when the next physical action is ambiguous. Remove that ambiguity through a short interview, then write the approved result into Todoist.

## Safety and tool use

Use the live Todoist MCP tool schemas; do not assume tool names or field names. Inspect what is actually available before planning a write.

Never create, edit, reschedule, label, or delete anything until the user has approved the displayed draft and the exact scope of the write.

If Todoist is unavailable, still complete the interview and provide a clean, copy-pasteable task plan in chat. Offer connection setup afterward.

If task durations are unsupported by the user's plan or the available tool, include estimates in each task description instead.

## Operating principles

1. **Next physical action, not category.** Every task names a concrete verb and object the user could begin within 60 seconds of reading it. "Write report" is a category. "Draft three bullets for the methods section" is an action. If a task prompts "…but how do I start that?", it is not decomposed enough.
2. **Right-sized chunks.** Aim for 15–45 minutes of focused work per task. Split bigger tasks. Merge smaller tasks unless one is a deliberate ignition step.
3. **If–then intentions.** Each task description carries one: `When <trigger>, I will <action>.` Specifying the trigger in advance makes the task easier to start.
4. **Name the obstacle.** Ask what has actually stopped the user before and pre-decide a response. Do not stop at picturing the completed goal.
5. **Trivially easy start.** Make the first task in every project almost insultingly small: open the file, create the document, or find the syllabus.
6. **Deadlines, not schedules.** Set deadline fields for genuine constraints only. Do not set due dates unless the user explicitly asks; they schedule their own days. Put effort estimates where the user can time-block from them.
7. **Plan the next milestone, not the whole thing.** The first pass produces 5–12 actions covering roughly the next week or the next milestone. A 25-task project recreates the overwhelm. Expand later during review.

## Phase 1 — Interview

Use information the user has already provided. Ask only the next one or two questions needed to produce a first draft. Stop interviewing once you know the outcome, real deadline, current state, likely obstacle, and available time. Usually three to seven questions total are enough.

A long interview becomes the next thing to procrastinate. Bias toward drafting early: a concrete draft the user corrects beats more questions.

Cover these topics in roughly this priority:

- **Outcome:** What does "done" look like, concretely enough to photograph? If two unrelated outcomes are tangled together, split them into separate projects.
- **Deadline:** Is there a hard date? Are there intermediate dates imposed by someone else?
- **Current state:** What already exists—notes, draft, repository, or reading? What is genuinely unknown versus merely unstarted? Unknowns become research tasks; unstarted things become execution tasks. Do not conflate them.
- **Available time:** How much time is realistically available per week?
- **Obstacle:** Ask, "What's stopped you on things like this before?" Push past "I get lazy" to the mechanism: opening the laptop and landing on YouTube, not knowing which paper to read first, or dreading a message. Then agree on an if–then response.

Do not silently pad estimates. State the raw estimate, then ask: "Should we add a 30–50% buffer? Most plans run over." Let the user choose.

Full WOOP—Wish, Outcome, Obstacle, Plan—is optional. Reserve it for goals the user is clearly avoiding or has stalled on before. It is too much ceremony for ordinary planning. The obstacle question is useful almost every time.

Use domain probes only when relevant:

- **Study:** Is the goal an exam or comprehension? What is the assessment format? Build in spaced revisits by re-encountering material days apart rather than in one block.
- **Work:** Who blocks or is blocked by this work? Is there a review or approval step? Turn those into handoff tasks with buffer before the deadline.
- **Personal:** Is this a one-off or a habit? Habits get a recurring task and a fixed trigger, not a project.

Before drafting, ask what the user is most likely to avoid. Give that task extra decomposition and the smallest possible first step.

## Phase 2 — Draft and approve

Do not write to Todoist yet. Show in chat:

- Project name.
- Sections or phases in order.
- Tasks under each section, with effort estimates and deadlines where they apply.
- The if–then plans to attach.
- The ignition task, called out explicitly.

Ask: "Does any of this still feel vague or too big?" Re-break whatever the user flags. Repeat until nothing is flagged; this iteration is the point of the skill.

Then get explicit authorization:

> Should I create this Todoist project exactly as shown? I'll create the project, these sections, these labels if needed, and these tasks—nothing else.

Only write after a clear yes.

## Phase 3 — Write to Todoist

Check the live tool schemas, then create in this order: project, sections, labels, tasks.

### Structure

- **Project:** Use one project per goal. Put obstacles and their if–then plans in the project description so the project page itself is the reminder.
- **Sections:** Use one section per phase, in execution order. Typical shapes are Research → Draft → Revise → Submit or Understand → Practice → Test.
- **Tasks:** Create 5–12 next actions for the first pass.

### Per task

- **Content:** State the next physical action. Put the verb first and keep it concise.
- **Description:** Include the if–then intention and specifics such as the file, chapter, or person.
- **Effort estimate:** Include one on every task—in the duration field when supported, otherwise in the description.
- **Deadline:** Use only for real constraints. Leave it blank otherwise.
- **Priority:** Reserve the top level for work that is genuinely urgent and important. If everything is top priority, nothing is.
- **Ordering:** Sequence tasks top-to-bottom in doing order. A task that cannot start yet should not sit at the top looking like a reproach.

### Labels

Keep the label set small:

- `next`: Exactly one task per project. When someone is frozen, one visible move beats three options. Across several projects the user still has a small menu; within a project, there is one thing to do.
- `deep` / `shallow`: Distinguish work that needs real focus from work that is doable while tired, so the user can match task to energy.
- `blocked`: The task is waiting on someone else.

## Phase 4 — Close the loop

In two or three sentences, name the single task to start with, describe what its first two minutes look like, and identify the if–then plan most likely to be needed. Then offer: "Want me to set a weekly review to see what stalled and re-break it?"

## Review mode

When the user returns and things have stalled, do not re-interview from scratch:

1. Pull the current project state and what has actually been completed.
2. For anything untouched across two reviews, assume the task is too vague or too big rather than assuming the user is lazy. Say so and re-break it into a smaller, more concrete task with a new ignition step.
3. Ask what specifically happened when the user sat down to it. The answer usually reveals a missing sub-step or unnamed obstacle. Add it.
4. Extend the plan to the next milestone if the current one is done.

## Tone

Be warm and matter-of-fact. Never moralize about procrastination or productivity. The user knows they have been stuck, and being told so can itself become a reason to avoid the list. Treat a stalled task as a bug in the plan, which is usually what it is.
