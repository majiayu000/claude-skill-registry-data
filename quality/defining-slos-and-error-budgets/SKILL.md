---
name: defining-slos-and-error-budgets
kind: skill
status: ready
provenance:
  principles:
  - P059
  - P026
  - P010
  - P011
  - P115
  - P128
  claims:
  - C00646
  - C00647
  - C00648
  - C01301
  - C01302
  - C01303
  - C00624
  - C01797
  - C00620
  - C00621
  - C00622
  - C01727
  evidence:
  - E00313
  - E00314
  - E00315
  - E00430
  - E00431
  - E00432
  - E00308
  - E00556
  - E00305
  - E00306
  - E00307
  - E00554
  source_anchors:
  - 9fe26df35c80-c0006
  - 9fe26df35c80-c0035
  - 9fe26df35c80-c0005
  - 0bea4daa68ab-c0005
  - 0bea4daa68ab-c0003
  authored_from_digest: 9a4eb58d1a2e56a5b43e0f22b46f0ad4d81ba21d7764ef201225825ca6ce21cd
---

# Defining SLOs and error budgets

## Purpose

Set a service's reliability target deliberately and govern releases with it. Manage to a chosen
Service Level Objective rather than to perfection, derive an error budget from it, and adopt an
error-budget policy that slows or halts feature work when the budget is spent (P002). Pair that
with observability built on user-facing symptoms and burn rate (P008). SRE is a concrete
implementation of DevOps that applies engineering methods to operations (CL045); this skill turns
"how reliable should we be?" into an explicit, shared, data-driven decision.

## When to use

- Defining or reviewing reliability targets for a service (SLIs, SLOs, alerting).
- Dev and ops disagree over how much reliability work versus feature work to do.
- A team is deciding whether it is safe to keep shipping features.
- Alerting is noisy or pages on causes rather than user impact.

Do not apply a standard SLO/error-budget posture where a safety-critical or contractual context
requires near-total reliability regardless of feature velocity — surface that exception and defer
the call to the accountable owner. For a batch/internal system with no meaningful user-facing
reliability signal, say the model does not fit.

## Procedure

1. **Reject 100% as the target (P002).** State plainly that perfect reliability is the wrong goal:
   it forbids the change and risk that deliver value, and the marginal cost is rarely worth it
   (CL046). Omitting an error-budget policy, or recommending a 100% target, is a forbidden output.
2. **Choose SLIs that reflect user experience (P008).** Pick Service Level Indicators that capture
   what users actually feel — availability, latency, correctness — and express targets as
   percentiles over a defined window, not single averages that hide tail pain (CL050).
3. **Set the SLO.** Fix an explicit objective on each SLI (e.g. a percentile target over a rolling
   window) that the team and its stakeholders agree is "reliable enough" for this service.
4. **Derive the error budget (P002).** Turn the SLO into an error budget — the amount of
   unreliability the service may spend — so the dev-versus-ops reliability argument becomes a
   shared, data-driven decision instead of an opinion contest (CL048).
5. **Adopt an explicit error-budget policy (P002).** Agree in advance what happens when the budget
   is exhausted: slow or halt feature releases and redirect effort to reliability until the
   service is back within objective (CL049). This is the neutral arbiter that aligns both sides — a
   shared budget means a feature team that spends the budget through outages owns the reliability
   cost, creating mutual accountability (CL060).
6. **Alert on symptoms and burn rate, not every cause (P008).** Page on user-visible symptoms and
   SLO burn rate, using multiple burn-rate windows to catch real problems early while limiting
   false pages (CL051) — not on every internal cause.
7. **Watch on-call load as a reliability signal (P008).** Treat persistently high pager volume as
   systemic reliability debt warranting engineering investment, not heroics (CL052); route the
   detail to `reducing-toil-and-on-call-load`.
8. **For `validate` requests,** check the design against the chain: user-facing SLIs → explicit SLO
   → derived error budget → written error-budget policy → symptom/burn-rate alerting. Name each
   missing link and what would close it.

## Inputs

- The service, its users, and what "reliable" means to them.
- Current targets and alerting (or their absence), and how dev/ops decide reliability vs feature
  work today.
- Whether the ask is to advise, review, validate readiness, or compare options.

## Output

An SLI/SLO definition, a derived error budget, an explicit error-budget policy stating what happens
when the budget is spent, and symptom/burn-rate alerting guidance — each tied to P002/P008. For
`validate`, a pass-or-gap line per link in the chain.

## References

- `references/sre-slo-and-error-budget-reference.md` — definitions and the SLI/SLO/error-budget
  taxonomy.
- Sibling skills: `reducing-toil-and-on-call-load`, `running-blameless-postmortems`.

## Provenance

Derived from principles P002 and P008 (claims CL045, CL046, CL048, CL049, CL050, CL051, CL052,
CL060; evidence EV045–EV052 as listed) in `comp500-15893c30` (The Site Reliability Workbook;
distillation-only — paraphrase, no verbatim quotation). These are expert SRE practices presented as
recommended practice rather than controlled studies; specific numeric targets are the team's to set
against current service data.
