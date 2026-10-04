---
name: generate-use-case
description: Create, refine, and review source-backed architecture use-case documents with actors, goals, flows, requirements, data handling, compliance controls, acceptance criteria, and stakeholder feedback. Use when the user supplies a use-case idea or reference such as UC-001, asks for a draft, or wants an existing use case updated after stakeholder discussion.
---

# Generate Use Case

## Workflow

1. Read the target repository's root `AGENTS.md`. When `project_name` is supplied, normalize it to lowercase letters, digits, and hyphens and load `profiles/<project_name>/profile.yaml` from the toolkit; reject an unknown project instead of choosing a nearby profile. Read the profile's `project_instructions.agents` and every `document_instructions.use_case` Markdown file completely, resolving those paths relative to the toolkit root. Also read the target repository's `architecture/toolkit-profile.yaml` when present, existing use cases, stakeholder notes, and relevant sources. Stop on a missing configured instruction. The target repository's root `AGENTS.md` remains authoritative; selected profile instructions may strengthen but not weaken it.
2. Resolve the next `UC-NNN` or the referenced existing use case. Never reuse or renumber an identifier.
3. Copy [assets/use-case-template.md](assets/use-case-template.md); replace every placeholder and remove irrelevant optional sections.
4. Separate stakeholder facts from proposals and assumptions. Ask focused questions when ambiguity changes scope, data handling, acceptance criteria, or risk.
5. Describe the main success flow and material alternate/error flows without prescribing architecture prematurely.
6. Apply the governance profile and the privacy/AI checklist in [references/use-case-quality.md](references/use-case-quality.md). Treat applicability as `To verify` when the project has not established it.
7. Keep status `Draft` while feedback is unresolved. Use `Reviewed` only with a cited stakeholder review source and `Approved` only with explicit authority.
8. Save under `architecture/use-cases/UC-NNN-<slug>.md` unless the repository has an established equivalent.

## Rules

- Use observable, testable language.
- Include only the minimum personal or health data categories needed; never include real subject data.
- Identify human decisions and automation boundaries for legal-, clinical-, or other high-impact outcomes.
- Preserve a concise feedback/change log when updating a reviewed draft.
- Link related ADDs, diagrams, ADRs, tasks, and evidence using repository-relative paths or authorized identifiers.
- Treat profile document instructions as domain-specific constraints. They may strengthen this workflow but must not override repository instructions, supplied evidence, lifecycle gates, or the prohibition on inferred approval and classification.
- Report the selected project key and each loaded instruction path so document-generation provenance is visible.

## Output

Return the draft path, status, assumptions, blocking questions, governance outcome, and recommended next step (`stakeholder review`, `$generate-bdr`, or `$generate-add` when a BDR is demonstrably unnecessary).
