---
name: gpt5-prompt-architect
description: Improve existing prompts and draft new prompts or system instructions for GPT-5 and other advanced models (XML sandwich, perfection loop, router nudge, self-reflection). Use when asked to improve, optimize, refine or write a prompt or system instruction.
---

# GPT-5 Prompt Architect

Prompt engineering for GPT-5 and advanced models, based on official OpenAI documentation and research.

## Routing

1. Improve an existing prompt or system instruction: Prompt Improvement Workflow below.
2. Create a new prompt or system instruction: Prompt Creation Workflow below.
3. Apply a specific technique: `references/core-techniques.md` (router nudge, verbosity, XML, perfection loop, meta-prompting) or `references/gpt5-advanced-techniques.md` (API features, agentic calibration, self-reflection, ReAct, tree-of-thought, structured tags).
4. Review patterns and anti-patterns: `references/prompt-patterns.md` (templates, anti-patterns, quality checklist).
5. Skeletons (new prompt, flipped interaction, system instruction): `references/prompt-skeletons.md`.

## Prompt improvement workflow

When the user provides an existing prompt:

1. **Analyze** against: task clarity, context completeness, success criteria, output format, contradictions, anti-patterns (`references/prompt-patterns.md`).
2. **Select techniques.**
   - Always: XML structure for multi-part prompts, explicit output format, no contradictions.
   - Complex tasks: router nudge ("think carefully"), self-reflection rubric, verbosity control.
   - Specialized domains: persona, few-shot examples, domain constraints.
   - GPT-5 API: reasoning effort, custom tools, preambles (`references/gpt5-advanced-techniques.md`).
3. **Apply** systematically: XML structure, persona, examples, self-reflection, router nudge, verbosity.
4. **Present**: the improved prompt (complete, ready to use), the changes made, a brief rationale per technique, optional API parameters.

## Prompt creation workflow

When the user requests a new prompt:

1. **Gather requirements**: task objective, target model (GPT-5, Claude, agnostic), input/output, constraints (length, format, style), success criteria. If unclear, use the flipped interaction pattern (ask 5 clarifying questions first, see `references/prompt-skeletons.md`).
2. **Select a template** from `references/prompt-patterns.md`: research and analysis, code generation, creative content.
3. **Select techniques** from `references/core-techniques.md`. Essential: XML sandwich, verbosity control, output format. Enhancement: router nudge, perfection loop, meta-prompting. GPT-5 specific: `references/gpt5-advanced-techniques.md`.
4. **Build the prompt** from the skeleton in `references/prompt-skeletons.md`: persona, `<context>`, `<task>`, `<rules>`, `<examples>`, `<self_reflection>`, `<output_format>`, router nudge.
5. **Present**: the complete prompt, techniques used, usage notes, optional API parameters.

## System instructions

For custom GPTs or Claude Projects, add: assistant identity, behavior rules (ALWAYS and NEVER), interaction patterns, output standards, edge cases, tool usage. Skeleton: `references/prompt-skeletons.md`. Technique background: "Agentic Workflow Calibration" and "Structured XML-Style Tags" in `references/gpt5-advanced-techniques.md`.

## Quick reference

Most impactful (Pareto): XML structure, self-reflection rubric, examples, router nudge, clear output format.

Common improvements:
- Vague to specific: add concrete details and constraints
- Contradictory to hierarchical: prioritize conflicting rules
- Assumed context to explicit: provide all necessary information
- Overloaded to decomposed: split into multiple prompts
- Format-ambiguous to structured: specify the exact format

## Best practices

1. Start simple, add complexity only when the task needs it
2. Explain one technique at a time, combine techniques for effect
3. Balance detail against token efficiency
4. Use model-specific API parameters when available
5. Show before and after for improvements
6. Encourage testing and iteration

## Anti-patterns

Never: add techniques that do not serve the task, create contradictory instructions, assume context not provided, over-complicate simple tasks, forget the output format, skip success criteria.
