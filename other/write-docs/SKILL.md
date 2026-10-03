---
metadata:
  name: write-docs
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "functional"
  description: "Produce written knowledge artifacts: READMEs, guides, API specs, tutorials."
  when_to_use: "Use this skill when the task involves write docs"
  triggers: ["document", "write guide", "readme", "tutorial", "spec", "wiki"]
  inputs: ["source material", "target audience", "document type", "scope"]
  outputs: ["written document", "section outline", "review checklist"]
---

# Write Docs

This skill allows the agent to produce high-quality written knowledge artifacts — READMEs, guides, API specs, tutorials, runbooks, and wikis — that are clear, accurate, and audience-appropriate.

## Steps

1. **Identify the document type.** Determine what artifact is needed: README, runbook, API spec, tutorial, changelog, etc. Each has a different structural contract.
2. **Define the target audience.** Who is reading this? (e.g., a new developer, an existing agent, a business stakeholder). Audience determines vocabulary, depth, and assumed knowledge.
3. **Read the source material fresh.** Apply the Zero-Drift Audit Law — do NOT write documentation from memory. Read the actual current state of the system/code/process.
4. **Draft an outline.** Define the sections before writing prose. Get the structure right first.
5. **Write section by section.** Fill each section with accurate, concise content. Prefer examples over abstract descriptions.
6. **Apply format standards.**
   - Use semantic heading hierarchy (single H1, then H2/H3)
   - Code blocks for all commands and code
   - Tables for comparative or multi-field data
   - Alerts/callouts for warnings and critical notes
7. **Self-review.** Check: Is every statement accurate? Is anything ambiguous? Are examples runnable?
8. **Output** the final document.

## Document Type Templates

| Type | Key Sections |
|---|---|
| README | What It Does, Setup, Usage, Examples |
| Runbook | Objective, Prerequisites, Steps, Rollback |
| API Spec | Endpoint, Method, Auth, Request, Response, Errors |
| Tutorial | Goal, Prerequisites, Step-by-step, Expected Output |
| Changelog | Version, Date, Added / Changed / Fixed / Removed |

## Notes
- Documentation written without reading source material is a liability, not an asset.
- For large codebases, use the `rag` toolbox (pyragify) to pre-chunk before documenting.
