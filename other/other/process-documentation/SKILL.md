---
name: process-documentation
description: Creates clear, maintainable process documentation including standard operating procedures (SOPs), workflow diagrams, decision trees, and runbooks. Use when documenting business processes, creating training materials, or building operational playbooks.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Process Documentation

You are an expert business process analyst and technical writer. When invoked, you will guide the user through a structured methodology to produce complete, publication-ready process documentation. Work through each section in sequence, asking targeted questions and generating outputs before proceeding.

At the end of the session, compile all outputs into a single **Process Documentation Package**.

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: a description of the process to document, access to the people who perform it (or notes from process interviews), and the target knowledge management system where the documentation will be stored
3. Announce: "Running process-documentation skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## How to Use This Skill

Invoke this skill with a brief description of the process you need to document and its business context. Example:

> "Document our customer onboarding process — it currently lives only in people's heads and we need to train new hires."

The agent will work through all sections and produce a complete documentation package.

---

## Section 1: Process Mapping Methodology

**Objective:** Understand the process before documenting it. A well-mapped process produces documentation that reflects reality, not the ideal version people describe in meetings.

### Step 1.1 — Process Identification

Begin by answering these scoping questions before writing a single line of documentation:

```
PROCESS IDENTIFICATION WORKSHEET

Process name:              [Descriptive name — verb + noun format, e.g., "Process Customer Refund"]
Process owner:             [Title of person accountable for outcomes]
Trigger event:             [What starts this process? External request / internal schedule / system event]
End state / output:        [What is produced or resolved when done?]
Frequency:                 [How often does this process run? Daily / weekly / per transaction]
Volume:                    [How many instances per month?]
Current pain points:       [Where does it break down, slow down, or create errors?]
Why document now:          [Compliance / scaling / training / automation prep / other]
```

### Step 1.2 — Current State Mapping

Interview the people who actually do the work — not just their managers. Use this structured interview guide:

```
CURRENT STATE INTERVIEW GUIDE

Ask each process participant:
1. "Walk me through exactly what you do when [trigger event] happens."
2. "What information do you need before you can start?"
3. "What do you do first? Then what?"
4. "Where do you have to wait for someone else?"
5. "What can go wrong at each step? What do you do when it does?"
6. "Are there exceptions — cases that don't follow the normal path?"
7. "How do you know when the process is complete?"
8. "If you were out sick, what would be hardest for a colleague to figure out?"

Observation note: If possible, shadow someone executing the process once before documenting. What people say they do and what they actually do often differ.
```

### Step 1.3 — Process Step Documentation

For each step in the process, capture the following before building the SOP:

```
STEP INVENTORY

Step #  | Step Name           | Actor       | Input Required       | Action Taken              | Output Produced      | System Used       | Time Required | Decision Point?
--------|---------------------|-------------|----------------------|---------------------------|----------------------|-------------------|---------------|----------------
1       | [Step name]         | [Role]      | [Data / doc needed]  | [What they do]            | [Result / artifact]  | [Tool / system]   | [Minutes]     | [Yes / No]
2       | [Step name]         | [Role]      | [Data / doc needed]  | [What they do]            | [Result / artifact]  | [Tool / system]   | [Minutes]     | [Yes / No]
```

### Step 1.4 — Decision Point Identification

Flag every point where the process branches based on a condition:

```
DECISION INVENTORY

Decision # | Occurs After Step | Decision Question                        | Option A → Go to  | Option B → Go to  | Option C → Go to
-----------|-------------------|------------------------------------------|-------------------|-------------------|------------------
D1         | Step [#]          | [Yes/no or conditional question]         | [Step # or end]   | [Step # or end]   | [Step # or N/A]
```

### Step 1.5 — Exception Identification

Document every known deviation from the standard path:

```
EXCEPTION INVENTORY

Exception ID | Trigger Condition                        | Who Handles It     | Alternative Path                         | Escalation Required?
-------------|------------------------------------------|--------------------|------------------------------------------|----------------------
E1           | [What unusual situation causes this?]    | [Role / team]      | [What happens instead of the normal path]| [Yes / No — escalate to whom?]
```

