---
name: respond
description: Respond to incoming code review comments on a PR you authored. Fetches every unresolved comment across all channels, inline threads, review bodies, PR-level conversation, and commit comments, classifies each by author and intent, verifies against the current code, fixes what is real, replies only inside a human's inline thread, closes bot threads and unrepliable channels without a comment, and monitors CI. Use when user says "respond to review", "address comments", "handle reviewer feedback", "reply to PR comments", "my PR has comments", or wants a structured pass over reviewer feedback. For performing a review, use /review; for unattended CI and bot handling with no human threads, use /ship --pipeline.
argument-hint: "/respond [fetch | reply <thread-id> | resolve <thread-id>] [<PR number or URL>] [--humans-only] [--dry-run] [--re-request]"
allowed-tools: "Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion"
sensitive: true
---

## Overview

Receive-side counterpart to `/review`. Turns the loose, error-prone workflow of "respond to PR review comments" into a structured, validated pipeline. The seven phases take the user from "I see comments on my PR" to "every thread is answered or closed, code changes are validated and pushed, CI is green".

[`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md) governs everything this skill publishes. One reply surface: a human's inline thread, four sentences at most. Bot threads are read, fixed when the finding is real, then resolved in silence. The three channels with no reply endpoint are answered by the code change and closed by minimizing.

## When to Use

- A pull request the acting account authored has unanswered review comments in any channel.
- A reviewer asked for changes and the fixes, replies, and resolves need to land as one batch.
- `/morning` routed an authored pull request with open feedback here.

## Process

Seven phases, each detailed below: discover the pull request, fetch every channel, classify and verify each item, draft the strategy, present the batch for approval, execute it with code first and replies second, then monitor CI and close.

### Subcommand Routing

| Invocation | Action |
|-----------|--------|
| `/respond` | Full workflow on the current branch's PR |
| `/respond <PR>` | Same workflow targeting a specific PR number or URL |
| `/respond fetch` | Phase 1 to Phase 3 only. List threads with classification. No implementation, no posting |
| `/respond reply <thread-id>` | Reply to one specific thread. Skip the batch flow |
| `/respond resolve <thread-id>` | Resolve one specific thread. No reply |

If no subcommand is given, default to the full workflow.

## Arguments

| Flag | Effect |
|------|--------|
| No args | Use the current branch's PR |
| `<PR number or URL>` | Target that PR |
| `--include-bots` | Default. AI bot threads are in the workflow, for fixing and closing. Bot threads never receive a reply. Accepted for compatibility; passing it changes nothing |
| `--humans-only` | Skip threads whose first comment is from a bot |
| `--auto` | Execute the approved batch without per-batch confirmation. Requires `RESPOND_AUTO_ACK=1` env var to take effect |
| `--interactive` | Confirm per thread instead of per batch |
| `--filter <pattern>` | Filter threads by file path glob or author login |
| `--dry-run` | Run Phases 1 through 5, print the proposed actions, exit without executing |
| `--re-request` | Re-request review from the original reviewers after the batch ships |
| `--no-resolve` | Skip the resolution step |
| `--resolve-by <author\|reviewer>` | Resolution convention. Default `author`, opt-in `reviewer` |
| `--force-during-review` | Allow force-push even when an open CHANGES_REQUESTED review exists. Off by default |

## Phase 1: Discover PR

1. Run **in parallel**: `git remote get-url origin`, `git branch --show-current`, `git status --porcelain`.
2. Detect platform from the remote URL. Supported platforms: GitHub, GitLab, Bitbucket Cloud. The default workflow in this file documents GitHub. For GitLab specifics, read [`platform-gitlab.md`](platform-gitlab.md) and substitute the API surface. For Bitbucket Cloud, read [`platform-bitbucket.md`](platform-bitbucket.md) and substitute. The classification taxonomy, reply templates, and bot triage rules are identical across platforms.
3. Resolve the platform account per [`../../standards/multi-account-cli.md`](../../standards/multi-account-cli.md). GitHub uses `GH_TOKEN=$(gh auth token --user <account>) gh ...`. GitLab uses `GITLAB_TOKEN=$(glab auth token --hostname <host>) glab ...`. Bitbucket uses `BITBUCKET_TOKEN` or `BITBUCKET_USERNAME`+`BITBUCKET_APP_PASSWORD` via `curl`.
4. Resolve the PR. If an argument is passed, parse it. Otherwise look up the PR for the current branch.

   ```bash
   GH_TOKEN=$(gh auth token --user <account>) gh pr view \
     --json number,url,state,headRefOid,headRefName,baseRefName,author,reviewRequests \
     --jq '{number, url, state, headRefOid, head: .headRefName, base: .baseRefName, author: .author.login, requested: [.reviewRequests[].requestedReviewer.login]}'
   ```

5. Validate. If PR is `CLOSED` or `MERGED`, ask before proceeding. If no PR is found and no argument is passed, stop.
6. Warn on uncommitted changes that conflict with the working tree the skill will modify.
7. When the PR author is the acting account, run `python3 ~/.claude/hooks/ai-review-request.py --repo <owner/name> --pr <n> --account <account>` once. It subscribes the PR to every AI reviewer the repository supports and does nothing when that is already in place. The push in Phase 6 triggers the same check through the hook.

## Phase 2: Fetch Comments

Read [`../../standards/pr-comment-channels.md`](../../standards/pr-comment-channels.md) and use its canonical fetch verbatim. That standard is the single source of truth for what a PR comment is, on all three platforms. Do not hand-roll a narrower query here; a narrower query is exactly how the P0 deadlock report was missed.

The four GitHub channels, all mandatory:

| Bucket | Source | Native resolve |
|--------|--------|----------------|
| Inline threads | `reviewThreads`, `subjectType` `LINE` or `FILE` | Yes |
| Review bodies | `reviews` | No |
| PR-level conversation | `comments` | No |
| Commit comments | `timelineItems`, `PULL_REQUEST_COMMIT_COMMENT_THREAD` | No |

Fetch every review state, not only `[APPROVED, CHANGES_REQUESTED, COMMENTED]`. Filter states after fetching so a `DISMISSED` review carrying an unanswered question stays visible.

Filter rules.

- Drop only what the standard's Terminal States table marks terminal. Everything else is in scope.
- Never drop on `isOutdated` or `isCollapsed` alone. An outdated comment can still name a live bug.
- Honor `isMinimized == true`. It is the closest thing the three non-resolvable channels have to a resolve action, on any of the seven `minimizedReason` values.
- Keep bot items by default. Apply the human filter only when `--humans-only` is set. The human filter keeps items whose first comment classifies as `human` in Axis 1.
- Group inline threads by file path, then sort by line number within file. Group the other three buckets separately.
- Review bodies, PR-level comments, and commit comments get no reply. They are answered by the code change and closed by minimizing, per the standard's "Answering Each Channel" table.
- Filter out PR-level comments whose body starts with auto-generated markers such as `<!-- LEAD_APPROVAL -->`, `<!-- linear-linkback -->`, or `<!-- This is an auto-generated comment: summarize by coderabbit.ai -->`, since these are tracker or bot signals, not actionable.
- Drop items authored by the running account, your own prior replies unless they were quoted as part of a multi-round conversation.

Cross-check after fetch. Run the Completeness Cross-Check from the standard. Report per-channel counts in Phase 5, never a single total. The skill must never report "nothing to respond to" while a substantive comment in any channel is still unanswered.

Classify by login, because the canonical fetch returns `author { login }` and no author type. Match case-insensitively on a substring, with or without the `[bot]` suffix, since the GraphQL API omits it. AI bot allowlist, the same list `/ship` uses in its 6a step: `coderabbit`, `copilot`, `greptile`, `sourcery`, `korbit`, `bito`, `qodo`, `codium`, `cursor`, `tabnine`, `gemini-code-assist`, `chatgpt-codex-connector`, `claude`. Auxiliary lint or dependency bots: `github-actions`, `dependabot`, `renovate`, `pre-commit-ci`, `lefthook`.

## Phase 3: Classify and Verify

For each thread, classify on three axes.

### Axis 1: Author type

| Value | Detection |
|-------|-----------|
| `self` | Author login matches the resolved account |
| `bot:ai` | Login matches the AI bot allowlist |
| `bot:lint` | Login matches an auxiliary lint or dependency bot |
| `bot:other` | Login ends in `[bot]` or `-bot` and matches neither list. Report it; never treat it as human |
| `human` | No other row matches |

### Axis 2: Comment intent

Use the Conventional Comments taxonomy. When the reviewer used an explicit prefix like `nitpick:`, `suggestion:`, `issue:`, `question:`, `praise:`, `thought:`, `chore:`, or `todo:`, trust that prefix verbatim. Otherwise classify heuristically.

| Intent | Conventional Comments mapping | Keyword and structural signals |
|--------|------------------------------|--------------------------------|
| `issue:blocking-bug` | `issue (blocking)` | "this is broken", "will crash", "null pointer", "off-by-one", reproducer present |
| `issue:blocking-security` | `issue (security, blocking)` | "leak", "injection", "auth", "permission", "secret", "CVE", "credential" |
| `issue:blocking-correctness` | `issue (blocking)` | "wrong", "incorrect logic", "this returns", "should be" with a clear assertion |
| `issue:architectural` | `issue (non-blocking)` | "rethink", "different approach", "this whole pattern", "redesign" |
| `suggestion` | `suggestion` | "consider", "could", "what about", "alternatively" |
| `question` | `question` | Ends with `?`, "why did you", "how does this", "is this intentional" |
| `thought` | `thought` | Reflective, no requested action, "I wonder if", "musing" |
| `nitpick` | `nitpick` | Prefixed `nit:`, `nitpick:`, `style:`, very small scope |
| `praise` | `praise` | "nice", "good catch", "clean", no actionable content |
| `chore:out-of-scope` | `chore` | "separate PR", "follow-up", "out of scope". The intent is the reviewer's framing, never a licence to defer |
| `todo` | `todo` | "leave a TODO", reminder for the future, not for this PR |
| `clarification-request` | `question` | "what does this do", "can you explain", "I do not follow" |

### Axis 3: Action decision

Set by the verification step below.

| Decision | Meaning |
|----------|---------|
| `implement` | Comment is correct, apply the fix |
| `push-back` | Comment is incorrect, explain why |
| `clarify` | Need more info from reviewer before acting |
| `dismiss` | The finding does not hold. Bot threads mostly end here |
| `ack` | Acknowledge praise or info-only comment |
| `accept-with-modification` | Implement a variant of the suggestion |
| `conflict` | Two reviewers contradict on the same line. See Multi-Reviewer Conflict Resolution |

For `issue:blocking-*` intents, the decision space is restricted to `implement`, `push-back`, `clarify`.

There is no `defer` decision. A problem that can be fixed in this change is fixed in this change, and no ticket, follow-up, or separate pull request stands in for the fix. See [`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md) and [`../../rules/found-fix.md`](../../rules/found-fix.md). When a fix is genuinely blocked outside the change, such as a coordinated release or a migration another team owns, the decision is `push-back` and the reply names the blocker in one sentence.

