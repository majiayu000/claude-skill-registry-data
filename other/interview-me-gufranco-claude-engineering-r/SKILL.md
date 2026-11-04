---
name: interview-me
description: One-question-at-a-time intent clarification for underspecified or ambiguous asks. Drives toward 95%+ intent confidence before any implementation. Use when user says "interview me", "grill me", "are we sure?", "stress-test my thinking", or when the request is too vague to act on without guessing. Use only while the request is underspecified; a concretely specified task proceeds straight to the work.
argument-hint: "/interview-me [topic]"
allowed-tools: "Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill"
sensitive: false
---

Structured intent-clarification interview. Forces one question at a time, with each subsequent question shaped by the previous answer, until the model can describe the work in three sentences without ambiguity.

## Overview

When a task is underspecified, the cost of one clarifying question is near zero compared to the cost of wrong-direction work. This skill formalizes the interview: it caps questions per turn at one, requires self-investigation between turns, and exits only when a Confidence Score reaches 9/10 or higher.

## When to Use

- User says "interview me", "grill me", "stress-test", "are we sure?"
- The ask uses vague verbs: "improve", "clean up", "fix", "simplify", "modernize"
- Multiple plausible interpretations exist and the model is about to guess
- Before starting non-trivial work where the cost of wrong direction is high
- After a partial implementation, when the user shifts scope mid-task

Do NOT use when:
- The user has named specific files, functions, or behavior
- The task is small enough that exploratory implementation is cheaper than clarification
- A `/plan` is already approved (use the plan, not the interview)

## Process

1. **Confidence baseline.** State current confidence as a number from 1 to 10 with one sentence each on what is known and what is unknown.
2. **Self-investigate first.** Before asking, spend up to one minute on read-only investigation: grep, glob, read named files. Resolve anything that can be resolved without the user.
3. **Ask one question.** First line is the question, worded so that "yes" accepts the recommended option. Second block names what was investigated, with paths. Third block lists 2 to 3 options with one decisive trade-off each; the recommended option comes first, its label ends with `(Recommended)`, and one sentence gives the decisive reason. Use `AskUserQuestion` for the question, not free-text prose.
   - When the question tests a domain term or a relationship between concepts, ground it in a concrete edge-case scenario invented for the purpose, such as "an order is half shipped when the customer cancels: is that one cancellation or two?" A scenario forces the boundary between concepts into the open where a definition lets it blur.
   - When talk cannot settle the question, as with how a screen should look or how a state model behaves across awkward cases, stop asking and call the Skill tool with `spike`, passing the question. Its verdict becomes the answer, and the interview resumes from step 4.
4. **Update confidence.** After the answer, restate confidence. If still below 9/10, repeat from step 2.
5. **Summarize.** When confidence reaches 9/10 or higher, write a three-sentence task statement: what will be done, what will NOT be done, how done will be verified. Wait for explicit "yes" before any implementation.

## When the project has a glossary

Before the first question, check for `GLOSSARY.md` at the project root, or `GLOSSARY-INDEX.md` pointing at per-context glossaries. See [`../../rules/project-glossary.md`](../../rules/project-glossary.md).

When a glossary exists:

- Load every term and its `Avoid` clause before asking anything.
- Phrase every question using the glossary's canonical terms.
- When the user uses a word listed under `Avoid`, call it out: "the glossary lists `<canonical>` for that concept and `<word-the-user-said>` under `Avoid`. Are we talking about the same thing, or has the meaning shifted?".
- When the user introduces a new term that has no entry, propose adding it inline. Update `GLOSSARY.md` with the Edit tool before continuing, creating it with Write on the first real term. Glossary edits are the only writes this skill makes before the task statement is approved.
- When the user's intent contradicts what the code does, surface it: "the glossary and the code both treat X as Y. You described it as Z. Which is the truth now?".

## When to offer an ADR

Offer to record an Architecture Decision Record only when all three are true:

1. The decision is hard to reverse. Switching it later would cost real time.
2. The decision will look surprising without context. A future reader will ask "why did they do it this way?".
3. The decision is the result of a real trade-off. There were genuine alternatives and the user picked one for specific reasons.

If any one is missing, skip the ADR. Do not bury easy-to-change calls in the ADR record. Do not record the obvious.

## Common Rationalizations

- "The ask is clear enough": restate it in three sentences. If two are about what the user did NOT say, it is not clear.
- "I will figure it out as I go": wrong-direction work is the most expensive mistake. The interview costs minutes; a refactor costs hours.
- "Asking too many questions is annoying": one well-formed question is not annoying. Five rapid-fire questions are. This skill caps at one per turn.
- "The user said `just do it`": that triggers execute-mode per CLAUDE.md, NOT this skill. Honor the directive.

## Red Flags

- About to invoke `Write` or `Edit` without a confidence score
- About to ask two questions in one turn
- Offering options with no recommendation, or a recommendation that is not listed first
- Asking a question whose answer is in the first file the user named
- Skipping the self-investigation step because "the user knows"
- Writing implementation code while confidence is below 8/10
- Restating the user's words back as a question instead of resolving them

## Verification

- Final task statement is three sentences: what, what-not, how-verified
- User has answered "yes" to the statement, not "ok" or "sure"
- Every question asked was preceded by at least one read or grep
- No question was bundled with another
- Every question carried a recommended option, listed first and labeled `(Recommended)`
- Confidence score documented before and after each round
