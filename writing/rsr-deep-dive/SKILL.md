---
name: rsr-deep-dive
version: 1.0.0
description: Run a structured, multi-source deep-research loop on a question until the answer stops changing.
author: matrixx0070
tags: [research, deep-research, multi-source, investigation, loop]
capabilities: []
---

# Deep Dive

## When to use
Reach for this when a question is open-ended enough that one search won't settle it — you need to decompose it, pull from several independent sources, and iterate until new sources stop moving the answer. Use it for "what's the state of X", "why did Y happen", or "how do the experts differ on Z".

**Not for:** looking up a single fact from a source you already trust (just answer it); verifying one discrete claim (use rsr-fact-check); grading one source in isolation (use rsr-source-eval); or writing the final stakeholder deliverable (use rsr-brief).

## Method
1. **Frame the question.** Restate it in one sentence and list the 3-5 sub-questions that must be answered for it to be resolved. *Decision:* if the question is ambiguous or unscoped, pin down scope (time range, geography, definition) before searching.
2. **Set a stop rule.** Pick a budget: max rounds (e.g. 3) or "stop when a round adds no new claims." Write it down so you don't loop forever.
3. **Round of search.** For each open sub-question, query 2-3 independent sources — prefer primary and diverse origins over echoes of one press release.
4. **Extract and tag.** Pull each claim with its source and date. Mark it Confirmed (2+ independent), Single-source, or Contested.
5. **Find the gaps.** *Decision:* if a sub-question is still Single-source or Contested and you have rounds left, run another targeted round on just that gap. Otherwise stop.
6. **Assemble.** Answer each sub-question, then the top question, flagging what stayed unresolved.

## Example
Question: "Is the EU AI Act's ban on real-time facial recognition already in force?" Sub-questions: (a) enactment date, (b) which provisions phase in when, (c) exceptions. Round 1: official EUR-Lex text confirms staggered application; a news source claims "already banned." Contested. Round 2: EUR-Lex Article on entry-into-application dates resolves it — prohibitions apply 6 months after entry into force, not day one. You answer with the phased date and note the news source oversimplified.

## Pitfalls
- Treating three articles that all cite one press release as three sources — that's one source.
- No stop rule, so you either quit after one search or loop indefinitely.
- Answering the headline question while leaving a load-bearing sub-question unresolved and unflagged.
- Letting the first plausible answer anchor you, then only searching for confirmation.

## Output format
```
Question: <one sentence>
Stop rule: <rounds or convergence criterion> — stopped after <n> rounds

Findings by sub-question:
- <sub-q>: <answer> [Confirmed | Single-source | Contested] (sources: A, B)
- ...

Bottom line: <2-3 sentences answering the top question>
Open gaps: <what stayed unresolved and why>
Sources: <numbered list with dates>
```
