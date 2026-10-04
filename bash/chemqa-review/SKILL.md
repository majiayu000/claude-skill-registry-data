---
name: chemqa-review
description: Use when an agent needs the ChemQA react_reviewed control protocol as an installable multi-agent skill bundle layered on top of a sibling debateclaw-v1 skill, with fixed proposer plus four reviewer lanes, strict artifact reconstruction, and fail-fast dependency checks.
---

# ChemQA Review

This directory is an installable skill bundle.

Treat the directory containing this `SKILL.md` as `<skill-root>`.
This bundle must be installed beside these sibling skill bundles under the same
`skills/` root:

- `debateclaw-v1`
- `paper-retrieval`
- `paper-access`
- `paper-parse`
- `rdkit`
- `pubchem`
- `opsin`
- `chem-calculator`

## Purpose

`chemqa-review` recreates ChemQA's `react_reviewed` control protocol as a
portable skill bundle:

- one fixed main proposer lane
- four fixed reviewer lanes
- DebateClaw V1 handles the low-level debate transport
- this bundle injects ChemQA-specific role constraints, prompt assets, and
  artifact reconstruction
- prompt routing can hand deterministic chemistry subtasks to sibling provider
  skills for numeric and structure-heavy questions

## Root Rule

Always pass `--root <skill-root>` when a script accepts `--root`.

Do not use repo-relative paths such as `../debateclaw-v1`.
Resolve sibling skills from `<skill-root>/../`.

## Standard Flow

### 1. Check runtime and sibling skill availability

```bash
python3 <skill-root>/scripts/check_runtime.py \
  --skill-root <skill-root> \
  --json
```

### 2. Compile and materialize a launch-ready run

```bash
python3 <skill-root>/scripts/launch_from_preset.py \
  --root <skill-root> \
  --preset chemqa-review@1 \
  --goal "Question: does Pt/C improve HER activity in 1 M KOH?" \
  --launch-mode print
```

### 3. Rebuild react_reviewed-style artifacts after the debate completes

```bash
python3 <skill-root>/scripts/collect_artifacts.py \
  --skill-root <skill-root> \
  --source-dir <run-output-dir> \
  --output-dir <artifact-dir> \
  --json
```

## Role Topology

- `debate-coordinator`: protocol coordinator and final artifact aggregator
- `proposer-1`: main ChemQA proposer
- `proposer-2`: `search_coverage` reviewer
- `proposer-3`: `evidence_trace` reviewer
- `proposer-4`: `reasoning_consistency` reviewer
- `proposer-5`: `counterevidence` reviewer

Important:

- Only `proposer-1` is allowed to own the candidate submission.
- Reviewer lanes must not drift into independent final-answer proposals.
- The coordinator must emit `chemqa_review_protocol.json` so the artifact
  collector can rebuild the `react_reviewed` protocol surface.

## Prompt Routing Notes

- Numeric questions should prefer `chem-calculator` before
  web search when the prompt already provides the needed givens.
- Structure questions should extract available SMILES or name text
  first, then route to `rdkit`, `opsin`, and `pubchem` as appropriate.
- Reviewer lanes should cite provider result JSON artifact paths or structured
  `tool_trace` entries when challenging numeric or structural claims.
- This phase does not include a dedicated image-reading or OCSR skill.

## References

- Runtime checks and bridge behavior live in `scripts/`.
- Prompt contracts live in `prompts/contracts/`.
- Shared policy and artifact requirements live in `prompts/modules/`.
- The fixed control defaults live in `control/config-snapshots/react-reviewed-default.json`.
