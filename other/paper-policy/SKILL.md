---
name: paper-policy
description: Resolve, validate, and audit manuscript integrity and applicable requirements for academic manuscripts and paper artifacts. Use when Codex needs to determine active paper rules from manuscript state, paper type, venue, submission stage, or workflow mode; lint a LaTeX paper project; assess submission readiness; create or update a paper policy profile; explain why a rule is active; or validate the paper-policy registries. Do not use as the primary skill for prose drafting, peer review, rebuttal writing, citation discovery, or figure/table creation.
---

# Paper Policy

Assess manuscript integrity, evidence and applicable project or venue requirements.
Editorial judgment lives in the writing, review and artifact guides. Choose wording,
structure and presentation for the task without preference-status records.

Read `references/authority-model.md` when resolving conflicts. Reliable venue or
project requirements can determine format; they cannot authorize fabricated facts
or unsupported claims. Keep artifact creation in its owning skill and evidence
management in the user-selected workflow.

## Choose the Operation

- **Ordinary writing or critique:** apply relevant integrity and explicit project
  constraints through the owning skill. No policy CLI, context file or full
  readiness assessment is required for a section edit.
- **Applicability or rule conflict:** read `references/context-schema.md` and
  explain which requirements apply and why.
- **Compliance or submission readiness:** read the context and compliance schemas,
  run relevant deterministic checks and inspect actual evidence.
- **Skill maintenance:** use `references/rule-maintenance.md` and validate changed
  registries, consumers and references together.

An existing context file or final-stage label does not expand the requested scope.
Briefs and working notes support continuity when useful; source snapshots needed
for an evidence-backed compliance PASS remain mandatory.

## Resolve and Assess

`references/hard-rules.yaml` contains manuscript requirements.
`references/profiles.yaml` activates conditional requirements from task context.
The scripts locate these files relative to the installed skill, with manuscript
paths supplied explicitly. Read `references/constraint-schema.md` for maintenance.

```bash
python3 /path/to/skills/paper-policy/scripts/resolve_policy.py /path/to/paper_context.yaml
python3 /path/to/skills/paper-policy/scripts/run_project_validation.py \
  /path/to/paper_context.yaml /path/to/paper --output-dir /path/to/validation-output
python3 /path/to/skills/paper-policy/scripts/assess_compliance.py \
  /path/to/paper_context.yaml --project /path/to/paper \
  --evidence /path/to/compliance-evidence.yaml
```

- Inspect scope, warnings and context provenance before interpreting results.
  Inference cannot activate provenance-sensitive requirements.
- Use `primary_tex` and optional `additional_tex` for multiple document roots;
  audit their include trees and referenced bibliographies.
- Generated artifact skeletons and evidence worklists are inspection aids, not
  evidence. Confirm discovered artifacts against their sources. Unused bibliography
  keys are maintenance candidates, not permission to delete entries.
- Check type is `deterministic`, `semantic` or `manual`. Missing admissible
  evidence leaves a requirement `UNVERIFIED`. Agent semantic PASS needs artifact,
  locator, reasoning and current source snapshots. Manual PASS requires human,
  user or venue evidence. Deterministic FAIL takes precedence over supplied PASS;
  agents cannot waive requirements. Follow `references/compliance-schema.md`.
- For a PDF or excerpt, inspect only what the available material supports and
  report unavailable checks. An empty TeX project cannot establish readiness.

## Output and Mutation

Resolution returns context, active requirements, activation reasons and unverified
inputs. It does not assign PASS. Assessment adds evidence-backed statuses and
unresolved checks. Report editorial recommendations only when useful to the task;
ordinary edits need no policy dump or per-choice explanation.

Assessment is read-only. When manuscript or bibliography fixes are already
requested, continue through the owning skill and make scoped, supported changes.
Registry validity does not establish scientific correctness or readiness.

## Resources

- `references/authority-model.md`: authority, waivers and execution boundaries.
- `references/constraint-schema.md`: requirement and activation-profile schema.
- `references/context-schema.md`: applicability, manuscript selection and provenance.
- `references/compliance-schema.md`: evidence, freshness and readiness semantics.
- `references/paper-context.example.yaml`: example formal-audit context.
- `scripts/validate_registry.py`: structural validation.
- `scripts/audit_skill_integration.py`: explicit references and registered rule IDs.
- `scripts/check_artifacts.py`: artifact sources, paths, formats and coverage.
- `scripts/discover_artifacts.py`: guarded LaTeX artifact inventory.
- `scripts/project_files.py`: selected TeX trees and bibliographies.
- `scripts/lint_project.py`: definite findings and contextual review hints.
- `scripts/run_project_validation.py`: resolution, lint, assessment, discovery,
  evidence worklist and located unused-key report.
