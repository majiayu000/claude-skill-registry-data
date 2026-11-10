---
name: azure-devops-work-item-review
description: Use only when the user explicitly invokes `$azure-devops-work-item-review` or names `azure-devops-work-item-review` to review an Azure DevOps Work Item before implementation.
---

# Azure DevOps Work Item Review

## Scope

Use this skill to review whether an Azure DevOps Work Item is ready for
implementation in the current local repository. This skill is read-only.

Read `../azure-devops-common/references/context.md` before resolving the Azure
DevOps target.

## Target Resolution

- Require a Work Item ID, an Azure DevOps Work Item URL, or an unambiguous user
  reference.
- If no Work Item is provided, stop and ask for the ID or URL.
- If the URL points to another organization or project, stop and explain that
  this skill is current-repository only.

## Workflow

1. Resolve repository context with `git status --short --branch`, git remotes,
   and `az devops configure --list`.
2. Fetch the Work Item with `az boards work-item show --id <id> --expand all`.
3. Inspect one-hop related Work Items and pull requests when relations are
   present and same-project.
4. Check for duplicate or already-active work.
   - Query active Work Items with relevant title terms when useful.
   - List open PRs with `az repos pr list` and look for linked Work Items,
     matching branches, or overlapping titles.
5. Read local repository guidance and likely implementation areas with `rg` and
   `rg --files`.
6. Apply the readiness gate.
   - Ready only when acceptance criteria, scope boundary, and dependencies are
     clear and verifiable.
   - Prefer "needs revision", "split", or "hold" for broad, ambiguous, blocked,
     or policy-setting Work Items.

## Output Format

Respond in the user's language:

```markdown
**Verdict**
- Ready to implement | Needs revision before implementation | Split before implementation | Hold
- <one-sentence reason>

**Critical Gaps**
- <missing acceptance criteria, ambiguity, dependency, or "None found">

**Scope & Dependencies**
- <related Work Items/PRs, blockers, sequencing, duplicates, or "No blockers found">

**Codebase Fit**
- <affected areas, feasibility, risks>

**Suggested Revision**
- <specific Work Item body changes>

**Implementation Notes**
- <guidance for the eventual implementer without starting implementation>

**Open Questions**
- <questions for the owner/user, or "None">
```

## Guardrails

- Do not create, update, assign, tag, close, comment on, or transition Work Items.
- Do not create branches, worktrees, commits, or PRs.
- Do not install dependencies or edit manifests or lockfiles.
- Do not assume cross-project context.
