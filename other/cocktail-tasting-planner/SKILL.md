---
name: cocktail-tasting-planner
description: Plan a bounded comparative cocktail tasting from an approved lineup, participant assignments, one declared learning question, sample sizes, ABV evidence, user-set alcohol ceiling, order, pacing, reveal method, and materials. Use for a checkable host packet. Do not use to choose bottles or recipes, prescribe consumption, certify sensory learning, run a tasting app, or replace responsible-hosting review.
---

# Cocktail tasting planner

Build a review-ready comparative tasting packet from choices the user already
approved. Reconcile each sample, participant assignment, material count, and
pure-alcohol figure without treating a preference as objective quality or a
planning ceiling as health advice.

## 1. Confirm the tasting job

Accept a bounded group tasting that compares approved cocktails or mixed
beverages around one stated learning question.

| Request | Route |
|---|---|
| Choose bottles, recipes, or a generic party menu | Recipe or bottle selection |
| Teach a cocktail taxonomy without an event | Cocktail family teaching |
| Build a scientifically valid blind experiment | Qualified study design |
| Interpret allergies, medical needs, or impairment | Qualified health review |
| Set a safe personal alcohol limit | Applicable public-health guidance |
| Send invitations, order supplies, or operate an app | External action after human review |

This skill can prepare an open or concealed tasting. It does not claim that
concealment, order, palate resets, or participant sheets remove bias.

Complete this step when one tasting event, one approved lineup, and one
learning question own the request.

## 2. Freeze the event contract

Record every field before constructing the flight.

| Field | Required record |
|---|---|
| Participants | Count, stable participant codes, opt-in assignments, non-alcoholic assignments, and unresolved responses |
| Learning question | One user-declared comparison question |
| Approved lineup | Sample identity, recipe or batch identity, final sample ABV, source and date, and role in the question |
| Pour plan | Sample volume, unit, preparation allowance, device increment, and spill policy |
| Format | Open or concealed, reveal timing, code owner, and code-access rule |
| Order | User-selected sequence or rotation plus its rationale and override |
| Pacing | Start, sample windows, pauses, reveal, finish, and user-selected minimum interval |
| Participant materials | Prompt fields, response format, missing-response marker, and spare count |
| Service materials | Vessels, water, user-selected palate reset, labels, trays, and waste plan |
| Alcohol basis | Jurisdictional reference or pure-alcohol formula plus a user-declared event ceiling |
| Safeguards | Participant access needs, unresolved review items, and a separate responsible-hosting plan when alcohol is assigned |

An alcoholic sample needs final served ABV, not the ABV of one ingredient.
Unknown ABV blocks pure-alcohol reconciliation. Never infer consent,
participant suitability, a medical restriction, or an alcohol ceiling.

Emit `STOPPED: REQUIRED TASTING EVIDENCE MISSING` when participant count,
approved lineup, learning question, pour size, order, pacing, or format is
absent. Issue no lineup replacement. Do not convert a relative date into a
calendar date or supply an example question, lineup, sample count, pour size,
interval, ceiling, jurisdictional limit, health source, or participant value.
List the missing fields without populating them.

Complete this step when another host can reproduce the event without choosing
an unstated drink, participant assignment, quantity, sequence, or limit.

## 3. Audit the comparison

Give each approved sample one declared role.

| Role | Required explanation |
|---|---|
| Anchor | Establishes the user's reference point |
| Contrast | Changes the feature named in the learning question |
| Near-miss | Intentionally falls outside the stated comparison boundary |
| Control | Holds a user-declared condition fixed |

The roles are planning labels rather than universal tasting taxonomy.
A social tasting does not require one-variable design. When the user claims a
controlled comparison, list every supplied difference and mark the claim
unresolved if another difference lacks an approved explanation.

Run a deletion check. Removing each sample must erase a unique learning role.
Move redundant samples to `OPTIONAL` instead of inflating the flight.

Complete this step when every included sample has one traceable contribution
and the packet discloses every known comparison limit.

## 4. Reconcile pours and materials

Read [the pour and alcohol ledger](references/pour-alcohol-ledger.md)
completely.

For every sample:

```text
assigned pours = count of participants assigned that sample
participant liquid = assigned pours × sample volume
required sample liquid = participant liquid + user-supplied preparation allowance
```

Round only to the user's device increment, then recompute the variance. Keep
alcohol-free and declined assignments explicit. Never direct a participant to
finish a pour.

Reconcile vessels, participant sheets, labels, water settings, palate-reset
units, trays, and spares against the assignment map. Missing physical inventory
creates an unresolved material gap rather than an assumed purchase.

Complete this step when every liquid and material total traces to participants,
samples, allowances, and user-supplied spares.

## 5. Reconcile pure alcohol

Calculate planned pure alcohol for each assigned participant from sample volume
and final served ABV. Use only the jurisdictional basis the user selected.

The result is the planned maximum if every assigned sample is consumed. Label
it `CALCULATED PLANNING EXPOSURE`, not a recommendation or predicted intake.

Compare each participant's calculated figure with the user-declared event
ceiling. The ceiling is a planning constraint, not a safe personal limit.
Never raise it to fit the lineup.

Emit `STOPPED: ALCOHOL BASIS OR CEILING UNRESOLVED` when an alcoholic assignment
lacks final ABV, the selected pure-alcohol basis, or the user's ceiling. Keep
alcohol-free-only assignments at zero without assigning them an alcoholic
alternative.

Complete this step when every assignment is zero or reconciled, and no plan
exceeds the declared ceiling.

When every assigned sample is documented at exactly 0.0% ABV, mark the
alcohol-specific ceiling and responsible-hosting alcohol branch
`NOT APPLICABLE: NO ALCOHOL ASSIGNED`. Preserve general voluntary
participation, access, water, and host-review safeguards.

## 6. Build order, pacing, and reveal

Read [the facilitation packet](references/facilitation-packet.md) completely.

Apply the user's selected sequence or rotation. Do not invent a universal
weak-to-strong, light-to-dark, or flavor-progression rule. Record the rationale
and any participant-specific override.

Use the supplied sample windows and intervals without claiming alcohol
clearance or palate recovery. Water, food, and a user-selected palate reset
remain available without pressure to consume.

For a concealed tasting, separate the code key from participant materials,
name its owner, and schedule reveal after response collection. Preserve
withdrawals and missing responses as missing rather than scores.

Complete this step when each participant has one order, every time block fits
the event window, and the reveal cannot occur accidentally through the packet.

## 7. Set the evidence state

Use one state when no stop applies.

| State | Gate |
|---|---|
| `TASTING PACKET READY: HOST REVIEW REQUIRED` | Comparison, assignments, alcohol ledger, materials, pacing, and safeguards reconcile |
| `PACKET PARTIAL: MATERIAL OR SAFEGUARD REVIEW REQUIRED` | Valid planning sections exist, but a material, access, or responsible-hosting item remains unresolved |

An earlier stop takes precedence. Preserve downstream gaps as secondary
blockers without printing another status label.

Participant feedback records preference and observation. It does not certify
objective quality, sensory ability, learning, sobriety, or safety.

Complete this step when the state follows from supplied evidence and the packet
stops before invitations, purchasing, service, or app operation.

## 8. Emit the host packet

Return these sections in order.

1. Status
2. Event contract
3. Learning question and comparison limits
4. Lineup roles and deletion check
5. Participant assignment and order
6. Pour, alcohol, and materials ledger
7. Participant sheet
8. Host run sheet and reveal
9. Safeguards, unresolved items, and human review

A stopped result marks the affected lineup and quantities `NOT ISSUED`. Provide
no replacement drink, consumption target, medical interpretation, invitation,
order, purchase, or external action. Keep the stopped packet to one primary
status, supplied facts, missing fields, category-level routes, and the ordered
sections marked `NOT ISSUED`. Ask only for the missing field names. Do not add
example values, example learning questions, specific health guidance, or
calendar inferences.

Complete the skill when the packet is reproducible, every calculation closes,
the user-selected ceiling is preserved, comparison limits remain visible, and
execution waits for host review.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users discover candidate
cocktails before the host approves a lineup for this tasting procedure.
