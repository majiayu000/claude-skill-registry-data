---
name: iru-code-one-task-group
description: >-
  Implement every task and sub-task in a single task group from an `implementation_plan.md`-style plan, dispatching each task by its declared language/framework key to the matching `<key>-code-one-task-group` skill (e.g. `iru-dotnet-code-one-task-group`, `iru-java-code-one-task-group`, `iru-java-springboot-code-one-task-group`, `iru-kotlin-springboot-code-one-task-group`, `iru-quarkus-code-one-task-group`, `iru-php-code-one-task-group`, `iru-typescript-code-one-task-group`, `iru-nestjs-code-one-task-group`, `iru-nextjs-code-one-task-group`, `iru-fastapi-code-one-task-group`, `iru-django-code-one-task-group`, `iru-android-code-one-task-group`, `iru-swift-code-one-task-group`, `iru-kmp-code-one-task-group`, `iru-react-native-code-one-task-group`, `iru-windows-code-one-task-group`, `iru-rust-code-one-task-group`, `iru-go-code-one-task-group`) — which itself captures one quality baseline for the group, implements the group's tasks (in parallel agents when the group is marked parallelizable), and validates the whole group once — falling back to implementing a task directly, best-effort, when its key has no matching `<key>-code-one-task-group` skill installed. Checks off each task/sub-task's box in `implementation_plan.md` and notifies the user as it happens, not just once the group finishes. Does not track a session task list or capture project-wide baselines — that bookkeeping belongs to the caller (`iru-code`). Invoke as `/iru-code-one-task-group <group text>`, passing the group's full text from the plan: every task/sub-task in the group, each one's language/framework tag if set, the group's `Parallelizable` verdict, and any relevant "Current code state" context. Used by the `iru-code` skill, which invokes this once per plan group, in order.
