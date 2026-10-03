---
name: codex-spec-driven-development
description: Use for prototype, MVP, fullstack feature, from-scratch feature, or multi-domain work that needs a SPEC.md before planning or implementation. Do not use for tiny one-file edits.
load_priority: on-demand
---

## TL;DR
Use before `$prototype`, MVP, fullstack, or high-ambiguity feature work. Write `.codex/specs/<slug>/SPEC.md` first, then plan, delegate, implement, and validate against acceptance criteria.

## Activation
1. Activate on `$spec`, `$prototype`, "spec-driven", "MVP", "fullstack prototype", "from scratch", or "build whole app".
2. Activate when a task spans frontend + backend, data, QA, or deployment concerns.
3. Activate when requirements are ambiguous enough that coding first would create rework.

## Hard Rules
- Do not implement prototype/fullstack work before a spec exists.
- Specs must include requirements, non-goals, acceptance criteria, FE/BE/data/QA impact, and validation plan.
- Specs must include `Schema-Version: 1.0`, AC IDs such as `AC-001`, and a traceability table mapping changed files to AC IDs and validation commands.
- Keep specs project-local under `.codex/specs/`; do not always load every spec.
- Use `check_spec.py` after code changes when `.codex/specs/` exists.
- Treat spec checks as advisory in quality gate unless the user makes spec compliance mandatory.

## Commands

```bash
python "<SKILLS_ROOT>/codex-spec-driven-development/scripts/init_spec.py" --project-root <path> --title "<title>"
python "<SKILLS_ROOT>/codex-spec-driven-development/scripts/check_spec.py" --project-root <path> --changed-files <csv>
```

## Output Contract
- `init_spec.py` returns JSON with `status`, `spec_path`, and `slug`.
- `check_spec.py` returns JSON with `schema_version`, `overall`, `matched_specs`, `matched_acceptance_criteria`, `unmapped_files`, and `suggested_actions`.

## Prototype Flow
1. Run `$hook` to detect domains and readiness.
2. Run `$init-profile` if profile is missing.
3. Run `$genome` and `$init-docs` if context/docs are missing.
4. Run `$spec` to lock requirements and acceptance criteria.
5. Run `$plan`, then `$sdd` or inline execution.
6. Run `$check-full` and update role docs/handoff.

## Reference Files
- `references/spec.schema.json`: required spec markdown contract and traceability fields.
