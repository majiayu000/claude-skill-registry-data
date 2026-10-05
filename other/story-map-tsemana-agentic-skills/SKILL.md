---
name: story-map
description: Use when facilitating a user story mapping session for a product, feature area, single activity, new persona, or cross-cutting feature. Orchestrates a Three Amigos agent team (Product Owner, Developer, QA) that debates via inter-agent messaging to produce a story map backbone, prioritised release slices, a walking skeleton, agreed Definitions of Done, and BDD readiness verdicts. Successive sessions incrementally build a single master story map file per product. Requires Claude Code agent teams (TeamCreate, SendMessage, named Agent teammates); not portable to runtimes without these tools.
version: 1.0.0
author: Tony Semana
license: MIT
metadata:
  runtime: claude-code
  tags: [story-mapping, agile, three-amigos, bdd, product-discovery, agent-teams]
  related_skills: []
---

# Story Mapping with an Agent Team

## Overview

This skill makes the agent the **Facilitator and Team Lead** of a story mapping session run by an agent team. The facilitator creates a team of three role agents — Product Owner, Developer, and QA Tester — who build and debate the map by messaging each other directly (a Three Amigos session). The facilitator never generates story content itself: it orchestrates, checkpoints with the user, synthesises the team's output, and writes the results to a single master map file per product.

Sessions are additive. The first session establishes the backbone; follow-up sessions go deep on one activity, add a persona's swim lane, or map a cross-cutting feature — each updating only its own scope in the master map.

Outputs per session: a validated backbone, prioritised release slices with outcome-based goals, a walking skeleton, Definitions of Done agreed between PO and Dev, acceptance criteria from QA, a risk and gap register, and BDD readiness verdicts per story.

## Requirements

This skill is built on **Claude Code agent teams** and requires these tools:

- `TeamCreate` / `TeamDelete` — create and clean up the session team
- `Agent` with `name` and `team_name` — spawn the PO, Dev, and QA teammates
- `SendMessage` — inter-agent debate and shutdown requests
- `Read`, `Write`, `Glob` — master map discovery and persistence

It will not run on agent runtimes that lack inter-agent messaging and named, addressable teammates.

## When to Use

- Starting discovery on a new product and needing a full-journey story map
- Mapping one feature area of a large product in depth
- Going deep on a single backbone activity after a product-level session
- Adding a new persona's journey to an existing map
- Scoping a cross-cutting feature that touches multiple activities
- Preparing stories for BDD / Example Mapping with readiness verdicts

Do not use for single-story refinement, sprint planning, or generating a backlog without user participation — the session checkpoints require a human in the loop.

## Session Types

| Type | Precondition | Output shape |
|---|---|---|
| Product (full) | First session for a product | Wide backbone (6–10+ activities), shallow stories, session sequence plan |
| Product (feature-scoped) | First session, product too large for one map | Narrower backbone (4–7 activities), deeper stories |
| Activity | Backbone exists | Deep stories for one activity |
| Persona | Backbone exists | New swim lane, divergence stories, backbone gaps |
| Feature | Backbone exists | Stories attached across affected activities |

## Reference Files

Load these on demand at the step that needs them — do not preload:

- `references/phase1-po-prompts.md` — the five Product Owner Phase 1 prompt variants (Product full, Product feature-scoped, Activity, Persona, Feature)
- `references/phase2-debate-prompts.md` — Developer and QA teammate prompts, plus the PO debate kick-off messages
- `references/master-map-format.md` — the master map markdown template and the update rules for additive sessions

## Procedure

You are the Facilitator and Team Lead. You create and manage the agent team, assign tasks, synthesise results, checkpoint with the user, and write to the master map. You do NOT generate story content — the team does.

### Step 0 — Discover existing map

Before asking the user anything, check whether a master map file already exists. Look for files matching `story-maps/*.md` in the current project directory using the Glob tool.

**If map files exist:**
- Present the list: "I found existing story maps: [list]. Are we continuing one of these, or starting a new product?"
- If continuing: load the file with the Read tool. Note which activities are Complete vs Pending.
- Summarise the current state to the user before proceeding.

**If no map files exist:** proceed to Step 1 with session type defaulting to `product`.

### Step 1 — Gather session context

Ask the user all of the following in one message. Wait for their responses.

