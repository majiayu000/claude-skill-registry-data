---
name: cx-conduct-risk-monitoring
description: Use to monitor support conversations for conduct risk — pressure, mis-selling, unfair outcomes, obstruction and misleading statements — as distinct from whether the answer matched policy. Trigger for "monitor for mis-selling", "conduct risk in our support conversations", "are agents pressuring customers", "customers being obstructed from cancelling", conduct surveillance, or a conduct finding raised by second line.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Conduct risk in support conversations

Policy compliance and good conduct are different tests, and an operation can pass the
first while failing the second. An agent who follows every documented step and leaves
the customer worse off than they should be has complied and behaved badly.

Conduct monitoring asks the second question: **was the customer treated fairly, and did
they end up with an outcome they should have had?**

## The risk categories

Each needs its own detection approach, and they have different severities:

**Obstruction.** Making it hard to do something the customer is entitled to do —
cancel, complain, claim, switch, get a refund. Look for repeated redirection,
requirements that do not exist, "you'll have to call", multiple transfers on a
cancellation request, and cancellation requests that generate a retention conversation
instead of a cancellation. **A right that is technically available and practically
obstructed is a serious finding**, and it is one of the most common.

**Pressure.** Urgency that is not real, discouraging a customer from a course they are
entitled to take, repeated retention attempts after a clear decision, implying a
consequence that does not follow.

**Mis-selling and unsuitable outcomes.** Recommending something that does not fit the
customer's stated circumstances, upgrading someone whose problem was a defect, or
selling into a conversation that started as a complaint.

**Misleading statements.** Overstating a benefit, understating a cost, describing a
discretionary act as a rule, or a rule as discretion. Also silence: omitting a material
condition is misleading even when everything said is true.

**Unequal treatment.** Similar customers getting different outcomes without
justification — and specifically, better outcomes for those who escalate loudest, which
systematically disadvantages the least confident.

**Failure to act on a signal.** Vulnerability, financial difficulty or a complaint that
was expressed and not recognised. Frequently the highest-severity category, because the
customer did their part.

## Detection: behavioural signals beat keyword lists

Language-based detection finds the crude cases. The informative signals are structural,
and they are computable without reading anything:

- **A cancellation request followed by more than one further contact** before the
  cancellation completed. Count the contacts and the elapsed time. This single measure
  finds obstruction better than any phrase search.
- **A complaint expressed and not logged** — compare complaint-shaped language against
  complaints actually recorded. The identification gap is a conduct finding as well as a
  process one.
- **A sale or upgrade in a conversation that opened with a problem.** Sequence, not
  content.
- **Redress dispersion for like cases** — same failure, different outcomes.
- **Outcome differences correlated with escalation intensity**, tenure, channel, market,
  or anything you could not defend.
- **Repeated contact on the same entitlement**, which means the customer is not getting
  it.

Prefer these. They are cheaper to compute, harder to game, and they do not depend on
catching a particular phrasing in a particular language.

## Sampling: risk-weighted, and honest about what that means

Conduct issues are rare, so uniform random sampling spends nearly all its budget on
routine conversations.

- **Stratify toward risk**: cancellations, complaints, retention conversations, redress
  decisions, conversations with vulnerability signals, and anything involving a sale.
- **Keep a small random core** as well. Risk-weighted sampling cannot produce a
  population rate, and you will be asked for one. The random core is what lets you say
  anything about prevalence.
- **Report them separately and never pool them into one rate.** A conduct-failure rate
  from a risk-weighted sample describes risky conversations, and quoting it as an
  organisation-wide rate is a serious misstatement in a document that may reach a
  regulator.
- **Cover every language and channel.** Voice in particular, where transcription quality
  varies.

## Distinguish individual from systemic

The response differs completely, so the classification is the analytical work:

- **Systemic** — the process, script, incentive, macro or system produces the behaviour.
  If several agents do the same thing, it is systemic, and treating it as individual
  performance will not fix it and will damage trust.
- **Individual** — a specific person acting outside a working process.

**Check the incentive before blaming the person.** A retention target, a handle-time
target, a save-rate metric or a commission structure will produce pressure and
obstruction reliably, from ordinary people. Where you find a conduct pattern, look for
the metric that rewards it — and report the metric as the finding.

Also check the script and the macros. An obstruction pattern is frequently written down
somewhere as the recommended approach.

## Guardrails

- **Conduct monitoring on employees is employee monitoring.** It has legal constraints
  that vary by jurisdiction and may require notice, consultation, or works-council
  agreement. Flag it; do not resolve it.
- **Do not present a suspected individual conduct finding as established.** It is an
  allegation until a proper process tests it, and the person is entitled to respond.
  Hand it to the process rather than writing a conclusion.
- **Do not fold conduct findings into QA scores.** Different purpose, different evidence
  standard, different consequences.
- **Do not brief a conduct finding widely.** Restrict distribution, and separate the
  aggregate pattern from any individual case.
- **Whether something is a conduct breach, and whether it is reportable, is a compliance
  and legal determination.** Provide the pattern and the evidence.
- **Cite ids; quote minimally and only where the wording is the finding.** These reports
  go to second line, audit and sometimes regulators.
- **A finding of immediate customer harm goes to its escalation route now**, not into the
  monthly report.

## Present results to the user

1. **How conversations entered the sample** — risk-weighted and random core, separately —
   and what population each result describes. Before any rate.
2. **Structural findings first** — obstruction measured as contacts-to-completion,
   unlogged complaints, sales-after-problems, redress dispersion. These are the strongest
   evidence.
3. **Per-category findings**, ranked by severity rather than volume, with failure-to-act
   cases at the top.
4. **Systemic versus individual**, with the incentive, script or macro named wherever a
   pattern spans several agents.
5. **Unequal treatment checks**, including correlation with escalation intensity and with
   anything indefensible.
6. **Detection limits** — languages, channels, and what behavioural signals cannot see.
7. **What needs a compliance determination**, and what has been escalated immediately
   rather than reported.
