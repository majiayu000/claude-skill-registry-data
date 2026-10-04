---
license: Apache-2.0
name: prompt-engineer
description: Expert prompt optimization for LLMs and AI systems. Use PROACTIVELY when building AI features, improving agent performance, or crafting system prompts. Masters prompt patterns and techniques.
allowed-tools: Read,Write,Edit,Glob,Grep,mcp__sequentialthinking__sequentialthinking
metadata:
  category: AI & Machine Learning
  tags:
    - prompt-engineering
    - llm
    - optimization
    - few-shot
    - chain-of-thought
  provenance:
    kind: first-party
    owners:
      - port-daddy
  pairs-with:
    - skill: agentic-app-architecture
      reason: Decides the app's transparency, memory, and execution shape first; this skill fills that shape in with the actual prompt wording once it exists.
    - skill: llm-router
      reason: Router picks the model tier by task complexity; this skill's prompt design (length, few-shot count, reasoning depth) is a primary input to that complexity estimate.
    - skill: output-contract-enforcer
      reason: Runtime-validates that the prompt's declared output contract (schema/format) is actually what the model returns, closing the loop this skill's audit only checks statically.
    - skill: ai-engineer
      reason: The prompt is one component of the larger LLM app that skill architects (RAG, agents, eval harness, guardrails).
  io-contract:
    kind: deliverable
    consumes:
      - kind: task-or-goal
        format: markdown
      - kind: model-target
        format: markdown
      - kind: prompt-spec
        format: json
    produces:
      - kind: engineered-prompt
        format: markdown
      - kind: rationale
        format: markdown
      - kind: prompt-audit
        format: json
---
# Prompt Engineer

Expert in crafting, optimizing, and debugging prompts for large language models. Transform vague requirements into precise, effective prompts that produce consistent, high-quality outputs.

## Quick Start

```
User: "My chatbot gives inconsistent answers about our refund policy"

Prompt Engineer:
1. Analyze current prompt structure
2. Identify ambiguity and edge cases
3. Apply constraint engineering
4. Add few-shot examples
5. Test with adversarial inputs
6. Measure improvement
```

**Result**: 40-60% improvement in response consistency

## Core Competencies

### 1. Prompt Architecture
- System prompt design for persona and constraints
- User prompt structure for clarity
- Context window optimization
- Multi-turn conversation design

### 2. Optimization Techniques
| Technique | When to Use | Expected Improvement |
|-----------|-------------|---------------------|
| **Chain-of-Thought** | Complex reasoning | 20-40% accuracy |
| **Few-Shot Examples** | Format consistency | 30-50% reliability |
| **Constraint Engineering** | Edge case handling | 50%+ consistency |
| **Role Prompting** | Domain expertise | 15-25% quality |
| **Self-Consistency** | Critical decisions | 10-20% accuracy |

### 3. Debugging & Testing
- Prompt ablation studies
- Adversarial input testing
- A/B testing frameworks
- Regression detection

## Prompt Patterns

### The CLEAR Framework

```
C - Context: What background does the model need?
L - Limits: What constraints apply?
E - Examples: What does good output look like?
A - Action: What specific task to perform?
R - Review: How to verify correctness?
```

### System Prompt Template

```markdown
You are [ROLE] with expertise in [DOMAIN].

## Your Task
[CLEAR, SPECIFIC INSTRUCTION]

## Constraints
- [CONSTRAINT 1]
- [CONSTRAINT 2]

## Output Format
[EXACT FORMAT SPECIFICATION]

## Examples
Input: [EXAMPLE INPUT]
Output: [EXAMPLE OUTPUT]
```

### Chain-of-Thought Pattern

```markdown
Think through this step-by-step:

1. First, identify [ASPECT 1]
2. Then, analyze [ASPECT 2]
3. Consider [EDGE CASES]
4. Finally, synthesize into [OUTPUT]

Show your reasoning before the final answer.
```

## Optimization Workflow

| Phase | Activities | Tools |
|-------|------------|-------|
| **Analyze** | Review current prompts, identify issues | Read, pattern analysis |
| **Hypothesize** | Form improvement hypotheses | Sequential thinking |
| **Implement** | Apply prompt engineering techniques | Write, Edit |
| **Test** | Validate with diverse inputs | Manual testing |
| **Measure** | Quantify improvement | A/B comparison |
| **Iterate** | Refine based on results | Repeat cycle |

## Common Issues & Fixes

### Issue: Hallucinations
```
Problem: Model fabricates information
Fix: Add "Only use information provided. Say 'I don't know' if uncertain."
```

### Issue: Verbose Output
```
Problem: Model produces too much text
Fix: Add "Be concise. Maximum 3 sentences." + format constraints
```

### Issue: Format Violations
```
Problem: Output doesn't match required format
Fix: Add explicit examples + "Follow this exact format:"
```

### Issue: Context Confusion
```
Problem: Model loses track in long conversations
Fix: Add periodic context summaries + clear role reminders
```

