---
name: bugfix
description: "Bug-fix playbook for Android apps: reproduce (test or emulator), root cause, minimal fix, regression test, review, commit."
argument-hint: "[ticket] [symptom]"
---

# Bug fix: $ARGUMENTS

Repo facts (modules, build/test commands, app id) come from the project's `CLAUDE.md`.

1. **Restate** the symptom, expected behaviour, and affected variant or device if known. Branch `fix/<ticket>-<slug>`.
2. **Locate.** An Explore subagent returns the path from symptom to code (screen → ViewModel → use case/repository → API) as `file:line` entries.
   Then read that whole path yourself, not the first suspicious line, because the subagent reads excerpts. `git log -S` for the change that introduced it.
3. **Reproduce.** Prefer a failing unit test in the module that owns the defect. For UI or platform bugs reproduce on the
   emulator with `/android-kit:run-app` (min-SDK AVD for min-SDK issues) and capture `android screen` and `adb logcat` excerpts.
   Quote the failing output. If the bug does not reproduce, stop and report what you
   tried and the evidence still needed. Do not ship a speculative fix.
4. **Root cause.** One paragraph: what is wrong and why it produces the symptom. If a fix would only mask it (catch-all,
   null guard), say so and propose the real fix. Ask `android-researcher` when a platform behaviour change is suspected.
5. **Fix** with the minimal diff. Note refactor candidates as follow-ups instead of doing them. If the test stays red, go back to step 4 rather
   than stacking changes. After three failed fixes, stop and report what each attempt showed.
6. **Verify.** Failing test now green plus the class's other tests, and the project's compile check. For UI bugs re-run on the
   emulator with a screenshot, and hand the screen's journey (if one exists) to the `android-verifier` agent and quote
   its results. A unit-only rerun stays in this session, because the reviewer checks the tests again.
7. **Review.** `android-reviewer` with the symptom and root cause as the task statement. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the compile check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open.
8. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
9. **Report**: cause, fix, evidence (test before/after, screenshots), regression risk, pre-existing issues noticed.
