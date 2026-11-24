---
name: spec-experiment
description: >
  Guide a person through a pre-registered experiment on their AI-agent workflow: write the design
  before any run, get it approved and hashed, run it, keep an honest log and cost ledger, then
  write the results against the rules fixed in advance. Use when the user says "run an
  experiment", "pre-register", "A/B test the agent", "compare prompts", "compare models",
  "does this prompt/model/workflow change actually help", "write up the experiment results",
  "fill my experiment timesheet", or "/spec-experiment". Works in any project. It records
  evidence and never decides what counts for any tax or grant scheme.
license: MIT
---

# Experiment

Answer "does this change actually help?" with a design that was fixed before the runs, so the
result can be trusted and shown to someone else. The `spec-driven-dev experiment` commands do
the bookkeeping (dated design, hash at approval, log, ledger, timesheet suggestions, results
scaffold). This skill does the thinking with the person.

## Project config (read first)

Load `.spec-driven.yml`: walk up from the current directory to the home folder, and the first one
found wins. If `{specs_dir}/team.yml` exists, read it first and let `.spec-driven.yml` override
it. This skill uses these keys:

- `experiments.dir`: where records live (default `experiments/`). It may be an absolute path
  outside the code repo. `--experiments=<dir>` overrides it for one command.
- `experiments.categories` (default `experiment`, `supporting`, `admin`) and
  `experiments.counted` (default `experiment`, `supporting`): timesheet categories and which of
  them count. These are the team's own choice. Never decide them yourself. The CLI records the
  category on each row; when summing time, count only the `experiments.counted` categories.

**No config?** Use the defaults and offer to save `experiments.dir` to `.spec-driven.yml`.

## Step 1: Where the records live

Say where the records will go (`experiments.dir`). If the team prefers records outside the code
repo, or the config says so, suggest an absolute path. Nothing in this skill writes to the code
repo's source. It writes only inside the experiments folder.

## Step 2: The question and the prior-art check

1. Get the question in one sentence, for example "Does prompt B finish the same tasks cheaper
   than prompt A?"
2. Ask why the answer is not already known. If the person expects "obviously yes" and cannot say
   why it is unknown, do not go on.
3. Ask for a prior-art check. Search the docs, papers and the project's own earlier results
   (`experiment ledger` output, old results notes). Write down what was found and what a
   competent practitioner would and would not know in advance.
4. If the answer is already known, say so plainly and stop. That is a good outcome.

## Step 3: Write the design

1. Run `spec-driven-dev experiment new <name>`. It creates a dated draft from the template in
   `references/design-template.md`.
2. Fill every section with the person. Replace every `{...}` placeholder. The approve command
   refuses while any remain.
3. Every number in the outcome rules (thresholds, run counts, what counts as a failed run) is
   fixed now, before any run. Ask "what result would change your mind?" and write it down.
4. Add harm controls when the change could make things worse elsewhere (quality, safety, cost,
   other tasks). If it cannot, say why in one line.
5. Build the decision table: each possible result, what it means, what happens next.
6. Estimate cost per run times number of runs. Use earlier ledger means when they exist, and
   say where each number came from.

## Step 4: Approval

1. Show the whole design to the person.
2. When they are happy, they approve it:
   `spec-driven-dev experiment approve <name> --by="<their name>"`. Use the name they give you.
3. Never approve on their behalf, and never invent a name for `--by`. The hash and the LOG line show any edit made outside `amend`, but plain files are not tamper-proof; keep designs under version control or a shared folder.
4. After approval the design does not change. A real change goes through
   `spec-driven-dev experiment amend <name> --reason="<why>" --by="<your name>"`, which logs the old hash, the new
   hash and the reason. Ask the person for the reason. Do not write it for them.

## Step 5: Runs

1. Run `spec-driven-dev experiment check <name>`. If it fails, stop and tell the person why.
2. State the cost (runs times estimate) and ask for an explicit go. No go, no runs. A go for one
   batch is not a go for the next one.
3. Run through `spec-driven-dev risk-eval ... --experiment=<name>` or the team's own harness.
4. A failed run (crash, timeout, tool error) is re-run and excluded from the counts. Say how many
   were excluded. Never drop a run because its result is inconvenient.
5. Record notable events with `spec-driven-dev experiment log "<text>"` (a run started, a run
   failed, a cost surprise, an amendment). Log what happened, plainly.

## Step 6: Results

1. Run `spec-driven-dev experiment ledger`, then `spec-driven-dev experiment results <name>`.
   It writes a note pre-filled with the rules, decision table, runs and costs.
2. Write the reading with the person, following `references/results-template.md`: find the
   decision table row the numbers fall in, and quote it.
3. If the result fits no row, or the mechanism contradicts the row, say so plainly. Do not follow
   the row's "next" anyway, and do not quietly rewrite the table.
4. Report what went against the hypothesis as clearly as what supported it.

## Step 7: Time (optional)

1. Offer `spec-driven-dev experiment timesheet --since=<date>`. It lists suggested work spans
   built only from the person's own typed messages, with the chosen gap and the 60-minute rule
   side by side. It reads only the experiments folder and the current folder by default;
   `--repos=a,b` adds named workspace repos, `--all-repos` adds all plus the workspace root.
   Each span shows how many messages came from which folder.
2. Present the suggestions. The person confirms, edits or drops each one. `--write` appends them
   as `unconfirmed`. Only the person confirms.
3. Never raise hours above what the messages show. Never count agent run time.
4. If asked to inflate, round up or invent time, decline and explain that records must reflect
   real work.

## Rules

- Never fabricate a result, a run, a cost or a time.
- Never write a verdict the numbers do not support. The results scaffold has empty slots for the
  reading. Fill them with evidence only.
- Never start paid runs without the person's explicit go for the stated cost.
- Never approve a design for the person, and never run an unapproved or edited design.
- Never edit, delete or reorder lines in `LOG.md`. Only append with `experiment log`.
- Never change a design after approval except through `amend`.
- Never edit recorded timesheet rows.
- Never name a company, product, country or tax or grant scheme in the design, results or log
  unless the person put it there. Do not judge eligibility for any scheme.
- Times are UTC with a trailing `Z`.
