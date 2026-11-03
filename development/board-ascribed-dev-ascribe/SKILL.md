---
name: board
description: "Read Ascribe's project board, move a card on it, or approve a pull request, from a session that can't reach GitHub Projects. Use whenever work involves the board (https://github.com/orgs/ascribed-dev/projects/1): triaging, picking up, handing off, or reviewing a card, or when `gh project` or `gh pr` fails with \"GraphQL is not available\"."
---

# The project board

Ascribe's work is tracked on [the project board](https://github.com/orgs/ascribed-dev/projects/1). Each card is an issue in `ascribed-dev/ascribe`, and its **Status** is its column: Backlog, Ready, In progress, In review, Done. The project's instructions say who moves a card out of each column. The skills `triage`, `implement`, and `review` say how each role does its part.

A Claude cloud session can't reach the board itself. Its GitHub access covers this repository's REST API and nothing else: no GraphQL, so no `gh project`, and no `gh pr`, `gh issue`, or `gh repo` commands, which use GraphQL too. Two workflows reach the board for you, and their headers have the details: [`board.yml`](../../../.github/workflows/board.yml) and [`approve.yml`](../../../.github/workflows/approve.yml).

## Read the board

Start Board with the GitHub MCP tool `actions_run_trigger`, never `gh workflow run` in the shell: `method: "run_workflow"`, `owner: "ascribed-dev"`, `repo: "ascribe"`, `workflow_id: "board.yml"`, `ref: "main"`, and no `inputs` to only read. Inputs are always strings. Wait for the run with `actions_list` (`method: "list_workflow_runs"`, `resource_id: "board.yml"`), taking the newest run created after you started it, since other sessions run Board too, until it has completed, then read `board.json` from the branch `board`:

```sh
gh api 'repos/ascribed-dev/ascribe/contents/board.json?ref=board' --jq .content | base64 -d > board.json
```

`board.json` has the project, its fields with each single-select field's options, and every item. An item's `status` is its column, and `content` names its issue or pull request:

```sh
jq -r '.items[] | select(.status == "Ready") | "#\(.content.number) \(.content.title)"' board.json
```

A run writes `board.json` only when the board changed, so the file can be older than the run. That's expected; it's still current.

## Move a card

The same tool and workflow, with the issue and the Status by its name as the board shows it: `inputs: { issue: "123", status: "In review" }`.

Then wait for it as above. A failed run says why in its error, for instance a Status the board doesn't have. An issue or pull request that isn't on the board yet is added. Move only cards your role owns, and only to the next column.

Several cards going to the same Status move in one run, listed with spaces or commas: `inputs: { issue: "123 124 125", status: "Ready" }`.

A move doesn't read the board, so `board.json` stays as it was; add `read: "true"` to `inputs` to read it in the same run. Every call the workflow makes to the board counts against one token's hourly GraphQL limit, and a read lists the whole board, so use one run for a batch and read only when you need to. When a run fails on the limit, its log says `API rate limit exceeded` or `unknown owner type`: wait for the limit to reset instead of retrying in a loop, since every retry spends the same limit and so do other sessions'.

## Start cards that don't collide

The coordinator moves cards from Ready to In progress, up to the project's limit. Cards that change the same files at once make their implementors merge `main` over and over, renumber, and sometimes build the same fix twice, so it also holds back a card that would collide:

- **Read the card's `Touches:` line** in triage's report ([the `triage` skill](../triage/SKILL.md), step 6) before starting it.
- **Don't start a card while an In progress card names the same module.** Start it once that card's pull request is merged. Two cards in different modules of one crate can run together; the line names modules so that they can.
- **Start a plan's phases in order,** each once the one before is merged, unless the plan says two can run at once.

The files nearly every card touches, `changes/`, generated references, and `project-docs/surface.md`, don't count as a collision.

## Approve a pull request

Agents post as the maintainer, who also authors their pull requests, and GitHub doesn't let a pull request's author approve it. Approve posts the approval as `github-actions[bot]`, for the commit you reviewed.

Start it the same way, with `actions_run_trigger`: `method: "run_workflow"`, `owner: "ascribed-dev"`, `repo: "ascribe"`, `workflow_id: "approve.yml"`, `ref: "main"`, and `inputs: { pr: "123", sha: "<the full head commit you reviewed>" }`. In a cloud session, auto mode's safety check refuses the shell command as self-approval; the MCP tools are allowed by the environment.

Give the commit you reviewed, not a fresh fetch: Approve refuses when the pull request's head has moved past the commit you give it, so new commits always get a review first. Then find the run with `actions_list` (`method: "list_workflow_runs"`, `resource_id: "approve.yml"`), the newest run created after you started it, and check that it passed before you merge.

## Everything else on GitHub

Use the GitHub MCP tools, or `gh api` with a REST path, for issues and pull requests: reading them, commenting, reviewing, and opening a pull request. Merge with the MCP tool `merge_pull_request`, for the same reason as Approve: `merge_method: "merge"`, since this repository merges with a merge commit, and `expectedHeadSha` set to the head you approved, so a push since your review stops the merge.
