---
name: evals
description: "Designing and maintaining evaluations for LLM prompts, agents, and Agent Skills: success criteria, test-set composition, code/LLM-judge/human graders, trajectory and tool-use grading, trigger evals, regression suites, eval saturation. WHEN: \"eval\", \"evaluation suite\", \"LLM-as-judge\", \"grader\", \"rubric grading\", \"pass@k\", \"pass^k\", \"test set for my prompt\", \"how do I know my agent got better\", \"trigger evals\", \"trace grading\", \"oaieval\", \"OpenAI Evals API\", \"benchmark contamination\". Do NOT use for: authoring SKILL.md content itself (use `agent-skills`); training/tuning runs and their loss metrics (use `fine-tuning`); building training corpora rather than test sets (use `training-datasets`); picking which frontier model to ship (use `model-selection`); red-teaming and prompt-injection defenses (use `ai-security`); Messages API parameters and tool-use wire format (use `claude-api`)."
license: MIT
---

# Evals for models, agents, and skills

An evaluation is a test for an AI system: give it an input, apply grading logic to its output, measure success. Everything below serves that one loop.

## Route the request first

| Request | Do this | Deep reference |
|---|---|---|
| "Is my prompt good enough to ship?" | Write SMART criteria, then a graded test set | `references/success-criteria-and-test-sets.md` |
| "How do I grade open-ended output?" | Pick grader type, design the judge prompt | `references/graders-and-llm-judge.md` |
| "My agent works sometimes" | Trajectory evals, pass@k / pass^k, outcome grading | `references/agent-and-trajectory-evals.md` |
| "Does my Skill trigger / help?" | Baseline-vs-Skill evals + trigger evals | `references/skill-evals.md` |
| "Which eval platform/harness?" | OpenAI Evals API, Datasets, `openai/evals` OSS | `references/openai-evals.md` |
| "Are my numbers real?" | Saturation, contamination, held-out refresh | `references/model-benchmarks-and-contamination.md` |
| OpenAI hosted-Evals sunset dates | Lifecycle facts and migration posture | `references/versions/openai-hosted-evals-2026.md` |

## Non-negotiable directives

**Always define measurable success criteria before writing a single test case.** Anthropic's SMART framing: Specific, Measurable, Achievable, Relevant. "Safe outputs" is not a criterion; "less than 0.1% of outputs out of 10,000 trials flagged for toxicity by our content filter" is.

**Always evaluate multiple dimensions at once.** Real applications need task fidelity *and* latency *and* cost *and* safety simultaneously. A single headline metric hides the regression you actually shipped.

**Always prefer volume with automated grading over a handful of hand-graded cases.** More questions with slightly lower-signal automated grading beats fewer high-quality manual evals — hand-grading does not survive contact with iteration speed.

**Never grade with the same model instance that generated the output.** Use a separate model/instance for judging; self-grading inflates scores.

**Never grade the path when you can grade the outcome.** Rigid step-sequence assertions penalize valid alternative solutions that frontier models find. Assert on final state and required-tool-call sets, not exact orderings.

**Never accept a 100% pass rate as good news.** That is eval saturation: the suite has stopped producing improvement signal. Refresh it with harder cases.

**Never conclude "the agent can't do this" from 0% pass@100.** That almost always means a broken or ambiguous task. Audit the task spec first.

**Always re-read raw transcripts periodically**, even when the grader is green. Graders measure a proxy; transcripts show what actually happened. What agents omit from their stated reasoning is more diagnostic than what they report.

## Success criteria

Write criteria that a stranger could verify without asking you a question. Anthropic's worked example: "Achieve an F1 score of at least 0.85 on a held-out test set of 10,000 diverse Twitter posts, a 5% improvement over baseline."

Cover these eight categories; drop the ones that genuinely don't apply and say why:
task fidelity, consistency, relevance/coherence, tone and style, privacy preservation, context utilization, latency, price.

Metric families: task-specific (F1, BLEU, ROUGE-L, perplexity), generic (accuracy/precision/recall), operational (ms, uptime, cost per call), qualitative (Likert scales, expert rubrics). Qualitative measures are valid only when applied consistently *alongside* quantitative ones.

## Test-set design

