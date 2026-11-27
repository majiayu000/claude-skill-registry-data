---
name: onboarding-checks
description: "Use when an owner wants small checks that warn when work drifts - a branch that grows too big, work that stalls, or a security note that goes stale - and wants to set how often they run and who hears about them. First-time setup, a repository with no drift checks, or a team changing the thresholds. Installs the check scripts and writes .thrum/policy/checks.json. Runs as one part of project-onboarding and on its own."
---
<!-- markdownlint-disable MD013 -->

# onboarding-checks

Sets up the drift checks. It asks for the branch prefixes to watch, the size and stalled thresholds, how often the checks
run and how a report is delivered, copies the check scripts into `.thrum/policy/checks/`, and writes
`.thrum/policy/checks.json`. `resources/checks-schema.md` defines every key. The `answers.cadence` and `sections.S5`
records go in `.thrum/policy/onboarding.json`. The section is the same on the Free and the Pro setup, because monitors,
checks and delivery are not licensed.

## Opening offer

Show this offer before any other question.

<!-- onboarding:offer -->
> Say: This part sets up small checks that warn you when work drifts: a branch that grows too big, work that stalls, or a security note that goes stale. It asks how often each one should run; the coordinator part schedules them.
> Ask: Do this part now, or skip it for now? If you skip it, running project-onboarding again offers it again.
<!-- /onboarding:offer -->

"Skip it for now" records `sections.S5.status: skipped` with `reason: owner` in `.thrum/policy/onboarding.json` and ends
the section. "Do it now" goes on. When this skill runs alone the same offer is shown, and a skip never changes a record
that is already `done`.

When `.thrum/policy/onboarding.json` is absent, this skill creates `.thrum/policy/` and the file, and leaves `profile`
unset so it reads as `team`. It never reads the licence.

## History analysis

When .thrum/results/history-analysis.md is absent or stale, follow
history-analysis.md in the project-onboarding resources before the first block.

## Plain terms

Before each question that uses one of these terms, show its one-line explanation first, as a `> Say:` line starting
"In plain terms:". The terms are cadence, wake-on-change, delivery and monitor:

> Say: In plain terms: the cadence is how often a check runs, for example every 24 hours.
> Say: In plain terms: wake-on-change means a check speaks up only when something new has happened since its last report, and stays quiet otherwise.
> Say: In plain terms: delivery is how a report reaches the agent that should read it: into its terminal window when it has one open, or into its inbox.
> Say: In plain terms: a monitor is a small timer that runs a check again and again, so nobody has to remember to.

## The settings

These are the values this skill offers and writes. They are never values a script falls back to: a check script that finds
no `checks.json`, or no key in it, reports the miss and stops.

| Setting | Key in `checks.json` | Offered value |
|---|---|---|
| branch prefixes the scope check watches | `branch_globs` | fix/ feature/ feat/ refactor/ test/ (`["fix/", "feature/", "feat/", "refactor/", "test/"]`) |
| a branch is large | `size_threshold` | more than 300 lines (`lines: 300`) or more than 15 files (`files: 15`) |
| a branch is stalled | `stalled_hours` | stalled after 6 h (`6`) |
| how often the checks run | `cadence_hours` | the hours that `resources/suggest-cadence.sh` prints |
| how a report is delivered | `delivery` | `auto` |

The other keys of `resources/checks-schema.md` are written from the schema as it defines them: `test_globs`,
`merge_target_from` and `security_doc` with their schema values, and `deliver_to` and `dashboard_generator` left out.
`coordinator` is written later by `onboarding-coordinator`, never here.

### Cadence

Run `resources/suggest-cadence.sh` from the repository root. It prints the suggested hours on stdout and its basis on
stderr, and it is suggested again on every re-run, because how often work lands changes. It needs no `checks.json`. When
it exits 1 it prints no hours: show its reason to the owner and ask for the hours themselves, never assume one.

### Delivery

The offered value is `auto`, which the owner can override (`pane` or `inbox`). To show what `auto` does today, run
`thrum tmux status --json` and report whether the agent that will receive reports has a live tmux session: with one the
report goes to its terminal window (the pane), without one to its inbox. `checks.json` records `auto`, not the resolved
value. The recipient is the merge king of the merge target,
`orchestration.merge_kings[<merge target>]`; the schema says how that resolves when `deliver_to` is absent.

## Solo

Read `profile` in `.thrum/policy/onboarding.json`. Under `profile: solo`, show every setting in one table: the branch
prefixes, the size thresholds, the stalled time, the suggested cadence and the detected delivery, each with its "In plain
terms:" line where it uses a term above. With little history, the cadence rule already gives 24 h.

Each row has a plain label, its value and its reason. Never show a raw key as a row's name.

A Solo row uses the same keys.

Then ask once:

> Ask: These are the recommended check settings for a solo setup. Use them as they are, or review each one?

- On "use them", write the values as shown and ask nothing more.
- On "review", ask each setting as for a team.

## Team

Ask the settings in the table above as one block, following `resources/question-blocks.md` of project-onboarding. Each
row has a plain label, never the raw key, and its offered value is the Recommended answer: the prefixes, the two size
thresholds, the stalled time, the cadence (Why: the suggestion and its basis) and the delivery (Why: what `auto` does
today). The owner keeps or changes each row.

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: checks_branch_globs, checks_size_threshold, checks_stalled_hours, checks_cadence_hours, checks_delivery.
The two size thresholds are one row.

When the history read was skipped or found nothing,
put the History: line under every fallback line, as question-blocks.md says.

## Install

1. Create `.thrum/policy/checks/` and copy `lib.sh` and the three scripts `scope-check.sh`, `security-check.sh` and
   `suggest-cadence.sh` from this skill's `resources/` into it, keeping the file modes. Every check script sources
   `lib.sh` from its own folder.
2. Write `.thrum/policy/checks.json` with the keys of `resources/checks-schema.md` and the owner's values. On a re-run,
   read the existing file first and show each value that differs from the one offered; write the whole file back in one
   pass.
3. Write `answers.cadence` (the hours) in `onboarding.json`.

## No monitors here

This skill installs no monitor and schedules nothing. Tell the owner that onboarding-coordinator installs the monitors,
at `answers.cadence`, and offer to run it now. If the owner says yes, hand over to `onboarding-coordinator`; if not, say
that running project-onboarding or `onboarding-coordinator` later will do it.

## The reports

The scope check counts added lines in production files, leaving out test files and Markdown, and reads branches from this
machine and from origin. The security check reports hits that have landed and hits on branches that have not, and labels
each.

## The security check

This skill reads no security-model file and raises no notice about one. It states the rule, and the skill that decides it
is `onboarding-coordinator`.

The security-check monitor, which `onboarding-coordinator` decides, is installed only when the S1 watch-list block
records `non_goals_confirmed: true`.

When it is `false`, the security check is not scheduled, and the owner is told why once. A re-run after S1 confirms a
non-goal installs it.

## Finish

- Write `sections.S5` (`status`, `date`, `sha`) and `answers.cadence` in `onboarding.json`.
- Write nothing outside `.thrum/policy/`.
