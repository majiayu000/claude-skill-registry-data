# Rule catalogue

Each rule finds **candidates** by pattern. "Ignore when" lists the usual false positives; "Rules miss" lists
what only a reader can catch. Sources for every rule and number are in [sources.md](sources.md).

Severity: **high** = likely to distort answers, **medium** = often a problem, **low** = worth a look,
**info** = a note that is not counted and does not fail `--strict`.

## Contents

- Wording rules: SB001 to SB008, SB021, SB026 (run on each question stem and each grid row)
- Question rules: SB017 to SB020, SB023 (run on the stem together with its options)
- Answer-option rules: SB009 to SB014, SB022, SB027, SB028
- Questionnaire rules: SB015, SB016, SB024, SB025
- Context flags
- What no rule checks
- QAS-99 crosswalk
- Results on the fixtures

## Wording rules

### SB001 double-barreled (medium)

Detects: `X and Y` in the stem; `X or Y` only when the answers are a rating scale, yes/no or numbers.
Text in parentheses, "between X and Y", fixed phrases ("terms and conditions", "friend or colleague") and
balanced pairs ("agree or disagree", "easy or difficult") are skipped.

- Before: How satisfied are you with the speed and reliability of our app?
- After: How satisfied or dissatisfied are you with the speed of the app? / How satisfied or dissatisfied
  are you with the reliability of the app?

Ignore when: the phrase names one concept ("research and development"), or "and" joins two clauses about one
thing. Rules miss: two questions joined without "and" ("How fast, reliable was ...").

### SB002 leading or loaded wording (high)

Detects: "don't you", "wouldn't you", "isn't it", "do you agree that", "would you agree", "most people",
"many people", "experts say/agree/recommend", "as you know", "obviously", "of course", "studies show",
"research shows", evaluative adjectives (amazing, awesome, fantastic, wonderful, incredible, great,
world-class, award-winning, revolutionary, terrible, awful, horrible, disastrous), "how much do/did you
love/enjoy", "new and improved".

- Before: Don't you agree that our amazing new dashboard saves time?
- After: Compared with the old dashboard, does the new dashboard take you more time, about the same time or
  less time? (More time / About the same / Less time)

Ignore when: the adjective is part of a name or a quoted statement being tested. Rules miss: one-sided
stems ("How satisfied are you ...?" without "or dissatisfied"), loaded nouns ("the failed rollout"), named
sponsors, and any wording outside the list.

### SB003 absolute (medium)

Detects: always, never, everyone, everybody, nobody, no one, every time, all the time, at all times, every
single. "Ever" and "all" are not flagged.

- Before: Do you always read the release notes? (Yes / No)
- After: Of the last 5 releases, for how many did you read the release notes? Enter a number from 0 to 5.

