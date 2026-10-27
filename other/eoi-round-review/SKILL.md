---
name: eoi-round-review
description: >
  AI-review a marketplace EOI round's responses on its labs criteria and write a shortlist doc. Needs the round slug.
disable-model-invocation: false
---

# EOI Round Review

The AI first pass on a marketplace round. It reads every response, scores each on the
round's evaluation criteria (saved on the round in labs, 1–10 per criterion), adds what
labs already knows about each organisation (rounds it answered before, what it actually
delivered on Connect), and writes one **AI review per response into labs**. Every statement
in a review is a **claim** that points at the evidence it rests on: the exact words in the
response, an answer that is silent on the point, or labs history or a web source. People
then review in labs, starting from those AI reviews and clicking a claim to see its
passages highlighted in the response (see § What happens next in labs). Before anything
is written to labs, a separate agent calibrates the scores and outcomes across the whole
pool, because each scoring batch otherwise picks its own best. It also writes two reports:
the internal shortlist a programme team acts on (who is recommended, in which role, why,
what to ask them first, who is the backup), and a de-identified version for funders and
partners. Across several rounds the internal one adds a short cross-round section. Every
outcome and flag is a word from labs' defined list (§ Outcomes and flags).

The criteria are the round's, not this skill's. EOI forms go out without a published
evaluation framework, so the criteria are written after the submissions arrive, by
`eoi-criteria-proposal`, approved by a person and saved on the round. This skill never
scores against a private rubric of its own: an AI review and a human review of the same
response must be scored on the same criteria to be comparable.

The yardstick is the team's own hand-built shortlist for the 2026 ULAB scoping EOI ("EOI
LLO recos" in the CGD Lead Research RFP doc): a bottom line, one table of the recommended,
a short note on each, who to keep in view, and who is not recommended with one reason each. Neal's R pipeline
(`dimagi-internal/connect-interviews-analysis`, `llm/eoi_*`) produces exhaustive reports
with good quotes that are too long to act on. This skill keeps the quotes and drops the
length.

**Responses are confidential to Dimagi.** Applicants' answers are never shared with other
applicants or outside Dimagi. The internal report goes in ACE's Drive area for Dimagi
people only (`@dimagi.com`, `@dimagi-ai.com`, `@dimagi-associate.com`). The external
report carries no organisation or person names and no applicants' words, and passes a
de-identification scan (step 13) before it is published. Both are published with sharing
off; the requester decides who receives each. Contact names, emails and phones are not
read (`include_contacts` stays false) and never appear in either report, or in any field
of a labs review, including a claim's `text` or a `quote`. Reviews
in labs are visible only inside the round's owner org (Dimagi), but treat every field as a
record others will read: cite the organisation's answers, never a person.

## Inputs

| Source | Artifact | Used for |
|---|---|---|
| Requester or `current_page` | round slug(s), e.g. `ulab-scoping-2026` | which rounds to read |
| connect-labs | `marketplace_rounds_list(slug=…)` | title, deadline, countries, questions, announcement link |
| Drive | the round's announcement doc (`announcement_url`) | what was asked: activities, priority areas, budget and rates, roles |
| connect-labs | `marketplace_round_responses(slug=…)` | every submission's answers (each `{question_id, question, answer}`; claims cite `question_id`), its `response_id` and matched org; `round.evaluation_criteria` and `round.rubric_version` |
| connect-labs | `list_reviews(response_id=…)` | reviews already on each response (an earlier AI pass, human reviews built on it) |
| connect-labs | `marketplace_orgs_get(slugs=…)` | each matched org's delivered and applied programmes, year established, team size |
| Requester (optional) | the team's own shortlist, for comparison | the agreement table (step 11) |

## Products

- **One AI review per response in labs**, written with `create_review(kind="ai", …)`:
  1–10 per criterion, `claims` (each criterion's reason, the strengths, the concerns, each
  with the passages it rests on), questions to ask, flags from the defined list, an
  outcome (key `pick` / `backup` / `waitlist` / `pass`, shown as Recommended / Recommended backup /
  Waitlist / Not recommended; § Outcomes and flags) and provenance. Labs fills the per-criterion notes, strengths and
  concerns from the claims, and computes the overall score from the criteria scores and
  the round's weights. Re-running replaces ACE's earlier AI review of that response.
- `calibration.md`, written by the calibrating agent (step 8): the score distributions,
  every change with before → after and why, the spot-check table and the final slate, plus
  `calibration.json`, the same changes as data. Working files; the internal report
  summarises them.
- `rubric-health.md`, written in step 9 by `rubric_health.py` and the agent reading it: how
  well the rubric served this pool, with keep / reweight / split / drop / add
  recommendations, each with its numbers. It goes in the internal report and, when it
  recommends a change, to `eoi-criteria-proposal` for the next version.
- **The internal report**, a Google Doc published with `gdoc-writer` under
  `Projects/<project>/` (the project is the round's programme or the requester's project
  name), sharing off. Dimagi only. It is the doc the round links to as its summary, and it
  has two tabs:
  1. **Overview**, under ~2 pages, written as an analyst making the case: the outcome of
     the review, not how it was done. Bottom line, one section per place (who, why them,
     what to settle before contracting, the backups), the program-wide questions the pool
     raised, what to ask every shortlisted applicant, what the next call should ask
     differently, and the next step in labs. No criteria names, weights, scores, version
     labels or flags.
  2. **Review details**: how it was scored (criteria, weights, `rubric_version`, outcome
     rules), the version comparison, calibration, rubric health, pool coverage and
     quality, the comparison with the team, the all-organisation table, and one ≤120-word
     entry per submission (outcome, role fit, cost, strengths and concerns citing the
     answer, questions to ask). Step 10 lists the sections.
  The doc opens with a link to the round page in labs,
  https://labs.connect.dimagi.com/labs/marketplace/rounds/<slug>/, where reviewers verify,
  agree, edit or add their own reviews. The doc is a summary of the AI pass; labs holds the
  reviews.
- **The round's summary link in labs**: once the internal report is published, step 13
  links it on the round with `marketplace_round_summary_set(slug, url)`, so the round page
  shows it to the round's owner org (Dimagi). The owner's approval to write the report
  covers this link; no separate ask.
