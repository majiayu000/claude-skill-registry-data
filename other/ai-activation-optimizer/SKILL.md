---
name: ai-activation-optimizer
description: "Produces an activation diagnosis and onboarding redesign for Artificial Intelligence (AI) products where output quality varies by user input: an aha-moment definition tied to retention, a time-to-first-good-output metric, a quality-aware activation funnel, first-session scaffolding, and quality-gated nudges. Use when AI product signups do not convert to retained users; users try the product once and leave after a mediocre output; defining the activation metric for an AI assistant, copilot, or agent; or redesigning the empty prompt box and first-run experience."
---

# AI Activation Optimizer

> In an AI product the first output is the onboarding - if it is mediocre, nothing else in the funnel matters.

## What this skill is

An activation workflow for products where the value a user sees depends on what they type, upload, or connect. Classic activation assumes a deterministic aha moment; AI products add a quality step - the user can complete every onboarding step and still get a poor answer. This skill defines activation as reaching a good output on a real task, measures how fast and how often new users get there, and redesigns the first session so the product does the work of good prompting and context setup for the user.

## What it solves

- Activation metrics that count "first prompt sent" instead of "first useful result"
- Empty prompt boxes that leave new users guessing what to ask
- First outputs that are generic because the product has no user context yet
- Nudges and lifecycle emails sent to users who already had a bad experience, accelerating churn
- Funnel analysis that cannot separate "did not try" from "tried and was disappointed"

## When to invoke

- Signup-to-retained conversion is low or falling for an AI assistant, copilot, or agent
- Setting the North Star or activation metric for a new AI product
- Redesigning onboarding, templates, or the first-run experience
- After a model change shifts output quality for new users
- Planning lifecycle messaging for a product-led AI offering

## Phase 1: Define the aha moment with retention data

List candidate behaviors and test which best predicts week-4 retention.

| Candidate behavior | Users who did it in first 7 days | Week-4 retention if yes | Week-4 retention if no | Lift |
|--------------------|---------------------------------:|------------------------:|-----------------------:|-----:|
| Sent first prompt | | | | |
| Accepted or copied an output | | | | |
| Connected own data source | | | | |
| Completed 3 tasks of the core job | | | | |
| Returned on a second day | | | | |

Pick the behavior with high lift and meaningful reach that the team can influence. Express it as: "<number> <quality-qualified action> within <days>", for example "3 accepted outputs on own data within 7 days." This is correlation; confirm with an experiment before treating it as causal.

## Phase 2: Define a good output

The activation event must include a quality signal. Choose observable proxies:

| Signal | Strength | Caveat |
|--------|----------|--------|
| Output accepted, inserted, sent, or exported | Strong | Requires an action surface |
| Output copied | Medium | Users copy to fix elsewhere |
| No regenerate or heavy edit within 2 minutes | Medium | Silent abandonment looks similar |
| Explicit positive rating | Weak | Low response rate, selection bias |
| Task-level automatic evaluation score | Medium | Needs a validated grader |

```
Good-output rate = sessions with at least one good output / sessions with at least one output
Time to first good output (TTFGO) = timestamp of first good output - signup timestamp
```

Report median and 75th percentile TTFGO; the tail is where churn hides.

## Phase 3: Build the quality-aware activation funnel

| Step | Definition | Conversion | Drop-off reason (hypothesis) |
|------|------------|-----------:|------------------------------|
| Signed up | Account created | 100% | |
| Context set | Role, use case, or data connected | | |
| First attempt | First prompt or task run | | |
| First output | Output rendered without error | | |
| First good output | Quality signal met | | |
| Activated | Aha-moment definition met | | |
| Retained | Active in week 4 | | |

Split the "first output to first good output" drop by: input type (blank prompt versus template), whether data was connected, task category, and model or route used. That split usually explains most of the activation gap.

## Phase 4: First-session scaffolding

| Lever | Pattern | Effect on quality |
|-------|---------|-------------------|
| Replace the blank box | 3-6 role-specific starter tasks with the prompt pre-filled | Removes prompt-writing skill as a prerequisite |
| Collect context up front | 2-3 onboarding questions that feed the system prompt | Less generic first output |
| Use sample data | A realistic workspace or document so value shows before setup | Separates "is it useful" from "is my data connected" |
| Show a worked example | One finished output for the chosen task before the user runs it | Sets expectations for format and depth |
| Ask before guessing | Clarifying question when the input is ambiguous | Fewer confident wrong answers |
| Make editing easy | Inline refine actions (shorter, more formal, add sources) | Turns a near miss into an accepted output |

Prioritize levers by the funnel step with the largest absolute drop.

## Phase 5: Quality-gated nudges

Route lifecycle messaging by the user's actual experience, not by time since signup.

| User state | Nudge | Never send |
|------------|-------|------------|
| No attempt within 24 hours | One starter task matched to stated role | Feature tour |
| Attempted, no good output | Recovery: a better template, a connected-data prompt, or a human help offer | "You are doing great" or upsell |
| One good output, not activated | Next task in the same job, building toward the aha definition | Unrelated feature |
| Activated | Habit loop: schedule, integration, or share with teammate | Basic tips |
| Quality incident affected the user | Acknowledgment and what changed | Generic re-engagement |

## Phase 6: Measure and iterate

Run each scaffolding or nudge change as an experiment with activation rate as the primary metric and week-4 retention as the confirming metric. Watch for activation inflation: a change that makes the activation event easier without raising retention has moved the metric, not the user.

## Output

- Aha-moment definition with the retention-lift evidence behind it
- Good-output definition and time-to-first-good-output baseline (median and 75th percentile)
- Quality-aware activation funnel with drop-off split by input type and data connection
- Prioritized first-session scaffolding changes
- Quality-gated nudge matrix
- Experiment backlog with expected lift per change

## Operating rules

**Always**
- Include a quality signal in the activation definition
- Validate the aha moment against week-4 retention before adopting it
- Report the tail of time to first good output, not only the median
- Route nudges by experienced quality, not by days since signup
- Re-baseline the funnel after every model or prompt change

**Never**
- Count "first prompt sent" as activation
- Leave new users with an empty prompt box and no starter tasks
- Send upsell or upgrade prompts to users who have not yet had a good output
- Rely on voluntary ratings as the only quality signal
- Declare a scaffolding change a win on activation alone if retention did not move
