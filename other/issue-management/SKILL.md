---
name: issue-management
description: Use for GitHub Issue searches, plan saving, creation and updates, Sub-issues, follow-up requests, writing or updating Issue/PR titles and bodies, and recording common standard candidates. For planning alone, finish after saving, verifying, and presenting. Preserve execution approval and explicit endpoints when implementation is also requested. Do not use for ordinary reading, conceptual explanation, or review alone.
---

# Record Issues and plans

Own Issue plans and records. Do not reinterpret Issue creation/update or the existence of a plan as approval to execute changes. Retain execution approval from clear change requests after saving. Distinguish Git-managed file changes, which need ordinary repository delivery, from GitHub-side settings changes, which need application and readback verification within their authorized scope.

Use only the Feature → Task hierarchy for Issue decomposition; Tasks are leaves and never own Sub-issues. Before creating or linking a Sub-issue, follow [Parent Issues and Sub-issues](references/issue-recording.md#parent-issues-and-sub-issues).

## Material to read at each stage

Read only material needed for the current stage. `docs/` refers to the working repository; resolve bundled links from the referring file.

| Stage or condition | Material |
| --- | --- |
| Investigation and planning for individual changes, execution scope and additional-confirmation decisions, validation dependencies | [Planning and execution scope](references/planning.md) |
| Searching, creating, or updating Issues, Sub-issues, follow-up requests, diagnostic plans, common standard candidates | [Recording and presenting Issues](references/issue-recording.md) |
| Writing or updating Issue/PR titles and bodies | [Writing Issues and PRs](references/github-writing.md) |
| Posting or updating Issue/PR bodies or comments, or deciding/presenting concrete procedures for them | [Markdown quality for GitHub](references/markdown-quality.md) |

## Stopping and handoff after recording

- Check necessary publication permission and formatting before posting or updating Issue bodies. Preserve original content, reasons, and requester, and after saving retrieve the body to check agreement and rendering, and confirm the URL. Do not claim unperformed posting or checks in simulated evaluations.
- For planning/diagnosis requests whose terminal deliverable is an Issue record only, present the saved Issue body and URL, then stop. For diagnoses ending in an answer, do not implicitly create Issues. When both Issue recording and implementation are requested, use the ordinary planning path and hand off to implementation after saving. Do not proceed from Issue-record-only requests to implementation, branch preparation, PRs, or formulaic implementation-approval questions, or automatically close the Issue.
- With approval to change Git-managed files, proceed after saving and verifying the plan through branch preparation, implementation, PR, required CI and conflict resolution on current HEAD, ordinary review of that HEAD, permitted merge, actual-main verification, synchronization, and branch cleanup. Protect other sessions' work and preserve the target's review and merge conditions; changed HEAD requires new checks and review. Do not repeatedly reapprove procedure changes within the same purpose and success conditions; when changing purpose, outcomes, acceptance conditions, external impact, or authority, follow the planning material's boundaries for confirmation.
- With approval to apply only GitHub-side repository settings, apply the authorized differences after the same plan saving and verification, retrieve settings, and diagnose again. Do not create empty commits or PRs. Hold affected operations when required access is unavailable, and deliver prerequisite file changes through the ordinary repository process.
- In consultation or review requesting only common standard candidate records, do not expand Issue recording into change-plan or delivery approval. Obtain explicit permission for the posting destination and draft when publishing unpublished decisions or material.
