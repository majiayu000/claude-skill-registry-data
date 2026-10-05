---
name: manage-issues
description: "Create, edit, search, close, and triage GitHub Issues via the gh CLI. Use when asked to file a bug, request a feature, create a task, report a problem, search the backlog, triage issues, or manage the issue tracker. Also use when the user says 'create an issue', 'file a bug', 'open a ticket', 'add to backlog', 'search issues', 'close issue', or mentions GitHub Issues in any task-management context. Handles label/milestone assignment, duplicate detection, and project board integration. Do NOT use for pull requests, changelog entries, or non-GitHub trackers (Jira, Linear, GitLab) or managing TODO.md file."
metadata:
  author: Serghei Iakovlev
  version: "1.3"
  category: roadmap
---

# Managing GitHub Issues

Manage the active repository's issue tracker via `gh`. Every issue must be self-contained, professional, and actionable without prior context. The skill applies only to repositories where Issues are enabled; if `ISSUES_ENABLED` is `false` in the taxonomy, stop and tell the user.

## Running scripts bundled with this skill

Script paths in this document (e.g. `scripts/`) are resolved relative to **this** SKILL.md file, not to your current working directory. If a relative command fails to resolve, prefix it with the path your platform loaded this SKILL.md from.

**Fallback.** If the script cannot be located, run the equivalent `gh` commands listed at the end of "Discover taxonomy" below; the script is a convenience wrapper around the same calls. If `gh` itself is missing or unauthenticated, the skill cannot proceed: surface the error to the user and stop.

## Discover taxonomy (run first)

Before any create, edit, or triage operation, fetch the live taxonomy for the active repo:

```bash
sh scripts/get_taxonomy.sh --cached
```

The output declares seven sections: `CACHED_AT`, `REPO`, `ISSUES_ENABLED`, `ISSUE_TYPES`, `LABEL_PREFIXES`, `LABELS`, `MILESTONES`, `PROJECT_BOARDS`. Use the values verbatim; never memorize or guess label names, milestone titles, type `node_id`s, or project names.

The `--cached` flag reads from a 24h file cache keyed by `owner/repo` under `${TMPDIR:-/tmp}/manage-issues-cache/`. Re-run without `--cached` when:

- An `Error recovery` row matches a "not found" condition.
- The user added, renamed, or closed labels, milestones, or projects in this session.
- `CACHED_AT` is older than 24 hours.

Branching on what the taxonomy reports:

| Section reports | Behavior |
|---|---|
| `ISSUES_ENABLED: false` | Stop. Tell the user the repository does not use GitHub Issues. |
| `ISSUE_TYPES: (none)` | Skip the issue-type assignment step; rely on labels for classification. |
| `LABEL_PREFIXES: (none; ...)` | Use flat labels exactly as listed; do not invent `prefix:value` style. |
| `LABEL_PREFIXES: <list>` | Follow the detected convention. Pick at least one label that scopes the affected subsystem when such a prefix exists (typically `area:`). |
| `MILESTONES: (none open)` | Omit `--milestone` everywhere. |
| `PROJECT_BOARDS: (none ...)` | Omit `--project` everywhere. |

If the script is unavailable, the equivalent calls are:

```bash
gh repo view --json nameWithOwner,hasIssuesEnabled
gh api "/orgs/{owner}/issue-types"
gh label list --limit 200
gh api "repos/{owner}/{repo}/milestones?state=open" --paginate
gh project list --owner {owner} --limit 10
```

## Issue Type assignment (only if configured)

If `ISSUE_TYPES` is non-empty, every issue must have exactly one type from that list. `gh issue create` does not accept `--type`, so set the type via GraphQL after creation:

```bash
ISSUE_NODE_ID=$(gh api "repos/{owner}/{repo}/issues/${ISSUE_NUMBER}" --jq '.node_id')
gh api graphql -f query="
mutation {
  updateIssue(input: {
    id: \"${ISSUE_NODE_ID}\"
    issueTypeId: \"<type node_id from taxonomy>\"
  }) {
    issue { number title }
  }
}"
```

`type` has no `gh` surface on the read side: it is not a `--json` field on `gh issue view` or `gh issue list`, and neither `gh issue create` nor `gh issue edit` accepts a `--type` flag (checked at gh 2.86.0). Read it back, and set it more briefly, through REST:

```bash
gh api "repos/{owner}/{repo}/issues/${ISSUE_NUMBER}" --jq '.type.name'
gh api -X PATCH "repos/{owner}/{repo}/issues/${ISSUE_NUMBER}" -f type='<type name from taxonomy>'
```

The REST form takes the type's display name, so it needs no `node_id` lookup. Read the type back after either form: an issue left untyped is reported by nothing downstream.

If `ISSUE_TYPES: (none)`, skip this step entirely. The repo uses labels, not GitHub Issue Types, for classification.

## Milestone matching

The user may reference a milestone by full title or by shorthand specific to their project (`M10`, `2025Q4`, `v2.1`, etc.).

