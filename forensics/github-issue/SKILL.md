---
name: github-issue
description: Search, write, and classify GitHub issues within live authorization.
---

# GitHub issues

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/github-issue/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use for durable follow-ups and pull-request linkage. Read local `AGENTS.md`, issue
templates, and repository-routing policy before any remote mutation.

## Mutation authority

- Caller authorization is required before any issue or taxonomy mutation. A credential does not
  grant scope.
- Resolve the authenticated identity, current repository, and requested target. Do not assume an
  owner prefix or visibility.
- Immediately before every write, refetch the exact target. Its canonical identity must still
  match, and the repository must not be archived.
- Issue operations require issues to be enabled and `viewerPermission` of `TRIAGE`, `WRITE`,
  `MAINTAIN`, or `ADMIN`. Issue creation additionally requires `viewerCanCreateIssues`.
- Applying existing metadata to a pull request uses that same permission set and does not require
  issues to be enabled.
- Creating, changing, or deleting taxonomy definitions requires `WRITE`, `MAINTAIN`, or `ADMIN`
  plus the operation-specific API capability. Creating, renaming, or closing a project requires
  project-write.
- Insufficient permission or capability, missing or inaccessible data, an identity change, or a
  mismatch is a hard deny. Approval cannot override it.
- Adding an item to an existing project uses the same permission set as applying existing metadata,
  plus project-write. That add mutates project membership and needs no separate approval.
- Missing project scope or capability denies the project step only. Skip it, report the gap, and
  do not work around it. The issue and its other metadata still proceed.

## Denied external target

- Do not write to a denied external creation target.
- Search for, then create or reuse, a tracking issue in the current repository or a
  consumer-selected tracker. Immediately before that write, refetch the destination and apply the
  issue-operation gate above.
- Include the intended upstream repository and a copy-ready report.
- Before naming that upstream repository, resolve it and compare the returned canonical name with
  the name being written. A rename redirect resolves under the stale name, so existence is not
  identity. This check is report accuracy, not the hard-deny mismatch above: write the canonical
  name. When the name does not resolve, route the follow-up to the current repository and do not
  name the unreachable target.
- Before copying details to a less-restricted destination, remove private repository identity,
  paths, links, code, and findings. If redaction would make the report unusable, require explicit
  destination approval or return the draft without mutation.
- Authorization to file the external issue includes this tracking fallback unless the caller opts
  out. Report the reroute. If no tracker passes, return the draft without mutation.
- Do not fall back silently, and do not fall back to an unverified repository.

## Issue workflow

1. Search open issues and relevant closed issues in the destination. Return a likely duplicate
   instead of filing one. Verify the paths and current behavior the issue names.
2. Before editing, commenting, relating, closing, or otherwise changing state, refetch the issue
   and its discussion. Confirm the mutation is still authorized and supported. Close only when the
   documented outcome and acceptance evidence show the work is resolved. Otherwise leave state
   unchanged and report the gap.
3. Write a self-contained issue: problem, desired outcome, ownership boundaries, concrete areas,
   validation, and external context. A discovered blocker does not widen implementation scope.
   - Before absorbing a newly discovered blocker, require the calling workflow to reproduce it
     against the refreshed default branch and provide the evidence, then search for an existing fix
     or issue. If a fix resolves it, report it so the caller can use and retest it. Otherwise ask
     whether to widen the accepted scope or only link or record a follow-up. Filing records work;
     it does not amend the accepted plan or authorize implementation.
   - A stop condition in an issue names a real decision for a human. Adding or changing an index,
     or a rewrite that returns the same rows, is never one: the worker makes the change and records
     the plan before and after.
   - Verify every existing path in `## Files / areas` against `HEAD`. Mark a proposed path `New`
     and verify its owning parent or module. Reject absolute and parent-traversal (`..`) paths. For
     a target outside the current checkout, verify only redacted remote metadata through the
     Contents API.
4. Fetch the complete live taxonomy, including open projects. Apply matching existing labels and a
   selected existing milestone with no separate approval.
   - Use an existing open project for strategic, initiative-level tracking, and a milestone for
     repo-local release or sequencing. Choose by the initiative, not by how many repositories it
     touches. A single-repo strategic initiative can have a project. An initiative can have both.
     An issue belongs to at most one project, and not every issue needs one.
   - Before adding a project item, check that item and any item the project's automation could
     pull in with it, such as a parent issue's sub-issues. If any already belongs to a different
     project, skip the add and report the conflict.
   - Adding an item to an existing, described project needs no separate approval. Creating,
     renaming, or closing a project is a separate taxonomy operation, as is creating a milestone.
   - Missing project scope or permission skips the project step. Report the gap and do not work
     around it.
   - Do not set a project status that closes the issue unless closing is separately authorized.
     GitHub's Auto-close issue workflow closes the issue when status becomes Done.
   - When a plan issue's source already has a milestone, apply that same milestone. When the source
     already has a project, refetch memberships and apply that project only when exactly one
     accessible open membership exists. Otherwise skip the project and report the conflict.
   - Omit a missing optional milestone. A missing required milestone blocks the issue. Omit a
     declined optional label. A missing required label blocks the issue.
   - For a missing label, use
     [review-github-issue-taxonomy](../review-github-issue-taxonomy/SKILL.md) and get explicit
     approval of the exact repository, name, description, and color before creating it.
5. Refetch the created or updated issue and verify metadata, including project membership. After a
   project add, re-read the project: automation can pull in more items, including into a second
   project. Report a partial failure without retrying creation. Preserve history and report the
   action, URL, labels, milestone, and project.
6. Link a pull request with a closing reference only when it fully resolves the issue. Fully
   qualify cross-repository references. Pull-request creation authority stays separate.
7. Use native sub-issues only for a real hierarchy, blocked-by only for a known dependency, and
   prose links for related work. Read every created relationship back.

For a batch, preflight every entry before writing any issue. One invalid entry fails the whole
batch. A partial transport failure stops further creation and reports every issue already created.
Do not retry an entry that succeeded.

## Bounded output

- A search returns at most five `#N: title -- url` lines.
- A near-duplicate returns `Duplicate of #N: <url>`.
- A mutation returns the action, URL, labels, and verification, plus milestone and project when set.

Consumer wrapper owns: repository allowlist, taxonomy, issue template, credential, and CLI wrapper.
It may tighten this gate and may not weaken it.
