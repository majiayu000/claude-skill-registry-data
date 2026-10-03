---
name: game-roadmap
description: Use only for video game projects; sequence prototype, vertical slice, demo, store page, festival, launch, and post-launch milestones
type: planning
version: v0.4
required_conventions: [alignment-page]
context_intake: artifact_only
visual_tier: visual
---

# Game Roadmap

## Alignment-YAML Routing

While an alignment page is in `review`, the only next action is section-feedback YAML or final compiled YAML from the bottom compile controls. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

Invoke as `$game-roadmap`.

Turn validated game research into production milestones.

## Output

Write or update `tasks/roadmap.md` with prototype, vertical slice, demo, store page, festival, launch, and post-launch phases.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/game-roadmap-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Next-Step Routing

After writing or updating `tasks/roadmap.md`:

- If the first milestone needs a concrete execution plan, check `.agents/project.json` for `agent-work-admin`; recommend `$plan-phase <first milestone>` when enabled, or `npx skillpacks install agent-work-admin` from the project shell when it is not enabled.
- If `tasks/todo.md` already contains executable work for the first milestone, check `.agents/project.json` for `exec-loop`; state that the approved task artifact is ready for an execution-loop runner; if runner tooling is missing, recommend installing `exec-loop` with the project package manager.
- If the roadmap is blocked by missing game research or validation evidence, recommend the specific missing game skill from the same pack, such as `$game-core-loop`, `$game-prototype-test`, or `$game-store-page-test`.
- If no project execution work remains, state that no follow-up command is recommended.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