- **The external report**, a de-identified Google Doc for funders and partners, published
  the same way with sharing off after the step 13 scan passes: no organisation or person
  names, no verbatim quotes, figures for the pool only, places only at the level of the
  call's priority sites or regions.
- The three links (both reports and the round page), in the reply to the requester, with
  who each report is for. No report is pasted into chat or email.

## Process

**On a connect-labs page** (the caller envelope's `site` block names `connect-labs` — the Connect Labs agent panel, whoever asked, ACE's owner included): every labs read and write below goes through canopy's `site_tools` / `site_call`, as the person who sent — never the native `connect-labs` MCP, which is unauthenticated there. See [`skills/_labs-on-a-page.md`](../_labs-on-a-page.md).


1. **Resolve the round(s).**
   - From the canopy panel, read `current_page`. A `labs-marketplace://rounds/<slug>` page
     names the round, so don't ask for it.
   - Otherwise take the slug(s) from the request, or match the name against
     `marketplace_rounds_list()`. If two rounds could be meant, ask in the chat.
   - Read each round with `marketplace_rounds_list(slug=…)`. If `applications` is 0 and
     the round has a response sheet, it has not been ingested. The usual cause is the
     sheet not being shared with the labs service account. Say so and stop: a review of
     zero responses is not a finding.

