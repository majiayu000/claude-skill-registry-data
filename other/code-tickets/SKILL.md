---
name: code-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
disable-model-invocation: true
---

# Code Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

The issue tracker and triage label vocabulary should have been provided to you. If not, read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

Then pick the entry point. **Split a spec into Phases only at a boundary where real use could change or cancel what follows** ([`planning.md`](../../../docs/agents/planning.md#phases)). Each Phase but the last ends at a **Phase gate**, the developer's go, reshape or drop ticket, which this skill writes and closes; closing the spec ends the last.

- **A Phase gate** (a `ready-for-human` issue with a `## Decision` section): go to [From a Phase gate](#from-a-phase-gate).
- **A phased spec** (one with a `## Phases` section): steps 2–7 for its next Phase, unless an earlier Phase is `ticketed` but not `done`: its gate is still open, so point the developer to it and stop.
- **Anything else is unphased**: steps 2–7, proposing Phases in step 3 if the spec has a boundary.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching, and the design.md principles that apply.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

- **Phased spec**: draft only the next `planned` Phase's tickets, plus its Phase gate unless it is the last Phase.
- **Unphased spec**: if the boundary criterion in [`planning.md`](../../../docs/agents/planning.md#phases) applies, propose Phases, naming Phase 1's stand-ins and outlining the later ones as provisional, and draft only Phase 1's tickets and its gate. Otherwise draft every ticket.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice changes at most ~10 files, counted by grepping the names it changes ([ticket size](../../../docs/agents/planning.md#ticket-size))
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket one **kind**:

- **Agent** (`ready-for-agent`): work a runner step can do.
- **Interactive** (`ready-for-interactive`): agent work a step can't do: a tier-3 action by the [tier list](../../../docs/targets-and-gates.md#which-tier-an-action-is-in), or a write outside the issue workspace, such as to `~/.claude`, by the [step write rule](../../../docs/claude-code-guardrails.md#the-hooks-and-the-project-agent). Group it by where the chain needs it, usually one per spec, and make each downstream ticket blocked by it.
- **Human** (`ready-for-human`): work only the developer can do.

Split a slice that needs two kinds into one ticket per kind; when one part needs another's output, that part's ticket blocks the other.

Give each `ready-for-agent` and `ready-for-interactive` ticket its **model fit**: one of the pairs in [`planning.md`](../../../docs/agents/planning.md#model-fit) and a one-line reason.

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Review the drafts for Halt risks

With 6 or more tickets to publish, a Phase gate counted, draft each ticket's full body in the local-ticket template to `<scratchpad>/tickets/<NN>-<slug>.md`, whatever the tracker. Then read [`.claude/skills/review-code-tickets/SKILL.md`](../review-code-tickets/SKILL.md) and follow it on that folder; it is user-invoked, so the Skill tool can't reach it. Act on its report once, before the developer sees the breakdown:

- **Fixes**: make each, as you judge best, true to the spec.
- **Interactive splits**: split that part into a `ready-for-interactive` ticket, blocking the work that needs it.
- **Spec gaps**: hold them for step 5's round.

With fewer than 6 tickets, skip this step; the developer can run `/review-code-tickets` on the published tickets.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **Kind**: agent, interactive or human; for an agent or interactive ticket, its model fit
- **What it delivers**: the end-to-end behaviour this ticket makes work
- **Files**: the count from the slice rules' grep, with the names; split a ticket over ~10 before showing it

When proposing Phases, add a **Phases** line before the list: each Phase's user story numbers, Phase 1's stand-ins, and which tickets are its gate's blockers.

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Put any spec gaps from step 4 after the list, as one round in the [`grilling`](../grilling/SKILL.md) format, then apply the answers. When an answer settles what the spec should have said, add a line saying so to the spec's body.

Iterate until the user approves the breakdown. Step 4's review runs once: carry the developer's changes into the drafts, where there are drafts, and publish them as they stand.

### 6. Publish the tickets to the configured tracker

Publish the approved tickets. **How** depends on the tracker in `docs/agents/issue-tracker.md`; the tickets are the same either way, only the shape of the blocking edges changes:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first). Each file's "Blocked by" lists the numbers/titles it depends on. Use the per-ticket file template below: one ticket per file, never a single combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. If the source was an existing issue, make each ticket its sub-issue (tracker doc's operation). Apply each ticket's kind as its triage label, `ready-for-agent`, `ready-for-interactive` or `ready-for-human`, unless instructed otherwise.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.

When the work has Phases:

- On an unphased spec, write the approved `## Phases` section into the spec before publishing Phase 1.
- Publish the Phase gate after the Phase's tickets, blocked by every one of them, using the gate template below.
- Add the Phase's tickets and gate as sub-issues after the earlier Phases' ones, so the runner's order follows the Phases.
- Set the Phase's status in `## Phases` to `ticketed`.

Do NOT close or modify any parent issue, except its `## Phases` section and the lines step 5 adds.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

**Status:** ready-for-agent, ready-for-interactive or ready-for-human

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

## New dependencies

- <name>

## Model fit

<Model> <effort>
<one-line reason>

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when blockers were set as native edges.

## New dependencies

- <name>

## Model fit

<Model> <effort>
<one-line reason>

</issue-template>

<phase-gate-template>

Title: `Phase gate: Phase <N> tested (<what real use tests>)`

## Parent

A reference to the spec.

## What to do

This is the developer's ticket; the runner never launches it, so everything after it waits. Test what Phase <N> built, record what you learn, tick one box under Decision, then run `/code-tickets` on this issue, which closes it, and rerun the runner. Put findings and any reshape details in comments here.

Phase <N>: a reference to each of its tickets.

- [ ] A test to run in real work
- [ ] Note: a piece of data to record, and what it decides

## Decision

- [ ] Go: ticket Phase <N+1> as outlined
- [ ] Reshape: change the later Phases as my comments say, then ticket Phase <N+1>
- [ ] Drop the rest

</phase-gate-template>

A Phase gate is labelled `ready-for-human` and has no `## Model fit`.

In either form, `## Model fit` is the last section of a `ready-for-agent` or `ready-for-interactive` ticket: a pair line, then a one-line reason. A `ready-for-human` ticket has none.

In either form, `## New dependencies` lists only the packages the ticket adds, one `- <name>` line each; leave the section out when it adds none. Never relist a package that's already a dependency, and a version change to an existing package and the packages a new one depends on need no line.

A `ready-for-human` ticket's body names what the developer runs: the skill (e.g. `/inbox`) or the numbered steps.

In either form, avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

### 7. Read back the model fit

Print the published tickets as one flat list in completion order, `#n Title: <Model> <effort> (reason)`, the read-back of each ticket's `## Model fit` section. Done when every `ready-for-agent` and `ready-for-interactive` ticket appears with the pair its section names.

## From a Phase gate

Read the gate's body, every comment on it, and the spec's `## Phases` section.

- **No box ticked, or more than one**: ask the developer which decision they meant, and stop.
- **Go**: set the gated Phase's status to `done`, then run steps 2–7 for the next Phase.
- **Reshape**: edit the later Phases' outlines in `## Phases` as the comments say, then do as for Go.
- **Drop the rest**: set the gated Phase to `done` and every remaining Phase to `dropped`, linking this gate, and publish nothing.

Every branch closes the gate with a comment: the new tickets' links for Go and Reshape, the dropped Phases for Drop the rest.
