---
name: merge-train
description: Build a Kaeri merge train - one branch from main merging several ready branches, checked locally, opened as one PR, reviewed by the maintainer on local builds, then auto-merged. Use when bundling ready branches for a single CI run and beta.
---

# Merge train

CI is expensive and every merge to main publishes a beta, so ready branches ship together in one
train.
The maintainer inspects every train before it merges, so keep trains few and complete.

1. **Base.** In your own worktree: `git fetch origin && git switch -c train/<date>[-n] origin/main`.
   If an earlier train PR is still open, wait for it to merge first.
2. **Merge** each ready branch in dependency order with `git merge --no-ff -S origin/<branch>`
   (message: `Merge <branch> into train/<date>` plus the Co-Authored-By trailer). Resolve
   conflicts keeping both sides' intent. Things to recheck after merging:
   - migration numbers in `crates/kaeri-store/src/schema.rs` don't collide;
   - new FFI record fields carry `uniffi(default)`;
   - `deploy/sync.sh --check` if store crates or their dependencies moved;
   - Android scenes re-recorded (`android/scripts/scenes.sh`) if engine records changed;
   - Cargo.lock: take one side, then `cargo check --locked`.
3. **Check** with the `local-checks` skill, everything the train touches, including both R8
   builds and the Mac Release signed with `signing-keychain.sh sign` when Apple or packaging
   changed. Fix what breaks with small signed train commits that say what they fix. Code that
   only breaks in combination is the usual find.
4. **Version.** After the merges, choose the bump. While the major is 0:
   - minor if the train breaks something: a plugin API change that needs plugins rebuilt, config
     or data the previous version can't read, a store protocol break, or a dropped OS version;
   - patch for everything else, new features included;
   - major (1.0) only when the maintainer asks for it.

   Set `[workspace.package] version` in `Cargo.toml` above the newest `v*` tag (with no tags yet,
   the version as it stands is the first release), run `cargo check --locked` so `Cargo.lock`
   matches (fix it with `cargo update -w` if not), and commit `Release X.Y.Z` on the train. No
   bot pushes to main, so this commit is the only place the version changes. A PR check fails a
   release that isn't newer than the newest tag.
5. **PR.** Push the branch and open ONE PR against main. The PR title is the line stable users
   read in the weekly list, so it says what changed for them. The first paragraphs are the
   beta's release notes, so keep them short and plain. Put internal detail (the version, the
   branches, conflicts and resolutions, train fixes, what was checked and what wasn't) under a
   `## Train` heading, which the stable notes drop. End
   with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
6. **Review builds.** Don't turn on auto-merge yet. Into `train-<n>/` in the review-builds folder
   the maintainer's own instructions name (outside the repository), put:
   - the Mac Release app from step 3, signed with Kaeri's certificate by `signing-keychain.sh sign`;
   - the Android app-flavour release APK from the R8 build, with a version code above the latest
     release, so it installs over the store build;
   - `README.md`: a few lines on what changed, before and after shots of every changed screen (from
     the branches' shot folders, or app-shots), what to try on the Mac and Android, and what wasn't
     checked.

   Build them even when a platform's code didn't change, because the engine reaches both. Never launch
   `app.kaeri.app` yourself; the maintainer runs these builds. Report the folder and the PR,
   then stop.
7. **Merge after the maintainer's go.** Only when the maintainer approves the train in the
   conversation, confirm protection first:
   `gh api repos/bitknox/kaeri/branches/main/protection/required_status_checks -q .contexts`
   must list `CI passed`. Then `gh pr merge <n> --auto --merge -R bitknox/kaeri`. Never merge
   without `--auto`; without protection it merges at once. If they find problems, fix them on the
   train with signed commits and rebuild step 6.
8. **After merge,** confirm the beta published: the Release run on the merge commit succeeded and
   the pre-release has all its files (see `ci-triage`). Stable comes from the weekly Promote
   workflow; never dispatch it unless the maintainer says to in so many words.
