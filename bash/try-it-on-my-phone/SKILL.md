---
name: try-it-on-my-phone
description: Verify a release by hand on real devices with a written checklist, one device at a time, and turn every failure into a fixed bug or a logged item. Use when the user says "hand test", "verify the release", "manual verification", "test it on my phone", or /try-it-on-my-phone.
---

# Hand test

Load `run-on-any-device`, `bug-trap` and `release-day` first, or ask your agent to follow them. Then do this in this session (see `be-my-cto`):

1. **Plan.** Read the release diff in every repo. Write one checklist in the project's docs folder (for example `docs/release-checklist.md`). Each row says: do this, then you should see this.
2. **Order.** Start with an old install that holds real-looking test data, then upgrade it, then run the checks. Do a fresh install last. If one device pairs with or depends on another (a phone that syncs with a desktop app), test the one the others depend on last.
3. **One device at a time,** each to a stable result. Pick one device to go first and keep that order. Check shared code once, on the fastest device.
4. **Report each check** as pass, fail with what you saw, or not run and why. Read the code behind every claim.
5. **A failure is a bug.** If it must be fixed before release, fix it on the release branch with a test. Otherwise log it as "after release" in the project's backlog or issue tracker.

## Screenshots in the PR

When a check passes on a device, add its screenshot to the PR as you go. Look at each shot before you upload it. The helper script does this through the GitHub CLI without pushing local code:

```
python3 scripts/pr_shots.py <repo-dir> <owner/repo> <pr-number> <file>... [--branch <branch>] [--dir <folder>]
```

- `--branch` defaults to the PR's head branch.
- `--dir` defaults to `docs/pr-screenshots/<branch>`.
- It needs `gh` signed in with write access to the repo. Without `gh`, commit the shots to that folder and add them to the PR body by hand.

## Deeper reference

`test-like-a-user/reference/test-doctrine.md` holds the full method for writing and fixing tests that prove what the user sees. Read it for any hard case.
