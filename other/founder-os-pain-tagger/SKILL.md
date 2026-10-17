---
name: founder-os-pain-tagger
description: FounderOS pain tagger and pain-log quality check. Ranks raw posts from a watering hole with Laya so the founder reads the painful ones first (Sales Safari pre-filter), and checks the founder's pain log for quotes that are not pain, unsourced or unclustered quotes, duplicates, thin job clusters and too few watering holes. Triggers when a founder at stage 2 pastes posts or a thread to mine, asks "which of these are pain", "is my pain log good enough", or before the stage 2 gate.
plugin: behalfbot-founder-os
enabled_when: "chassis.config.yaml modules.founder-os.enabled == true"
type: auditor-skill
stage: 2
question_set: pain-tagger
---

# Pain tagger and pain-log check

Sales Safari is Amy Hoy and Alex Hillman's method (30x500). Use their terms and
send the founder to their material. The founder reads their audience's own
words, in the places that audience already talks, and logs the pain in quotes.
Laya's job is the boring half: reading every post so the founder and you only
read the ones worth reading.

## When to run

- **Ranking:** the founder has a batch of posts or comments from a watering
  hole, as a JSON list of `{"id", "text"}`.
- **Log check:** the founder has logged pains with `add_pain` and wants to know
  if the log is good enough, or is heading to the stage 2 gate.

## Laya pass

Ranking:

```bash
python3 "$FOUNDER_OS_DIR/scripts/audit.py" pain-tagger --input posts.json --lang <en|pt|...> [--jobs jobs.json]
```

Log check:

```bash
python3 "$FOUNDER_OS_DIR/scripts/audit.py" pain-log --founder-id <founder_id> --lang <en|pt|...> --record
```

Pass `--lang` every time. What the question set does with it comes from the
measured run in new-jaxity #603:

- `is_pain` runs on the `english` checkpoint for English text (AUC 0.78). On
  the `multilingual` checkpoint it was at chance (AUC 0.53), so for any other
  language its `trust` is `chance`, ranking falls back to
  `money_or_workaround`, and a quote is never flagged as not-pain on that
  basis. You read those for pain yourself.
- `money_or_workaround` runs on `multilingual` for every language (AUC 0.84).
  Use it to fill the "what they buy, what they built" column.
- `intensity` and `pain_category` are advisory. The category options are the
  founder's own job clusters, passed as `--jobs` for ranking and taken from the
  log for the check. Do the clustering yourself; Laya's pick is a hint.
- Long posts are split into chunks that fit the checkpoint and the answer is
  taken from the strongest chunk, so a pain at the end of a long post is not
  cut off. `excerpt` shows which chunk carried it.

## Claude pass

**Ranking.** Read the top of the list, not all of it: roughly the top 30 or the
first quarter, whichever is smaller. Pull quotes in the author's own words. Say
which posts Laya put high that are not pain (launches, advice, opinions about
"people") so the founder learns the difference. For each quote you keep, help
the founder `add_pain` with `source_url`, `watering_hole` and a `job`.

**Log check.** Go through the `issues` per quote and the `log` block:

- `not_a_pain`: the quote reads as news, advice, a launch or an opinion. Check
  it; drop it or replace it with the author's actual complaint.
- `not_a_pain_unverified`: Laya's is_pain was at chance for this language.
  Judge it yourself.
- `no_source_url`, `no_watering_hole`, `no_job`, `duplicate_of:`, `too_short`.
- `thin_jobs` (fewer than 3 quotes), `too_few_watering_holes` (fewer than 3),
  `unclustered`, and `money_or_workaround_share`: a log where nobody has paid
  or hacked around the pain is a warning sign about the pain's size.

End with a verdict: is this log strong enough to cluster into jobs, and what is
the single most useful thing to go and collect next?

## Without Laya

If `mode` is `claude-only`, ranking returns the posts unscored: read them all
if there are few, or ask the founder to cut the batch. The log check still runs
every structural check (sources, jobs, duplicates, counts); only the Laya
checks are missing. Judge pain yourself and say in one line that Laya was
unavailable. Write no labels.

## Label capture

Ranking writes no labels, because raw posts are not ledger rows. Labels are
written by `pain-log --record`, one per quote and question, on that quote's
`pains` row. Ask the founder to confirm the tags you disputed and record them:

```bash
python3 "$FOUNDER_OS_DIR/scripts/labels.py" accept --founder-id <id> --by <founder_id> <label_id> ...
python3 "$FOUNDER_OS_DIR/scripts/labels.py" reject --founder-id <id> --by <founder_id> <label_id>
python3 "$FOUNDER_OS_DIR/scripts/labels.py" reject --founder-id <id> --by <founder_id> <label_id> --value 2
```

`is_pain` corrections on English text are the labels the fine-tune needs most.
The job category is not recorded: its options are this founder's own, so it
cannot be replayed as a training example. The cross-founder export is
operator-only.

## Ledger writes

- `pains` rows, by the founder with your help, only from quotes that survive.
- Labels from `pain-log --record`; corrections from `labels.py`.
- One `audits` row per quote you judged a problem:
  `record_audit.py --table pains --id <pain_id> --auditor claude --check pain_quality --verdict flag|fail --findings "<why>"`.
