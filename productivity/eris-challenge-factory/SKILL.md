---
name: eris-challenge-factory
description: Research, novelty-check, claim, hand off, build, revise, and final-audit Project Eris ML benchmark challenges across computers and Codex tasks. Use for dataset-first idea hunting, CPU-only challenge selection, permissive-license verification, duplicate audits, creating one new Codex task per approved idea, preparing real-data source packages, implementing prepare.py/grade.py/forms, applying reviewer feedback, maintaining challenge status, and checking rules, checkpoints, previous reviews, leakage, baselines, runtime, and submission robustness.
---

# Eris Challenge Factory

Use this single bundled copy for the portable Eris Challenge Bot. Do not create copies inside individual challenge folders. Keep challenge-specific facts in `Workspace/output/` or `Working/`, and keep shared policy in `Workspace/project/`.

## Resolve The Workspace

When `Config/workspace.json` exists in the portable bot, it is authoritative. The bot controller sets `ERIS_PROJECT_ROOT` and `ERIS_OUTPUT_ROOT` to directories inside the bot. Do not consult a user-profile factory configuration or legacy `C:`, `D:`, or `E:` challenge roots.

Otherwise, resolve paths in this order:

1. Explicit paths in the user's request.
2. `%USERPROFILE%\.codex\eris-challenge-factory.json`.
3. `ERIS_PROJECT_ROOT` and `ERIS_OUTPUT_ROOT` environment variables.
4. The current workspace when it contains `rules\LATEST.md`.

