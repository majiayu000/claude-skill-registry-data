---
name: master-plan
description: Sokka's master plan. Use for multi-step features, migrations, multi-phase or multi-PR programs, stacked PRs, "plan this out", or any work that should be broken into verifiable units before code is written. Produces a written plan where every unit ends in a check, and for a multi-PR program a box-by-box checklist that a check script validates.
---

# Sokka's master plan

Sokka has no bending. He wins with a plan, a map, and a willingness to throw the plan out when the ground changes. A plan is worth writing only if each step can be checked.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

You own the plan, not the code. The plan is a checklist an owner runs box by box and the operator audits from the evidence. The plan is the deliverable. Do not implement.

## Pick the size

1. **One or two files with an obvious approach.** Skip the plan. Say so and stop.
2. **One PR with several steps.** Write a unit plan. Follow [Unit plan](#unit-plan).
3. **Several phases or several PRs.** Write a program plan. Follow [Multi-PR program](#multi-pr-program).

## Unit plan

1. **State the outcome.** One sentence on what the user can do when this is done, and one sentence on what the next maintainer inherits.
2. **Survey the ground.** Run `seismic-sense` over every area the work touches. List the callers, the data shapes, and the tests that exist today. No plan rests on unread code.
3. **Name the data shape.** Write the core types, states, and ownership the work introduces or changes. If there are two plausible designs, run `war-room` before going further.
4. **Cut the work into units.** Each unit is one reviewable change that leaves the system working. For each unit write:
   - **Goal.** What changes, in one line.
   - **Files.** The paths it touches.
   - **Check.** The command, test, or observation that proves it. A check you cannot name means the unit is too vague.
   - **Depends on.** The units that must land first.
5. **Order for proof.** Subtraction first (dead code, stale paths), then scaffolding, then behavior. A failing test lands before the fix it proves. Units with disjoint files can run in parallel. Units that write the same file run one after another.
6. **Mark the risks.** Name the step most likely to fail, how you will know early, and what you will do instead. Name any irreversible step so it waits for the human.
7. **Write it down.** Save the plan as Markdown beside the work (for example `docs/plans/<slug>.md`, or a scratch file for short work). Use `tea-time` for the prose.
8. **Hand it to Appa.** Execution follows `steady-flight`. When a unit's check fails in a way the plan did not predict, stop and revise the plan rather than improvising around it.

```markdown
# <Outcome in a few words>

Outcome: <what the user can do>
Inherits: <what the maintainer gets>
Data shape: <types, states, ownership>

## Units
1. <Goal>
   Files: <paths>
   Check: <command or observation>
   Depends on: <none | unit numbers>

## Risks
- <risk>: <early signal>, <fallback>
```

## Multi-PR program

1. **Settle open questions by prototype before you write.** Run `scouting-flight` for each one. Keep the branch, the SHA, and the screenshots for Appendix A. Ask the operator only about a product or preference call that no run can settle, and give options with your recommendation (Never Block on the Human, Fire in `four-elements`).
2. **Explore in subagents.** Dispatch Toph (`subagent_type: "team-avatar:toph"`) on Toph's model from the avatar-setup sheet, one per area, so the bulk stays out of your context. Pick each dispatch's reasoning effort for the job as `avatar-mode` describes. Each returns file pointers, conventions, test commands, and entry points. No inlined dumps. When you are yourself a subagent, do this exploration yourself, one area after another.
3. **Fill the skeleton.** Copy the skeleton in [references/plan-skeleton.md](references/plan-skeleton.md) into the plan file and fill every placeholder. Keep every heading and every sub-block in the order shown.
   - Unless the operator names a path, write the file under the agent store, `${CLAUDE_CONFIG_DIR:-~/.claude}/orchestrate/<slug>/docs/` on Claude Code or `${CODEX_HOME:-~/.codex}/orchestrate/<slug>/docs/` on Codex.
   - One section per PR. One PR is one change with its own evidence (Sequence Work into Verifiable Units, Fire in `four-elements`).
   - Name the execution skill in **How to read this**. A queue of independent PRs takes `full-patrol`, where each owner drives its PR to merge-ready and the operator clicks every merge. A queue delivered as one linear stack the operator lands takes `shield-wall`. Follow the choice rule in `shield-wall` when the two are close. A standing program takes `kyoshi-command`.
   - The execution skill owns base selection, topology changes, and merge authority. Do not copy its rebase steps into the plan.
4. **Write it clean.** Write under `tea-time`. The body is one document type, a how-to. Appendices hold explanation and reference. Each heading states the task or the finding. No long dashes. No mid-sentence colons.
5. **Run the check script.** From the plugin root, run the shared plan checker on the plan file. From this skill's folder its path is `../../tools/check-plan.mjs`.

   ```sh
   node <plugin root>/tools/check-plan.mjs <plan.md>
   ```

   It prints one line per PR section with its box counts, then `<n> PR sections, <m> problems`, and exits 1 when any problem remains. Fix every line it prints to stderr and rerun until it reports 0 problems (Encode Lessons in Structure, Fire in `four-elements`).
6. **Hand back.** Post the plan path and the script's output, then stop. Execution starts on the operator's explicit go, under the execution skill the plan names.

### Verification rule

Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. That sentence is the verification rule, and every verification block opens with it.

- **Live block.** Mandatory. Ten lanes on Suki's model at the PR head drive the real surface through its driver skill, per `kyoshi-formation`. Each lane is one box with a concrete scenario, the screenshot it saves, and its pass predicate.
- **Regression lane against trunk.** One lane runs the same load-bearing scenario on trunk and head. If trunk does not have the feature, the lane records that fact and gates the behavior the diff adds plus the end state the user waits for. It never invents a trunk result.
- **Perf block.** The gate is dual-sided. Trunk and head must both produce the named metric. If trunk lacks the feature, also isolate the work the diff adds and set an absolute budget for that work plus the end-to-end state the user waits for. Do not claim a ratio between unlike scenarios. The block names the metric, the interleaved probe, the trunk baseline measured first, and the rule with the number that fails.
- **Review gate.** A PR that changes an interaction is review-gated. The operator reviews it in chat with screenshots and a video before merge. A PR that changes no interaction writes `**Review gate.** None. <PR id> is not review-gated.` and no boxes under it.

### Driver skill

Pick the driver for each surface and put the resolved skill path or the exact commands in each live lane's boot recipe. Use the project's own verification skill when it has one (see `vital-signs` to create one). Native mobile uses whatever simulator-driving skill the repo has. A PR that touches two surfaces gets lanes on both. A surface with no driver skill is a risk in Appendix C, and its live block still names how each lane drives it.

## Rules

- A unit without a check is not a unit. Split it or name the check.
- Do not plan past what you have read. Mark unknowns as unknowns and schedule the investigation as its own unit.
- Keep the plan shorter than the change it describes.

## Reply

- **Unit plan.** The plan path, the units in order, and the riskiest step.
- **Program plan.** The plan path, the PR ids with their dependencies and the review-gated set, what the prototypes proved and what stays unproven, and the check script's output.
