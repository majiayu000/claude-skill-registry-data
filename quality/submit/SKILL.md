---
name: "submit"
description: "Draft and submit a vulnerability report to the bug bounty platform. Reads scope.yaml for platform/program, uses brain + findings for content. Always drafts first for review."
---

# Submit

*Sourced from h-mmer-pentest-agents*

Prepare and submit a report for finding: $ARGUMENTS

Workflow:
0. Read `rules/identities.md` to learn which env vars hold the researcher handle, email alias, and API token for the platform identified in step 1. NEVER hardcode a username or email; always reference the env-var symbol. If a required var is unset, abort with `error: <VAR> is not set; refusing to guess` and surface it to the user.
1. Read `scope.yaml` to determine the platform and program handle.
2. Read the finding details from brain/findings/poc directory matching "$ARGUMENTS".
3. Use MCP tool `draft_report` to create a platform-formatted draft:
   - Format title as: `[Vuln Type] in [Component] allows [Impact] via [Vector]`
   - Include CVSS vector string (CVSS 3.1 for HackerOne, CVSS 4.0 for all others)
   - Map vulnerability type to platform-specific taxonomy (H1 weakness IDs, Bugcrowd VRT)
   - Include all reproduction steps, impact, and remediation
4. Show the draft to the user and ASK FOR CONFIRMATION before submitting.
5. ONLY after explicit user approval, use MCP tool `submit_report` to submit.
6. After submission, update the brain: `uv run python3 ../../tools/brain.py record <target> confirmed <technique> "Submitted as report #<id> on <platform>"`
7. Update findings.json status to "reported".

IMPORTANT: NEVER submit without showing the draft and getting explicit user confirmation.

## Top-Tier Submission Discipline

Submission is a controlled release.

Before asking for approval, verify:
- `/validate` PASS or explicit accepted equivalent exists
- `/quality` score is acceptable and blocking issues are fixed
- `/dupcheck` result is included or intentionally skipped with reason
- all evidence paths exist on disk
- platform taxonomy, severity, and CVSS version match the platform
- no secrets, customer data, or prohibited artifacts are over-shared
- remediation is actionable and scoped to the root cause

Show the user the final title, severity, platform, target asset, evidence list, and any residual risk. If anything changed after draft generation, re-run quality before submission.

