---
name: address-pr-comments
description: >
  Triages every open review thread on a merge request or pull request, then acts on each one. For a
  thread you agree with, it implements a tested fix, replies in-thread with the fixing commit, and
  resolves the thread. For a thread you disagree with, it replies with your reasoning and leaves the
  thread open for the human reviewer to close. It ships with adapters for GitLab and GitHub as the
  code host, and it degrades to any other host that tool discovery can reach. This skill is
  user-only: it runs only when the user invokes /address-pr-comments <MR or PR URL>. When the user
  wants to work through reviewer feedback on a GitLab MR or a GitHub PR, resolve review comments, or
  address a round of code review, suggest this command instead of triaging threads by hand.
argument-hint: "<merge/pull request URL>"
allowed-tools: [Read, Bash, ToolSearch]
disable-model-invocation: true
---

# Address PR/MR Comments

Two generic terms run through this skill. A "change" is what the host calls a merge request on GitLab, or a pull request on GitHub. The host adapter keeps that host's own word when it names a concrete API object or CLI call. A "thread" is a GitLab discussion or a GitHub review thread. It is a root comment plus its replies, and it resolves independently of the rest of the change.

The workflow is host-agnostic. The host-specific mechanics live in adapter files under `references/`, and each one loads only when you reach the step that needs it. That keeps the always-loaded body focused on judgment, which is the classification of each thread and the fix to the code. Both stay the same wherever the change lives.

This skill is not a code review. It acts only on threads that reviewers already raised, and it does not evaluate the change on its own merits. For a first-pass review that surfaces new findings, use `/pr-review` instead.

## Workflow

Work through the steps in order.

### Step 1: Identify the host and load its adapter

Determine which host holds the change, mainly from the shape of the URL:

- A URL that contains `…/-/merge_requests/<n>` is GitLab. Read `references/hosts/gitlab.md`.
- A URL that matches `github.com/<owner>/<repo>/pull/<n>` is GitHub. Read `references/hosts/github.md`.

The adapter file is the authority for the mechanics of that host. It covers URL parsing, the auth check, and the exact calls that list threads and fetch metadata. It covers the local-clone path convention, and how to reply to and resolve a thread. It also covers the gotchas of that host. Read it now, and follow it wherever a later step says "per the host adapter".

When no adapter file exists for the host in front of you, degrade instead of stopping. Discover the relevant tools with a keyword `ToolSearch`, or with the platform's CLI or API. Make sure that the fetch-metadata, list-threads, reply, and resolve operations you need exist, then proceed. Tell the user that you are running without a dedicated adapter, so they know that host-specific behavior is best-effort.

### Step 2: Fetch change metadata and open threads

Use the metadata call from the host adapter. Fetch the title, the source branch, and the web URL of the change. The summary in Step 10 needs all three, and the source branch drives the workspace in Step 3.

**If the metadata call fails with an auth error**, the CLI or tool that the host adapter names is not authenticated. An auth error is a 401, or a "not logged in" message. Stop and ask the user to authenticate, and quote the exact command from the adapter.

Use the list-threads call from the host adapter. Fetch every thread, then keep only the threads that are still open, which means unresolved. For each open thread, capture three things. Capture its ID, which you need to reply and to resolve. Capture the file and line it anchors to, when it is inline. Capture the full body of every comment in it. You need the whole exchange, not the first comment alone, because a later reply from a reviewer often narrows or changes the ask.

When there are no open threads, skip to Step 10 and report that there is nothing to address. No workspace is needed.

### Step 3: Prepare the fix workspace

This step holds real commits that get pushed back to the source branch of the change, which a read-only review never does. So the workspace sits on that branch, and never detaches at a SHA.

The script picks the workspace, and you must not ask the user which one to use. When the user's clone already has the source branch checked out, the script works there. That directory is the one the user watches, and one branch cannot be checked out twice anyway. Otherwise the script adds a separate worktree, so that a checkout does not switch the branch under the user.