1. List the full titles from the `MILESTONES` section of the taxonomy.
2. If the shorthand maps unambiguously to one full title (substring, leading token, prefix), use that exact full title in `--milestone`.
3. If multiple titles plausibly match, ask the user to disambiguate.
4. If the user did not name any milestone, pick the best-fitting open milestone based on the issue's theme. If none fits, omit `--milestone` rather than blocking or asking.

## Before creating an issue

### Duplicate check (BLOCKING)

```bash
gh issue list --search "<keywords>" --state all --limit 20 \
  --json number,title,state,labels,milestone \
  --jq '.[] | "#\(.number) [\(.state)] \(.title)"'
```

- **Exact duplicate.** Stop. Report the existing issue number.
- **Partial overlap.** Mention the related issue. Ask whether to proceed.
- **No match.** Proceed.

### Proportionality check

A issue is a durable artifact with a cost of its own: the prose to write it, and the re-derivation a future reader faces because the context that produced it is gone. When the change it would request is smaller than that cost, the issue is the more expensive half of the transaction.

Weigh both sides before creating:

- **The fix.** Is the whole change a small, local edit whose correctness is evident from the diff, inside code the current work already touches, and covered by the checks that work already runs?
- **The issue.** How much of the body would restate context that exists only right now, and how much re-derivation does a future reader inherit?

When the fix is clearly the cheaper half, do not create it. Propose the edit instead: name the file and lines, state the change in a sentence or two, give the cost comparison that justifies doing it now, and **ask the user for approval, then wait.** On approval, apply the edit under the boy-scout principle - leave the code better than you found it - and report it as applied rather than filed. On refusal or silence, create the issue as normal.

Never self-approve this path. The approval is what makes the edit part of the requested work instead of unrequested scope, which is the distinction a surgical-changes convention turns on.

Cheapness alone does not admit an edit. Create the issue regardless of size when the change would alter behaviour a user notices, touch a security boundary, require a decision the agent cannot make, or reach code the current work does not already touch.

## Create

### Body rules

- **Language.** English.
- **Tone.** Professional, concise, no filler.
- **Privacy.** Never include usernames, API keys, internal URLs, tokens, or personal information, regardless of whether the repository is public or private.
- **Self-contained.** A stranger must understand the issue from the body alone.
- **Bugs describe problems, not solutions.** The implementer chooses the fix.
- **Verification.** Required for Bug and Feature. Optional for Research, Docs, Refactor, Test (include when a concrete completion signal exists).
- **No hard wrapping.** Write each paragraph as a single line; GitHub handles word wrap at render time. Hard line breaks mid-sentence produce ragged diffs and noisy reflows.

### Body templates

Pick the template for the chosen issue type (or, if `ISSUE_TYPES: (none)`, the template matching the inferred kind of work). Load the matching `##` section of [assets/issue-templates.md](assets/issue-templates.md):

| Kind of work    | Section in assets/issue-templates.md |
|-----------------|--------------------------------------|
| Bug             | `## Bug`                             |
| Feature         | `## Feature`                         |
| Research        | `## Research`                        |
| Docs            | `## Docs`                            |
| Refactor / Test | `## Refactor / Test`                 |

Drop bracketed `[...]` sections of the template that do not apply. Required sections (no brackets) stay.

### Title rules

- Imperative mood, capitalize first word: "Add X", "Fix Y", "Implement Z".
- Backtick-wrap code identifiers: `` Add `--host` flag for HTTP bind address ``.
- Under 80 characters, no trailing period.
- No `[type]` prefix when `ISSUE_TYPES` is configured (the type carries the classification). When `ISSUE_TYPES: (none)`, match the title style already used in the repo (`gh issue list --state all --limit 20`); add a `[type]` prefix only when the repo's existing titles do.

### Composing the command

Use single quotes for `--body` to prevent shell interpolation. Escape literal single quotes in the body with `'\''`.

```bash
ISSUE_URL=$(gh issue create \
  --title '<title>' \
  --body '<body>' \
  --label '<label from taxonomy>' \
  --milestone '<full milestone title from taxonomy>' \
  --project '<project name from taxonomy>')

ISSUE_NUMBER=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')
```

Drop the `--label`, `--milestone`, or `--project` flags when the corresponding taxonomy section is `(none)`. After creation, run the GraphQL `updateIssue` mutation from "Issue Type assignment" if and only if `ISSUE_TYPES` is configured.

### Batch creation

When creating multiple related issues:

1. Present all planned issues as a numbered list (title, type if applicable, labels, milestone) before creating any.
2. Wait for user confirmation.
3. Create sequentially. Report each issue number after creation.
4. Print a summary table when done:

```
| # | Title | Type | Labels | Milestone |
|---|-------|------|--------|-----------|
```

## Search, Edit, Close

`gh` invocations for these three operations are catalogued in [references/gh-recipes.md](references/gh-recipes.md). Load that file when the user asks to find, modify, or close an issue. The rules below are policy and bind regardless of which recipe is used:

