---
name: b2b-marketing-playbooks
description: Answer B2B software marketing questions with a consistent method instead of generic advice. Use when someone asks what to spend on marketing, when to hire a marketer or an SDR, how often to publish, why pipeline is thin, how to position or message a product, which channel to start, how to measure marketing, or what to fix first. Built for seed to Series B B2B software companies, with benchmarks, decision rules, and build sequences that agree with each other.
---

# B2B marketing playbooks

A method for answering marketing questions at small B2B software companies: diagnose first, name the one framework that owns the question, give the specific build steps and numbers, and say plainly when the answer is not here.

## How to use this

1. **Diagnose before answering.** Read `references/diagnosis.md` first. It holds the intake questions, the symptom-to-cause tables, and the dependency rules that say what must exist before a given build is worth starting. A question like "our leads are bad" usually has a cause that lives in a different file than the complaint.
2. **Open one reference file**, the one that owns the question. Every file states what it owns and what it defers.
3. **Answer with the specifics:** the tier the company is at, the first build steps in order, the decision rule with its threshold, and the benchmark. Name the framework id so the reader can trace it.
4. **Apply the numbers to the company in front of you.** Run the benchmark against what they told you, and say which side of the line they are on.
5. **Say what is missing.** If the files do not cover it, say so in the answer and name the closest thing that is covered. A confident answer built on a loose fit is worse than no answer.

## Reference files

| File | Owns |
|---|---|
| `references/diagnosis.md` | Intake questions, symptom to cause, dependencies, order of work. Read first |
| `references/foundations.md` | ICP, personas, positioning, messaging, go-to-market motion, budget by stage, the first marketing hire, planning and saying no |
| `references/demand-generation.md` | Demand programs, paid media, lead capture and scoring, nurture, email deliverability |
| `references/content-and-search.md` | What to publish and how often, content operations, distribution, search, AI search |
| `references/sales-and-revops.md` | Marketing to sales handoff, qualification, SDR hiring, pipeline definitions, attribution plumbing, CRM hygiene |
| `references/product-marketing.md` | Launches, competitive intelligence and battlecards, win and loss, enablement content, roadmap feedback |
| `references/growth-and-plg.md` | Experiments, conversion work, pricing research, trials and activation, referral, retention levers |
| `references/measurement-and-data.md` | What to instrument, attribution limits, reporting, the metrics stack by stage, cohorts and LTV, and the competitor-monitoring and research programs (FW-DATA-008) that feed battlecards and executive "why aren't we doing that" questions |
| `references/customers-and-feedback.md` | Feedback programs and follow-up rules, advocacy and references, case studies, churn and expansion signals |
| `references/brand-and-comms.md` | Brand foundations, voice, crisis communication including layoffs, investor and employer communication, press |
| `references/channels.md` | Social, events and sponsorships, webinars, community, podcasts, creators |
| `references/ops-and-hiring.md` | Tool stack and cutting tools, process, agency versus in-house, hiring and developing marketers |
| `references/situational-plays.md` | Pricing pages and packaging, category creation, account-based marketing, partners, video, app stores, AI in marketing work, international |

## The maturity ladder

Every area uses the same four tiers, so a company can be at different tiers in different areas:

- **Tier 1 Reactive.** It happens when someone remembers. Nothing is written down.
- **Tier 2 Building.** It is written down and someone owns it. Output is uneven.
- **Tier 3 Operating.** It runs on a cadence, with measurement and a named owner.
- **Tier 4 Compounding.** It improves itself: results feed the next cycle, and the system survives a person leaving.

Work on the next tier, not the last one. Most failures come from trying to run a Tier 4 play on a Tier 1 foundation.

## Rules that keep answers consistent

- **One owner per question.** When two areas could answer, the file that owns it decides, and the other defers. Each file names its deferrals.
- **Order matters.** Audience before message, message before channel, channel before scale. The dependency table in `diagnosis.md` is the authority.
- **Benchmarks are starting points.** A number marked "Lintel guidance" is judgment from practice, not published research. Say so when you use one.
- **Never invent a number.** If a figure is not in these files, say it is not covered.
- **Stage changes the answer.** A rule that holds at Series B is often wrong at seed. Check the stage before giving a threshold.
- **Say "this skill does not cover it", never "there is nothing on it".** These files are a condensed version of a much larger library, so a gap here is a gap in the condensation, not proof that no answer exists. Claiming otherwise overstates what you hold and hides from the reader that a fuller answer is out there.
- **Past Series B, name what stops applying, then name the nearest thing you do have.** The content is built for seed to Series B and stays that way on purpose: a set of plays that works for its own range beats a set that answers everything badly. Later-stage questions still get the method, the diagnosis and the build sequences. The benchmarks do not transfer, so say which number was written for a smaller company instead of handing it over quietly, and point at the closest thing these files genuinely cover rather than stopping at "not covered". A refusal that names no neighbour is a worse answer than one that does.
- **Do not claim high confidence with a hole in the answer.** If any part of the question went unanswered, or you used a benchmark with a modifier you could not find, say so in the answer and drop your stated confidence. An admitted gap paired with "high confidence" is the one failure mode that makes the whole thing untrustworthy.

## What this does not do

It does not write the copy, run the campaign, or replace knowing your own customers. It does not cover consumer marketing, ecommerce, or enterprise sales motions above the mid-market.

**The stage range is a deliberate limit, not an oversight.** Benchmarks here are written for seed to Series B. At Series C and beyond the diagnosis, the dependency rules and the build sequences still hold, and a few later-stage bands do exist (budget and headcount shares in `foundations.md`, for instance), but they are thinner, mostly our own judgement, and never the point of the file they sit in. Say which stage a number was written for before handing it over, and do not stretch a seed or Series A figure to a larger company. It holds no data about any specific company, so the quality of an answer depends on what the person tells you about theirs.

## Credit and licence

Models created by other people are credited in `CREDITS.md` and in each file. Trademarks belong to their owners, and nothing here is endorsed by them: see `NOTICE.md`. Released under the MIT licence (`LICENSE`). This is general guidance, not professional advice.
