---
name: review
description: The lead's review of a lane's finished branch before it merges. Runs code-kit verify on the branch, checks the work against its story's requirements and acceptance criteria, the spec-check report, the approval log and the tests, runs the security reviewer on sensitive changes, and ends with merge or send back. Use when a lane agent or person finishes a story, when the person asks to review a branch or pull request, or runs /code-kit:review [branch, story ID or PR number].
---

# Review a lane's branch

Only the lead reviews. The argument names the branch (`web/st-4`), the story (`ST-4`, whose branch is `<lane>/st-4`) or a pull request number. With none, review every story `code-kit status` shows in review.

The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`. `<base>` is the branch the lanes started from: the lead's branch, or the first protected branch.

## 1. Find the work

- **The branch and its story.** `status --json` lists each story with its branch, its commits ahead of the base, and its worktree, if one is checked out. For a pull request, `gh pr view <n> --json headRefName,baseRefName` gives both.
- **Where to run things.** Use the branch's worktree if it has one. Otherwise check it out in a throwaway worktree: `git worktree add .claude/worktrees/review-st-<n> <branch>`, and remove it when you're done.
- **The spec-check report** is in that worktree, in `.claude/state/spec-check/<branch with / as _>.md`. The state folder isn't committed, so a branch pushed from elsewhere may not have one. Say so, and review against the specs directly.
- **The lane's report** is beside it, in `.claude/state/reports/<branch with / as _>.md`: what it did, the commands it ran with their output, and what's left. Its hand-back to you was a few lines naming this file; read the file here, not before, and only the parts the review needs.

## 2. Run the rules

From the branch's worktree:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" verify --base <base>
```

`verify` holds a `<lane>/…` branch to that lane's paths, and checks:

- that every protected change is in the approval log, which is append-only;
- new layer violations, and a baseline that grew;
- screens without an approved design, or with one only in the design tool;
- for a lane's branch that builds screens, each approved state the review hasn't yet compared and recorded ("Builds compared with their designs"): it lists the comparisons step 3 still owes, and clears as you record each screenshot, so it isn't a reason on its own to send the branch back;
- committed secrets;
- tests weakened (deleted, skipped or focused, cut down, or a snapshot rewritten) without the person's `tests` approval in the log;
- for a fix (its story has `**Fixes:**`, or the branch is `<lane>/fix-…`), that its tests fail without the fix, as the bug, and pass with it;
- the project's checks for the changed files.

Any other problem it reports means the branch goes back. Don't fix a lane's code yourself; the lead doesn't write lane paths.

## 3. Check the work against the story

Read the story and every requirement it cites. Then start from what's already been worked out, not the whole diff: the lane's report (`.claude/state/reports/<branch with / as _>.md`, in its worktree or the main checkout), the reviewer's findings when the background reviewer ran, and `git diff --stat <base>...<branch>`. Open the diff one file at a time (`git diff <base>...<branch> -- <file>`) for the files each requirement depends on and the files a finding names, and a changed file in full only where its diff doesn't show the behaviour. Everything you open stays in your context for the rest of the build, so open what the verdict needs. Then, for each requirement:

| Requirement | Acceptance criterion | Built (where) | Test (which) | Verdict |
| ----------- | -------------------- | ------------- | ------------ | ------- |

