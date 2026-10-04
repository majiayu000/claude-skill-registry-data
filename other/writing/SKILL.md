---
name: writing
description: Rewrite text that did not land, with clear context, plain language, and my writing preferences.
argument-hint: "[text, file, or feedback; omit for the last agent response]"
disable-model-invocation: true
---

# Writing

Rewrite the supplied text or named passage. With no target, rewrite the last substantive agent response. Treat feedback as direction for the rewrite; infer the target and audience from the conversation. Ask only when the target or intended meaning cannot be determined.

## Rebuild the explanation

Work out what the reader needs to understand and where the original lost them. Supply the missing context before the conclusion that depends on it. For project explanations, use the domain terms in `CONTEXT.md`; if `CONTEXT-MAP.md` exists, follow it to the relevant context. Read only what the explanation needs.

For technical English, use the clarity principles of ASD-STE100: familiar words, stable terminology, explicit actors, and short sentences with one main idea. Preserve necessary technical detail and explain unfamiliar terms. Treat this as a readability guide, not a claim of formal standards compliance. Apply the same clarity in the conversation's language.

Preserve facts, qualifications, links, identifiers, and the author's intended stance. Correct an error when the available evidence supports the correction. Keep uncertainty visible; never invent evidence, measurements, sources, or examples presented as facts to make a sentence more convincing.

## Remove formulaic writing

Replace inflated claims, sales adjectives, vague authority, and decorative metaphors with specific facts or actions. Name the mechanism instead of describing a feeling. Cut clauses that merely announce significance and conclusions that add no information.

Use ordinary verbs and consistent names. Remove filler, stacked hedges, forced contrasts, artificial triplets, synonym rotation, and meaningless ranges. Prefer active voice when the actor matters. Split sentences that require rereading. Keep useful nuance and natural variation in sentence length.

## My preferences

Lead with the useful point. End when the content ends; skip closing summaries, offers to help further, praise, and claims about the quality of your answer. Prefer connected prose; use headings, bullets, and bold only when they help the reader navigate.

Tone: calm, direct, opinionated when a judgment is called for. Avoid ceremonial openings, forced enthusiasm, sales language, and formulaic contrasts. Explain what matters in concrete terms.

Typography: no em dashes, en dashes, or hyphens used as dashes; do not substitute parenthetical asides. Colons only before lists or examples. Avoid semicolon chains. Use straight quotes and sentence case headings. No emoji or bolded proper nouns.

When drafting in my voice, infer it from my own wording and representative samples, not pasted or generated material. Preserve my stance and relationship to the reader. Do not manufacture anecdotes, emotions, slang, commitments, or mistakes to sound human.

Use the language of the conversation and a register that fits the audience and medium. In Czech, I prefer natural professional speech to official or corporate phrasing. Keep established English terms when they are clearer for the reader.

## Finish

Read the revision as the intended reader. Check that the point is understandable without reconstructing omitted context, the meaning is intact, and each sentence earns its place. Fix remaining generic or mechanical phrasing without adding personality the author did not supply.

For a requested rewrite or drafted message, return the text alone unless I ask for commentary or a material uncertainty prevents completion. If explicitly asked to edit a file, apply the rewrite there and briefly report the change. A rewrite request does not authorize sending or publishing the text.

Adapted from [unslop](https://github.com/backnotprop/pstack/blob/main/skills/unslop/SKILL.md), [wait-what](https://github.com/mattpocock/skills/blob/main/skills/productivity/wait-what/SKILL.md), and the former local writing preferences document.
