---
name: user-journeys
description: "One obvious path per task, dead ends drawn first."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, research]
    category: web
    related_skills: [web-design, user-research, information-architecture]
    web_designer_stages: [research, ia]
---

# User Journeys and Task Flows Skill

Map the steps a person takes to achieve a goal, so each task has one obvious path before any screen is drawn. This skill covers journey maps and user flows for each key path. It does not cover user research, which supplies the tasks, and it does not cover wireframing, which draws the screens the flows imply. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- Before wireframing, to decide which screens exist and in what order.
- For each key path: sign up, find a product, check out, submit a request, and the equivalents for the site in hand.
- When a journey shows where people get stuck, so the stuck point is designed out before it is built.
- When a flow must show the error path and the exit, not only the happy path.
- When two tasks share screens and the shared order must be settled before wireframing.
- Not after the screens are drawn: flows decide the screens, they do not describe screens already chosen.
- Not for every conceivable path: the top tasks first, one flow per task.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- The top tasks are known from research and intake, written in plain sentences.
- The personas and problem statement are on the record, so flows follow real people and real goals.
- The sitemap is in progress, so the flows can feed it the screens they imply.

## How to Run

1. List the top tasks in plain sentences, one per task.
   - A task names the goal in the visitor's words, not the system's steps.
   - Rank the tasks so the most important flow is drawn first.
2. Draw one flow per task, starting with the shortest path first.
   - The shortest path is the common case; edge cases branch off it, they do not define it.
3. For each flow, draw the happy path, the error path and the exit before any pixel is placed.
   - The happy path is the task done right, step by step.
   - The error path is what happens when a step fails, and how the visitor recovers.
   - The exit is how the visitor leaves the task part-way through, without damage.
4. Check each flow for dead ends, missing states and unnecessary steps, and remove them.
   - A dead end is a step with no onward route.
   - A missing state is a loading, empty or error state the flow never drew.
   - An unnecessary step is one the task does not need.
5. Use the flows to decide which screens exist and in what order, then hand that list to IA and wireframing.
   - Screens shared by two flows are drawn once and used by both.
6. Record the flows and the journey notes in the stage record.
   - Record where each journey shows people getting stuck, and what the flow does about it.
7. Re-check after any fix, and record what changed.
   - A changed flow is walked again end to end before the stage closes.
   - The flows recorded are the ones the sitemap follows, not earlier drafts.

## Quick Reference

- One flow per task; the top tasks are listed in plain sentences.
- Shortest path first: design the shortest path before the alternatives.
- Every flow draws three paths: happy path, error path, exit.
- Checks per flow: dead ends, missing states, unnecessary steps.
- Key paths: sign up, find a product, check out, submit a request — and the equivalents for the site in hand.
- Journey maps show where people get stuck, so the stuck point is designed out.
- Tasks: listed in plain sentences, in the visitor's words.
- Screens: decided by the flows, in the order the flows need.
- Shared screens: drawn once, used by every flow that needs them.
- Stuck points: named on the journey map, with what the flow does about them.
- Result: one obvious path per task, drawn before a pixel is placed.

## Procedure

### 1. What it is

Mapping the steps a person takes to achieve a goal — journey maps showing where they get stuck, plus user flows for each key path (sign up, find a product, check out, submit a request).

### 2. How Hermes applies it

Hermes lists top tasks in plain sentences, draws one flow per task, designs the shortest path first, and checks each flow for dead ends, missing states and unnecessary steps.

### 3. What it returns to the stage

- `research` stage record: `note` carries the journey maps — where people get stuck — and `sources` carries the evidence the journeys rest on.
- `ia` stage record: `flows` carries one flow per top task, each with happy path, error path and exit; `sitemap` carries the screens the flows imply, in the order the flows need.

### 4. Good looks like

Each task has one obvious path; the happy path, the error path and the exit are all drawn before a pixel is placed.

## Pitfalls

- A flow with no error path: the visitor who mistypes, loses connection or meets a validation error has nowhere to go.
- A flow with no exit: the visitor who changes their mind is trapped in the task.
- A dead end in the flow: a step with no onward route, discovered by a visitor instead of on paper.
- Missing states: a loading, empty or error state the flow never drew, so the build invents one under pressure.
- Unnecessary steps kept in the flow: each extra step is a place to abandon the task.
- The longest path designed first: the common case inherits the complexity of the edge case.
- A journey map that never names a stuck point: a map that only describes the happy path teaches nothing.
- Two flows that disagree on a shared screen: the same screen drawn twice, differently, because the flows were never compared.
- A task written in system steps instead of a plain sentence: the flow follows the system, not the visitor's goal.

## Verification

- Every top task has one flow, and each flow has one obvious path.
- The happy path, the error path and the exit are drawn for every flow before any pixel is placed.
- No flow contains a dead end, a missing state or an unnecessary step.
- The screens in the sitemap match the screens the flows imply, in the order the flows need.
- Each journey map names where people get stuck and what the flow does about it.
- Shared screens agree across the flows that use them.
- Each task is written in a plain sentence naming the goal in the visitor's words.
- The shortest path is designed first; edge cases branch off it, they do not define it.
- Shared screens agree across the flows that use them, and each shared screen is drawn once.
- The sitemap follows the flows, in the order the flows need.
- The stage record carries the final flows and journey notes, not earlier drafts.
- The content judger checks that each task path is clear and complete; the responsive judger checks the paths hold at mobile widths. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: research, ia. Returns: `research.note` (journey maps, where people get stuck); `ia.flows` (one flow per top task: happy path, error path, exit); `ia.sitemap` (screens the flows imply, in flow order). Judger boundary: content judger checks task paths are clear and complete; responsive judger checks the paths at mobile widths.
