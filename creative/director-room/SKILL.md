---
name: dircreative-director-room
description: Select dynamic narrative, visual-production, and model-continuity perspectives for Studio film-preproduction work.
---

# Adaptive Director Room

## Required Knowledge

- `docs/film-preproduction/director-room-routing.md`
- `docs/film-preproduction/schemas/director-role-harness.yaml`
- `docs/film-preproduction/schemas/director-room.yaml`

These are the terminal routing references. Load deeper craft files only when the
selected perspective needs them.

## Inputs

- routed mode and task
- supplied brief and locked facts
- requested outputs
- active artifact versions, if any

## Outputs

- recommendation first
- zero to three selected perspective judgments
- `no_material_conflict` or one concrete material conflict
- options only when the user asks to choose or a conflict cannot be resolved
- downstream owner and next artifact

## Chat Surface

Fast tasks do not enter Director Room. Return the revised copy, shot, storyboard,
or Prompt directly, with only the useful perspective judgments.

Studio tasks may show `阶段: 导演组判断`, but the requested artifact and
recommendation appear before any process note. Do not expose ten role cards or a
meeting transcript.

## Rules

- Select only `narrative_strategy`, `visual_production`, and
  `model_continuity`; never select more than three.
- Local copy or existing-script revision uses `narrative_strategy`, adding
  `visual_production` only when the edit changes screen execution.
- Local storyboard review uses `visual_production` and `model_continuity` without
  opening Director Room.
- Complete advertising-film development uses all three perspectives.
- Prompt compilation uses `visual_production` and `model_continuity` without a
  Council.
- One controlling agent synthesizes the result. Threads default to zero; nested
  dispatch is forbidden.
- Use the existing router's `collaboration` intent when collaboration is explicit.
  Naming the creative/director groups uses professional perspectives. Asking
  them to work jointly or explicitly requesting subagents permits up to two
  useful, bounded host subagents; explicit new tasks or real Threads use the
  host task capability instead. A group name never proves a worker ran.
- Check the current host tools before dispatch. Give workers disjoint scopes,
  locked facts, acceptance criteria and a concrete return artifact. Preserve the
  current host model settings. Do not create a user task for a subagent request.
- The route is only a plan: `not_dispatched` and an empty `dispatch_receipts` list
  remain until actual host calls supply identifiers and result evidence. Review
  the returned artifacts before adoption. Missing capability is `TOOL_BLOCKED`;
  continue independent work and describe any local perspective pass accurately.
- Negated/quoted/historical mentions do not dispatch. Maintenance and ADCO
  workers do not open this runtime or start nested work. Explicit collaboration
  does not expand a bounded artifact or satisfy a media/delivery gate.
- Do not invent disagreement. When judgments align, record
  `no_material_conflict` and keep `disagreements: []`.
- Record a disagreement only when competing choices have different material
  production consequences.
- Do not force 1/2/3 options when the user asks for direct optimization.
- Do not lock final direction before the owning external gate is resolved.
- Treat v1 fixed-seat artifacts as read-only compatibility inputs. New results
  conform to `director-room.yaml` v2.

## skill_run_receipt

Record mode, route, selected perspectives, Director Room use, conflict status,
downstream output, assumptions, and open questions. Fast fileless work needs no
receipt.
