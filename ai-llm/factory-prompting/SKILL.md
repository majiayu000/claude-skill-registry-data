---
name: factory-prompting
description: Structured prompting with XML tags. A small named vocabulary (`instructions`, `context`, `input`, `output_format`, `examples`, `constraints`, `role`, `thinking`) that turns a prose ask into something the model can parse without ambiguity. Read whenever you're authoring a prompt by hand, designing a prompt template for production, or rewriting a flaky ask. Paired with `/prompt`, which converts a rough ask into the structured form.
---

# Factory prompting

Each section leads with **Principle** (one sentence, model-agnostic), then **Why** (the constraint and the tradeoff), then **Recipe** (the canonical shape), and **Failure mode** when there's one to name. This skill governs how to *author* prompts; it doesn't tell you what to ask for.

## Why tags at all

**Principle.** XML tags are unambiguous delimiters. They tell the model *what role each chunk plays* without relying on prose cues.

**Why.** A bare prompt mixes roles: "Summarize these meeting notes (the meeting was with our vendor about Q3) — bullet points, max 150 words. Notes: …" The model has to infer which sentence is the ask, which is background, which is the material to operate on, and which is the output shape. It usually guesses right; under load, with long inputs, or with conflicting cues, it sometimes guesses wrong. Tags collapse the guess. `<instructions>` is the ask. `<input>` is the material. `<output_format>` is the shape. Each chunk has a labelled role, parseable independently.

The deeper reason: tags are *positional-independent*. You can reorder context and input without rewriting transition prose. Templates compose. Variable substitution stays clean.

**Tradeoff.** Tags add visual noise on short prompts. A one-line ask wrapped in five tags is worse, not better — that's decoration, not structure (see failure modes). Reach for tags when ambiguity is real, not as ritual.

## The vocabulary — small, named by role

**Principle.** A canonical set of ~8 tag names, each mapping to a role that genuinely differs in kind. Reuse the vocabulary across prompts; don't invent new tags per task.

**Why.** The same discipline that keeps a design token system legible (see `factory-design.md`) keeps a prompt template system legible. Ten roles you know cold beats fifty roles you have to read each time. Every prompt in the system should feel like the same product.

**The set.**

| Tag | Role | Use when |
|---|---|---|
| `<instructions>` | The literal ask — what the model should do | Always, unless the ask is the only thing in the prompt |
| `<context>` | Background that informs the task but isn't the material to operate on | The model needs to know *why* or *for whom* |
| `<input>` | The literal material to operate on (notes, email, transcript, code, query) | There's a thing to read/transform/answer |
| `<output_format>` | Shape and constraints of the response | The output needs structure (length, schema, tone, format) |
| `<examples>` (nests `<example>`) | Few-shot demonstrations of input → output | The task is fuzzy and one good example beats a paragraph of description |
| `<constraints>` | Hard rules (length caps, exclusions, must-include, forbidden phrasings) | A rule is binary, not advisory |
| `<role>` | Persona / domain stance | The voice or expertise frame genuinely changes the answer |
| `<thinking>` | Steer explicit reasoning before the answer | You want the model to lay out steps before committing to output |

Anything that doesn't map to one of these probably isn't a new tag — it's a child of `<input>` or a sentence in `<instructions>`.

**Nesting.** Multiple inputs get child tags inside `<input>`, named for what they are:

```xml
<input>
  <transcript>...</transcript>
  <crm_notes>...</crm_notes>
</input>
```

Same for examples:

```xml
<examples>
  <example>
    <input>...</input>
    <output>...</output>
  </example>
  <example>
    <input>...</input>
    <output>...</output>
  </example>
</examples>
```

Child names are descriptive of the artifact; parent names stay in the canonical set.

## The minimum-tagging rule

**Principle.** Only tag chunks whose role would otherwise be ambiguous. If a prompt has nothing to disambiguate, don't tag it.

**Why.** Tags exist to remove ambiguity. A one-line ask ("Translate this to French: Bonjour le monde") has no ambiguity — the input is obvious, the instruction is obvious, there's no context or constraints. Wrapping it in `<instructions>` and `<input>` adds noise without adding clarity. Tags are a tool for the cases where prose breaks down — long inputs, multiple inputs, structured outputs, conflicting cues — not a uniform shell to apply to every ask.

The watch-line: if you find yourself filling `<context></context>` with one short sentence, ask whether that sentence belongs in `<instructions>` instead. Empty or near-empty tags are a sign the template is heavier than the task.

**Recipe.** Reach for tags when at least one of these is true:

- The input is more than a couple lines, or there are multiple inputs
- The output shape is constrained (schema, length, format)
- The model needs background that isn't the input itself
- The prompt is going into production (a template, an agent, a system message) — long-run reuse pays the tagging cost back
- Few-shot examples are part of the prompt

Otherwise: write the prose ask. It's fine.

**Failure mode.** Wrapping every prompt in five tags because "structured prompts are best practice." The tags carry no information; they just add tokens. Decoration, not structure. Delete them.

## Order — instructions, then material, then shape

**Principle.** Canonical order: `<role>` → `<instructions>` → `<context>` → `<input>` → `<examples>` → `<output_format>` → `<constraints>` → `<thinking>`. Deviate only with reason.

**Why.** The order isn't arbitrary. The model reads top-to-bottom; what comes early frames what comes later. Role and instructions first set the lens. Context and input give the material. Examples calibrate. Output format and constraints close with the shape of the answer. `<thinking>` (when present) trails as a behavioural cue for *how* to respond.

