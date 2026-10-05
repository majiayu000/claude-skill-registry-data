---
name: eris-challenge-factory
description: Research, novelty-check, claim, hand off, build, revise, and final-audit Project Eris ML benchmark challenges across computers and Codex tasks. Use for dataset-first idea hunting, CPU-only challenge selection, permissive-license verification, duplicate audits, creating one new Codex task per approved idea, preparing real-data source packages, implementing prepare.py/grade.py/forms, applying reviewer feedback, maintaining challenge status, and checking rules, checkpoints, previous reviews, leakage, baselines, runtime, and submission robustness.
---

# Eris Challenge Factory

Use one installed copy of this skill per computer. Do not create a copy inside every challenge folder or task. Keep challenge-specific facts in that challenge folder and keep shared policy in the synchronized project workspace.

## Resolve The Workspace

Resolve paths in this order:

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
6. **Shortcut gate:** Measure metadata-only, lookup, template, parser, source-retrieval, hand-feature, and simple open-source baselines before making the grader harsher.
7. **Fairness gate:** Difficulty must come from the data, split, and task. Do not suppress scores with arbitrary powers, hidden weights, hostile exactness, or decorative dependent heads.
8. **Leakage gate:** Group all related source families together; strip source IDs and paths; test modality-specific source fingerprinting for named public corpora.
9. **Grader gate:** Enforce exact schema, IDs, finite values, ranges, JSON limits, malformed-input safety, perfect score 1.0, and a valid weak sample.

Do not promise that agents will score below a threshold before measuring baselines and skill sweeps.

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
