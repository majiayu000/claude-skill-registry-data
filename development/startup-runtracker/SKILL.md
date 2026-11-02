---
name: startup-runtracker
description: Set up, resume and wrap up work on the Run Tracker project on whichever PC I'm on (Windows or Linux). Use when I say "set up this PC", "get me started", "where was I", "what's next", "pick up work", "wrap up" or "I'm switching PCs" in the run-tracker repo.
---

# Run Tracker: setup, pick up, wrap up

Solo project, several PCs (Windows 11 and a Linux home PC, Docker Desktop on all of them). `CLAUDE.md` (already loaded) has the commands and workflow rules; `context.md` has the background and decisions, so read it when the task needs the why. Issues live on GitHub (`gh issue list`), not in a file.

## Set up this PC
1. `git status` and `git branch --show-current`. If this is a fresh clone, `git fetch --all`.
2. Run `npm run doctor` (needs `npm install` first if `node_modules` is missing; do that, it is safe).
3. For every ✗ the doctor prints, fix what you can without asking (`npm install`); `gh auth login` needs me, so tell me the command. For things only I can do, give me the OS-specific step from the doctor's hint and wait:
   - installing Android Studio, enabling USB debugging on the phone, plugging it in, a Linux udev rule
   - Docker is only needed from Phase 4; don't push me to fix it earlier.
4. Android items are only needed to run on the phone. Web work (`npm run dev`) needs only the "Required" group.
5. Finish by running the checks: `npm run type-check`, `npm run lint`, `npm run test:unit`. Report what passed. Say plainly if the phone run was not verified.

Never install system software or change global config on my behalf without asking.

## Pick up work
Show me, briefly:
- current branch and whether it is ahead/behind its remote
- uncommitted changes
- open PRs (`gh pr list`) and which are stacked on which (check each PR's base branch). Merge order matters for stacked PRs.
- issues with the `decision` label that are still open
- the next open issue in the lowest open milestone, skipping ones blocked by an undecided `decision` issue

Then ask which issue to take. Don't start coding until I pick one.

## Starting an issue
- Branch from the right base: `main`, or the PR branch it depends on if it needs that code (then open the PR against that branch and say it is stacked).
- Name: `feat/<n>-slug`, `task/<n>-slug`, `docs/slug`.
- Open a PR with `Closes #<n>`, using `.github/pull_request_template.md`. Leave PRs open for me to merge unless I say otherwise.
- Local checks before the PR: type-check, lint, unit tests. No CI exists on purpose.

## Wrap up / switching PCs
1. Everything committed and pushed? Show `git status` and unpushed commits; commit and push only if I ask.
2. List open PRs and what each is waiting for.
3. Note anything unverified (especially "not tried on the phone") in the PR description or the issue, so it is visible from the other PC.
4. If a decision was made in conversation, update `context.md` (Decisions / Pending decisions) on a `docs/` branch.

## Gotchas
- Git Bash on Windows rewrites `branch:path` arguments; use `MSYS_NO_PATHCONV=1` for `git show branch:file`.
- `.vscode/`, `android/`, `dist/` and `node_modules/` show up as untracked when on a branch that predates the scaffold; they are ignored once the scaffold is merged.
- Background GPS and keep-awake can only be verified on the real phone, never in the browser.