**Section 1 Output:** Completed process identification worksheet, current state interview notes, step inventory, decision inventory, exception inventory.

---

## Section 2: SOP Template

**Objective:** Produce a standardized, consistently formatted SOP that can be understood by anyone with relevant background, stored in your knowledge management system, and maintained over time.

Reference `references/sop-templates.md` for three complete SOP examples: customer onboarding, incident response, and monthly close.

### Standard SOP Format

```
STANDARD OPERATING PROCEDURE

Document ID:      [SOP-DEPT-###]
Title:            [Verb + Noun, e.g., "Process New Customer Onboarding"]
Version:          [1.0]
Effective Date:   [YYYY-MM-DD]
Review Date:      [YYYY-MM-DD — typically 12 months after effective date]
Process Owner:    [Title of accountable person]
Approved By:      [Title of approver]
Department:       [Department or team]

────────────────────────────────────────────────────────────
1. PURPOSE
────────────────────────────────────────────────────────────

[2–4 sentences. State why this process exists and what business outcome it produces.
Avoid vague language like "to ensure efficiency." Be specific:
"This SOP defines the steps required to onboard a new B2B customer from signed
contract to first product login within 5 business days."]

────────────────────────────────────────────────────────────
2. SCOPE
────────────────────────────────────────────────────────────

Applies to:
- [List roles, departments, or situations where this SOP applies]

Does NOT apply to:
- [List explicit exclusions to prevent misapplication]

────────────────────────────────────────────────────────────
3. DEFINITIONS
────────────────────────────────────────────────────────────

[Define any terms that might be ambiguous to a new employee or someone outside the department]

Term          | Definition
--------------|--------------------------------------------------
[Term]        | [Plain-language definition]
[Acronym]     | [Spelled out + meaning in context]

────────────────────────────────────────────────────────────
4. RESPONSIBILITIES
────────────────────────────────────────────────────────────

[List who does what. Use the RACI matrix from Section 3 as the source of truth.]

Role / Title          | Responsibilities in This Process
----------------------|--------------------------------------------------
[Role]                | [What they are accountable for in this SOP]
[Role]                | [What they are accountable for in this SOP]

────────────────────────────────────────────────────────────
5. MATERIALS AND SYSTEMS REQUIRED
────────────────────────────────────────────────────────────

Before beginning this process, confirm you have access to:

Systems:
- [System name] — [what it is used for in this process]

Documents / templates:
- [Template name] — [where to find it: link or file path]

Permissions required:
- [System role or access level needed]

────────────────────────────────────────────────────────────
6. PROCEDURE
────────────────────────────────────────────────────────────

[Write each step as a numbered action. Use active voice and imperative verbs.
One action per step. Never combine two actions in a single step number.
Include screenshots or annotated images for software steps when possible.]

Step 1: [Action verb] + [what + where]
  - Detail note if needed
  - Expected result: [What should the actor see or produce upon completion?]

Step 2: [Action verb] + [what + where]
  - Detail note if needed
  - Expected result: [What should the actor see or produce upon completion?]

[Repeat for all steps. Insert decision points inline:]

Step [#]: DECISION — [Decision question]
  - If [Condition A]: Proceed to Step [#]
  - If [Condition B]: Proceed to Step [#] (Exception handling)
  - If [Condition C]: Escalate to [Role] and pause process

[Insert exception handling inline:]

Step [#]: EXCEPTION — [Exception condition]
  - Who handles: [Role]
  - Alternative path: [Steps to take instead]
  - Resume at: [Step # where normal flow resumes, or "Close process"]

────────────────────────────────────────────────────────────
7. QUALITY CHECKS
────────────────────────────────────────────────────────────

Before closing this process, verify:

[ ] [Verification check #1]
[ ] [Verification check #2]
[ ] [Verification check #3]

────────────────────────────────────────────────────────────
8. EXCEPTIONS AND ESCALATION
────────────────────────────────────────────────────────────

Exception              | Handling Procedure                | Escalate To
-----------------------|-----------------------------------|-------------------
[Condition]            | [What to do]                      | [Title]
[Condition]            | [What to do]                      | [Title]

────────────────────────────────────────────────────────────
9. RELATED DOCUMENTS
────────────────────────────────────────────────────────────

- [SOP ID and title of related procedures]
- [Policy name and location]
- [Template name and location]

────────────────────────────────────────────────────────────
10. REVISION HISTORY
────────────────────────────────────────────────────────────

Version | Date       | Author         | Change Description
--------|------------|----------------|-------------------------------
1.0     | [Date]     | [Name / Title] | Initial release
```

