---
name: managing-prompts
description: Creates, analyzes, updates, and optimizes prompts using Claude 4.5 best practices, guardrails, context management, and prompt engineering patterns. Use when user asks how to write effective prompts, explaining prompt engineering techniques, understanding Claude 4.5 best practices, describing prompt patterns and structures, creating new prompts, evaluating existing prompts for improvements, determining if current logic should be extracted to prompts, identifying outdated prompt techniques, optimizing context usage, implementing guardrails, or when user mentions "prompt engineering", "hallucinations", "context optimization", "prompt caching", "chain-of-thought", or asks if logic should become a prompt.
---

# Managing Prompts

Comprehensive prompt engineering for Claude 4.5: creation, analysis, optimization, guardrails, context management.

## When to Use

- User requests creating/analyzing/optimizing prompts
- User asks if current logic should be extracted to prompt
- User mentions: hallucinations, consistency issues, context optimization, prompt caching, chain-of-thought, XML tags
- Context usage high and extraction would help
- Outdated prompt techniques need Claude 4.5 updates

## Core Workflows

### Workflow 1: Analyzing Existing Prompts

**Quick process:**
1. Read prompt file/content
2. Load quick-reference.md for validation checklist
3. Apply evaluation: structure, techniques, guardrails, context efficiency, Claude 4.5 optimization
4. Categorize issues: critical | major | minor
5. Generate recommendations with priority
6. Output using output-formats.md#analysis-report template

**Detailed evaluation:** Load analysis-patterns.md

**Common issues reference:** quick-reference.md#common-issues

---

### Workflow 2: Creating New Prompts

**Quick process:**
1. **Gather requirements:** objective, success criteria, inputs/outputs, complexity, risk factors
2. **Select architecture:** Load architecture-patterns.md, choose: simple_task | complex_reasoning | agent_workflow | multi_window
3. **Apply techniques:** Load technique-reference.md for indexed lookup by need
4. **Add guardrails:** Based on risk level, load guardrails-implementation.md for patterns
5. **Optimize context:** Load context-optimization.md if >10K tokens
6. **Validate:** Use quick-reference.md#quick-validation-checklist

**Technique order:**
1. Clear instructions (explicit, contextual motivation, success criteria, output format)
2. Examples (3-5 for complex tasks)
3. Chain-of-thought (for reasoning tasks)
4. XML tags (for structure)
5. Role assignment, prefilling, template variables

**Architecture selection:**
- Simple task: Clear objective, straightforward
- Complex reasoning: Multi-step analysis, judgment
- Agent workflow: Tool access, iterative, autonomous
- Multi-window: >100K tokens, extended work

**Guardrails by risk:**
- Low: Basic uncertainty permission
- Medium: Examples + format spec
- High: Quote-grounding + citations
- Critical: Full stack (quotes, citations, knowledge restriction, CoT)

**Context optimization:**
- Cache static content ≥1024 tokens
- Place 20K+ docs at beginning
- Remove Claude's existing knowledge
- Quote-grounding for large docs
- Split if >3 distinct subtasks

---

### Workflow 3: Optimizing Existing Prompts

**Quick process:**
1. Identify goal: reduce_tokens | improve_quality | increase_consistency | reduce_hallucinations | enable_caching | split_prompt
2. Load optimization-strategies.md for before/after examples
3. Apply transformation
4. Measure improvement
5. Document using output-formats.md#optimization-report

**Quick optimization strategies:**
- **Context reduction:** Remove redundancy, cache static, quote-grounding, split if >3 subtasks
- **Quality:** Add examples, CoT, explicit instructions, contextual motivation
- **Consistency:** Format spec, prefilling, 3-5 examples
- **Hallucinations:** Uncertainty permission, quote-grounding, citations
- **Caching:** Identify ≥1024 static tokens, restructure, add cache_control

**Decision aids:** quick-reference.md#fast-decision-trees

---

### Workflow 4: Updating Outdated Prompts

**Quick process:**
1. Load migration-guide.md for Claude 3→4.5 patterns
2. Identify outdated: insufficient explicitness, missing motivation, suggestion framing, no summary requests
3. Apply updates preserving core logic
4. Test and document

**Common migrations:**
- Vague → Explicit instructions with specifics
- No motivation → Add contextual reasoning
- Suggestion framing → Action framing ("Improve this" not "Can you improve?")
- No summaries → Explicit requests (4.5 less verbose by default)
- No quality modifiers → Add "Give it your all" for creative tasks

---

### Workflow 5: Deciding Logic Extraction

