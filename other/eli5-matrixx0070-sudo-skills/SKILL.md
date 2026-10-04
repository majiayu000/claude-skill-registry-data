---
name: eli5
version: 1.0.0
description: Explain any concept in plain words with one concrete analogy - clear enough for a smart child or a busy outsider, never condescending, never wrong.
triggers:
  - eli5
  - explain like i am five
  - explain this simply
  - simple explanation
  - break this down for me
capabilities: []
inputs:
  - name: concept
    required: true
    description: The concept, text, or question to explain simply.
  - name: audience
    required: false
    description: Optional real audience (e.g. "my mom", "a new intern") to calibrate tone.
---

# ELI5

## When to use
Use this when someone needs to *get* an idea fast without the vocabulary of the field: a smart child, a new intern, a client, a busy executive. The goal is an explanation they instantly grasp using one strong everyday analogy.

**Not for:** cases where precision is the point - legal wording, medical dosing, exact API contracts, or step-by-step instructions someone will follow literally. Simplifying those can make them dangerously wrong. Also not for readers who already know the field and want depth; ELI5 will feel like a waste of their time.

## Method
1. **Find the ONE thing** the person actually needs to understand. Resist explaining everything; pick the load-bearing idea.
2. **Choose one analogy from daily life** - kitchen, traffic, money, school, weather. *Decision point:* if you find yourself reaching for a second metaphor, stop; one carried all the way through beats three half-built ones.
3. **Answer first if it is a question.** Put the takeaway in the opening sentence, then explain.
4. **Explain in order:** what it is, why it matters, how it works, what would go wrong without it.
5. **Translate every technical term inline** in plain words, or drop the term. *Decision point:* if simplifying lost something true, add one "The fine print:" line at the end naming what you smoothed over - do not let the simple version become false.
6. **Close with a bolded one-sentence takeaway** they could repeat to someone else.

## Example
**Input:** What is DNS?

**Output:**
DNS is the internet's phone book. You know your friend's name, not their phone number - your phone looks the number up for you. Same thing: you type a website's name, and DNS quietly finds the numeric address computers actually use.

Why it matters: without it you would have to memorize strings like 142.250.72.14 instead of just google.com.

**Takeaway: DNS turns names people remember into numbers computers need.**

The fine print: real DNS is a chain of lookups with caching along the way, not one single book.

## Pitfalls
- **Metaphor pileup.** Switching analogies mid-explanation forces the reader to rebuild the mental model each time.
- **Sneaky jargon.** Leaving a term like "resolve" or "endpoint" unexplained because it feels basic to you.
- **Condescension.** "It's really easy!" and baby talk insult the reader; simplify the idea, not the person.
- **True-to-false drift.** Cutting a qualifier so the tidy version is now wrong. Guard it with the fine print line.

## Output format
```
<One-sentence direct answer, if the input was a question.>

<2-5 short paragraphs carrying a single analogy: what it is,
why it matters, how it works, what breaks without it.>

**Takeaway: <one memorable sentence.>**

The fine print: <one line, only if precision was lost.>
```
