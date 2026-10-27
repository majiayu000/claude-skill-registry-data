---
name: plan-github-work
description: Turn a feature, service, UI, or MVP idea into a scoped GitHub issue tree, save editable Markdown drafts, and publish using native GitHub relationships only after separate explicit confirmation. Use when planning a new unit of work or extending a related issue tree; excludes implementing the work and routine backlog administration.
---

# Plan GitHub work

Produce a self-contained set of issues that explains the work, gives each issue a clear boundary, and shows what depends on what. Favor readable, useful issues over exhaustive specifications.

The workflow is: understand the work, draft the tree, save an editable Markdown file, review it with the user, then publish only after separate explicit confirmation. An initial request to create issues does not authorize publication.

## Understand and divide the work

Inspect relevant code, documentation, repository instructions, and existing GitHub issues, labels, and milestones. Use available context before asking questions. If repository access is unavailable, continue drafting from supplied information and distinguish assumptions from verified facts.

Use an adaptive conversation to establish the intended users, desired outcome, scope, constraints, and decisions that affect the breakdown. Ask focused questions about missing information; do not impose a questionnaire when the request is already clear. Do not invent architecture, requirements, deadlines, or owners.

- Split work into coherent deliverables with clear completion points. Split further when outcomes, ownership boundaries, or genuine dependencies differ. Do not impose a number of issues, time limit, or one-pull-request rule.
- Prefer a shallow tree: a root explaining the whole effort, with implementation issues beneath it. Add intermediate parents only when they help readers navigate the work. A small request can remain one issue.
- Keep routine implementation steps, tests, and documentation with their deliverable. Separate them only when they represent independently useful work.
- Reuse relevant existing issues rather than duplicating them. Identify proposed edits or relationship changes explicitly; do not silently rewrite or reparent existing work.
- Resolve uncertainty that changes the breakdown. If investigation is itself necessary work, give it a specific question and expected decision, and leave dependent implementation scope provisional until that decision is made.
- Use parent relationships to express membership in the work. Add a blocking relationship only when completing one issue genuinely requires another's result. Explain the reason briefly in the review file. A preferred order or shared parent is not enough.

Check coverage, overlap, scope boundaries, excessive nesting, and dependency cycles before presenting the draft. Dependencies may cross branches of the tree. Avoid redundant links that merely repeat an existing chain of prerequisites.

## Write the issues

Assume a capable reader who may be new to the project. Use ordinary words, concrete titles, and short explanations. Retain technical details when they affect the agreed result, not to prescribe every implementation step.

Use these exact sections unless the user requests another format:

```markdown
## Overview

Explain the current situation, the intended change, and why it is needed.

## Scope and role within the work

Briefly explain the whole work unit and its main parts. State this issue's
contribution and what relevant sibling issues handle.

## Goal

State the result this issue will deliver.

## Acceptance checks

- List concise, observable conditions for completion.
```

The root carries the fuller overview and overall boundaries. Each child includes enough context to stand alone; links to the parent and relevant siblings supplement that explanation. Do not copy the entire root into every child or replace context with “see parent.”

Acceptance checks describe useful results. Avoid exhaustive edge-case lists, invented performance numbers, filenames, command sequences, and test implementation details unless the requirement calls for them. Keep important correctness requirements. Parent checks describe the combined outcome rather than merely saying all children are closed. Use as many checks as the issue needs, without padding to a quota.

Keep each check focused on an observable result. Do not add a separate “verification covers” or “tests cover” item that repeats the other checks. Leave routine format edge cases and test inputs to implementation unless the user identifies them as requirements; preserve explicit access, data correctness, and other consequential constraints.

### Diagrams where useful

Add a Mermaid diagram when it makes the issue's boundaries or interactions easier to understand. Suitable parents show a compact overview; relevant children show their contribution with enough surrounding context. Skip diagrams for straightforward issues. Place them under **Scope and role within the work**, alongside a short prose explanation, preserving the four sections.