model: sonnet
allowed-tools: Read Edit Write Bash(mvn *) Bash(./mvnw *) Bash(./gradlew *) Bash(gradle *) Bash(dotnet *) Bash(npm *) Bash(npx *) Bash(composer *) Bash(php *) Bash(vendor/bin/*) Bash(uv run *) Bash(poetry run *) Bash(python *) Bash(python3 *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Skill Agent
---

# Implement one task group

Carry out every task in a single plan group end to end against the real codebase: resolve each task's
language/framework, dispatch to the right execution skill (or implement it directly when none matches), keep
`implementation_plan.md` current as each task/sub-task lands, and report the group's outcome — with as little
back-and-forth with the user as possible. This is the execution unit the `iru-code` skill calls once per group; it
carries the dispatch and progress-tracking logic that used to live in `iru-code`'s own Step 4/Step 5, now scoped to
one group at a time so validation happens once per group instead of once per task. It uses a medium model on
purpose — the plan already did the hard reasoning (task breakdown, grouping, language resolution); this skill's
job is to execute it.

## Step 1 — Resolve each task's language/framework key

For every top-level task in the group (sub-tasks inherit their parent task's key unless the plan tags one of them
differently):

1. If the task's own line carries an explicit language/framework tag (e.g. `_(dotnet)_`), use that key.
2. Otherwise, if the caller passed a plan-wide **Language/framework** key that applies to the whole plan, use
   that key.
3. Otherwise, the task's language/framework is unknown or unsupported — it has no key.

Find which `*-code-one-task-group` skills are actually installed in this repository:
`find .claude/skills -maxdepth 1 -type d -name "*-code-one-task-group"`. The directory name minus its `iru-`
prefix and its `-code-one-task-group` suffix is the key (e.g. `iru-java-code-one-task-group` → `java`,
`iru-typescript-code-one-task-group` → `typescript`, `iru-android-code-one-task-group` → `android`,
`iru-swift-code-one-task-group` → `swift`, `iru-java-springboot-code-one-task-group` → `java-springboot`,
`iru-kotlin-springboot-code-one-task-group` → `kotlin-springboot`, `iru-quarkus-code-one-task-group` → `quarkus`,
`iru-php-code-one-task-group` → `php`, `iru-nestjs-code-one-task-group` → `nestjs`,
`iru-nextjs-code-one-task-group` → `nextjs`, `iru-fastapi-code-one-task-group` → `fastapi`,
`iru-django-code-one-task-group` → `django`, `iru-kmp-code-one-task-group` → `kmp`,
`iru-react-native-code-one-task-group` → `react-native`, `iru-windows-code-one-task-group` → `windows`,
`iru-rust-code-one-task-group` → `rust`, `iru-go-code-one-task-group` → `go`) — the
`iru-` prefix is only this catalog's marketplace-collision namespace, not part of the language/framework key
itself.

Partition the group's tasks into buckets: one bucket per resolved key that has a matching
`<key>-code-one-task-group` skill installed, and a final bucket for everything else (no key resolved, or a key
with no matching skill installed).

## Step 2 — Dispatch each keyed bucket to its language-specific group skill

For each bucket with a matching `<key>-code-one-task-group` skill, invoke it once for the whole bucket (not once
per task) via the `Skill` tool: `Skill({skill: "iru-<key>-code-one-task-group", args: "<every task/sub-task in this
bucket, each with its own text and sub-tasks, plus the group's overall Parallelizable verdict and any relevant
Current code state context>"})`. That skill is responsible for: capturing one pre-change quality baseline for the
whole bucket, implementing each of its tasks (in parallel agents when the group is marked `Parallelizable: yes`),
running license/doc/test/coverage/quality validation once for the whole bucket, checking off each task/sub-task's
box in `implementation_plan.md` as it completes, and notifying the user of that progress live. Wait for it to
report back before moving to the next bucket (buckets for different keys can be dispatched one after another;
there's no need to serialize within a single-key bucket beyond what that skill already does internally).

If a `<key>-code-one-task-group` skill reports that one of its tasks stopped on a blocker, record that against
this group's outcome (Step 4) — do not attempt to work around it or move on to other buckets' remaining
unblocked tasks silently; surface it as part of this skill's own report so the caller (`iru-code`) can decide whether
to stop the whole run.

## Step 3 — Implement the remaining bucket directly, best effort

For tasks with no resolved key, or a key with no matching `<key>-code-one-task-group` skill installed, there is no
specialized skill to delegate to — implement each one yourself, one at a time (or, if the group is marked
`Parallelizable: yes` and none of these tasks touch the same file(s), you may implement them concurrently using
your own judgment), following the same obligations a one-task skill would:

- Implement exactly what the task specifies (the named file(s), the described behavior), using this repository's
  own conventions from `CLAUDE.md`. Don't add anything the task didn't ask for.
- Write or update tests covering the new/changed behavior, following the existing test style/framework for that
  language.
- Add license headers to touched files if this repository has a convention for them — delegate to the
  `iru-gate-runner` agent rather than running `iru-check-license` directly if that skill is installed:
  `Agent({description: "Add license headers for <file(s)>", subagent_type: "iru-gate-runner", prompt: "Invoke
  Skill({skill: \"iru-check-license\", args: \"<file1,file2,...>\"}) scoped to the file(s) this task added or
  modified. Report back only which files were missing a header vs. fixed vs. already compliant."})`.
- Keep documentation comments current for the language in play, using whichever doc-comment skill this
  repository has installed for it, the same way, via `iru-gate-runner`.
- Run the relevant tests and check coverage for the touched code, and check for new code-quality issues against
  a pre-change baseline you capture yourself before implementing — all via `iru-gate-runner` delegating to whichever
  test/coverage/quality skills this repository has installed for that language, falling back to the language's
  own generic tooling directly (e.g. its native test runner) if none are installed.
- After each task in this bucket completes cleanly, immediately check off its box (and its sub-tasks') in
  `implementation_plan.md` per Step 4, and continue to the next.

If a test keeps failing after a genuine fix attempt in a way that suggests the plan's described approach is
actually wrong or infeasible, or the task is ambiguous in a way that changes correctness/scope and can't be
safely inferred, stop that task and record it as blocked (Step 4) rather than forcing it — same bar as any
one-task skill.

## Step 4 — Update `implementation_plan.md` and notify the user, per task and sub-task

As each task (from either Step 2's delegated buckets or Step 3's direct implementation) clears — don't batch this
until the whole group finishes:

- Check that task's own checkbox (`[ ]` → `[x]`), and the checkbox of every sub-task under it that was part of
  the completed work.
- Add a short note under the task naming the files touched, the tests added/updated, the coverage achieved, and
  the code-quality result, e.g. `- [x] Task 2. **Implement `SimpleWidget`** — tests in WidgetTest (94% line
  coverage, no new Checkstyle/PMD/SpotBugs issues).` If a new issue was left in place as unavoidable, name it and
  the reason here instead.
- Save the file immediately, then tell the user this specific task/sub-task just completed (a short one-line
  notification) — don't wait until the whole group is done to say anything, so progress is visible in real time
  across a group that might take a while.

If a task was reported blocked (Step 2 or Step 3), leave its checkbox unchecked, note the blocker under it in
`implementation_plan.md` in a short comment (not a checkbox note, since it's not done), and notify the user
immediately that this task is blocked, with enough detail (what was tried, what failed, why) to act on.

## Step 5 — Report the group's outcome

Once every task in the group has either completed cleanly or been recorded as blocked, hand control back to the
caller with a summary covering the whole group: per task, the files touched, tests added/updated, coverage
achieved, and code-quality outcome (or blocker detail if it didn't finish). This is what the caller (`iru-code`'s own
Step 5) uses to confirm the group's checkboxes and notify the user at the group level; this skill has already
handled the per-task/sub-task checkbox updates and notifications itself in Step 4.