1. **Project/product name** — what are we mapping?
2. **Session type** — Product (full), Product (feature-scoped), Activity, Persona, or Feature (see Session Types above)
3. **Primary persona(s)** — who is the user? (name, role, goal). For Product (full) sessions: list ALL known personas, even if only one is primary for this session.
4. **Mapping type** — As-Is (existing product), To-Be (future state), or Both?
5. **Session scope:**
   - For Product (full): confirm "whole product" or name the boundaries if the product has natural divisions
   - For Product (feature-scoped): name the feature area (e.g. "find/view products", "checkout", "account management")
   - For Activity/Persona/Feature: which activity, persona, or feature?
6. **Known constraints** — anything the team must respect (tech, time, regulatory)?
7. **BDD output needed?** — should the session end with a BDD Readiness assessment? (yes/no)

Store all answers as **SESSION CONTEXT**. Store the session type as **SESSION TYPE**.

### Step 2 — Create the team

Use the TeamCreate tool:

```
TeamCreate:
  team_name: "story-map-{product-name}"
  description: "Story mapping session for {product-name} — {session type} session"
```

This creates the shared task list that all teammates will coordinate through.

### Step 3 — Phase 1: Build the backbone (PO agent)

Read `references/phase1-po-prompts.md` and select the prompt variant matching the SESSION TYPE. Fill in the `{SESSION_CONTEXT}` placeholder (and, for additive sessions, the existing backbone/stories/personas placeholders from the loaded master map).

Spawn the PO teammate:

```
Agent:
  name: "product-owner"
  team_name: "story-map-{product-name}"
  subagent_type: "general-purpose"
  prompt: [selected PO Phase 1 prompt with placeholders filled]
```

### Backbone checkpoint

Once the PO agent completes Phase 1, present the backbone to the user.

- **Product (full)**: all personas identified, Big Goal, all Activities with Tasks. Emphasise the WIDTH: "Does this cover the full user journey? Are any major feature areas missing?" Also present the suggested session sequence for follow-up Activity sessions.
- **Product (feature-scoped)**: Big Goal for the feature area, all Activities with Tasks within scope.
- **Activity**: the task list and stories for the scoped activity.
- **Persona**: the persona definition and backbone gaps.
- **Feature**: the affected activities/tasks and backbone gaps.

Ask: **"Does this accurately represent the scope? Should anything change before the team debates it?"**

For Product (full) sessions specifically: remind the user that this backbone is intentionally shallow. The Three Amigos debate in Phase 2 will focus on release slicing and priority validation — not deep story exploration. Deep stories come in follow-up Activity sessions.

Wait for confirmation. Apply any changes. The backbone is now frozen for this session.

### Step 4 — Phase 2: Three Amigos debate (Dev + QA join)

This is the core of the session. Read `references/phase2-debate-prompts.md` for the Developer prompt, the QA prompt, and the PO debate kick-off message.

**Debate scope varies by session type:**

- **Product (full)**: the debate focuses on PRIORITISATION and RELEASE SLICING, not deep story DoDs. Dev challenges feasibility of the backbone structure and release goals. QA challenges testability of the release slices and identifies cross-cutting concerns. PO defends priorities. The output is a validated backbone with agreed release goals and a session plan — NOT stories with DoDs.
- **Product (feature-scoped) / Activity / Persona / Feature**: full debate — stories, DoDs, acceptance criteria, BDD readiness.