Run `scripts/workspace_probe.ps1` after resolving paths. On Windows systems that block local scripts, invoke it with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`. Do not silently use stale hard-coded paths from another computer.

The project root should contain the living rules and idea inventories. The output root should contain completed and active challenge folders. Treat those files, not chat memory, as authoritative.

## Select A Mode

- **Scout mode:** Find or assess novel challenge ideas and real datasets. Read [scout-workflow.md](references/scout-workflow.md).
- **Handoff mode:** Claim an approved idea and create one dedicated Codex task for it. Read [thread-handoff.md](references/thread-handoff.md).
- **Build mode:** Implement one challenge end to end. Read [build-workflow.md](references/build-workflow.md).
- **Revision mode:** Record reviewer feedback, fix the challenge, rerun all affected checks, and update the status record. Use the build workflow plus the live previous-review rules.
- **Audit mode:** Perform a rules/checkpoints/previous-reviews/final-submission audit without changing files unless the user asks for fixes.

If the user asks for an idea and then approves it, complete Scout mode first and use Handoff mode only after explicit approval.

## Load Living Policy

Before substantive work, locate and read when present:

- `.cursor\rules\challenge-creation.mdc`
- `rules\LATEST.md`
- `rules\checkpoints`
- `rules\prev_reviews.txt`
- other relevant files under `rules`
- `sprint_3\problems_with_acceptances.txt` or its current replacement
- current idea inventories and status records
- two or three relevant accepted examples

Follow the stricter current platform rule when sources conflict. Do not duplicate large living rule files inside this skill.

## Shared Gates

Apply these gates in every mode:

1. **Duplicate gate:** Scan titles, descriptions, modalities, target objects, output schemas, metrics, and solution families across all known challenge roots. A domain change alone is not novelty.
2. **Novelty gate:** Identify the closest dataset task, benchmark, paper, and local challenge. Stop when the core input, target, and standard solution remain substantially the same and novelty would be below the current threshold.
3. **Source gate:** Verify the official source, actual files, license text, commercial redistribution, attribution, archive size, checksums, and whether the needed labels truly exist. Never infer permission from a third-party mirror.
4. **Real-data gate:** Do not invent labels or claim generated data is real. Any permitted transformation must preserve the source-grounded learning problem and be documented.
5. **CPU gate:** Design and test for the current CPU, RAM, and wall-clock limits. Include runtime guidance in the platform-visible description.
6. **Dataset-size stability gate:** Use enough independent source-grounded units for a stable competition. For grouped image/map/audio/document tasks, do not ship tiny splits such as tens of train rows or a hidden test made from only a handful of source families. Do not treat a few hundred train rows and roughly one hundred test rows as review-ready when the source can support more; for image/map tasks, target on the order of 1,000+ train rows and several hundred test rows, with many independent held-out source families. Hidden worst-group scoring, abstention, or strict high-score caps require substantially more test rows and many independent held-out source families; otherwise one wrong decision can dominate variance and reviewers may reject the design even if checks pass.
7. **Shortcut gate:** Measure metadata-only, lookup, template, parser, source-retrieval, hand-feature, and simple open-source baselines before making the grader harsher.
8. **Fairness gate:** Difficulty must come from the data, split, and task. Do not suppress scores with arbitrary powers, hidden weights, hostile exactness, or decorative dependent heads.
9. **Leakage gate:** Group all related source families together; strip source IDs and paths; test modality-specific source fingerprinting for named public corpora.
10. **Grader gate:** Enforce exact schema, IDs, finite values, ranges, JSON limits, malformed-input safety, perfect score 1.0, and a valid weak sample.

## Scout-To-Build Readiness

Do not equate an interesting formulation with a build-ready challenge. Before recommending **proceed** or creating a dedicated build task, verify all of the following from actual source artifacts:

- the exact input and every scored target coexist at the required sample unit or can be joined deterministically;
- scored labels are native or independently derivable from authoritative before/after states, not parser output treated as truth;
- the official files or API are currently accessible without missing credentials and can legally be redistributed;
- a bounded pilot demonstrates usable-row yield, independent-family count, raw-package size, and lookup resistance;
- the projected split meets the dataset-size stability gate after filtering, not before;
- the challenge remains answerable after removing public-source identifiers;
- the strongest obvious rule/parser/retrieval baseline does not collapse the task.

Use these verdicts precisely:

- **Proceed:** all readiness evidence above is measured. A build task may be created.
- **Pilot:** the source is credible but one or more readiness facts are unmeasured. Do not create or describe a full build task; create a bounded pilot/audit task only when the user asks to run the pilot.
- **Hold:** access, license, label provenance, scale, or determinacy depends on an unresolved external condition. Do not claim the challenge.
- **Reject:** evidence shows the core formulation cannot pass without invented labels, public-answer lookup, trivial parsing, or a prohibited task type.

User approval does not turn a Pilot/Hold candidate into Proceed. Explain the missing evidence and complete the gate first.

Before any full build-task handoff, write a compact source-evidence card in the challenge registry containing the measured post-filter sample count, independent split-family count, official raw bytes/URLs, verified license, representative native label rows, lookup test, and strongest simple baseline. If any field is missing, keep the work in Scout mode and run the pilot there; never offload an unmeasured pilot gate to a task presented as challenge creation. If a dedicated pilot proves the source cannot meet scale or provenance requirements, mark the registry entry rejected with the measured reason and archive that pilot task.

Also require a machine-checkable `readiness` object and run `scripts/validate_handoff_readiness.ps1` before creating a full build task. Read [pre-handoff-gate.md](references/pre-handoff-gate.md) for the schema and failure-informed stop rules. A full build prompt must contain no unresolved discovery gate such as "find enough rows", "prove the labels exist", "check whether retrieval works", or "verify an accessible source". Those are Scout/Pilot tasks.

Treat a low toy baseline as insufficient evidence. Before `Proceed`, run one capability-matched attack that uses the strongest obvious domain method available to a capable solver, such as SIFT/RANSAC for maps, DTW/cross-correlation for signals, graph matching for diagrams, a finite-state parser for formal text, or exact/rare-phrase retrieval for public documents. Record both the attack and why it approximates the likely platform-agent route.

Write a short reviewer premortem before handoff. It must answer: why this is not the source's canonical task, why each input modality is necessary, why a no-op or copied input scores near the floor, why the hidden split contains enough independent groups, and what exact evidence would still cause rejection. If any answer depends on future work, the verdict is not `Proceed`.

Do not promise that agents will score below a threshold before measuring baselines and skill sweeps.

When a build task discovers a blocker that the pre-handoff gate should have measured, classify it as a handoff-process failure, add the reusable lesson to the Scout gate, and do not describe it as ordinary build uncertainty.

## Coordinate Multiple Computers

Read [coordination.md](references/coordination.md). Before starting work:

1. Sync or pull the shared project.
2. Scan the output root and `challenge_registry`.
3. Claim exactly one challenge using `scripts/new_challenge_status.ps1`.
4. Assign one owner machine and one owner task to each challenge folder.
5. Sync after milestones and before appending global reviewer memory.

Use separate JSON status files so independent challenges rarely edit the same coordination file. Never let two computers edit the same challenge folder concurrently unless the user explicitly assigns disjoint files.

## Completion Standard

Do not stop at a proposal when Build mode was requested. Complete implementation, source acquisition, preparation, grading, forms, smoke tests, baselines, audit, and handover unless a mandatory gate fails. If a gate fails, record the evidence and mark the challenge blocked or rejected instead of disguising the failure.

When this factory is running inside an automation batch whose target is a fixed number of successful challenges, a blocked/rejected verdict applies to the candidate formulation, not to the parent success slot. Return the evidence to the automation controller, preserve it as a candidate attempt, and scout a distinct replacement in the same slot. Never waive the mandatory gate, and never count the failed candidate toward the requested success total.
