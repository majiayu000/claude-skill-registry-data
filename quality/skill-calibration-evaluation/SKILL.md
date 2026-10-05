---
name: skill-calibration-evaluation
description: Run isolated calibration and drift evaluations for PyPI-distributed XRefKit Skills. Use when installed Skill packages expose evaluation manifests and the evaluator must run fixtures repeatedly without revealing expected answers, calibration rules, or held-out cases to the evaluated Skill.
---
<!-- xid: 720938921D2C -->
<a id="xid-720938921D2C"></a>


# Skill Calibration Evaluation

Run evaluation from the installed PyPI Skill package boundary. The repository
checkout is not the runtime source of a published Skill and must not be used as
the package contract.

## Inputs

- installed packages registered through the `xrefkit.skill_packages` entry-point;
- each package's strict `package_manifest.yaml` and co-located
  `evaluation/manifest.yaml`;
- model provider, exact model snapshot, and inference parameters;
- repetition count, normally at least three independent runs;
- output directory for raw outputs, scores, and the final human handoff.

## Isolation Rule

For each manifest case:

1. resolve the package root from the installed package entry point;
2. validate the evaluation manifest and case references;
3. create a fresh temporary target directory;
4. copy only the case's `target` fixture into that directory;
5. keep `expected` and `calibration` outside the target and outside the
   evaluated model context;
6. invoke the Skill through its normal package/runtime route;
7. destroy or quarantine the temporary target after collection.

The evaluated Skill receives the target and the ordinary task input. It does
not receive the expected answer, calibration rules, case id when that would
reveal the case purpose, or the evaluator's prior findings.

Use the bundled planner to produce an auditable plan:

```powershell
python scripts/plan_package_evals.py --discover --output work/eval-plan.json
```

Use `--package-root <installed-package-root>` only for package-level smoke
verification. Do not substitute a repository Skill path for an installed
package root in a published evaluation.

## Execution and Collection

Record for every run:

- package name, version, and package hash;
- Skill id and procedure hash;
- case corpus revision and fixture hash;
- model provider, model snapshot, and parameters;
- isolated target path and execution context id;
- raw Skill output and structured output artifact;
- expected/calibration evaluator result, kept outside the target context;
- run number and timestamp.

Run cases independently. Do not place multiple cases in one model context. Do
not tell the evaluated Skill that the input is an evaluation case when the
normal Skill task can be used instead.

## Calibration Evaluation

Score more than recall. Check:

- required output presence and schema validity;
- evidence and source-path coverage;
- severity or disposition calibration;
- `needs_confirmation`, unknown, and handoff behavior;
- forbidden overclaims from the case's calibration rules;
- repeat-to-repeat variance;
- regression against an approved baseline.

An alarm is a signal for human review, not permission to change the Skill. A
missing fixture, missing answer, package mismatch, or leaked evaluator asset is
`blocked`, not a passing or skipped case.

## Public and Held-Out Boundaries

Evaluation assets shipped in a public wheel are public smoke cases. They can
verify packaging and basic behavior but cannot protect against overfitting.
Held-out cases and their expected answers belong to a separate evaluator
package or controlled CI boundary. Never add held-out answers to the public
Skill package merely to make local scoring convenient.

## Human Handoff

Return a report with:

- `pass`, `alarm`, or `blocked` per case;
- raw-output and evidence links;
- missed expectations, overclaims, and calibration breaches;
- model/Skill/Knowledge change attribution where supported;
- baseline comparison and repeat spread;
- unresolved questions and the accountable Skill owner.

The Skill owner or quality reviewer decides whether to accept the alarm,
investigate the model, revise the Skill, revise the evaluation case, or update
the approved baseline. The evaluator must not self-approve a correction.
## Reporting Contract (共通報告)



- reporting_profile: checklist_verdict

Use the shared [Skill Reporting Contract](../../../docs/core/contracts/081_skill_reporting_contract.md#xid-6B2D9F4A1C73) in the final report. Start with these headings in this order:

1. Status — done, partial, blocked, or escalated
2. Result — what was produced or decided
3. Evidence — output, evidence, checks, or XIDs
4. Open Items — unresolved unknowns, risks, judgments, or なし
5. Handoff — next owner and next action, or なし

Keep this summary-first section visible before Skill-specific detail; do not omit empty sections.
