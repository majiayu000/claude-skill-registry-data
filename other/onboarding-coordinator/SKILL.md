---
name: onboarding-coordinator
description: "Use when an owner wants the coordinator agent that runs everything else set up - its role block, the owner's rulings, the hourly reminder, the drift-check and dash-tick monitors, and where it keeps its state. First-time setup, a repository whose coordinator has no written rules, or a licence change that needs the other setup. Installs the monitors, writes the coordinator's role block and the rulings, and runs configure-roles. Runs as the last part of project-onboarding and on its own."
---
<!-- markdownlint-disable MD013 -->

# onboarding-coordinator

Sets up the coordinator agent. It asks how often the coordinator is nudged, installs the monitors, writes the
coordinator's role block in `.thrum/policy/roles/coordinator.md`, writes the owner's rulings, sets up where the
coordinator keeps its state and its owner questions, and runs configure-roles. It records `sections.S6`, `variant` and
`answers.reminder_cadence` in `.thrum/policy/onboarding.json`, and writes `coordinator` in
`.thrum/policy/checks.json`. The checks and the dash tick are the same on both setups. The role block, the reminder text,
the rulings, the state and the owner questions follow the variant.

## Opening offer

Show this offer before any other question.

<!-- onboarding:offer -->
> Say: This part sets up the coordinator agent that runs everything else: its role, your rulings, its reminders and where it keeps its state. It asks a few questions about how you want to hear about work and decisions.
> Ask: Do this part now, or skip it for now? If you skip it, running project-onboarding again offers it again.
<!-- /onboarding:offer -->

"Skip it for now" records `sections.S6.status: skipped` with `reason: owner` in `.thrum/policy/onboarding.json` and ends
the section. "Do it now" goes on. When this skill runs alone the same offer is shown, and a skip never changes a record
that is already `done`.

When `.thrum/policy/onboarding.json` is absent, this skill creates `.thrum/policy/` and the file, and leaves `profile`
unset so it reads as `team`.

<!-- onboarding:licence -->
**Licence read.** Do this before the first question, every time this block runs.

1. Run `thrum license status --json` and rewrite the `licence` record in `.thrum/policy/onboarding.json` from it. Copy
   only `status`, `tier`, `capabilities`, `repo_capabilities` and `oss_grants`, and set `checked` to the current time.
   Never copy `registration_record`, `machine_id`, `repo_origin` or `repo_id`: the file is committed with the code. If
   the command fails, replace the whole record with `{checked, status: "unknown", capabilities: []}`, with no `tier`
   and no `oss_grants`.
2. Derive the variant. It is `pro` when `repo_capabilities` contains all three of `queue.write`, `state.write` and
   `memory.substrate`. Otherwise it is `free`. The skill never matches `oss_grants.repos[]` itself
   and never derives a repository id. Follow only that variant's instructions. Offer the dashboard only when the
   variant is `pro` and `repo_capabilities` also contains `dashboard.write`.
3. Never read a `licence` record left by an earlier run without refreshing it first.
4. If a Pro write is refused anyway, stop that step and print:

   > Say: Your licence no longer covers this step. Run onboarding-coordinator to switch to the matching setup.

   Inside `onboarding-coordinator` itself, do not print that line. Run step 1 again and continue with the variant it
   derives.
<!-- /onboarding:licence -->

## History analysis

When .thrum/results/history-analysis.md is absent or stale, follow
history-analysis.md in the project-onboarding resources before the first block.

## Plain terms

Before each question that uses one of these terms, show its one-line explanation first, as a `> Say:` line starting
"In plain terms:". The terms are cadence, reminder cadence and dashboard:

> Say: In plain terms: the cadence is how often a check runs, for example every 24 hours.
> Say: In plain terms: the reminder cadence is how often the coordinator gets a nudge to review its work list and your open questions, for example every hour.
> Say: In plain terms: the dashboard is a page that shows the work in flight and the questions waiting for you, so you can answer them with one click.

## The variant

Derive the variant once, from the licence read above, and use it for every item that has a variant: the reminder text,
the role block, the rulings, the state and the owner questions. The monitors for the checks and the dash tick, and the
configure-roles run, have no variant. No item mixes the two. At the end of the run write `variant` (`{value, date}`) in
`onboarding.json`. Read `.thrum/policy/installed.md` before any write; when it is absent, create it from
`resources/installed-template.md`. Every write outside `.thrum/policy/` and `.thrum/results/`, and every role block, gets
an `installed.md` row; a re-run updates `active` rows and never adds a duplicate.

