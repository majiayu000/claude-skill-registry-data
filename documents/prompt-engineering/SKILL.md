---
name: prompt-engineering
description: Prompt engineering workflow for designing, rewriting, debugging, evaluating, and optimizing LLM prompts, system prompts, developer prompts, few-shot examples, structured-output instructions, tool-use prompts, and prompt eval cases. Use when prompt behavior, reliability, safety, cost, latency, or model fit is the main task. Do not use for generic prose editing, model selection alone, or ordinary documentation work with no prompt artifact.
---

# Prompt Engineering

Treat prompts as small behavioral specs. Improve them by naming the job,
testing the behavior, changing one important thing at a time, and preserving
the prompt's operating context.

## Activity And Authority

- For review, return findings and evidence without rewriting files or changing
  a deployed prompt. A proposed revision may accompany findings when requested.
- For drafting or implementation, change the requested prompt artifact within
  existing authority. Separate local evaluation from deployments, live tool
  actions, sensitive-data use, and metered runs that need additional authority.
- Use the smallest useful output. A short rewrite need not produce a formal
  experiment report; a consequential behavior change needs explicit cases and
  honest evidence.

## Core Workflow

1. **Scope the prompt job.**
   Identify the target model or provider, audience, runtime surface, inputs,
   tools, output contract, constraints, and where the prompt will live. If the
   prompt belongs to a repo, inspect existing prompts, schemas, examples,
   tool definitions, evals, logs, and docs before asking avoidable questions.
2. **Define success before rewriting.**
   State the desired behavior, hard requirements, acceptable variation, known
   failure modes, and evidence that would prove the prompt improved. If success
   is vague, establish representative cases and meaningful failure criteria
   before editing. Preserve baseline cases and explain changed expectations.
3. **Choose the lightest pattern that fits.**
   Use direct instructions for simple tasks, structured sections for context
   control, few-shot examples for format or judgment calibration, schemas for
   machine-readable output, tool-use instructions for action boundaries, and
   repetition only when the model repeatedly drops critical constraints.
4. **Draft with clean boundaries.**
   Put task, context, constraints, examples, tools, and output format in
   separate labeled sections. Delimit user-controlled or retrieved content
   clearly. Keep stable instructions before variable content when prompt
   caching, reuse, or maintainability matters.
5. **Evaluate against reality.**
   Test representative, edge, adversarial, and regression cases. Compare outputs
   against explicit criteria instead of intuition. Record which failures changed
   and which remained. If execution is unavailable, label the assessment as
   static and name the material untested behavior; do not invent run results.
6. **Iterate deliberately.**
   Change one major variable at a time: instruction wording, context ordering,
   examples, output schema, tool contract, reasoning guidance, or model
   settings. Preserve the previous prompt and test cases until the new version
   wins on the target criteria.
7. **Ship the prompt with evidence.**
   Return the final prompt, assumptions, changed behavior, eval cases, expected
   outputs or grading criteria, remaining risks, and any provider-specific
   settings the caller must preserve.

## When To Use

- design, rewrite, debug, or review an LLM prompt
- create or revise a system prompt, developer prompt, tool-use prompt, few-shot
  examples, structured-output instruction, grader prompt, or prompt eval set
- investigate why a prompt is unreliable, unsafe, too costly, too slow, or
  mismatched to a target model
- optimize an existing prompt while preserving behavior and evidence

## Not For

- model selection alone
- generic prose editing, README writing, marketing copy, or voice matching
- ordinary LLM integration code when the prompt behavior is not the main issue
- security review where data exposure, authorization, tenant isolation, or tool
  abuse is the central risk

## Compose With

- When the session provides an OpenAI docs skill or official-doc tool, use it
  for OpenAI-specific current model, API, structured-output, tool-calling,
  reasoning, caching, or pricing behavior; otherwise verify official OpenAI
  docs directly. For other providers, verify current official provider docs
  when those details affect the prompt.
- Add a testing workflow when the main job is test strategy, evidence quality,
  grading design, or acceptance criteria rather than prompt wording.
