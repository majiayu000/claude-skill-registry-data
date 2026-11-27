---
name: onboarding-gates
description: "Use when an owner wants to set how changes are checked before they land - which tests run on every change, how often the full slow suite runs, and who merges. First-time setup, a repository with no gate configuration, or a team changing who lands merges. Asks about tiers, lane scope, topology and defaults, offers the checks and hooks the repository already has, and writes .thrum/policy/gates.json through project-gate-setup. Runs as one part of project-onboarding and on its own."
---
<!-- markdownlint-disable MD013 -->

# onboarding-gates

Sets how changes are checked before they land. It asks how the team lands changes, offers the checks already in the
repository, and hands every decision to `project-gate-setup`, which writes `.thrum/policy/gates.json`. It writes the
merge king's entry in `orchestration.merge_kings`, and the `answers` and `sections.S4` records in
`.thrum/policy/onboarding.json`.

## Opening offer

Show this offer before any other question.

<!-- onboarding:offer -->
> Say: This part sets how changes are checked before they land: which tests run and who merges them. It asks how your team lands changes, and offers the checks you already run, such as make targets and git hooks.
> Ask: Do this part now, or skip it for now? If you skip it, running project-onboarding again offers it again.
<!-- /onboarding:offer -->

"Skip it for now" records `sections.S4.status: skipped` with `reason: owner` in `.thrum/policy/onboarding.json` and ends
the section. "Do it now" goes on. When this skill runs alone the same offer is shown, and a skip never changes a record
that is already `done`.

When `.thrum/policy/onboarding.json` is absent, this skill creates `.thrum/policy/` and the file, and leaves `profile`
unset so it reads as `team`. It never reads the licence.

## History analysis

When .thrum/results/history-analysis.md is absent or stale, follow
history-analysis.md in the project-onboarding resources before the first block.

## Plain terms

Before each question that uses one of these terms, show its one-line explanation first, as a `> Say:` line starting
"In plain terms:". The terms are: tier, lane, changed-scope lane, batch race, topology, merge king, gate box, ratchet,
lens and unmeasured finding. Write each explanation in everyday words, in one line. The batch-race line is exactly:

> Say: In plain terms: a batch race means that once every N merges, the full slow test suite runs on the main branch, instead of on every merge.

The other nine are written the same way:

> Say: In plain terms: a tier is one level of checking, such as the quick checks every change gets or a slower check that runs less often.
> Say: In plain terms: a lane is one set of commands that checks a change, such as the tests or the linter.
> Say: In plain terms: a changed-scope lane runs only the tests that depend on the files a change touched, instead of every test.
> Say: In plain terms: topology is who does the landing work: who merges, who runs the checks, and on which machine.
> Say: In plain terms: the merge king is the one agent that is allowed to merge changes into the main branch.
> Say: In plain terms: a gate box is a separate machine that runs the checks, so they do not slow down your own.
> Say: In plain terms: a ratchet is a count that may fall but never rise, such as the number of lint warnings.
> Say: In plain terms: a lens is a focused review that reads a change for one kind of problem, such as breaking an engineering rule.
> Say: In plain terms: an unmeasured finding is a reviewer's concern that comes with no failing test and no way to reproduce it.

## Solo

Read `profile` in `.thrum/policy/onboarding.json`. Under `profile: solo`:

- Step 3 comes first. It is pre-answered with topology `solo`: one coordinator, which is also the merge king, and the
  gates run by that coordinator on the same machine. It asks only which agent coordinates (default: the agent running
  onboarding). It writes:
  - the `orchestration.merge_kings` entry for the merge target, set to that agent (Step 3 says how);
  - `runner`: that agent;
  - `gate_box: "local"`;
  - `merge_king: {"from": "orchestration.merge_kings"}`.
- Check reports go to that agent: it is the merge king, so it is the default recipient of the check reports.
- After Step 3's coordinator question, show the Solo values for Steps 1, 2 and 4 as blocks of at most seven rows, in the
  form of `resources/question-blocks.md` of project-onboarding, each headed `Block <i> of <k>: <topic>`. Each row has a plain label, its value and its reason. Never show a raw key as a row's name. Each row also shows the "In plain terms:" line of the first term it uses. The values are:
  - Step 1, tiers: the per-landing lane only, with no race lane, batch race, daily full gate, philosophy lens, hotpath
    lens or ratchets;
  - Step 2: `answers.lane_scope: whole`, because `coupling.changed_scope_viable` is `false` under Solo;
  - Step 4: `batch.every_n_landings: 0` (no batch race), `batch.cmd: ""`, `batch.required_for_deploy: false`, and the
    other three defaults (`per_landing_race: concurrency_only`, `retention_paths`,
    `policy.unmeasured_findings_block: false`).

  Then ask once:

  > Ask: These are the recommended gate settings for a solo setup. Use them as they are, or review each one?

  - On "use them", write the values, write `answers.hot_paths: []` and
    `tiers: {philosophy_lens: false, hotpath_lens: false}`, and run Step 6 (`project-gate-setup` only; the
    hotpath step is not chosen) and Step 7 with no further questions.
  - On "review", walk Steps 1, 2 and 4 as for a team, and Step 6 offers the hotpath step as for a team.
