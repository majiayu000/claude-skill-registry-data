# Survey bias check: method sources

Checked against the sources on 2026-11-12; the QAS-99 figures were re-read on 2026-11-19. "Read" means the source text itself was read; "abstract" means
only the abstract or a publisher summary was reachable. Numbers
with no source are under "Conventions".

## Sources

Main sources (the rules rest on these):

1. **Krosnick & Presser 2010**, "Question and Questionnaire Design", in Marsden & Wright (eds.),
   *Handbook of Survey Research*, 2nd ed., Emerald, pp. 263-313. Read.
   https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2010/2010%20Handbook%20of%20Survey%20Research.pdf
2. **Pew Research Center**, "Writing Survey Questions". Read.
   https://www.pewresearch.org/our-methods/u-s-surveys/writing-survey-questions/
3. **Harvard University Program on Survey Research**, "Tip Sheet on Question Wording" (C. Harrison, updated
   17 Nov 2007). Read. https://psr.iq.harvard.edu/book/questionnaire-design-tip-sheet
4. **Duke Initiative on Survey Methodology**, "Tipsheet: Question Wording" (P. R. Miller). Read.
   https://dism.duke.edu/files/2020/05/Tipsheet-Question_Wording.pdf
5. **Versta Research**, "How to Estimate the Length of a Survey". Read. A practitioner method, not a
   peer-reviewed one. https://verstaresearch.com/newsletters/how-to-estimate-the-length-of-a-survey/
6. **Revilla & Ochoa 2017**, "Ideal and Maximum Length for a Web Survey", *International Journal of Market
   Research* 59(5): 557-565, https://doi.org/10.2501/IJMR-2017-039. Figures read as reported in
   **Revilla & Höhne 2020**, "How long do respondents think online surveys should be?", *IJMR* 62(5):
   538-545, https://doi.org/10.1177/1470785320943049 (read).
7. **Roberts, Sturgis, McGee, Hamlyn, Minichino & Robinson 2026**, "Survey question evaluation at scale:
   applying large language models to the QAS-99", Survey Futures Working Paper no. 22, University of Essex.
   Read (a working paper, not yet peer-reviewed).
   https://www.iser.essex.ac.uk/wp-content/uploads/files/working-papers/survey-futures/sf-wp-22-survey-question-evaluation-scale-applying-llm-to-qas-99.pdf

Supporting sources:

- Willis & Lessler 1999, *Question Appraisal System QAS-99*, Research Triangle Institute: the origin of the
  27 appraisal decisions (26 codes in steps 1 to 7, one "other" in step 8; Table 3 of source 7 lists the
  number per step: 3, 2, 4, 3, 4, 3, 7, 1). Known here only through source 7.
- Graesser, Cai, Louwerse & Daniel 2006, "Question Understanding Aid (QUAID): A web facility that helps survey
  methodologists improve the comprehensibility of questions", *Public Opinion Quarterly* 70(1): 3-22. Known through source 1, which lists its
  five problem classes (unfamiliar technical terms, vague or imprecise predicate or relative terms, vague or
  imprecise noun phrases, complex syntax, working memory overload). The earlier tool paper is Graesser et al.
  2000, *Behavior Research Methods, Instruments, & Computers* 32,
  https://link.springer.com/article/10.3758/BF03207792 (not read; the page redirects to a sign-in).
- Saris, Revilla, Krosnick & Shaeffer 2010, "Comparing Questions with Agree/Disagree Response Options to
  Questions with Item-Specific Response Options", *Survey Research Methods* 4(1): 61-79. Abstract.
  https://ojs.ub.uni-konstanz.de/srm/article/view/2682
- Krosnick et al. 2002, "The Impact of 'No Opinion' Response Options on Data Quality", *Public Opinion
  Quarterly* 66: 371-403, https://doi.org/10.1086/341394. Abstract.
- Galesic & Bosnjak 2009, "Effects of Questionnaire Length on Participation and Indicators of Response
  Quality in a Web Survey", *Public Opinion Quarterly* 73(2): 349-360. Abstract.
- Décieux, Mergener, Neufang & Sischka 2015, "Implementation of the forced answering option within online
  surveys", *Psihologija* 48(4): 311-326, https://doi.org/10.2298/PSI1504311D. Abstract.
- Murphy, Allen, Stevens & Weatherhead 2005, "A Meta-analysis of Hypothetical Bias in Stated Preference
  Valuation", *Environmental and Resource Economics* 30(3): 313-325. Abstract.
- SQP 3.0 (Survey Quality Predictor), GESIS, https://sqp.gesis.org: predicts the reliability and validity of
  a question from its formal and linguistic characteristics. A complement to this linter, not a source.

