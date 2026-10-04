---
name: address
description: Work through review comments on the current PR. Triages each comment as Address / Push-back / Escalate and executes immediately — no approval gate. Addressed comments produce code changes, commits, and silent thread resolution via GraphQL (no reply text). Pushed-back comments stay unresolved. Escalations invoke /interview or /architect inline. Watches GitHub Actions after push — the loop is not complete until all checks pass.
---

# /address

Before rendering user-facing output, read `../_shared/plain-output.md`.

Work through pull-request review comments. You are empowered to push back on any comment — from `/code-review`, from humans, from anyone — when it conflicts with the locked architecture or AGENTS.md principles. **Autonomous: decide the triage, print it for transparency, execute immediately.** No approval gate.

## Preconditions

- A PR must exist for the current branch.
- `gh` authenticated.
- Working tree clean — uncommitted changes would confuse the commit-per-comment flow. If dirty, tell the user to commit or stash and stop.

## Phase A — Load

Resolve repo owner/name once:

```bash
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
PR="$(gh pr view --json number -q .number)"
```

Fetch all review threads with their resolved state and node IDs (needed for GraphQL resolve):

```bash
gh api graphql -F owner="${REPO%/*}" -F name="${REPO#*/}" -F number="$PR" -f query='
query($owner:String!,$name:String!,$number:Int!){
  repository(owner:$owner,name:$name){
    pullRequest(number:$number){
      reviewThreads(first:100){
        nodes{
          id
          isResolved
          path
          line
          comments(first:50){
            nodes{ id body author{login} url }
          }
        }
      }
    }
  }
}'
```

Also fetch general PR comments (issue-level, not tied to a line):

```bash
gh api "repos/${REPO}/issues/${PR}/comments"
```

Build one working list: `[{thread_id, reviewer, file, line, body, url, is_resolved}]`. Skip threads where `isResolved = true`.

## Phase B — Triage (autonomous)

For each unresolved comment, decide one of:

- **Address** — the comment is valid and aligned with the locked architecture. The code should change.
- **Push back** — the comment conflicts with the locked architecture / the issue's goal / AGENTS.md principles. The code should NOT change for this comment. No reply will be posted; the thread stays visibly unresolved.
- **Escalate** — the comment surfaces something non-trivial that requires re-thinking. Examples: questions the core problem framing, suggests a fundamentally different module boundary, exposes an assumption that was never pressure-tested.

Present the triage to the user as a table:

```
#   Reviewer         Verdict      File:Line              One-line reason
1   kieran           Address      src/foo.ts:42          Missing null check on optional arg
2   automated        Push back    src/bar.ts:17          Suggests shallow wrapper; architecture deliberately avoids
3   reviewer-bot     Escalate     src/baz.ts:9           Challenges the module boundary — needs /architect pass
...
```

Print the table, then proceed straight to Phase C / D. **Do not stop for approval.** The user can interrupt if they disagree — silence is consent.

For every Push-back row, the one-line reason must cite the specific principle / architecture decision / AGENTS.md rule the comment conflicts with. Pushback is a public, durable signal; it has to be defensible without you in the room.

## Phase C — Escalate

For any comment marked Escalate, handle inline before executing the others:

- If the comment is a problem-shape question → invoke the `/interview` skill with the comment body as the starting context.
- If the comment is an architecture question → invoke the `/architect` skill with the comment body as context, then run `/review`.

The output of an escalation may change the locked architecture. If it does:
1. Update the linked issue body via `gh issue edit`.
2. Re-triage all comments in light of the new architecture — some previously-Address comments may become Push-back, and vice versa.
3. Print the updated triage table and continue executing. No approval gate.

## Phase D — Execute (for Address comments)

For each comment marked Address, in order:

1. Read the file at the line.
2. Make the minimal code change that addresses the finding.
3. Run the tightest available verification loop (type-check, tests for the changed file). If verification fails, stop and surface the failure to the user — do not silently skip.
4. Commit:

```
review: <one-line summary of what changed>

Addresses <thread-url>
```

One commit per addressed comment. Do not batch.

## Phase E — Push & resolve

1. Push the new commits:

```bash
git push
```

2. For each successfully Addressed thread, resolve it silently via GraphQL. **No reply body.**

```bash
gh api graphql -F threadId="<thread_node_id>" -f query='
mutation($threadId:ID!){
  resolveReviewThread(input:{threadId:$threadId}){
    thread{ isResolved }
  }
}'
```

Verify `isResolved: true` in the response.

3. For each Push-back thread: do **nothing**. No reply. No resolve. The thread stays unresolved — the reviewer can see the agent did not take the suggestion and can follow up if they want to escalate.

## Phase F — Wait for GitHub Actions

After the push, do not hand off until CI terminates. The address loop is not complete until all checks pass.

```bash
gh pr checks "${PR}" --watch --fail-fast
```

- `--watch` blocks until every check finishes. `--fail-fast` exits on the first failure.
- If `gh pr checks` reports "no checks reported on the <branch> branch", treat as pass and continue.
- If any check fails:
  1. Identify the failing check(s) via `gh pr checks "${PR}" --json name,state,link -q '.[]|select(.state=="FAILURE")'`.
  2. Pull the last failed job log: `gh run view <run-id> --log-failed`.
  3. Decide whether the failure is caused by one of the addressed commits or is unrelated.
  4. If caused by an addressed commit: treat it like a new review comment — make a fix commit, push, and loop back to Phase E (re-resolve affected threads, re-watch CI).
  5. If unrelated infra: surface to the user, do not auto-fix, and do not post the handoff line. Tell the user: *"CI failed on an unrelated check (`<name>`). Resolve manually or re-run. Do not advance to `/learn` until CI is green."*

Do not retry checks automatically. Do not close the PR.

## Output

Use the Plain Senior shape:

````markdown
## Decision
Comments addressed or blocked by CI.

## Why
- addressed_resolved=<X>
- pushed_back_unresolved=<Y>
- escalated=<Z>

## Example
```bash
gh pr checks "${PR}" --watch --fail-fast
```

## Risk
<CI failure, unresolved pushback, or "None known">

## Next
<handoff line below>
````

If CI failed, do NOT print the handoff line — print the CI failure summary and stop.

On success (all checks green or no checks configured), end with exactly this line and stop:

> Comments addressed. CI green. Run `/code-review` again if more rounds are needed, or `/learn` to close the loop.

## Rules

- **Never post reply text.** The only communication channels this skill uses are: (a) commits that address the comment, (b) silent thread resolution, (c) unresolved threads as pushback signal.
- **Autonomous triage.** Decide, print the table for transparency, execute. No approval gate. The user can interrupt; silence is consent.
- **Pushback must cite a principle.** Every Push-back row's one-line reason names the specific rule it invokes (locked architecture, AGENTS.md principle, issue scope). Without a citable reason, the verdict becomes Address.
- **Escalation can invert the triage.** If escalation changes the architecture, previously-Address comments may become Push-back — re-print the updated table and keep executing.
- **One commit per addressed comment.** Makes it obvious which change answers which finding.
- **Grounding rules apply.** If a reviewer's suggestion references an API, verify it against docs before accepting the suggestion as valid.