### Verification step

For every thread classified as `issue:*`, `suggestion`, or `architectural`, read the cited file at the cited line, plus 50 lines of surrounding context. Verify against the current code, not against the code at the time the comment was posted.

| Check | Why |
|-------|-----|
| Does the cited code still exist? | If `isOutdated == true`, the comment may already be resolved by a later push |
| Does the cited code do what the reviewer claims? | False positives happen, especially with AI reviewers |
| Would the suggestion actually be better? | Apply the same criteria the `/review` skill uses |
| Are there hidden constraints the reviewer did not see, like tests, callers, or contracts? | Surfaces push-back cases with evidence |
| Can the bug be reproduced locally? | If not, the reply names the steps tried |

Output per thread: a classification record with author type, intent, decision, evidence, and a draft reply.

## Phase 4: Draft Strategy

For each thread, draft a reply and, when applicable, a code change.

### Step 1: Decide whether a reply exists at all

Author type decides this before a word is drafted, and it is recorded in the plan table.

| Author type | What gets published |
|-------------|---------------------|
| `human`, inline thread | A reply in the thread. The four principles below apply |
| `human`, other channel | No reply. The code change answers it; the commit names the point |
| `bot:ai`, `bot:lint`, `bot:other` | Nothing. Ever |
| `self` | Nothing |