## The coordinator and where its files live

After the offer is accepted and the variant is derived, and before any write, say:

> Say: This agent becomes your coordinator. From now on it receives the check reports and reminders in this session. When this session is closed, reports wait in its inbox, and it reads them when it next starts.

Then say the line for the derived variant, exactly one of the two:

- Free (variant `free`):

  > Say: On your Free licence, your work list and the decisions you make here are kept as files in .thrum/policy/, and the coordinator's notes in .thrum/results/ on this machine.

- Pro (variant `pro`):

  > Say: On your Pro licence, the work list, your decisions and the coordinator's notes are kept in Thrum itself, not as files in this repository. Open questions for you go in .thrum/policy/worklist.md, or in the dashboard if you choose it.

## Committed files notice

Before the first write to `worklist.md` or `rulings.md`, show the notice for the variant. Check `reported` in
`onboarding.json` for the signature `committed-files:<variant>`: show the notice only when it is absent, then add the
signature, so each owner sees it once per variant, whichever skill writes first.

- Free:

  > Say: Your work list and the decisions you make here go in .thrum/policy/worklist.md and .thrum/policy/rulings.md, which are committed with your code.

- Pro (only `worklist.md` is written, for owner questions without a dashboard):

  > Say: Open questions for you go in .thrum/policy/worklist.md, which is committed with your code.

## Step 0: Monitors already running

Do this before the block of questions in Step 1 is asked.

1. Before starting any monitor, run `thrum monitor list --json` and read what is already running.
2. Leave out every monitor that an active monitor row in installed.md names: those are Thrum's own.
3. For each job below that has no active monitor row and no kept-monitor row,
   look for a running monitor that does the same job.
   Judge by its name and its command (argv in the list). A schedule is never evidence.

| Job | A running monitor does this job when |
|---|---|
| the scope check | its command runs a script that reports branch size or runs scope-check.sh. |
| the security check | its command runs a script that scans for watch-list words or runs security-check.sh. |
| the dash tick | its command runs a dashboard or status tick script or runs dash-tick.sh. |
| the reminder | it has no script and sends a fixed text about the work. |

The job in the script column of a `kept-monitor` row is one of `scope-check.sh`, `security-check.sh`, `dash-tick.sh` or
`reminder`.

## Step 1: Asks

Ask these as one block, following `resources/question-blocks.md` of project-onboarding. Each row has Recommended and
Why. Rows 2 and 3 list their choices on a Choices line (pick one); row 1 is a free number and has no Choices line. On
Solo, the recommended answer for rows 2 and 3 is `off`.

When the history read was skipped or found nothing,
put the History: line under every fallback line, as question-blocks.md says.

1. The dash-tick cadence, with `answers.cadence` as the recommended answer, written to `answers.cadence`.
2. The reminder cadence, written to `answers.reminder_cadence`. Choices: `1h` / `off`; `1h` recommended on Team.
3. Whether to install the dashboard, written to `answers.dashboard`. Choices: yes / no. Include this row only when the variant is `pro` and
   `repo_capabilities` contains `dashboard.write`; otherwise write `false`, leave the row out, and when the owner
   declines write `false`.

For each job where Step 0 found a running monitor, add one more row to this block:

- Where one is found, ask a row: "You already have <name> (<schedule as listed>). Install Thrum's monitor for <job> as
   well?" Choices: keep yours / install Thrum's too. Recommended: keep yours. Why: names the monitor and what it runs.
- Where a running monitor might do the job and you cannot tell, ask the same row with Recommended: install Thrum's too,
   and the fallback line as its Why: "No evidence in this repository; this is Thrum's default."

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: coordinator_cadence, coordinator_reminder_cadence, coordinator_dashboard when that row is shown, and
coordinator_monitor_<job> for each monitor row.

Each asked term gets its "In plain terms:" line first.

## Step 2: Monitors

- Where none is found, start the monitor without asking.
- For "keep yours", add a kept-monitor row to installed.md with that monitor's name as the target and the job in the
   script column, and start no monitor for that job. The row covers that one job only.
- If the list cannot be read, say so, start no monitor, and go on with the rest of this part.

Start each monitor with `thrum monitor start --schedule '<cron>' --name <name> --match '.' --to <coordinator> -- <command>`,
staggering the minutes so no two run together. Add a `monitor` row to `installed.md` for each, with the monitor id as
the target. Install:

