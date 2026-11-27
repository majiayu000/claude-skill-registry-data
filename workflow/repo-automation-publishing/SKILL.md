---
name: repo-automation-publishing
description: Use when a scheduled job must publish into a shared repo.
version: "0.1.0"
license: MIT
author: Zoe
metadata:
  version: "0.1.0"
  areas: "software-development,devops"
  targets: "runtime-agnostic"
  summary: "publish from a routine: PR on one fixed head branch by default; direct push to the default branch when the operating contract decides the automation owns it — action floor, failure distinguishable from idle, fixture-tested state machine"
  summary_zh: "定时任务发布进共享仓：默认固定头分支开 PR；契约决定时直推默认分支 —— 动作地板、失败与空闲可区分、夹具测状态机"
  kind: "entry"
  hermes:
    tags: [git, automation, pull-request, cron, publishing]
    related_skills: [harness-engineering, concurrent-agent-repo-workflow, generated-runtime-repairs, ops-claim-verification, hermes-cron]
---

# Publishing automation into a shared repo

A routine (snapshot, port, generated catalog, sync job) whose *output* lands in a git repo that humans and
other agents also write to. The policy layer — branch + PR, linear history, who merges — belongs to the
repo's operating contract and the harness skill; this skill carries the state machine and the failure
semantics that make the automation safe to leave unattended.

## When to Use

- A scheduled job regenerates files and commits them into a shared repo.
- An automation "stopped updating" a repo, or a pipeline's output is stale by days (→ *Triage: a known
  publisher went stale*, below).
- You are changing how an existing sync routine publishes (push → PR, cadence, notification).
- You are choosing the delivery variant: PR on a head branch (the default for shared repos) or direct
  push to the default branch (only when the repo's operating contract says the automation owns it —
  see the decided-flow variant below).
- The owner asks to **pause / stop / repoint** the automation behind a repo ("先暂停 X 的自动提交") —
  locate the writer(s) first, and be ready to answer "this repo has no scheduled writer"
  (→ *Locating the writer*, below).

## Rules

1. **One fixed head branch, never the default branch.** The local default branch stays the generator's
   working branch; publication is `git push origin main:refs/heads/auto-sync/<area>`. The default branch
   advances only by a merge.
2. **Never force-push; a rejected push is a stop, not a retry.** Write the review queue, notify, exit
   non-zero. Do not "fall back" to pushing the default branch — a non-fast-forward means another writer owns
   that ref.
3. **Check often, act rarely.** The cadence and the action floor are separate knobs: the timer may run every
   2h while the floor holds actions ≥6h apart in a state file (`last_action_at`, `pr_number`, `last_pr_state`).
   Inside the window: still regenerate and commit locally, push nothing, exit 0 with one `held: …` line —
   "held" and "failed" must be distinguishable in the timer log, and a manual `--force-sync` bypass belongs on
   the script so nobody edits the state file by hand.
   **The floor's clock must outlive the merge-cycle state.** Merge detection (rule 7) clears the state file;
   if `clear` takes `last_action_at` with it, the floor resets at every merge and the effective cadence
   silently collapses to the timer's period — the tell is a merge history spaced *exactly* one timer period
   apart while every line of the script still reads as if the configured minimum were in force. Keep the
   action clock on `clear` and drop only the branch/PR/gate fields. Once the floor survives a merge, a held
   run leaves a **committed but unpublished** snapshot on the default branch, so the "nothing to do" test
   must compare `HEAD` against `origin/<default>` whenever the head branch does not exist: a `pending`
   count keyed on "did this run commit" reads 0 on the next idle run and strands that snapshot forever.
4. **A fail-closed stage must not read as idle.** A gate that aborts the run leaves the same
   operator-visible outcome as "nothing to publish"; without a delivered failure signal the pipeline can sit
   dark for days. Every failure path delivers (dedup state file + a channel the operator reads) and names the
   first failing stage.
