---
name: research-development-workflow
description: Run an explicit, stateful research-development workflow from an important problem through evidence, minimal models, mechanisms, falsification, boundaries, generalization, and contribution decisions. Use only when the user explicitly invokes this skill to start, diagnose, continue, challenge, or close a substantial research program; do not use for isolated literature searches, statistical tests, or routine writing.
---

# Research Development Workflow

Develop research from a concrete problem toward the strongest conclusion the evidence can support. Treat the process as a loop, not a mandatory linear checklist.

## Invocation boundary

This skill is explicit-only. Once invoked, it owns stage diagnosis and workflow order for the current research task. Other research, statistics, experiment-design, citation, or writing skills are optional specialists: load only the capability needed at the current stage, never all of them by default.

Do not enlarge the user's project merely to complete every stage. A rigorous concrete result, measurement contribution, dataset, tool, replication, or negative result can be a valid stopping point without a universal theory.

## Choose the mode

- **start**: turn an idea, phenomenon, or practical difficulty into an answerable research problem.
- **diagnose**: locate an existing project in the lifecycle, identify unsupported claims and the next blocked gate.
- **continue**: resume from a research-state record or a recoverable description of prior work.
- **challenge**: stress-test the favored mechanism through alternatives, counterexamples, assumption removal, and boundary probes.
- **close**: decide the supported contribution level, remaining claims, stopping point, and paper-ready evidence structure.

If no mode is supplied, infer it from the request and say which mode is being used. Ask only for information that would materially change the next research action.

## Required reading

1. Always read [core-framework.md](references/core-framework.md).
2. For `start`, `diagnose`, or `continue`, read [lifecycle-and-gates.md](references/lifecycle-and-gates.md).
3. For mechanism claims, stages 4-8, or `challenge`, read [mechanism-and-falsification.md](references/mechanism-and-falsification.md).
4. For boundary, transfer, universality, stages 9-10, or `challenge`, read [boundaries-and-generalization.md](references/boundaries-and-generalization.md).
5. For `close`, publication framing, or stopping decisions, read [contribution-and-stopping.md](references/contribution-and-stopping.md).
6. When the user wants persistence or cross-session recovery, use [RESEARCH_STATE_TEMPLATE.md](assets/RESEARCH_STATE_TEMPLATE.md). Do not create or edit a state file unless requested.

## Operating loop

1. Establish the user's intended outcome and constraints.
2. Recover existing evidence, decisions, failures, and open questions before proposing new work.
3. Diagnose the current stage and the earliest unsatisfied gate.
4. Separate observations, interpretations, assumptions, and proposed actions.
5. Select the smallest next action that can change the researcher's belief or unblock the gate.
6. Predict the expected result and the result that would weaken the favored explanation before running or recommending the test.
7. Inspect negative, anomalous, and boundary cases rather than reporting only aggregate gains.
8. Update the research state and contribution ceiling from the new evidence.
9. Stop when the user-approved objective is met or the next step is not justified by expected information gain, cost, or evidence needs.

## Evidence discipline

- "Works" and "why it works" are different claims.
- An ablation supports component contribution in the tested setup; it does not by itself prove the proposed mechanism or necessity.
- Failure to reject is not proof of equivalence or absence.
- Removing an assumption in a finite experiment does not prove that assumption unnecessary in general.
- Cross-domain analogy is a hypothesis until shared invariants and transport conditions are demonstrated.
- Label conclusions as observed, inferred, conjectured, or untested.
- Report the tested boundary before making real-world, causal, universal, or safety claims.

## Output contract

For a substantive run, provide:

1. **Current stage and mode**.
2. **Research claim under examination**.
3. **Evidence already available**, separated from interpretation.
4. **Main uncertainty or blocked gate**.
5. **Smallest next discriminating action**.
6. **Predicted outcomes and belief updates**.
7. **Current contribution ceiling**: what can be claimed now, not after hoped-for work.
8. **State update** when persistence was requested.

Do not manufacture novelty, citations, results, necessity, generality, or a paper story. Use the user's language unless a deliverable requires another language.