## Rules and what supports each

| Rule | What the source says | Source |
|---|---|---|
| SB001 double-barreled | "Ask about one thing at a time (avoid double-barreled questions)". Common phrases with "and" that name one concept ("free and fair elections") are not double-barreled. | 1 (p. 264), 2, 3, 4 |
| SB002 leading or loaded | "Avoid leading or loaded questions that push respondents toward an answer"; avoid "loaded, leading, emotional, or evocative language"; balance the question so that both answers are acceptable. | 1, 3, 4 |
| SB003 absolutes | Practitioner advice only: absolutes such as "always", "all", "every" corner the respondent in yes/no questions. | SurveyMonkey guide (below) |
| SB004 hypotheticals | Stated values for hypothetical choices exceed actual ones: median ratio of hypothetical to actual value 1.35 across 83 observations. The ratio is about monetary valuations; it sets no bound on purchase probability, so the skill reports stated intent as stated intent and never as an upper bound or a forecast. | Murphy et al. 2005 |
| SB005 negations | "Avoid questions with single or double negations." Pew's example: "do you favor or oppose not allowing gays and lesbians to legally marry". | 1, 2 |
| SB006 vague quantifiers | "Avoid words with ambiguous meanings"; wording should be "specific and concrete". | 1, 3 |
| SB007 jargon | "Use simple, familiar words (avoid technical terms, jargon, and slang)"; avoid "unfamiliar abbreviations or jargon". | 1, 2, 3, 4 |
| SB008 long question | 20 words ("Most questions can be composed in twenty words or less"), attributed to Payne 1951. Source 4 gives no number: "Strike a balance between too many and too few words." | Payne 1951 via DePaul handout |
| SB009 unbalanced scale | Choose labels "that divide up the continuum into approximately equal units"; make positive and negative responses equally acceptable. | 1 (section 9.4), 4 |
| SB010 numeric ranges | "Make response options exhaustive and mutually exclusive"; for a continuum "word your categories as a range". The continuous_gap check applies the same requirement to measures that take values between whole numbers; its medium severity is a convention. Open numbers are preferred for quantities (source 1, section 9.2: "open questions are usually preferable to closed items for measuring quantities"), which is why rewrites turn counts into open numbers. | 1, 3 |
| SB011 missing option | Options must be exhaustive; "it's often a good idea to include an 'Other-Specify' category". "Don't know" is disputed (below). | 1, 3 |
| SB012 inconsistent scales | Not stated as a rule in any source read; follows from "wording that all respondents will interpret in the same way". | 1 (indirect) |
| SB013 too many options | Pew: "the number of answer choices should be kept to a relatively small number – just four or perhaps five at most", mainly for opinion questions read aloud; facts and demographics can have more. On screen, respondents "tend to choose items at the top of the list". Phone mode uses Pew's 5; the web limit of 10 is a convention. | 2 |
| SB014 agree/disagree | "an acquiescence effect averaging about 10%"; "a better approach to eliminating acquiescence is to avoid using agree/disagree, true/false, and yes/no questions altogether". Item-specific questions gave higher-quality answers in a split-ballot multitrait-multimethod study. | 1 (section 9.5), Saris et al. 2010, 2 |
| SB015 length | Points: simple question 1; grid 1 per row; multi-select 1 per two options; answer needing mental calculation 2 (the script gives every numeric-entry question 2, a simplification); open end 3 per short phrase or sentence (the script assumes one); 1 per three sentences of reading, which the script applies to stems and to the introduction; count the longer of two mutually exclusive paths (`--route-skip`). Online minutes = points / 8 (7.5 seconds per point); phone = online x 1.5. Thresholds: median ideal 10 minutes, median maximum 20 minutes, as reported by respondents of one opt-in web panel (Mexico); a German replication found 10-15 and 20-28 minutes. The longer the stated length, the fewer start and finish. | 5, 6, Galesic & Bosnjak 2009 |
| SB016 sensitive handling | "Questions on sensitive topics that might make respondents uncomfortable should be placed at the end of the questionnaire"; "Demographic questions such as income, education or age should not be asked near the beginning of a survey" unless needed for eligibility or routing. Forcing answers raises drop-out. | 1 (p. 264), 2, Décieux et al. 2015 |
| SB017 reference period | "Provide Reference Frames ... 'How often have you felt sad during the past week?'". "One common way of simplifying the task is to shorten the reference period. Respondents will have an easier time recalling how often they have seen a physician in the last month than in the last year". QAS-99 codes 3d and 5c. No source gives a cut-off; the 12-month trigger is a convention. | 3, 1 (section 9.8), 7 |
| SB018 built-in assumption | "Avoid erroneous assumptions" (the headache example: ask first whether it happened). "Filter questions should be included, to avoid asking respondents questions that do not apply to them." QAS-99 code 4a. | 4, 1 (p. 264), 7 |
| SB019 stem and options | QAS-99 code 7b (question and categories do not match); balance: "explicitly including disagreement language in the question itself" ("support or oppose"). | 7, 4 |
| SB020 unlabelled scale | "reliability is higher when all points are labeled with words than when only some are"; numbers alone must be interpreted by the respondent. | 1 (section 9.4) |
| SB021 sensitive behaviour | "respondents understate alcohol and drug use, tax evasion and racial bias"; they "may overstate church attendance, charitable contributions and the likelihood that they will vote". QAS-99 codes 6a-6c. | 2, 7 |
| SB022 combined opt-out | "Make response options exhaustive and mutually exclusive" applied to opt-out options. No source read discusses merged opt-outs specifically. | 1 (by extension) |
| SB023 mental computation | "Avoid asking respondents to make any calculations beyond counting simple events in their heads"; "Scales that ask respondents to make complex calculations can cause problems". QAS-99 code 5d. | 4, 3, 7 |
| SB024 introduction | Leading wording as for SB002. QAS-99 step 2 covers introductions and instructions. Stated length changes who starts (Galesic & Bosnjak 2009), which is evidence that length matters to respondents, not a rule to state it: the time-estimate check is a convention. | 1, 7 |
| SB025 grid and open burden | Open ends cost 3 points against 1 for a closed question, and each grid row costs 1 (source 5). "Early questions should be easy and pleasant to answer". QAS-99 code 7a. The limits (10 rows, 3 open questions) are conventions. | 5, 1 (p. 264), 7 |
| SB026 syntax load | "Use simple syntax"; "Avoid Complex Sentences. Sentences with too many clauses or unusual constructions often confuse respondents." QUAID flags complex syntax and working memory overload. The signal counts are conventions. | 1, 3, 4, Graesser et al. 2006 via 1 |
| SB028 duplicate option | Options must be mutually exclusive; QAS-99 code 7e (overlapping categories). | 1, 7 |
| SB027 even-point scale | Omitting the middle alternative led respondents "to randomly select one of the moderate scale points ... This suggests that offering midpoints is desirable." Information only; see disagreements. | 1 (section 9.3) |