A bot thread is read, verified against the code, fixed when the finding survives the failure-scenario gate in [`../../rules/ai-review-convergence.md`](../../rules/ai-review-convergence.md), and then resolved. No verdict line, no acknowledgment, no dismissal note.

The reasoning is the same reasoning that used to justify a short bot reply, carried to its conclusion. A bot has no stake to manage, cannot be persuaded, will not answer, does not remember the thread, and did not miss anything. An audience with none of those properties needs a shorter message only if it needs a message. It does not. What the verdict line was for, telling a later reader what happened, is carried better by the commit that closed the thread, and a commit outlives any thread.

Never write any of these to a bot thread:

| Never | Why |
|-------|-----|
| A reply of any length | Nothing reads it |
| A verdict such as fixed, declined, or false positive | The commit and the resolve state already say it |
| Second-person address | Addresses a party that is not present |
| Praise or agreement | Credits an agent for a pattern match |
| Argument or persuasion | A bot has no position to change |
| A question | Nothing will answer |

### The four principles below are for human inline threads only

Skip this whole section when the author is a bot. There is nothing to draft.

Every reply obeys the ceiling in [`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md): four sentences, polite in a clause, no restatement of the comment, no closing offer. A reviewer is a person with other work. Anything past the ceiling belongs in the code or the pull-request description.

### Principle 1: Fix the code before explaining it

When a reviewer did not understand, the code is the first thing to change. Renaming a confusing variable, extracting a helper, or adding a code-level comment beats writing a thread reply that future readers will not see.

### Principle 2: Lead with reasoning when pushing back

Bare "I disagree" is a known failure mode. Use the Feedback Equation pattern: Observation, Impact, Request. State what the code does, what would change if you took the reviewer's path, and what you want from the reviewer next.

Example. Observation: "The current code uses `setTimeout` instead of `requestAnimationFrame`." Impact: "Switching to `requestAnimationFrame` would skip the ping when the tab is backgrounded, breaking the keep-alive contract documented in `docs/keepalive.md`." Request: "Want me to name the constraint in the function itself, say `pingWhileTabBackgrounded`, or do you see a way to keep the behavior with a different API?"

### Principle 3: Switch to synchronous after two round trips

When a thread has cycled twice without convergence, propose a brief call. The skill does not initiate calls but tags the thread `synchronous-recommended` so the user can act on it.

### Principle 4: When you cannot reproduce, name the steps

"Couldn't reproduce" is a defensive wall. "Couldn't reproduce. Steps I tried: A, B, C. Did I miss something?" invites the reviewer to clarify.

### Reply templates

Full exemplars with good and bad counterparts live in [`reply-templates.md`](reply-templates.md).

**The table below applies to human inline threads only.** A bot thread has no wording to choose. The intent axis still drives the decision for a bot thread, which is then closed silently.

| Intent x Decision | Template summary |
|-------------------|-------------------|
| `issue:blocking-bug` x `implement` | "You're right. Pushed `<SHA>`. <one sentence on the fix>." Add a named regression test |
| `issue:blocking-bug` x `push-back` | Feedback Equation form. End with "Did I miss something?" |
| `issue:blocking-security` x `implement` | "You're right. Pushed `<SHA>` with <fix>." Any second defect the same comment exposed is fixed in the same push |
| `issue:blocking-correctness` x `clarify` | "Want to make sure I am reading this right. <One-line restatement>. Is that it?" |
| `issue:architectural` x `push-back` | "Landing this with the current approach. <Reason>. The redesign is worth its own thread." |
| `suggestion` x `implement` | "Good call. Applied in `<SHA>`." Credit trailer for non-trivial suggestions |
| `suggestion` x `accept-with-modification` | "Took a variant in `<SHA>`. <Difference from the original>." |
| `suggestion` x `push-back` | "Considered that. Went with the current approach because <reason>. The alternative would <downside>." |
| `question` x `ack` | "<Direct answer>." If the answer reveals confusing code, fix the code instead |
| `clarification-request` x `ack` | "<Plain explanation>." If non-trivial, make the code say it: rename, extract, or tighten the type |
| `nitpick` x `implement` | "Fixed in `<SHA>`." |
| `nitpick` x `push-back` | "Sticking with the current style for consistency with <other pattern>." |
| `chore:out-of-scope` x `implement` | The default. A change small enough to be called out of scope is small enough to make: "Fixed in `<SHA>`." |
| `chore:out-of-scope` x `push-back` | Only when the fix is blocked outside this change. "<The blocker>, so it cannot land here." No ticket |
| `todo` x `implement` | Do the work now. A marker recording it is banned by the comments policy |
| `praise` x `ack` | No reply. React with a thumbs-up on GitHub and resolve |
| Bot x any | Not this table. No reply exists. Fix a surviving finding, resolve the thread, move on |

Every template passes the no-internal-config-leakage check before posting.

### Code change planning

For `implement` and `accept-with-modification` decisions, draft the change at the line level. Record: the file path, the lines to modify, the new content, and the validation tests that must pass after.

For `issue:blocking-*` decisions, plan a named regression test like `it('rejects an empty companyId')`; the name states the behavior, never a ticket or PR number. Apply when the bug has a specific reproducer, the fix is a one-line guard whose absence could regress invisibly, or the bug was filed by a user or downstream team. Skip when the regression would be loud, like a compile error or a type error.

## Phase 5: Present and Approve

Print a batched table to the terminal. One row per item. Two columns are mandatory. `Channel` is what makes an omitted channel visible rather than invisible. `Reply` is what makes a banned post visible before it is sent: only an `inline` row with a `human` author may carry a preview, and every other row must read `none`. A preview on any other row is a drafting error to fix, not to approve.

```
#  Channel     Author          Type   Location               Intent                 Decision      Reply                          Code change
1  inline      alice           human  src/auth.ts:42         issue:blocking-bug     implement     "You're right. Pushed..."      +12 -3 in src/auth.ts
2  inline      bob             human  src/auth.ts:78         suggestion             push-back     "Considered that. Went..."     none
3  inline      coderabbitai    bot    src/orders.ts:120      nitpick                implement     none, resolve                  +1 -1 in src/orders.ts
4  review-body carol           human  review #4 CHANGES_REQ  issue:blocking-bug     implement     none, minimize                 +8 -1 in src/db.ts
5  pr-level    dave            human  conversation           issue:blocking-bug     implement     none, minimize                 +4 -2 in src/lock.ts
6  commit      erin            human  a1b2c3d src/api.ts     question               implement     none, minimize                 +3 -1 in src/api.ts
7  inline      copilot         bot    src/api.ts:12          suggestion             dismiss       none, resolve                  none
```

Row 6 shows the shape a question in an unrepliable channel takes: the answer is a code change that makes the question stop arising, and the commit message carries the point. When a change alone would leave the reviewer guessing, add the sentence to the pull-request description rather than opening a comment.

Close the table with per-channel counts so a zero is never ambiguous:

```
inline 3 | review bodies 1 | PR-level 1 | commit 1
```

If the batch exceeds 25 rows, paginate with `--filter` suggestions.

Prompt the user to approve the batch as a whole, edit a specific row, split into smaller batches, or abort. `--auto` plus the `RESPOND_AUTO_ACK=1` env var skips the prompt. `--interactive` shifts to per-row approval.

If `--dry-run`, stop here and exit.

## Phase 6: Execute Approved Batch

Order: code first, then reply, then resolve. Each step has its own checkpoint.

### Step 0: Re-read the pull request state

Teammates merge while a batch is being worked, so the state read in Phase 1 goes stale. Immediately before Step 1, Step 3, and Step 5, run `GH_TOKEN=$(gh auth token --user <account>) gh pr view <pr> --json state,mergedAt,headRefOid`. When `state` is `MERGED` or `CLOSED`, stop the batch, leave the working tree clean, and report who merged it and when. When `headRefOid` moved, fetch and review the new commits before continuing.

### Step 1: Apply code changes

Each thread's change becomes its own commit. Commit message format: `fix(<scope>): <one-line description>`. Body includes `Refs: <comment URL>`. Credit trailers per "Commit Credit Conventions" below.

### Step 2: Run the local quality gate

In order. Show output for each. If any fails, stop and report.

| Step | Detection |
|------|-----------|
| Format | `prettier --check`, `black --check`, `gofmt -l`, `rustfmt --check`, depending on the project |
| Lint | `eslint`, `ruff`, `golangci-lint`, `clippy --deny warnings`, depending on the project |
| Type check | `tsc --noEmit`, `mypy --strict`, `pyright`, depending on the project |
| Test | The project's full suite, with coverage if scripted |
| Build | The project's build command |

Use the same detection logic as `/ship pr` step 4.

### Step 3: Push once at the end

After all commits land cleanly. Use `-u` if no upstream is set. Use `--force-with-lease` only if a rebase rewrote history. Never use `--force`. If an open CHANGES_REQUESTED review exists on the PR, the push hooks block force unless `--force-during-review` was passed.

### Step 4: Re-fetch threads

Confirm the latest SHA is on the PR and no new threads landed during execution.

### Step 5: Post replies via REST

One reply surface. Every other row posts nothing.

| Channel | Reply mechanism |
|---------|-----------------|
| Inline thread, human author | `POST repos/<o>/<r>/pulls/<pr>/comments/<comment-id>/replies` |
| Inline thread, bot author | None |
| Review body, PR-level, commit comment | None. Step 6 closes them |

A reply about a visible fix embeds a high-resolution `After:` screenshot, and `Before:` when the reply explains what changed. The replies endpoint cannot attach, so upload first and reuse the URL, per "Visual Evidence In Published Text" in [`../../standards/frontend-render-gate.md`](../../standards/frontend-render-gate.md):

```bash
GH_TOKEN=$(gh auth token --user <account>) gh pr edit <pr> --attach 'after.png#After: <screen>'
GH_TOKEN=$(gh auth token --user <account>) gh pr view <pr> --json body --jq .body
```

Copy the uploaded URL into the reply body as `![After: <screen>](<url>)`.

Write a JSON file to `/tmp/respond-reply-<thread-id>.json`. Single-quoted heredoc to prevent shell expansion.

```bash
cat <<'PAYLOAD' > /tmp/respond-reply-<thread-id>.json
{
  "body": "<draft reply body, includes the fix SHA>"
}
PAYLOAD

GH_TOKEN=$(gh auth token --user <account>) gh api \
  repos/<owner>/<repo>/pulls/<pr>/comments/<comment-id>/replies \
  -X POST \
  --input /tmp/respond-reply-<thread-id>.json
```

### Step 6: Close every item

Only inline threads can be resolved. For each inline thread whose decision is `implement`, `push-back`, `accept-with-modification`, `ack`, or `dismiss`, post the reply first when one exists, then resolve. Threads with decision `clarify` stay open. Threads with decision `conflict` stay open until the conflicting reviewers align.

```bash
GH_TOKEN=$(gh auth token --user <account>) gh api graphql \
  -f query='mutation($threadId: ID!) {
    resolveReviewThread(input: { threadId: $threadId }) {
      thread { id, isResolved }
    }
  }' -F threadId=<thread-id>