- Use `security` first when prompt injection, hidden-instruction leakage,
  unsafe tool use, data exposure, or trust boundaries dominate the risk;
  retain this skill for prompt-behavior mechanics.
- **Ownership rule with `context-engineering`:** picking *which* facts, files,
  or examples to load is `context-engineering`; deciding *how to word* the
  prompt, schema, or example is this skill. When work spans both, draft the
  context packet first, then own the prompt artifact here.

## Prompt Design Rules

- Put the user's real task first; do not optimize a prompt before the objective
  and failure mode are clear.
- Prefer explicit success criteria over broad "be better" instructions.
- Separate stable policy from per-request data and untrusted content. When the
  prompt embeds retrieved or user-supplied material, fence it with explicit
  delimiters (e.g. `<<untrusted:source>> ... <</untrusted>>`, matching the
  `context-engineering` convention) and tag fact provenance with
   `[src:code|user|tool|docs|memory|inferred]` when provenance affects judgment.
   These conventions aid inspection; they do not enforce trust or authorization.
   Grade permitted extraction or quotation separately from obeying embedded
   instructions, disclosing protected content, or taking unauthorized actions.
- Specify output shape with examples or schemas when downstream code depends on
  structure.
- Use examples that demonstrate decisions, not examples that merely repeat the
  instruction.
- Include negative and boundary cases when failure would be costly, silent, or
  hard to notice.
- Keep prompts short enough to maintain; move large context to retrieval,
  tools, files, or references when possible.
- Verify current official provider guidance before making model- or API-specific
  claims. Do not rely on memory for rapidly changing model behavior.
- Treat provider guidance as conditional. Load provider notes only when the
  target model, API, or runtime surface makes them relevant.

## Anti-Patterns

Prompts that look polished but fail in practice:

- **Over-explanation:** redundant instructions increase context cost and can
  obscure priorities; verify the effect rather than assuming how a model works.
- **Role stacking:** layering "you are an expert X, careful Y, helpful Z"
  before the task without evidence that the roles improve the target behavior.
- **Examples that contradict instructions:** when a few-shot demo violates a
  rule, the prompt supplies conflicting signals; repair the conflict and test.
- **Repetition without structure:** restating constraints in prose instead of
  putting them in a labeled section or schema.
- **Vague quality bars:** "be helpful", "be thorough", "use best practices"
  without observable criteria.
- **Schema mixed with freeform:** requesting prose outside a JSON-only contract.
  Put explanations in schema fields or a separate supported output channel when
  the consumer needs both.

## Failure Diagnosis

When a prompt fails, classify the failure before rewriting:

- **missing context:** the model did not receive facts it needed
- **ambiguous instruction:** multiple reasonable outputs satisfy the prompt
- **weak output contract:** format, fields, or refusal behavior are underspecified
- **bad examples:** examples teach the wrong pattern or conflict with rules
- **context collision:** retrieved, user, or tool content overrides intent
- **tool boundary drift:** the model calls tools too early, too late, or with bad arguments
- **model mismatch:** the prompt assumes capabilities, settings, or reasoning behavior the model does not provide
- **evaluation gap:** the prompt looks better on anecdotes but fails representative cases

## Output Shapes

Omit `Original Prompt Or Version` and `Run Metadata` for tiny rewrites when
they are unavailable or not material.

For a prompt rewrite:

```markdown
## Original Prompt Or Version
...

## Final Prompt
...

## What Changed
...

## Eval Cases
...

## Run Metadata
...

## Assumptions And Risks
...
```

For prompt debugging:

```markdown
## Diagnosis
Failure category and evidence.

## Original Prompt Or Version
...

## Revision
Changed prompt section or full prompt.

## Validation
Cases that should pass, fail, or remain uncertain.

## Run Metadata
...
```

## Reference Map

- [patterns-and-provider-notes.md](references/patterns-and-provider-notes.md) -
  prompt patterns, primary references, and provider-specific notes.
- [evaluation-flywheel.md](references/evaluation-flywheel.md) - lightweight
  prompt eval design, iteration, and grading workflow.
- [trigger-evals.md](references/trigger-evals.md) - positive and negative
  trigger checks for this skill.
