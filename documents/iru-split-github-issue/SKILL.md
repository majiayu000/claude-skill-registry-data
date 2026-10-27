---
name: iru-split-github-issue
description: "/iru-split-github-issue <issue-number> (stays the root) or /iru-split-github-issue draft:<path> (root created from the draft); optional force: yes skips the size assessment, label: <name> sets the label. Splits an oversized GitHub issue into dependency-ordered sub-issues (same Parallel group = independent) under a root issue and a milestone, reviewing each draft with iru-review-github-issue. GitHub-only. Creates nothing until the user confirms the proposed split. Use when an issue has many requirements, several independently deliverable capabilities, or is estimated hard or above."
model: sonnet
---

# Split GitHub Issue

Turn one oversized issue into a root issue plus small, self-sufficient sub-issues ordered by dependency, tracked by a
milestone. Body templates are in `reference/split-templates.md` (relative to this skill's directory); read it before
Step 5.

**Nothing is created, edited, linked or commented before the explicit confirmation in Step 6.** Steps 1-5 are
read-only.

## Step 1 — Resolve the input and fetch

Parse the arguments:

- `<issue-number>` (optionally `#`-prefixed): existing issue. It stays the root; see "Existing issue" below.
- `draft:<path>`: local Markdown draft (first line `# <title>`, rest is the body). Read it. If missing or without a
  title line, tell the user and stop.
- optional `force: yes`.
- optional `label: <name>` (passed by `iru-draft-github-issue`): the label for the root and the sub-issues. Use it only
  if it exists in `gh label list --json name`; otherwise tell the user and continue without it. Without the argument,
  an existing root keeps its own labels and sub-issues inherit them; a draft root gets none unless the user picks one
  from the actual list in Step 6. A `documentation`-kind sub-issue uses the `documentation` label instead when that
  label exists.
- Neither form: ask which issue number or draft path to split.

Confirm the repository is hosted on GitHub (`git remote get-url origin` matches `github.com` or a GitHub Enterprise
Server domain). Otherwise say this skill only splits GitHub issues and stop. Resolve owner and repo with
`gh repo view --json owner,name`.

For an existing issue run `gh issue view <n> --json number,title,body,labels,comments,state,url`. If `gh` is missing,
search for GitHub MCP tools (`ToolSearch` "github issue"); if none exist, tell the user and stop.

## Step 2 — Assess size

Judge (do not compute) whether the issue is large, using these signals:

1. more than about 7 acceptance criteria or functional requirements;
2. more than one independently deliverable capability;
3. more than one module or area touched (verify against the code with `Read`/grep when files are named);
4. estimated difficulty hard or above.

If no signal fires and `force: yes` was not given, say the issue is not large enough to split, name the signals
checked, and stop. If any signal fires (or `force: yes`), continue.

## Step 3 — Propose the sub-issues

Cut the issue into slices that each deliver something testable. For each sub-issue give: title, scope, the subset of
requirements and acceptance criteria it owns (every original requirement and criterion must land in exactly one
sub-issue; nothing may be dropped or invented), and kind (`functional` or `documentation`). Aim for at least 2 and
rarely more than about 8 sub-issues.

## Step 4 — Compute dependencies and groups

For each sub-issue decide which others it truly needs finished first (`Blocked by`). Assign group numbers:

- a sub-issue with no blockers is in group 1;
- otherwise its group is one more than the highest group among its blockers;
- issues in the same group are independent and can run in parallel; ordered groups are dependencies.

A dependency cycle means the slicing is wrong: re-cut the slices until the graph is acyclic.

## Step 5 — Review each sub-issue draft

Compose each sub-issue body from the sub-issue template, using placeholders for issue numbers that do not exist yet.
Write each draft to a temp file in the scratchpad (or temp directory) and run
`Skill({skill: "iru-review-github-issue", args: "draft:<path>"})`. The review is report-only. Consume its block
unchanged: resolve findings from the original issue text or the codebase when possible; otherwise put the
finding's question to the user. Do not proceed to confirmation with unresolved `gap` or `pending` findings unless
the user explicitly accepts them.

## Step 6 — Confirm

Show the user:

- the sub-issue table (group, title, blocked by, kind, requirements/criteria owned);
- the Mermaid `flowchart` of the dependencies (as in the root template);
- the milestone that will be created (or reused, when one with the root title already exists), the label(s) to apply,
  and, for an existing issue, that the root body will be rewritten.

Ask via `AskUserQuestion`: **Create everything now** / **Adjust the split first** (take edits, redo Steps 3-6) /
**Don't create anything** (stop; the proposal is the deliverable). Only the first option permits Step 7.

## Step 7 — Create

Write every body to a temp file and use `--body-file` (avoids quoting problems). Use `gh api` and the `gh issue`
commands; if `gh` is missing or unauthenticated, use GitHub MCP tools for the same operations.

1. **Look up an existing milestone** with the root title. Milestones are listed open-only by default, so ask for all
   states and match the title exactly:
   ```bash
   gh api --method GET repos/{owner}/{repo}/milestones -f state=all -f per_page=100 \
     --jq '.[] | select(.title == "<root title>") | {number, state, html_url}'
   ```
   Creating a milestone whose title already exists fails with `422 Validation Failed`, so never POST without this
   lookup. A match is reused after telling the user (a closed one is reopened with
   `gh api --method PATCH repos/{owner}/{repo}/milestones/<number> -f state=open`).
2. **Root issue first**, so the milestone can link it. Draft input:
   `gh issue create --title "<title>" --body-file <path> [--label "<label>"]`, with the group table holding
   placeholders; capture the root number and URL. Existing issue: the root is `#N` (see "Existing issue" below).
3. **Milestone** (title = root title, description linking the now-known root), unless step 1 found one:
   ```bash
   gh api --method POST repos/{owner}/{repo}/milestones -f title="<root title>" \
     -f description="Tracks #<root> (<root url>) and its sub-issues." --jq '{number, html_url}'
   ```
   Then put the root on it: `gh issue edit <root> --milestone "<root title>"`.
4. **Sub-issues in dependency order** (group 1 first), so `Blocked by` can use real numbers:
   ```bash
   gh issue create --title "<title>" --body-file <path> --milestone "<root title>" [--label "<label>"]
   ```
   Put the real `Parent: #<root>`, `Blocked by: ...` and `Parallel group: <n>` lines in each body.
5. **Link each as a sub-issue of the root.** The REST `sub_issue_id` is the child's numeric `id`, not its `number`:
   ```bash
   id=$(gh api repos/{owner}/{repo}/issues/<child-number> --jq .id)
   gh api repos/{owner}/{repo}/issues/<root>/sub_issues -F sub_issue_id=$id
   ```
6. **Update the root** with the final group table and diagram (real numbers) using
   `gh issue edit <root> --body-file <path>`.

Fallbacks:

- If the sub-issues endpoint is unavailable (GitHub Enterprise Server without the feature, or missing permissions),
  do not fail: add a task list `- [ ] #<n> <title>` per sub-issue to the root body, and tell the user plainly that
  native sub-issue links were not created.
- If a step fails midway, stop, report exactly what was created (numbers and URLs) and what is left, and do not
  retry blindly or delete anything.

## Existing issue

When the input is an issue `#N`:

- `#N` stays the root; no new root is created.
- Rewrite its body from the root template, preserving the original text verbatim under **Original description**.
- Show the user the rewritten body and obtain explicit confirmation (it is part of the Step 6 question, and ask
  again if the body changed afterwards) before running `gh issue edit <N> --body-file <path>`. The original body is
  never discarded; keep a copy in the report so it can be restored.
- The milestone is looked up or created in Step 7 (steps 1 and 3) and added with `gh issue edit <N> --milestone`,
  in the same call as the body edit or a separate one.

## Step 8 — Report

Give the user the milestone URL, the root issue number and URL, and a table of sub-issues (number, title, group,
blocked by). Mention any fallback used. Suggest `/iru-issue <n>` for a group-1 sub-issue to start; issues in the
same group can be worked in parallel.

## Verification

Read-only calls verified against `albertoirurueta/ai-catalog`:

- `gh label list` prints tab-separated `name, description, color` (only the GitHub default labels exist there).
- `gh api repos/{owner}/{repo}/milestones` returns `[]` (HTTP 200) when there are no open milestones; it lists open
  milestones only by default, so pass `-f state=all` (as a query, with `--method GET`) to also detect closed ones
  before reusing a title.
- `gh api repos/{owner}/{repo}/issues/<n>/sub_issues` returns `[]` (HTTP 200) for an existing issue without
  sub-issues, and `404 Not Found` only when the issue itself does not exist. An empty array therefore means "no
  sub-issues", not "feature unavailable"; a 404 on an existing issue number would be the unavailable signal.
- `gh issue view <n> --json id` returns the GraphQL node id (string), while `gh api repos/{owner}/{repo}/issues/<n>`
  returns the numeric `id` (e.g. 5866905130) required as `sub_issue_id`; always use the REST `.id` for linking.
- `gh issue view <n> --json ...` on a nonexistent number fails with a GraphQL "Could not resolve" error.

Unverified (written from the GitHub documentation; no scratch repository was available): `gh issue create`, the
milestone POST, the sub-issue POST and `gh issue edit` / `gh issue comment`.
