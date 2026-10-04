---
name: kanso-prompting
description: Use when rewriting, sharpening, or producing a prompt for Claude or another current frontier model. Sets standing rules for getting better LLM output through better prompts. Loaded by /kanso-task; not directly invoked by the user.
user-invocable: false
---

# kanso-prompting

Standing rules for prompting current frontier models. These principles apply to any prompt this session produces, including prompts being constructed on the user's behalf.

The single governing principle: **a prompt earns its length the same way code does**. Every clause must do work. Specificity beats verbosity; clarity beats cleverness; structure beats hope.

## The prompting taxonomy

### 1. Lead with the desired outcome

State what the model should produce, in what shape, for what audience, before any context. Don't bury the ask under preamble.

Bad: `I've been working on this codebase for a while and I noticed that the auth module has some issues, particularly around session handling, and I was wondering if maybe you could take a look...`

Good: `Audit src/auth/session.ts for race conditions in session creation. Report findings as a numbered list with file:line references.`

### 2. Explain the *why*, not just the *what*

Reasons let the model generalise correctly to cases you didn't spell out. Without the why, it follows the letter and misses the spirit.

Bad: `Never use ellipses.`

Good: `Never use ellipses — the output will be read aloud by a TTS engine that can't pronounce them.`

### 3. State what to do, not what to avoid

Negative-only instructions trigger the behaviour they warn against and leave a vacuum where positive guidance should be. Replace every "don't" with a "do".

Bad: `Don't use markdown.`

Good: `Write in flowing prose paragraphs.`

### 4. Front-load the full task in turn one

For coding and agentic work, ambiguous first turns produce worse results than a single dense first turn. Specify task, scope, constraints, and definition of done upfront. Don't rely on follow-up turns to recover.

### 5. Show, don't tell — examples beat description

Two or three concrete examples steer the model more than a paragraph of instruction. Use diverse examples that cover edge cases, not three rewrites of the same shape.

### 6. Structure complex prompts with tags

When a prompt mixes instructions, context, examples, and input, wrap each in tags: `<instructions>`, `<context>`, `<examples>`, `<input>`. Cuts the misinterpretation rate on anything non-trivial.

### 7. Long context: documents first, question last

Put large reference material at the top of the prompt; put the actual question at the bottom. Wrap each document in `<document>` with `<source>` and `<document_content>` subtags. Measured uplift on long-context retrieval.

For analysis over long documents, ask the model to extract grounded quotes before reasoning: `First extract relevant passages into <quotes>, then answer using only what's there.`

### 8. Match the prompt's voice to the desired output

Markdown-dense prompts produce markdown-dense replies. Plain-prose prompts produce plain-prose replies. Terse prompts produce terse replies. The prompt is a tone sample whether you intend it or not.

### 9. Ask for action when you want action

`Suggest changes` produces suggestions. `Make these edits` produces edits. `Review this and recommend` produces a memo. The verb sets the artefact.

### 10. Build in self-checks for high-stakes output

`Before finishing, verify each step against the constraints in <criteria>` catches a meaningful fraction of errors in code and reasoning tasks. Cheaper than a second prompt.

### 11. Chain rather than ask for the moon in one shot

Draft → critique against criteria → refine. Three small prompts beat one large one whenever the steps are inspectable. Use single-shot only when the task is genuinely indivisible.

### 12. Use the system prompt to set role and stance

Even one sentence (`You are a senior reviewer who flags only blocking issues`) sharpens tone, scope, and what gets surfaced. Don't waste it on filler.

## Current frontier models — what to assume

Prompt scaffolding written for older model generations now degrades output rather than improving it. Assume the following of any current frontier model:

- **Instruction following is literal.** The model does not silently generalise an instruction from one item to all similar items. If you want it applied broadly, say so explicitly.
- **Drop the aggressive language.** `CRITICAL`, `YOU MUST`, ALL CAPS, and triple exclamation marks over-trigger and cause worse output, not better. Use normal declarative voice.
- **Drop the anti-laziness scaffolds.** Force-thorough, force-tools, "do not stop until" preambles were workarounds for older models and are now noise.
- **Verbosity self-calibrates.** Short on simple tasks, long on open-ended ones. If you need a specific length, prompt with a positive example rather than a word count.
- **General reasoning instructions beat prescribed step plans.** `Think thoroughly before answering` outperforms a hand-written checklist in most cases. The model's reasoning is often better than what you'd prescribe.
- **Default voice is direct and not validation-forward.** Fewer emoji, less "great question". If you want warmth, ask for it.
- **If reasoning is shallow, raise effort before adding prompt scaffolding.** The effort parameter does more than re-prompting can.

### Perishable facts — checked 2026-07

Everything above is behavioural and ages slowly. The facts below are pinned to specific releases and go stale first — verify against current docs before repeating them:

- Current families: Claude 5 (Fable/Mythos), Opus 4.8, Sonnet 5, Haiku 4.5.
- Assistant-prefill is unavailable on Claude 4.6+ models. Use structured outputs or system-prompt guidance instead.

## Anti-patterns

- Vague one-liners (`make it better`, `clean this up`) with no success criteria.
- Stacking contradictions (`be thorough but concise`, `be creative but conservative`) and leaving the model to pick.
- Negative-only instructions with no positive replacement.
- ALL-CAPS emphasis or `CRITICAL:` flags — degrades on current models.
- Long document pasted *after* the question instead of before it.
- Stale Claude 3-era anti-laziness boilerplate copied forward.
- Asking `can you suggest` when you want edits made.
- Treating clarifying turns as a substitute for a precise first turn in agentic workflows — each clarifying turn costs context and momentum.
- Burying the ask under preamble. The first sentence is the highest-leverage sentence.

## Positive defaults

- Start with the verb. `Audit`, `Refactor`, `Write`, `Explain`.
- Name the artefact. `…as a numbered list`, `…as a single commit message`, `…as a diff`.
- Name the audience. `…for a senior reviewer`, `…for a new contributor`.
- State the stopping condition. `Stop after the report; do not edit files.`
- Give two examples when shape matters more than description.

## The kanso test for a prompt

Before sending: would another engineer, given only this prompt and no context from your head, produce something close to what you want? If not, the prompt is incomplete. Add the missing piece — don't hope the model fills it.
