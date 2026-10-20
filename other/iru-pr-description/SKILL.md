---
name: iru-pr-description
description: Check the current branch's code changes and draft a brief, concise pull request description (emojis and diagrams allowed where they genuinely clarify). Detects which platform hosts the repository — GitHub, Bitbucket, Azure DevOps, or TFS — and uses that platform's own tooling throughout instead of assuming `gh`/GitHub. Resolves the base branch the diff is described against — and that a new pull request would target — from an explicit `base-branch` argument, an `iru-issue` run earlier in the same conversation, a `Base branch:` line in `implementation_plan.md` (or its archived copy), or, failing all of those, the repository's default branch — so a PR opened through the `iru-issue` pipeline targets the base the user confirmed there instead of a re-derived one. If a pull request already exists for the current branch, offers to update its body with the draft; otherwise asks whether to commit the changes to a new branch and open a new pull request, prompting for branch name, destination branch, and PR title. Invoke as `/iru-pr-description`, optionally with a `base-branch` argument (as a `key`/`value` line, e.g. `base-branch` followed by the branch name) to pin the base explicitly. Use whenever the user wants a PR description generated from the actual diff instead of writing it by hand.
model: sonnet
---

# PR Description

Draft a pull request description from the real code changes, then either apply it to an existing PR or help open
a new one. This skill never pushes, commits, or opens/edits a PR without the user explicitly confirming the
specific action first.

## Step 1 — Determine the repository host and available tooling

Before touching any PR, determine which platform hosts this repository, so the right tool is used throughout
instead of assuming GitHub/`gh`:

- If `iru-explore` already ran earlier in this conversation (e.g. this skill was invoked as part of `iru-issue`, after its
  Step 5 exploration), reuse the `Repository host: ...` line from its Tech stack report rather than re-detecting.
