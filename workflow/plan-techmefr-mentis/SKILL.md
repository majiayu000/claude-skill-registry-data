---
name: plan
description: "Use when the architecture is set and the breakdown into atomic testable tasks is being written or reviewed, before tests or code. It supplies the discipline of the plan and tasks steps of the spec-kit cycle (discovery, ordering, review focus, proportion); the files are `speckit`'s."
---

# plan

Step 4 of the pipeline (`WORKFLOW.md`). Turn the target architecture into deliverable
increments. **This is not a second breakdown format.** The one process is the spec-kit cycle
(`skills/speckit`, `CONVENTIONS.md` Rule E): the increments are the cycle's `tasks.md`, step 0's discovery fills
`research.md`, and this block keeps its review rules (Review Focus, proportion, trust boundaries, verdict) on
top of them. Where the project's own template differs from this block's wording, the project's wins.

## When
After `archi`, before `tdd`, inside the cycle's plan and tasks steps, with or without the tool installed
(`skills/speckit` reference 01).

## Steps
0. **Documentation discovery, before anything is planned.** Find out what actually exists: read the
   documentation, the examples and the existing code paths the feature will touch, and write down the **allowed
   interfaces** (the functions, methods, options and signatures that are really there, each with the file or page it
   was read from) and the **anti-patterns to avoid** (things that sound plausible and do not exist, deprecated
   parameters, the wrong layer). Every later step plans against that list, not against what an interface "should"
   offer. Nothing in the plan names a call that is not on it.
1. Break into **atomic** increments: each one testable and deliverable independently.
2. Order by dependency (whatever unblocks the rest comes first).
3. Record **one tracked item per increment**, wherever the task's trail lives (a todo list, the ticket, a
   local orchestrator if there is one). The tracking must exist; the tool is not prescribed.
4. **What a step contains**: the minimum that lets the implementer write exactly one reasonable thing.
   A test step has the test name and its assertions with the spec's exact values; a code step has the file,
   the signature and the values the spec pins, and the body only for an algorithm the signature and tests
   do not determine; a verification step has the command and the output that means pass; a reference to
   another task points at that task's interface rather than repeating its code.
5. **Review Focus**: list at most five failure modes or inputs the spec implies but no task's tests
   exercise, most likely first, each pinned to a test in the task that owns the code. An empty list means
   the check was done and found none.
6. **Proportion check**: a plan several times longer than its spec has transcribed the code. Bring it back
   to signatures and assertions. A line that decides nothing ("handle edge cases") is the opposite fault.
7. **A reviewer of a plan adds phases; they never rewrite the original plan.** The author's phases stay as
   written and the added ones are marked as the reviewer's.

8. **Map the files before the tasks.** List which files will be created or changed and what each is
   responsible for, then cut the tasks along those lines; a task that needs a file the map does not show is a
   task the plan has not understood. Open the plan with a header that states the goal, the approach in a few
   lines and the global constraints that bind every task (exact values, formats, naming).
9. **No placeholders.** "TBD", "handle the edge cases", "add error handling" and "similar to task 3" are not
   steps: each is a decision postponed to whoever executes it. Write the decision, or write the question and
   who answers it.
10. **Self-review before handing the plan over**: re-read it against the spec, criterion by criterion; every
    criterion maps to a task, every task maps to a criterion. A spec that spans independent subsystems is cut
    into one plan per subsystem, each producing something that works alone.
11. **Frame a task as "follow this documented pattern at this location"** wherever a pattern exists (cite file
    and lines), not "convert the existing code". An executor copying a pattern it can see makes fewer inventions
    than one transforming code from a description.
12. **Delegated fact-gathering follows a report contract.** When delegated workers collect the facts
    for step 0, each report states: the sources consulted and what was read in them; the findings concretely
    (exact names and signatures, exact paths); where a copyable example lives; and a confidence note with the known
    gaps. A conclusion with no source is rejected and the work is sent again. Synthesis and the plan itself stay
    with whoever owns the plan (`skills/dispatch-parallel`).
