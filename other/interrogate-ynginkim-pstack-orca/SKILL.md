---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Adversaries try to break a change or design, and only findings proven by a run survive."
disable-model-invocation: true
---

# Interrogate

> Names in backticks, such as `spawn-worker` and `find-sessions`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here and whether a worker on another agent can be started.

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do not apply fixes.

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree. State the intent with the **in-your-own-words** skill, from the user's message, the commits, and the PR description. Ask with `ask-user` when the intent is unclear.

## Fan out

Run Phase A steps 3 and 4 and Phase B of the **arena** skill (`../arena/SKILL.md`), with four changes.

1. The seats are adversaries in place of runners: at least two, on different models and from different vendors when the computer has them, and more when the change is risky or costly to undo. A request to keep the run small narrows the scope, not the number of vendors. Only the user asking for fewer vendors does.
2. Copy the scope's uncommitted changes into each adversary's checkout.
3. An adversary writes only in its own checkout. It never pushes, and never writes to an outside service.
4. In place of the arena task and rationale, give each adversary the scope, the intent, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own checkout. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

## Verify

Verify each finding per arena Phase F by rerunning its command. Keep a finding when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Skip arena Phases C, D, and E. Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list.

## Clean up

After Verify, remove each adversary's checkout that this run made, with the exact step "Removing a worktree" in `../resolve-capability/references/exact-steps.md`, as written. First copy each repro file that a verified finding's command needs into a `mktemp -d` folder, and point the finding's command at the copy. Remove nothing this run did not make.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and the adversaries that found it, each named by agent, model, and effort. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, the count of dropped findings and why.
- **Cleanup**: the adversary checkouts removed, and any kept with the reason.