The SurveyMonkey guide for SB003: "5 common survey question mistakes that'll ruin your data",
https://www.surveymonkey.com/mp/5-common-survey-mistakes-ruin-your-data (vendor guide, read as a search
excerpt only).

### Why rules for these areas

Source 7 had a language model (LLM 1), a novice and an expert code 118 draft questions on the 27 QAS-99
decisions. Flagging rates on all 118 questions (share of possible problems flagged, as the paper's text
rounds Table 3), model / novice / expert: instructions 5% / 14% / 29%; sensitivity 8% / 28% / 46%; response
categories 7% / 16% / 37%. Overall agreement between the model and the expert was 63%. On a separate validation subset of 30
questions, coded by two models, two novices and three experts, the knowledge and recall step was flagged at
9% and 18% by the models, 27% and 17% by the novices and 32%, 20% and 34% by the experts (Table 3; the
paper's text rounds these to 8%, 18%, 18-30% and 20-31%). The paper names its models inconsistently: GPT-4
and Claude Sonnet 4.6 in the method and Table 2, GPT-4o and Claude 3.5 Sonnet under Table 3. A language
model reading a questionnaire unaided under-flags exactly these areas, which is why SB010, SB011 and SB017
to SB025 exist as mechanical checks. The reference coder in the main set is one expert, and the paper is a
working paper.

### Order guidance (agent judgment, not script rules)

- General before specific: "Questions on the same topic should proceed from general to specific"; group
  questions on one topic (source 1, p. 264).
- Easy and on-topic first; difficult or sensitive items not early (source 1).
- Earlier questions "can unintentionally provide context for the questions that follow" (source 2).
- Nominal lists: source 2 randomises many option sets, because on screen people favour the top of a list
  and by phone the end. Keeping "Other" and "None" fixed at the bottom is a convention.
- Rating scales keep their order: "it makes no sense to completely randomize the order in which scale
  points are presented" (source 1); "each point should be clearly higher or lower than the other" (source 3).
- A specific question (a behaviour, an attribute) before an overall rating can prime the rating; this is
  source 2's context effect applied to one common case. The skill leaves the order to judgment and sets no
  rule.

### Pretesting

"No matter how closely a questionnaire follows recommendations based on best practices, it is likely to
benefit from pretesting: a formal evaluation carried out before the main survey" (source 1, section 9.10).
The script's closing line rests on this. No number of pretest respondents is given because none was verified.

## Conventions (this tool's defaults, no source)

| Constant | Value | Flag |
|---|---|---|
| `MAX_OPTIONS` (SB013, web) | 10 | `--max-options` |
| `MAX_GRID_ROWS` (SB025) | 10; 5 in phone mode | `--max-grid-rows` |
| `MAX_OPEN` (SB025) | 3 open questions | `--max-open` |
| Long recall window (SB017) | 12 months or more, "last year", "ever" | none |
| Syntax load (SB026) | 2 or more of: conditional, exclusion, parenthetical of 5+ words, 3+ commas | none |
| Missing time estimate (SB024) | any introduction without minutes or a question count | none |
| Continuous gap (SB010) | medium severity; continuous = time, weight, distance or volume units, or "how long" with days to years | none |
| Ranges with words (SB010) | up to a third of the options (at least one) may be unparsed words; mixed time units skip the check | none |
| English check | over 80% Latin letters; 1 English-only function word for 3 to 7 words, 2 above; 2 words or fewer pass | `--language` |
| Unmarked options | two or more lines of 8 words or fewer after a stem ending in "?" | none |
| Reported length | minutes rounded up to the next half minute | none |

Sourced constants: `MAX_WORDS = 20` (secondhand), `PHONE_MAX_OPTIONS = 5` (source 2), `POINTS_PER_MINUTE = 8`,
points 1 / 1 per row / 1 per two options / 2 / 3, `SENTENCES_PER_POINT = 3`, `PHONE_TIME_FACTOR = 1.5`
(source 5), `IDEAL_MINUTES = 10`, `MAX_MINUTES = 20` (source 6).

## Where practitioners disagree

- **"Don't know" options.** Krosnick et al. 2002 found, over nine experiments, that leaving out a no-opinion
  option did not lower data quality and that offering one can hide real opinions. Others add it so that
  people without the knowledge are not forced to guess. The script suggests "Not sure" only for a yes/no
  question about a third party (an employer, a household).
- **Midpoints and number of points.** Krosnick & Presser conclude that "7-point scales are probably optimal
  in many instances", that gains level off "after about 7 points" and that a midpoint is desirable. Some
  practitioners drop the midpoint to force a direction, and many product surveys use 5 points or 0-10. The
  script notes an even-point bipolar scale (SB027, information only) and never judges scale length itself.
  The pack's default for a new scale (7 points bipolar, 5 unipolar, every point labelled; shared with
  `survey-from-decision`) is a convention built on that chapter, which does not state the 5/7 split. A
  rewrite that rebalances an existing scale keeps its length so it still matches the survey's other scales.
