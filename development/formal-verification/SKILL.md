---
name: formal-verification
description: |-
  Use when the user asks for formal verification or formal methods: writing or checking a design model (TLA+, Alloy, P, Quint), proving code against contracts (Dafny, Verus, SPARK, Frama-C, Lean, Rocq), model checking, invariants, liveness, vacuous passes, or counterexamples; deciding whether a design or requirement warrants formal verification; or keeping existing formal specs and proofs current. Not for prose requirements or "spec this out" (use sdd).
---

# Formal Verification

## Overview

A formal check proves that a model or code satisfies the statement it was given, under the stated assumptions and bounds.
It cannot show that the statement is what the user wanted.
In the documented failures of verified systems, the cause was a wrong specification, an unstated assumption, or a model that did not match the code.
Agents make this gap wider: they prove a given statement well, and they write the statement poorly.
In one benchmark, agent-written specifications passed their proofs in almost every run, and only 46 to 61 percent of them said what the issue required.

This skill guides one lifecycle with seven stages.
Each stage is an entry point: a job can start at any stage, and it enters only the stages it needs.
Every job carries a recorded purpose and a record of four alignment gaps, so that a later session can see what the work is for and what it has established.

## When to Use

- The user asks to model a design, check a protocol, or find concurrency or crash bugs with a model checker.
- The user asks to prove code correct, write contracts or loop invariants, or close proof obligations.
- The user asks whether a design, change, or requirement is worth formal verification, or which tool fits.
- An existing model, proof, or spec needs review, repair after a counterexample, or a check that it is still current.
- The user wants a formal model derived from existing code to find bugs in it.

## When Not to Use

- Writing prose requirements, proposals, or behavioral specs: use `sdd` or other "spec-driven development" methods.
  This skill reads SDD specs when they exist and never replaces them.
- Ordinary example tests, property-based tests, or fuzzing with no formal statement: use `writing-tests`.
- Formalizing mathematics that has no software requirement behind it.
- Installing or configuring a verifier.
  This skill presumes the tools are present.
  When a tool is missing, use search and your own knowledge to walk the user through setup, then return here.

## Invocation Notice

- Tell the user when this skill is running: `formal-verification`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Critical Constraints

These rules hold at every stage and for every tool.
They exist because each one blocks a failure observed in agent-led verification.

1. **A person decides what gets checked.**
   The user approves the purpose, the list of properties, and every statement before anything is proved or checked against it.
2. **No change to a statement without the user.**
   A counterexample can drive a change to code or to a proof without approval.
   A change to a specification, a property, a fairness assumption, a bound, a model configuration, or a contract goes to the user with a statement of what the change removes.
   "The property was too strict" is a proposal for the user, never a fix you apply.
3. **Mechanical gates, not prompts.**
   Use the tool's own checks and the statement freeze in `references/checking-and-proving.md`.
   A rule written in a prompt does not stop an agent that has found a way around it.
4. **Confirm a check can fail.**
   A pass counts only after you have seen the same check fail on a case it must reject.
5. **The report cites checker output.**
   Every pass, failure, bound, and assumption in the report cites a saved output file.
   Do not retype a result.
6. **Relate everything to the user's requirements.**
   A property derived from code, a model, or a published protocol is a description of that source, not of the user's intent.
   When code and a requirement disagree, the code is the suspect.
   Do not write the code's behavior into the specification.
7. **State what the evidence establishes; the user judges whether it is enough.**
   Do not call evidence weak, strong, sufficient, or insufficient.
   Say what was checked, how, within which bounds, and what it does not cover.

These instructions admit no exceptions.
"This is a quick model" or "I followed the intent" does not license skipping a step.
Small jobs stay small because they enter fewer stages, not because a stage gets skipped.

## Concepts

**The four alignment gaps.**
Each stage works on one or more of these, and the report states the status of each.

| Gap        | Question                                                                                       |
| ---------- | ---------------------------------------------------------------------------------------------- |
| user:agent | Does the agent understand what the user wants verified, and why?                               |
| user:spec  | Does the formal statement say what the user's requirements mean?                               |
| spec:code  | Does the thing that was checked or proved match the code that runs?                            |
| user:code  | Does the running code do what the user requires? The report answers this from the other three. |

**Purpose.**
Every job records three things before work starts:

- the question formal methods must answer;
- the decision the answer informs;
- the mode: **find bugs** or **establish assurance**.

The mode changes only what the report can claim.
The procedure is the same in both modes.
A find-bugs job reports findings with reproductions and never claims correctness.
If the user later asks "so it is correct?", that is a new assurance pass over the existing evidence: re-enter at the report stage in assurance mode and run any step the assurance claim needs that the first pass did not run.
Never switch the mode in the middle of a pass.

