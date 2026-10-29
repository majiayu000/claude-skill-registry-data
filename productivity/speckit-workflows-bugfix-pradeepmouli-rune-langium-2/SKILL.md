---
name: speckit-workflows-bugfix
description: Create a bug fix workflow with regression test and minimal documentation.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/bugfix.md
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.workflows.bugfix` (or `/speckit.bugfix`) in the triggering message **is** the bug description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that bug description, do this:

1. Run the script `.specify/extensions/workflows/scripts/bash/create-bugfix.sh` from repo root and parse its JSON output for BUG_ID, BRANCH_NAME, and BUG_REPORT_FILE. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

2. Load `.specify/extensions/workflows/templates/bugfix/bug-report-template.md` to understand required sections.

3. Write the bug report to BUG_REPORT_FILE using the template structure, replacing placeholders with concrete details derived from the bug description (arguments) while preserving section order and headings.
   - Extract current behavior, expected behavior, and reproduction steps from description
   - Mark severity based on description keywords (crash/data loss = Critical, broken feature = High, etc.)
   - Leave root cause analysis empty (to be filled during investigation)
   - Leave fix strategy empty (to be filled during planning)

4. Report completion with Next Steps:

```
Bug fix workflow initialized

**Branch**: [BRANCH_NAME]
**Bug ID**: [BUG_ID]
**Bug Report**: [BUG_REPORT_FILE]

**Next Steps:**
1. Review and investigate the bug
2. Update bug-report.md with root cause analysis
3. Run `/speckit.plan` to create fix plan (include regression test strategy)
4. Run `/speckit.tasks` to break down the fix into tasks
5. Run `/speckit.implement` to execute the fix

**Reminder**: Write regression test BEFORE implementing fix
```

Note: The script creates and checks out the new branch before writing files.