- Step 5 is offered only when `answers.burn_down` or `answers.ratchet_candidates` is non-empty, or `answers.inventory`
  holds a `pending` ratchet record. A writer that has nothing to write leaves `[]`, so these lists are never absent.

A Solo row uses the key of the same setting in Steps 1, 3 and 4.

Every key is still written, so no later step meets a missing key.

## Step 1: Tiers

Team asks Steps 1, 3 and 4 as blocks in the form of `resources/question-blocks.md` of project-onboarding: at most seven
rows, aim for five, numbered rows, a `Choices:` line with (pick one) or (pick several) only on a pick row, `Recommended:`,
`Why:`, and the reply line. Write each block as plain text in your reply. Show the "In plain terms:" line from the Plain
terms section directly above the row that first uses its term. A row with no evidence uses the fallback line from
`resources/question-blocks.md` and the fallback value for that setting.

When the history read was skipped or found nothing,
put the History: line under every fallback line, as question-blocks.md says.

The per-landing lane is always on, and you say so. Ask the other six options as one block of pick-one rows. A row
recommends `yes` when something found supports it (a race or sanitizer job in the repository's CI, performance findings
in the history analysis for the hotpath lens review, ratchet candidates for ratchets), and `no` with the fallback line
otherwise:

```text
Block 1 of 3: Tiers

1. Run a race or sanitizer lane, a separate slower check for concurrency problems?
   Choices: yes / no (pick one)
   Recommended: <yes when a race or sanitizer job was found, otherwise no>
   Why: <one line naming that job and where it was found, or the fallback line>
2. Run a batch race, the full slow suite on the trunk tip after every few landings?
   Choices: yes / no (pick one)
   Recommended: <yes or no, from what was found>
   Why: <one line naming the evidence, or the fallback line>
3. Run a daily full gate, the whole slow test suite once a day?
   Choices: yes / no (pick one)
   Recommended: <yes or no, from what was found>
   Why: <one line naming the evidence, or the fallback line>
4. Add a philosophy lens review?
   Choices: yes / no (pick one)
   Recommended: <yes or no, from what was found>
   Why: <one line naming the evidence, or the fallback line>
5. Add a hotpath lens review?
   Choices: yes / no (pick one)
   Recommended: <yes when the history analysis found performance areas, otherwise no>
   Why: <one line naming those areas, or the fallback line>
6. Add ratchets?
   Choices: yes / no (pick one)
   Recommended: <yes when ratchet candidates were found, otherwise no>
   Why: <one line naming them, or the fallback line>

Reply "yes to all", tell me what to change (for example "3: no"), say "not sure about 3", or ask "explain 3".
```

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: gates_race_lane, gates_batch_race, gates_daily_full, gates_philosophy_lens, gates_hotpath_lens,
gates_ratchets.

The batch-race row sets whether Step 4 shows the batch rows. On `no`, Step 4 skips the batch rows and writes `batch.every_n_landings: 0`, `batch.cmd: ""` and `batch.required_for_deploy: false`. On `yes`, Step 4 asks how many landings, with 5 recommended.

Record the choices as `tiers` for `project-gate-setup`. Write the two lens answers to `gates.json` as
`tiers.philosophy_lens` and `tiers.hotpath_lens`: `true` when the owner chose that lens review, `false` otherwise.

## Step 2: Lane scope

Read `coupling.changed_scope_viable` in `.thrum/policy/onboarding.json` and write `answers.lane_scope` (`changed` or
`whole`). When the key is `true`, offer changed-scope lanes. When it is `false`, write `whole`. When the key is absent,
never read that as `false`: tell the owner that the coupling measurement has not been made, name `onboarding-coupling` as
the skill that writes it, and stop this step until it is run.

## Step 3: Topology

Ask three questions as the second block, in the form of `resources/question-blocks.md` of project-onboarding:
who lands merges (the merge king); whether a gate agent runs the gates or the coordinator runs them inline; and whether a dedicated
gate box exists. Find the evidence first: `thrum team` shows whether a gate-role agent is registered, and `thrum peer list`
shows whether a second machine is paired. With no second machine and no gate agent registered, each row
recommends the coordinator as the one who merges, the checks run by the coordinator, on this machine, and `Why:` names
what was found: no second machine, no gate agent registered.

```text
Block 2 of 3: Who lands changes

1. Who lands merges?
   Choices: the coordinator / another agent, which you name (pick one)
   Recommended: the coordinator
   Why: <one line: no second machine, no gate agent registered>
2. Who runs the checks?
   Choices: the coordinator, inline / a gate agent (pick one)
   Recommended: the coordinator, inline
   Why: <one line: no gate agent registered>
3. Where do the checks run?
   Choices: on this machine / on a dedicated gate box (pick one)
   Recommended: on this machine
   Why: <one line: no second machine>

Reply "yes to all", tell me what to change (for example "2: a gate agent"), say "not sure about 2", or ask "explain 2".
```

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: gates_merger, gates_runner, gates_box.

Show the matching "In plain terms:" lines (topology, merge king, gate box) above the rows that first use them. Write
`answers.topology`.