**Quick process:**
1. Load extraction-decision-guide.md#decision-tree
2. Evaluate criteria (6 for prompt, 6 for script)
3. Score: 3+ = extract, <3 = keep inline
4. Output using output-formats.md#extraction-decision template

**Prompt extraction criteria (3+ to extract):**
- Reused across 3+ contexts
- Needs prompt techniques (examples, CoT, XML)
- Benefits from guardrails
- Context optimization beneficial
- Standardization needed
- Complex (>200 tokens instructions)

**Script extraction criteria (3+ to extract):**
- Deterministic/algorithmic
- Computation-heavy
- Unit testable
- Reused across prompts
- No reasoning required
- Format conversion/validation

**Keep inline:** One-time, context-specific, simple, requires real-time interaction

## Fast Reference System

**For validation:** quick-reference.md (quick checklist, common issues, decision trees, severity guide)

**For technique lookup:** technique-reference.md (indexed by use case, lookup table, application patterns, combinations)

**For output templates:** output-formats.md (analysis, optimization, extraction, creation, migration reports)

**For detailed patterns:**
- extended-thinking-implementation.md (internal reasoning, budget management, batch processing, multi-round strategies)
- prompt-chaining-architecture.md (sequential/parallel workflows, handoff patterns, orchestration, self-correction loops)
- consistency-techniques.md (prefilling, Structured Outputs, format enforcement, advanced patterns)
- claude-4-5-optimization.md (4.5-specific guidance: explicit instructions, context awareness, multi-context workflows, tool usage)
- architecture-patterns.md (5 pattern types: simple task, complex reasoning, agent, multi-window, multi-context workflows)
- guardrails-implementation.md (hallucination, consistency, security, character patterns, jailbreak prevention, prompt leak reduction)
- context-optimization.md (token management, caching with model-specific minimums, document org, splitting, cache invalidation patterns)
- optimization-strategies.md (11 before/after examples)
- migration-guide.md (Claude 3→4.5 patterns, 10 migration examples)
- extraction-decision-guide.md (decision trees, criteria, examples)
- analysis-patterns.md (common issues, quality assessment, evaluation examples)

## Claude 4.5 Critical Behaviors

**Strengths:** Long-horizon reasoning, context awareness, parallel execution, subagent delegation

**Requirements:** More explicit than Claude 3, contextual motivation, high-quality examples, action framing, explicit summary requests, quality modifiers

**Optimization:** Parallel tool guidance, clear success criteria, investigation before answering, aesthetic direction (UI), algorithm approach (code)

## Quick Troubleshooting

Load quick-reference.md for detailed troubleshooting with fixes.

**Common symptoms → Quick fixes:**
- Inconsistent outputs → Format spec + 3-5 examples
- Hallucinations → Quote-grounding + uncertainty permission
- High tokens → Cache static content, remove redundancy
- Too concise (4.5) → Explicit detail requests
- Suggests not implements (4.5) → Action framing
- Stops early (4.5) → Reference token budget available

## Tool Usage Pattern

**Standard workflow:**
1. Identify which workflow (1-5)
2. Load quick-reference.md for checklist/decisions
3. Load technique-reference.md if need technique lookup
4. Load detailed supporting file only when needed
5. Use output-formats.md template for deliverable

**Example - Analysis:**
1. Read prompt
2. quick-reference.md → validation checklist
3. technique-reference.md → identify techniques used
4. analysis-patterns.md → detailed framework (if complex)
5. output-formats.md#analysis-report → generate output

**Example - Creation:**
1. Gather requirements
2. technique-reference.md → select techniques by need
3. architecture-patterns.md → get template for pattern type
4. quick-reference.md → validation before finalizing
5. output-formats.md#creation-summary → document (optional)

**Example - Optimization:**
1. Identify goal
2. quick-reference.md#fast-decision-trees → decide strategy
3. optimization-strategies.md → get before/after pattern
4. Apply and test
5. output-formats.md#optimization-report → document

## Validation Before Deployment

Load quick-reference.md#quick-validation-checklist

**Essential checks:**
- [ ] Objective clear, success criteria defined
- [ ] Instructions explicit (action framing for 4.5)
- [ ] Output format specified
- [ ] Examples if complex (3-5, diverse, identical structure)
- [ ] CoT if reasoning required
- [ ] XML if multiple components
- [ ] Guardrails match risk level
- [ ] Context optimized (caching, placement, splitting)
- [ ] Claude 4.5 specificity (explicit, motivation, quality modifiers)

**Golden test:** "Would colleague understand with minimal context?"

## Summary

This skill provides prompt engineering optimized for Claude 4.5. Use workflows systematically, load references on-demand, validate thoroughly. Supporting files contain detailed patterns - SKILL.md provides navigation and quick process guidance.
