---
name: reach-grammar-check
description: Fixes grammar, spelling and punctuation only, with every change listed before and after with the rule, fixes that could change your meaning asked as questions, and your wording, tone and length left alone. Use for "run reach-grammar-check", "grammar check", "check my grammar", "fix typos only", "proofread without rewriting", "spelling check", "do not change my words", "clean up my message", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Grammar Check

## When To Use
You want it clean without it stopping sounding like you. The message is written and the substance is checked. This answers: what is wrong with the grammar, spelling and punctuation, and nothing more?

## When Not To Use
If you want to know whether the message is specific, warm or too pushy, use Message Checklist; this skill does not judge substance. If you want it rewritten, this is the wrong skill by design: a rewrite would no longer be your message.

## Inputs
- Your message, exactly as you would send it.
- The language and spelling you use, for example British or American English.
- Names, terms and deliberate informal touches to leave alone.
If you have none of this, I start from the message alone, assume the spelling it already mostly uses, and say so.

## Approach
A grammar-only edit that shows every change, described generically. The scope is narrow on purpose: grammar, spelling, punctuation, agreement and plain typos. The judgement is in what to leave alone. The failure it prevents is the editor that "just tidies" and quietly swaps your words for smoother ones, until your message sounds like every other message in the reader's inbox.

## Workflow
1. Ask at most three questions: the language and spelling, any names or terms to leave as they are, and any informal touches that are deliberate.
2. Read the message for errors in scope only: grammar, spelling, punctuation, agreement, plain typos.
3. Leave everything else: word choice, word order, tone, length, formality, the number of sentences. A fragment or a casual "Hi" is your style, not an error.
4. List every change: line, before, after, and the rule in a few words. No change is silent.
5. Where a fix could change your meaning (an ambiguous comma, a name, a word that may be intended), list it as a question and do not apply it.
6. Give the corrected message once, with only the listed changes applied. You accept or reject each one.
7. If there are no errors, say so and change nothing.

## Output Format
```markdown
# Grammar Changes
Language and spelling: [as you said, or as assumed] | Left alone on purpose: [names, terms, informal touches]
## Changes applied
| # | Line | Before | After | Rule |
|---|---|---|---|---|
| 1 | [line no.] | [text] | [text] | [a few words] |
## Questions (not applied)
| # | Line | Text | Possible fix | Why it was not applied |
|---|---|---|---|---|
| 1 | [line no.] | [text] | [fix] | [could change your meaning] |
## Corrected message
[Your message with only the changes above applied.]
## Decision
[Your name] accepts or rejects each change and answers each question, by [date].
```

## Done When
- Every difference between your message and the corrected one appears in the changes table.
- No word was swapped for style, and the length is unchanged apart from fixes.
- Every fix that could change meaning is a question, not applied.
- The message is not stored or reused for anything else.

## Quality Bar
- A rule is named for every change; "reads better" is not a rule.
- Names, titles and terms are checked against what you gave, never guessed.
- Your voice outranks a textbook preference where both are correct.
- No comment on substance, tone or whether to send.
- Grammar only, every change shown; the words stay yours and you send the message.

## Next
Run reach-outreach-rules-check (Outreach Rules Check) to see which rules questions this message raises.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
