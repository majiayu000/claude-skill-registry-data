---
name: orchestrate-dealer
description: Run the main session as an orchestrator that deals work out to clean-context subagents, so it can work for hours without /clear. Use for any task of more than one step (a plan task, a batch of fixes, a whole phase), when bringing material from another repo, and when the session context passes ~150k tokens.
license: MIT
compatibility: Claude Code or any Agent Skills agent with subagents; git; reads .claude/gw.json
metadata:
  version: "0.4.3"
  source: "Galivelop workshop; generalised from the Tarkor, installer and portal orchestrate-dealer"
---

# orchestrate-dealer

If `.claude/gw/orchestrate-dealer.md` exists in the project, read it first: it holds what is specific to the project.

The main session is the **orchestrator**: it holds the plan, the decisions and the thread with the user, and deals each
chunk of work to a subagent that starts with an empty context. Every deal is an automatic `/clear`: the main session
receives a short summary and grows slowly. Reply to the user in the project's `language`.

Config values used below come from `.claude/gw.json`: `check` (list of commands), `log` (handover file),
`protectedBranch`, `language`. Read it once at the start.

## Who does what

| Orchestrator (main session) | Subagent |
|---|---|
| Talk to the user, ask, present | Read code, long docs, logs, screenshots, other repos |
| Split the task and write each brief | Implement, debug, run the tests |
| Decide (design, what to fix, what to log) | Run a batch of manual or end-to-end checks |
| Review what returns: `git log`, `git diff --stat`; the whole diff only when in doubt | Commit and push its work, log update in the same commit |
| `/code-review`, `/opt-tokens`, `/retro`, PR and merge | none |

A read of more than ~200 lines, or a long output, in the main session is a chunk that was not dealt out.

## Steps

1. **Split.** With the `selector` already applied, cut the task into chunks one subagent can close in one go: a fix,
   a module, a screen, a command. Each chunk gets a **done criterion** that can be checked (a green test, a green
   CI job, a pushed commit), a list of what blocks it and the files it touches. The **frontier** (one wave) is the chunks
   nothing pending blocks: they go out together (see Rules), but two chunks of one wave never share a file: the second
   waits for the first. With more than ~5 chunks, a cheap-model subagent may review the split before launch (missing
   blockers, shared files, criteria that cannot be checked). Cap a subagent at ~30 tool calls (one or two proposal rows); at the cap it saves its state in `log` and the
   next one resumes from it. A subagent's context grows with every call: chunks of 44-55 calls averaged 100-116k (and 9 of the 10
   costliest subagents of one session went past 33 calls),
   and splitting them costs one more ~50k startup but far less than the drag. A one-file fix whose place the reviewer already gave is not a chunk: the main session
   makes it, with its tests (a subagent pays ~50k just to start and rediscovers what the session knows).
2. **Deal.** One subagent per chunk with the Agent tool, in the foreground when the next chunk depends on it. Model and
   effort follow the `selector` ladder: `sonnet` to implement, `opus` to debug something non-obvious. Fixes from a
   review go to `sonnet` too: the reviewer already closed the plan (where and what to change). The brief carries
   **pointers, not copies**: where the material is (the log row, the plan task, a doc, a commit, a file and
   function), never the pasted text. Template:

   ```text
   You work in this repository on branch <branch>. In a fresh, clean worktree, first check that `git log -1` matches
   `origin/<branch>`; if not, `git fetch origin <branch> && git reset --hard origin/<branch>`. Read your state with
   `python3 .claude/gw/scripts/recuperar.py --estado`; if it reports no row for your branch or the log has no
   per-branch rows, read the next step and pending sections of {log}. If you touch code, read REVIEW.md and
   AGENTS.md. Follow the project's commit and push rules: commit and push each stable point, log update in the
   same commit. If the push is rejected, `git fetch` and `git merge` (never rebase), then push again.
   At ~25 tool calls, commit (`WIP:` if red), push, and reply with what is left under MISSING.
   To wait for something long (a push with its check), run it with `run_in_background` and watch it with `Monitor`
   (load it with ToolSearch first) until it exits; keep your turn open while it runs, and never a foreground `sleep`.
   Push with its output to a file outside the tree (`git push … > "$(git rev-parse --git-dir)/push.log" 2>&1`); if it
   fails, read the pre-push reason in that file before retrying.
   Task: <what, in one or two sentences>.
   Files: <paths you touch>. Create: <exact names of what is new>. A path not listed here: stop and return it
   under QUESTIONS.
   Done when: <checkable criterion>. Run before pushing: {check}.
   For guard code or scripts: first list the edge cases (git states, platforms, empty or odd input) and write a
   test for each before calling the chunk done; the review afterwards is the safety net, not the first pass.
   Do not: <what belongs to another chunk or needs a user decision>.
   If you change a function or a field, grep every user of it and adjust them, or list them under MISSING.
   If you touch processes, paths or permissions, write it for every platform the project supports.
   If something needs a user decision, stop and return it as a question. Never merge into {protectedBranch}.
   Write your reply and commit message in {language}. Reply in at most 15 lines:
   DONE: … · COMMIT: <sha> · EVIDENCE: <command and summarised result> · MISSING: … · QUESTIONS: …
   If the chunk cannot be tested, reply NOT_TESTABLE: <reason> + the command that checks it another way, in place of
   EVIDENCE. Every number you report you counted yourself.
   Add FOUND: (one line per finding) and TOOLS: (failures of the project's scripts, hooks or CI) only if you have any.
   ```

   `{check}`, `{log}`, `{protectedBranch}` and `{language}` are filled from the config before sending. Add a line
   for each project rule a fresh agent could miss.
