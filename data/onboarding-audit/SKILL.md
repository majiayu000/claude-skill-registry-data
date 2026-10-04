---
name: onboarding-audit
description: Score the experience a new customer actually has, not just whether they activated. Grades the first 90 days on the moments that make someone feel taken care of, finds where the welcome goes cold, and hands back a scored audit with the specific fixes. Built for any post-sale team, customizable to your product and lifecycle. Trigger on "audit my onboarding", "score our onboarding experience", "why do new customers churn early", "grade our first 90 days", "where does onboarding go cold", "is our welcome any good", or any onboarding-quality question.
---

# Onboarding Audit

## What this does
Grades the experience a new customer actually has, not just whether a checkbox got ticked. Most onboarding scoring measures activation: did they log in, did they finish setup. This scores the feeling: were they expected, were they guided, did anyone notice when they went quiet. It walks the first 90 days moment by moment, scores each one, and hands back the specific places the welcome went cold and what to do about it. In commoditized software the experience is the moat, so this measures the moat.

## What you'll need
You do not need to connect anything to get value today. Describe your onboarding and the skill scores it now. Connect your tools and it grades against what customers actually did, not what the playbook says should happen.

- Works today with: a walk-through of your onboarding, the emails, the setup steps, the human touches, the first 90 days as a customer experiences them. Paste it and go.
- More powerful connected to a product-analytics tool: it sees where real customers stall versus where the playbook assumes they sail through.
- Sharper with a CRM or CS tool: it reads the human touches that actually happened, the calls, the check-ins, the silences.
- Sharper with support or survey data: it hears the friction in the customer's own words.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you describe today and gets sharper as you connect tools. It never scores a touch that did not happen, and never assumes a step landed just because it was sent. A gap is a prompt, not a guess.

- **Bring your data**: walk through your onboarding. The skill scores the full experience today and names the cold spots.
- **Connect your tools**: the same skill grades against real behavior and real touches, so the score reflects what customers lived, not the flowchart.
- **Just exploring**: no onboarding to show yet? Get the scoring rubric, the moments it grades, and a worked example, so you see the shape before you audit.

Every run ends with the one thing that would sharpen the next audit, a moment to instrument or a tool to connect.

## Customize this for yourself
This was built to be lifecycle-agnostic. Set these to your motion:

| Set this | What it is | Default / Example |
|---|---|---|
| LIFECYCLE | your onboarding window | first 30 / 60 / 90 days |
| MOMENTS | the touchpoints you grade | welcome, kickoff, first value, habit, check-in |
| VALUE_EVENT | the moment they first get value | your product's aha moment |
| HUMAN_TOUCHES | where a person shows up | kickoff call, check-in, QBR |
| SIGNALS | how you see a customer stalling | login gap, setup abandon, support spike |
| VOICE | the feeling you want to leave | your brand's version of "taken care of" |

The rubric is yours. The point is to grade the experience your customers should feel, not a generic checklist someone else outgrew.

## The method

### Score the moments, not the checkboxes
Walk the first 90 days as the customer lives it: the welcome, the kickoff, the first real value, the habit forming, the first check-in. Each moment gets a score on two axes: did it happen, and did it feel like someone was expecting them. A completed setup with no human warmth scores lower than it looks.

### Find where the welcome goes cold
Name the exact moment the attention drops off. For most teams it is right after setup: the sale got all the energy, activation got a sequence, and then the customer is alone. That cold spot is where early churn is born, and it has a location you can point to.

### Grade the human touches
Automation onboards; people make customers feel chosen. Score where a human actually shows up versus where the customer is handed to a drip. A high-value customer getting a templated welcome is a scored miss, not a nice-to-have.

### Catch the silent stall
Score whether anyone notices when a new customer goes quiet. The worst onboarding failure is invisible: they stopped, and no one reached out, because no signal was wired to a human. If the stall is silent, that is the finding.

### Turn the score into fixes
Every low-scoring moment ends in a specific move: the touch to add, the signal to wire, the human to insert. Not "improve onboarding." The exact cold spot and the exact fix.

## Quality gates
- Every graded moment scores both dimensions: did it happen, and did it feel intentional.
- The cold spot is named with a location, never "onboarding could be better."
- Human touches are scored separately from automation, never blended into one number.
- The silent-stall check is explicit: is a quiet customer noticed, yes or no.
- Every low score ends in a specific fix, never a generic recommendation.

## Output (example)
```
ONBOARDING AUDIT · [your product] · first 90 days

Moment              Happened   Felt intentional   Score
Welcome             yes        templated          2/5
Kickoff call        yes        warm, tailored     5/5
First value         partial    no guidance        2/5
Habit forming       no         -                  1/5
Day-30 check-in     no         -                  0/5

COLD SPOT: right after first value. The kickoff is great, then the
customer is alone. No habit nudge, no Day-30 human touch.

SILENT STALL: not caught. No signal wired to a human when a new
account goes quiet in week 3.

FIXES:
  1. Wire a week-3 inactivity signal to the CSM, not a drip.
  2. Add a habit nudge tied to the aha moment, day 7 to 14.
  3. Make the Day-30 check-in a human note, not an NPS survey.

Onboarding experience score: 2.0 / 5 (strong start, cold finish)
```

## Example chat
Here is the skill grading a real onboarding, moment by moment.

**You:** Audit our onboarding. New customers get a welcome email, a setup wizard, a kickoff call, then an automated 5-email drip over 30 days. Renewal's at month 12.

**Claude:** Scored it as the customer lives it, not as the flowchart draws it:
```
Welcome email     templated, no name of a human      2/5
Setup wizard      works, but no one watching          3/5
Kickoff call      the bright spot, warm and tailored  5/5
Day 1-30 drip     automated, same for everyone        2/5
```
The cold spot is obvious: your kickoff call is excellent, and then the customer falls into a drip that treats a $50k account the same as a free trial. The feeling goes from "chosen" to "processed" in a week. And the silent stall is not caught: if they stop logging in during the drip, nothing routes to a human.

**You:** So what would actually move it?

**Claude:** Three moves. Replace the day-14 drip email with a real check-in from the CSM who ran the kickoff, so the warmth carries. Wire an inactivity signal so a quiet account in week 3 pings a human, not an autoresponder. And make the day-30 touch a "here's what you've gotten to so far" note instead of a survey. One sharpener: connect your product-analytics tool and I'll show you exactly which day the average new account goes quiet, so the check-in lands the day before, not a week after.

## Go further
The audit is step one. Here is where an operator takes it once the score is real.

- **Wire the silent stall to a human.** Have a scheduled Claude task read Amplitude or your warehouse nightly and DM the CSM in Slack the new accounts that went quiet this week, so no welcome ever goes cold unnoticed.
- **Score every new cohort, not just once.** Re-run the audit each month against the latest cohort so a regression in the experience shows up as a dropping score, not as churn three months later.
- **Feed the cold spot into the offboarding side.** Hand the findings to an offboarding audit so you can see the full arc: how you greet them and how you say goodbye, and whether the two match.

You grade the welcome once, then keep it warm on purpose.

## Where the numbers come from
The moments, the window, and the scoring bar are yours to set. The examples here suited a 90-day mid-market onboarding. A self-serve motion compresses the window; an enterprise motion stretches it. The logic, score the feeling not the checkbox, find the cold spot, catch the silent stall, does not change.

## Make it yours
Fork it. Change the moments, the window, the rubric, the voice. The point is not to grade someone else's onboarding. It is to measure whether your customers feel taken care of, and to find the exact place they stop. Built by an operator. Customize it, break it, make it better.
