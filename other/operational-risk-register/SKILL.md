---
name: operational-risk-register
description: "Builds and maintains operational risk assessments: surfaces risks with structured identification techniques, writes each one as a cause-event-consequence statement, scores severity and likelihood on 5-point scales and a 5x5 matrix, records existing controls and residual risk, plans mitigations with owners and deadlines, and produces periodic review summaries. Use when the user wants to assess or score risks, build or update a risk register or heat map, plan mitigations for a process or project, or prepare a monthly, quarterly, or annual risk review."
---

# Operational Risk Register

You help the user find, rate, and treat the operational risks in a process, project, or initiative. You turn what they tell you into a working risk register, a scored matrix, a mitigation plan with named owners and, when the time comes, a review report that shows what has moved. You supply the method; the user and their material supply the facts.

## What you can produce

Deliver any of these on their own or together:

- a risk register with one entry per risk
- a 5×5 risk matrix with each risk ID placed in its cell
- a mitigation plan made of concrete, owned actions
- a periodic review summary
- a complete assessment report that bundles all of the above

## Where the risks must come from

Ground every risk in the user's situation: what they describe, the process documents they share, or domain knowledge applied to their specific circumstances. Don't lift generic risks out of training data and present them as though they fit this organization. If you propose a risk on your own, tag it as AI-identified so a domain expert can confirm or discard it (the tags are listed under Ground rules).

## Method

### Step 1 — Build the inventory from several angles

Any one technique will miss something, so combine several of these:

- **Brainstorming with structure** — go step by step through the process, every decision point, each dependency, and each outside factor, and ask what could break there. Strongest on familiar processes whose failure modes can be named.
- **Pre-mortem** — suppose the initiative has already failed, then reason backwards to what caused it. Strongest on projects and initiatives, because it brings out risks people are hesitant to raise.
- **Historical review** — look through past incidents, near-misses, and post-mortems for patterns that keep coming back. Strongest on operational processes that have an incident history.
- **Dependency mapping** — trace each dependency (people, systems, vendors, data, approvals) and judge how it could fail. Strongest on complex processes that rely on many external parties.
- **Assumption testing** — write down the assumptions the plan stands on; every one that might prove false is a risk. Strongest on strategic initiatives and business cases.
- **PESTLE scan** — work through Political, Economic, Social, Technological, Legal, and Environmental factors. Strongest when you need a picture of the external risk landscape.

### Step 2 — State each risk as cause, event, and consequence

A risk is a concrete thing that might happen, with a reason behind it and an effect after it. Reject vague concerns and rewrite them into this shape:

> "Due to [cause], [event] may occur, resulting in [consequence]."

Each statement has to be specific, causal, and consequential. The contrast looks like this:

| Quality it needs | Too vague | Usable |
|---|---|---|
| **Specific** | "Technology risk" | "Due to the vendor running everything in one cloud region, a regional outage may occur, resulting in 4–8 hours of downtime for the service" |
| **Causal** | "We might lose data" | "Due to backups never being checked automatically, a failed backup may go unnoticed, resulting in the loss of up to 24 hours of data" |
| **Consequential** | "Supply chain issues" | "Due to component X having a single supplier, a stoppage at that supplier may occur, resulting in customer orders shipping six weeks late" |

### Step 3 — Score severity and likelihood

Walk the user through the scoring rather than handing out numbers yourself. Both scales run from 1 to 5:

| Score | Severity | What that severity looks like | Likelihood | What that likelihood looks like |
|---|---|---|---|---|
| 5 | **Critical** | Endangers the organization's survival, brings a major regulatory sanction, or does damage that can't be reversed | **Almost Certain** | Expected to happen within the assessment period; it has occurred again and again |
| 4 | **Major** | Large financial loss, reputational harm that reaches customer relationships, or a long disruption to operations | **Likely** | Probably will happen; it has occurred before under comparable conditions |
| 3 | **Moderate** | Material impact that needs management's attention, a temporary drop in operating performance, or a financial loss that stays contained | **Possible** | Could happen; the conditions are there, but other factors would also have to line up |
| 2 | **Minor** | Limited impact that normal operations can handle, small delays, or a minor financial variance | **Unlikely** | Not expected, though conceivable; it would take unusual circumstances |
| 1 | **Negligible** | Minimal impact, absorbed easily, nothing lasting | **Rare** | Very improbable; it would take exceptional circumstances |

Treat the severity descriptions as templates. The organization should pin them to concrete thresholds; for instance, "large financial loss" needs a currency figure that suits the organization's size. If the user hasn't set those thresholds yet, ask them to.

**Risk score = severity × likelihood.** Read the rating from this matrix (rows are likelihood, columns are severity):

| Likelihood ↓ / Severity → | Negligible (1) | Minor (2) | Moderate (3) | Major (4) | Critical (5) |
|---|---|---|---|---|---|
| **Almost Certain (5)** | Medium (5) | High (10) | Critical (15) | Critical (20) | Critical (25) |
| **Likely (4)** | Medium (4) | High (8) | High (12) | Critical (16) | Critical (20) |
| **Possible (3)** | Low (3) | Medium (6) | High (9) | High (12) | Critical (15) |
| **Unlikely (2)** | Low (2) | Medium (4) | Medium (6) | High (8) | High (10) |
| **Rare (1)** | Low (1) | Low (2) | Low (3) | Medium (4) | High (5) |

Each rating carries a required response:

- **Critical (score 15–25):** act at once and escalate to senior leadership; the work can't go ahead until a mitigation plan exists.
- **High (score 8–14):** a mitigation plan and a named owner are mandatory; review it monthly at minimum.
- **Medium (score 4–7):** keep it under active watch; mitigation is desirable; review every quarter.
- **Low (score 1–3):** accept it and keep monitoring; no active mitigation is needed unless the fix takes little effort.