**Composition target** (Anthropic): 60–70% core/typical cases, 20–30% edge cases, 5–10% adversarial cases. Skewing to typical cases produces a suite that passes forever and catches nothing.

**Volume floors by use case:** sentiment/classification 1,000+; summarization 200+; customer service 100+; privacy/safety 500+; consistency 50+ groups of 3–5 paraphrases; context utilization 100+ multi-turn conversations. For a new *agent* eval, start at 20–50 tasks sourced from real observed failures rather than waiting for a comprehensive suite.

**Always mine existing artifacts first.** Manual QA checklists, bug reports, and production feedback convert directly into test cases and carry real-world distribution for free.

**Edge-case checklist:** typos and formatting anomalies, sarcasm/irony, mixed sentiment, implicit information, extremely long input, missing information, genuinely ambiguous cases where humans disagree, irrelevant or nonexistent input data, hostile user input. OpenAI adds: multilingual and non-text input, multiple intents in one request, ambiguous tool responses, jailbreak attempts, conflicting instructions.

**Always include negative cases.** A suite that only rewards one dimension pushes the system toward one-sided behavior — e.g. an agent that always escalates because escalation is never penalized.

**Always write specs two experts would grade identically.** If two domain experts reading the same transcript disagree on pass/fail, the task spec is the defect, not the model.

## Anatomy of a minimum viable suite

Ship this before ship anything else. It is small enough to build in an afternoon and it catches the regressions that matter.

1. **A criteria file** — the SMART criteria and their thresholds, in version control next to the prompt or Skill they gate. If the threshold lives only in someone's head, the suite has no pass condition.
2. **A cases file** — JSONL or CSV, one row per test, each row carrying the input plus whatever ground truth the grader needs (expected label, reference answer, `expected_behavior` checklist, `should_trigger` boolean).
3. **A runner** — for prompts, a loop over cases calling the model; for agents, a `while` loop alternating model and tool calls per task, each in a clean environment; for Skills, the harness you build yourself since there is no built-in Skill eval runner.
4. **Graders** — code graders first, LLM judge for what code can't check.
5. **A report** — pass rate, per-criterion breakdown, and the *list of failing cases with their outputs*. A bare percentage is not actionable; the failure list is the whole point.
6. **A held-out slice** never used during iteration, to detect overfitting to the cases you tuned against.

Record token consumption and wall-clock time per run from day one. Retrofitting cost telemetry after the suite grows is far more work than adding it at the start.

## Choosing a grader

| Grader | Use when | Cost of getting it wrong |
|---|---|---|
| Code-based (exact/fuzzy match, regex, unit tests, static analysis, state checks, tool-call verification) | Answer is categorical, structural, or verifiable by executing something | Brittleness — rejects `96.124991` when it expected `96.12` |
| Model-based (LLM-as-judge: rubric scoring, NL assertions, pairwise comparison, multi-judge consensus) | Output is open-ended, subjective, or long-form | Non-determinism and cost; needs human calibration |
| Human (SME review, spot-check sampling, A/B) | Gold standard, calibration set, high-stakes launches | Slow and expensive; use as calibration, not the main loop |

Default: code graders for everything checkable, LLM judge for the residue, humans to calibrate the judge. Combine methods — automated evals plus production monitoring plus A/B tests plus manual transcript review.

**Always implement partial credit for multi-component tasks.** All-or-nothing scoring throws away the signal that tells you which sub-step regressed.

Read `references/graders-and-llm-judge.md` before writing a judge prompt — it carries the grading-prompt template, the six Anthropic evaluation methods with code, and target thresholds per metric.

## LLM-as-judge rules

- Different model for grading than generation. Non-negotiable.
- State criteria explicitly in the grading prompt, with a descriptor for every rating level.
- Constrain the output format to something parseable — a bare number, `yes`/`no`, or a JSON Schema. Validate and handle parse failures explicitly rather than silently scoring zero.
- Prefer pass/fail over fine-grained numeric scales for reliability (OpenAI). Reserve 1–5 Likert/ordinal scales for tone, style, and context-utilization dimensions.
- Anchor human and model rubrics with example outputs at several score levels, and take consensus votes across multiple reviewers/judges.
- Control for response-length bias — judges systematically favor longer answers.
- Validate that the automated metric agrees with human labels *before* optimizing the judge for cost or latency.

## Agent and trajectory evals

