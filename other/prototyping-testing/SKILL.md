---
name: prototyping-testing
metadata:
  version: "1.0.0"
allowed-tools: "Read, Write"
description: >
  Prototyping and testing skill set covering prototyping strategy selection,
  usability test planning, heuristic evaluation, A/B experiment design, tree
  testing, five-second tests, concept testing, and research metrics frameworks.
  Use when asked to: choose a prototyping approach, plan or run a usability
  test, evaluate a design with heuristics, design an A/B experiment, run tree
  testing, validate a concept, assess design quality, define research metrics,
  calculate sample size, write task scenarios, or build a test plan. Also
  triggers on: prototype fidelity, clickable prototype, wireframe, lo-fi,
  usability test plan, think-aloud, Nielsen heuristics, heuristic severity,
  SUS score, SEQ, HEART framework, sample size, statistical power, p-value,
  tree test, IA validation, first-click, directness, five-second test,
  concept test, desirability testing, assumption mapping, or research metrics.
---

# Prototyping + Testing

Choose the right method, run it correctly, interpret results accurately.

<intake>

**Route by what the user needs to do:**

| User Says | Route To |
|-----------|----------|
| "how should I prototype this" / "what fidelity" / "paper vs clickable" | `references/prototyping-strategy.md` |
| "usability test plan" / "write task scenarios" / "test plan" | `references/usability-testing.md` |
| "evaluate this design" / "find usability issues" / "heuristic review" | `references/heuristic-evaluation.md` |
| "A/B test" / "experiment design" / "test this variation" | `references/ab-experiment-design.md` |
| "tree test" / "validate navigation" / "IA testing" | `references/tree-testing.md` |
| "five-second test" / "first impressions" / "does this land" | `references/five-second-concept-testing.md` |
| "concept test" / "validate this idea" / "assumption mapping" | `references/five-second-concept-testing.md` |
| "measure design quality" / "HEART framework" / "SUS score" / "SEQ" | `references/research-metrics.md` |

**If unclear:** Ask — "Are you choosing how to test, planning a test session, or evaluating an existing design?"

</intake>

<method_overview>

| Method | What it answers | When to use |
|---|---|---|
| Prototyping strategy | What should I build to test this? | Design is not yet testable |
| Usability testing | Can users complete tasks with this design? | Have a prototype or working product |
| Heuristic evaluation | Where are the usability problems? | Need expert review without recruiting users |
| A/B experiment | Which version performs better in production? | Have traffic and a metric to optimize |
| Tree testing | Can users find things in this navigation? | Validating or diagnosing an IA |
| Five-second test | Does the first impression communicate correctly? | Landing pages, new features, brand validation |
| Concept testing | Is this the right direction before we build? | Pre-design or early concept stage |
| Research metrics | How do we measure design quality over time? | Defining what good looks like with numbers |

</method_overview>

<quality_gates>

Before running any test session:

- [ ] Research question defined — what decision will this inform?
- [ ] Success criteria written before the session (not after)
- [ ] Participant screener matches the actual user population
- [ ] Tasks use scenario framing with no feature names in wording
- [ ] Metrics defined: what you will measure and how
- [ ] Recording consent obtained
- [ ] Analysis plan written before data collection begins
- [ ] Stakeholder readout scheduled before sessions start

</quality_gates>

<reference_index>

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/prototyping-strategy.md` | Fidelity types, decision matrix, build timeline | Choosing prototype approach |
| `references/usability-testing.md` | Test plan components, task writing, moderator protocol, analysis | Planning or running a usability test |
| `references/heuristic-evaluation.md` | 10 Nielsen heuristics, severity scale, evaluation process | Conducting a heuristic review |
| `references/ab-experiment-design.md` | Hypothesis format, sample size, anti-patterns, go/no-go criteria | Designing an A/B experiment |
| `references/tree-testing.md` | Setup, metrics, directness vs first-click, benchmarks | Validating information architecture |
| `references/five-second-concept-testing.md` | Five-second test process, desirability testing, assumption mapping | First impressions and concept validation |
| `references/research-metrics.md` | HEART framework, SUS grading scale, SEQ benchmarks | Measuring and interpreting design quality |

</reference_index>

## CLAIMS

- [SOURCED] Nielsen: 5 participants for qualitative moderated usability testing catch ~85% of usability problems on average — nngroup.com/articles/why-you-only-need-to-test-with-5-users. **Caveat:** assumes L=31%. For well-optimized interfaces (L < 31%), more users needed. Faulkner (2003) found groups of 5 found as few as 55%. Treat 5 as minimum for qualitative iteration, not a guaranteed ceiling.
- [SOURCED] SUS average is 68 (50th percentile, C grade on Sauro-Lewis curved grading scale); ≥80 is the common industry goal — Sauro & Lewis (2016); grading scale first published Sauro (2011) measuringu.com/sus
- [UNVERIFIED] Tree testing scale attributed to Albert & Tullis, *Measuring the User Experience* (2013): <60% = significant structural problems; 61–80% = good; 80–90% = very good; >90% = excellent. Cannot confirm this exact breakdown from the primary source — treat as [GENERATED] until verified against the book.
- [SOURCED] Optimal Workshop Treejack: 80%+ per-task success rate = well-performing IA — support.optimalworkshop.com/en/articles/2626846
- [SOURCED] Practitioner consensus (treetesting.atlassian.net): 65+ overall score is acceptable; below 65% = significant IA problems warranting investigation
- [SOURCED] MeasuringU (Sauro, 2013): mean tree test completion 66% across 77 tasks/3 studies — below usability test averages because search and visual cues are absent — measuringu.com/tree-testing-ia
- [SOURCED] [PERSON] (Neo Insight): usability scores average 29% higher than tree test scores on the same IA — a 70% tree score may correspond to ~90% in-product findability
- ! "Below 60% requires redesign" is practitioner shorthand — "warrants significant IA investigation" is the accurate framing; "redesign" is an inference, not a sourced claim
- [SOURCED] SEQ is more sensitive than SUS for individual task-level measurement because it captures perception immediately after a specific task, not the overall system

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- Remote unmoderated testing tools (Maze, Lyssna, UserTesting) have different reliability characteristics — sample bias is a significant concern for non-panel recruitment
- Accessibility-specific testing methods (screen reader sessions, switch access testing) are not covered
- Statistical power calculations for A/B tests assume normally distributed data — non-normal distributions (revenue, session length) require different approaches
