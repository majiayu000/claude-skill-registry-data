---
name: padosoft-ai-evaluation
description: >-
  Use this skill when measuring whether a model-backed feature works — building or changing an evaluation
  harness, a golden dataset, a metric, a scoring report, a regression gate on prompt or model changes. Also
  when the user asks how to know a prompt change made things better, how to stop a model upgrade silently
  regressing, what to put in a test set, how to score free-form output, or wants red-team coverage. It
  covers datasets and reports as versioned artifacts, the isolation an evaluation run needs, cohorts,
  and what must never leak into a report. Do not use it to write application tests
  (padosoft-test-integrity), to choose a model, or to design prompts.
license: MIT
compatibility: >-
  Stack-agnostic. Examples assume a harness that loads a dataset, invokes a system under test and emits a
  report; the artifact-contract rules apply to any of them.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A number without a dataset version and a run identity is not a measurement.
  profiles: ai
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: evaluation, evals, golden dataset, metrics, regression, red team, scoring, llm, harness
---

# AI evaluation harness

A model-backed feature has no failing test to point at: the output is different every time and often
plausibly wrong. So the question "did this change make it better?" is only answerable with a **measurement**
— and a measurement that cannot be reproduced or compared is a number somebody wrote down.

**The rule: a number without a dataset version and a run identity is not a measurement.**

---

## 1. The dataset and the report are versioned artifacts, not files

Both carry a **schema version**, so a consumer can reject what it does not understand instead of
misreading it.

- **Absent version means the original version**, for backward compatibility. An explicit unsupported one
  **fails at load**, loudly.
- **The value objects validate the version in their constructor**, not only the loader. Consumers construct
  them directly, and a check that lives in the parser protects nobody who did not go through the parser.
- **Reject mixed sources at the boundary.** If a dataset can come from a file or be built in code, taking
  metadata from one and samples from the other produces a report about something that never existed.
  Replacing a file-backed set with another file-backed set is fine; switching kind is not.
- **Report identity**: the dataset version, the system version, the model and its parameters, the prompt
  revision, the timestamp. Two reports are comparable only if those match, and the harness is what should
  say so rather than the person reading them.

## 2. What the run must isolate

- **Validate every sample before the first invocation.** Otherwise an invalid sample halfway through aborts
  the run after side effects have already happened.
- **Isolate the failure of one row and one metric.** An exception scoring one sample marks that cell as an
  error and the run continues; a harness that dies on row four hundred has measured nothing and cost
  everything.
- **Timeouts and retries are configuration**, declared per run and recorded in the report — they change the
  result, so they are part of it.
- **The invocation payload is minimal and serialisable.** Passing the whole sample to a queued runner drags
  expected outputs and free-form metadata that may not serialise; pass an input-only object. And a
  serialisation validator that walks structures needs a cycle guard — probe with an encoding attempt before
  the recursive walk exhausts the stack.
- **Compute the dispatch shape once**, outside the loop. Reflection per sample is the easiest performance
  mistake to introduce while supporting several callable shapes.

## 3. Metrics, and the shapes that make them lie

- **Score per sample, aggregate once.** Computing a mean, two percentiles and a pass rate with separate
  passes sorts the same list four times; aggregate in one helper and reuse the sorted values.
- **Round the boundaries of anything that becomes an artifact.** Histogram bucket edges are part of the
  report contract, and binary floating-point noise leaks into dashboards and makes every diff dirty.
- **Decide where the top value lands.** A perfect score must fall in the last bucket, and buckets with no
  samples still appear — an absent bucket and an empty one look different to every consumer.
- **Assertions over precomputed outputs** are a first-class mode: scoring a stored set of answers without
  re-invoking anything is how you iterate on the metric itself.
- **Evaluate components as well as the whole.** An end-to-end score tells you something regressed; a
  component or step score tells you where.

## 4. Cohorts

Tag samples and report per cohort — by feature, language, difficulty, source. A single aggregate hides the
one segment that broke, and the segment that broke is usually the smallest one.

- **A sample with several tags counts in every matching cohort.**
- **Missing is not a tag value.** Modelling untagged samples as a literal tag collides with a real dataset
  that uses that same string. Represent the untagged cohort with a null name and an explicit flag.
