---
name: feature-files-authoring
description: Applies repository-specific Gherkin and BDD conventions to feature files. Use this skill when creating or editing `.feature` files.
---
# Feature Files Authoring

## Discover the Repository Contract

Before editing, find and read the repository's agent instructions, contribution guide, feature-file README, documentation standards, test-runner configuration, and nearby feature files.
Treat repository rules and established local structure as authoritative.

Determine the following without assuming fixed names or locations:

- Feature-file roots and component or suite layout.
- Allowed tags and their placement.
- Required user-story or narrative format.
- Requirement and specification traceability formats.
- Supported Gherkin dialect and runner.
- Formatting, linting, dry-run, and test commands.

If identifier allocation or a required tag cannot be derived safely, ask for direction instead of inventing it.

## Author Executable Behavior

- Keep each feature focused on one coherent capability unless repository rules explicitly permit cross-component coverage.
- Describe observable behavior and outcomes rather than implementation details.
- Use domain language consistently with requirements, specifications, and existing scenarios.
- Give each scenario one clear behavioral purpose.
- Include preconditions only when they materially affect the behavior.
- Prefer reusable Background steps only when every scenario needs them.
- Use Scenario Outlines and Examples when they clarify meaningful input or outcome variations.
- Cover success, boundary, and failure behavior required by the source material without duplicating equivalent scenarios.
- Preserve existing step vocabulary when compatible steps already exist.

## Maintain Traceability

Derive tags and references from the repository's canonical identifiers and transformation rules.
Verify that every referenced requirement, specification, issue, or anchor exists.
Apply traceability at the Feature, Rule, Scenario, or Examples level exactly where local conventions require it.
Do not copy one repository's tag prefixes, suite names, identifier formats, or directory mapping into another repository.

## Preserve Gherkin Structure

Use the repository's required ordering for tags, `Feature:`, narrative text, `Background:`, `Rule:`, Scenarios, and Examples.
Keep step indentation and keyword usage consistent with neighboring files.
Use `Given` for context, `When` for the action or event, and `Then` for observable outcomes unless the project defines a different style.

## Validate the Result

Run the repository-provided formatter, Gherkin linter, runner dry-run, or targeted acceptance-test command.
Prefer project task runners over invoking underlying tools directly.
Do not send `.feature` files to Markdown tooling unless the repository explicitly requires it.
Report commands run, failures encountered, and checks that could not be performed.
