---
name: legion-retro
description: Use when an issue has passed review and its parked implementer is revived for the mandatory pre-merge Legion retrospective.
---

# Legion Retro

Retro is mandatory for every issue that passed review. The architect revives the parked
implementer so the person with implementation context performs the retrospective, and the
skill obtains a separate fresh-eyes perspective. Retro runs before merge.

Every path this skill cites (`packages/...`, `docs/...`) is in sjawhar/legion, the Legion
repository, which need not be the repository you are working in.

## Merge-gate ordering

Follow this ordering exactly. It keeps the reviewed branch clean while preserving the
retrospective's durable output.

1. Tester green and all code-review cycles finish.
2. The implementer pushes the `.legion/` deletion at the reviewer's direction, and the reviewer
   approves that head.
3. Run this retro: commit durable learnings to `docs/solutions/` and post the retro message on
   the Dispatch issue.
   Retro writes **no `.legion` file**, so it never re-dirties the cleaned handoff tree.
4. The merger verifies the tip is the approved head plus commits that change only
   `docs/solutions/` — `jj diff --from <approved-sha> --to <tip-sha> --summary`, quoted in READY —
   posts `READY` on the Dispatch issue, and publishes the same packet to the project's merge-queue
   role when configured. A human merges under the repository's GitHub branch-protection and
   CODEOWNERS requirements; GitHub's merge queue participates only when the repository enables it.
5. After that merge, the implementer — not the reviewer or merger — verifies the change in production
   and records it on the PR and the issue: the agent that developed it is responsible for testing
   in production. The architect's sign-off waits for that record.
   The record is the pull request's `Production:` line, one pull-request comment, and a
   `dispatch_message` on the issue, each naming what was driven, how, what was observed, and the
   merge commit. A defect the production check finds becomes a corrective child issue of the same tree,
   owned by the architect and implemented by the same implementer; the parent stays open until it lands.

Retro's commit sits above the reviewer's approved head and the approval stands: a commit that
changes only `docs/solutions/` does not void it, and the tree goes from retro to the merger —
never back to the tester or reviewer. A conflict-forced rebase after retro moves these documents
with the branch; retro does not re-run.

Do not start retro before step 2, skip it because the change seems mechanical, or publish `READY`
before step 3. The design gate is not a substitute for review and retro.

## Two perspectives

1. Re-read the issue, its acceptance criteria, the PR, test evidence, and review evidence.
   Confirm the PR carries both proofs: the implementer's own `E2E (implementer)` line and the tester's `E2E (tester)` line,
   each naming a production-like surface (the daemon's test harness (`packages/daemon/src/daemon/__tests__/`) and real-process fixtures; a live check at the operator's next daemon restart, recorded on the PR; a sandbox repository, a devN
   stack, staging, or a local stack with real migrations), a command or run id, an observation, a head
   SHA, and a negative control. If either is missing, or links only a unit suite, the retro's first
   durable learning is that gap and the issue goes back — to the implementer for its own proof, to the
   tester for the tester's — before `READY`.
   Do not rebase or create a new branch; work on the existing issue branch.
2. Spawn one fresh-eyes subagent. Give it the issue and PR, ask it to inspect the diff and
   return concrete reusable learnings, and require it to return analysis rather than edit files.
3. Independently record the implementer's perspective: surprising constraints, difficult
   decisions, failed approaches, and reusable patterns.
4. Integrate the two perspectives. The implementer owns the final judgment: reject generic or
   context-free suggestions and preserve only learning that will help a future worker.

## Durable outputs

Write the integrated learning as one or more discoverable documents under `docs/solutions/`.
Organize by reusable topic rather than by pull request. Search `docs/solutions/` for the topic
first: when a document already states the rule, update it in place (sharpen the rule, add this
issue and pull request to `related_issues`) rather than writing a sibling; when the new learning
replaces an old document, set the old one's `status: superseded` and add
`superseded_by: docs/solutions/<path>.md`. Open each document with the rule in a few imperative
lines; the incident that taught it goes in an Evidence section below, never in the rule. Each
document uses this front matter:

```yaml
---
title: "Descriptive title matching the H1"
category: subdirectory-name
tags:
  - searchable-topic
date: YYYY-MM-DD
status: active
module: affected-module
related_issues:
  - "LEGION-123"      # the Dispatch issue
  - "owner/repo#456"  # the pull request
---
```

Commit the documentation on the existing issue branch, advance its existing bookmark, and push
that branch. Do not create a replacement branch or bookmark. Then post one Dispatch message on
the issue — `issue` is your `LEGION_ISSUE`; Legion issues live on Dispatch, never on a GitHub
issue, and the `gh` shim refuses every GitHub-issue write — naming the documents, the
one-to-three most useful takeaways, the two proofs you read, and the production check that
follows the merge. The message must carry this revived implementer's structured
attribution footer with `phase` set to `retro`; the body is capped at 2,000 characters:

```ts
dispatch_message({
  issue: "<KEY>",
  body: `## Retro Complete

**Learnings documented in:**
- docs/solutions/<path>.md

**Key takeaways:**
- <reusable lesson>

**Proofs read:** implementer <surface/command>, tester <surface/command>.

**Production check:** <what the implementer will drive after the merge, or the deploy/restart step a human will have to perform first>

<!-- legion: {"session":"<session-id>","phase":"retro"} -->`,
})
```

The Dispatch message and the `docs/solutions/` commit are the only retro outputs. Never write a
handoff, phase artifact, local feedback log, or completion label; `.legion/` was deleted before
retro and nothing recreates it. Report completion with the `legion` tool's `handoff_complete` alone (its
summary: two sentences for the architect) — no `handoff_write`.

## Completion check

Before returning, verify all of the following:

- The reviewer cleanup commit remains below the retro documentation commit, and the reviewer's
  approval of that cleanup head stands: the merger accepts the approved head plus this commit.
- The learning documents and the Dispatch message both exist (never a GitHub issue comment).
- Both proofs were read, and any gap in either is recorded as a learning.
- No `.legion` file was created or modified by retro.
- The fresh-eyes analysis was considered alongside the implementer's context.
- The merger remains a subsequent step, not work performed by retro.
