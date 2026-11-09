---
name: android-uplift-deps
description: "Toolchain/dependency uplift playbook for Android apps: one axis per commit, release-note research, dependency diffs, review."
---

Read the project AGENTS.md and applicable global guidance first. Fall back to CLAUDE.md if AGENTS.md is absent. Follow the global rules for optional tools, specialist agents and Git actions.

# Dependency uplift: the user request

Repo facts (modules, compile/assemble commands, catalog vs Groovy scripts, deliberate opt-outs) come from the project's
`AGENTS.md` and its `gradle-deps` rule if present. Write the step 4 plan before editing dependency versions. Existing authorization to perform the uplift is sufficient.

Skills named below are optional companions. When one is missing, follow `references/companions.md` in the `android-standards` skill and continue.

1. **Baseline.** Clean `git status` on `feat/<ticket>-<slug>` (or the project's documented branch convention). Run the project's compile checks and
   `./gradlew :app:dependencies --configuration <debugVariant>RuntimeClasspath > <scratchpad>/deps-before.txt`. Quote results.
2. **Inventory.** List the in-scope entries with current versions (version catalog, or `build.gradle` files in Groovy repos).
   Note any `gradle.properties` opt-outs and convention plugins the uplift touches.
3. **Research.** Send one `android-researcher` per axis from step 4, in parallel, each asking for its inventory table. Ask for the latest stable of each item, its release notes, and compatibility
   (AGP↔Gradle↔JDK, Kotlin↔KSP↔Compose compiler). For AGP majors also load `agp-9-upgrade`.
4. **Plan.** One commit per axis, ordered Gradle → AGP → Kotlin/KSP → Compose BOM/AndroidX → third-party. Name the variants
   you will build and the tests you will run. Proceed within the user-authorized scope. Ask only about unresolved scope or consequential choices.
5. **Apply each axis.** Edit versions only where the project declares them. Rebuild all compile checks. For
   AGP/Kotlin/Gradle also run one release assemble (R8 path) and one debug assemble. Run the unit tests that passed at baseline.
   Diff `deps-after.txt` against `deps-before.txt` and list transitive changes.
6. **Runtime check** when native or vendored code is involved: `$android-run-app` on the 16 KB AVD, then the
   `android-verifier` agent runs the baseline tests and a smoke journey and returns the evidence.
7. **Review.** `android-reviewer`. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the compile check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open.
8. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
9. **Report** table: item, old, new, build result, test result, notable transitive changes, follow-ups.