5. **One exclusion source between producer and gate.** A gate comparing the destination to a manifest while
   the producer carries its own skip list cannot be satisfied by either side: a file only one of them knows
   about is a permanent standoff whose symptom is "no changes" every cycle. The manifest drives enumeration
   *and* pruning, and the prune step runs between producer and gate.
   **Under-enumeration is the same bug wearing a green gate.** The producer's rule must be written from
   what the *destination* must contain, not from the subtree the producer happens to own: a rule keyed on
   "directories I copied a real file from" silently drops companion files (description, index, manifest)
   for every directory reached through a symlink, and no check fires — the destination merely lacks them.
   Walk the whole source tree and filter by shape (is a link / is a leaf), then assert the written count
   against the count the rule implies. Fix it in the generator, never by adding the missing copies: the
   next run overwrites them.
6. **Review generated deletions in chunks with the unexplained count at zero.** Classify every deleted path
   (superseded / retired-by-design / local-only) across batches rather than accepting one summary line, and
   re-derive any credential- or data-shaped name from the generator instead of approving it from a report.
   **Release a reviewed batch through the guard's own switch, with the list as an artifact** — never by
   editing the threshold, which stays as the backstop for the batches nobody reviewed. Two contracts make
   the file trustworthy. *Format*: one repo-relative path per line, spelled exactly as the staging step
   prints them (`git diff --cached --diff-filter=D --name-only`), blank lines and `#` comments ignored —
   the guard compares by exact string, so an absolute path, a live-tree path or a trailing slash matches
   nothing and the whole batch stays refused. *Content*: a header carrying the four facts a reviewer needs —
   what was deleted (grouped, with counts), why it is legitimate (superseded by *what* — name the
   replacement and show it present in the destination — retired by design, or local-only), where the
   evidence lives, and how the content is recoverable (history, upstream). Classify from the destination's
   live state, never from the diff's plausibility. The batch is released on the owner's explicit
   instruction, quoted in that header; the refusal path leaves the tree reset and intact, so re-running
   after approval is cheap and safe. Nothing about "the deletions were not mine" shortens this — a batch
   another lane's library update produced is still a batch, not a self-approving one.
7. **Merge detection is part of the cycle, not an operator chore.** Newest PR for the head branch merged or
   closed ⇒ `git fetch` → `git reset --hard origin/main` → delete the stale remote branch when nothing is
   open → clear the state. That reset is safe only while the local default branch holds regenerated content
   and nothing hand-written — state that invariant in the script. Never change repo settings
   (`delete_branch_on_merge` etc.); retiring the branch is the script's step.
8. **An open PR is a delivery owed — "nothing to commit" is not "nothing to do".** Delivery completion is its
   own state, checked before the idle exit: if the head branch has an open PR, the run must finish *that*
   cycle (push the head if it is behind, re-run the gate, comment, merge) even when the generator produced no
   new content — a run that died after the push, or whose comment/merge failed, would otherwise strand the PR
   forever behind a cheerful `no changes`. Finishing a delivery that already started is not a new action, so
   the interval floor must never hold it; and the gate verdict is recorded per head commit so a resume reuses
   the comment it already posted instead of stacking a second one. The forge is the truth about what is open;
   the state file is a cache (and the fallback when the forge cannot be asked).
9. **Do not run the routine end-to-end to verify a change to its publication step.** The run performs the
   *current* side effects, so a brief that says "run it end-to-end" plus "do not push" is a contradiction —
   change the publication step first, or exercise only the pre-publication stages. Then give the publisher a
   switch that stops it *after* the commit (`SYNC_PUSH=0` / `--no-push`): that switch is what makes a real
   cycle verifiable later, with no repository side effect. Exercise a changed gate or
   notification helper in isolation instead too: source the shared lib into a stub with `NAME` / `STATE_DIR` /
   `LOG` overridden, call the helper, and the alert-and-suppress behaviour comes back in one command with no
   repository side effects.
   **A wrapper that has only ever taken its empty path is untested.** Take the ladder: (1) nothing under the
   scope ⇒ silent `rc=0` and no commit; (2) an untracked file outside the scope ⇒ the refusal line, no commit,
   tree unchanged; (3) a throwaway candidate with the switch on ⇒ a commit whose name list is *exactly* the
   scope. Then undo (3) and prove it: `git reset --soft HEAD~1`, unstage the scope, delete the probe, and assert
   `HEAD` and `git status --porcelain` equal the pre-run values. Prove remote and credential reachability with
   `git push --dry-run origin <default>` (`Everything up-to-date`, publishes nothing) rather than a real push.
   **When the wrapper's whole job is the push, drive the real pipeline against throwaway clones — not only
   the real repo behind the commit-only switch.** A bare repo as the remote plus `git clone --local` of the
   real repo with `origin` repointed exercises commit → gate → fetch/rebase → push → read-back end to end
   (the re-alignment path no `SYNC_PUSH=0` run reaches) while the real repo is read once and never a target;
   close the probe by asserting the real repo's `HEAD` and dirty set still equal their pre-probe values — a
   repo that was already dirty is compared against, not required to be clean. Harness, five-case matrix and
   the real-repo guard: `references/publisher-acceptance-probe.md`.
