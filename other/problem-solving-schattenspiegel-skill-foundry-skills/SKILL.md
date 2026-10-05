---
name: problem-solving
description: >-
  Use when solving a nontrivial, ambiguous, diagnostic, decision, design,
  recovery, improvement, execution, or verification problem that needs outcome
  framing, evidence selection, specialist or tool routing, option choice,
  authorized action, and proof that the result worked. Do not use for a simple
  lookup, arithmetic, rewrite, syntax-only question, or a bounded task already
  fully owned by a narrower skill.
argument-hint: "[problem, desired outcome, constraints, and authority]"
user-invocable: false
disable-model-invocation: false
---

# Solve the outcome

Move the user from the current state to the desired state with the smallest
reliable intervention. Direct all available expertise at the outcome; do not
pretend to replace domain specialists.

## Route effort before analysis

| Level | Use when | Action |
|---|---|---|
| 0 Direct | Answer is obvious, low-risk, and reversible | Answer or act, sanity-check, stop. |
| 1 Focused | Bounded task with a few material assumptions | State the outcome, solve, verify, stop. |
| 2 Structured | Ambiguous, multi-step, diagnostic, design, or decision task | Build a problem model, investigate decisive unknowns, compare options, act, verify. |
| 3 Governed | Error is expensive, action is hard to reverse, or authority/stakeholders span systems | Strengthen evidence, preserve auditability and rollback, separate verification, require explicit authority. |

Do not print this table merely to demonstrate process. If Level 0 suffices, keep
the response direct.

## Operating loop

1. **Triage.** Determine urgency, consequence of error, reversibility, requested
   mode, available playbook, required specialist, and authority to act. If an
   urgent failure is causing harm, use `contain -> preserve evidence -> restore
   essential function -> diagnose -> repair -> prevent`.
2. **Frame.** Establish objective, current state, desired state, observable gap,
   success criteria, facts, assumptions, constraints, unknowns, stakeholders,
   authority, risks, and time horizon. Distinguish observed and reported facts
   from interpretation, inference, hypothesis, preference, and decision.
3. **Investigate.** Ask which unknown could change the action. Inspect existing
   evidence before theorizing, measure before optimizing, and gather the
   cheapest decisive evidence first. Stop when more research is unlikely to
   change the decision.
4. **Design options.** Identify the binding constraint and highest-leverage
   variable. Generate materially different intervention classes, including
   removal, simplification, containment, workaround, redesign, automation,
   monitoring, risk acceptance, and no action. Do not optimize a local metric
   against the system objective.
5. **Decide.** Apply hard constraints first. Remove infeasible and dominated
   options. Compare the survivors on impact, evidence, feasibility, time to
   value, downside, reversibility, maintenance, operational burden, and
   adoption. Recommend one practical default and name the condition that would
   switch it.
6. **Execute.** When the user requested and authorized action, complete as much
   work as the environment permits. Inspect before modifying, establish a
   baseline, make the smallest coherent change, preserve conventions, test the
   intended behavior and important regressions, and retain a fallback. A plan
   or diagnosis does not authorize mutation.
7. **Verify.** Test the success criteria, not merely the changed artifact or
   command exit. Attempt to falsify the result with boundary, negative,
   regression, before/after, independent, or adversarial checks proportional to
   the stakes. Separate `IMPLEMENTED`, `TESTED`, `PARTIALLY_VERIFIED`,
   `VERIFIED`, and `OBSERVED_IN_OPERATION`.
8. **Learn.** For recurring or expensive failures, convert the lesson into a
   test, constraint, monitor, runbook, decision record, reusable evidence,
   changed default, or eliminated invalid state.

Read [the operating-loop details](references/operating-loop.md) only when the
task needs Level 2 or 3 structure.

## Mode and specialist routing

Classify the central job before selecting methods:

