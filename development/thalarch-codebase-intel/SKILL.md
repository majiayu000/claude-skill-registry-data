---
name: thalarch-codebase-intel
description: >
  Builds a bounded, evidence-backed mental model of an unfamiliar or large repository before
  architecture work, broad refactors, feature-level repair, onboarding, review, or cross-module
  debugging. Uses read-only project and diff probes to orient routing without replacing
  task-relevant source inspection.
---

# Thalarch Codebase Intel

Do not “read the repo”. Build only the map needed for the task.

## 1. Scan order

1. repository rules and intent docs;
2. build manifests, language/toolchain evidence and module graph;
3. entry points relevant to the task;
4. inbound/outbound dependencies of the changed/broken feature;
5. data/control flow;
6. tests around the same behavior and its consumers;
7. CI/runtime integration points;
8. recent Git history for the affected surface.

Every architectural/control-flow claim needs a concrete file path, command output, source location,
or runtime observation.

Mark important conclusions:

- `FACT`;
- `INFERENCE`;
- `UNKNOWN`.

Do not silently turn inference into fact.

## 2. Feature-level repair mapping

When the request is “make this feature/module work” rather than one isolated symptom, map a bounded
feature boundary before fixes:

- primary entry points;
- internal files actually participating in the path;
- dependencies imported/called;
- consumers/callers outside the feature;
- config/env/schema/API contracts;
- tests that directly exercise the feature and tests of important consumers;
- recent changes in the affected surface.

Do not mechanically read every file in a large folder. Follow the dependency/control-flow graph
until the relevant boundary is understood.

Use `thalarch-debug` for individual causal failures discovered inside that map.

## 3. Deliverable

Create a task-focused context packet:

- stack/languages/toolchain/modules;
- relevant call/data-flow;
- important interfaces/invariants;
- existing patterns/helpers to reuse;
- project-native tests/build commands;
- affected consumers;
- risk hotspots;
- open unknowns.

Do not create permanent documentation unless requested.

## 4. Optional project probe

When shell execution is available, `scripts/project_probe.py` provides a read-only orientation
snapshot of:

- repository rules;
- build/tooling markers;
- source-language counts;
- Git branch/status;
- changed files;
- recent commits.

Run scripts as black boxes before reading their source:

```bash
python scripts/project_probe.py --path <workspace>
```

Use `--json` when another agent/script will consume the output.

The probe is orientation evidence, not a substitute for reading task-relevant code.

## 5. Optional change probe

For non-trivial diffs/reviews, `scripts/change_probe.py` emits deterministic routing signals from
Git paths, diff stats, language extensions and added-line keywords:

```bash
# Working tree vs HEAD
python scripts/change_probe.py --path <workspace>

# Current branch vs a base ref using merge-base comparison
python scripts/change_probe.py --path <workspace> --base main
```

It reports:

- changed file/add/delete counts;
- languages touched;
- path signals such as security, migration/data, CI/release, API contract, build/tooling, UI;
- content signals for concurrency/security/network/persistence;
- suggested review lenses.

These are **routing leads, not defects or severity judgments**. Confirm all material findings in the
real source/runtime before changing code or blocking a PR.

## 6. Context economy

- search symbols/paths before opening full files;
- read implementation and a nearby analogue rather than broad directory dumps;
- use generated/build/cache folders only when the task specifically concerns them;
- use Git history on the affected surface, not the entire repository;
- store a compact context packet for handoff instead of pasting large files into every subagent.