- **Built end to end:** the behaviour works from the entry point to storage and back, including the errors, permissions and states the spec lists. A mock, stub, hard-coded response, placeholder screen, `TODO` or "coming soon" in shipped code fails the requirement.
- **Tested:** a test proves each acceptance criterion and names the requirement ID. The test would fail if the behaviour were broken; one that asserts nothing, or only asserts a mock, doesn't count.
- **Its journeys still pass end to end:** where the project has a QA lane, run the end-to-end suites that cover this story's requirements (the qa lane's command, filtered to them) against the branch. A journey that broke fails the review, even when the story's own tests pass. A story the QA lane delivered is reviewed the same way: each journey's test proves the requirements it cites, through the real screens and services, with no mocked responses.
- **The spec-check report matches:** its table has no row still `missing` or `conflicts` without an answer, and its questions were answered, not guessed.
- **Only the story:** changes beyond the story (refactors elsewhere, other stories' requirements) are sent back, or split into their own story. A new dependency is yours to judge, as in `/code-kit:decide`: the story's requirements need it, nothing the project has does the job, and it fits the principles and the layer. Only what crosses a guardrail (the spec, a contract, the architecture) is the person's call.
- **Built to its design:** for a story that builds screens, `code-kit designs ST-<n>` lists each screen's approved states. Take a screenshot of each built state at the design's viewport (the project's end-to-end runner, or a headless browser) as a PNG, and set it beside the state's PNG. A missing state or a different layout is a blocker, naming the state and its design file; different copy or components fail it too; spacing within the design system's scale is a nit. Record each screenshot you compared, whatever the verdict:

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" designs evidence ST-<n> <screen file> <state> <screenshot.png>
  ```

  It's refused when the screenshot isn't a PNG at the design's viewport (1x to 4x); take it again at that size. `verify`, and the merge queue, report every approved state of the branch's screens with no screenshot recorded since the screen last changed, so a branch that moves after your review is compared again. A state the build can't serve yet (the contract has no field for what the design shows) goes in the report with what's missing, and you add the story that provides it, rather than leaving a gap nobody sees.

- **Contracts respected:** the code uses the contracts as written. A lane that needed a contract change should have asked, not worked around it.
- **Standards kept:** `code-kit standards --for <changed files>` lists the project's standards for those files' layers. Check each changed file against the ones marked `checked` (the hooks already refuse what an `enforced` one names). A broken required standard sends the branch back, naming the standard's id and where; a broken recommended one is a concern; advice is at most a nit.

## 4. The security review

Ask whether the change needs it:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" security --base <base> --branch <branch>
```

It does when the diff touches sign-in, permissions, input from outside, personal data, encryption, payments, secrets, or queries and commands built from strings, adds dependencies, or the story cites a security requirement; it says which, and where. When it does:

- Run the `security-reviewer` agent (Agent tool, `subagent_type` `security-reviewer`, its `description` naming the branch, such as "Security review web/st-12", so the loop knows the story is under review) with the branch, the base, the story, its requirements, the spec files it touches (their `## Threat model` and `## Security requirements`) and the reasons `security` gave. It reads only, and ends with the same findings block as code-kit's reviewer: each finding graded blocker, concern or nit, with where, the attack and the fix.
- **A blocker fails the review**, like a failing test: the branch goes back to its lane with the finding (where, the attack, the fix). Concerns are yours to weigh: send back the ones the threat model says matter, and put the rest in the report. Nits go in the report.
- No `security-reviewer` agent in the project: `security` says so. Review the diff yourself against the same list in `${CLAUDE_PLUGIN_ROOT}/templates/security-reviewer.md`, and tell the person that re-running `/code-kit:init` adds the agent.
- A background reviewer can't start agents: it lists the security review as due, as a concern with the reasons, and the lead runs it.

## 5. Verdict

Report the table, `verify`'s result, the security review's findings (or that none was needed) and one of:

- **Files any agent may write** (`anyActor`, such as a lockfile or recorded decisions) have no owning lane, but they have a reviewer: `trace <file>` names it (the lead unless the config names a lane). Review those changes as that reviewer would, or ask that lane's agent.
- **Merge.** Everything passes, and the security review found no blocker. Put the branch in the merge queue, set the story's `**Status:**` to `done` in the plan, and commit:

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" queue add <branch>
  ```

  Branches merge from the queue one at a time, in the order their reviews passed, each verified against the base as it is then. Where `approvals.delegate.merge` is on and the harness's autonomy is `autonomous` or `vibe`, you merge the head: `code-kit queue merge --delegated` (code-kit's loop asks you when it's its turn). Otherwise the person merges it, with Merge in the code-kit band or `code-kit queue merge --person`. The queue records the commit your review passed and merges exactly that commit. A branch that moves on after your review leaves the queue: review it again, then queue it again. A head that no longer merges cleanly, or fails verify against the moved base, is sent back to its lane on its own; dispatch the fix as for any send-back. When the branch is merged, remove its worktree. Where the base's rules set `branches.publish`, the merge also reaches the remote's base on its own: pushed, or as a pull request code-kit opens from `code-kit/publish-<base>` (and merges, where pushing the base is delegated to you). Never merge a story into another branch to get it there: `code-kit publish --delegated` tries again when GitHub held it back. A branch that breaks the base merged on its own (a new API whose callers another story updates) is queued with the branches it lands with: `queue add <branch> --with <other>`. It waits in the queue, without asking for review again, until they're reviewed and queued too, and then they're verified and merged as one. In a team whose provider checks pushes for drift, a branch with an open finding at the level the provider's setting names waits in its place too, and the queue goes on with the next: `queue` and `next` say which finding and that the tech lead decides. It clears when the finding is resolved on the provider, or a push fixes what it found; never merge around it.

- **Send back.** List each problem, where it is, and what "fixed" looks like, with the requirement or the standard's id it breaks. Record the send-back, so `status` and `next` read the branch as waiting for its fix rather than finished:

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" sent-back <branch> --reason "<the problems, in one line>"
  ```

  Dispatch the story again to a fresh agent with the list added to the brief (`/code-kit:dispatch`, which first releases the branch's worktree), never to the agent that built it: its context is already large. Set the story's status to `in progress`.

- **Ask the person.** When the right answer is a product or scope decision (the spec is silent, or the lane found a real conflict), put the question to the person with your recommendation. Don't merge around it. Under vibe it's yours: decide it, record it in the brief's decision log, and send the branch back or merge accordingly.

Keep the report short: the verdict first, then the table, then the problems.