**The verified object.**
A check or proof is about one of three things, and the report names which:

- a **model** of the design (TLA+, Alloy, P, Quint);
- the **shipped code** (Dafny, Verus, SPARK, Frama-C, or Lean and Rocq when the code itself is written in them);
- a **translation** of the code into a prover's language, which is a model with the same gap to the code.

**The alignment file.**
One file per verification effort holds the purpose, the requirements trace, approvals, results, and stage history.
It grows by stage: each stage adds only its own section when the job enters it.
See `assets/alignment-template.md` for the sections and `references/alignment-file.md` for where it lives and how stages use it.

## Workflow

### Step 0: Entry gate

Run this at every entry, including a return in a new session.

1. **Find or create the alignment file.**
   Read `references/alignment-file.md`.
   If a file exists for this effort, read all of it before anything else.
2. **Confirm the purpose.**
   If the file has no purpose, elicit the question, the decision, and the mode from the user.
   Do not infer the mode from context.
   If the file has a purpose, state it back and confirm it still holds.
3. **Name the stage being entered.**
   Use the stage table below.
4. **Run that stage's entry check.**
   Each check confirms that the artifacts from earlier stages exist.
   If an artifact is missing, tell the user which stage would produce it.
   Run that stage, or record the gap as open with the user's agreement.
5. **Run the staleness check.**
   For every recorded result, compare the commit it was produced at with `HEAD` over its covered paths and the requirement source.
   See `references/reporting-and-maintenance.md`.
6. **State the gaps this stage works on**, from the stage table, before starting the stage.

### Stages

| Stage                | Gaps                    | Entry check                                                   | Reference                                 |
| -------------------- | ----------------------- | ------------------------------------------------------------- | ----------------------------------------- |
| 1. Decide            | user:agent              | User requirements exist, or the user agrees to state them now | `references/deciding.md`                  |
| 2. Specify           | user:spec               | Purpose recorded; tool chosen; requirements listed            | `references/specifying.md`                |
| 3. Validate the spec | user:spec               | Statement files exist in a freezable layout                   | `references/validating-the-spec.md`       |
| 4. Check or prove    | soundness of the result | Every statement approved, with an approved commit recorded    | `references/checking-and-proving.md`      |
| 5. Connect to code   | spec:code               | A result about a model or translation exists                  | `references/connecting-to-code.md`        |
| 6. Report            | all four                | At least one result with saved output                         | `references/reporting-and-maintenance.md` |
| 7. Maintain          | all four                | A prior result exists                                         | `references/reporting-and-maintenance.md` |

Read the stage's reference before you start the stage.
Do not work a stage from memory: each reference holds checks that the table does not.

Stage 5 applies only when the verified object is a model or a translation.
For a proof about the shipped code, the proof is the connection; record the remaining trusted gap (compiler, extraction, axioms) in the report and skip to stage 6.

Stages loop.
A counterexample often sends the job back to stage 2 or 3.
A loop back to a statement change goes through the user (constraint 2) and a new approval (stage 3).

### Tool facts

`references/tools.md` lists, per tool, the commands for vacuity checks, assumption listing, escape hatches, and gates.
Read the row for the chosen tool before stages 3 and 4.

### Independence

Two steps judge another step's work, and each must run in a fresh context that did not produce that work:

- the **blind back-translation** in stage 3, which must not see the requirements;
- the **result audit** in stage 4, which must not be the agent that produced the result.

Use a subagent for each when the harness has a subagent-dispatch tool (for example, `Agent` in Claude Code; substitute the harness's equivalent).
Without one, tell the user and ask them to run the step in a new session.

For long checking or proving runs, advise the user to start a separate session.
The alignment file is the handoff between sessions.

### Elective checks

The floor in each stage always runs.
Offer these as extra depth, recommend based on the cost of failure, and let the user choose:

- differential testing of the specification against an independent oracle, such as an older system or a reference implementation;
- a model-to-code connection in both directions (trace validation and test generation);
- a second model at finer atomicity after a clean run on a coarse model;
- a separate liveness model with smaller constants;
- proof-stability measurement for SMT-backed proofs.

Record which elective checks ran and which did not.

## Output

- The alignment file, current to the last stage entered.
- Statement files in a freezable layout, and models or proofs in their tool's location.
- Saved checker output for every run, cited by the report.
- A report that states, for each result: the purpose; the status of each gap with its evidence; the approval route of each statement; the verified object and what the result does not establish about the code; bounds and assumptions; elective checks run and not run; and staleness.