- **Ranges or open numbers.** Source 1 prefers open questions for quantities, because the cut points of
  ranges shift answers. Ranges stay common for income (sensitive) and for amounts people can only estimate.
  The pack asks counts as open numbers and keeps ranges for those cases.
- **Agree/disagree.** Still the most common format in product surveys, and needed when a validated
  instrument (for example SUS) uses it. Keep a validated instrument intact (`--keep`).
- **One-sided stems.** "How satisfied are you ...?" is standard in CSAT trackers; source 4 prefers naming
  both sides. SB019 reports it at low severity.
- **Unbalanced scales.** "Excellent / very good / good / fair / poor" is unbalanced on purpose and widely
  used for self-rated health; reported at low severity.
- **Question length.** Longer wording with a definition or a reference period can measure better (source 3:
  defining income "will lengthen the question, but ... makes the question more precise").
- **Length estimates.** Vendors use different seconds-per-question rules. The Versta figure is a planning
  heuristic; a timed pilot replaces it.
- **Replicating earlier wording.** A flawed question may be worth keeping unchanged when comparison with
  earlier data matters (source 1, section 9.11).

## Pitfalls

- Reporting pattern hits as defects. Report candidates, then judge each one.
- Flagging "and" inside one concept ("terms and conditions") or inside answer options.
- Treating every unbalanced scale, long question or agree/disagree item as an error.
- Suggesting "Don't know" on screeners or factual questions where it breaks routing.
- Running English word lists on other languages; such questions are reported as unchecked.
- Rewriting a validated or tracked question without telling the user what comparability is lost.
- Trusting the length estimate for surveys with heavy skip logic; it counts every question.
- Treating a clean lint as proof: a desk review does not replace a pretest.
