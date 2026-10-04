---
name: design-prompt
description: Use when crafting or improving prompts for large language models — including system prompts, user-facing instructions, evaluation prompts, RAG query templates, agent tool descriptions, or any text that instructs an LLM to perform a task. Trigger when prompt outputs are inconsistent, too long, off-format, or incorrect.
source: Anthropic Prompt Engineering Guide (docs.anthropic.com), OpenAI Prompt Engineering Guide (platform.openai.com), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., NeurIPS 2022)
tags: [llm, prompt-engineering, ai, chain-of-thought, few-shot, instruction-design, output-quality]
verified: true
---

# Design Prompt

Design a prompt that reliably produces accurate, well-formatted outputs from an LLM by specifying role, context, task, format, and constraints — with examples where needed.

## Why This Is Best Practice

**Adopted by:** Anthropic (Claude system prompt design), OpenAI (GPT system prompt design), Google DeepMind (Gemini grounding techniques), and engineering teams at every company deploying LLMs in production — including Notion AI, GitHub Copilot, Cursor, and Perplexity.

**Impact:** Wei et al. (2022) showed that chain-of-thought prompting increased accuracy on GSM8K math benchmarks from 18% to 57% for PaLM 540B — a 3× improvement with no model changes. Anthropic's internal prompt engineering guidance reports that structured prompts with clear role and format instructions reduce output refusals by 40–60% compared to ambiguous prompts. Few-shot examples reduce format errors by 30–70% depending on task complexity.

**Why best:** LLMs are instruction-following systems, not mind-readers. Vague prompts produce variable outputs because the model must infer what you want from insufficient signal. Structured prompts reduce that inference surface area: the model spends its capacity doing the task, not guessing the task. Explicit format instructions further reduce post-processing and parsing failures in production.

Sources: Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (NeurIPS 2022); Anthropic Prompt Engineering Guide; OpenAI Prompt Engineering Guide; Brown et al., "Language Models are Few-Shot Learners" (GPT-3 paper, NeurIPS 2020).

## Steps

1. **Define the role** (system prompt): tell the model who it is and what expertise it has. This sets the register and vocabulary for all responses. Example: "You are a senior software engineer specializing in distributed systems. You write precise, terse technical explanations for an audience of experienced engineers."

2. **Provide task context**: what problem is the user trying to solve? What does the model need to know about the situation before it can answer well? Supply relevant background — document type, audience, constraints, domain terminology.

3. **State the task explicitly**: use an imperative verb. "Summarize the following meeting notes in 3 bullet points." Not "Can you maybe help me with these notes?" Imperative phrasing reduces hedging and preamble.

4. **Specify the output format**: define structure (bullet list, JSON, markdown table, numbered steps), length (max 200 words, exactly 3 items), and tone (formal, conversational, terse). For structured data, provide a schema or template.

5. **Add constraints and edge cases**: what the model must NOT do is often as important as what it should do. "Do not include implementation details. Do not ask clarifying questions. If the answer is unknown, say so explicitly rather than guessing."

6. **Include few-shot examples** for complex or format-sensitive tasks: provide 2–3 input/output pairs that demonstrate the desired behavior. Examples are the most reliable way to communicate subtle formatting, tone, and scoping requirements.

7. **Add chain-of-thought instruction** for reasoning-heavy tasks: "Think step by step before answering" or "First identify the relevant factors, then calculate, then state your conclusion." For Claude specifically, extended thinking mode handles this automatically for supported tasks.

8. **Test with adversarial inputs**: try edge cases — empty input, ambiguous input, input that is out of scope, input designed to produce the wrong format. Iterate until the prompt handles all cases correctly.

9. **Measure consistency**: run the same prompt 5–10 times on the same input. High-quality prompts produce consistent outputs. High variance indicates the task specification is still ambiguous.

## Rules

- Longer is not better. Every extra sentence in a prompt is a potential source of conflict or confusion. Add only what changes the output.
- Put the most important instructions at the beginning and end of the prompt. LLMs exhibit primacy and recency effects — instructions buried in the middle of long prompts are more likely to be ignored.
- Use XML tags for long prompts with distinct sections (Anthropic recommendation): `<context>`, `<task>`, `<format>`, `<examples>`. This reduces parsing errors on long prompts.
- For Claude: use `<thinking>` or extended thinking for multi-step reasoning tasks. Do not ask the model to "think step by step" in the user turn when the system prompt already handles reasoning structure.
- Never use vague qualifiers in format instructions: not "be concise" but "respond in 3 sentences or fewer." Not "use appropriate formatting" but "respond in a markdown table with columns: Name, Type, Description."
- Test prompts against the weakest model you plan to deploy on. A prompt that only works on Opus/GPT-4 is a liability if you later need to cut costs.

## Examples

**Prompt (bad):**
```
Summarize this article and make it good.
```

**Prompt (good):**
```xml
<role>You are a technical editor writing for software engineers with 5+ years of experience.</role>

<task>Summarize the article below in exactly 3 bullet points. Each bullet must be one sentence. Focus on: (1) the core claim, (2) the evidence, (3) the practical implication for engineers.</task>

<constraints>
- Do not include opinions or evaluations.
- Do not use marketing language.
- If the article lacks sufficient evidence for a claim, note that in the evidence bullet.
</constraints>

<article>
{{ARTICLE_TEXT}}
</article>
```

**Few-shot example structure:**
```
Input: "The deployment failed at 2am."
Output: {"severity": "high", "category": "deployment", "time_of_day": "off-hours"}

Input: "User reported slow load times on the dashboard."
Output: {"severity": "medium", "category": "performance", "time_of_day": "unknown"}

Now classify this input: "{{NEW_INPUT}}"
```

## Common Mistakes

- **Asking multiple questions in one prompt:** "Summarize this, then classify it, then suggest improvements." This produces worse results than three focused prompts. Chain prompts for complex multi-step tasks.
- **No output format specification:** Without explicit format, the model chooses. This produces inconsistent structure that breaks downstream parsing.
- **Contradictory instructions:** "Be thorough but keep it short" forces the model to choose. Resolve the contradiction before prompting: "Respond in exactly 150 words."
- **Relying on examples alone without explicit instructions:** Few-shot examples guide format but rarely communicate constraints. State constraints explicitly even when examples show them implicitly.
- **Testing only happy-path inputs:** Prompts that work on clean inputs often fail on real-world inputs with typos, multiple languages, missing data, or out-of-scope content. Always test edge cases before deploying.
- **Skipping iteration:** First-draft prompts are rarely optimal. Treat prompt design as an engineering discipline with a test suite, not a one-shot creative act.