10. **Fixture-test the state machine before trusting it.** A state machine that has only ever walked its
   "nothing to do" path is untested: bare repo as remote + a shim for the forge CLI, then the five scenarios
   in `references/publisher-state-machine.md`. Assert the remote default branch's SHA never moves.
11. **Land the flow through itself (dogfood).** The change that introduces the PR path ships as the first PR
    it produces; whether the merge is a human action or the automation's own (a recorded local-CI comment that
    the repo contract names as the gate) is the contract's call — never the automation's improvisation.
12. **CI that cannot run becomes a recorded local gate — not a licence to merge blind.** When the forge's
    Actions cannot start (account billing, spending limit, private-repo minutes), read the check-run
    annotation for the reason: a job that settled in ~1s with an empty `steps` list never ran, and no code
    change turns it green. The bridge that keeps the repo shippable is mechanical, not prose:
    - run the workflow's **own steps locally, on the committed tree** (`git archive HEAD` — never the working
      tree), with the interpreter the workflow pins, verified; if the pin cannot be matched the stage fails
      with that reason instead of silently running another minor;
    - write the transcript (commit, interpreter, both steps, exit codes) to a task-dir log;
    - post it as a PR comment whose first line is exactly
      `verify: CI pass（本地跑 <workflow path>）`, followed by why the forge could not run (quoted annotation),
      the interpreter, both step results, and the transcript path. **That comment is the PR's CI gate**, and
      the automation merges through it (`gh pr merge --squash`), deleting the head branch explicitly;
    - a failing local run posts nothing and merges nothing: queue entry + deduped notification + non-zero exit.
    When the quota returns, re-enable the upstream check (`gh workflow enable <workflow>`) and go back to it —
    the local gate is a bridge, not a replacement. This is the cross-repo pattern for any repo whose CI cannot
    be paid for, so write the workflow file as the single definition both sides run.
13. **One delivery engine for every loop in the pattern; callers only map reasons.** When more than one
    repo/loop uses this protocol, implement fetch → ref existence → ff-or-rebase → dirty deferral →
    retry-once → read-back → never-force **once** in a shared module, and let each loop keep only its own
    gates, floor and reason→notification mapping. Hand-rolled copies drift silently — one loop gains the
    branch assertion and the retry while another keeps pushing by branch name — and the gap surfaces as an
    incident, not as a failing test. **Fix the pattern, not the repo the operator happened to name**:
    enumerate the members first (scheduler stores, each unit's `ExecStart`, hooks, forge workflows, and a
    grep for `git push` / `git -C` over the script trees). The caller validates the module's record shape
    before it evals it, and a git read that fails is a refusal — never `|| echo 0`, never "clean".
    **The member that does not source the module is the member an engine-side change silently skips.** One
    long-lived loop is typically a self-contained monolith — its own staging, commit, push, no `source` line
    — so the pattern has to be pasted into it in the *same* edit (same subject prefix, same guard) and that
    copy proved on its own: carve the shipped block out of the script between its two comment markers and
    evaluate it against throwaway clones, because there is no seam to source and a copy nobody
    executed is a copy that is wrong. Separate the two populations when reporting the rollout — who sources
    the module, and who carries a copy — and never take "the engine is patched" as coverage of the second.
    Command contract, reason keys and fixtures: `references/git-delivery-engine.md`.
