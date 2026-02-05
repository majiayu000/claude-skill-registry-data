---
name: change-request-builder
description: Creates comprehensive ServiceNow change request documentation when users request CR creation, need to generate change requests, ask to prepare deployment documentation, or mention creating release documentation. Automatically analyzes git history, queries functional requirements from BigQuery, generates technical change summaries, and creates properly formatted YAML files for L'Oréal BTDP deployments.
---

# Change Request Generation

When you are requested to create the content of a change request, follow this systematic process:

**IMPORTANT**: All git operations below must be executed in the project's git directory located at `../{template_name}/`, if the user does not mention it, ask them to specify the template

**NOTE**: Before starting the process, ensure that both `develop` and `master` branches are up to date with their remote counterparts.

## Step 1: Branch Synchronization

```bash
# Navigate to the project's git directory (in parent folder)
cd ../{template_name}/

# Ensure both branches are up to date
git checkout master
git pull origin master
git checkout develop
git pull origin develop
```

## Step 2: Identify Last Merge Commit

```bash
# Find the last merge commit on master to establish diff baseline
git log --oneline --merges master -1
```

**IMPORTANT**: After identifying the last merge commit, extract the sprint and MEP numbers from it, then **ASK the user to confirm** the sprint and MEP numbers for this new release. The last merge shows the previous release numbers, so you can suggest incrementing the MEP number, but always let the user confirm or provide different numbers.

Example:
- Last merge shows: SPRINT 18 MEP 1
- Suggest to user: "I see the last release was Sprint 18 MEP 1. Should this new release be Sprint 18 MEP 2, or different sprint/MEP numbers?"
- Wait for user confirmation before proceeding

## Step 3: Get Commit History Diff

```bash
# Get commits between master and develop since last merge
git log --oneline master..develop --reverse
```

## Step 4: Extract Story Numbers

Extract all story numbers (STRYXXXXXXX format) from the commit history for functional requirements lookup.

## Step 5: Query Functional Requirements

Use the BigQuery command with extracted story numbers:

```bash
bq query --use_legacy_sql=false --project_id=itg-housekeeping-dv "
SELECT
  number,
  short_description,
  description,
  epic_sk
FROM
  \`itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.story_v1\`
WHERE
  number IN ('STRY0000000', 'STRY0000001', ...)
ORDER BY number
"
```

## Step 6: Analyze Technical Changes

Review all modified files using:

```bash
# Get list of changed files between branches
git diff --name-status master..develop
```

## Step 7: Query Epic Information

Using the `epic_sk` values retrieved from Step 5, query the epic details from BigQuery:

```bash
bq query --use_legacy_sql=false --project_id=itg-housekeeping-dv "
SELECT
  number,
  short_description
FROM
  \`itg-btdppublished-gbl-ww-pd.btdp_ds_c1_054_agile_eu_pd.epic_v1\`
WHERE
  sys_id IN ('epic_sk_value_1', 'epic_sk_value_2', ...)
ORDER BY number
"
```

**Note**: Use the `epic_sk` values from the story query (Step 5) as the `sys_id` filter in this query.

## Step 8: Change Request Template Selection

1. **Ask for Required Information**: The user MUST provide:
   - Template name (e.g., "btdplogs", "housekeeping")
   - Change request number (format: CHG0012345)
   - Release number (format: RLSE0027806)
   - Planned start date (format: 2025-10-23 14:52:32)
     * If user doesn't provide time, default to 12:00:00 (noon)
   - Planned end date (format: 2025-10-23 14:52:32)
     * If user doesn't provide time, default to 12:00:00 (noon)
   - **Sprint and MEP numbers**: After analyzing the git history (Step 2), suggest sprint/MEP numbers based on the last merge and ask for user confirmation before proceeding

2. **Retrieve Template**: Load the template from `.claude/skills/change-request-builder/templates/{template_name}.yaml`

3. **Check for Template Inheritance**:
   - If the selected template starts with `# Heritated from template`, it is a child template that inherits from a base template
   - In this case:
     1. Read the base template name specified after `# Heritated from template`
     2. Load the base template from `.claude/skills/change-request-builder/templates/{base_template_name}.yaml`
     3. Use the base template as the starting point
     4. Override/merge fields from the base template with the fields defined in the selected (child) template
     5. The child template fields take precedence over base template fields

4. **Get Project Name**: Ask the user for the project name if not already provided

5. **Pre-fill Form**: Use the gathered information from previous steps to populate ONLY the empty fields

6. **Create Output File**: Save the pre-filled form to `output/change_requests/{template}_{change_request_number}.yaml`

## CRITICAL RULES

- **NEVER overwrite the original template** - always create a new file in the output directory
- **NEVER replace non-empty fields** - only fill in fields that are empty in the template
- **ALWAYS preserve** pre-existing values, formatting, and structure from the template
- Output file naming format: `{template_name}_{change_request_number}.yaml`
- Output file location: `output/change_requests/` from the root directory

## Field Formatting Requirements

- **Release Short description format**: `[<TEMPLATE NAME>]SPRINT <x> MEP <x>` (ALL CAPS)
  - Example: `[BTDPLOGS]SPRINT 42 MEP 3`
  - Template name should be in uppercase and match the template file name (btdplogs, housekeeping, etc.)
  - Sprint and MEP numbers are derived from the release number provided by the user

- **Release Description**: Should contain two sections:
  1. **Global description**: A summary of all updates being deployed in this release
     - Include functional requirements from BigQuery (story descriptions)
     - Provide context about what is being deployed
  2. **Commits list**: Raw list of commits from `git log --oneline master..develop --reverse`
     - Include the complete commit history as-is
     - Format: commit hash followed by commit message

