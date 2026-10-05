---
name: cx-control-testing
description: Use to test whether a support control actually operates, the way an auditor would test it, rather than confirming it exists on paper. Trigger for "test our controls", "does this control actually work", second-line assurance over support, control effectiveness testing, preparing for an internal audit, or a control that passed review and then failed in practice.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Testing a support control

A control is a thing that is supposed to prevent or detect a specific failure — a
four-eyes check on a refund above a threshold, a mandatory disclosure on a call, a
complaint identification step, an approval gate before an account is closed.

Most internal control review asks "is there a control?" and "is it documented?". An
auditor asks a harder question: **does it operate, on every occasion, and would it catch
the failure it exists for?** The gap between those is where findings live.

## Design effectiveness and operating effectiveness

Two separate tests. Both are needed and they fail differently.

**Design** — if the control operated perfectly every time, would it prevent or detect the
failure? Common design defects:

- **It detects too late** to prevent harm. A monthly review of daily decisions is a
  reporting activity, not a preventive control.
- **It is not linked to the risk.** A control that checks a form was completed, where the
  risk is that the form was completed wrongly.
- **It relies on the same person** who performs the action. Self-review is not a control.
- **It has no defined response.** A detection with no required action detects and does
  nothing, and this is extremely common.
- **It is bypassable** by design — an optional field, a skippable step, a warning with a
  continue button.

**Operating** — does it happen, every time, as designed? Test this on evidence, not on
assertion.

A control can be well designed and never operate, or operate diligently and be useless.
Report the two separately or the finding is uninterpretable.

## Test operation on evidence

- **Define the population** — every occasion the control should have operated. This is the
  hard part and the most common place testing goes wrong: if you sample from occasions
  where the control *did* operate, you can only ever conclude it operates. **Build the
  population from the underlying activity**, not from the control's own log.
- **Sample from that population**, randomly, and say how.
- **Look for the artefact.** A control that leaves no evidence cannot be tested, and that
  is itself a finding — an untestable control provides no assurance regardless of whether
  someone performs it.
- **Test the exceptions, not just the pass rate.** Where the control did not operate, what
  happened? Was the failure it exists to catch present in those cases?
- **Check timing.** A four-eyes check performed after the money left is not a preventive
  control. Compare the control timestamp with the action timestamp.
- **Check independence.** Was the reviewer different from the actor, and did they have
  standing to say no?
- **Check whether an override existed and was used**, and whether overrides carry a reason.

## The three tests that find the most

In practice these produce the majority of real findings, and none of them require reading
documentation:

**1. Rubber-stamping.** A control with a near-100% pass rate and near-zero time spent is
not operating. Compare the interval between the action and the approval; a median of
seconds means nobody looked. This is the single most productive test available.

**2. The control that fires and nothing happens.** Detection recorded, no response
recorded. Auto-fails logged and never closed out, alerts raised and never actioned,
exceptions flagged and never resolved. Measure the share of detections with a completed
response — the gap is a finding whatever the pass rate says.

**3. The population that never reaches the control.** Cases routed around it — a different
channel, a different queue, an automation path, a manual workaround, a bulk operation.
This is where a control with a perfect operating record misses everything that matters,
and you only find it by building the population independently.

## Negative testing

Confirming the control passes cases it should pass proves little. The stronger test is
whether it catches what it should catch.

- **Find real instances of the failure** the control targets, by another route, and check
  whether the control caught them. If it did not, operating effectiveness is irrelevant.
- **Reverse the direction**: rather than asking whether approvals happened, ask whether any
  unapproved action got through.
- **Do not test by injecting a failure into production.** In a live customer-facing system
  that risks real harm. Test against history, or in a non-production environment with the
  owner's agreement.

## Compensating and duplicative controls

- **Where a control is weak, look for what else would catch the failure.** A weak control
  with a strong downstream detection is a lower-severity finding, and saying so keeps the
  report credible.
- **Where several controls target the same failure and none is strong**, the honest finding
  is that the risk is not controlled — the count of controls is not the measure.
- **Where a control has no purpose you can trace to a risk**, recommend removing it.
  Ceremony controls consume attention that the real ones need.

## Guardrails

- **Do not conclude that a control is adequate for an obligation.** Report design and
  operating effectiveness; sufficiency against a requirement is a compliance, audit and
  legal determination.
- **Do not test by causing a real failure.**
- **Do not attribute an operating failure to the person who missed it** without checking
  whether the design made compliance impractical — a control that cannot be performed in
  the time available will fail, reliably, for ordinary people.
- **A control failure that has allowed actual customer harm** is not a testing finding. It
  goes to compliance and legal immediately, and it may carry a notification clock.
- **Read-only.** Do not remediate records you find.
- **Cite ids and counts; no transcripts.**

## Present results to the user

1. **The control, and the specific failure it exists to prevent or detect**, stated
   plainly. If that cannot be stated, that is the first finding.
2. **Design effectiveness**, with any of the design defects named.
3. **The population** — how it was built, independently of the control's own log, and its
   size.
4. **Operating effectiveness** — sample, method, pass rate, and the exceptions with what
   happened in them.
5. **The three tests**: rubber-stamping evidence, detections without responses, and the
   population that bypassed the control.
6. **Negative testing** — known failures, and whether the control caught them.
7. **Compensating controls**, and the resulting severity.
8. **Controls recommended for removal**, with the reason.
9. **Anything requiring immediate escalation**, separated from the report.