- **Filters and splits are part of the dataset**, and so is the ability to promote failing cases from a
  run back into it. That loop — failure becomes a permanent case — is what makes the set improve.

## 5. What must never reach the report

- **Never copy free-form sample metadata into the artifact.** It carries provider payloads, prompts, keys
  and personal data. Export a normalised, named subset until there is a redaction hook — see
  **`padosoft-logging-discipline`**.
- **Escape user-controlled text in rendered reports.** Tag names, metric names and error messages end up in
  table cells: pipes, backticks and newlines break the structure and make the output unparseable. Normalise
  multi-line error text to a single line.
- **A stored transcript is a data sink.** If the harness keeps model inputs and outputs, that store inherits
  every rule about personal data and provenance — see **`padosoft-rag-ingestion-security`**.

## 6. Red-team coverage is a dataset, not a mood

Give adversarial cases the same treatment as functional ones: named categories, samples, expected refusals,
and a score that moves. The categories worth having from the start:

| Category | What it probes |
|---|---|
| Prompt injection, direct and indirect | instructions arriving inside the content |
| Jailbreaks | refusal that holds under pressure and role-play |
| Data exfiltration | secrets, personal data, other tenants' content in the answer |
| Excessive agency | a tool called when the request did not warrant it |
| Server-side request forgery, command and query injection | when the model's output reaches a fetch, a shell or a query |
| Competitor and off-topic endorsement | brand-safety failures that read as helpfulness |

**A refusal is a correct answer**, and the metric has to say so — otherwise the harness rewards the model
that answers everything.

## 7. The gate

An evaluation nobody fails on is a report. Pick the thresholds that block — overall, and per cohort where a
segment matters more — and make the gate **fail closed** on a missing or stale run rather than passing
because the number was absent. A model or prompt change without a comparison run is an unmeasured change;
see **`padosoft-evidence-boundaries`**.

---

## Gotchas

- **A higher average with a worse worst case is usually a regression.** Watch a tail percentile next to the
  mean, and prefer the pass rate over either for gating.
- **Evaluating on the set you tuned on is optimistic.** Keep a held-out split, recorded by digest, and gate
  on that one.
- **A model-as-judge metric is itself a model-backed feature**, with its own drift, its own cost and its
  own need for evaluation. Pin its model and version it like any other component.
- **Non-determinism is a parameter, not a nuisance.** Record the sampling settings; a run at one
  temperature is not comparable to a run at another.
- **A dataset that never changes stops measuring the product** and starts measuring the dataset.
- **The harness is code, and it is the code nobody tests.** A scoring bug moves every number at once and
  looks exactly like a model change.

## Checklist

- [ ] Dataset and report carry a schema version; unsupported fails at load; absent defaults to the original
- [ ] Version validated in the value objects, not only in the loader
- [ ] Mixed sample sources rejected at the boundary
- [ ] Report identity: dataset, system, model, parameters, prompt revision, timestamp
- [ ] Every sample validated before the first invocation
- [ ] Row-level and metric-level failures isolated; timeouts and retries recorded
- [ ] Invocation payload minimal and serialisable; cycle guard on the validator
- [ ] Aggregation done once per metric; artifact boundary values rounded
- [ ] Cohorts reported; multi-tag samples counted in each; untagged modelled explicitly
- [ ] Failing cases promotable back into the dataset
- [ ] No free-form metadata in the report; user-controlled text escaped
- [ ] Red-team categories present, with refusal scored as success
- [ ] A gate with thresholds that fails closed on a missing run

## Final report

```
Run: <id> · dataset <name>@<version> · system <version> · model <id>/<params>
Samples: <n> (cohorts: <list>) · held-out split: <digest>
Results: pass rate <…> · mean <…> · p90 <…> · worst cohort <…>
Errors isolated: rows <n> · metrics <n>
Red team: categories <n/n> · refusal-scored: yes | no
Compared against: <previous run id> — verdict: better | worse | not comparable (<why>)
Gate: <threshold> → pass | fail | no run (fails closed)
```