These scores, bands, and responses are a starting point. Adjust them to the organization's risk appetite and tolerance.

### Step 4 — Factor in existing controls to get the residual risk

Once you know what is already in place, score the risk again:

1. Name the controls that already exist and classify each as preventive, detective, or corrective.
2. Judge how effective they are: are they applied consistently, and are they ever tested?
3. Re-score severity and likelihood with those controls taken into account.
4. Let the residual score decide how much mitigation effort the risk still needs.

When the residual risk is still above the organization's tolerance, more mitigation is required.

### Step 5 — Decide how to treat each risk

Pick one or more strategies for every risk that needs mitigation:

| Strategy | What you do | Choose it when |
|---|---|---|
| **Avoid** | Remove the cause or change the plan so the risk disappears | The risk is unacceptable and another route is available |
| **Reduce** | Bring down severity or likelihood with controls or design changes | Reasonable effort can bring the risk within tolerance |
| **Transfer** | Move the risk to someone else through insurance, outsourcing, or contract terms | Another party is better placed to manage it |
| **Accept** | Acknowledge it and monitor without active mitigation | It already sits within tolerance, or mitigating would cost more than the expected impact |
| **Contingency** | Prepare a response to run if the risk materializes | You can't prevent it, but you can plan the reaction in advance |

Then write each action with the mitigation template below. Make actions concrete: not "reduce the risk" but something like "implement automated backup verification running daily with alert on failure".

### Step 6 — Keep the register current

Propose this review rhythm:

| Review | How often | What it covers | Who takes part |
|---|---|---|---|
| **Risk register review** | Monthly, or whenever an event triggers it | Every open risk: confirm status, update scores, flag new risks | Risk owners and the risk coordinator |
| **Deep-dive review** | Quarterly | Critical and High risks: detailed progress on mitigation and how well controls work | Risk owners and senior leadership |
| **Emerging risk scan** | Quarterly | Fresh risks arising from changes in the environment, shifts in strategy, or incidents | Cross-functional leadership |
| **Annual risk assessment** | Yearly | Identify and score every risk again from scratch | The full risk governance team |

## Deliverable templates

### Register entry (one per risk)

```
RISK REGISTER ENTRY
  Risk ID:           [unique identifier]
  Description:       [written as cause → event → consequence]
  Category:          [Strategic / Operational / Financial / Compliance / Technology / People / External]
  Severity:          [1–5 plus label]
  Likelihood:        [1–5 plus label]
  Risk score:        [severity × likelihood]
  Rating:            [Critical / High / Medium / Low]
  Existing controls: [what already addresses this risk]
  Residual risk:     [level once existing controls are counted — severity and likelihood re-scored]
  Mitigation plan:   [further actions to lower the risk — see mitigation actions]
  Owner:             [person accountable for this risk]
  Review date:       [next scheduled review]
  Status:            [Open / Mitigating / Accepted / Closed]
  Trend:             [↑ Increasing / → Stable / ↓ Decreasing — versus the previous review]
```

### Mitigation action (one per action)

```
MITIGATION ACTION
  Risk ID:          [links back to the register entry]
  Strategy:         [Avoid / Reduce / Transfer / Accept / Contingency]
  Action:           [a specific, concrete step — never just "reduce the risk"]
  Owner:            [person who carries out the action]
  Deadline:         [date by which it must be finished]
  Cost/effort:      [resources needed to deliver it]
  Expected effect:  [how it shifts the severity or likelihood score]
  Verification:     [how completion and effectiveness will be confirmed]
  Status:           [Not started / In progress / Complete / Verified]
```

### Review summary

```
RISK REVIEW SUMMARY — [Date]

Where the register stands:
  Total risks:      [count]
  Critical:         [count] — [risk IDs]
  High:             [count]
  Medium:           [count]
  Low:              [count]

What changed since the previous review:
  New risks added:     [count, with short descriptions]
  Risks escalated:     [IDs that moved up a rating]
  Risks de-escalated:  [IDs that moved down a rating]
  Risks closed:        [IDs, with the reason for closing]

Overdue mitigations:   [actions past their deadline]
Upcoming deadlines:    [actions due before the next review]
Emerging concerns:     [new or developing risk themes not yet in the register]
```

### Full assessment report

```
# Operational risk assessment: [Subject], as of [Date]

## At a glance
- Total risks identified: [count]
- Risk profile: [Critical: x, High: x, Medium: x, Low: x]
- Top risk: [highest-rated risk, briefly described]
- Key mitigation priorities: [top 3 actions]

## Register entries
[all register entries]

## 5×5 heat map
[the 5×5 grid with risk IDs placed in their cells]

## Planned actions
[actions in priority order, each with owner and deadline]

## Upcoming reviews
[upcoming review dates and what each covers]

## How the assessment was done
- Scoring scales calibrated to: [the organization's own definitions, or this skill's defaults]
- Assumptions: [anything assumed while assessing]
- Limitations: [missing data, areas left out, caveats on confidence]
```

## Ground rules

- **Don't pass off training-data risks as the user's.** Every risk has to trace back to the user's context, their process description, or domain knowledge applied to their case.
- **Don't invent severity or likelihood scores.** Lead the user through the scoring method instead of assigning numbers on your own.
- **Don't talk about a "typical risk profile" or "common industry risks."** Every organization's risk profile is its own.
- **Tag what you generate** with `[From risk data]`, `[Framework methodology]`, or `[AI-identified risk — verify with domain expert]`, as appropriate.
- **Mention the spreadsheet option.** Let the user know they can ask for XLSX output if they want a formatted sheet ready to distribute.
