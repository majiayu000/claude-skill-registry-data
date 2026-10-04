---
name: watch
description: Waits for Copilot to review a PR and automatically chains the fix-comments cycle, up to two rounds. Use right after opening a PR with `ship`, and whenever the user says "wait for the review", "let me know when Copilot answers", "keep going with the PR", or asks to leave the PR review cycle running — or in Spanish "quedate esperando el review", "avisame cuando Copilot conteste", "seguí vos con el PR".
---

# Wait for the review and close the loop

Keeps the session busy watching a PR until the review cycle finishes or a human is needed.
The user works in another session meanwhile.

## How the wait works

For a single "ping me when the review lands" wait, the right tool is a **background Bash
command** that exits when the condition is met — not the Monitor tool (Claude Code's own
guidance points to background Bash for one-shot waits). You get exactly one notification when
the poller exits.

One environment caveat, only if you run Claude Code's **sandbox**: `gh` (a Go binary) fails
TLS verification inside it (`x509: OSStatus -26276`) because the sandbox proxy presents a CA
it won't validate, so the poller must run **outside** the sandbox — that's what
`dangerouslyDisableSandbox` is for below. No sandbox? Then you don't need it and plain
background Bash is enough.

## 1. Request the review — ALWAYS before waiting

Copilot doesn't start on its own, and **doesn't re-review on its own when you push** either.
This goes here, and **again after every push** that `fix` makes:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # -> {{owner}}/{{repo}}
PRID=$(gh api graphql -f query='query { repository(owner:"{{owner}}", name:"{{repo}}") { pullRequest(number:{{n}}) { id } } }' --jq '.data.repository.pullRequest.id')
gh api graphql -f query="mutation { requestReviews(input:{pullRequestId:\"$PRID\", botIds:[\"BOT_kgDOCnlnWA\"], union:true}) { clientMutationId } }"
```

`BOT_kgDOCnlnWA` is `copilot-pull-request-reviewer`, a single global GitHub App id (stable
across repos). `union: true` makes it idempotent, so re-requesting never breaks — when in
doubt, request again. The REST `requested_reviewers` API returns 422 (the bot isn't a
collaborator); use GraphQL with `botIds`.

**This is also how you avoid waiting forever for a review that will never come.** If Copilot
code review isn't enabled on the repo, its bot id can't be requested and the mutation comes
back with an `errors` array instead of a `clientMutationId`. So **check the result**: if it
errored, Copilot review isn't set up — do **not** arm the watcher. Tell the user to enable it
(repo Settings > Copilot > Code review, or add a "Copilot code review" rule under Settings >
Rules > Rulesets) and stop. A clean `clientMutationId` back means Copilot is available →
proceed to step 2. (The poller's timeout in step 3 is the backstop for the rarer case where
the request is accepted but no review ever lands.)

## 2. Arm the watcher — one background Bash call

The poller ships with this plugin and is on your `PATH` (Claude Code adds every plugin's
`bin/` there), so call it by name. Run it as a **background Bash command**
(`run_in_background: true`); if the sandbox is on, also pass **`dangerouslyDisableSandbox:
true`** (see "How the wait works"):

```bash
wait-for-review.sh {{n}} 60
```

The script polls every 30s for up to the given minutes, stays silent while waiting, prints a
single `RESULT=<STATE> detail=...` line, and exits. Because it's a background Bash command,
that exit is your only notification. It fails loudly with `RESULT=ERROR` if `gh` can't even
resolve the repo, so it never hangs silently — you always get a result to act on.

Confirm to the user in one line: which PR it's watching, and that they can move to another
session.

## 3. Act on the result

| Result | What to do |
|---|---|
| `REVIEWED` | Invoke the `fix` skill for the PR. When it finishes, if it applied fixes and pushed, **request the review again** (step 1) and re-arm (step 2). |
| `CI_FAILED` | Handle the broken checks first: `gh pr checks {{n}}`, read the failing job's logs, fix, commit, push, **request the review again** and re-arm. |
| `TIMEOUT` | Don't retry silently. Tell the user Copilot didn't answer and ask whether to retry or leave it. |
| `ERROR` | Read the detail on the result line, report the problem, and stop. |

## 4. Stop conditions

The full cycle ends when any of these happens:

- `fix` **escalated** a comment to human review this round -> **stop**, tell the user what's
  left. Note: the `needs-human` label alone doesn't stop the cycle — `ship` adds it to
  anything touching sensitive areas, and that stops the merge, not the review rounds.
- **Two rounds** completed (`ai-round-2` label) -> **stop**, even if Copilot keeps commenting.
- Copilot approved and no unresolved comments -> **stop** and say it's ready to merge.

Never merge. Never start a third automatic round.

## 5. Final report

One short message: PR URL, rounds used, how many comments were fixed, how many rejected with
justification, and what needs their decision. If nothing needs anything, say so in one line —
that's the merge signal.

---

*Convention: `{{like-this}}` marks a value to replace. `<>` is avoided because it breaks skill parsing.*