- **Change Request Short description**: A brief summary (~15 words) describing the nature of the changes
  - Example: "Deployment of excessive roles, dashboard industrializations and refactoring of contacts"
  - Should concisely capture the main purpose/scope of the change
  - Focus on what is being deployed/changed, not technical details

- **Description content**: Populated with the comprehensive analysis from Steps 1-7:
  - Summary of commits between master and develop
  - Epic information extracted from BigQuery (epic numbers and short descriptions)
  - Functional requirements extracted from BigQuery (story numbers and descriptions)
  - Technical changes analysis (grouped by functionality, not exhaustive file listings)
  - Business value and impact assessment

## Available Templates

- **btdplogs**: For BTDP Security Services changes
- **housekeeping**: For housekeeping related changes
- Additional templates may be added to the `.claude/skills/change-request-builder/templates/` directory

## Template Inheritance

Templates can inherit from other templates for reusability:
- A template that starts with `# Heritated from template {base_template_name}` will inherit all fields from the base template
- Fields defined in the child template override the corresponding fields in the base template
- This allows creating specialized templates without duplicating common fields
- Example: A template starting with `# Heritated from template btdplogs` will use btdplogs as base and override only specified fields

## Project Git Directories

- The git repositories for each project/template are located in the **parent folder** of this directory
- For a template named `{template_name}`, the git repository is at: `../{template_name}/` (or nearby name)
- Example: For "btdplogs" template, the git repository is at `../btdplogs/` (list all directory to be sure but it can be btdp-logs or something like)
- All git operations (checkout, pull, log, diff) must be executed in the respective project's git directory

## Template Usage

- Each template corresponds to a specific project/service type
- The project name helps identify which template file to use
- All templates are located in: `.claude/skills/change-request-builder/templates/{project_name}.yaml`
- Pre-fill **ONLY empty fields** in the template with:
  - **Number**: Change request number (provided by user)
  - **Short description**: `[<Template name>]SPRINT <x> MEP <x>` (using sprint and MEP from release number)
  - **Description**: Result from the "Process Steps To Determine The Description And Short Description" section (commits analysis, functional requirements, technical changes)
  - **Release**: Release number (provided by user)
  - Story numbers and functional requirements from BigQuery
  - Technical changes grouped by functionality
  - Implementation/test/backout plans based on the changes

## Output File Details

- **Directory**: `output/change_requests/` (from root directory)
- **Filename Format**: `{template_name}_{change_request_number}.yaml`
- **Example**: For template "btdplogs" with change request "CHG0012345", create:
  - `output/change_requests/btdplogs_CHG0012345.yaml`

## Post-Creation Steps

After creating the change request file, ALWAYS perform these steps automatically:

**Branch Naming Format**: `mep/<CHGXXXXXX>/sprint-<x>-mep-<x>`

**Step 1: Create Release Branch in Source Project**
Navigate to the source project directory and create the release branch from develop:
```bash
cd ../{template_name}/ && git checkout -b mep/CHG0012345/sprint-18-mep-2
```

**Step 2: Push Branch to Remote Repository**
Push the newly created branch to the remote repository:
```bash
cd ../{template_name}/ && git push -u origin mep/CHG0012345/sprint-18-mep-2
```

**Branch Naming Convention**:
- `<CHGXXXXXX>` is the change request number (e.g., CHG0012345)
- `sprint-<x>` is the sprint number extracted from the release description
- `mep-<x>` is the MEP number extracted from the release description

The sprint and MEP numbers should match those used in the Release Short description field.

**Important Notes**:
- The branch is created from the current branch (develop) in the source project
- The branch is automatically pushed to remote with upstream tracking (-u flag)
- Inform the user of the branch name and that it has been pushed to the repository

## Summary

[Brief summary of the overall change scope and impact - MAXIMUM TWO LINES]

## Execution Checklist

- [ ] User provided template name (btdplogs, housekeeping, etc.)
- [ ] User provided change request number (e.g., CHG0012345)
- [ ] User provided release number
- [ ] User provided planned start and end dates
- [ ] Project name identified from user request
- [ ] Template file loaded from `.claude/skills/change-request-builder/templates/{project_name}.yaml`
- [ ] Output directory verified/created: `output/change_requests/`
- [ ] Navigate to project git directory: `../{template_name}/`
- [ ] Branch synchronization completed (in project git directory)
- [ ] Last merge commit identified (in project git directory)
- [ ] Sprint and MEP numbers suggested to user based on last merge
- [ ] User confirmed sprint and MEP numbers for this release
- [ ] Commit diff history retrieved (in project git directory)
- [ ] Story numbers extracted from commits
- [ ] Functional requirements queried from BigQuery
- [ ] Epic information queried from BigQuery using epic_sk values
- [ ] Technical changes analyzed and categorized
- [ ] Template pre-filled with gathered information (ONLY empty fields)
- [ ] Output file created at `output/change_requests/{template}_{change_request_number}.yaml`
- [ ] Original template remains unchanged
- [ ] Release branch created in source project (in project git directory)
- [ ] Release branch pushed to remote repository with upstream tracking

## Notes

- Replace placeholder story numbers with actual extracted numbers
- Ensure BigQuery query uses correct project (itg-housekeeping-dv)
- **SUMMARIZE functional requirements**: Do not copy BigQuery results verbatim - provide clear business context and group related stories
- **SUMMARIZE technical changes**: Do not list every file - group related changes by functionality and explain overall impact
- Focus on business value and technical impact rather than exhaustive file listings
- Include full commit history since last master merge
