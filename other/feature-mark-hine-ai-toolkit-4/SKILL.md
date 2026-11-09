---
name: feature
description: "Feature or feature-change playbook for Android apps: intake, pattern discovery, plan, implement, tests, emulator check, review, commit."
argument-hint: "[ticket] [one-line summary]  (say 'modify' if changing an existing feature)"
---

# Feature work: $ARGUMENTS

Repo facts (modules, build/test commands, design-system names, app id) come from the project's `CLAUDE.md`. Never guess them.

Skills named below are optional companions. When one is missing, follow `references/companions.md` in `android-kit:standards` and continue.

1. **Intake.** If an Atlassian MCP tool is available, fetch the Jira ticket and quote its acceptance criteria. Otherwise
   restate the goal in three bullets plus an out-of-scope list. Branch `feat/<ticket>-<slug>` (or the project's documented branch convention) off the default branch.
2. **Discover the pattern.** Use an Explore subagent to find the closest existing screen or flow: its Activity/Fragment or
   Compose entry point, ViewModel, repository/use case, DI wiring, and tests. Note whether it is XML or Compose.
   For a *modify* task also map every caller of the code you will change.
   If it changes UI, capture the touched screens now, the same way as step 7, and label them `before`.
3. **Consult skills and references.** Route through `using-chrisbanes-skills` and load the compose-*/kotlin-* skills it names.
   Ask `android-researcher` only where guidance may have moved (navigation, insets, permissions, target-SDK behaviour).
4. **Plan (plan mode).** Files to add or change, state model (`UiState` sealed interface, StateFlow), where data code goes,
   DI wiring, test list, device checks. For UI changes, consult `/design-kit:standards` (tiered design rules, screen states, accessibility). Follow the project's architecture rules. Get approval.
5. **Implement** in small steps, running the project's compile check after each. New UI is Compose, Material3, following the design rules (AND-1 colour roles, AND-2 insets, A11Y-3 targets), inside the project's theme and components, split into stateless `XContent` and stateful `XScreen`. No orientation locks.
6. **Tests.** Follow the change-to-test mapping in the Android testing rule (`~/.claude/rules/android/testing.md`, or `references/testing.md` in `android-kit:standards` when the rule is not installed). ViewModel, use-case and repository changes get unit tests with fakes for owned code and MockK only at true boundaries. A new or changed screen gets a Compose UI test where the module has the infra, otherwise a preview per `UiState`, plus the journey in step 7. Run them with `--tests` and quote the summary.
7. **Device verification.** `/android-kit:run-app` on the default phone AVD, and on the tablet AVD for any new or changed screen.
   Then hand off to the `android-verifier` agent with the test command, the journey file(s) for the touched screen,
   each device serial and the application id. For a new or changed screen, also ask for a configuration capture of
   that screen on the phone (default, dark, font scale 2.0) and on the tablet, which A11Y-7 and AND-1 need. It returns
   the JSON journey result and labelled screenshot paths, so the images stay out of this session. Check insets
   (`edge-to-edge`) and large-screen layout (`adaptive`) against its findings. A FAILED action is a finding, not
   something to fix inside this step. A new screen gets a new journey.
8. **Review.** `android-reviewer` against the acceptance criteria, and delegate UI/layout changes to `ui-reviewer` with the labelled step 7 screenshot paths. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the compile check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open. List declined Nits.
9. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
10. **Report**: files changed, commands run with results, screenshot paths, what is left for QA.