13. **Every phase lists the anti-patterns it must not introduce**, as strings or patterns that can be searched.
    The final phase searches the changed files for them (`skills/gate`): the plan names what to look for,
    the gate looks. A check that cannot be searched is written as a review question instead.

14. **Every step traces to a line of the brief.** Walk the plan step by step and name the brief line it serves.
    A step with no such line is an addition nobody asked for, however reasonable it looks by itself: cut it, or
    send it back to the spec as a question. The same pass lists structure with exactly one use in the plan (an interface, a base
    class, a factory, a config option), each new dependency with what it buys over what the project already
    has, and error handling for states that cannot occur.
15. **Trust boundaries are named in the plan, not discovered in the code.** Every step that accepts data
    from outside the process (an HTTP call, a webhook, a message, a file, a third-party service) answers three questions: who may
    trigger it, what checks the incoming data, and what the response is allowed to contain. A step that crosses a boundary and names none of them is
    the plan's likeliest security defect, and answering it here costs a sentence. Add the one realistic
    failure or edge case the plan does not mention (one, not ten).
16. **An independent check ends in a verdict.** For a plan that carries risk, the check runs in a fresh
    context that never saw the plan being written, so it has no attachment to any part of it. It writes
    nothing and rewrites nothing; it returns `GO` (proportionate to the brief), `TRIM` (right shape, remove
    these items first) or `RETHINK` (it solves a different problem than the brief), with at most five findings
    ranked by cost. A plan that is fine gets `GO` in one line: inventing objections is the fault. It judges
    scope, structure and size, never naming or formatting.

17. **Self-review pass, task size and blocking edges.** Before handing `tasks.md` over, run the planner's own
    pass (name and type consistency across tasks, an Interfaces note per task), size each task, and write what
    blocks each one. Read [`references/17-self-review-sizing-and-edges.md`](./references/17-self-review-sizing-and-edges.md)
    when the task list is drafted or has to be cut or re-cut. It also holds the rule that tasks are cut
    as vertical slices, each run through `tdd` on its own.

## Output / checkpoint
`plan_done` + one tracked item per increment, in dependency order, recorded as the feature's `tasks.md`.

## Guardrails
No automatic execution of the whole plan (**no `/build auto`**: see `WORKFLOW.md`, auto-mode
was removed on purpose). The dev validates and moves forward step by step.

The one opt-in route to delegated execution is `skills/execute-plan`, which needs the operator's explicit decision
for every run. Writing a plan never starts one.

## Origin
Native / a market generalist dev skill catalogue (planning-and-task-breakdown), rewritten our
way.

Steps 4 to 6 rewritten from the `writing-plans` skill of `superpowers` (MIT, 6.4.x), read 2026-10-02, and steps 8 to 10 from the same skill (file map, header, no placeholders, self-review, one plan per subsystem). Steps 0, 11, 12 and 13 come from the `make-plan` and `do` skills of `claude-mem` (Apache-2.0, read 2026-10-02): documentation discovery first, copy-from-documentation framing, the sub-worker report contract and the searchable anti-pattern list. Rewritten in our words; no text copied, so its NOTICE obligations do not apply. Step 7 comes from the cross-model plan-review workflow in `claude-code-best-practice` (MIT), same date.

Steps 14 to 16 (brief traceability, speculative structure and dependency scrutiny, named trust boundaries, the GO/TRIM/RETHINK verdict from a fresh context, the five-finding cap) rewritten from the plan-check skill of abdian/claude-toolkit-laravel (MIT), read 2026-10-02. Rewritten in our words; no text copied. Nothing here relaxes the guard against automatic execution.

The provenance of step 17 (`references/17-self-review-sizing-and-edges.md`) and the owner's decision on vertical slicing (2026-10-19) are in [`references/origin.md`](./references/origin.md).
