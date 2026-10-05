---
tcaml_version: "1.8.1"
document_type: "skill"
skill_type: "connector"
skill_id: "local-folder-evidence-storage"
title: "Local Folder Evidence Storage Connector Skill"
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
# Local Folder Evidence Storage Connector Skill

## Purpose

Store AML case evidence in a local or network folder structure that supports audit trail, retention and reviewer access.

## When to Use

Use when the implementation profile requires local-first, network-drive or non-cloud evidence storage.

## Required Inputs

- root evidence folder;
- case identifier;
- subject name;
- check type;
- user/agent role;
- retention category if available.

## Recommended Folder Structure

```text
/cases/
  <case-id>_<subject>/
    01-inputs/
    02-source-evidence/
    03-working-notes/
    04-manual-review/
    05-final-human-decision/
```

## Workflow

1. Create or locate the case folder.
2. Store original inputs separately from source evidence.
3. Store draft working notes separately from final human decision records.
4. Add every saved file to the evidence log.
5. Preserve file versions where updates occur.
6. Do not delete earlier evidence unless the implementation profile permits it.

## Agent Must Not

- store sensitive AML evidence in an unapproved folder;
- mix final reviewer decisions with agent drafts;
- delete prior versions silently;
- expose case evidence to unauthorized channels.
