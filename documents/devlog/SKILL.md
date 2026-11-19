---
name: devlog
description: Commit, push, document and show game work so the user sees every new screen and nothing private or unlicensed goes public. Use when committing a batch, pushing, opening a PR, preparing a release, or when the user says "show me what you did", "push it", "report progress" or "devlog".
---

# Show your game work

1. **The repo.** Find the remote and the main branch (`git remote -v`, `git branch`). Push after a change is seen working. Small commits, one subsystem each.
2. **Pushes.** Clean tree, one at a time, in the background. Never force-push the main branch.
3. **Before any release** (a tag, a store build, an itch.io or GitHub release): refresh the review page with every changed screen and scene, run one `fix-it-everywhere` turn on it, and fix what it finds or name it. Check the exported build, not the editor run.
4. **Big or risky work** (a save format change, a new system) goes on a branch with a PR: what changed, why, and before and after screenshots under bold one-line captions.
5. **Show the user.** Screenshots of every new screen and scene, sent as they land, each with a one-line caption. Name anything not yet seen working.
6. **Keep the docs true.** README for setup and how the parts fit together. A design doc for decisions and the roadmap. Record a reversed decision with its date.
7. **Licences.** Credits stay with each asset (a licence file beside it). Nothing third-party goes public without the user's yes.
8. **No public release and no visibility change** (making the repo public, publishing a store page) without the user's yes.