```

One resolve per thread. The `bulk-resolve-blocker.py` hook enforces this.

Review bodies, PR-level comments, commit comments, and bot comments outside a resolvable thread are closed by minimizing, since they have no resolve action and get no reply:

```bash
GH_TOKEN=$(gh auth token --user <account>) gh api graphql \
  -f query='mutation($id: ID!) {
    minimizeComment(input: { subjectId: $id, classifier: RESOLVED }) {
      minimizedComment { isMinimized, minimizedReason }
    }
  }' -F id=<node-id>
```

Minimize only after the change that answers the comment has landed. Use `RESOLVED` when a change settled the point and `OUTDATED` when the cited code is gone. Never `SPAM`, `ABUSE`, or `LOW_QUALITY` on a human comment. When minimizing is unavailable, such as on a repository where the account lacks the permission, leave the item open and say so in the final report rather than posting a comment to mark it handled.

### Step 7: Re-request review

If `--re-request` was passed.

```bash
GH_TOKEN=$(gh auth token --user <account>) gh api \
  repos/<owner>/<repo>/pulls/<pr>/requested_reviewers \
  -X POST \
  -f reviewers='["alice","bob"]'
```

The re-request is the whole signal. What changed since the last round belongs in the pull-request description, which the reviewer reads anyway, never in a fresh comment.

### Step 8: Clean up

```bash
rm /tmp/respond-reply-*.json /tmp/respond-query-*.graphql
```

## Phase 7: Monitor and Close

After every push triggered by the batch, enter the Pipeline Monitoring loop from `/ship`. Reuse the same loop as a shared procedure. Loop until CI is green on the latest SHA AND no new threads have appeared since the last fetch. Bot threads that appear after the push go through the same triage, unless `--humans-only` was set, in which case they are deferred to `/ship --pipeline`.

Final output:

```
RESOLVED: 7 comments addressed on PR #1234.
  Channels swept: inline 4 | review bodies 1 | PR-level 1 | commit 1
  - 4 implemented (commits: a1b2c3d, e4f5g6h, i7j8k9l, m0n1o2p)
  - 2 pushed back with reasoning
  - 1 dismissed after the finding did not hold
  Replies posted: 2, both in human inline threads
  Inline threads resolved: 4. Unrepliable channels minimized: 3
  CI: 12 of 12 checks passed
  Re-requested review from: alice, bob
