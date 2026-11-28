---
name: git-hygiene
description: Version-control discipline — stage by explicit path, one logical change per commit with a why-message, branch before risky work, secrets never in history, no rewriting commits you don't own. Use when committing, staging, branching, amending, rebasing, stashing, force-pushing, writing commit messages, or starting any change large enough to want an undo point. Not for deciding what code to change.
---

# git-hygiene

Weak git use looks like: `git add -A && git commit -m "updates"` on main, with a debug script and a `.env` riding along. Strong git use makes every commit a deliberate, reversible, explainable unit. Git is the safety net and the paper trail; each step below protects one or the other.

## Before the work

1. **Check where you stand:** `git status` and `git branch --show-current`. Pre-existing uncommitted changes and stashes are the user's — not yours to stage, revert, or drop (see data-loss-guard).
2. **Branch before risky or user-visible work**, and never commit to main/master unprompted, even for "one small fix": `git switch -c <type>/<short-slug>` in the repo's naming style. A branch costs nothing; un-committing from main costs a conversation.
3. **Read history before "fixing" odd code:** `git log -S <symbol> --oneline` and `git blame -L <start>,<end> <file>` on the lines you're about to change. If a past commit did it deliberately, its message says why — respect it, or cite it when overriding.

## Staging

4. **Stage by explicit path, never by wildcard.** `git add <file> ...` or `git add -p`; never `git add -A` or `git add .`. First list every untracked path in `git status` and decide each: intended artifact (stage), ignorable (add to `.gitignore` if the repo would want that), or debris you created (delete). Anything untracked you didn't create gets asked about, not committed.
5. **Scan the staged diff for secrets before committing:** `git diff --cached | grep -inE 'api[_-]?key|secret|token|passw|PRIVATE KEY|AKIA[0-9A-Z]{16}'`. A hit means unstage and remove. A secret in an already-pushed commit is compromised even after amend or rebase — tell the user to rotate it; never present history rewriting as the fix.
6. **Read the staged diff top to bottom** (`git diff --cached`) — the last cheap moment to catch debug prints, commented-out experiments, and unrelated hunks (see workmanship). Unrelated hunks go in a separate commit or stay unstaged.

## Committing

7. **Commit only when asked**, then one logical change per commit. Run `git log --oneline -20` first and match the house style (prefix, tense, length). The subject states what and why for the person running `git log` during an incident: "fix utf8 filename crash in import", not "fix bug". Reasoning and behavior changes go in the body.
8. **Don't rewrite history you don't own.** Before `commit --amend`, `rebase`, `reset`, or any force-push, run `git log origin/<branch>..HEAD --format='%h %an %s'`: every commit you'd touch must be unpushed AND authored this session. Otherwise stop and ask. If a force-push is explicitly requested, use `--force-with-lease`, never `--force`.
9. **Never push, tag, or open a PR unprompted.** When asked, name the exact remote and branch in the report.

## Exit check

Report the branch, each commit hash and subject, and exactly what remains uncommitted or untracked and why. `git status` after your report should hold no surprises for the next person.