## Output Contract

An engineered prompt this skill hands off carries:

- `engineeredPrompt`: the finished system/user prompt text (markdown), applying the CLEAR framework and the relevant techniques from the Optimization Techniques table.
- `rationale`: markdown explaining which techniques were applied and why — which constraint(s) were prioritized, why a technique was skipped, what ablation/adversarial testing found.
- `promptSpec`: a structured JSON description of the prompt's own properties (see `schemas/prompt-spec.schema.json`) — role, output contract, few-shot count, guardrails, eval criteria, input-delimiting, and edge-case behavior. This is what `scripts/prompt_audit.mjs` audits.

Run `node scripts/prompt_audit.mjs --input <prompt-spec>.json` to get a deterministic `{ pass, score, findings, recommendations }` audit of a prompt's structural properties before shipping it. The scorer never reads prompt prose or does keyword matching — it scores the structured booleans/counts an engineer has already decided during Analyze/Implement, the same decisions `references/eval-criteria-patterns.md` and `references/injection-and-safety.md` walk through making.

## Anti-Patterns

### Anti-Pattern: Prompt Stuffing (Kitchen-Sink Overload)

**Novice**: Crams every possible instruction, edge case, and constraint into one system prompt "to be safe."
**Expert**: Prioritizes 3-5 key constraints and uses progressive disclosure (references, follow-up turns, retrieval) for the rest — an overloaded prompt dilutes the instructions that actually matter and the model can no longer tell what to prioritize.
**Detection**: `prompt_audit.mjs` returns a critical `kitchen-sink-overload` finding when `avoidsKitchenSink` is `false`.

### Anti-Pattern: Vague Instructions / No Role Grounding

**Novice**: "Write something good about our product" — no persona, no measurable criteria, no stated domain expertise for the model to inhabit.
**Expert**: States a specific role ("You are a senior support engineer who has resolved 10,000 refund tickets...") plus specific, testable requirements and examples.
**Detection**: `prompt_audit.mjs` returns a medium `no-clear-role` finding when `hasClearRole` is `false`.

### Anti-Pattern: Over-Constraining

**Novice**: 50+ rules the model must simultaneously satisfy, many of them contradictory once you look closely.
**Expert**: Essential constraints only — test each one for necessity before shipping it. This is the same overload failure as Prompt Stuffing, arrived at from the other direction (too many rules instead of too many topics).
**Detection**: Caught by the same `kitchen-sink-overload` finding (`avoidsKitchenSink: false`) — the scorer treats topic-overload and rule-overload as one failure mode: the model can't prioritize.

### Anti-Pattern: No Examples

**Novice**: A complex output format described entirely in prose, with zero example input/output pairs.
**Expert**: Always include 2-3 representative examples — a model infers a format far more reliably from examples than from a prose description alone.
**Detection**: `prompt_audit.mjs` returns an `insufficient-few-shot-examples` finding (medium when `fewShotExamples` is 0, low when it is exactly 1) whenever `fewShotExamples < 2`.

### Anti-Pattern: No Explicit Output Contract

**Novice**: Ships a prompt that describes the task but never states the required output shape, so the model free-forms JSON, prose, or markdown inconsistently across calls.
**Expert**: States the exact output contract (schema, structure, delimiters) in the prompt itself, and validates it downstream (pairs with `output-contract-enforcer`).
**Detection**: `prompt_audit.mjs` returns a critical `missing-output-contract` finding when `hasExplicitOutputContract` is `false`, and a high `output-format-unspecified` finding when `outputFormatSpecified` is `false`.

### Anti-Pattern: Undelimited Untrusted Input (Injection Risk)

**Novice**: Interpolates user-supplied or retrieved (RAG) text directly into the instruction stream with no delimiter, so a crafted input can be read as a new instruction ("ignore previous instructions...").
**Expert**: Wraps every untrusted/user-supplied span in an explicit delimiter (XML tags, a fenced block, a named variable) and instructs the model to treat that span as data, never as instructions. See `references/injection-and-safety.md`.
**Detection**: `prompt_audit.mjs` returns a critical `untrusted-input-not-delimited` finding when `delimitsUntrustedInput` is `false` — this fails closed: an unset or missing field is scored as undelimited, never assumed safe.

### Anti-Pattern: No Eval Criteria

**Novice**: Ships a prompt and finds out whether it "works" only from vibes or a single manual spot-check.
**Expert**: Defines eval criteria before shipping — a rubric, a set of golden input/output pairs, or an LLM-judge prompt — so a regression is detectable, not just felt. See `references/eval-criteria-patterns.md`.
**Detection**: `prompt_audit.mjs` returns a critical `no-eval-criteria` finding when `hasEvalCriteria` is `false`.

### Anti-Pattern: No Refusal / Edge-Case Behavior

