---
description: >-
  Check once whether the branch's merge target (the branch its PR is based on)
  advanced or the PR landed since the branch was last attested, then hand any
  advance back to the enclosing flow to decide. While the PR is open, also
  reconcile the `Proposed squash body:` comment `/finalize` left on it, and the
  PR title it lands under — editing both in place when the branch has drifted
  from them. A manual
  one-shot — run it when you return to a session whose branch is attested to see
  if the merge target moved out from under the branch. Pass an optional
  branch/PR target first (`/check-merge <branch|#PR|PR-url>`) to attach to that
  existing branch before checking. Use when the user says "check merge",
  "check main", "did main move", "/check-merge", or equivalents.
---

**Optional branch/PR target**: if the first token of the argument is a branch
name, `#NNN` PR number, or PR URL, then `/check-merge <target>` is shorthand for
attaching to that branch first and then checking — equivalent to
`/from-branch <target> check-merge`. Load `@.claude/skills/from-branch/SKILL.md`
and follow it to attach to `<target>`, then run the check below. With no
argument, check the current branch as usual.

Check **once** whether the branch's **merge target** has moved out from under
the branch, or whether the PR landed. The merge target is the branch the open PR
is **based on** — resolved from the PR, not hardcoded to `main` — so this stays
correct for a PR based on a promotion branch or a long-lived feature branch.
With no PR it falls back to the repo default branch. Once the branch is attested
the enclosing flow **ends its turn** (so the session reads as **idle**, not
pinned as "working"); when the operator returns and runs `/check-merge`, this
performs a single check and reports. This is the last check before the code
lands: nothing runs at merge time, so a base that moved out from under an
attested branch has no CI anywhere to catch it. An attestation names the base
SHA it was made against (`/finalize` Step 7) — this is the check that says
whether that SHA is still current.

The check is **stateless** — it computes everything from git on each run,
comparing the branch's own history against the freshly-fetched target tip.
There's no baseline file to record or reset: the branch's last merge of the
target _is_ the reference point, so once you merge a newer target in, the next
`/check-merge` simply reports "contained".

This skill **detects** movement and **hands back** to the enclosing flow
(usually `/finalize`) — it does **not** decide what to do about a move, drive
any re-merge, or re-attest. The "what to do when the base advanced" rules live
in the enclosing flow. The one thing it does actively maintain is the squash
record: whenever the PR is open it reconciles the `Proposed squash body:`
comment and the PR title against the branch's current state and edits them in
place if they drifted (Step 3).

`/finalize` reaches this at its very end, just before it attests. It can also be
invoked directly.

## Why the check is cheap

Resolving the target and fetching it is a couple of `gh`/`git` calls plus a
local ancestry test. The single `gh pr list` that resolves the target's base ref
also returns the PR state, so a landing (merged/closed) is classified from that
same call — no second lookup.

## Step 1: Run the check once

Run `scripts/check-merge.sh` once via the Bash tool. It returns immediately.
Read the printed line / exit code and act:

- `0` — the branch already **contains** the target's current tip (nothing to
  merge), and the PR is still open. → Report "no movement; branch is current
  with `origin/<target>`" and **stop**. The operator can run `/check-merge`
  again later. (Exit 0 also covers a transient network blip — the message says
  so; just re-run.) The printed line names the resolved `target=…`, so a base
  other than the default branch is visible at a glance.
- `10` — the target **advanced** beyond this branch. → Step 2.
- `20` — this branch's PR was **merged**. The work landed. → Report and
  **stop**.
- `21` — this branch's PR was **closed without merging**. → Report and **stop**;
  do not re-merge or re-CI.
- `1` — hard error (detached HEAD, `gh` lookup failure, missing tooling). →
  Surface it and stop.

No setup is needed before this — there's no baseline to establish. The check
compares the branch's history against the live target tip every run, so it's
correct whether it's the first call after the branch was attested or a later one
after you've merged the target in.

## Step 2: Target advanced — hand back to the enclosing flow

Do **not** decide here, and do **not** name a specific flow. State plainly what
the check reported (`origin/<target>` advanced `base..new`) and **hand control
back to the enclosing flow**, which decides per _its own_ target-advanced rules:

- When the enclosing flow is `/finalize`, its Step 6 hands you the deliberation
  (read the incoming diff; re-run the vet suite and re-attest only when the
  commits plausibly interact with this branch; otherwise merge-and-resume). Once
  the new target tip is merged into the branch, a later `/check-merge` reports
  "contained" again, so the cycle continues until the PR lands.
- If invoked standalone with no enclosing flow to hand back to, deliberate per
  the same criteria (load `@.claude/skills/finalize/base-advanced.md`) before
  acting — don't reflexively skip re-verification. On the
  demonstrably-independent path just merge and push.

The cycle always terminates: merging the advance in makes the next check
"contained", and the merge (exit 20) / close (exit 21) outcome is always
reachable on a later `/check-merge`.

## Step 3: Reconcile the squash record (PR open only)

Applies whenever the PR is still **open** — after a `contained` (exit `0`)
check, or after the enclosing flow has merged an `advanced` (exit `10`) tip back
in. Skip it for a landed/closed PR (exit `20`/`21`) and for a hard error (exit
`1`).

The squash record is the PR title plus a comment headed `Proposed squash body:`
— the fenced body sitting next to the merge button, after a title block on a
one-commit PR — posted when `/pr` opened the PR. Both go stale as the branch
moves: a base-advanced re-merge pulls in work that shifts the essence, a
`Closes #N`, or the body's paragraphs. This step keeps them current.

Invoke `@.claude/skills/squash-message/SKILL.md` in **`update-only`** mode,
passing the base the check resolved (the `target=…` the script printed) as the
diff base. That skill recomputes the title/body from the branch's current
committed state — including its draft-then-tighten pass — and edits the PR title
and the existing comment in place if they drifted. The reconcile may push a
commit as well as edit the comment — `/squash-message` decides, from the working
file it selects. `update-only` is what keeps this step from creating a proposal
no earlier step made: absence is reported, not filled in. Report what it
reports.

On the `advanced` (exit `10`) path the squash body depends on the merged-in
work, so run this reconcile **after** the enclosing flow incorporates the
advance (Step 2's hand-back) — before then the branch doesn't yet contain what
will land. If the advance isn't merged in this turn, defer the reconcile to the
next `/check-merge`, which will see `contained`.

This is the check most likely to find something the record should mention — an
advanced base carrying work the essence has to account for — and by the time an
operator runs it, `/finalize` has usually swept the tracked doc. That doesn't
mean composing a new message over the top of the old one: `/squash-message`
restores the swept file from git history and edits forward from its last text,
then sweeps it again in the same turn. Don't hand-roll either half here; it owns
both.
