---
name: prompt-engineering
description: Use when helping user write an LLM prompt. Cover structure, examples, output format, anti-patterns.
---

# Prompt Engineering — Write Prompts That Work

When the user asks you to help write or improve a prompt for an LLM, work from a structure. Don't just "polish" — diagnose what's missing and add it.

## Iron Law

**Test a prompt with at least 3 different inputs before declaring it done.** A prompt that works on one example is not a prompt; it's a coincidence. If you can't run the prompt, at least walk through it mentally with 3 inputs and predict the output.

## Anatomy of a Working Prompt

A good prompt has these elements, in roughly this order:

1. **Role / context** — who is the model acting as? What's the situation?
2. **Task** — what specifically should it do? One sentence.
3. **Constraints** — must / must-not. Brief, explicit.
4. **Examples** (few-shot) — 1-3 input → output pairs. Diverse.
5. **Output format** — concrete structure (XML / JSON / markdown / labeled sections).
6. **Evaluation criteria** (optional) — how to judge a good response.

Not every prompt needs all six. But missing more than two usually breaks it.

## Few-Shot vs Zero-Shot

- Zero-shot works for simple, well-known tasks ("translate this to French").
- Few-shot beats zero-shot for: domain-specific formats, unusual output structures, edge cases the model would otherwise miss.
- **3 examples is the sweet spot.** 1 example is risky (looks like an instance, not a pattern). 5+ has diminishing returns and bloats the prompt.
- Make examples **diverse**: different lengths, different edge cases, including one tricky case.

## Output Format — Be Concrete

Vague: "format the output nicely"
Better: "respond in markdown with H2 sections: Summary, Steps, Risks"
Better still:

```
<response>
  <summary>...</summary>
  <steps>
    <step>...</step>
  </steps>
  <risks>...</risks>
</response>
```

XML tags are easy for downstream parsing and the model follows them reliably. JSON works too but watch for trailing commas / unescaped quotes in the content.

## Modern Models — Skip Outdated Advice

- **"Think step by step"** — Opus/Sonnet 4.x do this internally already. Don't waste tokens. If you need explicit reasoning, use extended thinking (`thinking: {type: 'enabled'}`).
- **"You are a world-class expert"** — at best neutral, at worst sycophancy bait. Skip.
- **All-caps "VERY IMPORTANT" emphasis** — works less than you'd think and clutters. Use structure instead (section headers, lists).

## System vs User Message

- **System message**: role, persistent constraints, output format, examples. Things that don't change request-to-request.
- **User message**: the actual task / input for this call. Variable.

Anthropic models follow this split well. Putting everything in user message works but loses cache-ability (see `[[using-claude-api]]`).

## Long Prompts — Beginning and End Matter Most

The middle of a long prompt is most likely to be dropped or ignored. Place critical instructions:

- **Top**: role, task statement, output format
- **Bottom**: a brief reminder of constraints, the actual user input

Example structure:

```
[role + task at top]
[examples in the middle]
[REMINDER: must output XML. user input below:]
[user input]
```

## Negative + Positive

"Don't be verbose" → vague.
"Don't be verbose. Instead, keep responses under 200 words and use bullet points." → actionable.

Always pair "don't do X" with "instead do Y". Pure negatives leave the model guessing.

## Variables and Templating

When users have a templatable prompt:

```
<role>You are a {language} code reviewer.</role>
<input>{code_to_review}</input>
```

- Use `{}` or `{{}}` placeholders consistently
- Document what each variable should contain
- Note any escaping requirements (e.g., if input may contain `{`)

## Red Flags

- User pastes "make this better" with no context. Ask: better for what? Which model? What's failing?
- The prompt has no output format → outputs will drift across calls.
- Prompt is one giant paragraph. No structure means no reliability.
- Emotional appeals: "this is VERY IMPORTANT", "please be careful", "I'll tip you $200". Pure noise on modern models.
- Examples are all the same shape — model will overfit to that shape.
- "Don't hallucinate" — non-actionable, model already tries not to. Better: "if you don't know, say 'I don't know' instead of guessing."
- Prompt instructs different behavior in two places, contradicting itself.

## Not For

- User already has a working prompt and just wants you to **run it**. Just run it. Don't over-optimize.
- User is asking Claude (right now) a question — they're not writing a prompt for an LLM, they're talking to one. Don't apply this skill to their actual chat input.

## Examples

### Bad prompt user brings you

> "Write a tweet about AI"

Diagnosis: no role, no audience, no constraints, no format, no examples.

### Improved

```
<role>You write tweets for a B2B SaaS account targeting engineering leaders.</role>

<task>Write 3 tweet variants about {topic}.</task>

<constraints>
- 280 chars max each
- One concrete claim, not vague hype
- No hashtags
- No emoji
</constraints>

<examples>
Topic: "Postgres > MongoDB for most startups"
Output:
1. Most startups don't need a document DB. They need joins, transactions, and someone to call at 2am. Postgres has all three.
2. ...
3. ...
</examples>

<output_format>
Plain numbered list 1-3. No preamble.
</output_format>

Topic: {topic}
```

Now testable: try `{topic}` = "vector databases", "rate limiting", "code review" — outputs should all match the format and tone.

## Verification Step

Before handing the prompt back to the user, walk through it with 3 mental inputs:

1. A typical input
2. An edge case (very short / very long / unusual content)
3. A potentially adversarial input

If you can predict reasonable outputs for all three, ship it. If one breaks, fix the prompt.

## See Also

- `[[using-claude-api]]` — implementation: caching, models, tools.
- `[[verification-before-completion]]` — generally: don't claim done without testing.
