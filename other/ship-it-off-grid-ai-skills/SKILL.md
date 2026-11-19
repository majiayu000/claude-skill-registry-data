---
name: ship-it
description: Take a change all the way to release-ready, with code, design, tests, device checks and the release PR done together in one pass. Use when the user says "get it live", "ship it", "take this to release", "finish this and open the PR", or /ship-it.
---

# Get it live

You do the work, in this session, start to finish. All code and change work stays here. Helper agents or sub-threads only run hand tests on devices (see `be-my-cto`).

Load these skills first, or ask your agent to follow them: `no-fluff`, `dont-break-it`, `make-it-look-expensive`, `bug-trap`, `run-on-any-device`, `release-day`.

1. **State.** Read the release handoff note if there is one, `git log` and CI for every repo on the branch, and the open PRs. List what is left. Do not redo done work.
2. **Order the work.** Make one list and work it top to bottom. A shared package or component library goes first, and is pushed before the repos that use it. Keep the user's exact words and the quality bar (`make-it-look-expensive`, rule 1) in front of you. Done means pushed, captioned in the PR, and reported.
3. **Review as you go.** Look at every screen and flow against `make-it-look-expensive`. Read every new or changed test against `bug-trap`: what it fakes and how it seeds data. Fix a gap before you move on. Never ship it.
4. **CI green** in every repo. If the project has a guard against mocking its own code, keep it on. Fix a red test at its cause. Accept a fix only after a live check on real data.
5. **While CI runs, run one review loop.** Never sit idle waiting on CI. Run one turn of `fix-it-everywhere` on the project's screen review page: read open notes, judge every changed screen on each target platform (for a mobile app, iPhone and Android), fix what falls inside rules the user already approved, and pin the rest as notes for the user. A fix restarts CI. That is fine.
6. **Review page in the PR.** Before you report, the screen review page from `show-me` has fresh shots of every changed screen on every target platform, published to the same place as before. Commit and push the shots and the review folder (for example `docs/review/`) on the branch. The PR body has a **Screen review** line with the link to the page. If your agent cannot publish a hosted page, commit a local HTML page and link its path in the repo. The user reviews from that page.
7. **Report.** When the list is done, the review page is in the PR and CI is green, send the user one short summary with the PR links. If the project has a release tracker or dashboard, update it. Tell the user only what landed, or what needs their hands or a decision.
8. **No merge and no release build** until the user says yes.

## If the project lacks a piece

- No CI: run the project's full test, lint and type checks locally and say so in the report.
- No screen review page yet: run `show-me` once to make it.
- No device access: say which checks were not run on a device and why. Never claim them.
