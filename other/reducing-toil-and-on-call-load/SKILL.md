---
name: reducing-toil-and-on-call-load
kind: skill
status: ready
provenance:
  principles:
  - P020
  - P009
  - P016
  - P022
  - P024
  - P025
  claims:
  - C00765
  - C00773
  - C01878
  - C00731
  - C00732
  - C00733
  - C00734
  - C01950
  - C00483
  - C00594
  - C00595
  - C00813
  evidence:
  - E00339
  - E00340
  - E00559
  - E00335
  - E00336
  - E00337
  - E00338
  - E00563
  - E00259
  - E00302
  - E00303
  - E00349
  source_anchors:
  - 9fe26df35c80-c0011
  - 0bea4daa68ab-c0008
  - 9fe26df35c80-c0009
  - 0bea4daa68ab-c0011
  - 50b64948b031-c0006
  - 9fe26df35c80-c0004
  - 9fe26df35c80-c0013
  authored_from_digest: e0b4db28d53a5ed37e5fc1e99331105ed748a00ba65c4376f31f1280335c33d2
---

# Reducing toil and on-call load

## Purpose

Keep operational work sustainable by treating toil as a measured quantity to cap and engineer away
(P003), and by keeping on-call pager load low through symptom/burn-rate alerting and a clear sense
of when noise signals reliability debt (P008). SRE applies software-engineering methods to
operations — operational work is a problem to be solved with engineering, not absorbed
indefinitely (CL045).

## When to use

- On-call or ops work is dominated by repetitive manual tasks.
- Reviewing how an SRE/ops team spends its time.
- On-call is noisy — paging on causes rather than user impact — or the pager is burning people out.

Do not apply it where a task is genuinely one-off or requires irreducible human judgement — not all
manual work is toil. For a low-traffic internal tool with no real on-call burden, the model adds
little.

## Procedure

1. **Name what counts as toil (P003).** Toil is manual, repetitive, automatable operational work
   with no enduring value that scales with the service (CL047). Separate it from project work and
   from judgement-heavy work that should stay human.
2. **Measure it.** Quantify how much of the team's (especially on-call) time goes to toil. You
   cannot cap or reduce what you do not measure.
3. **Cap and engineer it away (P003).** Set a ceiling on toil as a share of time and treat work
   above the cap as a backlog to automate or eliminate — engineer the work away rather than
   absorbing it indefinitely (CL047).
4. **Cut alert noise at the source (P008).** Move alerting onto user-visible symptoms and SLO burn
   rate rather than every internal cause, using multiple burn-rate windows to catch real problems
   early while limiting false pages (CL051); make sure the SLIs behind those alerts reflect real
   user experience (CL050). Most pager noise is cause-based alerting that never needed a human.
5. **Read pager volume as a signal (P008).** Treat persistently high alert volume as systemic
   reliability debt that warrants engineering investment, not heroics or a bigger rota (CL052).
   Rising load is a prompt to fix the system, not to push people harder.
6. **Keep the incidents that remain organised.** Run incidents under a defined command structure
   with a clear incident commander coordinating mitigation and communication, so response is
   organised rather than chaotic (CL053) — which also limits the human cost of being on call.
7. **For `review`/`validate` requests,** assess: is toil measured and capped? Are alerts on
   symptoms/burn rate or on causes? Is high pager load being treated as debt to engineer away or as
   a staffing problem? Name each gap and the principle at stake.

## Inputs

- How on-call/ops time is spent today, and any measure of toil or pager volume.
- The current alerting design (symptom-based vs cause-based) and the SLIs behind it.
- Whether the ask is to advise, review, or validate against a sustainability bar.

## Output

A toil-and-on-call assessment: what counts as toil here, how to measure and cap it, where alerting
should move to cut noise, and how to read pager load as reliability debt — each tied to P003/P008.
For `validate`, a pass-or-gap line per element.

## References

- `references/sre-slo-and-error-budget-reference.md` — SLIs, burn-rate alerting, and the
  reliability model behind sustainable on-call.
- Sibling skills: `defining-slos-and-error-budgets`, `running-blameless-postmortems`.

## Provenance

Derived from principles P003 and P008 (claims CL045, CL047, CL050, CL051, CL052, CL053; evidence
EV045, EV047, EV050, EV051, EV052, EV053) in `comp500-15893c30` (distillation-only — paraphrase,
no verbatim quotation). These are expert SRE practices; specific toil caps and alert thresholds are
the team's to set against current operational data.