14. **Split the gate list by what may legitimately move the verdict.** Only code/repo integrity may abort a
    run: the control-plane test suite (fixture-driven), structure/scope/size checks, the staged secret scan. A
    verdict that moves because the *owner's real data* or a freshly-imported document moved is **advisory**: a
    snapshot the routine reads goes red on a legitimate loss, a content lint goes red on the file that was just
    imported, and fail-closed there means the pipeline refuses to persist reality whenever reality is
    inconvenient — one such gate also freezes every unrelated pending change behind it. Implement one
    `sync_warn` beside `sync_fail`: log every run, deliver at most once per distinct finding (signature = short
    hash of the message, so a new defect re-alerts and a repeat is suppressed), keep its **own** state file so a
    warning never masks — or is masked by — a FAIL, and keep `held` / `no changes` / `FAILED <stage>` /
    `WARNING <stage>` four distinct timer-log lines. Advisory drops the abort only; the finding still goes to
    the    review queue. Say which side a red gate is on in the report: a blocked run is about the *repository*,
    never about the owner's content, and leaving that implicit reads as "your data was refused".
15. **Stage the scope, not the worktree.** A shared engine's `git add -A` is the wrong primitive the moment
    you hang a new repo off an existing multi-repo loop: a locally-modified submodule pointer, another agent's
    in-flight file, a scratch note — everything dirty rides along into the commit and out to the shared default
    branch. Stage the published subtree explicitly (`git add -A -- <scope>`) and then assert the staged name
    list holds nothing outside `<scope>`, `git reset` + fail if it does. The engine's allowlist of roots is a
    first refusal only; the staged-set assertion is the binding check, because it also sees deletions and
    renames. A modified submodule pointer is *normal* in a repo that tracks its refs as submodules and must
    never appear in a landing commit — and it is never inert either: the same pointer is what
    `status --porcelain` counts, so one left on a commit the branch does not record turns the align into
    `deferred-dirty` and then `dirty-behind`, wedging the loop until a hand repair
    (`references/git-delivery-engine.md` → *Wedge*). Generalize: the loop owns a path, not the worktree — the repo's other
    dirty paths are someone else's state. Append the repo to the member registry and leave every existing
    member's row untouched (one registry edit, no per-repo copy of the flow).
16. **A gate that runs after the commit owns an uncommit, and resolves its own runner.** When the repo's
    checker can only run against a commit (it diffs the staged set against the base the push will be compared
    to), pair it with `git reset --mixed HEAD~1` on failure: an unpushed commit left behind trips the same gate
    on every later tick, and the local branch reads "one ahead" — the same state a floor-held snapshot leaves,
    so the failure stops being distinguishable. Bind it to the base the push will really be compared against, and resolve that base to a **sha** the
    checker never has to interpret (`--base "$(git merge-base origin/<default> HEAD)"`). Handing the checker
    the moving remote-tracking ref itself is the defect: a `--base` that diffs its two endpoints reads the
    remote's own newer commits as *your* change, so an `origin/<default>` another writer has advanced makes a
    perfectly in-scope commit fail as "touched paths outside the landing zone" — a false refusal that looks
    like a scope bug and reappears on every tick while the remote runs ahead. Print the resolved sha in the
    run log, so the verdict names the base it was computed against. Resolve its runner by absolute path
    (`command -v <runner>` first, then the version manager's shim path): an `env -i` or cron PATH has no shims,
    and a runner that cannot be found must fail closed naming the runner — never silently skip the gate.

17. **One unpushed commit per loop — and only the loop's own commit may be rewritten.** A loop that commits
    on every tick, plus every hand-run of its wrapper, leaves several local commits inside a single publish
    window; a push refused on one tick and retried on the next leaves more, and the "one ahead" read that
    tells a floor-held snapshot from a failed run stops identifying anything. Fold the window's changes into
    the one commit the loop created and keep re-creating it until it publishes, then start a fresh commit.
    - Guard the amend on **both** conditions: the head commit is the loop's own (match the message prefix it
      writes) **and** it is unpushed (`git merge-base --is-ancestor HEAD origin/<default>` is false). Any other
      head ⇒ a new commit. The same repo carries other writers' commits (another machine, another lane), and an
      unconditional amend folds a peer's semantic commit into the mechanical one, destroying its message and its
      attribution. The other direction needs no state: once the push succeeds the ancestor test passes and the
      next change starts a new commit by itself.
    - Keep the window commit's original author date (`--amend --no-edit --date=<author date>`), so the history
      reads as that window's changes rather than as the last tick's.
    - Promise the invariant **per loop** — "this loop contributes at most one unpushed commit" — never "the
      branch is never more than one ahead": a human or another lane committing directly still adds one.
    - A scoped loop (subtree-only) is unaffected: the amend still leaves one commit whose name list is inside
      the scope, so a `--base "$(git merge-base origin/<default> HEAD)"` scope checker still reads one commit.
    - Route manual and session-triggered runs through the commit-only switch (rule 9), so a hand-run neither
      publishes mid-window nor contributes a second commit.
    - Prove it on a throwaway clone: new → amend (one commit, name list unioned) → push → the next change
      creates a second commit; a push refused on one tick and retried on the next still leaves one commit; a
      a foreign commit at HEAD is committed-to, never amended. Give every scenario its own setup assertion, so
      a setup step that silently no-ops cannot pass the case (mechanism: skill `verification-probes`).
    - **Read the invariant off the live repo, not only off the fixture.** The two dates name the two facts:
      `git log --format='%h %ad %cd %s' --date=format:'%m-%d %H:%M'` shows the loop's commit keeping its
      original **author** date while its **committer** date moves to the tick that amended it, and `HEAD`
      stays exactly one ahead of `origin/<default>` until the floor's next eligible tick publishes it. The
      run's only other surface is its own journal — a unit that logs to stdout has no log file to tail —
      `journalctl --user -u <unit> -n 30 --no-pager -o short-iso`, where `amended <sha>` followed by
      `held (min interval … left)` is the pair proving the amend ran and the push was deferred by the floor
      rather than failing.