1. **The checks.** `scope-check.sh` and `security-check.sh` from `.thrum/policy/checks/`, at `answers.cadence`.
   - Scope check: install it.
   - Security check: install it only when the `onboarding-watch-list` block in `.thrum/policy/security-model.md`
     records `non_goals_confirmed: true`. With `false`, do not install it, and tell the owner why once: no non-goal is
     confirmed yet, so the check has nothing to enforce. A re-run after the security section confirms a non-goal installs
     it. When the file or the key is missing, this one step follows `missing-policy-alert.md` in the project-onboarding
     resources: the signature is `missing:security-model.md` when the file is missing, or
     `missing:security-model.md:non_goals_confirmed` when only the key is, and the skipped wording applies when the
     security section is recorded `skipped`. The step stops, and the other monitors still install.
2. **The dash tick.** Copy `resources/dash-tick.sh` into `.thrum/policy/checks/`, keeping its mode, and install it as a
   monitor at the dash-tick cadence. It uses `lib.sh` from the same folder.
3. **The reminder**, at `answers.reminder_cadence`, unless it is `off`. Its text is `resources/reminder-pro.md` (names the
   queue) on the Pro variant and `resources/reminder-free.md` (names `worklist.md` `## Work`) on the Free variant.

## Step 3: The role block

Write the variant's resource, `resources/role-block-pro.md` or `resources/role-block-free.md`, unchanged, as the block
between `<!-- onboarding:S6 -->` and `<!-- /onboarding:S6 -->` in `.thrum/policy/roles/coordinator.md`: read the file,
replace only that block or append it, write it back with `thrum roles rules set coordinator`, then apply it with
`thrum roles deploy`. The coordinator applies the owner-questions condition in the resource when it runs. Add one
`role-block` row to `installed.md`.

If the owner brought in custom skills, commands or agent prompts, name each by path in one line appended inside the block,
after the resource's text. That line is covered by the same `role-block` row.
An item whose answers.inventory decision is leave is not named.

## Step 4: Owner rulings

Write each entry of `answers.rulings` (an entry is `{id, date, trigger, rule, applies_to, from}`). Skip an entry whose id
already exists at the destination.

- Pro: one `thrum memory create --kind agent_rule` for each, with `onboarding:<id>` as the first body line. The command
  cannot name a role other than the caller's, and this skill runs as the coordinator:
  - an `applies_to: coordinator` ruling uses `--scope role`, which is the caller's own role;
  - every other ruling, including `all`, uses `--scope project --tag applies-to:<role|all>`, and its trigger line names
    the role, so every role's recall finds it.

  Add a `memory-rule` row for each memory.
- Free: one line each in `.thrum/policy/rulings.md`, in the format of the policy README.

The notes and memory entries the inventory found for this section are offered through the block below. A copy goes to
`imported/rules.md` with its `imported-from` row, and each one is appended to `answers.rulings`, so this step writes it
out with the other rulings.

<!-- onboarding:inventory -->
**Bring in what you already have.** Offer the items the inventory found for this section, never an item it skipped.

1. Offer each `answers.inventory` record whose `offered_in` is this section and whose `decision` is `pending`. With no
   `answers.inventory`, offer nothing. A `security-note` record is not offered: the security section reads it into the
   scan report and sets it `prefilled`.
2. Before the first copy is written, show the committed-copies line, unless `reported` already holds the signature
   `imported-copies`. After showing it, add that signature to `reported`.

   > Say: What you bring in is copied into .thrum/policy/imported/, which is committed with your code.

   In stealth mode, leave out the words about being committed with your code from every notice.

3. Team offers the part's found items as blocks in the form of `resources/question-blocks.md`, one row per item, or one
   row per file when the file has more than seven found items. A file with more than seven found items is one row. On
   that row, "choose one by one" opens its own blocks. Each row has the choices bring in / leave, `Recommended:` is
   `bring in`, and `Why:` says in one line what the item is.
   When you cannot say what an item is, recommend "leave" and use the fallback line.
   `<n>` on a file row never counts an item skipped as a credential.

   Solo asks one table question per section that has found items, covering all of them, and asks nothing when nothing
   was found. On that question, "choose one by one" opens blocks:

   > Ask: I found <n> things you already have that fit this part of the setup. Bring them all in, choose one by one, or leave them all?

