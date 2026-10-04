---
name: deep-think-reasoning
description: Structured deep-reasoning workflow inspired by public Gemini Deep Think descriptions and research patterns such as multi-hypothesis search, self-consistency, critique, verification, and reflection. Use when Codex is asked to think through a hard problem, emulate Deep Think, solve complex math/code/research/planning questions, compare competing strategies, or produce a high-confidence answer that needs explicit assumptions, dissent, evidence, and verification.
---

# Deep Think Reasoning

## Operating Principle

Use this skill to reproduce Deep Think-like behavior at the workflow layer, not to claim access to Gemini's private model internals. The public pattern to emulate is: allocate more reasoning time, explore multiple hypotheses in parallel, critique and combine candidates, verify claims with tools or evidence, then synthesize a compact final answer.

For source grounding and design rationale, read `references/source-grounding.md` when explaining why the workflow is shaped this way.

## Mode Selection

Pick the smallest mode that can catch the risk:

| Mode | Use for | Shape |
| --- | --- | --- |
| `quick` | reversible questions, early brainstorming | 2 candidates, 1 critique pass, brief synthesis |
| `standard` | most complex planning, research, code, math, design | 3-5 candidates, rubric review, verification plan |
| `deep` | high-stakes correctness, hard proofs, architecture, research strategy | 4-6 candidates, independent lanes or subagents, tool checks, repair loop |

Before `deep`, state the expected cost/time in one sentence and ask for confirmation if it will require long-running searches, many subagents, or broad file changes.

## Workflow

### 1. Frame The Problem

Create a compact problem frame before solving:

- `question`: the exact problem to answer.
- `success`: what a good answer must achieve.
- `constraints`: hard limits, repo boundaries, assumptions, deadlines, allowed tools.
- `unknowns`: facts that require lookup, experiments, tests, or user confirmation.
- `failure modes`: what would make a confident answer wrong.

If the problem is under-specified but a reasonable assumption is safe, proceed and mark the assumption. Ask only when the missing choice changes the answer materially.

### 2. Generate Independent Candidates

Create multiple candidate solution lanes before choosing one. Keep lanes independent until review.

Recommended lane prompts:

- `Direct`: solve with the most straightforward method.
- `Decompose`: break the problem into smaller lemmas, modules, or milestones.
- `Contrarian`: challenge the premise and look for simpler or reversed framing.
- `Search/Tool`: identify what evidence, tests, or code execution can decide the question.
- `Creative`: explore a less obvious but plausible route.
- `Risk`: focus on safety, edge cases, and what can fail.

For substantial tasks, use native subagents when available and worthwhile. Give each lane the same problem frame, but do not include other lanes' answers. If subagents are unavailable or too costly, simulate lanes as separate concise internal passes.

### 3. Critique And Score

Review candidates anonymously or by lane name. Do not reward verbosity. Score or rank using:

- `correctness`: factual, logical, mathematical, or behavioral validity.
- `coverage`: handles constraints, edge cases, and user intent.
- `feasibility`: can be implemented or acted on with available tools.
- `robustness`: survives plausible counterexamples and failures.
- `verification`: includes concrete tests, evidence, or proof obligations.
- `cost`: reasonable time, tokens, complexity, and user burden.

Preserve dissent. A weaker candidate can still contribute a blocker, test, or insight.

### 4. Verify

Use the strongest verification available:

- For current facts, search live sources and prefer official or primary sources.
- For code, inspect the repo, run the smallest relevant tests, and check diffs.
- For math/logic, test boundary cases and restate the proof skeleton.
- For design/planning, identify irreversible decisions, rollback paths, and measurable success criteria.
- For research claims, separate source evidence from interpretation.

If verification is unavailable, say `not verified` and lower confidence.

### 5. Reflect Or Restart

Run at most one targeted repair loop by default:

1. Name the blocker or uncertainty.
2. Patch the best candidate or generate one new candidate aimed at that weakness.
3. Re-check only the changed claim.

Escalate to another loop only when the user requested deep work or the answer is blocked without it.

### 6. Synthesize

Return a concise final answer with this structure:

```markdown
**结论**
<best answer or decision>

**为什么**
- <2-5 key reasons>

**保留的异议/风险**
- <material dissent, blockers, or unknowns>

**验证**
- <what was checked, or what remains unverified>

**下一步**
- <smallest useful action>
```

For simple user-facing answers, compress the sections into natural prose, but keep the decision, evidence, uncertainty, and next action visible.

## Output Rules

- Do not expose long hidden chain-of-thought. Provide a useful rationale, assumptions, checks, and final reasoning summary.
- Do not claim this is Gemini Deep Think. Say it is a workflow-level reproduction inspired by public descriptions.
- Do not claim consensus or verification unless candidates were compared and checks were actually performed.
- If sources, tests, or browser checks were used, cite or summarize them in the final answer.
- Prefer actionable conclusions over theatrical deliberation.