2. **Read the call itself.**
   - Open `announcement_url` with `drive_read_file` (or `read_personal_drive_doc` if the
     service account can't see it).
   - Pull out what the work is, the units and their rates, the total budget, the priority
     geographies, the roles being filled (e.g. "household survey LLO" vs "value-chain
     lead"), and the timeline.
   - Every score and the recommendation are checked against these facts, not
     against what applicants say about the call.

3. **Require the round's criteria.**
   - Read `round.evaluation_criteria` and `round.rubric_version` from
     `marketplace_round_responses(slug=…)` (step 4 makes this call; make it now if
     needed).
   - **If the criteria are empty, run `eoi-criteria-proposal` first** and come back once
     the requester has approved and saved a set. Do not invent a rubric here, and do not
     score against criteria that exist only in this conversation. If the requester brings
     their own criteria, they go through `eoi-criteria-proposal` too, so they are tested
     against the pool and saved on the round.
   - If the criteria exist but the requester questions them, or they plainly do not fit
     the pool (a criterion every response would score the same), say so and offer
     `eoi-criteria-proposal` before scoring. Replacing them later invalidates this pass.
   - Save the round to `criteria.json` and run
     `python3 "${CLAUDE_PLUGIN_ROOT}/skills/eoi-criteria-proposal/check_rubric.py" criteria.json`.
     If it does not print `OK: rubric is explicit` (anchors at 1/3/5/7/10, a Silent rule,
     outcome rules in `criteria_basis`), say which parts are missing and offer
     `eoi-criteria-proposal`. Scoring on a rubric without anchors or outcome rules is
     possible, but each batch then reads the bands and settles the slate its own way; say
     so in the internal report's "How we scored".
   - Show the criteria (name, weight) in one short list before scoring, with the
     `rubric_version` the reviews will carry, and the outcome rules.

4. **Pull every response, without contacts.**
   - Call `marketplace_round_responses(slug=…)`. Leave `include_contacts` false: the
     review never needs a person's address.
   - If `truncated` is true, say so in the doc.
   - Keep each answer's `question_id` and its `answer` text exactly as returned. Claims
     cite answers by `question_id`, and every `quote` is checked against that `answer`
     text, so never pass subagents a cleaned-up, summarised or re-wrapped copy.
   - Group duplicate submissions (the same org name, or the same matched `org_slug`, more
     than once). Review the latest and note the duplicate. Never count one org twice. Each
     duplicate still has its own `response_id`; write the AI review on the latest, flagged
     `templated` (the same response submitted twice), with a `flag` claim noting the
     earlier submission.

5. **Add what labs already knows about each organisation.**
   - For every matched `org_slug`, call `marketplace_orgs_get` (≤100 slugs per call).
   - Use `delivered_programs` (what they actually ran on Connect) and `applied_programs`
     (what they asked for). A strong record on Connect is evidence. A string of
     applications with no delivery is a pattern worth one line.
   - An unmatched submission has no history here. Say "no labs record", not "new".

6. **Review each response on the round's criteria.**
   - Split the responses into batches of about 8 and give each batch to a subagent, in
     parallel. Write the files to a working directory (the session scratch dir) and pass
     each subagent the paths:
     - `batch-<n>.json`, the responses exactly as labs returned them, in this shape (the
       shape `check_claims.py` reads):

       ```
       [{response_id, org_name, org_slug, earlier_submissions, labs_history,
         answers: [{question_id, question, answer}]}]
       ```

       `earlier_submissions` lists this org's other responses in this or earlier rounds
       (step 4), `labs_history` what step 5 found (or null: "no labs record");
     - `criteria.json`, the round's saved criteria list exactly as labs returned it (ids,
       names, weights, scoring guides);
     - and, in the prompt itself, the call facts from step 2.
   - The brief includes these rules (§ Claims and evidence below is part of it; paste it
     in), and the instruction to write its reviews to `out-<n>.json` and **run the checker
     until it prints `OK: every claim checks` before returning**:

     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/skills/eoi-round-review/check_claims.py" \
       batch-<n>.json out-<n>.json criteria.json
     ```

     It mirrors labs' save-time check (lowercase, collapse runs of whitespace, ‘’ → ',
     “” → ", – and — → -, then a substring test) and also checks that every `question` is
     a real `question_id` of that response, claim ids are unique, every criterion has a
     1–10 score and at least one `criterion:<id>` claim, the outcome is one of the four
     outcome keys with an `outcome` claim, every flag is on the defined list (labs refuses
     any other) with a `flag` claim that names it, every web cite has a url, every
     response in the batch was reviewed, and, when the round's guides are anchored, that
     every criterion claim names the anchor nearest its score. It prints each problem and exits 1, so a
     subagent fixes and re-runs; a quote is fixed by copying the words from the answer,
     never by loosening the claim's cite to make it pass.
   - Each subagent returns `out-<n>.json`: a list with one entry per response,

     ```
     [{response_id, org_name, criteria_scores, claims, outcome, role,
       cost_per_site_usd, cost_note, ask_next, flags, one_line}]
     ```

     where:
     - `criteria_scores`: `{criterion_id: 1–10}` for **every** criterion on the round,
       scored against that criterion's `scoring_guide` anchors: find the anchor the
       answer matches, then move a point up or down for what it adds or lacks; an answer
       that says nothing gets the Silent score. Ids exactly as saved;
     - `claims`: the review's statements, in the shape in § Claims and evidence:
       - at least one `about: "criterion:<criterion_id>"` claim for **every** criterion
         scored, giving the reason for that score and naming the anchor it was read
         against (§ Claims and evidence: the text starts `Anchor <n>: ` or `Silent: `);
       - 2–4 `strength` and 2–4 `concern` claims;
       - a `flag` claim for each flag, its text starting with the flag's label (or key)
         and saying what in the response raised it: `Long but thin: every answer
         restates the question and names no site.`;
       - one `outcome` claim giving the reason for the provisional outcome;
       - the role it suits (or neither) and the cost per unit go in a strength, concern or
         outcome claim, citing the answer they come from;
     - `role`: which role it suits, or neither (for the doc);
     - `cost_per_site_usd`: their quote converted to USD per site (or per the call's own
       unit when the call is not priced per site), or null when not given;
       `cost_note`: the unit, what was quoted and how it was converted;
     - `ask_next`: 2–3 questions to ask before shortlisting;
     - `flags`: keys from the fixed list in § Outcomes and flags (`unsupported`,
       `inconsistent`, `templated`, `padded`, `incomplete`, `out-of-scope`, `capacity`,
       `cost`, `early-start`, `safety`), or `[]`. **Labs refuses a review with any other
       flag**, and `check_claims.py` refuses it first: there is no "another label when none
       fits". A flag is something to check, never a penalty (the scores do that). Never
       flag "AI use" as such; flag what the answer contains (`padded`, `templated`,
       `unsupported`). When nothing on the list fits, say it in a `concern` claim;
     - `outcome`: a provisional outcome key. A batch sees only its own responses, so it
       picks its own best: in the 44-response dry run (2026-10-18) the batches recommended
       10 for 4 slots, and one region alone had 4 recommended and 6 backups. Step 8 settles
       outcomes across the pool and rewrites the `outcome` claim of every one it changes;
     - `one_line`: one sentence for the all-organisation table (no names of people).
   - **Separate facts from inference.** What they wrote is what they say about
     themselves. A statement confirmed by labs history or by a source counts as evidence,
     and the claim cites that source as well as the answer.
   - Do not reward a confident statement that has no evidence behind it.
   - Web-check only the candidates heading for the shortlist (Recommended or Recommended backup): registration, age,
     visible track record, and named partners. Cite every source as a `web` cite with its
     url.
   - When the batches come back, run `check_claims.py` on every batch yourself; do not
     take a subagent's "OK" on trust. Fix what fails by copying the words from the answer,
     or send the response back to a subagent. This catches most of what labs would refuse.

7. **Read across the whole pool before choosing.**
   - Find what the pool has in common and what separates it, the same way the team's
     ULAB notes do. Look at:
     - geography: who names districts, who claims many states and is vague outside one;
     - who has real access to the chain or the actors;
     - how young the organisations are;
     - how they sample, and who addresses bias;
     - the spread of prices, expressed in the call's units.
   - These patterns go to the calibrator (step 8) and become the "what the pool told us"
     and "before-launch conditions" sections of the internal report (step 10).
   - If the pool shows a criterion is not separating anyone, or something decisive has no
     criterion, say so in the reply and suggest `eoi-criteria-proposal`. Do not adjust the
     scores to compensate.

8. **Calibrate across the pool: a separate agent, before anything is written to labs.**
   Each batch scored and chose outcomes seeing only its own responses, so the batches
   disagree on how hard each anchor is and each picks its own best. Calibration fixes this
   once, across the pool. Dispatch it as its own subagent that scored no batch. Pass it
   the paths of every `batch-<n>.json` and checked `out-<n>.json`, `criteria.json`, the
   call facts (roles and how many slots each has, priority sites or regions, budget), and
   the patterns from step 7. Pass outputs as paths, not inline, so the spot-check in (b)
   can read the raw answers first. The calibrator:
   - **(a) Tabulates the per-criterion score distributions**, overall and per batch, and
     finds pairs of responses where similar evidence got scores 3 or more points apart, or
     where batches read an anchor differently (one batch gives 7 for a named district,
     another 4). It rescores against the criterion's `scoring_guide`, rewriting the
     `criterion:<id>` claim to match the new score.
   - **(b) Blind spot-checks 6 responses**: the top 3 by weighted score, plus 3 from
     other batches. For each, it reads the raw answers in `batch-<n>.json` and scores every
     criterion **before** opening the scorer's review of it, then compares. A gap of 3 or
     more points on any criterion is a finding: settle the score and look for the same
     misreading in that batch.
   - **(c) Checks that each claim's text is supported by its cites**, not only that the
     quote exists. A claim that says more than its passage does is rewritten to what the
     passage shows, re-cited, or marked `synthesized` honestly.
   - **(d) Settles outcomes across the pool by the rubric's outcome rules** in
     `criteria_basis` (Slots, Recommended, Recommended backup, Waitlist, Not recommended,
     Overrides); when the round has none, about one Recommended (`pick`) per slot and two
     Recommended backups (`backup`) per slot, then Waitlist (`waitlist`) for the credible rest and
     Not recommended (`pass`). A Recommended backup must clear the Recommended bar (every
     condition the Recommended rule sets on the applicant itself: minimum scores, "no
     criterion at 1", no disqualifier) and is only behind the recommended applicant(s) for
     its slot; an applicant who would be next in score order but fails that bar is not a
     backup, it goes to Waitlist or Not recommended per the rules. Every outcome claim
     names the outcome in the words people read and the rule it applied, and an outcome
     that goes against the score order names the override (for example "Recommended backup, slot rule: a higher scorer covers Ghana north",
     "Recommended, rescoping override: conditional on one site within budget"). It
     rewrites the `outcome` claim of every response whose outcome changes.
   - **(e) Writes `calibration.md`**: the distributions (before and after), every change
     with before → after and why (scores, outcomes, rewritten claims), the spot-check table
     (response, scorer's score, blind score, gap, per criterion), and the final slate per
     slot. It also writes every change as data in `calibration.json`, which step 9 reads:

     ```
     {"changes": [{"response_id", "field": "outcome" | "score:<criterion_id>",
                   "before", "after", "why"}]}
     ```
   - Re-runs `check_claims.py` on every batch it changed, until each prints `OK: every
     claim checks`, and returns the calibrated `out-<n>.json` files.
   For scale, in the 44-response dry run (2026-10-18) calibration changed 16 outcomes and
   8 scores and rewrote 3 claims, and its spot-check found no gap of 3 or more. A
   calibration that changes nothing is possible but worth a second look: check the slate
   against the slot count before believing it.

9. **Check how well the rubric served the pool** (rubric health). Run after calibration,
   on the calibrated reviews, before the reports; run it again once people have reviewed
   in labs, since their agreements and disagreements are the best evidence of all.
   - Save the round (`marketplace_round_responses`) to `round.json` and the reviews to
     `reviews.json`: before the labs write, the calibrated `out-<n>.json` entries with
     `kind: "ai"` added; after it, every response's `list_reviews` result, which also
     carries people's reviews (`kind: "human"`, `based_on`, `stance`). Then:

     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/skills/eoi-round-review/rubric_health.py" \
       round.json reviews.json --calibration calibration.json --json rubric-health.json \
       > rubric-health.md
     ```

   - It reports, per criterion: the score distribution (mean, SD, histogram, the share on
     three adjacent values: does it spread or bunch?); whether it separates the shortlist
     (Recommended and Recommended backup) from Not recommended (means, and the AUC: the chance a
     random shortlisted response out-scores a random not-recommended one); its effective weight (how much of the weighted score's
     spread it actually produces) against its nominal weight; the share of its scores with
     no exact passage behind them, and the share that are a low score for a missing answer
     (hard to judge from the form); and its correlation with answer length (the words in the
     response, from the responses `round.json` carries: r ≥ 0.5 means the anchors reward
     length rather than what the answer names, which `eoi-criteria-proposal` forbids). Across criteria: the correlation matrix (|r| ≥ 0.7 is a
     redundant pair). For the slate: which responses got a better outcome than a higher
     scorer and what the outcome claims say it turned on (slot or geography, rescoping,
     safety or scope). And where calibration and people changed scores or outcomes, by
     criterion and stance.
   - Its recommendations are a starting point with the thresholds in the script. Read the
     numbers and the claims behind them and write the final list: **keep / reweight /
     split / drop / add**, one line each, every one with the numbers it rests on (for
     example "reweight cost_fit 15 → 10: AUC 0.64, the lowest; the slate turned on
     rescoping, not on the quote"). An "add" is for what the slate turned on that no
     criterion or outcome rule captures. Also say which anchors the scores show were read
     inconsistently (the same kind of answer scored 1, 2 and 3), and what the Silent rule
     should be.
   - Do not change scores or outcomes to fit the findings. A change to the rubric goes
     through `eoi-criteria-proposal`, and replacing the criteria invalidates this pass.

10. **Write the two reports.** Both draw on the calibrated reviews and `calibration.md`.
   Plain language. No scores in the bottom line. Numbers only where they decide something
   (a price, a count, a budget). Recommended, Recommended backup, Waitlist and Not recommended are
   exactly the calibrated outcomes, so labs and the internal report agree. Reports use
   these words, never the keys (`pick`, `waitlist`, `pass`); an applicant with no outcome
   is "No recommendation yet".

   **The internal report** (Dimagi only):
   - *Overview tab* (first), under ~2 pages. Write it as an analyst making the case to
     the program team: say who to fund and why, plainly and briefly, as conclusions. The
     reader wants the outcome, not the method; everything about how the review was run
     goes in the second tab. No criteria ids or weights, no score numbers, no version
     labels, no flag words, no "the rubric". Numbers only where they decide something
     (a price, a count, a budget).
     - **Bottom line**: who to fund, for which place, within what budget, in two or
       three sentences, plus the biggest program-level finding in one more.
     - **One section per place** (a `###` heading naming the place and the Recommended
       applicant): why them, in terms of what the work needs (site, trade knowledge,
       a way to reach the households, team, cost); their gap; the condition to settle
       before contracting, or "none"; and the Recommended backups, each with what it
       would need to step in. Use headed sections and bullets, not a table: the Overview
       tab is written by `scripts/gdoc-tab.ts`, which refuses pipe tables.
     - **Program-wide questions**: decisions for the program team that the whole pool
       surfaced, numbered, each one counted from the responses ("only 9 of 44 …") and
       ending in the decision to make. Draw them from the program-design reading: places
       nobody credible covers, which site serves the call's purpose, the unit of
       payment, the safety line, scope drift, and every assumption in the call the
       responses contradict.
     - **Ask every shortlisted applicant before contracting**: the shared questions,
       numbered (each review's own `ask_next` stays in labs).
     - **What the next call should ask differently**: short bullets.
     - **Next step**: one or two lines on reviewing in labs, with the round page and
       Scores page links.
     - Notable Not recommended applicants and the Waitlist go in the second tab, unless
       one is a strong applicant that only misses this round's scope; then name it in
       one line under the bottom line, so the team keeps it for later.
   - *Review details tab* (second):
     - **How we scored**: the round's criteria and weights (with `rubric_version`), the
       outcome rules applied, what the criteria basis says was dropped, and, when an
       earlier version exists, the moves from `marketplace_round_scores(compare_with=…)`.
     - **The slate in full**: the Recommended table (partner, country and site, role,
       score, condition), Recommended backup and Waitlist with one reason each, and the
       notable Not recommended with one line of reason.
     - **What the pool told us about the work**: what applicants report about the field
       the call is in. For a value-chain call that is the trade itself: prices, buyers,
       destinations and household practice. Present these as the applicants' own reports
       ("12 applicants describe…"), not as findings.
     - **Pool coverage and quality**: responses by country and priority site or region,
       sites with no credible applicant, duplicates, and how many answers were specific
       versus generic.
     - **How it was reviewed**: the criteria table (id, name, weight, one-line
       rationale), the calibration summary (what changed and why), the spot-check table,
       and evidence counts (claims, quoted vs synthesized, cites by kind, web checks).
     - **Comparison with the team** (step 11), when there is one.
     - **Rubric health** (step 9): the recommendations with their numbers, the
       per-criterion table and the slate-override table, in under a page.
     - **Program design: what this pool tells us** (the full counted reading; its
       decisions are the Overview's Program-wide questions): what the program team should think
       about before contracting, grounded in the responses and counted ("31 of 44 ..."):
       - questions the team should answer before contracting (what the pool shows is
         undecided: the unit of payment, whether "we don't know" answers are acceptable,
         what happens at a slot nobody credible covers);
       - design risks the pool exposed (scope drift into collection, safety at
         breaking or smelting sites, start dates before contracting, capacity resting on
         one person);
       - assumptions in the call the responses contradict (for example the battery life
         assumed, who households sell to, where the batteries go);
       - what to ask the shortlisted organisations before contracting, beyond each
         review's `ask_next`: the questions the whole slate leaves open;
       - what the next call should ask differently (form questions, structured fields,
         pricing guidance), merged with the next-form advice below.
       Present applicants' reports as their reports, not findings; give the count behind
       every point.
     - **Next-form advice**: questions to add, cut or structure, from the criteria basis
       and what this review could not judge.
     - **All-organisation table**: every response, one row: organisation, country and
       site, outcome, role, weighted score, cost per site, `one_line`.
     - **Every response**: one ≤120-word entry per submission, with outcome, role fit,
       cost, strengths and concerns citing the answer, and questions to ask.
   - For several rounds, add **Across rounds**: organisations that answered more than one
     round and how they did, how the pools differed, and any organisation strong in one
     round that is worth inviting to another.

   **The external report** (de-identified, for funders and partners):
   - No organisation or person names, and no verbatim quotes: paraphrase, and describe
     applicants by kind ("a farmer cooperative in a priority region").
   - Figures for the pool only (counts, ranges, medians), never one applicant's figure
     that would identify it. Place names only at the level of the call's priority sites
     or regions.
   - What the call sought and what the pool looked like; the criteria and why each was
     chosen; what separated strong responses from weak ones; what the pool told us about
     the work (the same section as internal, pooled and de-identified); and lessons for
     running the next call (form, timeline, outreach, pricing guidance).
   - No outcomes, shortlist or anything that lets a reader work out who was chosen.

11. **Compare with the team's shortlist when there is one.**
    - When the requester gives the team's own shortlist (as for ULAB), add a short table
      to the internal report with each applicant either side shortlisted, theirs vs
      ACE's outcome, agree or differ, and why.
    - A difference is information, not an error to hide. A difference ACE cannot defend
      from the responses is a finding about this skill. Note it in the reply.

12. **Write the AI reviews to labs.**
    - For each response, call `list_reviews(response_id=…)` first. If people have already
      reviewed on top of ACE's earlier AI review (`based_on` it, or feedback on it), say so
      in the reply before replacing it: their review stays, but it now sits on an AI review
      that changed.
    - Then call, per response, from the calibrated `out-<n>.json`:

      ```
      create_review(
        public_record_acknowledged=true,
        response_id=<response_id>,
        llo_entity_id=<matched org_slug, or "">,
        kind="ai",
        criteria_scores={<criterion_id>: <1-10>, ...},   # every criterion on the round
        claims=[{id, about, text, basis, cites}, ...],   # § Claims and evidence
        ask_next="<2-3 questions>",
        flags=[...],                                      # defined keys only; labs refuses others
        outcome="pick" | "backup" | "waitlist" | "pass",  # Recommended / Recommended backup / Waitlist / Not recommended
        provenance={
          model: "<the model running this skill>",
          skill: "eoi-round-review",
          skill_version: "<ACE plugin version: cat ${CLAUDE_PLUGIN_ROOT}/VERSION>",
          rubric_version: <round.rubric_version>,
          sources: ["form answers", "labs org history", "web: <url>", ...],
        },
      )
      ```

      Do not pass `score` (labs computes it from `criteria_scores` and the round's
      weights) or `based_on` (a human field). Do not pass `strengths`, `concerns` or
      `criteria_notes` either: labs fills them from the claims, and a second copy in the
      flat fields would drift from the evidence. `sources` lists only what this review
      actually used.
    - **Pace the writes.** The connect-labs MCP allows 30 writes per minute per user,
      counted across every session writing as that user. In the dry run, 14 of 44
      back-to-back `create_review` calls came back with "Write rate limit exceeded
      (30/m)". Write from one place, in sequence (never fan `create_review` out to
      parallel subagents), with at least 2.5 s between calls. When a call is rate-limited,
      wait 60 s and retry the same call unchanged. A rate-limit refusal is not a quote
      refusal: nothing about the review is wrong, and it does not count towards the
      "refused twice" rule below.
    - **Labs checks every quote on save.** If any `quote` is not found in the answer its
      `question` names, labs returns `BAD_REQUEST` for the whole review, naming each
      quote it could not find. Then:
      1. For each quote named, reopen that response's answer to that `question_id` and
         copy the words exactly as they appear there (or the answer they actually came
         from, fixing `question`). Never paraphrase inside `quote` to make it pass.
      2. If the point is not in the answer in so many words, change the cite instead:
         `whole: true` with `basis: "synthesized"`, `absent: true` if the claim is that
         the answer is silent, or drop the claim if nothing supports it.
      3. Re-run `check_claims.py` on the batch, then retry `create_review` with the
         corrected claims. Nothing was saved by the refused call, so retry the full
         review, not just the fixed claims.
      4. If the same response is refused twice for quotes, stop retrying it, list its
         `response_id` and the quotes labs named in the reply, and do not report the pass
         complete.
    - Contact details never go in any field, claim or quote. Name the organisation, never
      a person.
    - Re-running on the same criteria version replaces ACE's AI review of that response; it
      never adds a second one. Re-running after the criteria were replaced writes the review
      on the new version, and labs keeps the earlier AI review as superseded history on the
      old version (`marketplace_round_versions` counts both).
    - **When an earlier version exists, report what the re-score changed from labs' own
      figures**: `marketplace_round_scores(slug, compare_with=<previous version>)` returns
      whose recommendation moved, the mean score shift, and each criterion's weight, mean
      and shortlist gap in both versions. Put those moves in the reply and the internal
      report, and link the round's Scores page
      (`https://labs.connect.dimagi.com/labs/marketplace/rounds/<slug>/scores/`), which shows
      the same comparison. Do not hand-build the diff from local batch files: the comparison
      people open in labs is the one to quote.
    - Read back with `list_reviews` for a sample of responses (and every Recommended one)
      and check the scores, the claims (with their cites), the outcome and `rubric_version` landed,
      and that labs filled the strengths, concerns and criteria notes from them. If any
      write failed, list the response ids in the reply; do not report the pass complete.
    - If `rubric_version` on the round changed while this ran, stop: the reviews written so
      far carry a version that no longer applies. Re-run.

13. **De-identify, publish and share the links.**
    - **Run the de-identification scan on the external report before publishing it.** Build
      a deny list from the batches and the answers:
      - every `org_name`, and every distinctive word in one (skip generic words such as
        "foundation", "initiative", "development", "community", "association", "network",
        "limited"; keep a word that would point a reader at the organisation);
      - every town, village or neighbourhood that only one applicant mentioned (places
        several applicants share, and the call's own priority sites or regions, may stay);
      - every programme, project, funder and partner name the answers mention.
      Search the external report's text for each entry, ignoring case and as a whole word.
      Any hit is rewritten (pooled, generalised or removed) and the scan re-run until it
      finds nothing. Also re-read it for a figure, quote-like phrase or detail that only
      one applicant reported. Record in the reply that the scan ran and found nothing.
    - Publish both reports with `gdoc-writer`, each with `--share none` (sharing off), the
      internal one with the round-page link at the top. For the internal report, publish
      the **Review details** content with `gdoc-writer` first (it renders its tables),
      then add the Overview as the first tab and name the second:

      ```bash
      ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
      node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/gdoc-tab.ts" --doc <docId> --md overview.md \
        --title "Overview" --index 0 --rename-tab "Tab 1=Review details"
      ```

      The script prints the doc's tabs; confirm it lists `Overview` then `Review details`.
      Re-running it replaces the Overview tab in place (same doc, same link). After any
      `gdoc-writer --replace` of the doc, re-run it and check both tabs again. To revise
      an existing summary, edit that doc in place this way rather than publishing a new
      one, so the round's summary link keeps working.
    - **Link the internal report on the round**: call
      `marketplace_round_summary_set(slug=<round slug>, url=<internal report url>)` for
      each round it covers. Labs shows the link on the round page, which only the round's
      owner org (Dimagi) can see, so the link reveals nothing the doc's own sharing does
      not. The requester's approval to write the report covers this link. The url must be
      `https`; an empty url clears the link. If the call fails, say so in the reply and give
      the link there; the reports still stand. Never link the external report here.
    - Run `agent-turn-review` before replying.
    - Reply with the three links (internal report, external report, round page), saying
      which is which: the internal report is for Dimagi people only (`@dimagi.com`,
      `@dimagi-ai.com`, `@dimagi-associate.com`); the external one is de-identified for
      funders and partners. The requester decides who receives each; share only on their
      say-so, never the internal report outside Dimagi. Add three lines (who, why, what to
      ask first) and one line on what happens next in labs (below).

## Claims and evidence

A claim is one statement in the review, tied to what it rests on. Reviewers click a claim
in labs and see its passages highlighted in the response, so a claim is only as useful as
its cites are exact.

- `id`: short, unique within the review: `"c1"`, `"c2"`, …
- `about`: `"criterion:<criterion_id>"` (the reason for that criterion's score),
  `"strength"`, `"concern"`, `"flag"` or `"outcome"`. A `flag` claim explains one flag on
  the review: its text starts with that flag's label or key (`Claims to check: ` or
  `unsupported: `), and every flag on the review has one (`check_claims.py` enforces
  both). An `outcome` claim says the outcome in the words people read (Recommended,
  Recommended backup, Waitlist, Not recommended), not the key.
- `text`: one sentence in plain language. No names, emails or phone numbers. A
  `criterion:<id>` claim on an anchored rubric starts by naming the anchor its score was
  read against: `Anchor 7: names one priority LGA, but not its urban/rural mix.` The anchor
  is the one nearest the score (2 reads against 1 or 3, 8 against 7, 9 against 10), and
  the rest of the sentence says what moved it off the anchor. An answer that says nothing
  starts `Silent: ` and gets the rubric's Silent score, citing the answer `absent: true`.
  `check_claims.py` enforces both.
- `basis`: `"quoted"` when the claim rests on specific passages, or `"synthesized"` when
  it is a judgement drawn from across the response ("the text is generic throughout",
  "the answers contradict each other on staff numbers"). A synthesized claim is fully
  legitimate, not an unsourced one; mark it honestly rather than hunting for a quote that
  only half supports it.
- `cites`: a list; each entry is one of:
  - `{"question": "<question_id>", "quote": "<exact words from that answer>"}`. The quote
    must appear **verbatim** in that answer. Labs ignores case and runs of whitespace and
    normalises curly quotes and dashes, nothing else, so copy the words: never
    paraphrase, fix spelling or grammar, translate, join two passages with "…", or add
    words inside `quote`. Keep it short: the phrase that carries the point, typically 3
    to 25 words. Several cites per claim are fine, across several questions.
  - `{"question": "<question_id>", "absent": true}`: the claim is about something missing
    from that answer ("names no battery buyer").
  - `{"question": "<question_id>", "whole": true}`: a synthesized claim drawn from that
    whole answer.
  - `{"source": "labs", "detail": "<what labs shows>"}` for labs history, e.g. delivered
    programmes; `{"source": "web", "detail": "<what the page shows>", "url": "<url>"}`
    for the web (the url is required).
- A synthesized claim may have no cites at all when it is drawn from the whole response.
- **Contact details never go in a quote.** If the only passage that supports a claim
  contains a person's name, email or phone, cite that answer with `whole: true` instead
  of quoting it.

Example, for an invented applicant (criterion ids are whatever the round saved):

```json
[
  {"id": "c1", "about": "criterion:named_sites", "basis": "quoted",
   "text": "Anchor 7: names three districts and the markets it already works in there.",
   "cites": [{"question": "q4", "quote": "we work in Kisumu, Siaya and Homa Bay"},
             {"question": "q4", "quote": "weekly visits to the Kibuye and Bondo markets"}]},
  {"id": "c2", "about": "criterion:cost_fit", "basis": "quoted",
   "text": "Anchor 7: quotes 9 USD per household survey, under the call's rate.",
   "cites": [{"question": "q9", "quote": "USD 9 per completed household survey"}]},
  {"id": "c3", "about": "strength", "basis": "quoted",
   "text": "Has delivered a Connect programme before, and finished it.",
   "cites": [{"source": "labs", "detail": "delivered one Connect programme in 2025"},
             {"question": "q6", "quote": "completed our first Connect project last year"}]},
  {"id": "c4", "about": "concern", "basis": "quoted",
   "text": "Does not say who would buy the batteries it plans to collect.",
   "cites": [{"question": "q7", "absent": true}]},
  {"id": "c5", "about": "flag", "basis": "synthesized",
   "text": "Long but thin: both answers restate the question and name no site, buyer or past job.",
   "cites": [{"question": "q2", "whole": true}, {"question": "q3", "whole": true}]},
  {"id": "c6", "about": "outcome", "basis": "synthesized",
   "text": "Recommended backup, slot rule: strong sites and price, but a higher scorer holds the survey slot and it names no buyer for the value-chain role."}
]
```

With that example the review's `flags` is `["padded"]` and its `outcome` is `"backup"`.

## Outcomes and flags

Labs defines the words a review is written in (connect-labs
`connect_labs/solicitations/vocabulary.py`; `skills/eoi-round-review/vocabulary.py` is
ACE's copy, which the checkers read). The API stores and takes the **keys**; people read the
**labels**, so every report, outcome claim and reply uses the labels.

**Outcomes:**

| Key | Label | Meaning |
|---|---|---|
| `pick` | Recommended | Proposed for one of the round's places now. |
| `backup` | Recommended backup | Meets every condition for Recommended, but ranks behind the recommended applicant(s) for a named place; ready to step in if one falls through. |
| `waitlist` | Waitlist | Credible, but not needed for this round's places; worth asking again in a later round. |
| `pass` | Not recommended | Not a fit for this round, for the reasons the review gives. |
| (none) | No recommendation yet | Nobody has reviewed it, or the review set no outcome. |

The **shortlist** is Recommended plus Recommended backup.

**Flags** are things for a reviewer to check before relying on a response, never
penalties: the criterion scores carry the judgement. Use only these keys; **labs refuses
a review with any other flag** (it maps a few older free-text names to these, but this
skill writes only the keys). Each one needs a `flag` claim saying what raised it.

| Key | Label | Raise it when |
|---|---|---|
| `unsupported` | Claims to check | Numbers, partners, licences or past work look inflated, or nothing in the response or labs history backs them up. |
| `inconsistent` | Answers disagree | Two answers in the same response contradict each other (dates, numbers, places, staff). |
| `templated` | Shared or template text | Placeholders left in, text near-identical to another applicant's, or the same response submitted twice. |
| `padded` | Long but thin | Answers at length with few checkable facts: restates the question, describes intentions rather than what they know or have done. |
| `incomplete` | Incomplete | A key answer is missing, cut off or does not address the question. |
| `out-of-scope` | Outside the brief | Proposes places, activities or a scale the call did not ask for. |
| `capacity` | Thin capacity | The work rests on one person, or on a team already committed elsewhere at the same time. |
| `cost` | Cost out of line | The quote is far from the others or from the budget, or cannot be compared with them. |
| `early-start` | Starts before contract | Plans to begin work before a contract is in place. |
| `safety` | Safety | The plan puts staff or respondents at risk without saying how. |

Never flag "AI use" as such: whether an applicant used AI is not checkable and not the
point. Flag what the answer contains (`padded`, `templated`, `unsupported`).

## What happens next in labs

The AI review is a first pass, not the decision. On the round page
(https://labs.connect.dimagi.com/labs/marketplace/rounds/<slug>/) a reviewer sees each
response and its reviews side by side. Clicking a claim in a review highlights the
passages it cites in the response (or marks the answer it says is silent, or shows the
labs or web source), so a reviewer checks the AI's reasoning against the applicant's own
words instead of taking it on trust.

Once reviews exist, the round page lists the recommended first, and its **Start reviewing** button
(**Next to check** once started) walks the reviewer through the applicants no person has
checked yet. On a response page a reviewer works in one of four ways:

- **I agree**: one save creates their own review, linked to the AI one, with stance
  "agrees".
- **Add to it**: keeps the AI's review as it is and adds their own reasons, passages and
  questions, marked as theirs (stance "adds").
- **Copy and edit as mine**: starts their own review from the AI's. They edit the scores,
  the reason under each score, and the strengths and concerns; drop a cited passage with
  ×, or select text in an answer and use **Attach selected text** to cite it.
- **I disagree**: the stance is preset to "disagrees"; they change the outcome and the
  scores.

Each way leaves the reviewer's own review beside the AI's. **The AI review never changes**
when a person agrees, adds to, copies or disagrees with it. Several people may review the same
response; every review is scored on the same criteria and `rubric_version`, so they can
be compared side by side. Re-running this skill replaces only ACE's AI review; human
reviews stay. If the criteria are replaced, every review on the old version (AI and human)
was scored against criteria that no longer apply, which is why `eoi-criteria-proposal`
asks before replacing them. Labs keeps each version and the reviews on it, and the round's
**Scores** page (`/labs/marketplace/rounds/<slug>/scores/`) has a version picker and a
"what changed" comparison between versions.

When telling the requester what happens next, name the four ways and the Start reviewing
button in one or two lines; the reviewers are the audience.

## MCP Tools Used

- connect-labs: `marketplace_rounds_list`, `marketplace_round_responses` (owner-gated:
  ACE's labs user must belong to Dimagi, the owner of every directory round),
  `marketplace_orgs_get`, `list_reviews`, `create_review` (`kind="ai"`, with `claims`;
  `BAD_REQUEST` on a quote it cannot find or a flag not on the defined list; 30 writes per
  minute per user), `marketplace_round_summary_set` (links the internal report on the
  round; owner-org members only), `marketplace_round_scores` (`compare_with` for the
  version-to-version moves) and `marketplace_round_versions` (read-only, owner only)
- canopy-web: `current_page` (when started from the marketplace panel)
- Google Drive: `drive_read_file`, `read_personal_drive_doc` (the announcement);
  publishing goes through `gdoc-writer`
- Web search, for shortlist candidates only
- `skills/eoi-round-review/check_claims.py` (python3, stdlib only): the quote, structure,
  flag and anchor-citation check every batch passes before labs sees it
- `skills/eoi-round-review/vocabulary.py`: ACE's copy of labs' outcome and flag words
- `skills/eoi-criteria-proposal/check_rubric.py`: whether the round's rubric is explicit
  (step 3)
- `skills/eoi-round-review/rubric_health.py` (python3, stdlib only): how well the rubric
  served the pool (step 9)

## Mode Behavior

- **Auto:** with criteria on the round, score, calibrate, write the AI reviews, publish
  both reports with sharing off, link the internal report on the round and reply with the
  links. With no criteria, run `eoi-criteria-proposal`, which always waits for
  approval before saving; scoring starts after that.
- **Review:** show the criteria from step 3 and wait for a go-ahead before scoring and
  writing reviews. Publish the draft and wait for the requester's edits before it goes to
  anyone else.

## Terminology

The doc and every review are prose a person reads. Follow `skills/_terminology.md`: the
platform is "Connect".

## Related skills

- `eoi-criteria-proposal` writes the round's criteria from the pool; run it first when the
  round has none.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-19 | The internal report's first tab is an analyst Overview: the outcome and the case for each recommendation, with the program-wide questions the pool raised, and no scoring mechanics; how it was scored, versions, calibration and rubric health move to the second tab, Review details. The two tabs are now actually produced: `scripts/gdoc-tab.ts` (lib `markdown-docs-tab.ts`) writes the Overview tab, which `gdoc-writer` could not. Requested by Jonathan on the ULAB summary | ACE team |
| 2026-10-19 | Human review: four ways, not three — labs' response page also offers **Add to it** (stance `adds`), verified against `templates/solicitations/round_response.html` (connect-labs `docs/marketplace-round-review.md`, #2615) | ACE team |
| 2026-10-19 | Versions: a re-score on replaced criteria supersedes the earlier AI review (kept as history on the old version); when an earlier version exists, the reply and internal report quote labs' own comparison (`marketplace_round_scores(compare_with=…)`) and link the Scores page, never a hand-built diff | ACE team |
| 2026-10-18 | A Recommended backup must clear the Recommended bar and is only behind the recommended applicant(s) for its slot; an applicant next in score order that fails it goes to Waitlist or Not recommended | ACE team |
| 2026-10-18 | Outcome labels renamed in labs (`vocabulary.py`): `backup` is Recommended backup (was Backup), `waitlist` is Waitlist (was Keep in view); keys unchanged | ACE team |
| 2026-10-18 | `rubric_health.py` reports each criterion's correlation with answer length (from the responses in `round.json`) and notes r ≥ 0.5 in its recommendation: method criteria were rewarding longer answers | ACE team |
| 2026-10-18 | Labs' defined vocabulary: flags are a fixed list of ten keys (labs refuses any other; `check_claims.py` refuses it first, and requires a `flag` claim naming each flag); outcomes keep their keys but are shown as Recommended / Backup / Keep in view / Not recommended in reports, claims and `rubric_health.py`; new § Outcomes and flags; step 13 links the internal report on the round with `marketplace_round_summary_set` | ACE team |
| 2026-10-18 | Explicit rubric and rubric health: step 3 checks the round's rubric with `check_rubric.py`; criterion claims name the anchor they were read against (`Anchor <n>: ` / `Silent: `, enforced by `check_claims.py`); calibration settles outcomes by the outcome rules in `criteria_basis` and writes `calibration.json`; new step 9 runs `rubric_health.py` (distribution, separation, effective weight, evidence, correlation, slate overrides, calibration and human changes) and writes keep/reweight/split/drop/add with numbers; the internal report gains Rubric health and "Program design: what this pool tells us" | ACE team |
| 2026-10-18 | Learnings from a 44-response dry run: shipped `check_claims.py` (labs' quote matching plus structure checks) that every batch runs until OK; batch in/out shapes (`cost_per_site_usd`, `cost_note`, `one_line`); a separate calibration agent before any labs write (distributions, blind spot-check of 6, claim support, outcomes settled per slot, `calibration.md`); labs writes paced ≥2.5 s and retried after 60 s on the 30/m limit; internal and de-identified external reports, both published with sharing off after a de-identification scan; the three human review modes and the round page's Start reviewing walk | ACE team |
| 2026-10-17 | Evidence: every statement in an AI review is a claim citing the response's exact words (`question_id` + verbatim quote), an absent or whole answer, or labs/web history; strengths, concerns and criterion notes go in `claims` (labs fills the flat fields); fix-and-retry on `BAD_REQUEST`; reviewers click a claim to see its passages | ACE team |
| 2026-10-17 | Scores on the round's saved criteria (1–10, via `eoi-criteria-proposal`; no private rubric), writes one AI review per response to labs (`create_review(kind="ai")`), links the doc to the round page, explains the human review flow in labs | ACE team |
| 2026-10-16 | Initial version, modelled on the team's ULAB shortlist and Sagar's ULAB EOI prompt; reads round responses through connect-labs `marketplace_round_responses` (connect-labs#2586) | ACE team |