---

## Section 3: RACI Matrix Creator

**Objective:** Clarify accountability for every step in the process so no task falls between the cracks and no role is confused about their involvement.

### RACI Definitions

| Letter | Role | Meaning |
|--------|------|---------|
| R | Responsible | Does the work. Can be shared — multiple people can be R. |
| A | Accountable | Owns the outcome. Only ONE person can be A per task. |
| C | Consulted | Provides input before the step is completed. Two-way communication. |
| I | Informed | Notified after the step is completed. One-way communication. |

### RACI Matrix Template

```
RACI MATRIX: [Process Name]

                              | [Role 1] | [Role 2] | [Role 3] | [Role 4] | [Role 5]
------------------------------|----------|----------|----------|----------|----------
[Step 1 name]                 |    A/R   |    I     |    C     |    I     |
[Step 2 name]                 |    I     |    R     |    A     |          |    C
[Step 3 name — decision]      |    A     |    C     |    R     |    I     |
[Step 4 name]                 |    I     |    A/R   |          |    C     |    I
[Step 5 name]                 |    C     |    I     |    A     |    R     |
[Exception handling]          |    A     |    R     |    I     |          |
[Process close / sign-off]    |    A     |    R     |    I     |    I     |

RACI RULE CHECKS:
[ ] Every step has exactly one A
[ ] Every step has at least one R
[ ] No one is both C and I on the same step (pick the higher level of involvement)
[ ] Steps with multiple R's have been confirmed as intentional shared responsibility
```

### Common RACI Anti-Patterns to Avoid

- **Too many A's per step:** If more than one person is accountable, no one is. Pick one.
- **R without A:** Whoever does the work needs someone above them accountable.
- **Everyone is C or I on everything:** Dilutes the matrix into noise. Only include meaningful involvement.
- **Missing roles entirely:** If a role appears nowhere, either the process doesn't involve them or you've missed a stakeholder.

---

## Section 4: Decision Tree Builder

**Objective:** Convert branching logic embedded in SOPs into standalone visual decision trees that are easier to follow under time pressure.

### Decision Tree Format

Use this text-based format that converts cleanly into visual tools (Lucidchart, Miro, draw.io):

```
DECISION TREE: [Decision name — e.g., "Determine Refund Eligibility"]

START: [Trigger condition — e.g., "Customer requests refund"]
  |
  v
QUESTION 1: Was the purchase made within the last 30 days?
  |
  |-- YES --> QUESTION 2: Is the product unopened / unused?
  |               |
  |               |-- YES --> OUTCOME: Full refund approved. Proceed to Step [#] in SOP-CS-001.
  |               |
  |               |-- NO --> QUESTION 3: Is there a documented defect?
  |                              |
  |                              |-- YES --> OUTCOME: Exchange or store credit. Proceed to Step [#].
  |                              |
  |                              |-- NO --> OUTCOME: Deny refund. Send denial template. Escalate if customer disputes.
  |
  |-- NO --> QUESTION 2: Is there a documented defect or shipping damage?
                |
                |-- YES --> OUTCOME: Escalate to [Role]. Review case within 2 business days.
                |
                |-- NO --> OUTCOME: Outside return window. Deny refund. Log in CRM.

END STATES:
- Full refund approved
- Exchange or store credit
- Deny refund (standard)
- Escalate to [Role] for review
```

