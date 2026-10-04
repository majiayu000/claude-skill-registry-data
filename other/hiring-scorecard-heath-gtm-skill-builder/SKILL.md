---
name: hiring-scorecard
description: Turn a GTM opening into a scorecard and an interview kit before you post it. Defines the outcomes the role must hit, the competencies that predict them, the interview questions per competency, and a scoring rubric every interviewer uses. Built for B2B hiring managers, customizable to your role and stage. Trigger on "build a scorecard for this role", "what should I interview for", "score this candidate", "interview kit for an AE", "define the outcomes for this hire", or any GTM hiring prep.
---

# Hiring Scorecard

## What this does
Takes the role you are hiring for and builds the thing you should have before the first interview: a scorecard. It writes the outcomes the person must hit in their first stretch, the competencies that predict those outcomes, a set of interview questions mapped to each competency, and a rubric so every interviewer scores the same candidate on the same scale. You hire against evidence instead of a gut read at the end.

## What you'll need
You do not need to connect anything to get value today. Bring the role and the skill runs now. Connect the tools below and it pulls context automatically and sharpens the outcomes.

- Works today with: the role, the level, the motion it sells into, and a rough sense of what "great in year one" looks like. Paste a job description or just describe it.
- More powerful connected to a CRM: it reads what your current strong performers in the role actually do, so the outcomes are grounded, not generic.
- Sharper with an ATS: it can align the scorecard to your stages and keep every interviewer scoring in one place.
- Sharper with a meeting or notes tool: it can turn interview debriefs into rubric scores instead of loose impressions.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the description you give it today and gets more powerful as you connect tools. It never invents a metric it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: describe the role or paste the job description. The skill builds the full scorecard and interview kit today. No connection required.
- **Connect your tools**: the same skill grounds the outcomes in what your top performers actually do and keeps scores in one place. Same output, less effort, sharper.
- **Just exploring**: no role locked yet? Get the framework, the competency library, and a worked example on a sample AE role, so you can see the shape before you fill it in.

Every run ends with the one thing that would make the next run sharper, a detail to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS GTM org hiring quota-carrying and support roles. Set these to your role:

| Set this | What it is | Default / Example |
|---|---|---|
| ROLE | the opening | AE, SDR, CSM, Sales Manager, RevOps |
| LEVEL | seniority | mid-market AE, enterprise AE, team lead |
| MOTION | what they sell into | inbound, outbound, expansion, renewal |
| RAMP_WINDOW | when outcomes are judged | first 90 / 180 / 365 days |
| COMPETENCIES | the traits you weight | pick 5-6 from the library, or add yours |
| ATS | your applicant tracking system | Greenhouse, Lever, Ashby |
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| SCORE_SCALE | the rubric range | 1-4 (forces a call, no safe middle) |

Weight the competencies for your motion. An outbound SDR and an expansion CSM do not share a top competency, so do not score them on the same one.

## The method

### Outcomes first
Before competencies, the scorecard names 3 to 5 outcomes the hire must produce inside the RAMP_WINDOW, written as results, not activities. "Sourced pipeline covering quota by day 90," not "does prospecting." Outcomes are what you are actually buying. Everything else predicts them.

### Competencies that predict the outcomes
For each outcome, name the 1 or 2 competencies that predict it, drawn from a library: prospecting rigor, discovery depth, deal control, multi-threading, forecasting honesty, coachability, customer empathy, commercial judgment. Cap the list at 5 or 6. A scorecard that weights everything weights nothing.

### Questions per competency
Each competency gets 2 or 3 interview questions, behavioral and past-tense, plus what a strong answer sounds like and what a weak one sounds like. Behavioral because past behavior predicts, and the "strong vs weak" note keeps interviewers from grading on charisma.

### Scoring rubric
A shared rubric on the SCORE_SCALE, with each competency defined at each level so a 3 means the same thing to every interviewer. An even scale forces a call and kills the safe middle. Each interviewer scores only the 1 or 2 competencies they own, so the debrief is coverage, not repetition.

### Interviewer assignment
The kit assigns competencies across the loop so every one is covered by someone and no candidate is graded twice on the same thing. The hiring manager owns outcomes fit. Coverage over consensus.

## Quality gates
- Outcomes are written as results with a date, never as activities.
- Competencies are capped at 5 or 6, each tied to an outcome it predicts.
- Every question is behavioral and past-tense, with a strong-answer and weak-answer note.
- The rubric scale is even, so no interviewer can hide in the middle.
- Every competency is assigned to a named seat in the loop.

## Output (example)
```
SCORECARD · Mid-Market AE · judged at day 180

Outcomes:
  1. Self-sourced pipeline at 3x quota by day 120
  2. First closed-won by day 90
  3. Forecast within 15% by second full quarter

Competencies (weighted):
  Prospecting rigor      -> outcome 1   (owner: SDR manager)
  Discovery depth        -> outcome 2   (owner: hiring manager)
  Deal control           -> outcome 2   (owner: peer AE)
  Forecasting honesty    -> outcome 3   (owner: sales leader)
  Coachability           -> all         (owner: hiring manager)

Sample question (Discovery depth):
  "Tell me about a deal you lost. When did you first know, and what
   had you not asked?"
  Strong: names the missing question, owns it, changed their process.
  Weak: blames budget, timing, or the champion leaving.

Rubric: 1-4 per competency. Advance only on avg >= 3 with no 1s on
a weighted competency.
```

## Where the numbers come from
The RAMP_WINDOW, the 3x pipeline target, and the 1-4 scale are examples for illustration, not benchmarks. They suited a mid-market SaaS AE. Set outcomes to your own ramp and quota, and pick a scale your interviewers will actually use. The framework does not change. The bar is yours.

## Example chat
Here is the skill running on a real req, start to finish.

**You:** I'm opening a Mid-Market AE req. Build me the scorecard before I post it.

**Claude:** Here's the outcomes-first scorecard, ramp window set to 180 days.
```
Outcomes:
  1. Self-sourced pipeline at 3x quota by day 120
  2. First closed-won by day 90
  3. Forecast within 15% by second full quarter

Competencies (weighted):
  Prospecting rigor   -> outcome 1   (owner: SDR manager)
  Discovery depth     -> outcome 2   (owner: hiring manager)
  Forecasting honesty -> outcome 3   (owner: sales leader)
```
The competency I'd watch hardest is forecasting honesty. It's the one outcome nobody screens for in a resume, and it's the one that burns a manager six months in. One sharpener: connect your CRM and I'll pull what your current top AE actually did in their first 180 days, so outcome 1 is grounded in your real ramp instead of a 3x rule of thumb.

## Go further
The scorecard is step one. Here is where an operator takes it once the manual version proves out.

- **Score every candidate the same way, automatically.** Feed interview notes from Gong or a meeting tool into a scheduled Claude task that scores each competency against the rubric and writes it to Greenhouse or Lever.
- **Catch drift before the debrief.** DM the hiring manager in Slack the moment two interviewers score the same competency more than one point apart.
- **Close the loop with real performance.** Pull 90-day and 180-day actuals from Salesforce and compare them to the outcomes you wrote, so next quarter's scorecard is calibrated on your own hires, not a guess.

You built the bar once, now every interview gets held to it.


## Make it yours
Fork it. Change the outcomes, the competency weights, the questions. The point is not to interview against someone else's idea of the role. It is to hire against yours, consistently, so the debrief is about evidence instead of who liked the candidate most. Built by an operator. Customize it, break it, make it better.
