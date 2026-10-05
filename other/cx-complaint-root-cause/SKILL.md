---
name: cx-complaint-root-cause
description: Use to find the causes behind a complaint population and track whether remediation actually stopped them recurring. Trigger for "root cause analysis on our complaints", "why do we keep getting the same complaints", "complaint themes and remediation", recurring complaint categories, complaint reduction programmes, or a remediation that was signed off and did not work.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Complaint root cause and remediation

Complaint root-cause analysis has a characteristic failure: the analysis is done, the
themes are named, actions are assigned, the report is filed — and the complaints keep
arriving at the same rate. A year later the same themes are rediscovered by a different
analyst.

The reason is almost never the analysis. It is that **remediation is not tracked to
outcome**, so nobody notices when an action was completed and the cause was not
removed.

## Cause, not category

A complaint category is a reporting bucket. A cause is a mechanism you could remove.

> Category: "payment delays"
> Cause: "transfers submitted after 15:00 miss the cut-off, and the product does not
> say so until after submission"

The second one names something a team can change. The first names something you can
count. **Most complaint reporting stops at the first and then wonders why the numbers
do not move.**

Get to causes bottom-up. Read a sample of the actual complaints in a category rather
than trusting its label, and expect to find that one category contains three unrelated
causes and that two categories share one.

## Classify the cause by where it sits

The classification determines the owner and the remedy, and this is where the analysis
earns its keep:

- **Product or service defect** — it did not work.
- **Process design** — it worked as designed and the design produces a bad outcome.
- **Communication** — the outcome was correct and the customer was not told, or was told
  in a way they could not act on. Reliably one of the largest and most fixable groups.
- **Handling** — the underlying issue was minor and the way it was handled created the
  complaint. Distinguish this carefully; a handling complaint about a product defect is
  still fundamentally a product defect.
- **Expectation set at sale** — they were sold something that does not behave as
  described. Route to sales and marketing; support cannot fix it.
- **Customer error, with a design contribution** — they made a mistake the design made
  easy. Almost never purely the customer's fault; look for the affordance that allowed it.
- **No fault** — the outcome was correct, well-communicated, and they are unhappy anyway.
  A legitimate category, and it should be small. **A large "no fault" share is usually a
  sign the analysis is defending the firm rather than examining it**, so check a sample
  of these specifically.

## Complaints are the tip

Every complaint category has a much larger silent population who had the same
experience and did not complain. Complaint propensity varies enormously by segment,
channel, product and customer confidence — so **complaint volume is a poor proxy for
harm volume**, and ranking causes by complaint count systematically under-weights
issues affecting customers least likely to complain.

Wherever possible, size the affected population from operational data rather than from
complaints: how many customers hit that cut-off, received that letter, saw that error.
Then report both, and rank on the population.

This matters beyond accuracy. If the cause produced a detriment, **remediating only the
customers who complained is usually not defensible** — proactive remediation of the
affected population is the question, and it is one for compliance and legal, not for
the analyst.

## Track remediation to outcome, not to completion

This is the part that fixes the recurring-theme problem. For each cause:

- **A named owner and a specific change**, not "review the process".
- **A measurable prediction**: which complaint category should fall, by roughly how
  much, and by when. Writing the prediction down before the change ships is what makes
  the check possible.
- **The date the change actually took effect**, which is frequently much later than the
  sign-off date and is the date that matters for measurement.
- **A verification date**, deliberately after enough volume has accrued to tell a real
  fall from noise.
- **The verification result**, recorded — and a cause whose complaints did not fall goes
  back on the list rather than staying closed.

**"Action completed" is not "cause removed."** Track both states separately. The gap
between them is the most useful metric this whole exercise produces, and almost nobody
has it.

When checking whether complaints fell, check whether the *rate* fell rather than the
count, and confirm the movement exceeds normal variation before declaring success.
Complaint volumes are low, so a good month proves very little.

## Traps

- **Reclassification masquerading as improvement.** A category that falls sharply
  immediately after a taxonomy change or a new triage rule has not improved. Check for
  definition changes before celebrating.
- **A remediation that moves the complaints rather than removing them.** Complaints
  falling in one category and rising in an adjacent one is a redirect, not a fix.
- **Five Whys stopping at the person.** "The agent didn't check" is a symptom. The
  question is why the process let an unchecked case through, and what made checking
  hard.
- **Root causing individual complaints only.** Per-case root cause is required for the
  response to that customer; thematic root cause is what reduces volume. They are
  different exercises and the first does not aggregate into the second.
- **Small numbers.** A category with four complaints does not support a trend. Report the
  count, suppress the rate, and do not run a programme off it.
- **Complaints closed as "resolved" with no cause recorded.** Common, and it removes
  those cases from every subsequent analysis. Report the share.

## Guardrails

- **Whether a cause produced a reportable failure, and whether proactive remediation is
  required, is a compliance and legal determination.** Produce the cause, the affected
  population and the evidence; flag it clearly and do not rule on it.
- **Do not attribute causes to named individuals** in a thematic analysis. If a genuine
  individual performance issue emerges, it belongs in a separate, properly-controlled
  process.
- **Cite ids; do not paste complaint content.** Complaint files hold financial
  circumstances, health disclosures and vulnerability information, and these reports
  circulate.
- **Do not let a complaint-reduction target become a complaint-recording target.** If
  reducing complaints is an objective, the guardrail is the identification rate — a fall
  in recorded complaints with no fall in the underlying driver means fewer are being
  logged.

## Present results to the user

1. **Causes, not categories**, derived bottom-up, with the category-to-cause mapping shown
   where one category split or two merged.
2. **The cause classification**, with an owner per class, and the "no fault" share checked
   rather than assumed.
3. **Affected population per cause**, from operational data where available, alongside
   complaint count — and ranked on population.
4. **The remediation register**: owner, specific change, predicted effect, effective date,
   verification date, verification result.
5. **Completed-but-not-verified and verified-but-not-fixed**, as separate lists. The
   second is the one that explains recurring themes.
6. **Causes recurring from a previous analysis**, named as such.
7. **What needs a compliance determination** — reportability and proactive remediation.
8. **Data gaps** — complaints with no recorded cause, categories too small to analyse.
