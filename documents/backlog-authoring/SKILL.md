---
name: backlog-authoring
description:
  Author plans and native records for existing Backlog.md projects, using their configured MCP or CLI workflow. Use for
  planning requests or task, milestone, decision, and doc updates only when the project already contains a backlog/
  directory belonging to Backlog.md. Does not apply without that directory and does not initialize Backlog.md.
---

# Backlog.md authoring

This general skill is for [Backlog.md](https://github.com/MrLesk/Backlog.md), the Markdown-based tracker with a CLI and
an MCP server. It is not tied to any particular project.

Keep executable work in tasks, delivery outcomes in milestones, durable choices in decisions, and maintained guidance in
docs. For every applicable planning request, consider all four record types, then change only the records that
materially support the requested work.

## Confirm applicability and read the local workflow

Resolve the project root first, since the current working directory may be nested. If the project has no `backlog/`
directory, this skill does not apply. Do not create that directory, initialize Backlog.md, or migrate another tracker to
make the skill apply. Continue ordinary planning when requested, and treat tracker setup as separate work. An MCP server
exposing only initialization guidance does not satisfy this prerequisite.

Confirm that the existing directory belongs to Backlog.md using the project's configuration and guidance. Read
applicable AGENTS.md instructions, the documentation index, and the configured Backlog.md workflow. Do not assume a
particular package manager, version, directory layout beyond the applicability check, or project-specific policy.

Backlog.md provides both CLI and MCP access. Use the interface required by the project. Otherwise, use a configured MCP
connection for operations it supports, with the project-local CLI as a fallback for missing operations or unavailable
MCP access. Verify that the selected MCP server targets this project before reading or changing records; a globally
registered server may point elsewhere. Follow repository wrappers and pinned versions for CLI calls. Do not require both
interfaces to be installed or reconfigure either merely to author a plan.

Read the workflow overview once per conversation through the selected interface: the exposed MCP workflow resource or
tool, or the installed CLI's instructions command. Read the relevant creation, execution, or finalization guide before
those lifecycle operations. Discover actual MCP tools and schemas, and use CLI help for unfamiliar commands. Do not
assume the two interfaces expose identical operations or invent unavailable tools.

Search existing tasks and drafts before creating work. Read the selected task, dependencies, candidate milestone
descriptions, and only the relevant docs and decisions. Ground implementation plans in current source where available,
and distinguish established behavior from requirements, hypotheses, and unverified production state.

## Choose records proportionally

| Record    | Use it for                                                                                                | Prefer                                                                                                                                                              |
| --------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task      | A scoped outcome, acceptance criteria, researched plan, progress, and verification evidence               | Extend the matching task; split only when ownership, dependencies, or independently deliverable outcomes justify it.                                                |
| Milestone | A coherent delivery objective spanning related work                                                       | Reuse a milestone whose description fits. Clarify its description when authorized scope warrants it; create a new milestone only for a distinct delivery objective. |
| Decision  | A significant, durable product, architecture, data, security, or operating-policy choice                  | Reuse a relevant decision or create a linked successor when a material choice changes.                                                                              |
| Doc       | Maintained requirements, behavior, operational guidance, or verification scenarios needed beyond one task | Update the existing canonical topic and link the task or decision. Create a doc only when the topic needs a maintained home that does not already exist.            |

A decision deserves its own record when future work needs to preserve both the choice and its reasoning, especially
where alternatives have lasting consequences or affect multiple features. Public privacy guarantees, data-retention
contracts, or architecture boundaries can qualify. Routine helper names, small UI adjustments, ordinary implementation
details, and every individual acceptance criterion do not.

Keep minor choices and task-specific rationale in the task plan or notes. Do not create one record of each type as a
checklist, duplicate the plan in a separate document, invent milestones for individual fixes, or rewrite historical
decisions to imply that a later choice was always intended. When no related record needs a change, say so briefly if
useful.

## Author the plan and related changes

Make the selected task self-contained: state the problem and intended outcome, testable acceptance criteria, the
implementation approach at the useful level of detail, relevant dependencies, and verification appropriate to the
changed contract. Preserve user decisions, boundaries, rejected alternatives that still matter, and material unknowns.
Avoid generic process padding.

Assess milestone fit and documentation impact while planning, even when the user asks only for a plan. Capture the
resulting links and any deferred documentation work in native task fields. A short note is enough; do not create another
assessment document.

Follow the local lifecycle for storing a researched plan. Keep status and ownership truthful: planning activity is not
completed implementation, and a future implementation task should not remain In Progress merely to hold a plan. Do not
check implementation acceptance criteria based only on documentation or intended tests.

An explicitly accepted significant policy may be recorded before implementation. Label implementation as pending and
link its task. Likewise, distinguish proposed decisions from accepted ones. Existing guides can reference accepted
future requirements without claiming the behavior has shipped; update detailed runtime instructions when there is
evidence for them.

A planning request authorizes the requested planning records and their relevant links. It does not by itself authorize
application implementation, production operations, commits, or unrelated documentation expansion. Use existing session
authorization and local rules; do not introduce blanket approval gates for ordinary planning edits.

## Document visual changes before completion

For an applicable Backlog.md project that includes a web app, document a task's visual changes with screenshots after
implementation, just before marking the task Done. Apply this step during task finalization.

Capture and inspect the changed UI states. Store the images under the project's `backlog/assets/`, using task-specific
filenames or subdirectories. Embed them in the owning task's implementation notes as Markdown images, for example
`![Settings page at 390x844 with validation errors](../assets/task-123/settings-error-mobile.png)` for a task in
`backlog/tasks/`. Resolve image paths from the task file's actual location. Plain links and filesystem paths do not
satisfy the embedding requirement.

Caption each image with the route or fixture, viewport, and state shown. Include before/after views when a baseline is
available and narrow layouts when responsive behavior changes. Verify that the embedded images exist and render before
completing the task. If capture is blocked, record the concrete blocker and missing views, and keep the task open.

## Write and verify native records

Use supported Backlog.md MCP tools or CLI operations for task, draft, milestone, document, and decision changes, subject
to the project's chosen workflow. Preserve generated IDs, metadata, relationships, and history. If an operation is
unavailable through MCP, check the local CLI. If neither supports it, follow an explicit repository exception when one
exists; do not turn a version-specific workaround into universal permission to hand-edit records.

Respect the repository's Git-index and automatic-commit rules. Pass multiline Markdown and literal code spans safely
through the shell.

Read back each changed record through MCP or CLI with the project target verified. Check links, dependencies, milestone
membership, policy/implementation status, and the resulting diff. Run the available Backlog consistency check when
appropriate. Treat missing or unsupported checks as limitations, not successful verification.

Report the saved plan and the related records actually created, updated, or deliberately deferred. Explain significant
deferrals briefly. Keep completion claims limited to the work and evidence that exist.
