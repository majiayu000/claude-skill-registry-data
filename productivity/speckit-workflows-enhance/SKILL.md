---
name: speckit-workflows-enhance
description: Create a minor enhancement workflow with condensed single-document planning.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/enhance.md
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.workflows.enhance` (or `/speckit.enhance`) in the triggering message **is** the enhancement description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that enhancement description, do this:

1. **Read configuration** — Check for a project config at `.specify/extensions/workflows/workflows-config.yml`. If present, read `enhance.max_tasks` and `enhance.min_tasks`. If absent, use the extension defaults: `max_tasks=7`, `min_tasks=3`. The environment variable `SPECKIT_WORKFLOWS_ENHANCE_MAX_TASKS` overrides both (highest priority). Call the resolved values MAX_TASKS and MIN_TASKS for the steps below.

2. Run the script `.specify/extensions/workflows/scripts/bash/create-enhance.sh` from repo root and parse its JSON output for ENHANCE_ID, BRANCH_NAME, and ENHANCEMENT_FILE. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

3. Load `.specify/extensions/workflows/templates/enhance/enhancement-template.md` to understand required sections.

4. Write the enhancement document to ENHANCEMENT_FILE using the template structure, replacing placeholders with concrete details derived from the enhancement description while preserving section order and headings.
   - Extract what is being enhanced and why from the description
   - Define proposed changes clearly
   - Create a simple, single-phase implementation plan
   - Break down into MIN_TASKS–MAX_TASKS specific tasks. If the scope clearly requires more than MAX_TASKS tasks, **stop and suggest `/speckit.specify` instead** before creating any files.
   - Define clear acceptance criteria
   - Mark priority based on description (enhancement requests are typically Medium unless specified)

5. Report completion with Next Steps:

```
Enhancement workflow initialized

**Branch**: [BRANCH_NAME]
**Enhancement ID**: [ENHANCE_ID]
**Enhancement Document**: [ENHANCEMENT_FILE]
**Task limit applied**: MIN_TASKS–MAX_TASKS tasks (from [config file | env var | extension defaults])

**Next Steps:**
1. Review the enhancement.md document
2. Verify the implementation plan is appropriate for a minor enhancement
3. Run `/speckit.implement` to execute the enhancement
4. Verify all tests pass and functionality works as expected

**Reminder**:
- If this requires more than 1 phase or >MAX_TASKS tasks, consider using `/speckit.specify` instead
- Enhancement workflow is for quick, minor improvements only
- All changes should still include appropriate tests
- To change the task limit: edit `.specify/extensions/workflows/workflows-config.yml`
  or set `SPECKIT_WORKFLOWS_ENHANCE_MAX_TASKS=<n>` in your environment
```

Note: The script creates and checks out the new branch before writing files.