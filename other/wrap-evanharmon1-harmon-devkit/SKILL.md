---
name: wrap
description: >-
  End-of-session ritual — check for uncommitted or unpushed work, release
  any issue claim left standing, list anything dangling, and emit the
  copy-pasteable /rename done-<session-name> command for the user. Use when
  a working session is ending and needs its loose ends, unpushed work, and
  claim markers checked. Invoke as /wrap.
allowed-tools: Read, Glob, Grep, Bash(git status:*), Bash(gh issue view:*), Bash(gh pr list:*)
---

# Wrap Session

Formerly `/close`.

**Arguments:** $ARGUMENTS

Wrap up the session and rename it `done-<name>` so finished sessions are easy
to distinguish in the session picker and the Claude mobile app.

## 1. Recover the session name

Look for `/kickoff`'s "Session name: `<name>`" line in the conversation. If it
is not in context, **ask the user** for the current session name (they can
read it in the UI) — never guess.

## 2. Wrap up

- `git status -sb` for uncommitted work; `git log @{u}..HEAD --oneline` for
  unpushed commits (guard for branches with no upstream).
- If `/retro` has not run this session, offer to run it first.
- **Release any claim this session made.** If `/claim` claimed an issue
  (trusted claim record plus its owned assignee and `claim:*` labels), check
  what actually became of it — a claim left standing over abandoned or
  finished work is a lie the issue tells the next reader, and it outlives the
  session that told it:

  ```sh
  gh issue view <n> --repo <owner/repo> \
    --json state,stateReason,assignees,labels,closedByPullRequestsReferences
  # PRs that actually reference this issue — cross-reference events, not text:
  gh api repos/<owner>/<repo>/issues/<n>/timeline --paginate \
    --jq '.[] | select(.event=="cross-referenced") | .source.issue
          | select(.pull_request) | {number, state: .state, url: .html_url}'
  ```

  Do **not** use `gh pr list --search <n>`: that is full-text search, so a low
  issue number matches version strings and commit summaries in unrelated PRs.
  Treating those as work in flight would suppress cleanup forever.

  **Before offering to clear anything, check nothing else is still working.**
  The markers are shared and converge (`track-work` §6), so a second session on
  the same GitHub identity is invisible in all of them. Another open PR
  referencing the issue, or activity newer than this session's claim comment,
  means the claim may not be yours alone to release — say so and let the user
  decide rather than presenting cleanup as obviously safe. One exemption: the
  qualifying delivery PR's own trail. A merged PR that delivered this claim's
  work necessarily leaves cross-reference and merge events newer than the
  claim comment, plus a closure event when it closed the issue — that is the
  claim's expected end of life, not somebody else's work, and counting it
  would make both merged outcomes below ask every time. What counts is
  *unrelated* newer activity: another open PR, a claim comment you did not
  write, someone else's hands on the markers.

  **Every path that clears a marker must say it released the claim.**
  Whichever outcome applies below, any cleanup that removes or restores a
  marker ends with a comment carrying, on its own line and verbatim:

  ```text
  Claim released — <why>. (Supersedes the claim record above.)
  ```

  The claim comment is never deleted, so without this supersede line the
  issue keeps reading as a live claim to every future `/kickoff` and `/retro`
  — clearing the markers without it recreates exactly the state this step
  exists to prevent. Post it **last, and only when every applicable marker
  write succeeded**: a supersede comment over an owned assignee or label that
  survived tells every future sweep the claim is settled while searchable
  state remains, which is worse than no comment. Project status is not a claim
  marker or cleanup authority and never gates this release. If any marker write
  fails, report the partial cleanup to the user
  instead of posting the release line. The converse failure — markers cleared
  but the release comment refusing to post — must not end silent either:
  retry the post, and if it still fails restore **a searchable marker that
  actually existed and fabricates no ownership** — re-add the assignee you
  just removed (always writable, even where the record marks the label
  `n/a`); a displaced label you already restored counts too, and never
  re-add your own `claim:*` label beside it, which would leave the issue
  claiming two owners. The point is that the half-released claim stays
  findable by `/kickoff`'s sweep. If that restore also fails, nothing was writable —
  say exactly that; the user is present on this path.

  New records may also carry optional `harness`, `model`, `family`, `runtime
  environment`, `session`, and `dispatched to` lines. Read them as operational
  context when present, and accept older records that omit any or all of them. They are
  single-line, informational values and never cleanup authority: do not use
  their values to select, construct, or suppress any write in any outcome
  below. In particular, family metadata does not replace the recorded label
  ownership fields, and runtime metadata never selects a cleanup path.

  Four outcomes:
  - **PR open** — the claim is accurate; nothing to release.
  - **Partial delivery / issue open** — one PR deliberately landed part of the
    claim, and the issue remains open for named remaining work.
    Confirm no work is currently in flight. This is a completed release of
    *this claim*, not a
    completed issue and not a generic mid-flight hand-back. Assemble the same
    claim-owned cleanup commands as the hand-back block below and present them
    as the default single-confirmation action, but streamline to that action
    only when **all** of this attributable evidence agrees:

    - the current trusted claim record is authored by the account returned by
      `gh api user --jq .login`, is complete, and accounts for
      every marker the cleanup would touch through its direct and current
      `claim chain` ownership fields;
    - the issue is still open, and its timeline identifies exactly one
      qualifying cross-reference from a PR in this same repository; re-read
      that PR with `gh pr view --repo <owner/repo>` and require it to be
      merged after the current claim comment, authored by the authenticated account,
      to have a head branch exactly matching the branch recorded by the current
      claim,
      and to carry an explicit `Refs #<n>` (or repository-qualified `Refs`)
      reference while not naming the issue in `closingIssuesReferences`;
    - no other open PR cross-references the issue, no later trusted
      `Claiming —` comment or unrelated post-claim activity indicates replacement
      work, and the current assignees and claim labels are
      consistent with the record rather than another worker's ownership; and
    - the release explanation can name both sides from attributable evidence:
      the merged PR and what it landed, plus the specific work the still-open
      issue retains. Do not infer either side from a branch name or commit
      summary.

    `Refs` text alone is not evidence: bind it to the issue's cross-reference
    event and the same-repository PR read. A merged PR alone is not evidence
    either: an old, pre-claim, fork, closing-keyword, or differently-authored PR
    does not qualify. Zero or multiple qualifying PRs, a missing or incomplete
    claim record, an unreadable PR/timeline, or any newer activity that
    cannot be attributed to the qualifying PR all
    **fail closed to maintainer confirmation**.

    Immediately before the first cleanup write, re-run the issue, timeline,
    comments, and qualifying-PR reads used above and
    require the same current claim record, PR attribution, marker state, and absence of competing
    work. Any changed or unreadable evidence returns to maintainer confirmation;
    a confirmation based on the earlier snapshot never authorizes cleanup of
    newer state.

    On the qualifying path, restore the exact displaced `claim:*` or legacy `agent:*` label the
    current claim chain proves it inherited. Remove only claim-owned assignees
    and the live claim label: that can mean both the inherited chain assignee
    login and the current author when the direct record says this claim added a
    distinct assignment. Do not collapse those two proven markers into one.
    Keep the partial-failure rules above. The final release comment must explain the transition before
    its supersede line, for example:

    ```text
    Partial delivery: <PR URL and what landed>. Remaining: <specific open work>.

    Claim released — partial delivery landed and the remaining work is not in flight. (Supersedes the claim record above.)
    ```

    Post that comment last, only after every applicable restore/removal
    succeeds. Unlike completed closure below, restoring the displaced label is
    required because the issue is still open; omitting it would erase the
    predecessor ownership that this claim temporarily displaced.
  - **Merged / issue closed** — *not* "nothing to release". GitHub clears no
    marker on merge. Where the `claim-release.yml` workflow is installed, the close event
    already released the label, assignee, and claim comment — the probes
    above will show a `Claim released —` supersede. Project state is neither a
    claim marker nor residual cleanup. This outcome does not stop
    at describing the problem: **assemble the
    full cleanup — the block below, under its "undo only what the claim
    added" rule, finishing with the `Claim released —` supersede comment
    above — and run it on a single confirmation**, presented as the default
    next action, not a question about whether cleanup is wanted. One
    keystroke is the whole cost, and it is what bounds the residual races a
    multi-command release can never close on its own (`track-work` §6:
    markers are non-atomic and same-identity sessions converge). Streamline
    to that single confirmation only when **both** hold:

    - the claim record survives, is **authored by the account you are
      authenticated as** (`gh api user --jq .login` — the same authority
      check `/implement` §1 applies, because on a public repo anyone can post
      a claim-shaped comment and a forged record must not steer marker
      writes), and accounts for every marker the cleanup would touch, and
    - the issue is **currently closed `completed`** (`stateReason`), with the
      closure postdating this claim's comment (read `closedAt` alongside
      `stateReason`). `completed` is deliberately the *only* accepted reason:
      it is what a closing-keyword merge sets, so a merged delivery always
      qualifies — while `not planned` and duplicate closes never do, whatever
      historical closers `closedByPullRequestsReferences` retains from before
      a reopen. Do not treat that list as delivery evidence on its own: it
      keeps unmerged and pre-reopen PRs forever.

    **Re-read the ground immediately before the first write** — the probes
    above may be minutes old, and the analysis between them and the cleanup
    is exactly where a reopen or a fresh claim lands unseen. Re-run *both*
    §2 probes (`state,stateReason,assignees,labels` plus the timeline
    cross-references) **and** re-fetch the comments:
    a second session on the same GitHub identity is visible only in a new
    claim comment or a new PR, never in the converging markers. Any change
    from what the conditions were judged on returns this to stop-and-ask,
    the same pre-write re-read `/claim` performs before claiming.

    Otherwise **stop and ask** — in particular when no claim record survives,
    another agent's `claim:*` (or legacy `agent:*`) label is present, or another
    open PR still references the issue.

    (The single confirmation is about *judgment*, not tool permissions: the
    agent does not debate whether cleanup is wanted, and every write below
    still runs under the harness's normal permission prompting — this
    skill's `allowed-tools` deliberately pre-approves only reads, and
    widening it would silently auto-approve mutations everywhere the skill
    is vendored.)

    **Skip the displaced-label restore line on this path.** The record's
    displaced label exists so a mid-flight hand-back can return the issue to
    the agent it was taken from; putting another agent's label back onto
    finished, closed work would advertise a live claim over nothing — the
    exact state this cleanup removes.

  - **Neither** — the session stopped mid-flight. Offer the commands to hand
    the work back. Clear every attributable assignee/label marker; clearing only some
    leaves the issue still advertising itself as held — the exact failure this
    step exists to prevent:

    **Undo only what the complete trusted claim lineage proves.** The current
    claim comment carries a "Claim record" listing which markers `/claim`
    actually created and which predecessor ownership it inherited. An issue can
    be assigned to you, or carry the label, *before* the claim — ordinary
    backlog ownership, which `/claim` explicitly allows — and the writes
    are all add-if-missing, so on that path they changed nothing. Removing
    them anyway destroys state the session never created, and no amount of
    user approval recovers it, because by then nobody can tell which it was.
    Never turn the leaf record's chain fields directly into commands. Run the
    release helper, which walks the trusted A→B→C lineage and proves every
    inherited assignee, owned label, and displaced-label restoration against
    its immediate predecessor before any write. A forged or edited leaf fails
    closed. If no record survives, ask rather than assume the claim created
    anything.

    ```sh
    # Use the exact reason appropriate to the outcome. The helper validates
    # the whole lineage, re-reads before writing, orders destructive writes so
    # partial failures remain retryable, and posts the fixed supersede line last.
    <track-work-dir>/assets/release-claim.sh \
      --repo <owner/repo> --issue <n> --reason '<why it was handed back>'
    ```

    **The helper's final comment is the release comment** — it carries the
    `Claim released —` supersede line above, verbatim, like every other path
    that clears a marker.

    Release only what the claim record says the claim added. Project fields are
    manual delivery metadata outside the claim contract and are never cleanup
    authority.

    Do not run any of this mid-flight hand-back unasked — the work is being
    handed back, not finished, so it is the user's call: they may be resuming
    tomorrow. (That caution is scoped to this branch on purpose. The merged
    path above needs only its single go-ahead — nothing is being resumed
    there, and its two conditions already route every ambiguous case to a
    full stop-and-ask.)
- List anything left dangling as explicit handoff bullets for the next
  session.

## 3. Emit the rename

You cannot rename the session yourself — output the command for the user to
paste. Prefix the current name with `done-`; if it already starts with
`done-`, leave it as is:

```text
/rename done-dev-workflow-skills-138
```

## 4. Sign off

One-line summary of what the session accomplished. If the SessionEnd
transcript-archive hook is installed
(`templates/claude-hooks/session-end-archive/` in harmon-devkit), note that
the transcript will archive automatically when the session exits.