- **Never comment.** Do not post a comment on an issue in any operation. Nothing reads them: every consumer of an issue reads its title, body, and metadata, so a comment lands in a channel with no reader and leaves the false impression that the issue was brought up to date. Answering a person who asked a question is correspondence rather than a tracker-management operation, and is out of scope for this skill either way.
- **Edit.** Confirm destructive edits (body replacement, milestone change, project removal) with the user before executing.
- **Close.** Use `gh issue close --reason completed` or `--reason "not planned"`, never `--comment`. When a closing rationale genuinely needs to be recorded, it belongs in the issue body, and only when the issue is ours.
- **Foreign issues.** An issue is foreign when its author is neither a maintainer of the active repository nor a bot whose authorship is incontrovertible. Decide by `author.login`; `authorAssociation` is not evidence, since a `MEMBER` who is not a maintainer is still foreign. Never edit a foreign issue's title or body. With comments forbidden as well, a foreign issue has nowhere to record a rationale at all, so close it without one. The link from the resolving pull request already appears in the issue timeline without anyone writing it there.
- **Milestone arguments.** Use the full title from the taxonomy, never the shorthand.

## Linking dependencies

Apply this section only when the user wants to record that one issue blocks or depends on another. Many workflows have no blocker relationships; skip it entirely when none apply.

GitHub exposes native issue dependencies (a "blocked by" / "blocking" relationship that renders on both issues in the UI). Prefer these over a free-text "Blocked by #N" line: native links are queryable and visible from both ends. The feature is relatively new and may be unavailable or disabled on some repositories or plans, so degrade gracefully when it is.

**Key gotcha.** The API identifies the blocking issue by its **database id**, not its issue number. Resolve the id first, then record that `{issue_number}` is blocked by `{blocker_number}`:

```bash
BLOCKER_ID=$(gh api repos/{owner}/{repo}/issues/{blocker_number} --jq '.id')
gh api --method POST \
  repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by \
  -F issue_id="$BLOCKER_ID"
```

The inverse "blocking" relationship appears automatically on the blocker. List or remove:

```bash
gh api repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by --jq '[.[].number]'
gh api --method DELETE repos/{owner}/{repo}/issues/{issue_number}/dependencies/blocked_by/$BLOCKER_ID
```

These endpoints need a recent REST API version. Current `gh` sends a recent default; if a call fails with a version error, add `-H "X-GitHub-Api-Version: 2026-03-10"` (or newer).

**Graceful degradation.** If the endpoint returns 404, 410, or 422 (feature unavailable, not enabled, or invalid target), do not block the task. Fall back to a textual "Blocked by #N" line in the issue body and tell the user the native link could not be set. Always confirm a successful link with the list call above.

## Triage

When triaging a finding from code, logs, review, or conversation into the backlog:

1. **Extract the concern.** State it in one sentence.
2. **Duplicate check.** Run the procedure in "Before creating an issue" above (BLOCKING).
3. **Classify.** If `ISSUE_TYPES` is configured, pick one. Pick labels per the detected convention.
4. **Place in milestone.** Match the milestone whose theme fits the concern, or omit.
5. **Draft the body** using the template for the chosen kind of work.
6. **Present the full `gh issue create` command for review** before executing.

## Quality checklist

Before executing `gh issue create`, verify:

- [ ] Taxonomy fetched this session (or cache is under 24h old)
- [ ] `ISSUES_ENABLED: true`
- [ ] Duplicate check performed
- [ ] Proportionality weighed: filing costs less than the change it requests, or the cheaper edit was proposed and approved
- [ ] Title: imperative, under 80 chars, no trailing period
- [ ] Issue type assigned via GraphQL `updateIssue` if `ISSUE_TYPES` is configured (else skipped)
- [ ] At least one label from taxonomy, following the detected convention
- [ ] Milestone uses full title from taxonomy, or omitted when `MILESTONES: (none open)` or no milestone fits
- [ ] Body matches the template for the chosen kind of work
- [ ] Verification criteria present for Bug and Feature
- [ ] No usernames, keys, internal URLs, tokens, or personal information
- [ ] No solution prescribed in bug reports
- [ ] Related issues referenced with `#NNN` where applicable
- [ ] `--project` uses project name from taxonomy, or omitted when `PROJECT_BOARDS` is empty
- [ ] Blocker relationships, when the workflow uses them, linked natively (or a textual "Blocked by #N" fallback added when the API is unavailable)

## Error recovery

| Error | Recovery |
|---|---|
| `ISSUES_ENABLED: false` | Stop. The repository does not use GitHub Issues. |
| Issue type not found | Re-run taxonomy without `--cached`; use exact `node_id` from output. |
| Milestone not found | Re-run taxonomy without `--cached`; if still no match, omit `--milestone`. |
| Label not found | Re-run taxonomy without `--cached`; label may have been renamed or deleted. |
| Project not found | `gh project list --owner <owner>` to verify name and access. |
| HTTP 403 on project | `gh auth refresh -s project,read:project` to add project scope. |
| HTTP 422 on create | Check for duplicate title or missing required fields. |
| GraphQL `updateIssue` returns null | Verify the type `node_id` matches the current org's `ISSUE_TYPES` output. |
| HTTP 404/410/422 on `dependencies/blocked_by` | Native dependencies may be unavailable or not enabled for this repo; fall back to a textual "Blocked by #N" note. Confirm `issue_id` is the blocker's database id, not its issue number. |
