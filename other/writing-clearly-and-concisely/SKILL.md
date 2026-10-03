---
name: writing-clearly-and-concisely
description: Use when writing prose humans will read—documentation, commit messages, error messages, explanations, reports, or UI text. Applies Strunk's timeless rules for clearer, stronger, more professional writing.
---

# Writing Clearly and Concisely

## Overview

Write with clarity and force. This skill covers what to do (Strunk) and what not to do (AI patterns).

## Limited Context Strategy

When context is tight:

1. Write your draft using judgment
2. If native delegation is available, assign a **read-only review role** the draft and one relevant section file
3. Have that role return a copyedited revision without writing files; the main context accepts or adjusts it
4. If delegation is unavailable, load that one section and perform the copyedit sequentially in the main context

Loading a single section (~1,000-4,500 tokens) instead of everything saves significant context.
Use the current CLI's built-in explorer/reviewer; do not require a custom agent name or vendor-specific task schema.

## Elements of Style

William Strunk Jr.'s *The Elements of Style* (1918) is the reference. The rules most violated in practice:

- **Use active voice** — passive buries the agent and weakens sentences
- **Put statements in positive form** — "he was not honest" → "he was dishonest"
- **Use definite, specific, concrete language** — vague nouns and abstract claims lose readers
- **Omit needless words** — every word should do work
- **Place emphatic words at end of sentence** — the last word is the most memorable position

For complete rules with examples, load the relevant section:

| Section | File | ~Tokens |
|---------|------|---------|
| Grammar, punctuation, comma rules | `02-elementary-rules-of-usage.md` | 2,500 |
| Paragraph structure, active voice, concision | `03-elementary-principles-of-composition.md` | 4,500 |
| Headings, quotations, formatting | `04-a-few-matters-of-form.md` | 1,000 |
| Word choice, common errors | `05-words-and-expressions-commonly-misused.md` | 4,000 |

**Most tasks need only `03-elementary-principles-of-composition.md`** — it covers active voice, positive form, concrete language, and omitting needless words.

## AI Writing Patterns to Avoid

LLMs regress to statistical means, producing generic, puffy prose. Avoid:

- **Puffery:** pivotal, crucial, vital, testament, enduring legacy
- **Empty "-ing" phrases:** ensuring reliability, showcasing features, highlighting capabilities
- **Promotional adjectives:** groundbreaking, seamless, robust, cutting-edge
- **Overused AI vocabulary:** delve, leverage, multifaceted, foster, realm, tapestry
- **Formatting overuse:** excessive bullets, emoji decorations, bold on every other word

Be specific, not grandiose. Say what it actually does.

For comprehensive research on why these patterns occur, see `signs-of-ai-writing.md`. Wikipedia editors developed this guide to detect AI-generated submissions — their patterns are well-documented and field-tested.

## Bottom Line

Writing for humans? Load the relevant section from `elements-of-style/` and apply the rules. For most tasks, `03-elementary-principles-of-composition.md` covers what matters most.
