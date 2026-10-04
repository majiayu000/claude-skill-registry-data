---
name: project-living-docs
description: Use for AI-assisted code changes that must keep project living docs in sync. Triggers on feature work, bug fixes, refactors, API/schema/security/deployment changes, requirement updates, tests, guardrails, and change records. Do not use for general Q&A or non-project snippets.
---

# Project Living Docs

Use NOC Living Docs as an agent memory router. For feature-archive projects, let the CLI identify or create the feature archive, read only routed docs, update `overview.md` through structured patches, record real evidence, and verify consistency. For simplified and v1 projects, keep the compatible legacy flow and do not silently migrate.

## Trigger

Use this skill for:

- initializing or migrating `noc_docs/`
- discussing a requirement and then changing code
- new features, bug fixes, refactors, API/data/security/deployment changes
- checking whether code changes need docs updates
- querying or auditing project living docs

Do not use it for general questions that do not involve project memory, code behavior, requirements, guardrails, tests, or NOC documentation.

## Execution

1. Detect the NOC layout from the machine-readable `noc work <project> --path <code/path> --json --intent "<agreed requirement>"` output and, if needed, `noc_docs/.living-docs/config.json`.
2. For `layout: feature-archive`, follow the feature-archive workflow below.
3. For `layout: simplified`, use the project-level three-file flow. Do not create `features/`, do not call `feature ensure`, and do not silently migrate.
4. For v1 `small` or `domain`, use the legacy feature/domain workflow. Do not convert the project to feature-archive unless the user explicitly asks for migration.

### Feature-Archive Workflow

1. Run:

```bash
noc work /path/to/project --path <code/path> --json --intent "<agreed requirement>"
```

Use `--staged` or `--changed` when the Git diff is the clearest input. Use `--feature <feature>` when the user has named a specific feature.

2. Select the feature:
   - If `candidates[0].confidence` is high confidence and not ambiguous, use that existing feature.
   - If the user clearly requested a new business feature, create it with `noc feature ensure <project> --id <ascii-kebab-id> --name "<display name>" --json`. Use a stable English ASCII feature id; keep Chinese display names in `name`.
   - If candidates are ambiguous or low confidence, ask the user once which feature to use or whether to create a new one. Do not ask multiple NOC-internal questions.
3. Before editing code, read only the routed project memory and selected feature docs: `project.md`, `guardrails.md`, `verification.md`, and the relevant `noc_docs/features/<feature-id>/overview.md`.
4. Make the code change.
5. Run real, relevant verification commands from `verification.md`, the feature overview, or the project’s existing test conventions. Do not record `passed` unless the command actually ran and exited 0; passed requires exit_code 0.
6. Collect code evidence with `noc evidence <project> --staged --json`.
7. Record verification evidence with `noc evidence record <project> --feature-id <feature-id> --file <evidence.json> --json`.
8. Generate a structured patch from the explicit user requirement, actual code diff, and verification result. Apply it only with `noc feature update <project> --id <feature-id> --patch-file <patch.json> --json`.
9. Check consistency with `noc check <project> --feature-impact-file <impact.json> --json`.
10. Reply briefly in the user’s language, normally Chinese for `language: zh-CN`, naming the change, verification, and NOC docs updated.

Do not freely rewrite `overview.md`. Do not directly edit the whole overview, translate existing Chinese prose into English, invent requirements, turn plans into current implementation, mark tests passed without evidence, or classify ordinary changes as major changes.

## Memory Impact

- `none`: formatting, comment fixes, local renames, behavior-preserving small refactors, implementation bug fixes that restore existing requirements, running existing tests, and ordinary tests added under the existing verification approach. Do not modify `noc_docs/`.
- `project`: project goals, project phase, major capabilities, technical boundaries, or architecture facts changed. In v2, update only `project.md`.
- `guardrails`: durable security, permission, data-loss, compatibility, public API, migration, or deployment constraints changed. In v2, update only `guardrails.md`.
- `verification`: standard test commands, build/release/acceptance procedures, or durable verification gates changed. In v2, update only `verification.md`.

Multiple durable impacts may apply; update only their corresponding files. Do not create `change-record.md`, `test-record.md`, `notes.md`, areas, or any new long-term document type for v2. For v1, keep reading the existing structure but apply the same semantic threshold and avoid routine document churn.

If the next Codex session did not know this fact, and that would not materially affect future work, do not store it in project memory.

For detailed workflow rules, read `references/workflow.md`.

## Language Rules

When `language: zh-CN`, write feature names, confirmed requirements, current implementation notes, verification summaries, major changes, and final responses in Simplified Chinese. Preserve the user’s Chinese requirement wording when it is explicit. JSON/YAML keys, feature ids, CLI flags, paths, code identifiers, and commands stay English or in their original spelling. Do not translate existing Chinese documents to English.

## Do Not Proceed

Stop and ask the user before editing code when:

- the request conflicts with `guardrails.md` or domain guardrails
- product intent conflicts with `requirements.md` and the intended direction is unclear
- affected feature/domain cannot be identified and the change is not obviously global
- required docs are missing and the task depends on unknown requirements or constraints
- the user asks to silently rewrite requirements to match current code
- the change touches security, permissions, billing, data loss, migrations, or public API contracts and the requested behavior is ambiguous
- the feature-archive candidate is ambiguous after `noc work`; ask the user once instead of guessing
- the project is simplified, small, or domain and the next step would require migration; migration requires an explicit user request

## Definition Of Done

A task using this skill is done only when the rules for the detected protocol are satisfied.

### v2 feature-archive projects

- `noc work --json` was used to identify candidate features
- high confidence candidates were selected automatically, or ambiguity was resolved by asking the user once
- new clear business features were created through `noc feature ensure`
- `project.md`, `guardrails.md`, `verification.md`, and the selected `overview.md` were read before code changes
- real verification was run, or a skipped verification reason was reported
- code and verification evidence were collected or recorded with `noc evidence` and `noc evidence record`
- `overview.md` was updated only through `noc feature update` with a structured patch
- `noc check <project> --feature-impact-file <impact.json> --json` passed, or failures were reported honestly

### v2 simplified projects

- affected memory was identified through v2 routing data
- `project.md`, `guardrails.md`, and `verification.md` were read as routed, or missing files were called out
- the actual diff was classified by memory impact
- only the memory files selected by that impact were updated; `none` caused no memory update
- code changes and project memory agree
- available checks were run, or skipped with a reason
- no feature archive was created and no migration was performed unless the user explicitly requested it

### v1 legacy projects

- the affected feature or domain was identified through the feature map
- required feature/domain docs were read, or missing docs were called out
- code changes and docs changes agree
- `requirements.md` changed only for intended behavior changes
- `status.md` reflects current behavior after behavior changes
- `test-record.md` records verification or explains why verification was not run
- `change-record.md` records important implementation changes, not routine churn
- indexes/checks were run when available, or skipped with a reason

Use a normal final response focused on development and test results. Do not output a fixed NOC template. Only when memory changed, append one short sentence such as `Project memory updated: project.md`.

## References

- `references/workflow.md`: mode selection, fallback rules, conflict handling, work loop
- `references/feature-doc-template.md`: what each feature doc should contain
- `references/domain-mode-guide.md`: when and how to use domain mode
- `references/codex-prompts.md`: recommended user prompts for Codex plan/goal/code workflows