There's a known long-context wrinkle: for very long inputs (tens of thousands of tokens), repeating the instructions *after* the input — or placing them last — often improves adherence, because the instruction is closer to the generation step. Anthropic's prompt-engineering guidance calls this out. For normal-length prompts, the canonical order is fine; for long-context tasks, consider putting `<instructions>` last or echoing them.

**Failure mode.** Putting `<output_format>` before `<instructions>` and `<input>`. The model commits to a shape before it knows what the task or material is, and the output skews toward filling the shape rather than answering the ask.

## Variables — single-brace or double-brace, pick one

**Principle.** When a prompt is a template, mark variable slots with a syntax distinct from the tag delimiters. `{{variable}}` is the common choice.

**Why.** Templates get string-substituted before the model sees them. The substitution syntax has to be unambiguous to the templating layer (Python f-string, Jinja, Mustache, a hand-rolled `.replace()`) and visible to the human author. `{{variable}}` works across most renderers and doesn't collide with XML tags. Single braces (`{variable}`) work too but collide with JSON in `<output_format>` or `<examples>`.

**Recipe.**

```xml
<instructions>
Summarize the meeting notes below. Focus on actionable items.
</instructions>

<context>
{{meeting_context}}
</context>

<input>
<notes>
{{meeting_notes}}
</notes>
</input>

<output_format>
- Bullet points
- Max {{max_words}} words
- Bold any deadlines
</output_format>
```

Keep variable names snake_case and descriptive. `{{notes}}` is fine in a one-template world; `{{meeting_notes}}` is better in a template library where collisions matter.

**Failure mode.** Mixing brace styles (`{x}` in one slot, `{{y}}` in another) inside the same template. The renderer silently misses one and the model gets a literal `{x}` in the prompt.

## When to use `<examples>` vs prose description

**Principle.** Use examples when the task shape is hard to describe in prose; use prose when one rule covers the cases.

**Why.** Examples are expensive — they take tokens, take authoring time, and they pin the model toward the demonstrated pattern (which can over-narrow on edge cases the examples don't cover). Use them when the task is irregular: "extract sentiment but only when the speaker is the customer, not the agent," "format these dates the way our finance team writes them, which isn't ISO and isn't US-standard." Prose for the universal rule, examples for the texture.

**Recipe.** Two or three diverse examples beat one or ten. Diversity > volume — show the edges, not the easy middle. Each example should add a distinguishing case the others don't cover.

```xml
<examples>
  <example>
    <input>Customer paid the invoice on March 5.</input>
    <output>{"event": "payment", "date": "2026-03-05"}</output>
  </example>
  <example>
    <input>Follow up next Tuesday about the renewal.</input>
    <output>{"event": "follow_up", "date": null, "relative": "next Tuesday"}</output>
  </example>
</examples>
```

The second example teaches "relative dates go to `relative`, not `date`" — a rule that's faster to demonstrate than to write out.

**Failure mode.** Ten examples that all look the same. The model overfits to a shape it would have inferred from one. Diversity carries the signal.

## `<thinking>` — when explicit reasoning belongs in the prompt

**Principle.** Use `<thinking>` to ask the model to lay out reasoning before answering, when the task benefits from intermediate steps the user doesn't want in the final output.

**Why.** Some tasks improve sharply with chain-of-thought (multi-step math, multi-constraint planning, classification with hidden criteria). The prompt can carve out a `<thinking>` section the model fills before the `<answer>` it returns. Distinct from Claude's extended thinking feature, which is a model-level capability — `<thinking>` in the prompt is a structural cue, useful even when extended thinking isn't on.

**Recipe.**

```xml
<instructions>
Decide which support tier this ticket needs.
First, in <thinking>, list the criteria you're weighing.
Then, in <answer>, output just the tier name.
</instructions>

<input>{{ticket}}</input>
```

The caller can strip `<thinking>` from the response and keep `<answer>`. The reasoning becomes auditable without polluting the output.

**Failure mode.** Asking for `<thinking>` on tasks that don't need it. Adds latency and tokens for no quality gain. Reach for it when the task has hidden criteria or multi-step structure, not as default.

## Failure mode — tag sprawl

The same disease that hits design tokens hits prompt vocabularies. `<background>` next to `<context>`. `<task>` next to `<instructions>`. `<rules>` next to `<constraints>`. `<format>` next to `<output_format>`. Each addition feels precise in the moment; in aggregate they collapse the vocabulary back into noise, and the team (or you-on-a-different-day) can't remember which to reach for.

The discipline: before inventing a new tag, write the rule in English — *what role does this play that the existing set doesn't already name?* If the answer is "it's basically context but a different kind of context," reject and use `<context>`. If the answer names a genuinely new role, add it to this file so the next prompt uses the same name.

## Failure mode — decoration tags

A short, unambiguous ask wrapped in tags it doesn't need:

```xml
<instructions>What's 2 + 2?</instructions>
```

That's not structure; that's ceremony. The prose version is shorter and reads the same to the model. Tags carry weight when they remove real ambiguity (long input, multiple inputs, constrained output). Otherwise: prose.

## Where this applies

- Hand-authored prompts you're about to paste into a Claude / GPT / Gemini chat
- Prompt templates in production code (system messages, agent prompts, RAG prompts)
- The output of the `/prompt` slash command, which rewrites a rough ask into this shape
- `factory-llm-workflows.md` — LangGraph nodes that use structured prompts; tag vocabulary here is what those prompts use

## Related

- `/prompt` — slash command that converts a rough ask into the structured form, using this vocabulary
- `factory-llm-workflows.md` — where production prompts live in the stack
- `factory-voice.md` — the voice you'd use *inside* `<instructions>` when authoring for Claude
- Anthropic prompt-engineering docs — the upstream source for XML-tag conventions and the long-context ordering wrinkle
