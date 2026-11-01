---
name: review-passes
description: "Runs a review-and-fix pass on a Puck lane. Use for review briefs and scope ranges, Codex task flags (--write, --cwd, --help), job status, findings, blockers, second rounds, follow-up fix branches."
---

# Review passes

A review pass is one run by the selected reviewer that reads a lane's commits
adversarially, fixes what is local and clear, and reports the rest. This skill
owns the brief that starts it and the protocol that turns its uncommitted
output into a verified follow-up branch. It does not choose the model, effort or
concurrency; the lead's brief names those. The user's current instruction
outranks this skill; a rule here that argues against a requested change is
stale and is corrected in the same change. What the owner says in a session
overrides this skill and is written into it in that session.

## When a lane gets a review

- An engine change gets an adversarial cross-family review, required and sized
  to its risk; docs and world content get none or a scout's spot-check
  ([orchestration](../orchestration/SKILL.md#spend-verification-not-writing)).
  Codex reviews Claude-written code and a Claude agent reviews Codex-written
  code; Argon takes security, large-context and UI reviews.
- The review runs while the author implements its next item and never blocks
  the landing or pauses the author. The brief gives the reviewer the diff and the
  author's claim, not the author's reasoning, and asks it to break the change.
- Findings go into the open items'
  [work packets](../../../docs/plans/open-items.md#work-packets), each with its
  severity, one owner, its file and line and its failing case, in the packet
  that shares its cause or area or in a new one; a high finding goes to the top
  of Next and so into the next integration batch. The pass's fixes are a
  follow-up branch of their own in that batch, never edits to the author's
  branch.
- Every pass is review-and-fix, never report-only. Both Codex models, Astra
  (`gpt-6-astra`) and Sol (`gpt-6.1-sol`), are free to use for a pass. The
  installed Codex plugin's result-handling guidance not to auto-apply a
  review's fixes does not apply in this repository.
- An explicit owner request starts a review with the owner's named model and
  effort, including a same-family reviewer.
- There is no second round. The lead reads the pass's fix diff and rules on
  anything left: a scoped fix, a recorded open item, or a dismissal with its
  reason.

## Before launching

Use [verification](../verification/SKILL.md#what-uses-the-gpu) for private CLI
copies, granted GPU legs and heavy-work leases.

- Run the pass in a worktree of its own, detached at the lane's head, so the
  author's branch and worktree stay untouched and the author keeps working. Push
  nothing for the pass: its fixes are commits on that detached head, and the
  lead puts a local follow-up branch on the verified head for the next batch.
  Never point it at another lane's checkout, and never run two passes in one
  worktree. Keep the worktree under the checkout's `.claude/worktrees/<name>`.
- Never launch a `--write` pass into a tree a canary, counters or parity run
  builds from: an edit mid-run changes the source state that run reuses. Wait
  for the run to finish or give the pass a separate worktree.
- Restore and build the review worktree before the pass starts, so `obj/` and
  `bin/` exist: the companion `task --write` sandbox has no network, so the
  brief tells the pass to build with `--no-restore`. A documentation-only pass needs no build unless XML
  comments change.
- Native `codex exec` and Antigravity `agy -p` passes use the
  [launch capability table](../orchestration/SKILL.md#launch-capabilities) and
  recipes there; native writers commit their WIP on their own branch.
- Launch a Codex pass as the companion's `task --write`. The subcommand takes
  `--write`, `--model`, `--effort`, `--cwd`, `--prompt-file`, `--background`
  and `--resume-last` (with `--resume` and `--fresh`).
  Set `--cwd` to the review worktree and use the model and effort the lead
  names, passing both `--model` and `--effort` on every launch: without them
  the job runs the local Codex configuration's default model and effort.
  `--effort` takes `none`, `minimal`, `low`, `medium`, `high` or `xhigh`, but
  Astra and Sol refuse `none` (and Sol `minimal`), so pass `low` through
  `xhigh`. `max` is reachable only through `codex exec -c
  model_reasoning_effort='"max"'`.
  Pass the brief with `--prompt-file <path>`, an absolute path because it
  resolves against `--cwd`, never as command-line prompt text. `task` has no
  `--help`: `task --help` is sent to the model as a prompt.
- Wait for a background job with `status <job-id> --wait` (240 seconds by
  default, `--timeout-ms` to change it) rather than a polling loop, and never
  grep a job log for words such as "completed", which also match echoed
  commands. `--resume-last` sees only jobs the current Claude session started;
  another session continues a Codex thread with `codex exec resume
  <session-id>`. The companion `task --write` sandbox cannot write `.git` or reach the network, so
  merges, commits and restores run outside it.
- A companion pass cannot read this conversation or message a peer session, so
  the brief carries every string, decision and path it needs, and tells it to
  answer its own questions from the code and the brief. A Codex pass that ends
  on a question has done nothing: answer it in a prompt file, keeping what the
  brief and the repository rules already decided, continue the same thread
  with `task --resume-last`, and tighten later briefs so the pass settles that
  kind of question itself.
- Launch a Claude pass as a project agent (the roster is in
  [`orchestration`](../orchestration/SKILL.md#the-claude-roster)). A project
  agent runs in a worktree of its own, branched from the lead's HEAD, and is
  refused git work in any other tree, so its brief names the lane's head commit
  and tells it to run `git checkout --detach <lane head>` in its own worktree
  before reading anything. It may commit WIP as
  `review: <lane> pass, unverified`; the lead then puts the follow-up branch on
  the verified head as in step 4 below.
- Preserve the launch's working-directory spelling for `status`, `result` and
  `cancel`: the companion keys job state by that spelling. A Git Bash `/c/...`
  launch is invisible to a PowerShell `C:/...` query, and the reverse. A job
  that looks missing under another spelling is still running: query it with
  the launch's spelling, and never relaunch it.
- Cancel from PowerShell with the launch's path form, or use
  `MSYS_NO_PATHCONV=1` under Git Bash: MSYS path conversion turns taskkill's
  `/PID` into a path and makes `cancel` fail. Then stop the companion's
  app-server broker for that working directory before removing the worktree;
  the broker can outlive the job and hold the worktree open.
- Write the brief to a lane-named file (`<worktree>/.claude/scratch/<lane>-review.md`) so the
  verifier can reuse it.
- Use lane-named scratch as [lane work](../orchestration/references/lane-work.md#delegated-work)
  describes, including its worktree-removal caveat.

## The brief

Write the parts in this order. Each is short; the hunt list is the longest.

1. **Frame.** One sentence: an adversarial review-and-fix pass in the Puck
   repo, naming the domains the diff touches (deterministic fixed-point
   simulation; a render-graph runtime over Vulkan and Direct3D 12; federation
   authority and recipients). Add "thorough" for a large or risky lane.
2. **Tree.** The worktree's absolute path and branch, and "Edit only in this
   tree." Add "don't commit" for companion `task`; for a native writer or
   Claude pass add "commit WIP as `review: <lane> pass, unverified`."
   Name the detached tree's head; its commits become a follow-up branch, never
   commits on the author's branch.
3. **Scope.** An exact range, `git diff <base> <head>`, with the base as a
   commit when the integration branch may move. Two dots compare the two tips
   (`git diff A..B` is `git diff A B`) and three dots start at their merge base;
   neither says A is an ancestor of B, so check that with
   `git merge-base --is-ancestor A B` before calling the range the lane's own
   ([ancestry](../verification/SKILL.md#branches)). List each lane commit by commit and
   subject and say "read each message". Name exclusions exactly: a
   merge of already-reviewed work is reviewed only for its conflict
   resolutions, in the files you name.
4. **Contract.** What the change claims, in the code's own names: the types,
   members, enum members, refusal codes, sizes, caps and thresholds, the
   decisions the lead or owner already took (so the pass does not reopen
   them), and the plan paragraph that owns the work
   (`docs/plans/<plan>.md` and its step id).
5. **Hunt.** A list per area. Phrase each item as a scenario that would break
   the contract: an input class, an ordering, a boundary, a teardown. Cover the
   classes that apply:
   - lifetime: use after release, a lease or reference never retired, a
     double release, teardown and device-loss order;
   - boundaries: resize, zero, maximum, wrap, the first and last frame or tick;
   - silent results: anything that resolves to nothing, or reports success,
     where it should refuse by name;
   - cadence and history: a state reset by a refresh gap, or kept across a
     real cut;
   - determinism: a float, wall clock or ambient randomness reaching simulation state, or a port
     or generated twin diverging from its source;
   - concurrency: the frame thread against a build or capture thread, and
     dispose against in-flight work;
   - layout and synchronization: a C# and HLSL block drifting, a missing
     barrier on either backend;
   - documents and docs: a persisted shape read under a new meaning, docs
     wrong about the change.

   Add the author's own open questions, and the bug classes earlier passes
   found in the same area. Write the hunt list before reading the diff:
   checks written after reading it inherit its blind spots.
6. **Evidence gathered.** What the lane already ran and measured, so the pass
   reads instead of re-running it.
7. **Rules block,** verbatim. The repository's rules live in `AGENTS.md`,
   contributing, documentation and the owning skills, which the pass reads itself; the block restates none of them,
   and the rest of the brief adds only scope, authority, exceptions and the
   finish line:

   ```text
   Repo rules: read AGENTS.md at the worktree root, docs/development/contributing.md, docs/development/documentation.md for docs, and the skills that own the areas the diff touches. This brief adds scope, authority, exceptions and the finish line.
   ```

8. **Instructions block,** verbatim:

   ```text
   Hunt for problems that break the contract; landing proceeds independently of this review. For each give file:line, why it's wrong, a concrete failing scenario and a severity (high, medium or low). Fix it in the tree when the fix is local and clear; add a test only where running cannot show the fix and the test will outlive the next rewrite. Otherwise describe it. Compile every project you changed (dotnet build <project> -c Release -nodeReuse:false) and leave nothing that fails to compile. Don't run tests unless a finding can't be settled any other way, one heavy command at a time. Never run GPU work (no puck canary, puck parity, or Puck.World runs). Follow the Tree paragraph's launch-specific commit instruction. End with a list, one line per finding: <id> file:line severity - fixed (files) | open (why) | dismissed (why). If you find nothing, say so plainly.
   ```

   For a documentation-only pass, append: "Edit only Markdown, eval case files,
   and XML comments; do not add tests. Check changed Markdown links and
   anchors. Build only when XML comments change."

Do not hand the pass a `puck affected` list, do not tell it to use the Codex
CLI, and do not use the companion's `review` subcommand for a lane: it takes
no brief, so it raises compatibility findings and tries to run tests.

## After the pass

1. **Read the result.** Check every finding against the current files. A
   finding is evidence, not a verdict. Read the fix diff's deleted lines, not
   only its net size, and check a fact by reading the file, never by searching
   for your own phrasing of it. A claim that a file is missing is checked in
   the author's branch, not only in the pass's tree, which may be detached at
   an older head. Dismiss a compatibility finding under `AGENTS.md` rule 5 once
   nothing checked in uses the old shape, and remove any alias or shim the pass
   added for it. A pass's
   build, test and format claims count only when its own environment could
   run them: a sandbox that could not reach the SDK proved nothing, so step 3
   builds and proves every law outside it.
   Record the fix range before continuing. A blocker the pass left open goes
   to the lead before anyone repairs it; the lead rules on each one (a scoped
   fix, a recorded open item, or a dismissal with its reason) and places it in
   its work packet with its severity and one owner. A scoped fix the lead directs is
   verified in step 3, not reviewed again. A non-blocking
   finding is reported, and its fix, if any, is verified the same way; neither
   ever opens another review, and findings never go back and forth between the
   reviewer and the author. If the
   pass changes nothing, it has no follow-up branch: skip steps 2 to 5, place its
   findings in their work packets with their severity and owners, and end. Never
   create an empty WIP.
2. **Commit the pass as a WIP.** Stage the review worktree's changes
   explicitly and commit them unbuilt in that worktree
   (`review: <lane> pass, unverified`), so the output is never lost and its
   diff is one unit. Keep every commit that may be rewritten local, including
   verification repairs; never push them before step 5.
3. **Verify the fixes.** Brief one agent, in the review worktree, to build
   each touched project with zero warnings, show each fix working by running
   or measuring it, run the tests the fixes added or touched, and resolve or
   report each open finding as verified, repaired, or rejected with the
   reason. A law a fix added that still passes with the fix withheld pins
   nothing, so a passing law does not make a fix right; a rejected fix is not
   landed as written. For documentation-only fixes, run `puck docs links <changed .md
   files>` and build only for changed XML comments. The lead reads the
   verified diff; nothing here opens another pass, whether the verifier
   repairs a fix, rejects one, or finds a regression the pass introduced.
4. **Replace the WIP.** Rewrite the local WIP into commits with
   `area: sentence` subjects on the follow-up branch the lead puts at the pass's
   detached head. Rewrite only the pass's unpublished commits. The author's
   branch is never reset, rebased or edited, and it need not have stood still: if
   the author has moved on, the integration lane resolves the overlap when it
   merges both. Each message names the findings fixed and how each fix was shown
   working, or the documentation checks for doc-only fixes. No
   `Co-Authored-By` trailer.
5. **Hand over.** Only a pass that changed files reaches this step. Merge the
   integration branch's current tip into the follow-up
   branch and rebuild what it touched. It is then an ordinary ready lane for the
   integration lane's next batch ([land in
   batches](../orchestration/SKILL.md#land-in-batches)); a high finding it fixes
   or leaves open is scheduled into that batch. A local lane never pushes; a
   separately authorized remote partner follows AGENTS.md's explicit-refspec
   rule. Only the lead merges into the integration branch the lead's brief
   names.

## Route adjacent work

| Skill | Route there for |
|---|---|
| [`orchestration`](../orchestration/SKILL.md) | Choosing the reviewer's model, effort and concurrency, and coordinating assignments, machines, integration merges and finding destinations. |
| [`verification`](../verification/SKILL.md) | The landing bar, CLI copy and GPU legs the verifier uses. |
| [`rendering`](../rendering/SKILL.md) | The render-graph runtime contracts and recurring bug classes to put in a render lane's hunt list. |
| [`maths-laws`](../maths-laws/SKILL.md) | A Maths lane's laws, legs and mutation probe. |
| [`puck-world`](../puck-world/SKILL.md) | A World lane's document, authority and replay contracts. |