Write the merge king's entry in `orchestration.merge_kings` for the merge target (the branch changes land on; default
the repository's default branch). That key is a fleet map that `thrum config set` takes only whole:

1. Read it with `thrum config show orchestration.merge_kings --json`; its `value` is the map.
2. Change the one entry for the merge target.
3. Write the whole map back with `thrum config set orchestration.merge_kings '<JSON>'`.

Never edit `.thrum/config.json` by hand. Then append a row to `.thrum/policy/installed.md` of kind `config-write`, with
target `orchestration.merge_kings[<target>]` and `prior` set to that entry's earlier value, or `absent`.

Also write these for `project-gate-setup`:

- `runner`: the agent name of the agent that runs the gates, or `gate_agent` when the coordinator sends each gate to a
  gate-runner agent;
- `gate_box`: `local` when there is no dedicated gate box, or the name of the dedicated gate box;
- `merge_king: {"from": "orchestration.merge_kings"}`.

## Step 4: Defaults

Show the five defaults as the third block, in the form of `resources/question-blocks.md` of project-onboarding: at most
seven rows, one row per default, with a plain label, the default as `Recommended:` and its reason as `Why:`. A pick row
names its kind in its `Choices:` line; the landing-count row is free text and has no `Choices:` line. The `Key` column
below is for the agent: what the owner is shown is the default and its reason, never the key. When the Step 1 answer to
the batch-race row is `no`, skip the two batch rows (rows 2 and 3 below). The owner keeps or changes each one:

```text
Block 3 of 3: Defaults

1. When a change touches concurrency, race the whole suite or only that change's own tests?
   Choices: only the change's own tests / the whole suite on every landing (pick one)
   Recommended: only the change's own tests
   Why: per-landing speed
2. How many landings between batch races on the trunk tip?
   Recommended: 5
   Why: catches races without slowing landings
3. Should anything deploy without a green batch race?
   Choices: no, nothing deploys without one / yes, deploys do not wait (pick one)
   Recommended: no, nothing deploys without one
   Why: correctness
4. What happens to the gate evidence after the verdict?
   Choices: delete it / keep it (pick one)
   Recommended: delete it
   Why: no repo noise
5. Can a finding with no failing test or reproduction block a change?
   Choices: never blocks / may block (pick one)
   Recommended: never blocks
   Why: stops opinion-driven blocking

Reply "yes to all", tell me what to change (for example "2: 10"), say "not sure about 2", or ask "explain 2".
```

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: gates_per_landing_race, gates_batch_every, gates_deploy_needs_batch, gates_evidence, gates_unmeasured_block.

| Default | Reason | Key |
|---|---|---|
| no full race on every landing; race only the change's own tests for concurrency changes | per-landing speed | `per_landing_race: concurrency_only` |
| batch race every 5 landings on the trunk tip | catches races without slowing landings | `batch.every_n_landings: 5`, `batch.cmd` |
| nothing deploys without a green batch race | correctness | `batch.required_for_deploy: true` |
| gate evidence is deleted after the verdict | no repo noise | `retention_paths` |
| a finding with no failing test or reproduction never blocks | stops opinion-driven blocking | `policy.unmeasured_findings_block: false` |

Each default the owner changes is appended to `answers.rulings` as `{id, date, trigger, rule, applies_to, from}` with
`applies_to: coordinator`.

## Step 5: Ratchets

Build the candidates from `answers.burn_down` and `answers.ratchet_candidates`. Each runs as an `always_run` lens. Step 5
is offered when either list is non-empty, or `answers.inventory` holds a `pending` ratchet record, under both profiles.
Offer the found ratchet scripts first, through this block:

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

On a yes, append the ratchet to `answers.ratchet_candidates`. Each one becomes a `ratchets[]` entry for
`project-gate-setup`: `detector_cmd` runs the owner's script at its own path from the repository root, and
`baseline_file` is the owner's ceiling file.

## Step 6: Generators

Run `project-gate-setup`, and `project-hotpath-gate` only when `tiers.hotpath_lens` is `true`. Before this step, list the
gate commands and hooks the inventory found, by where each came from, and offer them through the block in Step 5 (the
`gate-command` and `hook` records). Hand the decisions to `project-gate-setup` through `answers.inventory`; it writes a
lane for each record brought in.

## Step 7: Validate

Before any command runs, show this line once:

> Ask: Next I run each of these commands once to check that it works: <commands>. Some may be slow. Say "ok" to run them all, or name any to skip; a skipped one is recorded as not validated.

Wait for the answer before any command runs.

A command the owner skips is not run, and it is appended to `answers.unvalidated_commands` (defined in
`resources/onboarding-schema.md` of project-onboarding).

Run each generated command once on HEAD, with a zero-match control: a selector that must match nothing, which has to
report nothing, beside the real one, which has to report something. Run each ratchet entry brought in once on HEAD the
same way, with a control. A command that fails is shown to the owner, never skipped.

## Finish

- Write `sections.S4` (`status`, `date`, `sha`) in `onboarding.json`.
- Write nothing outside `.thrum/policy/` apart from the `orchestration.merge_kings` entry.
