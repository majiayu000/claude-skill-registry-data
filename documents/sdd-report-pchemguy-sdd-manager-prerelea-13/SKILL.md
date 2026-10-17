---
name: sdd-report
description: Use when drafting a task issue, Git commit message, pull request description, or evidence-backed task, milestone, phase or final implementation report, review/revision campaign plan or report, package preparation result, curated Git release highlights, release notes or release outcome for an SDD project. Adapt the summary to feature, bug, code health, performance, security, testing, documentation, integration, or compatibility work without inventing results.
---

# Report SDD work

For Markdown output or document work within this skill's scope, apply the shared [Markdown style](../sdd-conventions/references/markdown-style.md): blank lines after headings and around top-level lists and code blocks, plus four-space structural indentation, including nested lists, with exactly one space after each list marker. This applies to direct calls as well as coordinated work; it does not expand editing or review authority.

Choose the requested output and load only its reference:

| Output | Load |
| --- | --- |
| First SDD commit disclosure/usage evidence (drafting only) | **sdd-manage**: `skills/sdd-manage/references/repository-bootstrap.md` (bundled dependency) |
| Planned task issue title and body, task/amendment or merge commit message, or pull request draft | [drafts for hosted and Git objects](references/object-drafts.md) |
| Task, milestone, phase, final implementation, branch boundary, or interrupted-work status report | [completion reports](references/completion-reports.md) |
| Package/workflow preparation, Git release highlights, release notes or release outcomes | [package and release reporting](references/releases.md) |
| Adjacent SPEC/PLAN/TASKS preparation QC reports and appended correction/recheck sections | [document QC reports](references/document-qc-reports.md) |
| Review plan/report or revision plan/report, including focused prompt-driven review | [campaign artifacts](references/campaign-artifacts.md) |
| Kind-specific emphasis and reusable What, Why, Verification, Result patterns | [change kinds](references/change-kinds.md) |

Use the owning TASKS or active FEATURE-TASKS entry, applicable design, SPEC, PLAN, and layout, actual changes, verification output, and Git evidence appropriate to the requested output. Obtain hosted issue references from **sdd-forge** when available; a guessed issue number is never acceptable. Separate *planned*, *performed*, *verified*, and *blocked* statements. State missing or limited evidence plainly; do not turn an example, unchecked task, or intended benchmark into a completed result. Follow project-specific title and reporting conventions where they exist.

Compose only the requested text or structured draft. Keep a concise shared core of **What**, **Why**, **Verification**, and **Result**, varying the labels and optional sections to suit the actual change. For a planned issue, Verification is an acceptance or check plan and Result is an intended outcome, not a completed claim. Emoji labels are optional presentation, not required metadata.

Task-associated subjects must begin with exactly one owning `[<task-id>]` marker and an imperative description; use the [task subject rules](references/object-drafts.md#task-commit-subjects) and return composition conflicts to the commit owner. Do not invent IDs for non-task campaign, preparation or merge work.

This skill drafts reports and messages. The active implementation or steering workflow owns its work commits and task status; **sdd-manage** coordinates other persistence and explicit boundary merges, **sdd-forge** owns hosted issue/milestone mutations, and any future PR workflow owns PR creation or merge. A draft does not grant authorization for those actions or establish task completion. Return the draft, source task IDs and issue references actually resolved, evidence used, and any facts still needed before publication.
