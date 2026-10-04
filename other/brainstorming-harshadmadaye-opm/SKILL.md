---
name: brainstorming
description: Turns a rough idea into an approved design or written spec through one-question-at-a-time dialogue, scaled to spike, bounded, or architectural work. Use when asked to create a feature, build a component, add functionality, modify behavior, or start a new project, before any code is written.
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by classifying how much process the request needs, then work through your path: understand the context, refine the idea, present a design, and get your human partner's approval.

**Announce at start:** "Using opm:brainstorming to design this before building it."

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have told your human partner what you intend and they have approved it. This applies to EVERY task on EVERY path below. The ceremony scales with the task; the approval gate never does.
</HARD-GATE>

## Three Paths

Before your first question, classify the request and say the classification out loud ("this looks bounded, so I'll present a short design here rather than write a spec") so your human partner can override it:

- **Spike** - a feasibility question ("can we...", "is it possible...", "quick and dirty is fine") whose output is an answer, not code you keep. Present the question and what you will try in 2-3 sentences, get a nod, then find out as cheaply as correctness allows. No design doc, no spec file. Report findings as a recommendation; anything you built stays labeled throwaway.
- **Bounded** - a well-scoped change to code that already exists in this repo: a new flag, a small endpoint, a one-file fix. Understanding the kind of app is not enough; bounded means the flow you are changing is already here to read. If there is no existing flow to change, the task is not bounded. Ask the clarifying questions that matter, present a short design IN CHAT (a few sentences to a few short paragraphs), and STOP. Implementation starts only after your human partner says yes. No spec file, no plan document.
- **Architectural** - new projects, new subsystems, changes that restructure how components fit together or alter interfaces others depend on. Follow the full process: questions, approaches, sectioned design, written spec, then `opm:writing-plans`.

When in doubt between two paths, take the heavier one. The ratchet is one-way: hidden complexity discovered mid-task upgrades the path. Stop, say so, and step up. Nothing downgrades mid-task.

If the architectural work spans multiple phases or more than roughly a week, hand off to `opm:milestone-planning` after the spec instead of straight to `opm:writing-plans`.

## Anti-Pattern: "Too Simple To Need Approval"

Every path ends with your human partner approving your intent before implementation. A todo list, a single-function utility, a config change: the design may be two sentences in chat, but you MUST present it and get approval. "Simple" tasks are where unexamined assumptions cause the most wasted work. What scales with simplicity is the artifact, never the approval.

## Red Flags

| Thought | Reality |
|---------|---------|
| "This is too simple to need a design" | Simple means a short design, not no design. Two sentences in chat, then approval. |
| "I'll call it bounded and skip the spec" | Reaching for a label to skip work IS the doubt. Take the heavier path. |
| "It's bounded and the design is obvious, I'll start while they read it" | The gate is the approval, not the design's length. Present, then stop until you hear yes. |
| "I understand this kind of app, so it's bounded" | Bounded measures the repo, not your familiarity. A new project has no existing flow; it is architectural. |
| "The spike works, so I'll keep the code" | A spike's output is an answer. Keeping the code is a new request; classify it. |
| "It grew, but I'm almost done, no need to re-classify" | Hidden complexity upgrades the path mid-task. Stop and say so. |
| "They approved the spike, so the follow-up change is approved too" | Each task gets its own classification and its own approval. |

## Checklist

Classify first, announce the path, then create a todo for each item on your path and complete them in order.

**Spike:**
1. **Explore project context** - enough to frame the probe
2. **Present question + probe plan** - 2-3 sentences
3. **Get approval** - a nod is enough
4. **Investigate** - as cheaply as correctness allows
5. **Report findings** - a recommendation; label anything built as throwaway

**Bounded:**
1. **Explore project context** - check files, docs, recent commits
2. **Ask clarifying questions** - one at a time, only the ones that matter
3. **Present short design in chat** - approach, files touched, testing
4. **Get approval** - STOP and wait for an explicit yes; presenting the design and starting in the same breath is skipping the gate
5. **Implement** - proceed with the normal development workflow (`opm:tdd-workflow` applies); no plan document

