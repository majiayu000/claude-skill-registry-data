---
name: eval-driven-development
description: Use to design the evals for a build before you build it, right after the Goal and Constraint Brief, and again to run them in the Evaluate phase. Runs a short interview to name the outcome the eval must prove, source an eval set from real failures, write outcome-graded pass/fail tasks with negative and distractor cases, choose graders (rules, LLM-as-judge, or human), set the reliability bar (pass@k versus pass^k), and wire the suite into the Learn-phase reward signal, then produces a one-page Eval Plan. Use when the user asks to define or write evals, decide how to measure or grade a model or agent, set a pass rate or reliability bar, prove an outcome before building, run the evals, or check whether the build passed, or runs /goal-evals. This grades model and agent outcomes; unit-testing code before writing it is test-driven-development instead.
---

# Eval-Driven Development

The Evaluate-phase skill, run eval-first. `goal-and-constraints` names the goal and the eval set it depends on; this skill turns that into a real **Eval Plan** *before* the build, runs it to prove the outcome, and feeds it into Learn as the reward signal. It makes GOAL's promise real: **outcome over output** needs a way to measure the outcome, and **verifiable rewards** need a verifiable grade.

It plans the evals; it does not build the harness. Building the runnable harness is the How, handed to Specify (OpenSpec) and Build (Superpowers), or to the user's existing eval tooling. GOAL plans; the build implements.

## What to do

Interview the user briefly (one step at a time is fine), then fill `references/eval-plan-template.md`, save it as `eval-plan.md` in the working project, and show it to the user.

1. **Anchor to the goal (hard gate).** Read the goal from the Brief. What outcome must the eval prove? If you and the user cannot write one concrete pass/fail task in under two minutes, stop and return to `goal-and-constraints`: the goal is not measurable yet. This gate is what makes development eval-driven, not eval-decorated.
2. **Source the eval set.** Start from real failures, not invented cases. Target 20 to 50 tasks to start. Name the ground truth, the development/held-out split, and how the set grows over cycles.
3. **Write tasks.** Grade the outcome (the final state), and grade the path too where the path carries an outcome (a safety-critical or irreversible action, tool misuse, a policy or PII violation, or a cost, token, or latency budget). Unambiguous (two experts would agree), with negative and distractor cases, partial credit where a task has parts, and a calibration check where the system reports a confidence.
4. **Design graders.** Rules, LLM-as-judge, or human per task. Commit to reading transcripts, not only scores. Validate any LLM-judge that gates a release against human labels before trusting it. See `references/grading-and-reliability.md`.
5. **Set the reliability bar.** pass@k (can it ever succeed) versus pass^k (does it succeed every time), pass^k for customer-facing or high-stakes. State the trial count k and report a confidence interval, so the bar is computable and is met only when the interval clears it. See `references/grading-and-reliability.md`.
6. **Wire to Learn.** Name the one field signal that becomes a new labeled task (for example, every job the user dismisses), where it is written, and the saturation check that says this suite has stopped discriminating. Keep the held-out portion out of the loop. A mechanism, not a vision.
7. **Hand off.** State what the build must implement, pointing at the user's existing eval tooling if any, then point the user to Specify (OpenSpec) and Build (Superpowers).

## Self-check before you finish

Check the Eval Plan against this rubric, and fix anything that fails:

- Every goal in the Brief maps to at least one eval task.
- Each task grades the outcome, and where the path carries an outcome that is graded too. Two experts would agree on the pass/fail.
- The set includes negative and distractor cases, not only happy paths.
- The set has a development portion and a held-out portion, and the held-out portion is never used for optimization or fed to the RL loop.
- Each task class has a stated bar (pass@k versus pass^k, pass^k for customer-facing or high-stakes), with a trial count k and a confidence interval.
- Any LLM-as-judge that gates a release is validated against human labels, with judge biases named.
- The plan names how it guards against optimizing to the test (Goodhart): a held-out measure, spot trajectory checks on passing runs, and periodic human transcript review.
- The plan says who builds the harness (the handoff is explicit) and points at existing eval tooling if the user has any.
- The Learn wiring is named: how the suite becomes the RL environment, the saturation watch, and the failure-to-task loop.
- The plan is grounded in real failures, not invented tasks.

## Two ideas that carry the skill

- **pass@k versus pass^k.** "It worked once" is not "it works every time". pass@k asks whether the system can ever succeed in k tries; pass^k asks whether it succeeds on all k. Customer-facing trust needs pass^k. This is the most confused idea in evals, so name which one each task class is held to. Depth in `references/grading-and-reliability.md`.
- **Grade the outcome, but do not test on the training set.** The development portion of the suite tunes the build and feeds the Learn reward loop; a held-out portion the system never trains on is what still measures whether it generalized, rather than whether it learned to pass the test (Goodhart).

## Phase state (for the GOAL status-line HUD)

This skill runs at two moments. When you **author** the plan early (right after the Brief), leave the current phase unchanged. When you **execute** the plan, this is the Evaluate phase: if the user runs the HUD (`docs/statusline.md`), set `.goal/state.json` in the working project to `{ "phase": "Evaluate", "project": "<the project folder name>" }`.

## Hand off

The Eval Plan hands the harness to Specify (OpenSpec) and Build (Superpowers), and its suite becomes the Learn-phase RL environment. `forward-deployed-pod` reviews the plan at the Discover/Specify gate and the eval report at the Evaluate gate. The reliability bar (pass^k) is the trust evidence `agency-design` uses to earn a step's climb to a higher autonomy level.

See `references/examples/` for two worked Eval Plans: `jobmate-ranking-evals.md` (an AI-native ranker) and `manufacturing-quality-evals.md` (a factory quality classifier).