**Novice**: The prompt only covers the happy path; when the model hits something out of scope, adversarial, or ambiguous, behavior is undefined.
**Expert**: Explicitly specifies what to do at the edges — refuse, ask a clarifying question, or degrade gracefully — as part of the prompt itself, not left as an emergent property.
**Detection**: `prompt_audit.mjs` returns a critical `no-refusal-behavior` finding when `specifiesRefusalBehavior` is `false`.

### Anti-Pattern: No Guardrails

**Novice**: No hallucination guard, no scope boundary, no "only use information provided" instruction — the model is free to fabricate.
**Expert**: Adds explicit guardrails appropriate to the task's risk level (see Common Issues & Fixes above for the canonical hallucination fix).
**Detection**: `prompt_audit.mjs` returns a medium `no-guardrails-present` finding when `guardrailsPresent` is `false`.

## Quality Metrics

| Metric | How to Measure | Target |
|--------|----------------|--------|
| **Consistency** | Same input, same output quality | &gt;90% |
| **Accuracy** | Correct information | &gt;95% |
| **Format Compliance** | Follows specified format | &gt;98% |
| **Latency** | Time to first token | &lt;2s |
| **Token Efficiency** | Output tokens per task | -20% waste |

## When to Use

**Use for:**
- Designing system prompts for chatbots
- Optimizing agent instructions
- Reducing hallucinations
- Improving output consistency
- Creating prompt templates

**Do NOT use for:**
- Building end-to-end LLM applications, RAG pipelines, or agent orchestration — a production-integration concern, not prompt wording
- Automated, self-improving prompt optimization loops — a distinct automation concern; this skill covers deliberate, expert-driven prompt engineering
- General coding tasks (use language-specific skills)
- Infrastructure setup (use deployment skills)

---

**Core insight**: Great prompts are like great specifications — specific enough to eliminate ambiguity, flexible enough to handle variation, and tested against adversarial inputs.

**Pairs with**: `agentic-app-architecture` (app shape before prompt wording) | `llm-router` (prompt complexity informs model-tier choice) | `output-contract-enforcer` (validates the output contract this skill's prompts declare).

## References

| File | Load When |
| --- | --- |
| `references/injection-and-safety.md` | Need to delimit untrusted/user-supplied input, or design refusal/guardrail behavior for adversarial or out-of-scope input. |
| `references/eval-criteria-patterns.md` | Need to define how to tell whether a prompt's output is actually correct — rubrics, golden examples, or an LLM-judge pattern. |
| `examples/expected-output.md` | Need to see a weak prompt spec audited, then the same prompt fixed and passing. |
| `templates/output-template.md` | Need a reusable template for the engineered prompt + rationale + prompt spec handoff. |
| `schemas/prompt-spec.schema.json` | Need to validate a prompt-spec JSON payload's structure before auditing it. |
| `scripts/prompt_audit.mjs` | Need deterministic scoring of a prompt's structural properties. |
| `agents/openai.yaml` | Need a subagent descriptor for delegated prompt engineering. |

<!-- BEGIN BUNDLE INDEX (auto: index_references.py) -->

## Skill Bundle Index

*Every file in this skill, and when to open it. Auto-generated; run `scripts/index_references.py --fix`.*

**root**
- [`CHANGELOG.md`](CHANGELOG.md) — Prompt Engineer — Changelog — - Imported from the global jury_rig skill catalog (SKILL.md only) and upgraded to the port-daddy agentic-family standard.
- [`README.md`](README.md) — Prompt Engineer — Craft, optimize, and debug prompts for large language models: the CLEAR framework, chain-of-thought and few-shot patterns, and a determinist

**`agents/`**
- [`agents/openai.yaml`](agents/openai.yaml) — openai (data/schema)

**`examples/`**
- [`examples/expected-output.md`](examples/expected-output.md) — Example Output: Prompt Engineer — Scenario: an agent writes a first-draft system prompt for a support chatbot that answers refund-policy questions using retrieved ticket hist
- [`examples/sample-input.json`](examples/sample-input.json) — sample input (data/schema)

**`references/`**
- [`references/eval-criteria-patterns.md`](references/eval-criteria-patterns.md) — Defining Eval Criteria for a Prompt — Use this when you need a way to tell whether a prompt change is an improvement or a regression, instead of relying on a single manual read o
- [`references/injection-and-safety.md`](references/injection-and-safety.md) — Delimiting Untrusted Input & Refusal Behavior — Use this when you need to embed user-supplied or retrieved (RAG, tool-output, ticket-history, web-fetch) text inside a prompt, or need to de

**`schemas/`**
- [`schemas/prompt-spec.schema.json`](schemas/prompt-spec.schema.json) — prompt spec.schema (data/schema)

**`scripts/`**
- [`scripts/prompt_audit.mjs`](scripts/prompt_audit.mjs)

**`templates/`**
- [`templates/output-template.md`](templates/output-template.md) — Engineered Prompt Handoff Template — Fill in every section before handing the prompt off.

<!-- END BUNDLE INDEX -->
