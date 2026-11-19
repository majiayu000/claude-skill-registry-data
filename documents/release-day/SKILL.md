---
name: release-day
description: Keep release branches, pushes and PRs clean across one or many repos, with captioned screenshots, a screen review link, and no merge or release build without your yes. Use when working on a release/ branch, opening or updating a release PR, or when the user says "prep the release", "release branch rules" or "get the PRs ready to ship".
---

# Release

1. **One session, one branch name** across all the repos in the release. Work the repos in order: a shared package first, pushed before the repos that use it.
2. **Clean tree, one push at a time.** Keep the tree passing. Change one file at a time and commit it before you move on. Write long drafts outside the repo. If pre-push hooks test the whole tree, a half-done file blocks the push. Run pushes in the background and one at a time: overlapping hooks can overload the machine until tests time out.
3. **Screenshots in every PR that changes UI.** Light mode (or the app's default theme), taken from the running app, saved in `docs/pr-screenshots/<branch>/` in each app repo. Show before and after of each new screen and state.
4. **Caption every screen.** Each feature gets a `###` section, one short paragraph, then each screen under its own bold one-line caption. Readers and any release dashboard read these words. Name any screen you could not reach and say why.
5. **Screen review page in every PR.** Each release PR body has a **Screen review** line that links the project's review page (made by `show-me`; keep its link in the repo, for example `docs/review/ARTIFACT_URL`, or link the local HTML page). Before you ask for review or merge: refresh the page with every changed screen on each target platform, publish it to the same place, and commit the shots and the review folder on the branch. While CI runs, run one `fix-it-everywhere` turn on that page (see `ship-it` step 5).
6. **Upload as you go.** After each check passes, add its shots to the PR: `python3 <skills>/try-it-on-my-phone/scripts/pr_shots.py <repo-dir> <owner/repo> <pr> <file>…`, where `<skills>` is wherever this skill set is installed. Look at each shot first.
7. **Report to the release tracker** if the project has one, when it asks: the user's exact words, what you built, the proof, and the user's decisions.
8. **After merge, the release branch is frozen.** Fixes go on `release/<name>-fixes`, branched from main, in every repo that needs them.
9. **No merge and no release build** without the user's yes.
10. **Freeze main while a release build runs.** If the build or upload checks that its commit still matches main, merge nothing to main in the repos it builds from until the uploads finish.
