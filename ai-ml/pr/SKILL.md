---
name: pr
description: >-
  Create, promote, or clean up the GitHub PR for the current branch; keep the description
  brutally short, preserve durable acceptance evidence in comments, and handle review threads.
  Never carries transcripts — the exported /sy:ship session is attached to the task by /sy:ship,
  not posted to the PR.
argument-hint: "[optional emphasis or draft]"
---

Create/update the GitHub PR for the **current branch**. `$ARGUMENTS` may provide emphasis or `draft`.

This skill inherits caller model/effort. Assess scope before reading: a handful of short comments can be read directly; long review/thread tails go to `sy:sweep` and return briefs.

## 1. Detect state

Never operate on `main`. Confirm branch and PR state.

- **No PR** ⇒ create; push first if needed.
- **Draft exists** ⇒ promote/refresh when caller requests readiness.
- **Open non-draft exists** ⇒ cleanup/update. If called directly by a human, ask via `AskUserQuestion` before rewriting mutable metadata (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`); when `/sy:ship` explicitly invokes promotion/refresh, that invocation is authorization for that operation.

## 2. Description contract

Base on real diff/log. The mutable description is the PR's human-attention section — the judgment a reviewer has to make — so mechanical detail belongs in the dedicated PR comment `/sy:ship` posts separately rather than here. Keep the body concise:

- a link to the tracker ticket: its issue key or URL, so the PR and the durable record each reach the other;
- why and why this approach;
- 2–4 single-line summary bullets;
- no redundant file/function inventory;
- caveats only when reviewers cannot infer them from the diff;
- manual-only test plan; omit if none;
- optional small table only when genuinely clearer;
- image placeholder only when needed;
- no AI self-credit/co-author lines.

**Acceptance criteria/evidence never live only in the mutable description.** `/sy:ship` posts them as a dedicated PR comment so promotion/refresh cannot erase them.

What belongs in which of those two, and how hard to cut each, is `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/context-economy.md`; `/sy:tighten` is the pass that applies it, and the description goes through it — destination a PR description — before it is written.

Title: `<TICKET> - <imperative summary>` when branch carries a ticket key.

## 3. Review threads

Resolve `ship.request_ci_reviewer` — `get_config {"key": "ship.request_ci_reviewer"}` (see `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`) — before marking the PR ready. This gates only the automated-reviewer *request* below; it is additive to, never a substitute for, `sy:gate`'s own independent review, which always runs regardless of this setting.

When it resolves false, mark the PR ready with `gh pr ready <pr>` and skip straight to "Only then read the thread list" below — there is no bot request to make or confirm.

When it resolves true: a draft PR gets **no** automated review — Copilot and similar reviewers do not comment until the PR is marked ready, so a draft that is never promoted shows a permanently empty thread list that reads as "nothing to reconcile". Marking it ready with `gh pr ready <pr>` is necessary but not sufficient: observed runs show the automated reviewer does not fire on readiness alone, so an explicit request is the normal path, not a rare fallback. Immediately after marking ready, walk this ladder and stop at the first rung that lands:

1. **By login** — `gh pr edit <pr> --add-reviewer "@copilot"` (gh ≥2.87.0), or the repo's configured automated reviewer login. gh special-cases `@copilot` onto GitHub's bot path, so this is *not* the same call as a raw REST review request and usually succeeds where one does not.
2. **By node id over GraphQL** — a raw REST `POST .../requested_reviewers` naming the bot's login fails `422 Reviews may only be requested from collaborators`, because a review bot is not a repository collaborator; rung 1 fails the same way on a gh old enough to lack the special case. The bot is also absent from `suggestedActors`, so read its node id off any review it has already left in this repo, then request by id:

   ```bash
   gh api graphql -f query='{repository(owner:"<o>",name:"<r>"){pullRequest(number:<n>){reviews(first:20){nodes{author{__typename login ... on Bot{id}}}}}}}'  # <n> is a PR the bot has previously reviewed, not necessarily this one
   gh api graphql -f query='{repository(owner:"<o>",name:"<r>"){pullRequest(number:<this pr>){id}}}'  # this PR's own node id, separate from <n> above
   gh api graphql -f query='mutation($pr:ID!,$bot:ID!){requestReviews(input:{pullRequestId:$pr,botIds:[$bot],union:true}){clientMutationId}}' \
     -f pr=<this PR's node id> -f bot=<bot node id>
   ```

   `union:true` adds the bot without clearing reviewers already requested.
3. **Surface it loudly** — when no rung lands, including a repo with no prior bot review to read an id from, report the failure and hand off to the repo's manual "request review" control. Never skip it silently.

Then confirm the request actually landed, over GraphQL and not REST — `gh pr view <pr> --json reviewRequests` renders `[]` for a bot reviewer that *is* requested, so it is a false negative rather than a confirmation:

```bash
gh api graphql -f query='{repository(owner:"<o>",name:"<r>"){pullRequest(number:<n>){reviewRequests(first:10){nodes{requestedReviewer{__typename ... on Bot{login}}}}}}}'
```

Only then read the thread list. An empty one is never evidence of "reviewed, nothing to say": it is indistinguishable from a review nobody requested, and only a confirmed request reaching a terminal state tells the two apart.

Reconcile the reviewer's threads by **author bot-type, not a hardcoded login.** The same reviewer's bot login is not stable across the GitHub REST and GraphQL surfaces (e.g. a `-bot` suffix or `[bot]` bracket form differs between them), so a query filtered to one literal login silently returns zero threads on the other surface and reports a false "0 new comments". Enumerate all review comments/threads and select by author type being a bot — for example `gh api repos/<o>/<r>/pulls/<pr>/comments --jq '[.[] | select(.user.type=="Bot")]'` (or the GraphQL `reviewThreads` with `author { __typename }` matched against `Bot`) — so every bot thread is caught regardless of which login form that surface reports. Reconcile against comment/thread ids, not login strings.

Every relevant review thread gets an answer; push back on bad trade-offs instead of rubber-stamping. When a thread surfaces a small, adjacent, low-risk fix, fold it into this branch rather than deferring to a follow-up that loses the context — the follow-up must justify itself (see `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/scope-discipline.md`). A reply is a posted record: one later found wrong is corrected on the thread, not left standing (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/write-integrity.md`, retroactive honesty).

