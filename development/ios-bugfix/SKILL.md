---
name: ios-bugfix
description: "Bug-fix playbook for iOS apps: reproduce (test or simulator), root cause, minimal fix, regression test, review, commit."
---

Read the project AGENTS.md and applicable global guidance first. Fall back to CLAUDE.md if AGENTS.md is absent. Follow the global rules for optional tools, specialist agents and Git actions.

# Bug fix: the user request

Repo facts (workspace, schemes, build/test commands, test framework, bundle id) come from the project's `AGENTS.md`.

1. **Restate** the symptom, expected behaviour, and affected scheme, OS version or device if known. Branch `fix/<ticket>-<slug>`.
2. **Locate.** An explorer subagent returns the path from symptom to code (view → view model → service/repository → API) as `file:line` entries.
   Then read that whole path yourself, not the first suspicious line, because the subagent reads excerpts. `git log -S` for the change that introduced it.
3. **Reproduce.** Prefer a failing unit test in the target that owns the defect. For UI or platform bugs reproduce on the
   simulator with `$ios-run-app` (an older runtime from `xcrun simctl list runtimes` for OS-specific issues) and capture a
   screenshot and the relevant `log show` excerpt. Quote the failing output. If the bug does not reproduce, stop and report what you
   tried and the evidence still needed. Do not ship a speculative fix.
4. **Root cause.** One paragraph: what is wrong and why it produces the symptom. If a fix would only mask it (optional
   chaining that hides a nil, `DispatchQueue.main.async` to paper over isolation, a `try?`), say so and propose the real fix.
   Ask `ios-researcher` when an OS behaviour change or deprecation is suspected.
5. **Fix** with the minimal diff. Note refactor candidates as follow-ups instead of doing them. If the test stays red, go back to step 4 rather
   than stacking changes. After three failed fixes, stop and report what each attempt showed.
6. **Verify.** Failing test now green plus the suite's other tests (`xcodebuild test … -only-testing:`), and the project's build
   command for every scheme it lists. Hand the test rerun and, for UI bugs, the simulator smoke check and the screen's
   journey (if one exists) to the `ios-verifier` agent and quote its results.
7. **Review.** `ios-reviewer` with the symptom and root cause as the task statement. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the compile check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open.
8. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
9. **Report**: cause, fix, evidence (test before/after, screenshots), regression risk, pre-existing issues noticed.
