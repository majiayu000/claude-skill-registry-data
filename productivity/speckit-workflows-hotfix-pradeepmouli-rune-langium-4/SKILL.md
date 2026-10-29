---
name: speckit-workflows-hotfix
description: Create an emergency hotfix workflow with expedited process and mandatory
  post-mortem.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:workflows
---

# Workflows Hotfix Skill

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.workflows.hotfix` (or `/speckit.hotfix`) in the triggering message **is** the incident description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

**EMERGENCY WORKFLOW - EXPEDITED PROCESS**

Given that incident description, do this:

1. Run the script `.specify/extensions/workflows/scripts/bash/create-hotfix.sh --json "$ARGUMENTS"` from repo root and parse its JSON output for HOTFIX_ID, BRANCH_NAME, HOTFIX_FILE, POSTMORTEM_FILE, and TIMESTAMP. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

2. Load `.specify/extensions/workflows/templates/hotfix/hotfix-template.md` to understand required sections.

3. Write the hotfix incident log to HOTFIX_FILE using the template structure:
   - Fill incident timeline with TIMESTAMP from script output
   - Assess severity from description (P0 = service down, P1 = major feature broken, P2 = workaround available)
   - Describe the incident clearly
   - Leave "Immediate Fix Applied" section empty (to be filled during planning)
   - Leave root cause analysis preliminary (to be refined)
   - Document impact assessment from description

4. Report completion with Next Steps:

```
HOTFIX WORKFLOW INITIATED (EXPEDITED)

**Hotfix ID**: [HOTFIX_ID]
**Branch**: [BRANCH_NAME]
**Incident Time**: [TIMESTAMP]
**Severity**: [P0/P1/P2]
**Hotfix Report**: [HOTFIX_FILE]

**Next Steps (URGENT):**
1. Review incident details and confirm severity
2. Notify stakeholders of incident status
3. Run `/speckit.plan` to create expedited fix plan
4. Run `/speckit.tasks` to create minimal task breakdown
5. Run `/speckit.implement` to apply hotfix immediately

**Post-Deployment:**
- Monitor production after deployment
- Schedule post-mortem within 24-48 hours
- Create follow-up `/speckit.bugfix` for proper fix with tests

**Note**: This is the ONLY workflow that permits test-after approach due to emergency
```

Note: Hotfix workflow bypasses normal TDD process due to emergency nature. Tests must be added AFTER fix is deployed. This is the ONLY workflow that permits this deviation from the constitution.