- small thread set ⇒ read directly;
- long auto-reviewer/multi-round tail ⇒ `sy:sweep` brief with open suggestion, target `file:line`, and addressed/unaddressed state.

Caller reads decisive threads and writes replies. Stage each reply body as a file, then post it by **reading the file** — never by handing `@path` to a literal-string flag:

- inline thread reply ⇒ `gh api --method POST repos/<o>/<r>/pulls/<pr>/comments/<id>/replies -F body=@<file>` (or `--input <file>`);
- top-level PR comment ⇒ `gh pr comment <pr> --body-file <file>`;
- edit an existing comment ⇒ `gh api --method PATCH repos/<o>/<r>/pulls/comments/<id> -F body=@<file>`.

`gh api -F/--raw-field key=@file` reads the file; `-f/--field key=@file` posts the literal `@file` — a silent-corruption trap. After posting, read the stored body back (`gh api .../comments/<id> --jq .body`) and confirm it is the intended prose, not a value starting with `@`.

## 4. Merge (verified-head only)

Merging is `/sy:ship`'s explicit-authorization path (`ship/references/merge-accounting.md`), not part of the normal create/promote/cleanup flow. Resolve the configured strategy once — `get_config {"key": "ship.merge_strategy"}` (one of `squash`, `merge`, `rebase`; see `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`) — and gate every merge on the exact validated commit regardless of strategy:

```bash
# squash: compose the message from the PR's own description (§2) rather than accepting GitHub's
# default, which concatenates every branch commit subject into the body
gh pr merge <pr> --squash \
  --subject "<TICKET> - <imperative summary>" \
  --body-file <staged summary file> \
  --match-head-commit <CI-green + reviewed SHA>

# merge/rebase: no subject/body to compose
gh pr merge <pr> --merge --match-head-commit <CI-green + reviewed SHA>
gh pr merge <pr> --rebase --match-head-commit <CI-green + reviewed SHA>
```

- `--match-head-commit` aborts the merge if the head moved since validation, so only the reviewed/CI-green commit can land, never a race-pushed one — true for every strategy. Composing a message never relaxes that guard — drop the subject and body before you drop the head match.
- Only `squash` composes a subject/body; stage it from the description's why plus its summary bullets, so the squashed commit reads as the changelog entry for the change rather than as build noise. `merge` and `rebase` pass neither flag.
- `gh pr merge -F/--body-file` takes a **plain file path**, a different convention from the `-F key=@file` form used for comment bodies in §3 above; conflating the two silently posts the wrong thing.
- add `--admin` only to clear a ruleset the author cannot satisfy alone (e.g. a required approval the author can't self-give), and only with the owner's explicit go-ahead — it bypasses the ruleset, not CI/review freshness.

This skill never runs tests or review; `/sy:ci` and `sy:gate` own those gates, and session transcripts belong on the task via `/sy:ship`. End by printing the PR URL and what state change/comment action occurred.

Every subagent dispatch resolves its model from config and passes it as the `Agent` invocation's actual model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`; a nested dispatch inherits nothing and must resolve again.