## Decided-flow variant: direct push to the default branch

A repo's operating contract may decide the automation **owns** its default branch — typically because the
branch carries only regenerated, review-free content and a human merge would rubber-stamp. Then the default
branch is the delivery target, and the PR mechanics of rules 1–2 and 7–8 (branch push, PR create/update,
merge detection, comment gate, stale-branch cleanup) plus the resume/open-PR path do not exist. The cycle:

0. **Align first, always — and read the ref you will push.** `git fetch`, then decide the remote branch's
   existence from `git ls-remote <push-url> refs/heads/<default>`: a successful fetch does not prove the ref
   is there or current (a stale tracking ref, a fetch refspec that excludes it, a fetch URL different from
   the push URL all read as "in sync"). Ahead of the remote with a dirty tree ⇒ fail closed; behind ⇒
   `git merge --ff-only`; diverged ⇒ `git rebase` with **verified** rollback — on conflict, error or
   timeout abort and prove it (HEAD back at the pre-rebase sha, no in-progress markers left), and report a
   rollback you could not prove under its own key. A rebase left in progress wedges every later run, so a
   timeout that skips the abort turns one bad run into a permanent outage. **Never force, never
   auto-resolve, never push a half-rebased tree.**
1. regenerate → prune → gate → staged guards → one commit per run — unchanged (rules 4–6).
2. the idle exit compares `git rev-list --count origin/<default>..HEAD`: "this run committed nothing" is
   not "nothing to deliver" — a run the floor held still owes its snapshot.
3. the action floor: the state file keeps **only** `last_action_at`; `--force-sync` bypasses the floor and
   nothing else.
4. **Re-align in report-only mode, then gate.** Whatever the gate validates must be what ships: nothing may
   move the branch between the gate and the push, so the pre-gate align is read-only (`--report-only`, no
   reconcile) — a mode that reconciles the workspace first silently re-cuts the very commit CI approved.
