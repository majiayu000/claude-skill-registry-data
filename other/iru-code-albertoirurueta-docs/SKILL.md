---
name: iru-code
description: Execute the tasks in implementation_plan.md at the repository root, one task group at a time — implement every task in a group (in parallel where the plan marks the group parallelizable), validate the whole group once (tests, coverage, code quality), and check off each task's checkbox directly in implementation_plan.md before moving to the next group. Dispatches each group to the `iru-code-one-task-group` skill, which in turn resolves the language/framework-specific `<key>-code-one-task-group` skill declared by the plan (e.g. `iru-java-code-one-task-group`, `iru-java-springboot-code-one-task-group`, `iru-kotlin-springboot-code-one-task-group`, `iru-quarkus-code-one-task-group`, `iru-php-code-one-task-group`, `iru-dotnet-code-one-task-group`, `iru-typescript-code-one-task-group`, `iru-nestjs-code-one-task-group`, `iru-nextjs-code-one-task-group`, `iru-fastapi-code-one-task-group`, `iru-django-code-one-task-group`, `iru-android-code-one-task-group`, `iru-swift-code-one-task-group`, `iru-kmp-code-one-task-group`, `iru-react-native-code-one-task-group`, `iru-windows-code-one-task-group`, `iru-rust-code-one-task-group`, `iru-go-code-one-task-group`) — falling back to implementing a task directly when the plan names no matching key. Runs autonomously — user intervention is limited to unresolved errors, decisions only the user can make, or permissions the allowed-tools list doesn't cover. Warns the user up front if implementation_plan.md already exists at the repository root (expected only when resuming an interrupted prior run). On successful completion, updates the project's Antora documentation (via the `iru-update-docs` skill) to reflect all the changes the plan made, archives the plan to .archive/, asks the user whether to open follow-up tasks or new tickets (on whichever tracker the plan originated from — a GitHub issue via `gh issue create`, or a Jira ticket via the `iru-create-jira-ticket` skill) if overall code quality isn't excellent, and asks for a final review of all code and documentation changes. Invoke as `/iru-code` once implementation_plan.md exists (e.g. produced by the `iru-plan` skill).
model: sonnet
allowed-tools: Read Edit Write Bash(mvn *) Bash(./mvnw *) Bash(./gradlew *) Bash(npm *) Bash(composer *) Bash(vendor/bin/*) Bash(detect-secrets *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(mkdir *) Bash(mv *) Bash(date *) Bash(gh issue create *) TaskCreate TaskUpdate TaskList TaskGet Skill Agent
---

# Implementation

Execute `implementation_plan.md` end to end: implement every task group listed against the real codebase, back
each group with a single consolidated validation pass, check tasks off in the plan file as they land, and move
on — with as little back-and-forth with the user as possible. This skill writes code; it is the execution
counterpart to the `iru-plan` skill. It uses a medium model on purpose: the plan already carries the hard reasoning
(task breakdown, dependency grouping, language/framework resolution) — this skill's job is to drive execution of
that plan, not to re-derive it. On successful completion it brings the project's documentation in line with
everything the plan changed (Step 8) and archives the plan file (Step 9) so the root only ever holds the plan for
work that is still outstanding.

## Step 1 — Load the plan, and warn if one already exists

Read `implementation_plan.md` at the repository root.

- **Missing or empty**: tell the user there is nothing to execute and suggest running `/iru-plan` first. Stop — this
  is not a case to interrupt the user about, just report it.
- **Present**: warn the user before doing anything else — this is a heads-up, not a question, so don't block on
  it unless the file looks genuinely inconsistent with the current task. Because a successful run always
  archives the plan to `.archive/` (Step 9), finding `implementation_plan.md` at the root when a run starts
  should only mean one of:
  - It was just written by the `iru-plan` skill for the task about to be executed (no checkboxes checked yet).
  - A previous `/iru-code` run on this same task was interrupted before finishing (some checkboxes checked, some
    not).
  - Unusually, every checkbox is already checked — a prior run finished all tasks but was interrupted before it
    could archive the file. Say so explicitly, then archive it immediately per Step 9 and report there is
    nothing left to execute, rather than re-running already-completed work.
  State which of these applies based on the checkbox state you see, then continue treating the file as the plan
  to execute/resume. If the plan's content clearly describes unrelated or stale work (not the task currently
  being asked about), stop and confirm with the user instead of assuming.
- Otherwise, read the plan in full, including the "Task summary" and "Current code state" sections for context,
  and the numbered "Implementation steps" (organized into task groups) for the actual work list.

## Step 2 — Verify checkbox placeholders and task groups

The `iru-plan` skill gives every top-level task and every sub-task its own empty markdown checkbox (`[ ]`), organized
into task groups each marked `Parallelizable: yes`/`Parallelizable: no`. Track completion by checking those boxes
— do not introduce a separate status tag or notation.

- Confirm each task/sub-task line has a `[ ]`/`[x]` checkbox. If the plan predates this convention and is
  missing checkboxes on some lines, add `[ ]` to those lines now (don't guess completion state — treat anything
  without a checked box as not done) and save the file before continuing.
- Confirm the plan organizes tasks into groups. If the plan predates the grouping convention and is a flat task
  list instead, treat every remaining (unchecked) top-level task as belonging to its own single-task group with
  `Parallelizable: yes` (a group of one is trivially parallelizable), preserving plan order — this keeps older
  plans executable without requiring the user to regenerate them.
- Treat any task or sub-task whose checkbox is already `[x]` (from a prior run of this skill) as already done —
  this makes the skill resumable across interrupted runs. A group where every task is already `[x]` is itself
  done; skip it entirely in Step 4.

## Step 3 — Track progress, and capture project-wide quality and security baselines

Mirror the plan's task groups into the session's task list (`TaskCreate`), one per pending group, so the user
can see live progress at the group level. Mark each `TaskUpdate`d as completed as you finish it, in step with the
plan-file confirmation in Step 5. This is in addition to, not a replacement for, updating `implementation_plan.md`
— the plan file is the durable record; the task list is the live view.

Before implementing anything, determine which language/framework(s) this plan is in play for: read the "Task
summary" section's **Language/framework** line if the plan declared one key for the whole plan, or the per-task
tags in "Implementation steps" if it declared them per task instead (this is exactly what the `iru-plan` skill's Step
5 produces). Collect the distinct set of keys found across the whole plan — usually just one (e.g. `java`,
`java-springboot`, `kotlin-springboot`, `quarkus`, `php`, `fastapi`, `django`, `dotnet`, `typescript`, `nestjs`, `nextjs`, `android`,
`swift`, `kmp`, `react-native`, `windows`, `rust`, or `go`), occasionally more for a plan spanning several languages.

Framework keys share their language's gate skills rather than having their own, so resolve each key's quality
skill as follows before looking it up (and use the same mapping in Step 7): `java-springboot` →
`iru-java-code-quality`; `kotlin-springboot` → `iru-kotlin-code-quality`; `quarkus` → `iru-java-code-quality` for a
Java build or `iru-kotlin-code-quality` for a Kotlin one (per `iru-explore`'s report or `src/main/kotlin/`); `php` →
`iru-php-code-quality`; `fastapi`/`django` → `iru-python-code-quality`; `nestjs`/`nextjs`/`react-native` →
`iru-typescript-code-quality`; `kmp` → `iru-kmp-code-quality`; `windows` → `iru-dotnet-code-quality`; any other key →
`iru-<key>-code-quality`.

For each distinct key, capture a project-wide quality baseline by delegating to the `iru-gate-runner` agent rather
than running that language's quality skill directly — use the quality skill resolved above for the
detected language/framework, e.g. `iru-java-code-quality` when the plan is Java (Checkstyle/PMD/SpotBugs), or
`iru-dotnet-code-quality` when it's .NET or a Windows desktop app (StyleCop.Analyzers/CA rules), `iru-typescript-code-quality` when it's
TypeScript (including NestJS/Next.js/React Native), `iru-kmp-code-quality` when it's Kotlin Multiplatform
(detekt/ktlint/Android Lint/SwiftLint), `iru-kotlin-code-quality` when it's Kotlin Spring Boot or Kotlin Quarkus
(detekt/ktlint), `iru-php-code-quality` when it's PHP (PHPStan/Psalm/PHPCS), `iru-python-code-quality` when it's
FastAPI or Django (Ruff/mypy), `iru-android-code-quality` when it's
Android, `iru-swift-code-quality` when it's Swift, `iru-rust-code-quality` when it's Rust (clippy/rustfmt/cargo-deny),
`iru-go-code-quality` when it's Go (golangci-lint/go vet/govulncheck), or whichever other quality skill the mapping above resolves to
and is found in this repository's `.claude/skills`: `Agent({description: "Capture code-quality baseline
(<key>)", subagent_type: "iru-gate-runner", prompt: "Invoke Skill({skill: \"<resolved quality skill>\"}) unscoped. Report
back only the total issue count per tool and the per-file list of issues."})`. `iru-gate-runner` runs in its own
separate context and is built to report back just the issue list rather than the full generated reports, keeping
that content out of the main context window since only the resulting list of issues is needed here. Record each
returned list, keyed by its language/framework, as that key's baseline — the final check in Step 7 compares each
one back against its own key's baseline to judge whether the plan's work left overall code quality at least as
good as it found it. Skip capturing a baseline for any key whose resolved quality skill isn't
installed in this repository, and skip this baseline capture entirely if no language/framework key could be
determined for the plan at all. When two keys resolve to the same quality skill (e.g. `java` and
`java-springboot`), capture its baseline once and share it between them.

Also capture a project-wide security baseline the same way, by delegating to `iru-gate-runner` rather than running
`iru-check-security` directly: `Agent({description: "Capture security baseline", subagent_type: "iru-gate-runner",
prompt: "Invoke Skill({skill: \"iru-check-security\"}) unscoped, project-wide. Report back only the count and the
per-file list of flagged secrets (new since the last `.secrets.baseline` update, plus any still lacking a triage
label)."})`. As with the quality baseline, this keeps the raw scan output out of the main context window since
only the resulting issue count/list is needed here. Record that returned count/list as the baseline the final
check in Step 7 compares against — the goal is to catch any task in this run that introduces a new secret into
the codebase, not to fix pre-existing findings this run didn't cause. If the sub-agent reports that
`detect-secrets` could not be installed and the user chose to continue without scanning, record that security
scanning is unavailable for this run, skip this and the corresponding Step 7 security check entirely, and say so
plainly in the Step 9 summary rather than silently omitting it. Skip this baseline capture outright if the
`iru-check-security` skill is unavailable in this repository.

## Step 4 — Implement task groups one at a time, in plan order

Process task groups strictly in the order they appear in the plan (the `iru-plan` skill orders them so each is
buildable on top of the previous one). Skip any group that is already fully done per Step 2. For each remaining
group, invoke the `iru-code-one-task-group` skill via the `iru-isolated-skill-executor` agent rather than calling
`Skill(...)` directly:

```
Agent({
  description: "Implement task group <N>",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-code-one-task-group\", args: \"<the full text of every task and sub-task in
    this group from the plan, each with its own language/framework tag if the plan sets one, the group's
    Parallelizable verdict, and any relevant \\\"Current code state\\\" context>\"}). Report back, per task in
    the group: the files touched, tests added/updated, coverage achieved, the code-quality outcome (including any
    issue left in place as unavoidable and why), whether license-header generation was skipped, and whether the
    task stopped on a blocker instead of finishing.",
  run_in_background: false
})
```

`iru-code-one-task-group` determines each task's language/framework, dispatches it to the matching
`<key>-code-one-task-group` skill when one is installed (or implements it directly as a best effort otherwise),
runs it in parallel across the group's tasks when the plan marked the group `Parallelizable: yes`, checks off
each task/sub-task's box in `implementation_plan.md` as it completes, and notifies the user of that per-task/
sub-task progress itself — none of that bookkeeping needs to happen again here. Running it via
`iru-isolated-skill-executor` keeps its own file reads/edits/reasoning out of `iru-code`'s own context, the same way the
one-task skills used to be invoked directly; this matters most on a plan with many groups, since without this
every group's full implementation transcript would accumulate in `iru-code`'s context across the whole run instead of
staying flat regardless of plan size. Wait for the agent to finish (`run_in_background: false` — Step 5 needs its
outcome before confirming the group's completion and moving on) before proceeding.

If the invoked `iru-code-one-task-group` skill reports that one of the group's tasks stopped short on a blocker (a
failing test that suggests the plan's approach itself is wrong, or an ambiguity only the user can resolve),
treat it the same as if it happened here: don't treat the group as complete, surface the blocker to the user via
`AskUserQuestion`, and stop rather than moving to the next group. If it reports the user chose to skip
license-header generation for some task, respect that choice for the rest of this run — don't ask again on later
groups.

Once `iru-code-one-task-group` reports every task in the group finished cleanly, proceed to Step 5 for this group,
then continue to the next unchecked group.

## Step 5 — Confirm the group's checkboxes and notify the user

`iru-code-one-task-group` already checks off each task/sub-task's own box in `implementation_plan.md` (and any
progress note) as it completes them — this skill does not re-write those lines. Immediately after a group clears
Step 4:

- Re-read `implementation_plan.md` and confirm every task/sub-task in the group is now checked (`[x]`). If any
  line in the group is still unchecked despite a clean report, treat that as inconsistent — re-invoke
  `iru-code-one-task-group` scoped to just the unfinished task(s) before moving on, rather than silently proceeding.
- Notify the user that the group completed: name the group, the tasks it covered, the files touched overall, and
  the aggregate coverage/code-quality outcome across the group's tasks — in addition to the plan file already
  reflecting it. This progress notification happens after every group, not just at the end of the whole run.
- Update the mirrored entry in the session task list (Step 3) to completed.

## Step 6 — When to interrupt the user

Keep interruptions rare — by design, this skill should run start-to-finish unattended on a well-formed plan.
Stop and use `AskUserQuestion` (or plain text if no real choice is being offered) only when:

- The `iru-code-one-task-group` skill invoked in Step 4 reports that one of the group's tasks stopped on a blocker —
  a test that keeps failing after a genuine fix attempt where the failure suggests the plan's described approach
  is actually wrong or infeasible against the real code, or an ambiguity that changes correctness or scope and
  can't be safely inferred (conflicting instructions, a choice only the user can make, a missing decision).
  Mirror the bar used by the `iru-plan` skill's Step 4: don't ask about things with an obvious best-practice answer.
- A tool call needs a permission outside this skill's `allowed-tools` list and the underlying action is risky or
  irreversible (e.g. anything beyond the scoped `mvn`/read-only `git` commands this skill is pre-approved for) —
  in this case the harness will already prompt; just make the case for why it's needed if asked.
- `implementation_plan.md` already has every checkbox checked when a run starts — handled in Step 1, not here;
  don't redo finished work.

Do not stop merely because a task is nontrivial — implement it. Do not check a task's box to move past a
blocker; leave it unchecked and surface the blocker instead (and skip Step 8's documentation update and Step 9's
archiving — an incomplete plan stays at the root so the next run can resume it).

## Step 7 — Final verification

Once every checkbox is checked, confirm the whole build — not just the incrementally-tested pieces — is healthy
by running the full local verification once per distinct language/framework key recorded in the plan (the same
keys Step 3 collected). Resolve the command for each key as follows:

1. If the repository's `CLAUDE.md` names a full local verification command for that stack (a "build", "verify",
   or "full check" command), use it verbatim.
2. Otherwise fall back to this key → command table:
   - `java`: `mvn clean jacoco:prepare-agent install jacoco:report javadoc:jar source:jar -P '!build-extras'`
     for Maven, `./gradlew build` for Gradle
   - `java-springboot`: `mvn -B -ntp clean verify`
   - `kotlin-springboot`, `quarkus`: `./mvnw -B -ntp clean verify` (or `mvn` without a wrapper) for Maven,
     `./gradlew build` for Gradle — container-backed tests in it need Docker; if Docker is unavailable, say so
     in Step 9 instead of treating the failure as a code defect
   - `php`: `composer validate --strict`, then the project's own `composer` test/lint scripts if defined,
     otherwise `vendor/bin/pest` or `vendor/bin/phpunit`, plus `vendor/bin/phpstan analyse` when configured
   - `fastapi`, `django`: the project runner prefix (`uv run` with a `uv.lock`, `poetry run`, `pdm run`, or the
     `.venv`) in front of `ruff check .`, `ruff format --check .`, `mypy .` (when configured) and
     `pytest` (the whole suite — `integration`-marked tests need Docker; if Docker is unavailable, say so in Step 9
     instead of treating the failure as a code defect); `django` adds `python manage.py check` and
     `python manage.py makemigrations --check --dry-run`; `fastapi` with Alembic adds `alembic check` when a
     database is reachable
   - `dotnet`: `dotnet build && dotnet test`; for a command-line tool (a `PublishAot` `Exe` using System.CommandLine)
     also `dotnet publish <cli project> -c Release -r <host RID>` so trim/AOT warnings surface — Native AOT needs the
     platform's native toolchain; when it is missing say so in Step 9
   - `windows`: `dotnet build -c Release` then `dotnet test --filter "TestCategory!=UI"` for the whole solution — on
     a non-Windows host add `-p:EnableWindowsTargeting=true` (WPF/WinForms and the Core project still build there) and
     run only the projects that can execute there (the `net10.0` Core tests), saying in Step 9 that the app run, the
     WinUI build and the UI tests are unverified (needs Windows); on Windows also run the desktop UI tests through
     `iru-dotnet-test` with the `ui` selector (it takes `.integration-test.lock` itself)
   - `typescript`: the package manager's `lint`, `typecheck` (when present), and `test` scripts, in that order
     (`npm run lint && npm run typecheck && npm test`, or the `pnpm`/`yarn` equivalents matching the lockfile)
   - `nestjs`: the same scripts as `typescript`, then `npm run build`
   - `nextjs`: the same scripts as `typescript`, then `npm run build` (`next build` — the build itself type-checks
     and verifies routes/caching rules)
   - `android`: `./gradlew build`
   - `kmp`: `./gradlew build -x iosSimulatorArm64Test -x iosX64Test` (compiles every target and runs the JVM/Android
     tests; the excluded Kotlin/Native simulator test tasks would boot a simulator outside the repository-wide
     `.integration-test.lock` — drop an `-x` for a task the build doesn't define), then, on macOS with Xcode, the iOS
     tests through `iru-kmp-test` with `target: ios` (it takes `.integration-test.lock` itself and reports
     "unverified" when no simulator runtime is available) and the iOS host app's `xcodebuild build` for a
     simulator destination (regenerating the project first with `xcodegen generate` when `iosApp/project.yml`
     exists); on any other host say in Step 9 that the iOS side is unverified
   - `react-native`: the same scripts as `typescript` (`lint`, `typecheck`, `test`); then for the `metro`
     toolchain `./gradlew assembleDebug` from `android/` and, on macOS, `pod install` + `xcodebuild build` of
     `ios/<App>.xcworkspace` for a simulator destination; for the `expo` toolchain `npx expo export` (the
     native-toolchain-free bundle check) — e2e flows are not part of this step
   - `swift`: `swift build && swift test` for a SwiftPM package, or `xcodebuild build-for-testing` (with the
     project's scheme and a simulator destination) for an Xcode app — `-destination 'platform=macOS'` for a
     macOS-only desktop app, plus `swift test` in its local `Packages/Core` (regenerate the project first with
     `xcodegen generate` when a `project.yml` exists); on a non-macOS host say in Step 9 that it is unverified
     (a SwiftPM command-line tool — an ArgumentParser executable — is just `swift build && swift test`, which
     also runs its CLI end-to-end tests, on macOS or Linux)
   - `rust`: `cargo fmt --all --check`, `cargo clippy --workspace --all-targets --all-features --locked -- -D
     warnings`, `cargo test --workspace --all-features --locked` (doctests included; `cargo nextest run` plus
     `cargo test --doc` when the project configures nextest), `cargo deny check` when a `deny.toml` exists, and for a
     command-line tool with an `xtask` member `cargo xtask docs` (the generated man page / CLI reference must still
     build) — `#[ignore]`d container-backed tests need Docker; if Docker is unavailable, say so in Step 9
   - `go`: `go build ./...`, `go vet ./...`, `go test -race ./...` (without `-race` when cgo is unavailable), then
     `golangci-lint run` when a `.golangci.yml` exists and `govulncheck ./...` when installed; with a
     `.goreleaser.yaml`, `goreleaser check` — `integration`-tagged tests need Docker; if Docker is unavailable, say
     so in Step 9
   - any other key: skip the full verification for that key and say so in Step 9's summary.

Run each resolved command through the `iru-gate-runner` agent, for the same reason as the other verification
steps in Step 4: `Agent({description: "Run full local verification (<key>)", subagent_type: "iru-gate-runner",
prompt: "Run `<resolved command>`. If it succeeds, report back only that the build succeeded. If it fails, report
back only the failing module/goal/target, the failure reason, and the relevant error output/stack trace."})`.
Running this via `iru-gate-runner` keeps the verbose build output out of the main context window. If a run fails,
fix it (or, if it's a genuine blocker per Step 6, stop and surface it) — do not archive a plan behind a broken
build. Re-invoke the same agent call after fixing, and repeat until it reports success. Skip this full
verification entirely (and note it in Step 9's summary) if no language/framework key could be determined for
the plan at all.

Then assess overall code quality against the baseline(s) captured in Step 3, once per distinct language/framework
key found in the plan:

1. For each key a baseline was captured for in Step 3, run its project-wide quality check by delegating to the
   `iru-gate-runner` agent, for the same reason as the other quality checks in this skill: `Agent({description:
   "Compare final quality against baseline (<key>)", subagent_type: "iru-gate-runner", prompt: "Invoke Skill({skill:
   \"<resolved quality skill>\"}) unscoped, project-wide. Compare the reported issues against this baseline: <that key's
   baseline from Step 3>. Report back only the total issue count per tool and the per-file list of issues."})` —
   e.g. `iru-java-code-quality` for the `java` baseline, `iru-dotnet-code-quality` for the `dotnet` baseline,
   `iru-typescript-code-quality` for `typescript`/`nestjs`/`nextjs`/`react-native`, `iru-kmp-code-quality` for
   `kmp`, `iru-dotnet-code-quality` for `windows`, `iru-kotlin-code-quality` for
   `kotlin-springboot` (and a Kotlin `quarkus`), `iru-php-code-quality` for `php`, `iru-python-code-quality` for
   `fastapi`/`django`, `iru-android-code-quality` for
   `android`, `iru-swift-code-quality` for `swift`, `iru-rust-code-quality` for `rust`, `iru-go-code-quality` for
   `go` — per the Step 3 mapping. Running each
   via `iru-gate-runner` keeps the full reports out of the main context window. Compare each returned counts/per-file
   list against that same key's Step 3 baseline.
2. If, across every key checked, the total issue count did not increase and is zero (or was already zero at
   baseline and still is), overall quality is excellent — proceed to Step 8.
3. Otherwise — one or more keys leave the project with more issues than it started with, or a nonzero count
   persists for one or more of them — do not silently proceed. Use `AskUserQuestion` to tell the user what
   remains (counts and a short summary per tool, grouped by language/framework key if more than one is involved)
   and ask whether they want to:
   - add follow-up task(s) to `implementation_plan.md` to fix the remaining issues before this run archives it
     (if chosen, add the task(s) — as a new group — with empty checkboxes and return to Step 4 to implement them —
     do not archive yet), or
   - file the remaining issues as new tickets instead — on whichever tracker the plan itself originated from, so
     follow-up work lands next to the ticket that spawned it rather than always defaulting to GitHub. Determine
     that origin the same way Step 9 will (check the "Task summary" section's `Source:` line, or any other clear
     ticket reference in the plan):
     - **Plan originated from a GitHub issue** (or no ticket origin is identifiable and this repository is
       GitHub-hosted, per `iru-explore`'s Step 2 detection): file via `gh issue create`, one issue per distinct
       problem or logical group, with enough detail (file, line, tool, message) to act on later.
     - **Plan originated from a Jira ticket**: file via the `iru-create-jira-ticket` skill instead, once per
       distinct problem or logical group — `Skill({skill: "iru-create-jira-ticket", args: "<file, line, tool,
       message, and enough surrounding detail to act on later>"})`. Since this problem is already fully
       characterized here, pass that detail directly as the skill's argument rather than letting it ask the user
       for purpose/context from scratch; still let it show its drafted ticket for confirmation before filing,
       per its own Step 4-equivalent review. If `iru-create-jira-ticket` reports it can't proceed (e.g. no Jira
       MCP tool connected), fall back to asking the user (`AskUserQuestion`) whether to file on GitHub instead or
       skip filing for now.
     - **Origin can't be determined and the repository isn't GitHub-hosted either**: ask the user
       (`AskUserQuestion`) which tracker to file to rather than guessing.
     or
   - leave it as-is and proceed to archive without further action.
   Respect whichever the user picks; only proceed to Step 8 once this choice has been acted on (issues filed, or
   explicit acknowledgment to proceed as-is).
4. If no language/framework key could be determined for the plan, or none of the keys involved have their resolved
   quality skill installed in this repository, skip this quality assessment entirely and proceed
   directly to the security assessment below. If only some keys have a matching skill, assess just those and note
   in the Step 9 summary which key(s) were skipped for lacking one.

Then assess security against the baseline captured in Step 3 (skip this entire assessment if Step 3 recorded
that security scanning is unavailable for this run, or if the `iru-check-security` skill is unavailable in this
repository):

1. Run the project-wide security check by delegating to the `iru-gate-runner` agent, for the same reason as the
   quality check above: `Agent({description: "Compare final security scan against baseline", subagent_type:
   "iru-gate-runner", prompt: "Invoke Skill({skill: \"iru-check-security\"}) unscoped, project-wide. Report back only the
   count and the per-file list of flagged secrets (new since the last `.secrets.baseline` update, plus any still
   lacking a triage label)."})`. Running this via `iru-gate-runner` keeps the raw scan output out of the main context
   window. Compare the returned count/per-file list against the Step 3 baseline.
2. If the count did not increase (zero flagged secrets beyond what Step 3 already recorded), security is
   clean — proceed to Step 8.
3. If the count increased — this run's tasks introduced a new secret, or left one newly unaudited — treat this
   as a hard stop, unlike the quality gate above: there is no "leave as-is and proceed" option here, since that
   risks committing a real credential. Use `AskUserQuestion` to show the user exactly what's new (file, line,
   secret type) and ask them to either:
   - remove or rotate the real secret(s) now, or
   - mark any false positives themselves via `detect-secrets audit .secrets.baseline` (this skill never performs
     that labeling on the user's behalf — see `iru-check-security`'s own Step 6),
   then re-run this security check (repeat from item 1) until it reports no increase. Do not proceed to Step 8 —
   do not check off, archive, or otherwise treat any task as complete — while an unresolved increase remains.
   This is what keeps a leaked secret from ever reaching a state that this skill, or any skill/session that picks
   up after it (e.g. `iru-pr-description`, `iru-issue`, or the user's own next `git commit`), could commit, push, or
   include in a pull request.
4. If the `iru-check-security` skill is unavailable in this repository, or Step 3 recorded that scanning was skipped
   for this run, skip this security assessment and proceed to Step 8 directly.

## Step 8 — Update documentation

Once Step 7 passes clean (healthy build, and the quality and security gates both resolved), bring the project's
Antora documentation in line with everything this run actually changed, by delegating to the `iru-update-docs` skill:
`Skill({skill: "iru-update-docs"})`. Invoked with no argument, `iru-update-docs` covers uncommitted changes plus any
commits already made on the current branch that aren't on the base branch — which is exactly this run's surface,
since Step 9 hasn't committed or archived anything yet. That means it picks up every group processed across all
of Step 4's iterations, not just the last one, so the docs reflect the plan's full scope rather than only its
final group.

- If this repository has no Antora documentation site, `iru-update-docs` should report that plainly rather than
  fail — treat that as nothing to do here and continue to Step 9.
- If `iru-update-docs` needs to ask something only the user can resolve (per its own rules), let it surface via
  `AskUserQuestion` rather than guessing on its behalf.
- Note what `iru-update-docs` changed (which pages, for which behavior) so it can be folded into the Step 9 summary
  alongside the code changes.

Then continue to Step 9.

## Step 9 — Archive the plan and ask for review

Only after Step 7 passes clean, with every task's checkbox checked, both the quality and security gates above
resolved, and Step 8's documentation update done:

1. Determine an identifier for the archived filename:
   - If the plan was grounded in a tracked ticket, check the "Task summary" section for a `Source:` line (per
     `iru-plan`'s Step 6.1) or any other clear reference to the plan's origin, and use that ticket's id/key:
     - A GitHub issue (e.g. "Source: GitHub issue #42", or just "issue #42") → use the bare issue number, `42`.
     - A Jira ticket (e.g. "Source: Jira PROJ-123", or a bare key matching the `PROJECTKEY-ID` pattern — one or
       more uppercase letters/digits starting with a letter, a hyphen, then digits) → use that key as-is,
       `PROJ-123`. Jira keys already contain a hyphen, so keep the identifier intact rather than splitting on it.
     - If the plan's origin is ambiguous (e.g. a older plan predating the `Source:` convention) but a ticket
       reference is still clearly present somewhere in the plan, use your best judgment to extract it rather than
       falling back to a timestamp.
   - Otherwise (a manually described task with no ticket, or genuinely no identifiable reference), use the
     current timestamp: `date +%Y%m%d%H%M%S`.
2. Create the archive directory if it doesn't exist yet (`mkdir -p .archive`), then move the plan there, renamed
   to embed that identifier: `mv implementation_plan.md .archive/implementation_plan_<ticket_id>.md` (e.g.
   `.archive/implementation_plan_42.md` for a GitHub issue, `.archive/implementation_plan_PROJ-123.md` for a
   Jira ticket, or `.archive/implementation_plan_20260707153000.md` with no ticket). The repository root must no
   longer have an `implementation_plan.md` once this step completes successfully.
3. Summarize for the user: which groups/tasks were completed, the files touched overall, the coverage achieved
   per task/class, the final code-quality outcome (excellent / follow-up filed / issues left as-is per Step 7),
   the final security outcome (clean / not run, since a resolved-but-triggered gate is otherwise indistinguishable
   from clean once Step 7 passes), what Step 8 updated in the documentation (or that there was no documentation
   site to update), and where the plan was archived to.
4. Explicitly ask the user to review the code and documentation changes (e.g. `git diff` / `git status`) before
   anything is committed. Do not commit, push, or open a PR — this skill's job ends at working, tested, reviewable
   code. This applies with extra force if Step 7's security gate ever fired during this run: even though it must
   have been
   resolved to reach this point, remind the user to double-check the resolution (secret actually removed/rotated,
   or genuinely a false positive) before they or any subsequent skill commits, pushes, or opens a PR.
