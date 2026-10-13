---
name: agent-quality-patterns
description: Apply production-grade quality patterns to AI agents and LLM-powered features. Covers self-critique loops, evaluator-optimizer pipelines, LLM-as-judge scoring, and golden dataset evaluation. Separates prototype-quality ("it worked in my demo") from production-quality ("it works reliably at scale with measurable correctness").
triggers:
  - "agent quality"
  - "LLM as judge"
  - "evaluator optimizer"
  - "self critique"
  - "is this agent ready to ship"
  - "test my agent"
  - "eval pipeline"
  - "agent evals"
  - "prompt regression"
  - "production agent"
audience:
  - engineer
  - manager
---

# Agent Quality Patterns

Move your AI agent from "it worked in my demo" to "it works reliably in production."

---

## The Prototype-to-Production Gap

Most AI agents are shipped at prototype quality. Here's what that looks like:

| Dimension | Prototype | Production |
|---|---|---|
| **Testing** | 3-5 manual examples | Golden dataset of 50-200+ cases |
| **Quality gate** | "Looks good to me" | Scored rubric on every run |
| **Generation** | Single-shot prompt | Generate → evaluate → revise loop |
| **Regression detection** | None | Evals run in CI on every prompt change |
| **Output measurement** | Vibes | Quantified metric (e.g., 87% pass rate) |
| **Failure mode** | Silent degradation | Caught by eval suite before deploy |
| **Prompt changes** | Deployed with fingers crossed | A/B tested against eval baseline |

---

## Pattern 1: Self-Critique Loop

The agent generates an output, then critiques its own output against explicit criteria, then optionally revises.

### When to use
- Single-agent setup (no separate judge model)
- You want quick quality improvement without infrastructure
- Tasks with verifiable correctness (code, SQL, structured output)

### Structure
```
Step 1 — Generate
  SYSTEM: You are a [role]. [Task instructions.]
  USER: [Task]
  → Output: [draft answer]

Step 2 — Critique
  SYSTEM: You are a strict reviewer. Evaluate the following output against these criteria:
    1. [Criterion A — e.g., "Is the SQL syntactically valid?"]
    2. [Criterion B — e.g., "Does it handle NULL inputs?"]
    3. [Criterion C — e.g., "Is it under 10 lines?"]
  USER: Output to review: [draft answer]
  → Output: { "pass": [list], "fail": [list], "score": N/5, "issues": "..." }

Step 3 — Revise (if score < threshold)
  SYSTEM: You are a [role]. Revise the following output to fix these issues: [issues from critique]
  USER: Original output: [draft] \n Issues: [critique output]
  → Output: [revised answer]
```

### Self-critique prompt template
```
Review your previous answer against these criteria. Be critical — do not defend it.

Criteria:
1. [specific, verifiable criterion]
2. [specific, verifiable criterion]
3. [specific, verifiable criterion]

For each criterion, state: PASS or FAIL with a one-sentence reason.
Then state an overall score (0-N) and the top issue to fix.
If score < [threshold], rewrite the answer to fix the issues.
```

### Anti-patterns
- **Sycophantic self-critique**: Model always says PASS to its own output. Fix: Use a separate system prompt with an adversarial persona, or use a separate model for the judge step.
- **Infinite loops**: Set a max revision count (2-3 attempts max).
- **Vague criteria**: "Is it good?" → always passes. "Does it handle the empty string case?" → verifiable.

---

## Pattern 2: Evaluator-Optimizer Pipeline

Two separate roles: a **generator** produces output, an **evaluator** scores it with structured feedback, the generator uses that feedback to retry.

### When to use
- Higher-stakes outputs where single-shot quality is insufficient
- When you want logged, auditable quality scores
- When generator and evaluator benefit from different personas/temperatures

### Architecture
```
┌─────────────┐     draft      ┌─────────────┐
│  Generator  │ ─────────────► │  Evaluator  │
│  (creative, │                │  (critical, │
│  temp=0.7)  │ ◄───────────── │  temp=0.1)  │
└─────────────┘   score+reason └─────────────┘
       │
       │ if score < threshold: retry with feedback
       │ if score >= threshold OR max_attempts: return
       ▼
   Final Output + Audit Log
```

### Evaluator prompt template
```
You are a strict quality evaluator. Score the following output on each dimension from 1-5.
Do not be lenient. A score of 3 means "acceptable but has clear issues."

Output to evaluate:
---
[output]
---

Task context:
---
[original task / user request]
---

Score each dimension:
| Dimension | Score (1-5) | Evidence | Required fix (if < 4) |
|---|---|---|---|
| Correctness | | | |
| Completeness | | | |
| [Domain-specific criterion] | | | |
| [Domain-specific criterion] | | | |

Overall score: [average]
Ship? [YES if all dimensions >= 4 / NO with top fix to make]
```

### Generator retry prompt template
```
Your previous output scored [N/5] from the evaluator.
Required fixes:
- [fix 1 from evaluator]
- [fix 2 from evaluator]

Previous output:
---
[previous output]
---

Rewrite to address these specific issues. Keep what was correct.
```

---

## Pattern 3: LLM-as-Judge

Use a second LLM call (or a dedicated judge model) to score outputs against a rubric. Produces repeatable, logged, comparable scores — the foundation of an eval suite.