4. When a ratchet script has only a guessed ceiling file, Team makes the ceiling a row of the block, in the same row
   form: the question is whether `<file>` is the ceiling that `<script>` checks against, the choices are yes / no,
   `Recommended:` is `yes`, and `Why:` names the file as the nearest checked-in data file to the script.

5. A ruling made from a brought-in item has these fields:
   - `trigger` is "working in this repository".
   - `rule` is the item's first line, without its list marker. For a whole-file note, it is the file's first heading,
     or failing that its first line.
   - `applies_to` is `all`.
   - `from` is `<section title>, imported/rules.md#i-<n>`, and the `rulings.md` line renders it as written. The full
     text stays in the copy.
6. After the copies are written, a section that wrote at least one copy shows this line once, as the last action of the
   copy step: the copy step is not finished until the line below is shown. A section that copied nothing does not show
   it, and a ratchet brought in is not a copy, so it does not count.

   > Say: Thrum's copy in .thrum/policy/imported/ is now the one to edit. Your original is untouched and is still read by any tool that reads it today, so a rule you change in one place should be changed in the other. A full re-run notices a changed original and offers to refresh the copy.
<!-- /onboarding:inventory -->

## Step 5: State

- Pro: before the first `thrum state set --kind personal_state`, run `thrum state describe personal_state` and give
  every non-optional field a string value. All values are strings, `next_actions` included; it is not an array. Pass the
  JSON with `--stdin` and a quoted heredoc.
- Pro: set the base state with `thrum state set --kind personal_state --scope self`, and the topic scopes
  `personal_state:.merge_gates`, `personal_state:.security` and `personal_state:.scope`, each with a `cold_successor`.
  Add a `state-scope` row for each scope. The prime shows only `.merge_gates`, which is why the Pro role block tells the
  coordinator to run `thrum state get` for the others at session start.
  Write each topic scope with --scope set to the part after "personal_state:", for example
  thrum state set --kind personal_state --scope .security, and read it back with thrum state get personal_state:.security.
- Free: create `.thrum/results/coordinator-state.md` with the headings `## Current state`, `## Next actions`,
  `## Merge gates`, `## Security` and `## Scope`, in that order. Each of the last three ends with a `Cold successor:`
  line.

## Step 6: Owner questions

- Pro, when `answers.dashboard` is `true`: action-picks on the dashboard.
- Otherwise: create `.thrum/policy/worklist.md` with empty `## Work` and `## Owner questions` sections, if it is
  absent, after the committed files notice.

## Step 7: configure-roles

Run the configure-roles skill; it lists every role. Then write `sections.S6` (`status`, `date`, `sha`), `variant` and
`answers.reminder_cadence` and `answers.dashboard` in `onboarding.json`, and `coordinator` (this agent's name) in `.thrum/policy/checks.json`.

## A licence change

A re-run where the derived variant differs from the recorded `variant` is a licence change. Offer to copy by id, and
add a `copied-item` row to `installed.md` for each copy. An id that already exists at the destination is skipped, so a second
copy run copies nothing.

- Free to Pro: offer to copy the open `## Work` items to the queue, the open `## Owner questions` to the dashboard when
  `answers.dashboard` is `true`, each `rulings.md` line to an `agent_rule` memory, and the state file to
  `personal_state`. After the switch the Pro variant ignores `rulings.md`, `coordinator-state.md` and the `## Work`
  section, and offers to delete them; delete only on a yes. Keep the `## Owner questions` section: it stays the Pro
  channel unless `answers.dashboard` is `true` and every open question was copied to it.
- Pro to Free: reads stay free, so offer to copy the open queue items, the rulings and the state into the Free files, by
  id. Then switch the block, the reminder and the dash tick to Free. Write the block as in Step 3: the Free resource,
  plus the custom-commands line when the owner brought any in. The dash tick follows variant.value, so its monitor stays
  as it is.

## Solo

Read `profile` in `.thrum/policy/onboarding.json`. Under `profile: solo`, install the checks and the dash tick, the role
block, the rulings, the state, the owner questions (the no-dashboard branch) and the configure-roles run. The hourly
reminder and the dashboard are offered, defaulting to off. Offer the import as one table question, as in the block above.

## Finish

- Write `sections.S6`, `variant` and `answers.reminder_cadence` in `onboarding.json`.
- Write nothing outside `.thrum/policy/` and `.thrum/results/` apart from the monitors, the memories, the state scopes
  and the role deploy.