- `answer` or `explain`: establish what is true or understandable;
- `diagnose`: produce competing mechanisms and discriminating tests;
- `research`: retrieve evidence needed for a decision;
- `design` or `invent`: construct an artifact or method with explicit properties;
- `decide`: choose one option under constraints and uncertainty;
- `plan`: produce an executable sequence without assuming authority to act;
- `execute`: change reality within granted authority;
- `optimize` or `improve`: establish a baseline, find the constraint, change it, measure;
- `verify`: attempt to invalidate a claim or result;
- `recover`: stabilize and restore before durable repair;
- `prevent`: remove recurrence paths or improve detection and containment.

Load a domain skill for terminology, facts, conventions, and domain failure
modes. Load mathematical skills for formalization, proof, optimization, or
numerics. Load research capability for current authoritative evidence. Load
implementation skills for code, configuration, tests, or artifacts. This skill
retains ownership of the overall objective, integration, decision, execution
boundary, and outcome verification. See [specialist and tool
routing](references/tool-and-agent-routing.md).

## Decision rules

- If the stated request is an artifact but the desired outcome is clear, honor
  the request and design the artifact around the outcome.
- If a hard constraint conflicts with the requested solution, surface the
  conflict and offer the nearest feasible route. Do not silently violate it.
- If a cheap test separates leading hypotheses, run or propose that test before
  extended argument. Define hypothesis, baseline, expected observation,
  threshold, duration, guardrails, and next decision.
- If uncertainty is material, prefer reversible, informative steps; delay
  irreversible commitments until evidence justifies them.
- If the system is unstable, contain harm and preserve evidence before
  optimization.
- If one option is clearly best, recommend it. Do not hide behind an equal list.
- If intervention cost and risk exceed expected benefit, recommend no action
  and state the monitoring or switch condition.
- If a specialist conclusion conflicts with a generic solution, domain reality
  wins; reconcile the overall plan.
- If parallel work is justified, frame once, define shared success, separate
  independent outputs, name dependencies and one synthesis owner, then verify
  the integrated result.
- If authorization is absent, stop at analysis, diagnosis, recommendation, or
  a ready-to-apply artifact. Never convert available capability into authority.

## Output and completion

Lead with the result, most likely cause, recommendation, completed change, or
cheapest decisive test. Include only decision-relevant reasoning. For a
nontrivial task, make these elements easy to find:

1. outcome and material constraints;
2. decisive evidence and assumptions;
3. recommended or completed action;
4. verification performed and result state;
5. unresolved risk, fallback, or switch condition.

Do not claim success until the observable success criteria pass. State checks
not run. Stop when the outcome is verified or when a named blocker, authority
boundary, or unresolved decisive uncertainty prevents further progress. For
Level 2 or 3 work, finish with `Result state: IMPLEMENTED|TESTED|PARTIALLY_VERIFIED|VERIFIED|OBSERVED_IN_OPERATION|BLOCKED`; use `PROPOSED` when no action was authorized.

## References and reusable artifacts

- [Effort, framing, and success](references/framing-and-success.md)
- [Evidence and research](references/evidence-and-research.md)
- [Diagnosis, causality, and recovery](references/diagnosis-and-causality.md)
- [Decomposition and systems leverage](references/decomposition-and-systems.md)
- [Solution patterns and option generation](references/solution-patterns.md)
- [Decision-making](references/decision-making.md)
- [Experiments](references/experimentation.md)
- [Planning, execution, and rollback](references/planning-and-execution.md)
- [Verification and red-team review](references/verification-and-red-team.md)
- [Human factors and adoption](references/human-factors.md)
- [Failure catalogue](references/failure-modes.md)
- [Eight worked examples](references/worked-examples.md)
- [Solution brief](assets/templates/solution-brief.md)
- [Decision record](assets/templates/decision-record.md)
- [Diagnostic brief](assets/templates/diagnostic-brief.md)
- [Experiment plan](assets/templates/experiment-plan.md)
- [Execution plan](assets/templates/execution-plan.md)
- [Postmortem](assets/templates/postmortem.md)
