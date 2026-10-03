---
name: tools-creusot-extract-spec-prop
description: Build and maintain a simplified spec-to-proof documentation set for Creusot by extracting properties from component specs, tracking assumptions/trusted boundaries, and generating drift/coverage reports.
argument-hint: "[component-name or spec-path]"
---

Use this skill when specs changed (or may have changed) and you need a clear, low-noise answer to:
1. What properties should we prove now?
2. What assumptions/trusted points still exist?
3. What coverage and drift gaps remain?

## Canonical storage and file model

In-repo folder:
- `modelling/creusot/creusot-spec-coverage/`

Green/local mirror:
- `/home/cornel/PY_AGENT/creusot-spec-coverage/`

Maintained source files (human-maintained):
- `properties_to_prove.md`
- `assumptions_and_trusted.md`
- `README.md`

Coverage files (tool-generated/refreshable):
- `coverage/coverage_report.md`
- `coverage/spec_drift_report.md`

History archive:
- `history/` contains previous snapshots and superseded docs.

## Plain-English terminology

- **Global canonical sources**: component `spec.md` and product Rust code.
- **Properties to prove**: verification-target statements derived from those sources.
- **Coverage report**: generated view; never the source of truth.
- **Owner interface**: component interface responsible for implementing/proving a property.
- **Stale**: proof/report item no longer aligned with current code/spec.

## Required outputs

Always update:
1. `properties_to_prove.md`
2. `assumptions_and_trusted.md`
3. `coverage/coverage_report.md`
4. `coverage/spec_drift_report.md`

Always append/update a short **Document Evolution Summary** section at the end of each report.

## Workflow

### 1) Discover and select component specs

Process rule:
- **Automation first** (discover/scan/diff with script), then **manual semantic review**.

Run discovery:

```bash
find components -type f \( -path "*/specs/*/spec.md" -o -path "*/.specify/specs/*/spec.md" \) | sort
```

Then:
- Identify all candidate specs for the target component(s).
- Select active spec(s) (typically latest numbered spec folder).
- Record selected vs ignored specs in `coverage/spec_drift_report.md`.

### 2) Extract properties-to-prove from selected specs

Create/update `properties_to_prove.md` with:
- stable property IDs (`P1..Pn`),
- plain-English requirement,
- owner interface,
- scope marker (`active` vs `legacy` if spec removed workflow).

Rules:
- Preserve IDs when intent is unchanged.
- Use new ID only for materially new semantics.
- Never silently drop a property; mark `legacy`/`retired` with reason.

### 3) Assign property ownership by component interface

For each property, assign primary owner:
- `IDispatcher`: system-level API behavior and orchestration.
- `IDispatchMap`: per-entry state machine and map invariants.
- mark `shared` when both are required, but still choose one primary owner.

Add a human-readable ownership table to `coverage/spec_drift_report.md`.

### 4) Refresh assumptions and trusted boundaries

Update `assumptions_and_trusted.md`:
- active assumptions (A1..An),
- trusted items/lemmas,
- risk level and impact.

Explain each item in plain English for non-formal-method readers.

### 5) Generate coverage reports

#### `coverage/spec_drift_report.md`
Must include:
- selected spec files,
- key spec deltas (added/removed/changed requirements),
- impacted properties,
- ownership map by interface,
- plain-English interpretation.

#### `coverage/coverage_report.md`
Must include:
- coverage counts,
- status buckets (`Verified/Unchecked/Stale/Retired`),
- highest-priority gaps,
- plain-English reading guidance.

### 6) Archive superseded files

Move superseded docs to `history/` instead of deleting.
Add a brief note in `history/README.md` if the archive changed significantly.

## Validation checklist before finish

- Maintained files exist and are internally consistent.
- Derived files match maintained sources (no contradictory status text).
- Every property has an owner interface.
- Spec drift impacts are explicitly listed (no hidden removals).
- Each report ends with a Document Evolution Summary.

## Suggested automation hooks

If `/home/cornel/PY_AGENT/spec_trace_agent.py` is available, use it for:
- spec inventory generation,
- coverage snapshot generation,
- drift detection assistance.

Then run manual semantic review to:
- confirm active spec selection,
- validate property wording and ownership assignment,
- validate status bucket correctness (`Verified/Unchecked/Stale/Retired`).

## Final output format to user

Report:
1. Which specs were analyzed.
2. What changed in `properties_to_prove.md`.
3. What changed in `assumptions_and_trusted.md`.
4. Coverage/drift highlights.
5. Exact files updated.
