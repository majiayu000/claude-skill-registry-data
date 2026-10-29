---
name: speckit-workflows-refactor
description: Create a refactoring workflow with metrics tracking and behavior preservation
  validation.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:workflows
---

# Workflows Refactor Skill

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.workflows.refactor` (or `/speckit.refactor`) in the triggering message **is** the refactoring description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that refactoring description, do this:

1. Run the script `.specify/extensions/workflows/scripts/bash/create-refactor.sh --json "$ARGUMENTS"` from repo root and parse its JSON output for REFACTOR_ID, BRANCH_NAME, REFACTOR_SPEC_FILE, TESTING_GAPS, METRICS_BEFORE, BEHAVIORAL_SNAPSHOT. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

2. Load `.specify/extensions/workflows/templates/refactor/refactor-template.md` to understand required sections.

3. Write the refactor spec to REFACTOR_SPEC_FILE using the template structure:
   - Fill "Motivation" section with code smells and justification from description
   - Fill "Proposed Improvement" with refactoring approach
   - Identify files that will be affected
   - Fill "Phase 0: Testing Gap Assessment" with initial assessment
   - Leave baseline metrics sections empty (will be filled by measure-metrics.sh)
   - Document behavior preservation requirements
   - Assess risk level (High/Medium/Low)

4. Update TESTING_GAPS file with initial testing gap assessment:
   - Identify code areas that will be modified during refactoring
   - List files/functions/classes to be refactored
   - Flag this as critical first step before baseline
   - Provide guidance on assessing test coverage

5. Update BEHAVIORAL_SNAPSHOT file with key behaviors to preserve:
   - Extract observable behaviors from description
   - Document inputs and expected outputs
   - Create verification checklist

6. Report completion with Next Steps:

```
Refactor workflow initialized

**Refactor ID**: [REFACTOR_ID]
**Branch**: [BRANCH_NAME]
**Refactor Spec**: [REFACTOR_SPEC_FILE]
**Testing Gaps**: [TESTING_GAPS]
**Behavioral Snapshot**: [BEHAVIORAL_SNAPSHOT]

**Next Steps:**
1. **CRITICAL FIRST STEP**: Complete testing gap assessment in [TESTING_GAPS]
   - Identify all code that will be modified
   - Assess test coverage for affected areas
   - Add tests for critical gaps BEFORE capturing baseline
2. Review refactoring goals and behaviors to preserve
3. Once testing gaps are addressed, baseline metrics have been automatically captured
4. Run `/speckit.plan` to create refactoring plan
5. Run `/speckit.tasks` to break down into tasks
6. Run `/speckit.implement` to execute refactoring

**Reminder**: Behavior must not change - all tests must still pass
**NEW**: Testing gap assessment ensures adequate coverage exists to validate behavior preservation
```

Note: The script creates and checks out the new branch before writing files. Refactoring MUST follow test-first approach - all existing tests must pass before and after. **NEW**: Testing gaps must be assessed and critical gaps filled BEFORE baseline capture. Baseline metrics are automatically captured during workflow creation but should only be trusted after testing gaps are addressed.
