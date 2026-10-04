---
name: evaluating-mcp-agents-and-judges
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P009
  - P019
  - P022
  - P023
  - P036
  - P040
  - P053
  - P056
  - P059
  - P063
  - P066
  - P067
  - P068
  - P074
  - P078
  - P079
  - P082
  - P083
  - P084
  - P089
  - P095
  - P097
  - P103
  - P119
  - P120
  - P121
  - P122
  - P130
  - P137
  - P139
  - P140
  - P141
  - P147
  - P148
  - P181
  - P182
  - P183
  - P190
  - P191
  - P192
  - P193
  - P194
  authored_from_digest: 4b4a4152fa8d571bec49ba36ac06c1255c135e3911125ae2414211c6cab50790
---

# Skill: evaluating-mcp-agents-and-judges

## Purpose

Design an evaluation that proves an MCP agent's or server's quality with measurement rather than
assertion: choose metrics for the reliability question, evaluate against real servers, construct sound
benchmarks, and reliability-check any LLM judge before trusting it [P022], [P019], [P084].

## When to use

- Proving or improving an MCP agent's or server's quality with an evaluation.
- Choosing metrics, real-vs-mocked servers, benchmark construction, or a grading strategy.
- Deciding whether and how to use an LLM-as-a-Judge, and localising failures.

## Procedure

1. **Evaluate against real servers, eval-first.** Run against exclusively real, production servers so
   authentic error modes appear; treat evals as routine development artifacts defined early and iterated
   like unit tests [P022], [P121].
2. **Select metrics to match the reliability question.** Use single-run success or pass@k when one success
   suffices, pass^k when every attempt must succeed; read classification metrics (precision/recall per
   tool) diagnostically and watch for saturation [P019], [P040], [P068].
3. **Choose grader types by trade-off.** Prefer deterministic code-based graders where possible; use an
   LLM judge for open-ended quality, and score argument correctness with targeted metrics (hallucinated
   names, missing required, wrong values) [P067], [P148].
4. **Do not trust a single judge blindly.** Choose a strong judge and use multi-model majority voting when
   reliability is uncertain; before deploying a judge, run a reliability suite that stress-tests it with
   meaning-preserving perturbations and requires format invariance [P009], [P084], [P097].
5. **Construct benchmarks soundly.** Use a two-stage proposer/validator human pipeline; build the tool
   environment from stable, reproducible real interfaces; decompose tasks into explicit completion
   criteria grounded against raw outputs to resist tool-use hallucination [P083], [P063], [P082].
6. **Evaluate realistic multi-tool flows.** Exercise large-scale, multi-server, dynamic toolsets that force
   real retrieval and composition; single-tool-call evaluation does not cover sequential flows where later
   calls consume earlier outputs [P137], [P147].
7. **Localise failures and read transcripts.** Structure diagnostic judging around the verified evidence
   trace, expected vs missed claims, and actual behaviour; read transcripts and grades regularly and
   verify tasks and graders are fair before trusting poor scores [P190], [P140], [P141].

## Pitfalls / anti-patterns

- Presenting a server or agent as high quality without an evaluation against real servers [P022].
- Assuming the largest or most expensive model is the best judge [P036].
- Assuming MCP wrapping alone improves accuracy over an equivalent function-call implementation [P122].

## Principles applied