Spawn both teammates with their prompts (placeholders filled with SESSION CONTEXT, the approved backbone, and the PO's Phase 1 output):

```
Agent:
  name: "developer"
  team_name: "story-map-{product-name}"
  subagent_type: "general-purpose"
  prompt: [Developer prompt]

Agent:
  name: "qa-tester"
  team_name: "story-map-{product-name}"
  subagent_type: "general-purpose"
  prompt: [QA prompt]
```

Then send the PO the debate kick-off message (use the variant matching the session type) via SendMessage.

### Step 5 — Monitor the debate

While the team debates, you monitor. Messages from teammates are delivered to you automatically.

- Let the agents work. Do not intervene unless they get stuck or go off-scope.
- If the debate stalls (agents repeat the same point without resolution), intervene: escalate the specific disagreement to the user for a decision.
- If agents go beyond the agreed scope, message them to refocus.
- Track which stories have reached consensus (PO + Dev + QA all agree).

The debate is complete when all three agents have marked their debate tasks as completed.

### Step 6 — Synthesise and write to master map

Collect the final outputs from all three agents and synthesise into the master map.

**Conflict resolution rule**: if PO and Dev/QA still disagree on a story after their debate, apply the confidence test:

- [ ] Can a real user accomplish the release goal using only what is in this slice?
- [ ] Does the slice have a clear, testable outcome?
- [ ] Is every story necessary (no gold-plating)?
- [ ] Is everything necessary included (no hidden dependencies)?

If the confidence test fails, move the story to Release 2 and note the reason. Surface any unresolved items to the user.

Write to `story-maps/{product-name}.md` using the template in `references/master-map-format.md`. Product sessions create the file; Activity/Persona/Feature sessions load, update relevant sections, and write back — following the **update rules for additive sessions** in that same reference file.

### Step 7 — Shutdown and handoff

Send shutdown requests to all three teammates:

```
SendMessage:
  target_agent_id: "product-owner" | "developer" | "qa-tester"
  type: "shutdown_request"
  message: "Session complete. Shutting down."
```

Then use TeamDelete to clean up the team.

**Present to the user:**

1. **Session summary** — session type, scope, stories produced, debates resolved, readiness verdicts
2. **What remains unmapped** — activities still Pending in the backbone status
3. **Suggested next session** — based on priorities, recommend the next session type and scope

**Offer next steps:**

- **Continue mapping** — start another session (returns to Step 1 with map loaded)
- **Export to BDD pipeline** — hand the "Ready for Example Mapping" stories to an Example Mapping session (use a companion `example-map` skill if one is installed; otherwise share the BDD Readiness table with the team)
- **Review the full map** — display the complete master map

## Facilitation Rules (non-negotiable)

- **Backbone before debate.** Dev and QA never join until the backbone checkpoint is passed. No exceptions.
- **User actions only on the backbone.** Activities and Tasks describe what the user does, not what the system does.
- **Outcome-based release goals.** A feature list or a date is not a release goal. Name what the user can accomplish.
- **Walking Skeleton ≠ MVP.** Skeleton = architecture validated. MVP = minimum user value. Never conflate.
- **Stories not on the map are not ready for BDD.** No Activity + Task home = return to PO.
- **The backbone is frozen after the checkpoint.** If debate surfaces backbone changes, escalate to the user.
- **Additive sessions do not overwrite previous work.** Only touch sections within the current session's scope.
- **One master map file per product.** All sessions read from and write to the same file.
- **The debate must converge.** If agents repeat the same point three times without resolution, the Facilitator escalates to the user. Do not let agents loop.
- **Definition of Done requires Dev + PO agreement.** QA validates testability but does not define Done.
- **BDD Readiness requires all three.** A story is only READY when PO defines value, Dev defines Done, and QA confirms testability.

## Common Pitfalls

- **Facilitator writes story content.** The facilitator orchestrates and synthesises only; if you catch yourself inventing stories, stop and route the work to the PO agent.
- **Dev/QA spawned before the backbone checkpoint.** The debate then anchors on an unvalidated backbone and the user's corrections arrive too late.
- **System actions creep onto the backbone.** "Display product catalogue" is a system action; "Browse products" is the user action. Rewrite on sight.
- **Deep-diving stories in a Product (full) session.** The wide map loses its purpose; depth belongs in follow-up Activity sessions.
- **Letting the debate loop.** Two agents restating positions is not progress — apply the three-repeats escalation rule.
- **Overwriting prior sessions' sections** when updating the master map. Follow the additive update rules in `references/master-map-format.md`.
- **Conflating Walking Skeleton with MVP** in release planning discussions.
- **Date- or feature-list release goals** slipping through the synthesis step unchallenged.

## Verification Checklist

Before closing a session, confirm:

- [ ] Backbone checkpoint was approved by the user before Phase 2 began
- [ ] All three agents marked their debate tasks completed
- [ ] Every Release 1 story has an Activity + Task home, a PO+Dev agreed DoD, and a QA testability verdict
- [ ] Confidence test applied to each release slice; failures moved to Release 2 with reasons
- [ ] Master map updated additively — sessions log appended, out-of-scope sections untouched
- [ ] Unresolved disagreements surfaced to the user, not silently dropped
- [ ] Team shut down (`shutdown_request` to all three) and deleted via TeamDelete
- [ ] Session summary, unmapped activities, and a next-session recommendation presented to the user