Locating the clone, fetching, and refusing to build on a leftover or colliding workspace is deterministic and identical on every run. So a bundled script does it, instead of inline bash. The script also sidesteps shell code that has to work on both POSIX shells and PowerShell:

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(readlink -f "<skill_dir>/SKILL.md")")")}"
python3 "$PLUGIN_ROOT/scripts/setup_workspace.py" --repo-path <repo_path> --source-branch <source_branch> --change-id <id>
```

Use `python` in place of `python3` when `python3` is not on `PATH`. Some native Windows installs carry only one of the two.

The first line resolves the shared helper at the plugin root, in either install mode.

`<repo_path>` is the relative shape that the host adapter states, such as the namespace for GitLab or `owner/repo` for GitHub. The script searches common project roots, and then searches by remote URL, because no single clone location is standard enough to assume.

On success it prints two lines. `MODE:` is `main-clone` or `worktree`, and Step 9 reads it to decide what to clean up. `WORKSPACE_PATH: <path>` is the workspace itself.

On a refusal it prints `STOP: <reason>` and exits non-zero. Stop and tell the user, instead of working around it. Four cases refuse. A leftover worktree is dirty or unpushed. The clone holds the source branch with uncommitted changes, which per-thread commits would capture. The clone holds commits that origin does not, which the push in Step 7 would carry. Another worktree holds the source branch, which means that another agent works on it.

When the script cannot locate the repo at all, ask the user for the local clone path, and re-run with `--repo-root <path>` in place of `--repo-path`.

Use the printed `WORKSPACE_PATH` for every read, every edit, and every commit from here on.

### Step 4: Classify each thread

For each open thread, read every comment in it, and put the thread in one of three classes:

- **Already fixed**: the code already does what the thread asks, probably through a later commit in the same change. Reply and explain where and how, then resolve the thread. No code change is needed.
- **Needs fix**: the ask is actionable and you agree with it. Implement it in Step 5.
- **Disagree**: the ask is arguably wrong, out of scope for this change, or based on a misunderstanding. Reply and explain your reasoning, and leave the thread open, as Step 8 describes. Closing a thread that a reviewer raised is the reviewer's call, and you cannot make that decision on their behalf.

### Step 5: Implement fixes

For each thread classified as **needs fix**, implement the fix with a test that fails before the fix. Land each thread as one atomic commit. Keep the fix for each thread isolated in its own commit. That isolation lets you cite a single commit SHA when you reply in Step 8. It also lets the reviewer verify the fix for one thread without reading through another.

### Step 6: Run the test suite

Run the full build, plus the unit and integration suites. Report the counts of passed, failed, and skipped tests. That result is what tells you that the fixes are safe to push, and it goes in the summary either way.

If anything fails, stop and fix it before you move on. Never push, and never resolve a thread, against a red suite.

### Step 7: Push the branch

```bash
git -C <worktree_path> push origin <source_branch>
```

Push only after Step 6 is green, and only ever to the source branch of the change. Push nowhere else. When git rejects the push, stop and tell the user what git reported. A rejection happens when the push is non-fast-forward, because someone else pushed to the branch meanwhile. Never force-push, because a force-push over someone else's branch can discard their work in silence.

### Step 8: Reply and resolve, per the host adapter

For each thread classified as **needs fix** or **already fixed**, reply with the short commit SHA and what changed. A SHA identifies the fix, and it does not explain the fix, so never let one stand alone. "Fixed in abc1234 by capping the batch size at 500" tells the reviewer whether to keep reading, and "Fixed in abc1234" does not. Both hosts turn a bare SHA into a link to the commit, as the markup section of the host adapter describes, so write no URL of your own. For an already-fixed thread, say where the existing code already covers the ask. Then resolve the thread. The host adapter states the exact reply and resolve calls. Always post a true threaded reply, tied to the ID of the thread. Never post a new standalone or general comment.

For each thread classified as **disagree**, reply with your reasoning, and leave the thread unresolved.

A human reviewer reads every reply. Write short sentences in the active voice, define a term that the reviewer can miss at its first use, and cut filler. That matters most on a disagreement, where the reply carries the reasoning on its own. Never paraphrase a commit SHA, a file path, or a symbol name. When a plain-English writing skill such as `simple-english` is available, invoke it and apply its rules to the replies.

### Step 9: Remove the worktree

Remove nothing when Step 3 printed `MODE: main-clone`. The workspace is the user's own clone, and the branch was checked out there before this run started.

When Step 3 printed `MODE: worktree`, remove that worktree now, even when an earlier step failed partway through. When Step 3 stopped before it printed a path, this run created no worktree, so remove nothing here:

```bash
git -C <repo_path> worktree remove <worktree_path>
```

`<worktree_path>` is the `WORKSPACE_PATH` that Step 3 printed, and `<repo_path>` is the clone it came from.

If git refuses the removal, leave the worktree in place, and tell the user exactly what git reported.

### Step 10: Output the summary

Summarize directly in the conversation, and post nothing to the change. Give the title and link of the change, plus the test results from Step 6. List the threads that you fixed and resolved, with the commit SHA of each. List the threads that were already fixed and resolved, with where and how. List the threads that you left open, with your reasoning. Give the number of commits pushed to the source branch. Skip a category that holds nothing, instead of noting its absence.

## Hard constraints

The steps above carry their own reasoning. These three repeat because each one destroys work that is not yours to destroy.

- **Never** force-push. When git rejects the push in Step 7, stop and ask the user how to proceed.
- **Never** resolve a thread classified as disagree. Reply, then leave it for the reviewer to close.
- **Never** switch the branch of the user's clone. Work only in the workspace that Step 3 printed, which is either that clone on the branch it already held, or a separate worktree.