Read [Diagram guidance and examples](references/diagrams.md) when adding diagrams. Use known or agreed architecture, consistent component names and node IDs, and an explicit “this issue” label on the component or interface being addressed. A user-flow diagram can help when architecture is undecided; do not invent infrastructure to fill a picture. System arrows describe interactions, while native GitHub relationships describe issue dependencies.

### Required no-ai-slop pass

Read and apply the installed `no-ai-slop` skill and its referenced evaluation checks to every issue title and body. If it is unavailable locally, read the upstream [SKILL.md](https://github.com/petergyang/no-ai-slop/blob/main/skills/no-ai-slop/SKILL.md) and [eval.md](https://github.com/petergyang/no-ai-slop/blob/main/skills/no-ai-slop/eval.md). Follow referenced paths relative to that source. Do not silently substitute remembered rules or install anything automatically.

Supply your own issue drafts as the editing input, using the established audience and purpose. Apply the writing pass to diagram labels and captions too, preserving valid Mermaid syntax. Preserve the user's required headings. Keep editorial commentary, including any “What changed” note, outside issue bodies. Apply the checks again after substantive revisions. If neither installed nor upstream instructions can be read, continue scope planning and save a clearly marked draft, but explain that the required writing pass is incomplete and do not present it as ready to publish.

## Organize the work on GitHub

Default to one repository and a milestone containing the tree. Reuse a suitable milestone or propose a new one without inventing a due date. Respect another grouping or no grouping when requested. Reuse relevant labels and configured issue types; propose new labels only when they help. Leave assignees, estimates, priorities, and dates unset unless supplied or established by applicable conventions.

Support multiple repositories when requested. Specify each issue's repository and propose a shared GitHub Project, reusing a suitable existing one when available. Milestones are repository-specific. Check native relationship restrictions before promising a cross-repository tree; agree on a supported structure if the requested arrangement is unavailable.

Read [GitHub publishing](references/github-publishing.md) when inspecting GitHub capabilities or preparing publication. Use native parent/sub-issue and blocked-by relationships. Text links and checklists do not substitute for those relationships.

## Save the editable review file

Before requesting publication confirmation, write the complete proposal to a local Markdown file and give the user its path as a clickable link. Follow an established planning-document location; otherwise use `docs/plans/<work-slug>.md` in the target checkout, or the current workspace when there is no checkout. Respect a user-supplied path. Never overwrite an unrelated file with the same name; choose an unused descriptive filename.

The file is the source for publication, not a disposable copy of the conversation. Include:

- A short summary, assumptions, unresolved decisions, and whether the proposal is ready for publication.
- The destination repository or repositories; the proposed milestone, Project, or explicit choice of no grouping; and any new metadata to create.
- A compact tree using stable draft IDs such as `W1`, `W2`, and `W3`, plus any dependencies and their short reasons. Explain their direction using the actual issues. If there are no dependencies, state that briefly; omit hypothetical relationships and unrelated draft IDs.
- Every full issue title and body, including parent issues. Before each body, list its draft ID, repository, parent, blockers, labels, and whether to create or reuse an issue. For reused issues, include the URL and proposed changes. Add optional metadata only when applicable.

For readability, introduce each draft with a level-one heading such as `# W2: Send workspace invitations`, followed by its metadata and the four level-two body headings. Keep review metadata, dependency explanations, and editorial notes outside the issue body. Use draft IDs for cross-references that will become GitHub links after publication. These IDs are planning references, not prefixes for published titles.

Keep Mermaid source inside the issue bodies in this file, so users can edit and review diagrams with the prose. Images rendered for inspection are optional previews, not replacements for the source.

Tell the user they can edit the file directly. Before revising it, reread it and preserve their edits. If its overview tree and per-issue metadata disagree, resolve the discrepancy before publishing. Compare diagrams with the issue's scope and related diagrams too: an edited highlight, component, or interface must not silently contradict the prose or agreed design. Validate edited IDs and references; do not guess which issue a broken reference meant. Diagram changes follow the same review and confirmation rules as other body edits.

## Review and obtain confirmation

Present the file link with a short summary of the tree and proposed external changes. Make the actual issue drafts and grouping details reviewable before asking for approval. Resolve outstanding scope decisions and complete the writing pass first.

Require clear, explicit, separate confirmation to publish the reviewed proposal. For example: “Publish the issues from this file to owner/repo, including the listed milestone and relationships?” Explain that this skill requires separate confirmation before GitHub changes, and link this instruction file when explaining the pause.

The initial task request, silence, approval of the idea, or an ambiguous “looks good” does not count. “Publish the issues from the file” after the review does count. Confirmation covers the listed issue, relationship, milestone, Project, label, and existing-issue changes; do not make preparatory GitHub writes before it.

When confirmation arrives, reread the Markdown file, including user edits, and validate it. If confirmation clearly covers that edited version and it is ready, publish its contents. If you need to resolve ambiguity or make substantive changes, show the revision and obtain renewed confirmation. Do not quietly rewrite approved prose. Changes after confirmation require confirmation of the changed version before they are published.

## Publish and verify

Follow the publishing reference. Record the approved file version and map draft IDs to created or reused issue IDs, numbers, and URLs. Create the approved grouping and issues, apply native relationships, and replace draft cross-references with real links. Read back the results to verify bodies, metadata, hierarchy, and dependency direction.

Preserve the editable Markdown file. Record publication URLs and any incomplete operations in it without overwriting concurrent user edits. Do not automatically synchronize later file edits back to GitHub.

Return the file link, grouping and root links, a compact linked tree, and the work that can start immediately. Report any unverified or incomplete operations plainly. For partial failure, preserve successful work, inspect before retrying, and resume only the missing approved operations. Do not automatically delete, close, or recreate successful issues. Unchanged, already-approved work does not need repeated approval; material additions do.

## Worked example

Suppose the agreed requirement is to let workspace owners email invitations and let existing account holders accept them. Creating accounts remains part of the existing sign-up flow. A draft might contain the following tree:

```text
W1 Let workspace owners invite teammates
├── W2 Send workspace invitations
└── W3 Let invited people join a workspace

W3 is blocked by W2: joining through an invitation needs the invitation
records and links delivered by W2. Preparatory development can overlap.
```

The issue bodies could read as follows. The actual review file also includes the per-issue metadata described above.

### W1: Let workspace owners invite teammates

```markdown
## Overview

Adding teammates currently requires help from an administrator. Workspace
owners should be able to invite people themselves.

## Scope and role within the work

This work covers sending invitations and accepting them. W2 handles sending;
W3 handles joining. New account creation stays in the existing sign-up flow.

## Goal

Let an owner invite someone who can then join the workspace.

## Acceptance checks

- An owner can send an invitation and its recipient can use it to join.
- The new teammate appears in the workspace's member list.
```

### W2: Send workspace invitations

```markdown
## Overview

Owners need a way to invite teammates without asking an administrator.

## Scope and role within the work

The invitation flow covers sending invitations and joining a workspace.
This issue creates and emails invitations. W3 handles accepting them.

## Goal

Let an owner send a workspace invitation to an email address.

## Acceptance checks

- An owner can send an invitation from the workspace.
- The recipient receives a link identifying the invitation and workspace.
- Someone who is not an owner cannot send workspace invitations.
```

### W3: Let invited people join a workspace

```markdown
## Overview

People who receive a workspace invitation need to be able to accept it.

## Scope and role within the work

The invitation flow covers sending invitations and joining a workspace.
This issue uses the invitations from W2 to add recipients as members.
It uses existing sign-in and sign-up flows.

## Goal

Let the invited person accept an invitation and enter the workspace.

## Acceptance checks

- The invited person can accept the invitation while signed in.
- Accepting adds them to the intended workspace.
- Another account cannot accept their invitation.
```