3. **Review what returns.** Fetch and check the commit (`git fetch`, `git log -1 --stat`) and that the done
   criterion holds. If it does not close, the retry climbs one ladder rung; two failures, stop and tell the user.
   Chunks that depended on the failed one are marked "cancelled: blocked by X" and listed to the user, never left waiting.
   For every subagent branch built in a worktree, **before merging it**, a subagent reviewer runs a short
   `/code-review` of its diff and returns only the findings; nothing merges until they are fixed. The reviewer's
   brief asks it to compare the diff with the **contract**: the doc that describes it and the real callers outside
   the branch (grep on the working branch), not the diff alone. Short per-branch reviews miss cross-branch breaks:
   a script against its backend, a doc against its code, two branches that edit the same rule.
   Log what comes back: `FOUND` and `TOOLS` into `log` (or the records the project keeps for them). `QUESTIONS`
   go to the user as they are, with the answer you recommend.
4. **Close the wave.** After merging the whole wave, one reviewer subagent compares the merged result with the task
   and returns `MISSING_ITEMS`: what the task asks for and no chunk covers. Each item becomes a chunk or a question.
5. **Continue.** Next chunk. One line to the user per chunk closed; the detail lives in `log`. When something long
   starts (a push with its check, a background subagent), one line to the user with what runs and roughly how long it
   takes; then wait for its notification.

## Rules

- **Code from a subagent gets its own review:** every chunk that changes code (always the hooks, push/merge guards
  and the scripts they call; also code a subagent commits on the working branch, not only worktree branches)
  passes a short `/code-review` by a reviewer subagent as soon as the chunk returns, before the next chunk starts
  (commit it first, as `WIP:` if needed, so nothing is lost if the session ends). The reviewer compares the diff with
  the contract (`AGENTS.md`, `REVIEW.md`, the callers), not the diff alone; its fixes land before moving on.
- **Before the PR, only what matters:** fix what is serious or medium, and what the fix itself breaks; log the minor
  findings as pending in `log` and do not review them again in this PR (`/code-review --max-findings all` still
  serves to list them). Otherwise every fix is reviewed again, brings new findings and the PR grows without end.
- **One writing subagent at a time on the same branch.** Two that commit to the same branch collide in the log and in
  shared files. In parallel, only what does not write (searching, reading, measuring).
- **Code fixes of the frontier, in parallel, in isolated worktrees:** each subagent runs with `isolation: "worktree"` in
  the background, commits at every stable point (`WIP:` if still red, so a restart loses nothing), does not touch the
  log or push, and returns its branch. The main session has each one reviewed (step 3), merges them one by one
  (merge, never rebase; `check` after each), writes the log and pushes. When the session folder is not the repo root
  (a cloud session starts in `/home/user`, next to other repos, and `isolation` lands the worktree in the wrong one),
  the main session creates each worktree itself with `git -C <repo> worktree add <folder> -b <branch>` and puts that
  folder in the brief, without `isolation`.
- **Shared records, main session only:** with parallel subagents none touches `log`, the findings register or any other
  shared record; they return their entries under `FOUND` and the main session writes them. Parallel writes conflict
  on merge.
- **What names files of a branch, after merging it:** indexes and docs that link to files created in a worktree are
  written in the main session after that branch is merged; before, the links point at files that do not exist yet.
- **Manual or end-to-end batches run in a `sonnet` subagent, in series:** the main session does not drive the
  tool itself; it deals batches and logs what returns. **Size a batch by its items: 6-8 checks**, and split it on
  the fly when it grows (batches of 11-14 blew a 60-call cap; 6-8 kept within it). Screenshots only when the finding
  is visual; otherwise the text tool's output. Batches share the environment, so each leaves it in a state the
  next can resume from and says so under `MISSING`. **Before dealing a batch, check that the starting state gives
  each check its precondition** (the scenario, data or account it needs); if not, the first chunk prepares it.
  Checks dealt on a state that cannot reach them burn whole subagent calls.
- **A subagent never talks to the user:** what it needs from them returns as `QUESTIONS`.
- **A subagent cut off by a usage or API limit is resumed, not restarted:** send it a message (SendMessage to its id)
  once the limit resets; it continues from its transcript. A new subagent would redo the work. Commit its partial
  work as `WIP:` meanwhile.
- **Intermediate state stays out of git:** dumps, screenshots, scratch logs and bench outputs go to a scratch folder
  (or a path in `.gitignore`); only results, tests and the log are committed.
- **Measure:** `/opt-tokens` before each PR compares the average context per call, the compactions and the per-model
  split with the previous session; if they do not fall, the dealing is staying in the main session.
- **A batch of approved rows is dealt, not worked inline:** the rows of an approved proposal or a findings list go
  one per subagent (or 2 small related rows per subagent), in series on the working branch, each reviewed as in
  step 3. A row the main session keeps (a one-file fix) counts against a stretch: every 4-5 rows, or as soon as the
  context passes ~150k, it writes the handover in `log` and recommends a `/clear`. Saying "dealt out" and then
  working 18 rows inline cost a 191k average context over 157 calls.
- **Automatic compaction is the net, not the plan:** at task boundaries write the handover in `log` and recommend
  a `/clear` to the user rather than letting the context grow. In the cloud the net may be missing: the session
  starts outside the repo and does not load its `.claude/settings.json` (`doctor.py` warns).
