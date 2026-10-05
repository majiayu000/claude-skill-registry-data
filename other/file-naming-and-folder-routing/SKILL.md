---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "connector"
skill_id: "file-naming-and-folder-routing"
title: "File Naming and Folder Routing Connector Skill"
risk_area:
  - evidence
human_review_required: true
final_decision_allowed: false
paid_source_boundary: false
source_access_required: "not_applicable"
private_configuration_required_for:
  - client-specific Implementation Profiles
  - private source configuration
  - evidence rules
  - MLRO escalation logic
---
# File Naming and Folder Routing Connector Skill

## Purpose

Apply consistent file names and folder routing rules for AML evidence and draft reports.

## When to Use

Use whenever an agent saves a screenshot, PDF, report draft, checklist, source record or manual review package.

## Naming Pattern

Use the selected implementation profile. If no profile exists, use:

```text
<case-id>_<subject>_<source>_<check-type>_<YYYYMMDD>.<ext>
```

For source records with a source case ID:

```text
<case-id>_<subject>_<source>_<source-case-id>_<YYYYMMDD>.<ext>
```

## Workflow

1. Normalize the subject name without changing legal meaning.
2. Select the source and check type.
3. Add date in `YYYYMMDD` format unless the implementation profile specifies otherwise.
4. Avoid special characters that break file systems.
5. Save into the correct case subfolder.
6. Record the file path in the evidence log.

## Agent Must Not

- use names that expose unnecessary sensitive data;
- overwrite a file without versioning;
- create ambiguous names such as `final.pdf` or `report.pdf`;
- route evidence to personal folders unless policy allows it.