5. local CI (rule 12, when the forge's CI cannot run) on the committed tree — the transcript is the
   artifact; there is no PR, so no `verify: CI pass` comment carries the verdict any more.
6. **Push the object the gate validated, by id.** `git push origin <sha>:refs/heads/<default>
   --no-follow-tags --recurse-submodules=no` — never a branch name (`HEAD:refs/…` lets the ref move under
   the gate) and never a force. Classify the refusal before retrying: non-fast-forward ⇒ re-fetch and retry
   **once**; permission/hook/policy denial ⇒ stop under its own key, since no retry can succeed. Then read
   the ref back from the **push URL** (`git ls-remote <push-url>`); that SHA must equal the pushed object,
   and a remote that acknowledged but cannot be read back is pushed-but-unverified — never "failed,
   nothing happened", because the remote already moved.
7. record `last_action_at` — nothing else. `held` / `no changes` / `FAILED <stage>` stay the three
   distinguishable lines in the timer log.

What this variant deliberately removes: the forge-CLI dependency in every form (branch push, PR
create/update, merge detection, comment gate, stale-branch cleanup, resume/open-PR, the `gh`-missing
failure path) and the PR bookkeeping keys. What it keeps: the regenerated-only invariant, the gates, the
staged guards, the floor, the review queue, and the reason-keyed daily notification. The compensating
control for "no human merge" is that every commit is regenerated from the source of truth on every run and
passes the same gates a PR would have passed — nothing hand-written may live on that branch.

Fixture the variant the same way, inverted: the pre-receive hook **allows** the default branch and
**refuses every other ref**; every run asserts with `git ls-remote` that no other ref ever appears (the
claim "it only ever pushes the default branch" must be falsifiable), and a `gh` tripwire shim sits first on
`PATH` so any call is logged — its log must stay empty for the whole suite.

## Locating the writer before pausing or repointing an automation

"Pause the auto-commit for repo X" is an attribution question before it is an edit: name the process that
writes X, or say plainly that none exists. Stopping one is a runtime-config change (reversible, but it
changes future behaviour), so snapshot the current state, make the edit, verify through the scheduler's own
view, and record the undo on the same line.

1. **Enumerate every timed writer in one pass** — the unit/job *name* is not the writer; the command it runs
   is:
   - scheduler stores: root **and every** `profiles/*/cron/jobs.json` — a listing command typically shows
     the root store only, so the profile stores are where the surprise lives;
   - `systemctl --user list-timers --all` **plus each unit's `ExecStart`**, then system timers, `/etc/cron.d`,
     `/etc/cron.daily`;
   - git hooks (`git config core.hooksPath`, `.git/hooks`) and the forge's workflow list with each
     workflow's `on:` block — a `push`/`schedule` workflow is the only repo-side writer candidate;
   - then grep the script trees for `git commit` / `git push`: a writer named `*-watchdog.sh` that commits is
     exactly what a name-based inventory misses.
2. **Read the publish script's own conditions, not the workflow's name.** A release job that tags on every
   default-branch push and commits only under an explicit manual argument is *not* an auto-committer — the
   commit sits inside its own branch (`if <explicit part> is not None: … commit … push`), and the normal path
   returns after tagging. Quote the condition as the evidence.
3. **A snapshot pipeline that resolves symlinks is a writer for the owner's purpose.** A home/config
   snapshot loop copies the *bodies* behind symlinks, so a refactored source tree (skill library, dotfiles)
   lands as commits in the snapshot's repo while the source repo itself has no automation at all. Report both
   refs: "nothing commits X" can be literally true and still useless to an owner who is about to refactor X.
4. **Hand back the inventory, never a guess.** One numbered line per writer (what runs / cadence / next fire /
   destination ref), then ask which one to stop — a wrong stop is silent staleness, and stopping one of
   several writers leaves the rest running.
5. **A temporary stop needs its restore trigger named in the same breath.** Who re-enables it (the owner on a
   date, or a job that restores the prior state) is part of the change; an unowned pause becomes permanent by
   default, and a paused job still reads as coverage in later audits.
6. **Verify the pause by the scheduler's own view** (`systemctl --user list-timers <unit>`, the job's own
   state field) and keep the exact reverse command beside it — not the pause command's exit code.
7. **Re-opening is the same enumeration in reverse, and the owner's description names at most one artifact.**
   "Turn the automation back on" / "re-open repo X" points at the mechanism the owner remembers; the freeze may
   equally live in a pause or allowlist record read by a *different* subsystem (a generator guard, a skill
   materialization pause file), and lifting that one writes into other environments entirely. Enumerate the
   suppressors first, run each one's own dry-run, and report the blast radius (how many destinations, how many
   items, how many of those items are already dirty) before touching anything. A stop that a host toolchain
   honours is outside the authority of "sync this repo": two artifacts, two separate answers — one owner
   sentence is not consent for both.
8. **A red drift/diagnostic report on a freshly re-opened repo is often the pause working, not a regression.**
   Date the finding before treating it as a defect: a check whose red list is exactly the destinations the
   suppressor covers, or whose red appears with none of your own files implicated, is the freeze's signature.

## Triage: a known publisher went stale

Order matters — each step either names the failing stage or rules it out:

