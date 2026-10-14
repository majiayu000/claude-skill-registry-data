---
name: ground-and-draft
description: Pull real customer evidence from the Amdahl corpus, freeze it, and draft GTM copy grounded in it. Use at the start of any GTM writing task — outbound email, sequence step, one-pager, call prep, website copy — BEFORE grading. Hands back a draft for a human to read.
---

# ground-and-draft

The first half of the loop: Write → **Ground → Draft** → (grade-and-report).

**This skill stops at a readable draft.** Do not chain straight into grading.
The gap between the two skills is where a human looks at the draft and decides
whether they agree with it, and that is where the judgment in this loop lives.
Automate the gap away and the exercise stops producing anything you could not
get from a load test.

## When it applies

Any time you are about to write GTM copy and want it grounded in what buyers
actually said rather than in what the model assumes they would say.

## Steps

1. **Write the intent** — one line: what you are drafting and for whom (persona,
   segment, and a real trigger or signal if this is outbound). Vague intent is
   what produces a draft that grades as "not commercial outreach".

2. **Ground — scoped the way the grade will be scoped.**

   ```bash
   export AMDAHL_KEY='...'              # Settings, then Developer, Create key
   bash scripts/ground.sh semantic "their pain, in plain language" \
     evidence/$(date +%F)-launch.json 25 \
     '[{"field":"speaker_type","op":"eq","value":"external"}]'
   ```
   - **`speaker_type: external` belongs on nearly every pull.** It is step 3
     below, enforced at retrieval instead of eyeballed after.
   - **Account scoping is `company_id` (`eq` / `in`)**, and only when the account
     is already in your corpus.
   - **On a cold account there is correctly nothing narrower than the cohort.**
     A company that has never spoken to you has no words to retrieve; a
     `company_id` filter would return an empty pull, and an empty pull is not
     grounding. Pull the cohort instead and attribute at that scope when you
     write — _"the eng leaders we talk to say"_ is supported, _"your engineers
     said"_ is not. That is the normal case for first-touch outbound, not a
     degraded one.
   - **Audience predicates need `mode filter`.** The semantic lane admits only
     `company_id`, `occurred_at` and `speaker_type`; `role_level`,
     `speaker_title`, `inferred_persona` and `industry` are refused there with
     `invalid_argument`. Run them as a second `filter`-mode pull into its own
     dated file — rows by predicate, complementing the similarity pull rather
     than replacing it. `GET /search/fields` lists the vocabulary per surface.
   - Prefer `semantic` (vector similarity, fast). The `fuzzy`/NL lane has a ~15s
     ceiling and returns `status=failed` on broad asks.
   - **A new pull is a new dated file.** The script refuses to overwrite one.
   - Scraped or competitor material is not customer evidence. Keep it in a
     separate directory and never feed it in as though a customer said it.

3. **Check who is talking.** The script prints a `speakers` breakdown. Unfiltered
   corpus retrieval does not filter on speaker side, and a meaningful share of a
   typical pull is your own team, not a buyer. A claim about what customers want
   that is grounded in your own rep's words is the quiet failure here — and it
   will still score, because the words are real and on-topic. Passing
   `speaker_type: external` in step 2 is the structural version of this check;
   read the breakdown anyway, because a pull that comes back thin after filtering
   is telling you the theme is yours, not theirs.

4. **Draft.** Their problem first, in their words. One proof point. No invented
   numbers, no invented peer names, no invented case studies — the eval checks
   specifics against the corpus and a fabricated one is worse than a vague one.
   Obey the artifact's own length and voice rules.

5. **Create the run folder.**
   ```
   runs/$(date +%F-%H%M)-<slug>/outputs/draft.md
   ```
   Record the evidence file and the prompt version in a `manifest.json` beside
   it. You will want to know which evidence produced which draft when the
   scorecards start piling up.

**Hand the draft to a human. Then run `grade-and-report`.**

## Freeze the evidence when you are comparing

Live search is right when you are producing work. **Frozen evidence is required
when you are comparing two versions**, because a second search returns different
quotes and any difference you measure could be retrieval rather than your edit.

Two ways to freeze:

- **Across drafting attempts** — the dated file this skill writes.
- **Across graded runs** — pass `evidence_from_run: "<run id>"` to `evals.run`,
  and the new run reuses the first run's quotes with no file to manage.
  `grade-and-report`'s `ab.sh` does this for you.

## Gotchas

- **Corpus grain.** One call fans out to many utterance rows. Count
  `DISTINCT parent_interaction_id` for anything you would call a "number of
  conversations" — counting rows over-counts by chat volume.
- **`search.fields`** (`GET /search/fields`) lists the filter vocabulary before
  you write typed predicates, so you are not guessing field names.
- **MCP sessions can drop mid-task.** `ground.sh` uses REST with retries, so a
  single blip does not lose the pull.
