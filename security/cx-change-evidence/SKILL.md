---
name: cx-change-evidence
description: Use to prove that a support process, policy or script change actually took effect — when, for whom, and whether behaviour followed — rather than that it was approved. Trigger for "prove we made that change", "when did this policy actually change", "did the team adopt the new process", evidencing remediation, "we told everyone" claims, or a change that was signed off and never landed.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Evidencing that a change actually happened

Somebody needs to show that a support change was made: a policy updated after a
complaint theme, a script corrected after a conduct finding, a new step added after an
audit. The evidence usually offered is the approval — a ticket, a meeting minute, a
sign-off.

**An approval is evidence of a decision, not of a change.** The questions that get asked
next are when it took effect, who it reached, and whether behaviour actually changed —
and those are answerable from support data, which is why this analysis exists.

It matters most for remediation. A remediation whose effective date is wrong, or which
never reached part of the operation, leaves customers affected after the date the firm
says it was fixed. That is a worse position than not having remediated, because it has
been asserted.

## Four dates, and they are not the same day

Establish each separately:

1. **Decision date** — when it was approved.
2. **Effective date** — when the changed artefact actually went live: the macro updated,
   the article published, the routing rule deployed, the scorecard version released.
3. **Communication date** — when the people who had to act on it were told.
4. **Adoption date** — when behaviour actually changed, which is observable and is usually
   the latest of the four.

The gap between 1 and 2 is where remediation dates get overstated. The gap between 2 and 4
is where "we made the change" fails on contact with the evidence. **Report all four.** If a
firm has told a regulator the change took effect on the decision date, the difference
matters.

## Evidence for each

**Effective date** — from the artefact's own version history: knowledge article revisions,
macro edit timestamps, scorecard version records, deployment logs, config change history.
Where an artefact has no version history, say so; the effective date is then unevidenced
and that is itself a finding.

**Communication date** — the announcement, the training record, the acknowledgement.
Distinguish *sent* from *received* from *acknowledged*. "We told everyone" usually means an
announcement was posted, which is the weakest of the three. Check coverage: night shifts,
part-time staff, contractors, vendor sites and people on leave are the routine gaps, and
vendor sites are the most commonly missed.

**Adoption date** — the interesting one, because it is measurable in the work:

- **Macro or template usage** — the old version's distinctive phrasing disappearing from
  sent messages and the new one appearing. This is the cleanest available signal.
- **The behaviour the change was meant to produce**, measured directly: the new step
  appearing, the disclosure being given, the process being followed.
- **The outcome the change was meant to move**, which is slower and confounded but is the
  substantive test.

## Adoption is usually partial, and the partial part is the finding

Expect a curve, not a step. What matters is where it flattens and who is on the wrong side
of it.

- **Segment adoption by team, site, channel, tenure and vendor.** A change adopted at 95%
  overall and 40% at one site is a site finding, and the average conceals it entirely.
- **Find the persistent non-adopters** and ask why. Usually one of: they never heard, the
  old way is still available, the new way is slower, or the system still permits the old
  path. **The last is the most common and the most fixable** — a change that relies on
  people choosing the new option, while the old option remains, will not fully land.
- **Check whether the old artefact still exists.** An outdated macro left active is the
  single most reliable cause of a change not sticking, and it is trivially checkable.
- **Watch for decay.** Adoption that reached 90% and fell back is a different finding from
  one that never got there, and it needs a re-measurement point some weeks later. Build the
  second measurement into the plan rather than declaring success at the peak.

## Distinguish the change from its effect

Two claims people conflate:

- **"The change was made and adopted."** Evidenced as above, and reasonably clean.
- **"The change fixed the problem."** A causal claim needing the outcome to move by more
  than normal variation, ideally with the prediction written before the change.

You can honestly evidence the first while reporting that the second is unproven — and that
is frequently the correct output. Note that adoption without the expected outcome movement
is informative in itself: it means the change was the wrong change, which is more useful
than a vague "still monitoring".

## Traps

- **The decision date used as the effective date** in a remediation report. The specific
  error this skill exists to catch.
- **Retroactive artefact edits.** A knowledge article edited and its history overwritten
  cannot support any date claim. Check whether history is retained before relying on it.
- **A change communicated but not enforceable.** Optional adoption of a mandatory change is
  a control design problem, not a training problem.
- **Reverse migration.** A change adopted, then a system update or a template restore
  quietly reinstating the old behaviour.
- **Measuring adoption on volume rather than on eligible occasions.** The denominator is the
  occasions the change applied to, not total contacts.
- **Vendor and contractor populations excluded from the measurement** because they are in a
  different system. They are frequently the lowest adopters and they are handling your
  customers.

## Guardrails

- **Read-only. Do not create or backdate evidence.** Producing a record to fill a gap, or
  presenting a reconstructed artefact as contemporaneous, is falsified evidence regardless
  of intent.
- **Where the effective date cannot be evidenced, say so plainly** rather than inferring it
  from the approval. The honest statement is that the change is undated.
- **A gap between the asserted and actual effective date, on a remediation already reported
  externally**, is a matter for compliance and legal immediately. Customers may have been
  affected after the date the firm stated it was fixed.
- **Do not name persistent non-adopters as individuals** in the report. Segment to team or
  site; individual follow-up is a management conversation with its own process.
- **Cite ids and counts; no transcripts.**

## Present results to the user

1. **The four dates**, side by side, with the evidence for each and any that could not be
   evidenced.
2. **Communication coverage** — sent, received, acknowledged — and the populations missed,
   vendor sites specifically.
3. **The adoption curve**, with the measurement basis and the eligible-occasion denominator.
4. **Adoption by segment**, with the flattening point and the persistent non-adopters by
   team or site rather than by name.
5. **Why the non-adopters have not adopted**, with the old-path-still-available check
   answered explicitly.
6. **Decay**, from a re-measurement some weeks after the initial one.
7. **The change-versus-effect distinction**, stating clearly which is evidenced.
8. **Any discrepancy with a date previously asserted externally**, escalated rather than
   noted.