- Otherwise, detect it directly — the same way `iru-explore`'s own Step 2 does: get the remote URL (`git remote
  get-url origin`, falling back to `git remote -v` or whichever remote the current branch tracks) and match it
  against known patterns:
  - `github.com` (or a GitHub Enterprise Server domain) → **GitHub**. Tooling: the `gh` CLI, or GitHub MCP tools
    (`ToolSearch` "github").
  - `bitbucket.org` (cloud), or a self-hosted domain with a `/scm/<project>/<repo>.git` path (Bitbucket
    Server/Data Center) → **Bitbucket**. Tooling: search for Bitbucket MCP tools first (`ToolSearch` "bitbucket"),
    otherwise the Bitbucket REST API.
  - `dev.azure.com` or `<org>.visualstudio.com` → **Azure DevOps (cloud)**. Tooling: `az repos` (the Azure CLI
    with the `azure-devops` extension) if installed, or Azure DevOps MCP tools (`ToolSearch` "azure devops").
  - A self-hosted domain with a `/tfs/` path segment, or bare `_git` in the path without a `dev.azure.com`/
    `visualstudio.com` domain → **Azure DevOps Server / TFS**. Same tooling family as Azure DevOps, but confirm
    the collection URL and API version before assuming parity.
  - If the URL doesn't clearly match any of these, ask the user (`AskUserQuestion`) which platform it is rather
    than guessing.
- If there's no remote configured at all, tell the user a PR can't be inspected or created without a hosted
  remote, and stop — every step from here on assumes one exists (or will, once the branch is pushed).

Record the detected host — every later step's "use the host's tool" instruction refers back to this.

## Step 2 — Determine the diff to describe, then delegate drafting

- Determine the current branch: `git branch --show-current`.
- Determine `<base-branch>` — the branch this work forks from, which is both the range the diff is read against
  and the default destination for a new pull request in Step 6. Take the **first** of these that yields a branch,
  rather than deriving it from the repository's default branch straight away: when this skill runs as part of the
  `iru-issue` pipeline, the base was already resolved and confirmed with the user there, and re-deriving it here
  would silently describe (and target) a different base than the work was actually branched from.
  1. **An explicit `base-branch: <name>` line in this skill's `args`** — how `iru-issue` (Step 8) and `iru-release`
     (Step 14) hand over the base they already resolved. Authoritative: use it verbatim, don't re-derive.
  2. **`iru-issue` ran earlier in this conversation** — reuse the `<base-branch>` it resolved and confirmed in its
     own Step 4.2, the same way Step 1 above reuses `iru-explore`'s repository-host detection.
  3. **A `Base branch: <name>` line in the plan's "Task summary"** — read `implementation_plan.md` at the
     repository root, or, if it's already been archived by a finished `iru-code` run, the most recent
     `.archive/implementation_plan_*.md`. This is what carries the choice across sessions, for the case where the
     user reviewed the plan manually and came back to run `/iru-code` and `/iru-pr-description` themselves later.
  4. **Otherwise, derive it**: `git symbolic-ref refs/remotes/origin/HEAD` (strip the `refs/remotes/origin/`
     prefix), falling back to `main`/`master` if that ref isn't set, or asking the user if genuinely ambiguous.
  Note which of the four supplied the base — Step 7 reports it, so a wrong inherited value is visible rather than
  silently applied.
- Check whether there's anything to describe at all, without reading the full diff yet: `git status`, `git diff
  --stat`, and `git diff <base-branch>...HEAD --stat`. If all three come back empty (no commits ahead of base, no
  staged/unstaged changes, no untracked files), tell the user and stop rather than inventing a description.
- Otherwise, delegate reading the full diff and drafting the description to a sub-agent, so the raw diff stays out
  of this conversation and only the drafted text comes back — nothing later in this skill needs the diff itself,
  only the draft:

  ```
  Agent({
    description: "Draft PR description from diff",
    prompt: "Read the full diff for this repository: commits already on the current branch (<current-branch>) but
      not on <base-branch> (git diff <base-branch>...HEAD), plus anything not yet committed (git status, git diff,
      git diff --staged), and recent commit messages for context on intent (git log --oneline against the same
      range). Draft a brief, concise pull request description grounded in what actually changed: one or two
      summary sentences, then a short bulleted list of the concrete changes if there is more than one logical
      change (omit any section that would be empty or redundant). Emojis are fine, used sparingly — one per bullet
      to categorize (✨ feature, 🐛 fix, ♻️ refactor, 📝 docs, ✅ tests) —
      don't overuse them. A small Mermaid diagram (a fenced ```mermaid block) is fine when a change reshapes
      control/data flow in a way a diagram clarifies faster than prose; skip it for straightforward changes
      regardless — most PRs don't need one. Don't invent behavior that isn't in the diff, and don't editorialize
      about code quality. Report back only the drafted description text — not the diff or commit log.",
    run_in_background: false
  })
  ```

  Reading a large diff directly into this conversation, when only the compact draft is ever used afterward, is
  the same class of waste `iru-gate-runner`/`iru-change-summarizer` already solve elsewhere in this catalog for other
  skills — a plain, unnamed sub-agent is enough here since this is a single, localized delegation rather than a
  shape repeated across several skills.

## Step 3 — Check whether a pull request already exists

Use the tool matching the host detected in Step 1:

- **GitHub**:
  ```bash
  gh pr view --json number,title,url,baseRefName,headRefName,body 2>/dev/null
  ```
  If that returns nothing (e.g. the branch hasn't been pushed yet), also try:
  ```bash
  gh pr list --head <branch> --json number,url,title,baseRefName,body
  ```
  If `gh` is unavailable/unauthenticated, search for GitHub MCP tools instead (`ToolSearch` "github pull
  request").
- **Bitbucket**: look up open pull requests via Bitbucket MCP tools if connected, otherwise the REST API (`GET
  /2.0/repositories/<workspace>/<repo>/pullrequests?q=source.branch.name="<branch>"` for Cloud, or the Server/Data
  Center equivalent) — find the one whose source branch matches the current branch.
- **Azure DevOps / TFS**: `az repos pr list --source-branch <branch> --status active`, or Azure DevOps MCP tools
  if connected — find the one matching the current branch.

If no tool for the detected host is available at all (no CLI installed/authenticated and no matching MCP
connection), tell the user and treat this as "no PR exists" — skip straight to Step 4, and in Step 6 only offer
the printed description rather than attempting to create one.

## Step 4 — Show the draft to the user

The description itself was already drafted by Step 2's sub-agent, grounded in the actual diff and recent commit
messages. Before taking any further action: show it to the user as-is, and if the repository host is Bitbucket
(from Step 1), strip or flag any Mermaid block first — GitHub and Azure DevOps render Mermaid natively in PR/
description bodies, Bitbucket does not.

## Step 5 — Existing PR: offer to update it

If Step 3 found an existing PR:

- Show its number, URL, and current body next to the new draft.
- Ask the user whether to replace the PR's body with the draft.
- If yes: apply it with the tool matching the host detected in Step 1:
  - **GitHub**: write the draft to a temp file and run `gh pr edit <number> --body-file <path>` (a temp file
    avoids shell-quoting issues with multi-line/Markdown content).
  - **Bitbucket**: update the description via Bitbucket MCP tools if connected, otherwise a REST API call to the
    pull request's update endpoint with the new description field.
  - **Azure DevOps / TFS**: `az repos pr update --id <number> --description "$(cat <path>)"`, or Azure DevOps MCP
    tools if connected.
  This edits shared, visible state — proceed only after the user's explicit yes.
- If no: stop — the draft has already been shown, there's nothing else to do.

## Step 6 — No PR: offer to commit and open one

If Step 3 found no existing PR, ask the user (via `AskUserQuestion`) whether they want to commit the current
changes to a new branch and open a pull request now, or just keep the drafted description for manual use.
Creating branches, committing, pushing, and opening a PR are all visible and/or hard-to-reverse actions — never
do any of them without this explicit confirmation.

If they decline: stop — the draft from Step 4 is the deliverable.

If they accept, collect the specifics via `AskUserQuestion`, offering an inferred default for each so the user
can accept or override in one step:

- **Branch name** — default: when the work resolves a known GitHub issue or Jira ticket (a `Source:` line in the
  plan's "Task summary" — the same `implementation_plan.md` or archived copy Step 2 reads — or a ticket handled
  earlier in this conversation), follow the same convention `iru-issue` uses:
  `feature/<ticket-id>-<slug>` or `hotfix/<ticket-id>-<slug>`, where `<ticket-id>` is the bare issue number or the
  Jira key (`42`, `PROJ-123`), the prefix is `hotfix` for a bug fix and `feature` otherwise (judged from the
  ticket/draft), and `<slug>` is a short kebab-case summary of the ticket title (e.g.
  `hotfix/PROJ-123-login-fails-after-session-timeout`). With no ticket, a kebab-case slug derived from the draft's
  summary (e.g. `fix-list-item-move-detection`). If the current branch is already a non-default branch with commits ahead of
  base and no uncommitted changes, ask instead whether to reuse it rather than creating a new one — except when
  the current branch matches `claude/*`, the throwaway per-session branch of a Claude Code cloud/web run: say so
  and default to a new, properly named branch instead of offering to reuse it.
- **Destination branch** — default: `<base-branch>` as resolved in Step 2. Still ask (this step opens a PR), but
  pre-select that value rather than re-deriving the repository's default branch here. Never default to a
  `claude/*` branch as a destination.
- **Pull request title** — default: a concise, imperative one-liner derived from the draft.

Then, in order:

1. If there are uncommitted changes, create the branch (`git checkout -b <branch-name>`), stage the relevant
   files by name (avoid `git add -A`/`git add .`, and check contents of anything unfamiliar before staging in
   case it holds secrets), and commit with a message consistent with this repo's recent style
   (`git log --oneline -10` for reference). If reusing the current branch per the note above, skip straight to
   step 2.
2. Push the branch: `git push -u origin <branch-name>`.
3. Write the Step 4 draft to a temp file and open the PR with the tool matching the host detected in Step 1:
   - **GitHub**: `gh pr create --base <destination-branch> --head <branch-name> --title "<title>" --body-file
     <path>`.
   - **Bitbucket**: Bitbucket MCP tools if connected, otherwise `POST
     /2.0/repositories/<workspace>/<repo>/pullrequests` (Cloud) or the Server/Data Center equivalent, with the
     title, the temp file's content as the description, the source branch, and the destination branch.
   - **Azure DevOps / TFS**: `az repos pr create --target-branch <destination-branch> --source-branch
     <branch-name> --title "<title>" --description "$(cat <path>)"`, or Azure DevOps MCP tools if connected.
4. Report the PR URL: the create command's own output for GitHub/Azure CLI; the API/MCP response's web link for
   Bitbucket; or `az repos pr show --id <id> --query "_links.web.href" -o tsv` for Azure DevOps/TFS if the create
   step didn't already surface it.

## Step 7 — Report

Summarize what happened: the drafted description, the `<base-branch>` used and which of Step 2's four sources it
came from (explicit `args`, an `iru-issue` run earlier in this conversation, the plan's `Base branch:` line, or
derived from the repository default), and the outcome — PR body updated (with URL), new PR created (with URL), or
description-only with no further action taken.
