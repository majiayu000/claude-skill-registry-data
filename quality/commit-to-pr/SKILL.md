---
name: commit-to-pr
description: Use when the user invokes /workbench:commit-to-pr or asks to commit changes and open or update a pull request, including "ship this" or "make a PR for these changes". Not for reviewing code or deciding whether unfinished work should ship.
---

# Commit to PR

Turn uncommitted work (or unpushed commits) into a pull request: survey → branch → stage → commit → push → PR. Requires git, plus an authenticated `gh` for the push and PR.

**This is packaging, not verification.** Don't run tests, builds, linters, or reviews — CI and reviewers own those, and a PR step that runs them is slow and duplicates their work. The one exception is pre-commit hooks, which run on their own. Because nothing here verifies the change, the PR body makes no claims about tests, coverage, or quality; if the user asks you to write "all tests pass", say this step didn't check that and leave it out. When a calling skill (such as `workbench:enhance`) hands you a PR body or verification it actually ran, use that as given — the rule is about not inventing claims, not about stripping evidence someone else produced.

Arguments: `[commit-message]` (use verbatim as the subject), `[base-branch]` (default: the repo's real default branch), `--draft`.

## 1. Survey

```bash
git status --porcelain=v1 --branch
git diff --stat; git diff --staged --stat
git log --no-merges -20 --format='%s'
git log -1 --format='%b'
git remote -v
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

Twenty subjects, because conventions vary and a short sample misleads; the last body shows whether the repo uses trailers.

- Nothing modified and nothing ahead of upstream → stop, nothing to ship.
- Nothing modified but commits ahead → skip to push.
- Detached HEAD → stop and ask where the work should live.
- No remote → commit locally, then stop and say there's nowhere to push.

## 2. Branch

- **On the default branch:** create a branch before staging, so nothing lands on it by accident.
- **On an auto-generated name** (`adoring-leakey-5e0704` style) with no upstream: rename it (`git branch -m`). If it has an upstream, keep it — renaming orphans the remote branch and any PR.
- **On a meaningful name:** keep it.

Follow the repo's evident naming (e.g. `feat/…`, `fix/…`); otherwise `change/<slug>`, where the slug names the change in 2–5 kebab words. Leave `claude/` and `codex/` prefixes alone.

## 3. Stage deliberately

Read the actual diff, not just `--stat` — you need it for the message, and it's how you notice changes that belong to other work.

- Stage tracked changes that belong to this unit of work, path by path when not all of them do. Name untracked files explicitly; never bulk-add (`git add .` / `-A`).
- Leave unrelated edits unstaged and mention them in the report. If it's genuinely unclear whether something belongs, ask.
- **Don't stage** credential-shaped files (`.env*`, `*.pem`, `*.key`, `id_rsa*`, `credentials.json`, `.npmrc`, `.netrc`), secret-shaped content (`PRIVATE KEY`, `sk-ant-`, `ghp_`, `github_pat_`, `AKIA…`), build output (`dist/`, `build/`, `node_modules/`, `target/`, `.venv/`), or files over ~1 MB. For a secret, check `git log --all --diff-filter=A -- <path>`: empty means it never left the machine and needs no rotation — say so; otherwise name the commits and stop (rewriting history is the user's call). If `.gitignore` doesn't cover what you caught, add the rule in its own commit ahead of the work commit, so it's easy to drop.

## 4. Commit in the repo's voice

Match the history: conventional `type(scope): …` if that's what recent subjects use, plain imperative prose if that is. Imperative, under ~72 characters, saying what changed rather than which files moved. Add a body only when a reviewer would otherwise ask why. Mirror the repo's trailers — if recent commits carry `Co-Authored-By: Claude …`, include one with this session's model; if the repo never uses trailers, don't add one. Split only genuinely separable work.

If a pre-commit hook rejects the commit, read why and fix it. If it rewrote files, check the rewrite and re-stage only the intended paths before committing again. Never `--no-verify` unless the user asks.

## 5. Push

`git push -u origin <branch>`. If it's rejected as non-fast-forward or blocked by push protection, stop and report. Never force-push unless asked.

## 6. Open or update the PR

Check for an existing one first: `gh pr view --json url,title,body`. If one exists, you've just pushed to it — reread its title and body against what the branch now contains and fix whichever went stale with `gh pr edit`.

Otherwise `gh pr create` against the base, with `--draft` if asked and no `--label` (it fails on labels the repo doesn't define). Title: the commit subject, or a summary line for several commits. Pass the body with `--body-file` from a quoted heredoc (`<<'EOF'`) — an inline `--body` mangles backticks. If the repo's merged PRs have a house shape (`gh pr list --state merged --limit 5 --json body`), match it; otherwise:

```markdown
## What

[What changed and why, 2–6 lines, for someone who hasn't seen the diff.]

## Notes

[Only if a reviewer would otherwise miss something: a decision and the rejected
alternative, something left out on purpose. Drop the section if empty.]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 7. Report

A few lines: branch (and any rename), commit subject(s), anything left unstaged and why, the PR URL. If you stopped early, say where and what's needed to continue — committed-but-unpushed work is safe, and the user should know that.
