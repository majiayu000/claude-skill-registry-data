---
name: cx-reverse-etl
description: Use to design a safe pipeline that writes derived attributes back into a helpdesk — risk scores, segments, health flags — without corrupting agent workflows or creating an unexplainable feedback loop. Trigger for "push scores back into Zendesk", "sync warehouse attributes to the helpdesk", "write our churn risk onto the ticket", reverse ETL for support, or an automation that started firing on a synced field.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Writing derived data back into a helpdesk

Reverse ETL puts warehouse-computed attributes where agents can see them: a customer
segment, a risk score, a lifetime value band, a churn flag. Done well it is one of the
highest-leverage things a data team can do for a support operation.

Done carelessly it is worse than the analysis being unavailable, and for a reason people
underestimate: **the helpdesk is not a read-only display surface. It has automations.**
A synced field can trigger routing rules, SLA policies, macros, notifications and
customer-facing messages that nobody connected to the pipeline knows exist.

## Before designing anything

**1. What decision does this attribute change?** An attribute nobody acts on is clutter on
an already-crowded ticket view, and clutter has a cost — agents stop reading the sidebar.
If the answer is "it's useful context", ask who has asked for it.

**2. What automations could fire on it?** Enumerate them **before the first write**: routing
rules, triggers, SLA policies, views, macros, and anything watching for field changes. This
is the step that gets skipped and it is where the outages come from.

**3. Is the attribute defensible on the ticket?** Anything visible to an agent may be
repeated to a customer, appear in a subject access request, or be screenshotted. "Churn risk:
high" is defensible. A pejorative label, or an inferred vulnerability or affordability
marker, is not — and inferred sensitive attributes should not be written back at all.

**4. What happens when it is wrong?** Every derived attribute has an error rate. If a wrong
value changes how a customer is treated, the error rate is a customer-impact rate.

## Write derived, never authoritative

The hard rule that prevents the worst failures:

- **Write to fields the pipeline owns exclusively.** Namespace them so ownership is obvious
  from the field name.
- **Never write to a field agents also edit.** The sync will overwrite their work, silently,
  on its next run — and they will not know why.
- **Never write to an authoritative field.** Status, assignee, priority, tags shared with
  human workflow. If a derived value should influence priority, let a rule read the derived
  field and set priority; do not have the pipeline set priority.
- **Never write to a field that is part of a customer-facing communication** without treating
  it as a content change with a review.

## Make it explainable on the ticket

An agent looking at "Risk: 72" with no context will either ignore it or misuse it. Alongside
the value, sync:

- **What it means**, in a sentence, or a link to a definition that stays current.
- **When it was computed.** A stale score presented without its age gets trusted as current;
  this is the single cheapest safeguard.
- **The top contributing factors**, where the model supports it. A score with a reason is
  actionable; a bare number invites invention.
- **Its precision.** "High risk" at 15% precision needs saying, or agents will treat it as a
  fact about the customer.

## Bound the write path

Reverse ETL is a bulk mutation against a production system with real customer data. It
carries the same obligations as any other write:

- **Dry run by default**, producing a diff of what would change. The diff is the artefact a
  human reviews.
- **A bounded batch size**, raised deliberately, so a mistaken transformation affects fifty
  records rather than five hundred thousand.
- **An append-only audit log** — record, field, before, after, timestamp, and the run it came
  from. This is what answers "why did this ticket's field change" three weeks later.
- **Idempotent and resumable**, journaling completed ids so an interrupted run does not
  double-apply.
- **Only write what changed.** Rewriting unchanged values burns rate limit and, worse, fires
  every field-change automation on every run.
- **Verify after applying** by re-reading a sample.
- **A kill switch** the support team can use without waiting for a deploy, because they will
  notice a bad sync before you do.

Where an existing platform mutation skill covers the target helpdesk, run the write through
it rather than building a second write path with weaker guarantees.

## Avoid the feedback loop

A subtle failure worth designing out: if a derived attribute changes how conversations are
handled, and the model is retrained on the resulting data, the model learns from its own
effects.

- A "high risk" flag that triggers faster handling produces better outcomes for flagged
  accounts, which makes the flag look wrong on retraining.
- A routing rule reading a synced segment changes who handles what, which changes the
  training distribution.

**Record which conversations were influenced by a synced attribute**, so the model's next
training run can account for it — or at minimum so someone can tell that apparent model
degradation is the intervention working.

## Operational realities

- **Rate limits.** A backfill across every customer record will consume the same budget the
  helpdesk's own integrations need. Throttle, and run large backfills outside business hours.
- **Field limits.** Helpdesks cap custom fields, and adding one is a configuration change
  with its own review.
- **Deleted and merged records** will fail the write. Expect them and do not let them fail
  the run.
- **Sync cadence versus staleness.** Daily is usually fine for a segment and useless for
  something intended to influence a live conversation. Match cadence to use and show the
  computation time either way.
- **Two-way conflict.** If anything else writes the same field, you have a conflict you must
  resolve deliberately rather than by last-writer-wins.

## Guardrails

- **Do not write inferred sensitive attributes** — vulnerability, health, financial
  difficulty, ability to pay — into a helpdesk field. Sensitive status belongs in a process
  designed for it, recorded by a human, not inferred by a pipeline and shown in a sidebar.
- **Do not write anything that would differentiate service by revenue** in a way you could
  not defend to a customer or a regulator.
- **Synced attributes are personal data** and they expand the record. They are in scope for
  subject access requests and for retention, and the helpdesk's retention may differ from the
  warehouse's.
- **Do not enable a new automation on a synced field in the same change** as the first sync.
  Land the data, verify it, then wire the rule.
- **Tell the support team before the first write**, and tell them what the field means. A
  field appearing without explanation gets misinterpreted immediately.

## Present results to the user

1. **The decision each attribute changes**, and who asked for it.
2. **The automation inventory** — every rule, trigger, SLA policy and view that could fire on
   the target field. Before the first write.
3. **Field ownership** — that the pipeline writes only namespaced fields it owns exclusively,
   and nothing authoritative.
4. **The explainability payload** — meaning, computation time, contributing factors, precision.
5. **The write-path guardrails** — dry-run diff, batch bound, audit log, resume, changed-only
   writes, verification, kill switch.
6. **The feedback-loop record**, so influenced conversations are identifiable later.
7. **Cadence versus staleness**, and how age is surfaced to agents.
8. **What is deliberately not synced**, especially inferred sensitive attributes, and why.