### When to use
- Building an eval suite to run in CI
- Comparing prompt versions (A/B testing prompts)
- Tracking quality over time as the model or prompt changes
- When human review doesn't scale

### Judge prompt structure
```
You are an expert evaluator for [domain]. Your job is to score AI-generated outputs.
Be consistent — identical outputs should receive identical scores.
Do not be influenced by length or confidence of the output.

Task given to the AI:
---
[task/prompt]
---

AI output to evaluate:
---
[output]
---

[Optional: Reference answer / ground truth]
---
[reference]
---

Score on each criterion (1-5):
- **Accuracy**: Is the information factually correct?
- **Relevance**: Does it directly address what was asked?
- **Completeness**: Are all required elements present?
- **[Domain criterion]**: [definition]

Return JSON:
{
  "scores": { "accuracy": N, "relevance": N, "completeness": N },
  "overall": N,
  "pass": true/false,
  "reasoning": "one paragraph",
  "top_issue": "most important fix if failing"
}
```

### Consistency tips for LLM judges
- Set temperature to 0 for the judge — you want determinism
- Use few-shot examples in the judge prompt: show a PASS and a FAIL example with scores
- Test your judge: run the same output through 5 times; scores should be identical at temp=0
- Use a stronger/larger model for the judge than the generator when possible

---

## Pattern 4: Golden Dataset Evals

A **golden dataset** is a curated set of inputs with expected outputs (or expected quality scores). Running your agent against it gives you a pass rate — your key quality metric.

### Building a golden dataset
```
Minimum viable: 20-50 examples
Production target: 100-500 examples
Coverage requirements:
  - Happy path (expected normal inputs): 40%
  - Edge cases (empty, boundary, unusual): 30%
  - Adversarial (malformed, off-topic, injections): 20%
  - Regression cases (past failures): 10%
```

### Golden dataset schema
```json
{
  "id": "tc-001",
  "input": "Summarize this PR description in one sentence: [...]",
  "expected_output": null,
  "expected_criteria": {
    "max_words": 20,
    "must_contain": ["key change"],
    "must_not_contain": ["I", "we"]
  },
  "judge_rubric": "accuracy,completeness",
  "pass_threshold": 4.0,
  "tags": ["summarization", "PR", "happy-path"]
}
```

### Running evals in CI
```yaml
# .github/workflows/evals.yml
name: Agent Evals
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run eval suite
        run: python evals/run_evals.py --dataset evals/golden.jsonl --threshold 0.85
      - name: Comment pass rate on PR
        # Post: "Eval pass rate: 91% (182/200) — baseline: 89% (+2%)"
```

**Gate on pass rate, not individual cases.** A 95% pass rate with known acceptable failures is production-ready. 100% on 5 manual tests is not.

---

## Prototype vs. Production Checklist

Use this before shipping an AI-powered feature:

### Minimum for production
- [ ] Golden dataset exists with ≥ 20 test cases covering happy path + edge cases
- [ ] Eval suite runs automatically (CI or nightly)
- [ ] Pass rate baseline established and documented
- [ ] Prompt changes are compared against baseline before merge
- [ ] Failure modes documented: what does the agent do when it doesn't know?
- [ ] Hallucination risk assessed: is the output verifiable, or taken on faith?
- [ ] Output schema validated (if structured output): JSON schema, type checking
- [ ] Latency measured at p50 and p95 under expected load
- [ ] Cost per call calculated at expected volume

### Signals you're still at prototype quality
- No eval suite exists
- Quality is assessed only through human spot-checks
- You've never tested with adversarial or malformed inputs
- Prompt was written once and never A/B tested
- There's no plan for what happens when the model API changes versions
- You don't know your pass rate — only that "it usually works"

---

## Eval Metrics Reference

| Metric | What it measures | How |
|---|---|---|
| **Pass rate** | % of golden dataset cases that pass | LLM judge or deterministic checker |
| **Exact match** | Output matches expected exactly | String comparison (for structured output) |
| **Semantic similarity** | Meaning matches even if wording differs | Embedding cosine similarity |
| **Rubric score** | Quality on defined dimensions (1-5) | LLM-as-judge |
| **Latency p50/p95** | Speed under load | Timing instrumentation |
| **Cost per call** | Tokens in + out × price | Token counter |
| **Refusal rate** | % of valid inputs the model refuses | Track in logs |
| **Hallucination rate** | % of outputs containing unverifiable claims | LLM judge + factuality rubric |

---

## Connecting to Your CI/CD Pipeline

```
Developer changes prompt or agent code
        ↓
CI runs eval suite against golden dataset
        ↓
   Pass rate ≥ baseline?
   ├── YES → PR can merge
   └── NO  → PR blocked; eval report posted as comment
                    ↓
         Developer sees: which cases failed, why, score delta
                    ↓
              Fix prompt, re-run evals
```

> Pair with the `ci-cd-pipeline-analysis` skill for pipeline setup, and `continuous-delivery` for deployment gates.

---

## References
- Anthropic: [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- OpenAI: [A practical guide to LLM evals](https://cookbook.openai.com/examples/evaluation/getting_started_with_openai_evals)
- LMSYS: [MT-Bench and LLM-as-Judge](https://arxiv.org/abs/2306.05685)
- Hamel Husain: [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
- Eugene Yan: [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)
