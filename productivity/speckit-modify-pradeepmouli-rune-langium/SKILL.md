---
name: speckit-modify
description: Modify an existing feature with impact analysis and backward compatibility
  tracking.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/modify.md
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.workflows.modify` (or `/speckit.modify`) in the triggering message can be:
- `/speckit.workflows.modify <feature-number> "modification description"` - Direct with feature number
- `/speckit.workflows.modify "modification description"` - Interactive (will prompt for feature selection)

Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below.

Given that modification request, do this:

1. Parse $ARGUMENTS to check if feature number is provided
   - If starts with 3 digits (e.g., "014 add compression"), extract feature number and description
   - If no leading digits (e.g., "add compression"), treat as description-only (interactive mode)

2. **If interactive mode** (no feature number provided):
   a. Run `.specify/extensions/workflows/scripts/bash/create-modification.sh --list-features "<description>"` to get list of features
   b. Parse the JSON output which contains: `{"mode":"list","description":"...","features":[...]}`
   c. Present the features list to the user in a clear, numbered format:
      ```
      Which feature do you want to modify?

      1. 001 - ability-for-new
      2. 002 - ability-for-users
      3. 014 - edit-profile-form
      ...

      Type the feature number (e.g., 014) or respond with the line number (e.g., 3).
      ```
   d. Wait for user response with their selection
   e. Extract the feature number from their response (handle both "014" and "3" formats)
   f. Continue to step 3 with the selected feature number

3. **Normal workflow** (feature number now available):
   Run the script `.specify/extensions/workflows/scripts/bash/create-modification.sh --json <feature-number> "<description>"` from repo root and parse its JSON output for MOD_ID, BRANCH_NAME, MOD_SPEC_FILE, IMPACT_FILE, and FEATURE_NAME. All file paths must be absolute.
   **IMPORTANT** You must only ever run this script once per feature selection. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

5. Read the impact analysis from IMPACT_FILE to understand what files and contracts are affected.

6. Load the original feature spec from `specs/<FEATURE_NAME>/spec.md` to understand the baseline.

7. Load `.specify/extensions/workflows/templates/modify/modification-template.md` to understand required sections.

8. Write the modification spec to MOD_SPEC_FILE using the template structure:
   - Fill "Why Modify?" with business justification from description
   - Fill "What's Changing?" sections (Added/Modified/Removed) based on description
   - Include impact analysis summary from IMPACT_FILE
   - Document backward compatibility considerations
   - Leave detailed implementation sections for planning phase

9. Report completion with Next Steps:

```
Modification workflow initialized

**Modification ID**: [MOD_ID]
**Original Feature**: specs/[FEATURE_NAME]
**Modification Spec**: [MOD_SPEC_FILE]
**Impact Analysis**: [IMPACT_FILE]

**Impact Summary:**
- [X] files affected
- [Y] contracts changed
- [Z] tests need updates

**Next Steps:**
1. Review modification spec and impact analysis
2. Refine requirements if needed (edit modification-spec.md)
3. Run `/speckit.plan` to create implementation plan
4. Run `/speckit.tasks` to break down into tasks
5. Run `/speckit.implement` to execute changes

**Reminder**: Consider backward compatibility and migration strategy
```

Note: The script creates and checks out the new branch, runs impact analysis, and prepares directory structure before writing.

**Interactive Mode Usage Examples**:
- User: `/speckit.workflows.modify "add avatar compression"` -> Shows feature list -> User selects -> Creates modification
- User: `/speckit.workflows.modify 014 "add avatar compression"` -> Directly creates modification for feature 014