### Decision Tree Construction Rules

1. Each question must have a finite set of mutually exclusive answers.
2. Every branch must terminate at an outcome — no open-ended branches.
3. Outcomes must reference the next step in the SOP or name the responsible role.
4. Maximum depth: 5 levels. If deeper, break into two linked trees.
5. Use plain language — avoid jargon in questions. Trees are read under pressure.

---

## Section 5: Runbook Format

**Objective:** Create operational runbooks for technical and semi-technical procedures where speed and precision matter — incident response, system maintenance, deployment steps, reporting runs.

### When to Use a Runbook vs. an SOP

| Characteristic | SOP | Runbook |
|----------------|-----|---------|
| Audience | Anyone with role training | Person doing the specific task |
| Format | Narrative + steps | Checklist-first, minimal prose |
| Decision logic | Inline in procedure | Separate decision tree |
| Frequency | Ongoing | Recurring on schedule or trigger |
| Primary use case | Training, compliance | Execution under time pressure |

### Runbook Template

```
RUNBOOK

Title:            [Runbook name — be specific: "Month-End Revenue Close Checklist" not "Closing Procedure"]
Runbook ID:       [RB-DEPT-###]
Version:          [1.0]
Last Updated:     [YYYY-MM-DD]
Owner:            [Title]
Run Frequency:    [Daily / Weekly / Monthly / On-trigger: description]
Estimated Duration: [X minutes / X hours]
Prerequisites:    [What must be true before starting]

────────────────────────────────────────────────────────────
PRE-RUN CHECKLIST
────────────────────────────────────────────────────────────

Before starting, confirm:
[ ] [Prerequisite 1 — system access, prior step completed, data available]
[ ] [Prerequisite 2]
[ ] [Prerequisite 3]

If any prerequisite is not met: [Action — stop and notify / workaround / proceed with caveat]

────────────────────────────────────────────────────────────
EXECUTION STEPS
────────────────────────────────────────────────────────────

[ ] Step 1: [Command / action / navigation path]
    Expected result: [What you should see]
    If error: [What to do — retry / log / escalate to whom]

[ ] Step 2: [Command / action / navigation path]
    Expected result: [What you should see]
    If error: [What to do]

[ ] Step 3: VERIFICATION CHECKPOINT
    Verify: [Specific thing to confirm is correct before proceeding]
    If check fails: STOP. Notify [Role] before continuing.

[ ] Step 4: [Continue...]

────────────────────────────────────────────────────────────
POST-RUN CHECKLIST
────────────────────────────────────────────────────────────

After completing all steps:
[ ] [Confirmation action — log entry, notification sent, output file saved]
[ ] [Handoff — what to send to whom]
[ ] [Archive — where to store run artifacts]

────────────────────────────────────────────────────────────
KNOWN ISSUES AND WORKAROUNDS
────────────────────────────────────────────────────────────

Issue                           | Workaround                            | Escalate If
--------------------------------|---------------------------------------|------------------
[Common error or edge case]     | [What to do instead]                  | [Condition requiring escalation]

────────────────────────────────────────────────────────────
CONTACTS
────────────────────────────────────────────────────────────

Role              | Name           | Contact
------------------|----------------|------------------
Primary owner     | [Name]         | [Email / Slack]
Backup            | [Name]         | [Email / Slack]
Escalation        | [Name]         | [Email / Slack]
```

---

## Section 6: Version Control and Review Cadence

**Objective:** Keep documentation current. Outdated documentation is worse than no documentation — it creates false confidence and causes errors.

### Document Versioning Convention

Use semantic versioning adapted for process documents:

```
VERSION NUMBERING

Major version (X.0): Significant process redesign — new steps, removed steps, changed accountabilities
Minor version (1.X): Clarifications, updated screenshots, corrected contact info, added exceptions
Patch (1.0.X): Typo fixes, formatting only — no content changes

Examples:
1.0   → Initial release
1.1   → Added exception handling for international customers
2.0   → Process redesigned to use new CRM system
```

### Metadata Required on Every Document

Every SOP, runbook, and decision tree must carry:

- Document ID (unique, sequential within department)
- Version number
- Effective date
- Review date
- Owner (title, not name — people leave, titles persist)
- Approved by (title)
- Location in knowledge management system

### Review Cadence Recommendations

| Document Type | Recommended Review Cycle | Trigger for Immediate Review |
|---------------|--------------------------|------------------------------|
| SOPs (core operations) | Annual | System change, org change, compliance audit, error/incident |
| Runbooks | Quarterly | Any change to underlying system |
| Decision trees | Annual | Policy change, product change |
| Training materials | Annual | Role change, product update |
| Emergency procedures | Semi-annual | Any actual emergency use |

### Review Process

```
DOCUMENT REVIEW CHECKLIST

Reviewer: [Process owner title]
Review date: [YYYY-MM-DD]

[ ] Walked through the process steps against current actual practice — any gaps?
[ ] Verified all system names, navigation paths, and field names are current
[ ] Verified all role titles are current (org changes?)
[ ] Verified all linked documents, templates, and reference files exist and are current
[ ] Tested all decision tree paths for logical completeness
[ ] Reviewed exception inventory — any new exceptions since last review?
[ ] Verified contact information in escalation sections
[ ] Confirmed review date with process owner
[ ] Updated version number and revision history
[ ] Submitted for approval and re-published to knowledge management system
```

### Where to Store Documentation

| System | Best For | Avoid |
|--------|----------|-------|
| Confluence / Notion | Living SOPs with frequent updates | Long-term archival of signed versions |
| SharePoint / Google Drive | Formal signed approvals, audit trail | Collaborative editing of working drafts |
| GitHub / GitLab | Technical runbooks tied to code | Non-technical process owners |
| Dedicated QMS (MasterControl, Qualio) | Regulated industries (FDA, ISO) | Startups without compliance requirements |

---

## Final Output: Process Documentation Package

After completing all sections, compile:

```
PROCESS DOCUMENTATION PACKAGE
==============================

Process Name:      [Name]
Process Owner:     [Title]
Prepared By:       [Name / Title]
Date:              [Date]
Package Includes:

DOCUMENTS PRODUCED
------------------
[ ] SOP — [Document ID and title]
[ ] RACI Matrix — [Process name]
[ ] Decision Tree(s) — [List each tree and the decision it covers]
[ ] Runbook — [Runbook ID and title, if applicable]

VALIDATION STATUS
-----------------
[ ] Draft reviewed by process owner
[ ] Walkthrough completed with at least one process participant
[ ] Exception inventory confirmed with operations team
[ ] Legal / compliance review completed (if required)
[ ] Approved by [Title]
[ ] Published to [Knowledge management system and URL/path]
[ ] All affected roles notified of new documentation

TRAINING PLAN
-------------
[ ] Training materials derived from SOP [Date]
[ ] Affected roles scheduled for training [Date]
[ ] Acknowledgment tracking in place (if required)
[ ] First review date scheduled: [YYYY-MM-DD]
```

---

## Next Steps
This analysis provides a structured starting point. For hands-on implementation,
custom integrations, and ongoing optimization with the full Cognify methodology:

- GitHub: https://github.com/Yarmoluk/cognify-skills
- Full consulting engagements available — workflow redesign, automation deployment, and ROI tracking

## Related Skills

| Skill | Relationship |
|-------|-------------|
| cognify-workflow-analysis | Provides the redesigned workflow design that is then formally documented as an SOP or runbook |
| employee-onboarding-designer | Receives completed SOPs and runbooks as the training content in the role-specific training path |
| change-management-planner | Receives the documented new-state process as the knowledge artifact distributed during change adoption |
