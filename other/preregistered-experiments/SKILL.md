---
name: "preregistered-experiments"
description: "Running paid or learned-model experiments in this repository: plan first, jobs on Hugging Face or GitHub runners, cost caps, restart safety, behavior audits, and the failure modes met so far."
---

# Preregistered experiments

The rules are in `experiments/METHOD.md`: plan merged before the run, one factor at a time, paired designs, held-out partners, test sets used once, bootstrap intervals, and nulls reported. This skill adds the practice that made those rules work, and the ways runs went wrong.

A deterministic enumeration needs its rules, domain, counter and coverage check. Use a participant protocol when the question turns on what a player actually does. For example, counting losses after a pairs-first move cannot establish how often people choose that move.

## Running

- Launch with `experiments/hfrun.py` at a pushed commit. It clones that commit, installs one dependency group, runs one module and writes a manifest (commit, hardware, return code, seconds). Outputs go to the private dataset, and summaries go to the game's `results/`.
- Free CPU work that splits into pieces runs as a matrix on GitHub Actions (`.github/workflows/experiment.yml`). Paid GPU work runs on Hugging Face Jobs.
- **Pilot first.** One short job measures speed and setup time, and the main runs are sized from it to fit the cap. Report setup time against run time.
- **Cost.** Each plan states an expected cost and a hard cap. Every job gets a timeout. Language-model calls are metered as the provider's reported tokens times the listed price, because providers return tokens but not cost.
- **Hardware queues.** A cheap GPU can wait over an hour. Switch hardware by a dated amendment written before the main runs, not after.

## Restart safety

- Before relaunching anything, list the jobs and check the dataset for outputs that already exist.
- Never rerun a test job whose outputs exist, since the test set is scored once. If a job failed after sending calls, record how many were sent, and score only the rerun.
- Commit work in small pieces, so a lost session loses little.

## Checks before believing a result

- **Agreement test.** A learning environment must agree with the repository's own rules engine on legal moves and scores over thousands of random games before any training. Replay the evaluation games in the reference engine.
- **Behavior audit.** Report what the agents do, not only their scores: who hints, plays and discards, and how often an option is picked by its position in a list.
- **Shortcuts.** A policy trained to pick from a list learned to pick the first item. Shuffle option order, and check the share of picks by position.
- **Repeat check.** Send a sample of prompts again at temperature 0. Report how often the action changed; providers are not deterministic.
- **Empty and malformed replies.** Count them per split. A provider returned empty replies on 28% of test calls and 0.05% of validation calls a few hours earlier, so recheck the result on the boards with no empty reply.
- **Sensitivity.** Rerun the analysis with key constants halved and doubled. Analyses added after seeing the test scores are labeled exploratory.

## Seeds and random numbers

- Common random numbers are right for comparing arms: the same boards, deals and seeds give a paired difference with a smaller interval.
- They are wrong when simulations are meant as independent checks of different exact values. Three Tenzi simulations seeded game i with i, so they were not three checks; each now has its own seed.
- Never choose a seed by its result. Use fixed seeds (0, or 1 to 5) and print them.

## Data terms

- Commit aggregates only. Per-item strings derived from a dataset whose license is unclear can reconstruct it, and a pushed commit stays reachable by its SHA even after a rewrite.
- Record the license of every dataset and model in the README before the first run.

## Per-unit records

A result that is only a mean cannot be diagnosed. Keep one row per arm and evaluation unit (a board, a deal or a turn), so that a single unit can be opened and every number on it traced. `codenames/diagnose_records.py` holds the schema (`SCHEMA`) and the code; other games can copy it.

- **Fields.** Experiment, split, arm, task, unit id (`seed:index`), board seed and index, training and call seeds, the SHA-256 of the input (the board text or the prompt), the board, the chosen action, the top-k candidates with the chooser's scores, each scorer's exact value, each guesser's first-pick distribution, the legality level and the related board words, and for a model call the SHA-256 of the raw reply, the provider, the model, the latency, the tokens and the cost. A field a run does not have is null.
- **Writing.** A future run builds rows with `record(...)` and writes them with `write_parquet(rows, path)` (DuckDB, in the `codenames` group) to the private dataset as `runs/<experiment>/records/<job>.parquet`, beside the raw replies. Values are written unrounded. A row's reply hash lets anyone check a copied reply against the log.
- **Reading.** `load(paths)` returns one DuckDB relation over those files and the results already committed (C3, C4, C6, C7 and C10). The committed ones hold a subset of the fields: picks and exact values, and the language models' played-out values where they exist. C3 committed no clues; `codenames.diagnose_c3` regenerates them from the committed weights and checks every pick against the committed per-board value.
- **Diagnosing.** `codenames.diagnose` reads the records: `case <experiment> <board>` writes a case file (the board, every arm's clue and its legality, each guesser's first picks, and the turn value split into the chances of each way the turn ends), `slices` gives paired differences by slices fixed before they are computed, with Holm's correction, and `disagree` lists the boards where two kinds of guesser disagree most, with case files for the first ten. All of it is exploratory.
- **A failure found this way.** The clue filter of every Codenames experiment forbade only board words and substrings, so forms of a board word (residency with RESIDENCE) passed. Picks chosen by their value to embedding guessers named such forms on 28% of boards, against 7% for the first choice. Check the legality of the chosen actions, not only of the candidate list, before believing a giver result, and fix a filter by a dated amendment before any data is collected.
