---
name: onboarding-coupling
description: "Use when an owner wants to know which parts of the code change together and wants rules that keep changes small - first-time setup, a repository whose changes keep re-testing everything, or a gate setup that needs to know whether tests can run only for what changed. Measures the import graph and the recent git history, writes .thrum/policy/coupling.md, and records the keep-separate rules the owner picks. Runs as one part of project-onboarding and on its own."
---
<!-- markdownlint-disable MD013 -->

# onboarding-coupling

Measures how the code is coupled, reports it, and records the rules the owner picks to keep changes small. It writes
`.thrum/policy/coupling.md`, the measurement script in `.thrum/policy/coupling/`, and one marked block in
`.thrum/policy/philosophy.md`.

## Opening offer

Show this offer before any other question.

<!-- onboarding:offer -->
> Say: This part measures which parts of your code change together, from your recent git history, and suggests rules that keep changes small. It reads that history first, then asks you to pick the rules you want enforced.
> Ask: Do this part now, or skip it for now? If you skip it, running project-onboarding again offers it again.
<!-- /onboarding:offer -->

"Skip it for now" records `sections.S3.status: skipped` with `reason: owner` in `.thrum/policy/onboarding.json`, writes
`coupling.changed_scope_viable: false` with `coupling.source: "owner-skip"`, and ends the section. "Do it now" goes on.
Under the Solo profile the default answer is "skip it for now", recorded with `reason: profile` and
`coupling.source: "solo-default"`. When this skill runs alone the same offer is shown, and a skip never changes a record
that is already `done`.

When `.thrum/policy/onboarding.json` is absent, this skill creates `.thrum/policy/` and the file, and leaves `profile`
unset so it reads as `team`. It never reads the licence.

## History analysis

When .thrum/results/history-analysis.md is absent or stale, follow
history-analysis.md in the project-onboarding resources before the first block.

## Step 1: Build the graph

Build the import graph of the repository with test imports included: a test that imports another unit makes that unit
part of what the test depends on, and a graph of production imports alone hides the loops tests create. Use the
repository's own tool when it has one. Otherwise write a small script for the language in use. Either way, save the
script in `.thrum/policy/coupling/`, so a later measurement is comparable.

Check the method with a control: the production-only graph must show none of the loops that the full graph shows, or the
loops come from the script and not from the code. `resources/coupling-report-template.md` has a worked example of the
blocks below.

## Step 2: The report

Write `.thrum/policy/coupling.md` from `resources/coupling-report-template.md`, with five blocks under these headings:
"Inventory", "Cycles", "Impact distribution", "Size outliers" and "Invisible coupling".

Then replay the last 60 commits: for each one, take the units it changed and count the test units that depend on them,
directly or through imports. Changed-scope lanes are viable when the median change re-tests under 25% of the test units
and fewer than half of the changes fall back to a full run. Write the answer to `coupling.changed_scope_viable` in
`.thrum/policy/onboarding.json`, with `coupling.source: "measured"`, and show the owner the two numbers it rests on
before asking them to confirm it.

If the repository has fewer than 60 commits, replay all of them and say how many there were.

## Step 3: Questions the graph cannot answer

Ask these four as one block, following `resources/question-blocks.md` of project-onboarding, and write the answers
into `coupling.md`. Each recommended answer and its `Why:` line come from the coupling report's evidence. A row the
report has no evidence for takes the fallback line from `resources/question-blocks.md`.

When the history read was skipped or found nothing,
put the History: line under every fallback line, as question-blocks.md says.

```text
Block 1 of 1: Questions the graph cannot answer

1. Does any code look up the repository root, so that it behaves differently from another checkout?
   Choices: yes / no (pick one)
   Recommended: <the answer the report's evidence supports>
   Why: <one line naming that evidence>

2. Do tests share a database, a port or a directory?
   Choices: yes / no (pick one)
   Recommended: <the answer the report's evidence supports>
   Why: <one line naming that evidence>

3. Do tests start other programs that this graph cannot see?
   Choices: yes / no (pick one)
   Recommended: <the answer the report's evidence supports>
   Why: <one line naming that evidence>

4. How long may one test lane run before you call it too slow?
   Recommended: <a time the report's lane timings support>
   Why: <one line naming that evidence>

Reply "yes to all", tell me what to change (for example "4: 10 minutes"), say "not sure about 3", or ask "explain 3".
```

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: coupling_repo_root, coupling_shared_resources, coupling_hidden_programs, coupling_lane_limit.

## Step 4: Keep-separate rules

Offer one candidate rule for each loop, outlier and invisible coupling the report found, as one pick-several row of a
block in the `resources/question-blocks.md` form. Its Choices line lists the candidates, and the candidates the report
supports are the Recommended set. Do not add a rule the owner did not pick.

Record how each answer was given in answers_source, and a note the owner added in answers_notes, under these keys, in
row order: coupling_keep_separate.

In stealth mode, leave out the words about being committed with your code from every notice.

- Write each picked rule into the block between `<!-- onboarding:S3 -->` and `<!-- /onboarding:S3 -->` in
  `.thrum/policy/philosophy.md`. Read the file, replace only that block or append it, and write it back. If the file does
  not exist, do not create it: tell the owner to run project-philosophy first, and stop this step.
- Append each rule a script can detect to `answers.ratchet_candidates`.
- Append each picked rule to `answers.rulings` as `{id, date, trigger, rule, applies_to, from}`.

## Step 5: The work list

The list is the same on both licence tiers.

1. Show the owner the whole list first: each fix that would remove a loop or an outlier, in the order that shrinks the
   re-test set most.
2. Ask before writing any issue:

   > Ask: May I add these fixes to your issue tracker, one issue each with a step to measure again afterwards?

3. On yes, read the effective tracker with `thrum config show tracker --json` (its `value` is `beads` or `native`; one
   always resolves), and create one issue per fix with that tracker's command (`bd create`, or `thrum issue add`), each
   with a step to measure again.
4. On no, or when the tracker command fails, write the list as a checklist in `coupling.md`.
5. Either way, write the destination to `coupling.work_list` (`tracker` or `coupling.md`), and append a row to
   `.thrum/policy/installed.md` for each issue created (kind `tracker-issue`, target `<tracker>:<id>`). Undo lists these
   rows and never removes the issues.

## Finish

- Write `sections.S3` (`status`, `date`, `sha`) in `onboarding.json`.
- Write nothing outside `.thrum/policy/` apart from the tracker issues.
