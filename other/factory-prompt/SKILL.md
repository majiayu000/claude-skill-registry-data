---
name: factory-prompt
description: Convert a rough ask into a structured XML-tagged prompt using the factory-prompting vocabulary
argument-hint: <rough ask — the messy one-liner or paragraph you want structured>
---

You're rewriting a rough ask into a structured prompt. The goal is a ready-to-paste prompt that uses the canonical XML tag vocabulary from `factory-prompting.md`, with nothing decorative and nothing missing.

**Invocation input:** the rough ask. It may be a one-liner, a paragraph, or include literal input material. If empty, ask the user for it and stop.

## What to do

1. **Load the vocabulary.** Load the canonical `factory-prompting` skill through the host's skill capability if it is not already active. The canonical tag set is: `<role>`, `<instructions>`, `<context>`, `<input>`, `<examples>`, `<output_format>`, `<constraints>`, `<thinking>`. Do not invent tags outside this set; for multiple inputs, nest descriptive child tags inside `<input>`.

2. **Parse the rough ask.** Identify which canonical roles are actually present:
   - **Instructions** — the verb of the ask ("summarize", "extract", "rewrite", "decide")
   - **Context** — background about *why* or *for whom*, distinct from the material itself
   - **Input** — literal material to operate on (notes, email, code, query). If multiple, plan child tags
   - **Output format** — shape constraints (length, schema, bullets, tone)
   - **Constraints** — hard rules (must-include, must-exclude, length caps)
   - **Examples** — only if the user provided demonstrations
   - **Role** — only if the rough ask explicitly invokes a persona
   - **Thinking** — only if the task has hidden criteria the model should expose

3. **Apply the minimum-tagging rule.** Skip any tag whose content would be empty or trivially derivable. A one-line ask with no input, no constraints, and no shape needs no tags — say so and return the prose. Tags exist to disambiguate; if there's nothing to disambiguate, don't add them.

4. **Decide literal vs template form.**
   - If the rough ask contains concrete material (real notes, real code, a real question), produce the **literal** form with that material inline.
   - If the rough ask describes a *kind* of prompt for reuse ("a prompt to summarize any meeting notes"), produce the **template** form with `{{snake_case_variable}}` placeholders.
   - If ambiguous, default to literal and offer to re-emit as a template.

5. **Order the tags canonically.** `<role>` → `<instructions>` → `<context>` → `<input>` → `<examples>` → `<output_format>` → `<constraints>` → `<thinking>`. Deviate only if the input is very long, in which case place `<instructions>` last and say why.

6. **Emit the prompt.** Put it in a single fenced code block, no preamble, ready to copy. Indentation: two spaces inside nested tags.

7. **One-line rationale.** After the code block, a single line of the form:
   ```
   Tags: <list>. Skipped: <list, if any>, because <one reason>.
   ```
   This is the learning aid — it shows which roles you saw in the ask and which you deliberately left out. Keep it to one line; no further commentary.

8. **No narration.** Don't explain what you're about to do, don't summarize the rough ask back, don't close with "let me know if you'd like changes." The code block plus the one-line rationale is the entire response.

## Example

**User:**
```
/prompt Summarize meeting notes from a Q3 vendor sync. Professional tone, bullets, 150 words max, bold the deadlines. Notes: vendor will ship API update by Aug 15, John asked for beta by Aug 1, pricing proposal due next Tuesday.
```

**Output:**

````
```xml
<instructions>
Summarize the meeting notes below. Focus on actionable items. Keep the tone professional.
</instructions>

<context>
The meeting was a Q3 sync with our primary software vendor.
</context>

<input>
<notes>
Vendor will ship the API update by August 15.
John asked if we could get beta access by August 1.
Vendor agreed to send a pricing proposal by next Tuesday.
</notes>
</input>

<output_format>
- Bullet points
- Maximum 150 words
- Bold all deadlines
</output_format>
```

Tags: instructions, context, input, output_format. Skipped: examples, constraints, role, thinking, because nothing in the ask warranted them.
````

## Style

Follow `factory-voice.md`. The output is a ready-to-paste artifact, not a conversation — that's why there's no preamble and no trailing pleasantries. The one-line rationale exists so the user learns the vocabulary by seeing which tags you picked and which you left out, not so you can show your work. If the rough ask is too thin to structure usefully (one short sentence, no input, no constraints), say so in one line and return the prose unchanged — refuse to decorate.
