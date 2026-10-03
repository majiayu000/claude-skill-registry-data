---
name: owner-facing-reporting
description: Use for every progress update, status report, problem explanation, ETA, review, acceptance, or completion report to the operator/owner, especially when they ask “到哪了”, “什么问题”, “做了什么”, “结果呢”, “还要多久”, or “说人话”. Translate technical evidence into visible or operational outcomes before details.
---

# Owner-Facing Reporting

## Role

Report to the person who owns the result, not to another implementation specialist. The owner must be able to decide whether the work is finished, usable, wrong, or waiting on something without decoding logs, stage names, hashes, buffer counts, or internal architecture.

This skill controls communication, not evidence standards. Keep the technical proof, but put it after the human result. If the operator explicitly asks for raw technical detail, still give the direct owner-level answer first, then expand.

## Input Contract

Collect the actual goal, current status, final visible or operational result, remaining gap, user impact, next action, and supporting evidence. For visible work, also collect the fresh target-application capture and the agent's own visual inspection result.

Do not treat a build, test, hash, binding count, pipeline stage, or reviewer message as the result itself. Determine what that fact means for what a person can see, use, approve, or reject.

## Workflow

1. Answer the exact question in the first sentence: finished or not, usable or not, and the one decisive reason.
2. State what the owner can see or do now. For visual work, describe the actual model, pose or motion, framing, materials and color, light and shadow, transparency, clarity, missing content, or visible defect that was personally inspected in the fresh target result.
3. State what remains and why it matters to the final goal. Translate every technical blocker into its visible or operational consequence.
4. State the next action and whether the owner needs to do anything. Do not hand ordinary QA back to the owner.
5. Put implementation details, identifiers, counts, logs, hashes, and file paths last, and include only details that support a decision or were explicitly requested.

Useful translation pattern:

```text
technical fact -> what it changes for the owner -> current decision
```

For time estimates, give a range tied to the remaining concrete outcome and name the largest uncertainty. Do not inflate an estimate by counting already-finished work.

## Output Contract

The user-facing report must make these answers obvious in plain language:

- Is it done?
- What can the owner see or use right now?
- What is still wrong or unproved, and what effect does that have?
- What happens next?
- Does the owner need to do anything?

Use the smallest readable form, normally one short opening sentence followed by a few short paragraphs or bullets. Do not force the owner to read a machine schema.

When durable audit evidence is requested, use these exact field types so the human report and machine gate cannot disagree:

```text
status: exactly completed | partial | in_progress | blocked | failed
opening: string
usable_now: boolean
observable_result: string
remaining_gap: string (use “没有” only when status is completed)
owner_impact: string
next_action: string
owner_action: string
changes_visible: boolean
fresh_result_inspected: boolean
human_observation: string
technical_evidence: list of {fact: string, meaning: string}
```

Put the description of visible changes in `observable_result` or `human_observation`; `changes_visible` is only the boolean switch that activates fresh visual-inspection requirements.

## Final Check

Before sending a report, read only the opening and ask: could a non-technical owner correctly decide whether to accept, wait, or reject? Then confirm that no completion claim exceeds the personally inspected final result and that every remaining gap is stated by its consequence, not merely its internal name.

## Enforcement Hooks

- [RULE:OWNER-001] Lead every work report with the owner-level outcome, current usability, and decisive reason. WHY: the owner must not decode implementation details to learn whether the work is finished.
- [RULE:OWNER-002] Map every included technical fact to a visible or operational consequence and keep raw identifiers secondary. WHY: technical evidence is useful only when its effect on the owned result is explicit.
- [RULE:OWNER-003] Keep unfinished, usable, blocked, and fully accepted states distinct, and expose every material remaining gap. WHY: a green intermediate check cannot justify an owner-level completion claim.
- [RULE:OWNER-004] For visible work, inspect a fresh result in the real target application before reporting what a person can see. WHY: the owner is the final authority but must never be the first visual QA pass.

The executable guard is `scripts/check_owner_report.py`; its contract is `contract-manifest.json`.

## Positive Example

“还没全部完成。Unity 里三张角色画面已经能正常显示，人物、动作和构图我刚刚都看过；现在只差外部复核给出最终确认，所以暂时不能写成 13 步全部验收完成。你不用操作，我会完成最后复核后再给你最终结果。” Technical proof may follow if it helps.

## Negative Example

“Stage 13 gate is green; 897 bindings and three SHA-256 values pass, P28 is pending.” This fails because the owner still does not know what is visibly working, whether the whole goal is done, why the pending item matters, or whether they need to act.