```

The "Channels swept" line is mandatory. It is the evidence that all four channels were queried, and it is the line a user can check when they suspect a comment was missed.

Before writing `RESOLVED:`, count the done state with the query in "The Done State" of [`standards/pr-comment-discipline.md`](../../standards/pr-comment-discipline.md): zero unresolved review threads and zero bot review bodies left unminimized. Bot status comments, such as previews, coverage reports, lead-approval markers and Linear links, are not review comments and stay visible. A nonzero count means the pass is not done.

## Service Level Expectations

The skill embeds the cycle-time discipline from Google eng-practices and Pragmatic Engineer.

| Action | Target |
|--------|--------|
| Acknowledge a human review comment | Within 4 hours of becoming aware |
| First substantive response to a batch | Within 1 business day |
| Batch responses, single push | One push covers all approved replies and fixes for the round |
| Re-request review after addressing | The explicit re-request. No accompanying comment |
| Synchronous escalation | After two round trips with no convergence |
| Stale PR handling | If no movement for 7 days, the author either pushes a status update or closes the PR |

The skill enforces these by surfacing reminders, never by acting unilaterally. When a thread has been open for more than 4 hours without acknowledgment, the skill prints a notice. When a PR has been idle for more than 7 days, the skill suggests a status update or closure.

## AI Bot Triage Tactics

Full pattern catalog with per-tool false positives lives in [`bot-triage.md`](bot-triage.md). The summary below is the operational ruleset for bot threads, which are in scope unless `--humans-only` is set.

### Severity baseline

Treat every AI-bot comment as P3 until corroborated by a human reviewer or by a verification check. Independent audits show CodeRabbit precision around 50%, Greptile with the highest catch rate but also the highest false-positive rate, Copilot reporting 71% actionable.

### Known false-positive patterns

| Pattern | Common origin |
|---------|---------------|
| Style suggestion that contradicts the project's lint config | CodeRabbit, Sourcery |
| Imagined APIs, like suggesting a `lodash` helper in a project that bans lodash | CodeRabbit |
| "Add a try/catch" on code that intentionally propagates the error | Multiple bots |
| Security warning on input already validated upstream | CodeRabbit, Greptile |
| "Add JSDoc" in a project whose convention is types-as-docs | CodeRabbit |
| Refactor suggestion that does not compile under TypeScript strict | All bots |
| "Consider using async/await" on code that already uses it | Copilot |

### A wrong bot finding is closed, never answered

Resolve the thread and move on. Nothing is written into it.

Some tools claim to learn from a written dismissal over two to four weeks. The claim is unverified here, and it is the only argument that ever favored writing to a bot. Weighed against a reply on every false positive, on every pull request, for a reader who does not exist, the trade is not worth taking. When a bot repeatedly misses a project rule, the fix is the tool's own configuration file, which is durable, rather than a comment that is not.

### Commands cheat sheet

| Command | Effect |
|---------|--------|
| `@coderabbitai pause` in the PR description | Pauses re-review during heavy iteration. In the description, never in a comment |
| `@coderabbitai resume` | Resumes |
| `@coderabbitai review` | Single re-pass |
| `@coderabbitai ignore` | Disables on this PR |
| `bugbot run` | Triggers a new Cursor BugBot pass |
| `cursor review` | Same |

### Never credit a bot as commit author

The personal CLAUDE.md rule and the broader research both prohibit attributing commits or PRs to AI tooling. The `ai-attribution-blocker.py` hook is the runtime enforcement layer. The skill's draft commit message must not name any AI tool in any author or co-author trailer.

## Multi-Reviewer Conflict Resolution

When two reviewers contradict, the skill surfaces a `conflict` decision instead of executing.

| Pattern | Skill action |
|---------|--------------|
| Reviewer A wants X, Reviewer B wants Y, on the same line | Mark both threads `conflict`. Draft a reply that quotes both verbatim, states the author's slight preference with reasoning, and asks A and B to align before the author pushes |
| Reviewer A approved, Reviewer B has not responded in over 24 hours | Print a notice. Default: do not auto-merge. Suggest a one-time re-request of review from B |
| Reviewer A blocks, Reviewer B has not yet weighed in | Hold the merge. The skill never dismisses a CHANGES_REQUESTED review without an explicit user decision |
| Both reviewers stale for over 2 round trips with no convergence | Tag the threads `synchronous-recommended` and suggest escalation to a tech lead or module owner |

The skill never silently merges or dismisses a CHANGES_REQUESTED review. Re-requesting review is a manual action behind `--re-request <user>`.

## Resolution Convention

Two community conventions exist.

### Default convention from Tidyverse and GitLab

The author resolves only the threads they have fully addressed and that are unambiguous. Anything with an open reply, an open question, a suggestion the author chose not to take, or a request for verification stays open for the reviewer to resolve. This is the default in the skill.

### Alternative convention from Dan Clarke

The person who started the thread resolves. The author never resolves. Opt in with `--resolve-by reviewer`.

In both conventions, the skill never bulk-resolves. Each resolve is a single GraphQL call tied to a specific thread whose action just completed. The `bulk-resolve-blocker.py` hook enforces this at the runtime layer.

### Outdated vs Resolved

GitHub auto-marks comments as `outdated` when the cited line changes. Outdated is not the same as resolved. An outdated comment can still name a live bug: the line moved, the concern did not. The skill never relies on `isOutdated == true` as a substitute for an explicit resolution, and never drops an item on that basis. The same holds for `isCollapsed`, which is a display hint. Force-pushing to mark threads outdated is an anti-pattern flagged in the "As Reviewee" section of [`../../standards/code-review.md`](../../standards/code-review.md).

`isMinimized == true` is different: minimizing is a deliberate human decision recorded on the platform, and it is the nearest thing to a resolve action that the three non-resolvable channels have. Honor it as terminal.

## Commit Credit Conventions

Use Git trailers to credit human reviewers.

| Trailer | When to use |
|---------|-------------|
| `Co-authored-by: <Name> <email>` | The reviewer wrote a portion of the fix, supplied a non-trivial algorithm, or proposed a change the author took verbatim |
| `Suggested-by: <Name> <email>` | The reviewer suggested the direction. The author implemented it independently |
| `Reviewed-by: <Name> <email>` | The reviewer reviewed and approved the change. Common in kernel and Rust projects |

Apply only to human reviewers. Never to AI tools or any non-human contributor. The `ai-attribution-blocker.py` hook is the runtime enforcement layer.

The skill prompts before adding any credit trailer. The default is no trailer unless the reviewer's input was substantive.

## Rules

- Every comment channel in [`../../standards/pr-comment-channels.md`](../../standards/pr-comment-channels.md) is swept every run. Inline threads are one channel of four. Never report "nothing to respond to" without per-channel counts backing the claim.
- Only the Terminal States table drops an item. `isOutdated` and `isCollapsed` are never drop criteria.
- Every drafted reply passes the no-internal-config-leakage check before posting. No `~/.claude/` paths, no rule citations, no checklist numbers in any external output.
- Every code change goes through the full local quality gate before push.
- Closure requires either a posted reply or a landed fix. Resolving a thread that received neither is forbidden.
- A reply is published only into a human's inline thread, at four sentences or fewer. Bot threads and the three unrepliable channels are closed without a comment, per [`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md).
- Bulk resolve is forbidden. Each thread is resolved individually after its action completes. The `bulk-resolve-blocker.py` hook backs this rule at runtime.
- `--auto` is the only path that skips per-batch approval. It additionally requires `RESPOND_AUTO_ACK=1` to take effect. Two locks reduce accidental triggers.
- Nothing is deferred and no tracker item is created. The fix lands in this change or the reply names the external blocker.
- AI bot threads are in scope by default and `--humans-only` excludes them. In scope or not, they receive no reply.
- Account safety: every `gh` call uses `GH_TOKEN=$(gh auth token --user <account>)` inline.
- Never `git push --no-verify`. Never bypass hooks without an explicit user-confirmed env var.
- Force-push is blocked during open CHANGES_REQUESTED reviews unless `--force-during-review` is passed.
- The skill never dismisses, deletes, or downgrades a review that the running user did not author.
- Restore the working tree on any failure inside Phase 6. The skill leaves a clean tree if it cannot complete the batch.