Agents are harder than single-turn prompts because of multi-turn state, error propagation across turns, valid-but-unexpected solutions, and success that lives in environment state rather than transcript text.

**Always isolate trial environments.** Every trial starts from a clean state, or failures correlate through shared infrastructure and you debug noise.

**Metrics beyond top-line accuracy** — track total task and per-tool-call runtime, number of tool calls, total token consumption, and tool errors. Redundant calls mean parameters need adjusting; repeated invalid parameters mean the *tool description* needs clarifying, not the model.

**Repeated-trial metrics:** `pass@k` (at least one success in k attempts) for tasks where one good solution suffices, e.g. code generation. `pass^k` (all k attempts succeed) for customer-facing agents where consistency is the product.

**Trace grading** (OpenAI framing) answers workflow-level questions fast: did the agent pick the right tool, did the handoff fire, did the run violate an instruction or safety policy, what did that routing change actually do.

Run agent evals programmatically — a simple `while`-loop wrapping alternating model calls and tool calls, one loop per task, each paired with a verifiable outcome. Enabling interleaved thinking during eval runs surfaces *why* a tool was or wasn't called.

Watch for reward hacking: any loophole that lets the agent satisfy the grader without solving the task will eventually be found.

Read `references/agent-and-trajectory-evals.md` for the rubric structures (coding-agent and support-agent task cards) and the full pitfall list.

## Evaluating Agent Skills

**Always create evaluations BEFORE writing extensive Skill documentation.** Anthropic states this directly — it keeps a Skill anchored to real failures instead of imagined ones.

The loop: run Claude on representative tasks *without* the Skill and record the specific failures → build at least three eval scenarios targeting those gaps → measure the baseline → write the minimum instructions that pass → iterate. There is no built-in eval runner for Skills; you build the harness. Evaluations are the source of truth for Skill effectiveness.