1. **Confirm it is stale from the destination, not the timer.** `git -C <dest> log -1 --format='%h %ad'` on
   `origin/<default>` against now. A timer reading `active (waiting)` says nothing about whether pushes land.
2. **Read the timer journal, not the last notification.** `journalctl --user -u <unit> --since '3 days ago'`.
   The notification is deduped per reason per day, so a *persistent* failure notifies once and then goes
   silent while every tick still logs its stage line. Consecutive identical failures in the journal are the
   signal the notification withheld — never read silence as health. Nor is a red in the notification channel
   a state: a notifier that fires only on failure leaves its last red standing after a later tick or hand-run
   recovered, so the owner's "it is failing again" is first of all a claim about a *message*. Date it against
   the review queue, the action clock in the state file and the journal's stage lines before diagnosing
   anything; when the report turns out to be a stale red, answer with the recovery (which run cleared it,
   which commit landed and when) instead of re-running the whole triage in front of the owner.
3. **Read the failing stage's own output *and* the source repo's state.** `git -C <src> status` and
   `git -C <src> log origin/<default>..HEAD` separate "a gate aborted before any commit" (dirty worktree)
   from "committed locally, push withheld by the action floor" (clean, one ahead). The two need opposite
   fixes: generalize an offending file vs. just wait for the floor / re-run with `--force-sync`.
4. **When a repo-wide gate failed, the offender is usually in another file.** One path failing a whole-tree
   scan blocks every unrelated pending change with it, so fix that path (in the source of truth the routine
   regenerates from) and re-run — do not widen the gate, and do not treat it as a pipeline defect. Then
   verify `origin/<default> == HEAD` and a clean worktree, and clear any stale `systemd` failed state
   (`systemctl --user reset-failed <unit>`) so the next tick's verdict is the current one.
5. **Enumerate every gate; the reported stage is only the first red one.** Gates run in a fixed sequence and
   the run stops at the first failure, so every later offender is invisible until the earlier one clears —
   and the stage line *changing* between ticks reads like "the same failure mutated" when it actually means
   "the next gate is now exposed". Run each gate by hand from the wrapper's own commands before declaring a
   fix. The failure **signature** in the log is a hash of the message, so it is the identity of the failure:
   two gates produce two signatures and therefore two alerts (not a flapping job), and a
   `suppressed duplicate alert (<sig>)` line means that tick equalled the already-notified failure — never
   that the tick was healthy.

## Pitfalls

