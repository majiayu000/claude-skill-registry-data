---
name: ship
description: "Use when asked to commit, push, open or prepare a PR, resolve conflicts, set up a worktree, or finish a branch; not for explanatory questions."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "obra/superpowers 7.0.0 skills/finishing-a-development-branch, skills/using-git-worktrees; mattpocock/skills resolving-merge-conflicts; garrytan/gstack 1.60.1.0 ship/SKILL.md.tmpl (pre-flight, bisectable commits, verification gate, push), ship/sections/pr-body.md; cursor/plugins pstack 0.15.25 skills/principle-sequence-verifiable-units; MCT (local) ~/.claude/skills/git-pr-workflow, ~/.claude/commands/commit-ready.md, ~/.claude/commands/pr-ready.md, ~/.claude/MCT.md (TODO Commit Flow)"
---

# Ship

Do exactly the git action the user asked for. A commit, a push and a PR are three separate requests. "Prepare a PR" means drafting the title and body in chat, without pushing or creating anything.

An explanatory question such as "How would I deploy this?" requests guidance only. An action request phrased as a question, such as "Can you push these changes?", authorizes that named action. Preserve authorization already given in the conversation; do not infer extra publication actions from a skill being loaded.

## Safety rules

- NEVER force-push. A rejected push means the remote moved: fetch, look at what changed, integrate it and rerun the checks. Use `--force-with-lease` only when the user asks for a force push. A plain force-push silently deletes other people's commits.
- NEVER run `git add -A` or `git add .` without first reading `git status`. Blind staging sweeps in secrets, build output and the user's unrelated work.
- NEVER mention AI, assistants, Claude, Codex, MCT or honey-stack in a commit subject or PR title. Add a co-author trailer only when the harness or the user's config asks for one.
- Leave `--no-verify`, `reset --hard`, `branch -D`, `worktree remove --force` and `clean -f` alone unless the user asks for them by name.

## Commit

1. **Prove the tree.** Run the `verify` skill on exactly what will be committed. Done when: its receipt is fresh.
2. **Inspect.** Run `git status`, `git diff` and `git diff --staged`. Pick out changes that aren't part of this task and leave them unstaged. Done when: you know which paths belong to this change.
3. **Stage by path.** Run `git add <path>...`, then check `git diff --staged --stat`. Scan the staged diff for secrets, `.env` files, large binaries and debug leftovers. Done when: the staged diff is the change and nothing else.
4. **Write the message.** The subject is `<type>(<scope>): <imperative summary>` in 72 characters or fewer, using one of feat, fix, refactor, perf, test, docs, build, ci or chore, unless `git log` shows the repo uses another convention. Describe only what the diff contains. Add a body when the why isn't obvious. Commit one logical change at a time: split mixed work into commits that each build and pass on their own, keeping each test in the same commit as its code.
5. **Commit.** If a hook fails, no commit was made. Fix the cause, re-stage and commit again. `--amend` would rewrite the previous commit. Done when: `git log -1 --stat` shows the intended files and message.

## Push

Run `git push`, adding `-u origin <branch>` the first time. On the default branch, check that the user meant it before pushing. Done when: `git status -sb` shows the branch in sync with its upstream.

## PR

1. **Check for an existing PR** with `gh pr view --json url,state` (`glab mr view` on GitLab). If one is open, update its body instead of opening a second.
2. **Pick the base.** Use the branch's upstream, or the branch it forked from. If the base has moved, bring it in and rerun `verify` before opening.
3. **Write the title** like a commit subject. Write the body to a file. Follow `.github/pull_request_template.md` if the repo has one, otherwise use:

   ```
   ## Summary   what changed; every commit in `git log <base>..HEAD` is reflected
   ## Why       the problem or request behind it
   ## Verification   commands run and results, UI evidence (from the receipt)
   ## Risk      what could break, migrations or rollout notes, what wasn't checked
   ```

4. **Open it** with `gh pr create --base <base> --title "<title>" --body-file <file>`, and pass `--draft` if the user asked for a draft. Done when: `gh pr view` prints the URL, and you report it.

## Merge conflict

1. **Read the state.** Run `git status` to see which operation is in progress (merge, rebase or cherry-pick) and which files conflict. Use `git log --merge --oneline` to list the commits behind each side.
2. **Understand both intents.** Read the commit messages, PRs and issues behind each conflicting hunk before editing.
3. **Resolve each hunk** so it keeps both intents. Where they can't coexist, keep the side that matches the merge's goal and note the trade-off. Add no new behavior. Regenerate lockfiles and generated files with their tool rather than hand-merging them.
4. **Recheck.** Run `git diff --check`, search for conflict markers (`<<<<<<<`), then run the `verify` skill and fix whatever the merge broke.
5. **Finish.** Stage the resolved files and run `git merge --continue` or `git rebase --continue` until the operation completes. Use `--abort` only if the user asks. Done when: no markers remain, the checks pass and `git status` shows no operation in progress.

## Worktree

Check whether you are already in a worktree first: compare `git rev-parse --git-dir` with `git rev-parse --git-common-dir`. A submodule also shows a difference, and `git rev-parse --show-superproject-working-tree` prints a path there. Don't nest worktrees. Otherwise:

- Prefer the harness's native worktree tool, such as EnterWorktree on Claude Code or Codex's worktree mode.
- Without one, run `git check-ignore -q .worktrees`, and if the directory isn't ignored, add it to `.gitignore` and say so. Then run `git worktree add .worktrees/<branch> -b <branch>`.
- Install dependencies and run the baseline tests. Report baseline failures before starting work, so later failures aren't ambiguous.

Done when: the path, branch and baseline result are reported.

## Finish a branch

Run `verify` on the branch tip, and stop to report if it fails. Then give one decision brief, and act only on the answer. For the commands and cleanup rules, read `references/finish-branch.md`.

```
Branch <b>: <n> commits ahead of <base>. Checks: <result>.
1. Merge into <base> locally, rerun checks on the merged result, then delete the branch
2. Push and open a PR, and keep the worktree for review fixes
3. Keep as-is
4. Discard: deletes branch <b>, commits <list>, worktree <path>. Type "discard" to confirm.
Recommendation: <n>, because <reason>.
```

On a detached HEAD, drop option 1. Done when: the chosen option has run and its end state is reported.