**Five dimensions to clear before production:** triggering accuracy, isolation behavior (works alone), coexistence (doesn't steal triggers or degrade siblings), instruction following, output quality.

**Always test in isolation AND alongside the active Skill set.** An overly broad description that steals a sibling's triggers only shows up in coexistence testing.

**Always test across Haiku, Sonnet, and Opus.** Instructions sufficient for Opus frequently underspecify for Haiku.

**Always phrase trigger tests in your own words, not the description's wording** — otherwise you are testing string overlap, not routing.

### The trigger-eval pattern (this marketplace)

Each plugin here keeps `evals/trigger-evals.json` with one positive and one near-miss negative prompt per skill. That pattern is the minimum viable implementation of the guidance above: submit 3–5 representative queries per Skill covering should-trigger, should-NOT-trigger, and ambiguous edge cases. The near-miss negative is the load-bearing half — it is what detects a description that has grown too broad.

Shape used here — one positive and one near-miss negative per skill, in `<plugin>/evals/trigger-evals.json`:

```json
{
  "id": "<skill>-pos",  "skill": "<skill>",
  "prompt": "<realistic request in the user's own words>",
  "should_trigger": true
}
```

Rules that make the pattern work rather than merely exist:

- **Write the negative against the *sibling* it would be confused with**, not against an unrelated topic. A negative prompt about databases proves nothing for an eval skill; a negative prompt about tuning hyperparameters proves the `fine-tuning` boundary holds.
- **Never reuse the description's wording** in the prompt. Overlap turns a routing test into a string-match test.
- **Never let two cases share a prompt.** Duplicated prompts inflate the case count and measure the same thing twice.

Add a case whenever you add or rename a skill; run `scripts/lint-trigger-evals.py` to catch missing pairs and duplicated prompts.

**Recall degrades as Skill count grows.** API requests support a maximum of 8 Skills per request, and each additional Skill's name+description competes for attention. Use the eval suite to measure recall as you add Skills and stop adding when it degrades. Consolidate narrow Skills into a broader one only when the merged Skill's evals confirm equivalent performance to the ones it replaces.

Read `references/skill-evals.md` for the eval-case JSON structure, the Claude A/Claude B refinement pattern, observation signals, and the enterprise lifecycle/governance policy.

## Diagnosing a suspicious result

| Symptom | Most likely cause | Fix |
|---|---|---|
| 100% pass rate | Saturation — the suite stopped discriminating | Add harder edge and adversarial cases |
| 0% pass@100 on one task | Broken or ambiguous task spec, not model incapability | Audit the spec; have a second expert grade a transcript |
| Score moves on reruns with no change | Non-deterministic judge, or shared state between trials | Pin judge temperature, isolate environments, average over trials |
| Judge scores high, humans disagree | Judge not calibrated; length bias | Re-anchor the rubric with example outputs; validate agreement against human labels |
| Passes evals, fails in production | Test distribution doesn't match real traffic | Rebuild cases from production data and bug reports |
| Improvements don't generalize | Overfitting to the iteration set | Score on the held-out slice |
| Grader green, transcript wrong | Reward hacking or a proxy metric | Read raw transcripts; close the loophole; assert on final state |

## Regression testing and lifecycle

- Run evals on **every change** — eval-driven development, not a one-time gate.
- Pin Skills and prompts to specific versions in production; require the full suite to pass before promoting a new version; keep the previous version as immediate rollback.
- Rerun suites periodically even with no code change — models and workflows drift underneath you.
- Use held-out test sets during iteration so improvements generalize rather than overfitting to the cases you tuned against.
- Feed results into lifecycle decisions: declining trigger accuracy → fix the description; coexistence conflicts → consolidate or narrow; persistent failures across versions → deprecate.

## Contamination and saturation cautions

State clearly what is and isn't verified here. Anthropic and OpenAI documentation fetched for this skill contains **no explicit contamination checklist for custom application evals**; treat any such checklist as your own engineering judgment, not vendor guidance. What *is* documented:

- Eval saturation (100% pass) is the same observable failure as contamination — the suite no longer discriminates. Refresh it.
- Held-out suites rerun on every version bump are the documented mechanism for catching regression and drift.
- Public benchmark datasets (including `anthropics/evals` model-written evals) are on the open internet and therefore plausibly in training data. Never use a published benchmark as your sole ship gate.

Read `references/model-benchmarks-and-contamination.md` for the `anthropics/evals` dataset collections and the DeepMind Frontier Safety Framework material, including what that source does and does not establish.

## Reference files

- `references/success-criteria-and-test-sets.md` — SMART criteria, eight criteria categories, metric families, test-set composition and volume floors, edge-case taxonomy, iterative workflow.
- `references/graders-and-llm-judge.md` — six Anthropic evaluation methods with code, metric/target table, grading-prompt template, judge best practices, OpenAI grader-type catalog.
- `references/agent-and-trajectory-evals.md` — agent eval design strategies, three grader types, rubric task cards, pass@k/pass^k, tool-use metrics, pitfalls, collaborative iteration.
- `references/skill-evals.md` — eval-driven Skill authoring, eval-case JSON, Claude A/B pattern, five production dimensions, enterprise lifecycle/governance, recall limits, OpenAI's `codex exec` skill-eval methodology with deterministic and rubric grading.
- `references/openai-evals.md` — Evals API config and graders, Datasets workflow, `openai/evals` OSS framework (templates, registry YAML, `oaieval`, completion functions, custom evals).
- `references/model-benchmarks-and-contamination.md` — `anthropics/evals` collections, DeepMind FSF capability levels, contamination guidance and its documented limits.
- `references/versions/openai-hosted-evals-2026.md` — hosted Evals read-only and shutdown dates, what replaces it, what is unaffected.

## Scripts

- `scripts/lint-trigger-evals.py` — read-only linter for a plugin's `evals/trigger-evals.json`: flags skills missing a positive or negative case, duplicate/near-duplicate prompts, and skills present on disk with no eval coverage. Run: `python scripts/lint-trigger-evals.py <path-to-plugin-dir>`.

## Sources

- https://platform.claude.com/docs/en/test-and-evaluate/define-success
- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise
- https://developers.openai.com/api/docs/guides/evals
- https://developers.openai.com/api/docs/guides/evaluation-best-practices
- https://developers.openai.com/api/docs/guides/agent-evals
- https://developers.openai.com/api/docs/guides/evaluation-getting-started
- https://developers.openai.com/blog/eval-skills
- https://github.com/openai/evals
- https://github.com/anthropics/evals/blob/main/README.md
- https://deepmind.google/blog/updating-the-frontier-safety-framework/

Fetched: 2026-08-05