Ignore when: the absolute is inside a quoted statement being tested. A screener built on "never" ("Have you
never used ...?") is also a negation (SB005): ask "Have you ever used ...? (Yes / No)" instead.

### SB004 hypothetical (medium)

Detects: "would you buy/pay/use/consider/switch/subscribe/try/...", "if we/you/it added/offered/were/...",
imagine, suppose, hypothetically, "in the future", "will you", "how likely are you to
buy/pay/use/subscribe/renew/...". "How would you rate/describe" and "likely to recommend" are not flagged.

- Before: If we added a team plan, would you pay $20 per month for it?
- After: In the past 12 months, did your team pay for a shared plan of any similar tool? (Yes / No / Not
  sure). If intent must be asked, report it as stated intent in its own units, not as a forecast; check it
  against behaviour (past purchases, a trial) before forecasting what people will buy. To set a price, use a
  price method (`van-westendorp-analysis`, `gabor-granger-analysis`, `conjoint-design`) instead.

Ignore when: the study is about intent by design (concept test, pricing study) and the report treats the
numbers as stated intent.

### SB005 negation (high for double, medium for single)

Detects: two or more negations in one stem (not, n't, cannot, never, plus words such as unable, unlikely,
dissatisfied, oppose, prevent when a "not" is present): high. One negation when the answers are yes/no or
agree/disagree: medium.

- Before: Is it not true that you did not find the setup difficult?
- After: How easy or difficult was the setup? (Very easy ... Very difficult)
- Before (grid row, agree/disagree): The pricing is not clear.
- After: How clear or unclear is the pricing? (Very clear ... Very unclear)

Ignore when: the negation is in a quoted statement the study tests. Single negations in other question
types ("What did you not like?") are not flagged.

### SB006 vague quantifier (low)

Detects in the stem: regularly, frequently, occasionally, recently, lately, sometimes, seldom, "a lot",
and "often" unless it follows "how". Detects in options: two or more of often, sometimes, rarely,
occasionally, frequently, regularly, seldom, usually, "hardly ever".

- Before: How often do you use the mobile app? (Often / Sometimes / Rarely / Never)
- After: In the past 7 days, on how many days did you use the mobile app? Enter a number from 0 to 7.

Ignore when: a perception is wanted, not a count, or the scale belongs to a validated instrument.
A missing reference period is SB017.

### SB007 jargon or acronym (low)

Detects: capitalised acronyms of 2 to 6 characters that are not defined in parentheses and not in a short
list of common ones (US, UK, EU, TV, IT, HR, CEO, PDF, ...); and synergy, omnichannel, paradigm, utilize,
holistic, touchpoint, "value proposition", "pain point", "use case".

- Before: How would you rate the SSO setup?
- After: How would you rate the setup of single sign-on (SSO)?

Ignore when: every respondent uses the term at work (a survey of IT administrators). Rules miss: technical
words that are not acronyms ("myocardial infarction", "tort reform").

### SB008 long question (low)

Detects: a stem of more than 20 words (`--max-words`).

- Before: Thinking about the last time you contacted our support team by email or by chat about a billing
  problem, how long did it take before you received a first reply that addressed your question?
- After: (intro line) The next question is about the last time you contacted support about billing.
  (question) How long did it take to get a first reply? (Less than 1 hour / 1 to under 5 hours / 5 to under
  24 hours / 24 hours or more)

Ignore when: the extra words are a definition or a reference period that the question needs.

### SB021 sensitive or socially desirable behaviour (low)

Detects a short list of topics that people under-report (cheating, theft, illegal acts, drug use, alcohol,
smoking, gambling, arrests, abortion, sexual activity, self-harm, debt, lying, bribery, piracy) or
over-report (voting, giving to charity, attending religious services).

- Before: Have you ever cheated on your taxes? (Yes / No)
- After: no wording fix is enough. At minimum make the question optional and self-completed, frame it
  neutrally ("Some people ... , others ..."), and say truthfully who can see the answer. When the estimate
  matters, an indirect method (a list experiment or randomized response) is a design decision outside this
  check.

Ignore when: the topic is the declared subject of an anonymous study built for it. Rules miss: any topic
outside the list (exercise, recycling, reading, income comparisons).

### SB026 syntax load (low)

Detects two or more of: a conditional clause (if, unless, provided that), an exclusion (excluding, not
counting, other than, except), a parenthetical of five or more words, three or more commas.

- Before: If you train outdoors, how many hours did you train last week, not counting warm-ups, cool-downs,
  stretching (or similar light activity before a session)?
- After: (filter) In the past 7 days, did you train outdoors? (question) In the past 7 days, how many hours
  did you train outdoors? Do not count warm-ups or stretching.

Ignore when: the clause is a definition the question needs and the sentence still reads easily aloud.

## Question rules

### SB017 reference period (low)

- **no_period**: "how often", "how many times/days/hours" or "have you used/contacted/bought/visited ..."
  with no time phrase in the stem.
- **long_window**: a count or frequency question over 12 months or more, "last year", "ever" or "in your
  lifetime".

- Before: How often do you use the mobile app?
- After: In the past 7 days, on how many days did you use the mobile app?

Ignore when: the period is stated in an introduction line just above, or (long_window) the event is rare and
memorable, such as a house purchase. "Have you ever ..." screeners are not flagged.

### SB018 built-in assumption (medium for behaviour, low for experience)

Runs on closed questions only. **behaviour**: "how often", "how many times", "when did you last", "why
do/did you" with no zero answer ("Never", "0", "Does not apply", "I have not ...") and no earlier filter
question. **experience**: "how satisfied" in the same situation, unless the stem says "overall" or "in
general". An earlier yes/no or select-all question that shares a content word counts as a filter.

- Before: How often do you exercise? (Often / Sometimes)
- After: In the past 7 days, on how many days did you exercise? Enter a number from 0 to 7.

Ignore when: the sample is defined by the behaviour (customers who just bought). Rules miss: assumptions in
open questions and in any other wording ("Who treated your headache?").

### SB019 stem and options mismatch (high, medium or low)

- **mismatch** (high): "how satisfied / often / likely / easy" answered by Yes / No, by a scale of another
  kind, or by vague frequency words.
- **closed_stem** (medium): a yes/no question ("Is ...", "Do ...") answered by a rating scale whose words do
  not appear in the stem.
- **one_sided** (low): "how satisfied / likely / easy" over a two-sided scale without naming the other side.

- Before: How satisfied are you with the app? (Yes / No)
- After: How satisfied or dissatisfied are you with the app? (Very satisfied ... Very dissatisfied)

Ignore when (one_sided): a tracker needs the old wording. Rules miss: mismatches in other question families.

### SB020 unlabelled numeric scale (medium)

Detects: answer options that are only consecutive whole numbers starting at 0 or 1, or a `[scale]` question
with no options, when the stem does not say what the numbers mean ("where 1 is ...").

- Before: How easy was it to book a class? (1 / 2 / 3 / 4 / 5)
- After: How easy or difficult was it to book a class? (Very difficult / Somewhat difficult / Neither easy
  nor difficult / Somewhat easy / Very easy). A tracked 0-10 scale such as NPS keeps its end labels so waves
  and benchmarks compare: pass `--keep`.

Counts ("How many cars ...? 0 / 1 / 2 / 3") and years are not flagged.

### SB023 mental computation (low)

Runs on questions that ask for a number. Detects: "on average", "average", "percentage of", "as a
percentage", "what percent/share", "in total", "per year", "annually".

- Before: What is your average monthly spend on fitness as a percentage of your income?
- After: In the past 30 days, about how much did you spend on fitness? (an open amount). Ask income
  separately, in ranges because it is sensitive, and compute the share yourself.

Ignore when: respondents know the figure without calculating (an annual salary).

## Answer-option rules

### SB022 combined opt-out (medium)

Detects: one option that merges two different opt-outs: "None / Other", "Don't know / Prefer not to say",
"N/A or other". "Don't know / Not sure" is one answer and is not flagged.

- After: separate options: Other (please specify) / None of these / Prefer not to say.

### SB028 duplicate option (high)

Detects: the same option text twice in one question (case, spaces and end punctuation ignored).

- Before: Did the update fix the problem? (Yes / Yes / No)
- After: Yes / No / Not sure (check which option the copy replaced; usually a transcription slip).

### SB027 even-point bipolar scale (info)

Notes a two-sided scale with an even number of points and no midpoint. Not a defect: sources differ (see
sources.md). Decide on purpose whether neutral respondents should be forced to one side.

### SB009 unbalanced scale (high; low for excellent/good/fair/poor)

Detects: a rating scale with both positive and negative labels in unequal numbers, or two or more labels on
one side of a "Neither ..." / "Neutral" midpoint and none on the other. "Not at all ..." counts as the zero
point of a unipolar scale, not as a negative label, except beside a "Not very ..." step (Very / Somewhat /
Not very / Not at all likely is balanced). Numbered labels ("1 - Very dissatisfied") are read by their words.

- Before: Very satisfied / Satisfied / Somewhat satisfied / Neutral / Dissatisfied
- After: Very satisfied / Somewhat satisfied / Neither satisfied nor dissatisfied / Somewhat dissatisfied /
  Very dissatisfied

**ladder** (medium): an amount or intensity ladder (a lot, quite a lot, very, somewhat, slightly, not much)
with no zero end ("Not at all", "None", "Never") and more labels at the high end than at the low end. Every
label must be a recognised ladder step, so mixed lists are left alone.

- Before: A lot / Quite a lot / Somewhat / Not much
- After: Not at all / A little / Somewhat / A lot / A great deal

Rules miss: scales whose labels are not in the word lists, and uneven spacing ("Excellent / Good / OK").

### SB010 numeric ranges (high; medium for continuous_gap)

Detects, after sorting the ranges by their start and comparing each with the furthest end seen so far:
**overlap** (a range starts at or below that end), **gap** (a range starts more than one step above it) and
**reversed** bounds. The step is 1, or 0.1 / 0.01 when the options use decimals or the stem asks for cents.
"Under N" excludes N; "N or more" and "N+" include it; "Over N" excludes it; "N to under M" includes N and
excludes M. Negative bounds are read. Up to a third of the options (at least one) may be words the parser
cannot read ("It varies", "Never"); the rest are still checked.

**continuous_gap** (medium): for a continuous measure (hours, minutes, weights, distances, or a "how long"
question in days, weeks, months or years), ranges that meet at whole numbers ("5-6 hours / 7-8 hours")
leave the values in between (6.5 hours) without an option. Counts, ages in years and money are treated as
whole units.

- Before: Under $25,000 / $25,000-$50,000 / $50,000-$100,000 / $100,000-$150,000
- After: Under $25,000 / $25,000-$49,999 / $50,000-$99,999 / $100,000-$149,999 / $150,000 or more
- Before: Less than 1 hour / 1-4 hours / 6-24 hours / More than 24 hours
- After: Less than 1 hour / 1 to under 5 hours / 5 to under 24 hours / 24 hours or more, or ask for the
  number of hours.

Rules miss: a missing open-ended top or bottom range (check by reading: can everyone answer?), ranges with
mixed units ("6 months to 1 year"; skipped), ranges written in words, and ranges listed out of order (the
check sorts them first; read the order yourself).

### SB011 missing answer option (medium or low)

- **none** (medium): a select-all question with no "None of these". Also, at low severity, a single-choice
  "Which ... do you use / have / own" or "Which ... have you used" question with no "None" answer.
- **other** (low): a list of four or more named options with no "Other", or any "Which ... do you use /
  have / own" list of two or more. Comparison stems ("which do you use more", "A or B") are skipped.
- **dk** (low): a yes/no question about a third party ("Does your company ...") with no "Not sure".

- Before: Which of these features have you used? (Select all that apply) Dashboards / Alerts / Reports /
  Integrations
- After: ... Dashboards / Alerts / Reports / Integrations / Other (please specify) / None of these

Ignore when: the list is complete by construction (plans, months), or the question is a screener where
"Not sure" breaks routing. "Don't know" on opinion questions is disputed; see sources.md.

### SB012 inconsistent scales (medium)

- **direction**: a rating scale that runs negative-to-positive when most scales in the questionnaire run
  positive-to-negative, or the reverse. When the two directions are split evenly, the scales that differ
  from the first one are reported and the message says the split is even.
- **length**: the same kind of scale (agreement, satisfaction, ...) with a different number of points than
  the others. "Don't know" and similar options are not counted as points.

- Before: Q11 Strongly agree ... Strongly disagree (5 points); Q12 Strongly disagree / Disagree / Agree /
  Strongly agree (4 points)
- After: use the Q11 scale, in the Q11 order, for both.

Ignore when: the questions come from different validated instruments.

### SB013 too many options (low)

Detects: more than 10 named options (`--max-options`), not counting Other / None / Don't know. Numeric and
rating scales are exempt.

- Fix: group options, use a dropdown with search for long factual lists (country), or randomise the order.

Ignore when: the list is factual and familiar (countries, departments in one company).

### SB014 agree/disagree format (medium for grids, low for single items)

Detects: answer options with both "agree" and "disagree" labels; a grid when the question has lettered rows.

- Before: I would recommend the app to a colleague. (Strongly disagree ... Strongly agree)
- After: How likely or unlikely are you to recommend the app to a colleague? (Very unlikely ... Very likely)
- Before (grid row): The app is easy to use.
- After: How easy or difficult is the app to use? (Very difficult ... Very easy)

Ignore when: the items are a validated instrument, or a tracker needs the old wording.

## Questionnaire rules

### SB015 survey length (medium above 20 minutes, low above 10)

The estimate is always printed. Points: single choice or scale 1; grid 1 per row; select-all 1 per two
options; `[number]` questions 2; open questions 3 (Versta charges 3 per expected phrase or sentence; the
script assumes one, so raise it by hand when a question asks for a paragraph); plus 1 for every three
sentences in a stem; the introduction 1 per three sentences, rounded up. Minutes = points / 8, times 1.5 by
phone; `minutes_rounded` rounds up to the next half minute for the report. Every question is counted
unless `--route-skip` names the questions a respondent on the longest route never sees (Versta counts the
longer of two exclusive paths). Replace the estimate with pilot timings when they exist. The 10- and
20-minute thresholds are the median ideal and maximum lengths reported by one web panel's respondents.

### SB016 sensitive question handling (medium or low)

- **opening** (low): the questionnaire opens with demographic or sensitive questions (income, age, gender,
  race, religion, health, ...). All questions in that opening run are reported.
- **required** (medium): a required question on a sensitive topic (income, race or ethnicity, religion,
  sexual orientation, politics, health, weight, phone number, address) with no "Prefer not to say".

- Before: Q1 What is your annual household income? (required)
- After: move to the end, make it optional or add "Prefer not to say".

Ignore when: the question screens or routes respondents.

### SB024 introduction (medium or low)

Text before the first question is read as the introduction (in JSON: `intro`).

- **leading** (medium): an authority cue ("experts say", "most people") or a statement of what the study
  hopes to find ("we want to show that ...").
- **no_time_estimate** (low): an introduction with no minutes or number of questions.

- Before: Experts say regular exercise matters. We want to show that our members are healthier than most.
- After: This survey is about your exercise habits. It has 13 questions and takes about 4 minutes.

When no introduction is given the script says so and checks nothing; report it under "Not checked".

### SB025 grid and open-question burden (low)

- **grid_rows**: a grid with more than 10 rows (`--max-grid-rows`).
- **open_count**: more than 3 open questions (`--max-open`).
- **open_first**: the first question is open.

A question with no options that asks for a count, an amount, a duration, an age or a year ("how many",
"how much", "how long", "what is your age", "in which year") is numeric entry (2 points), not an open
question, for all of these checks and for the length estimate. The open-question checks are skipped when no question in the input has answer options, because a paste of
bare questions carries no question types. The limits are conventions, not research findings.

## Context flags

- `--mode phone`: the option limit drops to 5 and the grid limit to 5, and the time estimate is multiplied
  by 1.5. Lists and grids must be read aloud and held in memory.
- `--audience expert`: skips SB007, for respondents who use the terms at work.
- `--keep Q7,Q9`: findings on these questions (and their grid rows) are printed as "keep as is" and left out
  of the counts. Use it for validated instruments and tracked questions. An exact ID ("Q7" in JSON, a tag in
  `qsf-convert` Markdown) is matched first; otherwise a leading Q is dropped.
- `--route-skip Q5,Q6`: leaves these questions out of the length estimate only.
- `--language en|other`: by default each stem is checked for English (mostly Latin letters and English
  function words other languages do not share); `en` runs the wording rules on everything, `other` on
  nothing.

## What no rule checks

Review these by reading the questionnaire:

- Order: general questions before specific ones on the same topic; an earlier question that primes a later
  one (a specific behaviour or attribute asked before an overall rating pulls the rating toward it).
- `[multi]` opt-outs ("None of these", "Prefer not to say") set as exclusive in the survey tool; required
  questions with no way out; intro claims (time, anonymity) the questionnaire contradicts; skip logic that
  leads nowhere or routes on a multi-select.
- Nominal lists: should the order be randomised, with "Other" and "None" kept last?
- Ordinal options: are they in a logical order, from low to high or high to low?
- Jargon or vague words inside answer options (SB007 and most of SB006 read the stem only).

- Built-in assumptions outside the SB018 patterns ("Who treated your headache?" assumes a headache and a
  treatment), and assumptions in open questions.
- Social desirability outside the SB021 word list (exercise, recycling, reading).
- Undefined terms ("income": personal or household, before or after tax?), and a reference period in
  question types SB017 does not read.
- Whether the options fit this audience, and whether "Other" would collect most answers.
- Missing open-ended top or bottom ranges.
- Whether each question serves the decision the survey is for.
- Screen layout, mobile rendering and accessibility.
- Any language other than English.

## QAS-99 crosswalk

QAS-99 (Willis & Lessler 1999) has 26 specific yes/no appraisal codes in seven steps and one "other" code in
step 8: 27 decisions. Step 2 has two codes. The code numbers below follow Roberts et al. 2026 (see
sources.md); the short descriptions are ours.

| Code | About | Covered by |
|---|---|---|
| 1a | What the reader must read aloud or silently | agent judgment |
| 1b | Information missing for whoever administers the question | agent judgment |
| 1c | Question hard to read as written | agent judgment |
| 2a | Conflicting or inaccurate introductions and instructions | SB024 (introduction only), agent judgment |
| 2b | Complicated instructions | SB026 on stems, agent judgment for instructions |
| 3a | Lengthy, awkward or complex wording | SB005, SB008, SB026 |
| 3b | Undefined technical terms | SB007 |
| 3c | Vague wording | SB006, agent judgment |
| 3d | Reference period missing or unclear | SB017 no_period |
| 4a | Inappropriate assumptions | SB018, agent judgment |
| 4b | Assumes behaviour is constant | SB003 (partly), agent judgment |
| 4c | Double-barreled | SB001 |
| 5a | Respondent may not know the answer | SB011 dk (narrow), agent judgment |
| 5b | Attitude may not exist | agent judgment |
| 5c | Recall failure | SB017 long_window |
| 5d | Computation needed | SB023 |
| 6a | Sensitive content | SB016, SB021 |
| 6b | Sensitive wording | SB002 (partly), agent judgment |
| 6c | Socially acceptable answer implied | SB002, SB021, SB024 |
| 7a | Open-ended question | SB025 (count and position only), agent judgment |
| 7b | Question and answer categories do not match | SB019 |
| 7c | Technical terms in categories | agent judgment |
| 7d | Vague categories | SB006 options, SB020 |
| 7e | Overlapping categories | SB010 overlap, SB022, SB028 |
| 7f | Missing categories | SB010 gap, SB011, SB018 |
| 7g | Illogical order of categories | agent judgment (SB012 compares direction across questions, not order within one) |
| 8 | Other problems | agent judgment |

Rules with no QAS-99 code: SB004 (hypotheticals), SB009 (balance), SB013 (list length), SB014
(agree/disagree), SB015 (length), SB027 (midpoint).

## Results on the fixtures

These are results on this skill's own fixtures, which were written to exercise the rules. They are not an
accuracy estimate for real questionnaires.

| Fixture | Questions | Hand-listed problems | Found | Missed | Extra |
|---|---|---|---|---|---|
| `flawed.input.md` | 14 | 27 and 1 note | 27 and 1 note | 0 | 0 |
| `gaps.input.md` | 14 | 18 and 1 note | 18 and 1 note | 0 | 0 |
| `mini.input.json` | 4 | 8 | 8 | 0 | 0 |
| `unnumbered.input.txt` | 3 | 1 | 1 | 0 | 0 |
| `clean.input.md` | 12 | 0 | 0 | - | 0 |
| `gaps_clean.input.md` | 10 | 0 | 0 | - | 0 |

False alarms on the two clean fixtures: 0 of 22 questions. The unit tests add a list of 29 single questions that sit
next to a rule and must stay clean, plus negative cases for each of SB017 to SB027; all stay clean.

Unseen questionnaires (four, 38 questions, not kept as fixtures) were also run during development; the
misses and false alarms they exposed became rules and unit tests. That is a handful of surveys read by one
person each, not an accuracy estimate. A unit test in the respondent-view format of `survey-from-decision`
(answer-box tags, routing lines, a closing line) checks that none of them is read as question text.