- **[P007]** Diagnose agent failures into distinct categories - query errors (poor or wrong-granularity queries from weak task decomposition), retrieve errors (retriever misses a semantically equivalent tool), tool errors (correct tool invoked with wrong parameters), and other errors (unhandled transient failures) - and route each to its own remediation.
- **[P009]** Choose a strong judge model for LLM-as-a-Judge evaluation, and when any single evaluator's reliability is uncertain use multi-model majority voting; relative agent rankings are robust to evaluator bias even though absolute agreement varies by judge.
- **[P019]** Select evaluation metrics to match the reliability question: use single-run success or pass@k when one successful attempt is enough, and pass^k when every attempt must succeed consistently.
- **[P022]** Run evaluation against exclusively real, production servers rather than mocked substitutes so authentic error modes (rate limits, pagination, schema-version mismatches, transient errors) are exercised.
- **[P023]** Include reasoning-intensive, multi-step tasks that require resolving indirect or scattered clues across sources to reach a specific answer.
- **[P036]** Do not assume any single judge is uniformly reliable, or that the largest or most expensive model is the best judge; benchmark cost against reliability, since a smaller, cheaper open model can match or beat premium frontier judges at a fraction of the inference cost.
- **[P040]** Read the classification metrics diagnostically: low precision for a tool means it is being over-triggered (called when not expected), and low recall typically means it is under-triggered (missed, or confused with another tool); when two semantically similar tools are confused, expect the over-called tool's precision and the under-called tool's recall to both drop.
- **[P053]** Understand each evaluation method's trade-offs before relying on it: automated evals give fast, reproducible, no-user-impact iteration but need maintenance and can create false confidence; production monitoring gives ground truth but is reactive and noisy; A/B testing measures real outcomes and controls confounds but is slow and needs traffic; user feedback surfaces unanticipated problems but is sparse and skewed; manual transcript review builds intuition but doesn't scale; human studies are gold-standard but expensive and slow.
- **[P056]** Measure a description change with execution-based metrics rather than assuming its effect: Success Rate, Average Evaluator score (partial completion), and Average Steps as a cost proxy, using a benchmark that combines programmatic evaluators with LLM judgment; a Tool Description Router can swap description variants at runtime to run these comparisons without changing server code, and augmentation reliably lifts rubric scores whose task-level payoff must still be measured.
- **[P059]** Establish protocol-level orchestration benchmarks and validator suites that emit binary results plus structured failure traces; without them, orchestration failures under injected errors go undetected and model benchmarks miss multi-tool correctness.
- **[P063]** Build the tool environment from stable, reproducible interfaces rather than unstable or simulated APIs: aggregate real MCP servers, drop any that require proprietary API keys, curate and vet for quality, and pin a dependency-free, containerized, security-checked toolset version.
- **[P066]** Report efficiency work reproducibly and honestly: fix seeds, release a no-API token-counting harness, validate on a community-standard benchmark rather than only synthetic (even if calibrated) workloads, and explicitly mark projected downstream metrics as extrapolations to be verified against live agents.
- **[P067]** Choose grader types by trade-off: prefer deterministic code-based graders where possible (fast, cheap, reproducible, but brittle to valid variation), use model-based graders where flexibility or nuance is needed (scalable but non-deterministic and needing calibration), and use human graders judiciously for validation (gold standard but expensive and slow).
- **[P068]** Watch for saturation: an eval at 100% pass rate tracks regressions but gives no signal for improvement, and near saturation large capability gains show up as small score increases (e.g. SWE-Bench Verified moved from ~30% to >80% within a year), so retire or refresh saturated evals for capability measurement.
- **[P074]** Select an MCP orchestration pattern by its trade-off and cover its dominant failure mode, and defer costly tool invocations when confidence is low or context is absent: static composition is auditable but brittle to drift, dynamic orchestration generalizes but needs runtime checks, multi-agent coordination parallelizes but risks memory leakage.
- **[P078]** Judge efficiency by execution steps on a cost-accuracy Pareto frontier rather than by model size: richer descriptions push most tasks to more steps, and a smaller model can dominate a larger one that spends more steps for equal or lower accuracy.
- **[P079]** Expect a wide performance spread across MCP servers (measured accuracy ~10-64%, latency <15s to ~231s) and select a server by benchmarking candidates on your own task instead of trusting popularity or defaults.
- **[P082]** Make evaluation robust to tool-use hallucination by decomposing the task into explicit completion criteria and grounding each key point against the raw tool outputs, rather than trusting the agent's self-reported completion or brittle rule-based/answer-based checks that do not scale in dynamic environments.
- **[P083]** Construct benchmark tasks with a two-stage human pipeline of separate proposers and validators, allowing LLM-assisted ideation only when each candidate task is human-vetted for authenticity, and having verifiers consolidate duplicates and check feasibility and execution quality.
- **[P084]** Before trusting or deploying an LLM judge, run a reliability validation suite that stress-tests it with targeted perturbations rather than relying on a single point estimate of agreement with human raters on a small validation set.
- **[P089]** Structure the offline evaluation pipeline as three stages — fulfillment (run each benchmark across multiple models with the full tool list supplied, recording invoked tools and arguments), evaluation (compute metrics and scores from the raw outputs), and summarization (aggregate dataset-level statistics into a final report).
- **[P095]** Scope MCP audit conclusions to their validity boundaries: prevalence rates come from a public-server corpus (prototypes overrepresented), the proposed extensions are unvalidated testbed reference prototypes, and rates depend on the operational definitions used, so do not over-generalize them to proprietary or production systems.
- **[P097]** Test a judge's consistency with meaning-preserving perturbations — formatting-only changes, semantic paraphrase, and verbosity variants — and require its score to stay constant when the underlying quality is unchanged.
- **[P103]** Bound the agent reasoning loop with an explicit maximum-iteration cap, and on retry have the evaluator return structured feedback that the planner consumes to revise the plan.
- **[P119]** Treat tool-use hallucination as real but low-prevalence and largely detectable (about 9% of invocations, ~1.6% evaluation inconsistency, detection stable across judges), while still guarding the known weak spot: evaluators overlook critical details in excessively long, complex trajectories.
- **[P120]** Use one shared failure-mode vocabulary for human reviewers and automated diagnostic judges, assigning the primary root-cause mode plus contributing modes with explicit confidence and disambiguation rules.
- **[P121]** Treat evaluations as routine development artifacts: define realistic capability evals early, iterate on them like unit tests, and use them to make progress and unstated expectations visible.
- **[P122]** Do not assume an MCP server outperforms an equivalent function-call/tool-use implementation on accuracy; MCP wrapping alone yields no measured accuracy gain, so justify MCP adoption by other benefits (standardization, interoperability) rather than expected accuracy.
- **[P130]** Build a fault taxonomy for an immature domain inductively: use faceted, bottom-up open coding rather than predefined categories, code artifacts independently with multiple coders and report inter-rater agreement, and iterate through refinement rounds until no new categories emerge (saturation).
- **[P137]** Evaluate MCP tool-use agents on large-scale, multi-server, dynamic toolsets that force real tool retrieval and multi-tool composition; do not rely on single-server setups that inject a fixed tool list directly into the model context.
- **[P139]** Expect cognitive failures to dominate once basic tool mechanics are solved: the bottleneck moves to deciding when enough evidence is gathered and synthesizing the answer, so target claim-aware stopping criteria and trajectory-grounded verification of the answer against collected evidence.
- **[P140]** Read transcripts and grades from many trials regularly and invest in transcript-viewing tooling, because you cannot know whether graders work without doing so; a failed-task transcript reveals whether the agent made a genuine mistake or the grader rejected a valid solution.
- **[P141]** Before trusting poor eval scores, verify that the tasks and graders are fair, unambiguous, and correctly configured so failures reflect agent behavior rather than broken evaluation.
- **[P147]** Recognize that single-tool-call evaluation does not cover real sequential multi-tool flows, where later calls consume earlier outputs; to evaluate such flows, actually execute the tool calls or faithfully mock their responses instead of only fetching the tool list, and score selection as multi-label (not multi-class) classification when one input can trigger several tools.
- **[P148]** Score argument correctness with four targeted metrics — argument hallucination (arg names not defined for the tool), all-expected-arguments-provided, all-required-arguments-provided, and exact value match — and compute them only over tool calls that were correctly selected.
- **[P181]** For coding agents, rely on deterministic outcome tests (does the code run, do the tests pass) plus an LLM rubric for overall code quality, adding heuristic code-quality rules and transcript grading of tool/user interaction only as needed.
- **[P182]** Build evals early in development, when product requirements translate naturally into test cases; waiting forces you to reverse-engineer success criteria from a live system.
- **[P183]** Explicitly test format invariance (blank lines, extra spaces, indentation), because judges are frequently more brittle to formatting than to semantic changes and formatting brittleness can distort downstream model comparisons and leaderboards even when meaning is unchanged.
- **[P190]** Structure diagnostic judging around the verified evidence trace, expected claims, missed claims, and actual behavior so failures are localized without penalizing alternative valid plans.
- **[P191]** Treat the coverage threshold as a reporting decision (the rubric returns a real-valued coverage score), report mean coverage and pass rate at several thresholds, and expect model rankings to be largely preserved across thresholds.
- **[P192]** For conversational agents, evaluate the interaction itself: combine verifiable end-state outcomes, transcript constraints (e.g. finished under N turns), and LLM rubrics for task completion and interaction quality, often using a second LLM to simulate the user across multi-turn dialogue.
- **[P193]** Treat the eval suite as a living artifact with clear ownership: a durable model is a dedicated evals team owning core infrastructure while domain experts and product teams contribute most tasks and run the evaluations themselves.
- **[P194]** Profile MCP at the protocol level rather than as an end-to-end black box: standardization removes n-by-m integration glue but adds schema-discovery, injection, and context-management overhead that answer-level benchmarks miss and that affects latency and tokens even when answer quality is unchanged.

Sources are distillation-only: this skill paraphrases and restructures; no verbatim source quotation.