- **One byte in a repo-wide gate blocks every delivery.** A pre-commit scan over the whole ported tree (host
  paths, account/machine names, ids, credential shapes) aborts the *entire* commit on a single hit, so
  unrelated pending changes freeze with it and the destination sits at the last good commit while the log
  names only one file. Grep the whole staged diff against the gate's own regexes before pushing (read the
  token set from the gate script itself — a copy of those literals inside a ported doc is the same finding),
  and never admit the offending literal through the allowlist.
  **The usual trigger is an edit to a ported file, not the producer** — a skill that gains the owner's
  handle in prose, or a generated banner that hard-codes the script's own path — and it surfaces up to a full
  cadence later, in a run nobody was watching (four occurrences in one week on this host came that way). So
  when you edit anything inside the ported tree, run the gate's own scanner over the touched paths *before*
  you finish instead of waiting for the next tick, and read the token set out of the gate script rather than
  from memory: its name/id/path patterns match *every* line of a ported document, comments included, which is
  what makes ordinary prose the usual offender. Fix the finding in the live source of truth, never in the
  generated copy, and never by widening the allowlist.
  **Check the edit before the next tick without disturbing the real checkout**: hard-link a copy of the
  generated source tree (`cp -al <checkout> <tmp>`, then drop the copy's `.git`), replace inside the copy
  only the files you touched with their live versions, and run the gate's own script against that copy — the
  whole-tree verdict comes back with the real repo untouched, and the copy is deleted afterwards. Replace
  means remove-then-copy: editing a hard-linked file in place writes through to the original. Pass the copy
  as the repo root the gate takes from its argument; a gate that reads a fixed live path instead cannot be
  probed this way, and a hand-rolled grep over the touched files is not the gate's verdict.
- **Scope a recursive grep to the script/unit trees, never the whole home.** Ledger/session JSON under
  `~/.hermes/checkpoints/store/ledgers/` (plus install and backup trees) holds single-file JSON of tens of
  MB, so `grep -r` from `~/.hermes` or `~/claw` walks it and hits the tool timeout after the answer was
  already in the first files — pointing the same grep at `~/.hermes/scripts`, `cron/`, `systemd/user` and the
  target repo returns in seconds.
- **Reading the wrapper's closing line as the run's outcome.** `nothing committed` covers "no changes" *and*
  "a gate failed and aborted the run"; read the per-stage lines and timestamps.
- **Letting the automation commit the PR body from prose.** Conclusion line + gate result with counts +
  `git diff --shortstat` + deletion classes + review-queue path; the PR is what the reviewing human reads
  before merging, so no pasted logs and no raw JSON.
- **Opening a second PR for the same head branch.** An existing PR is updated by the push; only a merged or
  closed one starts a new cycle.
- **Merging on a gate nobody can see.** A bare "CI pass" comment is unverifiable: it must carry why the forge
  could not run (the annotation, quoted), the interpreter the workflow pins, both step results with counts, and
  the transcript path. The same failure that makes the forge CI unavailable also makes an unwritten local run
  unfalsifiable.
- **Assuming CI covered the change.** When the workflow never starts, the local-CI comment is the whole
  evidence — say so instead of implying the PR was gated upstream, and re-check whether the quota has returned
  before assuming the bridge is still needed.
- **Writing the PR path into a routine whose repo decided otherwise.** Check the repo's operating contract
  first: a routine that pushes a head branch or calls the forge CLI against a decided direct-push repo
  regresses to dead machinery (and an unattended failure mode) — the variant section above is the whole
  contract for that case.
- **A gate that asserts over live or regenerated data encodes the regime it was written in.** A validator
  reading the newest snapshot / ledger / generated config in the tree goes red when the *data* legitimately
  changes shape (a metric crosses a bound, a sign flips) with no code change involved. The tell is a red gate
  starting at the tick right after the branch fast-forwarded a new upstream commit in, with the gate's own
  file untouched — date it from the branch's reflog, not from the gate. Fixture such assertions (frozen
  input, not the live artifact) and treat the **assertion** as the defect: editing the artifact to make the
  gate pass destroys the thing the gate exists to protect. Fixturing is not sufficient on its own either: it
  makes the assertion a trustworthy guard, while rule 14 is what stops it — or any other data/content-dependent
  check — from aborting the run and holding unrelated pending changes hostage.
- **A lint rule with no autofix survives the pre-commit auto-heal.** A heal stage running `lint --fix` over
  dirty files clears only the mechanically fixable violations, so a non-fixable rule (broken link fragments,
  invalid anchors) keeps the gate red while the heal step reports success — read fixability from the linter,
  not from the heal step's exit code. In an imported or mirrored document the fix is to make the target exist
  (materialize the anchors), not to restructure the source for style.
- **A hand-run of a producer→gate pipeline must replay the whole sequence, prune included.** The gate
  judges the *destination* tree, so replaying only "regenerate → gate" reports every artifact the
  pipeline's prune step exists to remove (live-edit backups, runtime state) as a fresh violation — a
  wall of `port: never` findings on paths the change never touched, which reads like a producer
  regression and sends the operator hunting the wrong stage. The producer's copy list and the manifest
  drift by design; the prune step is what reconciles them and it runs *between* producer and gate
  (rule 5). Drive the pipeline itself, or replay its order exactly: a red gate whose paths your change
  never touched is the missing step before it is a defect.

## Reference

- `references/publisher-state-machine.md` — cycle (including the local-CI gate + merge), state file, merge
  detection commands, the local-CI transcript/comment contract, the direct-push variant's commands and
  scenarios, fixture harness.
- `references/git-delivery-engine.md` — the shared module contract (record format, reason keys), the full
  align/deliver command set, push / read-back / retry / rollback rules, the `dirty-behind` wedge a stray
  submodule pointer causes and its repair sequence, the race-and-tag fixture recipes, and the review checklist
  a fixture-green first draft still fails.
- `references/publisher-acceptance-probe.md` — the throwaway-clone harness and its five-case matrix
  (in-scope push, outside-path isolation, sensitive refusal, shape refusal, advanced remote), the
  real-repo-untouched assertions, and the pre-flight for a gate that will judge a new file inside a tree
  the host *generates*.