**Architectural:**
1. **Explore project context** - check files, docs, recent commits
2. **Ask clarifying questions** - one at a time; understand purpose, constraints, success criteria
3. **Propose 2-3 approaches** - with trade-offs and your recommendation
4. **Present design** - in sections scaled to their complexity; get approval after each section
5. **Write design doc** - save to `docs/specs/YYYY-MM-DD-<topic>.md` and commit
6. **Spec self-review** - inline check for placeholders, contradictions, ambiguity, scope (see below)
7. **User reviews written spec** - ask the user to review the spec file before proceeding
8. **Transition to implementation** - invoke `opm:writing-plans` (or `opm:milestone-planning` for multi-week scope)

**Terminal states are path-bound.** Architectural: the ONLY skill you invoke after brainstorming is `opm:writing-plans` (or `opm:milestone-planning`), never an implementation skill. Bounded: after approval, implementation proceeds directly through the normal development workflow with no plan document. Spike: the terminal state is a reported recommendation.

## The Process

The subsections below serve the bounded and architectural paths (a spike stops at "present the probe, get a nod"). Sections from **Exploring approaches** onward are architectural-path depth; for bounded work, context plus a few questions plus a short in-chat design is the whole process.

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits).
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems (e.g. "build a platform with chat, file storage, billing, and analytics"), flag this immediately. Do not spend questions refining details of a project that needs to be decomposed first.
- If the project is too large for a single spec, help the user decompose it into sub-projects: what are the independent pieces, how do they relate, what order should they be built? Then brainstorm the first sub-project through the normal design flow. Each sub-project gets its own spec -> plan -> implementation cycle.
- For appropriately-scoped projects, ask questions one at a time to refine the idea.
- Prefer multiple-choice questions when possible; open-ended is fine too.
- **Only one question per message.** If a topic needs more exploration, break it into multiple questions.
- Focus on understanding: purpose, constraints, success criteria.

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs.
- Present options conversationally; lead with your recommended option and explain why.
- YAGNI ruthlessly: remove unnecessary features from every approach and design.

**Presenting the design:**

- Once you believe you understand what you are building, present the design.
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced.
- Ask after each section whether it looks right so far.
- Cover: architecture, components, data flow, error handling, testing.
- Be ready to go back and clarify if something does not make sense.

**Design for isolation and clarity:**

- Break the system into smaller units that each have one clear purpose, communicate through well-defined interfaces, and can be understood and tested independently.
- For each unit you should be able to answer: what does it do, how do you use it, what does it depend on?
- Can someone understand a unit without reading its internals? Can you change the internals without breaking consumers? If not, the boundaries need work.
- Smaller, well-bounded units are also easier for you to work with: you reason better about code you can hold in context at once. A file growing large is often a signal that it does too much.

**Working in existing codebases:**

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work (a file grown too large, unclear boundaries, tangled responsibilities), include targeted improvements in the design, the way a good developer improves code they are working in.
- Do not propose unrelated refactoring. Stay focused on what serves the current goal.

## After the Design (architectural path)

**Documentation:**

- Write the validated design (spec) to `docs/specs/YYYY-MM-DD-<topic>.md`. User preferences for spec location override this default.
- Commit the design document to git.

**Spec Self-Review.** After writing the spec, look at it with fresh eyes:

1. **Placeholder scan:** Any "TBD", "TODO", incomplete sections, or vague requirements? Fix them.
2. **Internal consistency:** Do any sections contradict each other? Does the architecture match the feature descriptions?
3. **Scope check:** Is this focused enough for a single implementation plan, or does it need decomposition (or `opm:milestone-planning`)?
4. **Ambiguity check:** Could any requirement be read two ways? Pick one and make it explicit.

Fix any issues inline. No need to re-review; fix and move on.

**User Review Gate.** After the self-review passes, ask the user to review the written spec:

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Wait for the user's response. If they request changes, make them and re-run the self-review. Only proceed once the user approves.

**Hand-off to planning:**

- Invoke `opm:writing-plans` to create a detailed implementation plan.
- Do NOT invoke any other skill. `opm:writing-plans` is the next step.

<!-- Adapted from obra/superpowers (MIT) -->