## Platform Reference Files

| File | When to read |
|------|-------------|
| [`platform-gitlab.md`](platform-gitlab.md) | When the detected platform is GitLab. Documents glab CLI and REST API patterns, discussion model, resolve semantics, and bot allowlist |
| [`platform-bitbucket.md`](platform-bitbucket.md) | When the detected platform is Bitbucket Cloud. Documents REST API patterns, auth model, and the absence of a native resolve concept |

## Common Rationalizations

- "The inline threads are the review": they are one channel of four. Sweep all four and report per-channel counts.
- "The bot is usually wrong, resolve it unread": verify every finding against the current code first; about half of bot findings are real.
- "A short thank-you reply to the bot keeps things tidy": a bot thread gets no reply of any length. Fix or resolve it in silence.
- "This one is out of scope, a ticket can carry it": fix it in this change, or name the external blocker in the reply.
- "The comment is outdated, so it is handled": an outdated comment can still name a live bug. Re-read the cited code.

## Red Flags

- Stop and drop the preview when a reply draft sits on any row other than a human inline thread.
- Stop and re-run the fetch when one channel reports zero items and the standard's cross-check was not run.
- Stop and use `--force-with-lease` when a push command carries `--force`.
- Stop and redact when a draft reply contains a `~/.claude/` path, a rule citation, or a checklist number.
- Stop and resolve one thread per call when about to resolve several in one command.

## Verification

- The final report carries the "Channels swept" line with a count for each of the four channels.
- Every implemented item has a commit, and the local quality gate output is shown before the push.
- Every published reply sits in a human inline thread and is four sentences or fewer.
- CI is green on the latest SHA, and a re-fetch after the push found no new threads.
- The counted done state shows 0 unresolved threads and 0 unminimized bot review bodies.

## Related skills

| Skill | When to use it |
|-------|----------------|
| `/review` | Performing a review on someone else's PR. Generates verdicts using the same Conventional Comments taxonomy |
| `/ship --pipeline` | Unattended handling of AI bot threads and CI monitoring without human-thread work. When `RESPOND_DRIVES_PIPELINE=1` is set, `/ship --pipeline` delegates the AI-bot sweep to this skill via `--auto --include-bots`, unifying the vocabulary across both flows |
| `/ship pr` | Creating or updating a PR before review starts |
| `/test` | Running tests after a code change before posting "Fixed in `<SHA>`" |
| `/investigate` | When a reviewer reports a bug that does not reproduce, before drafting the reply |
| `/plan` | When a reviewer requests an architectural change too large for inline reply |
